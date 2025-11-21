"""Playwright-style Selenium smoke tests for a generic web login form.

Usage
-----
1. Update BASE_URL and locator values to match the target application under test.
2. (Optional) Adjust TEST_CASES to mirror relevant positive and negative flows.
3. Install dependencies once: ``pip install pytest selenium webdriver-manager``.
4. Execute the suite and create both HTML and JSON reports:
   ``pytest 1.py --html=reports/login_pytest_report.html --self-contained-html``

High-level test coverage
------------------------
- ``TC01`` Valid username and password → expect success banner.
- ``TC02`` Valid username with wrong password → expect authentication failure message.
- ``TC03`` Unknown username → expect account not found message.
- ``TC04`` Empty credentials submission → expect required-field validation.
- ``TC05`` Potential injection payload → expect safe rejection with no stack trace.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class LoginTestCase:
	name: str
	username: str
	password: str
	expected_success: bool
	expected_message: str
	notes: Optional[str] = None


TEST_CASES: List[LoginTestCase] = [
	LoginTestCase(
		name="TC01_valid_login",
		username="standard_user",
		password="secret_password",
		expected_success=True,
		expected_message="Login successful",
		notes="Baseline happy path with active account.",
	),
	LoginTestCase(
		name="TC02_invalid_password",
		username="standard_user",
		password="wrong_password",
		expected_success=False,
		expected_message="Invalid credentials",
		notes="Wrong password should trigger authentication error banner.",
	),
	LoginTestCase(
		name="TC03_unknown_user",
		username="ghost_user",
		password="any_password",
		expected_success=False,
		expected_message="Account does not exist",
		notes="Unknown user id should not reveal which field failed.",
	),
	LoginTestCase(
		name="TC04_blank_fields",
		username="",
		password="",
		expected_success=False,
		expected_message="Username is required",
		notes="Form-level validation for empty submission.",
	),
	LoginTestCase(
		name="TC05_sql_injection_attempt",
		username="' OR 1=1 --",
		password="anything",
		expected_success=False,
		expected_message="Invalid credentials",
		notes="Ensure defensive coding against injection-style payloads.",
	),
]


def _build_reports_dir() -> Path:
	reports_dir = Path("reports")
	reports_dir.mkdir(parents=True, exist_ok=True)
	(reports_dir / "screenshots").mkdir(parents=True, exist_ok=True)
	return reports_dir


class ResultRecorder:
	"""Collects per-test run data for later aggregation."""

	def __init__(self) -> None:
		self.records: List[Dict[str, object]] = []

	def add(
		self,
		*,
		case: LoginTestCase,
		actual_message: str,
		passed: bool,
		screenshot_path: Optional[Path],
	) -> None:
		entry = {
			**asdict(case),
			"timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
			"actual_message": actual_message,
			"passed": passed,
			"screenshot": str(screenshot_path) if screenshot_path else None,
		}
		self.records.append(entry)

	def write(self) -> None:
		if not self.records:
			return
		reports_dir = _build_reports_dir()
		json_path = reports_dir / "login_test_results.json"
		json_path.write_text(
			json.dumps(self.records, indent=2),
			encoding="utf-8",
		)
		summary_path = reports_dir / "login_test_summary.md"
		summary_lines = [
			"# Login Test Report",
			f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
			"",
			"| Test Case | Status | Expected | Actual | Screenshot |",
			"|-----------|--------|----------|--------|------------|",
		]
		for record in self.records:
			status = "✅ PASS" if record["passed"] else "❌ FAIL"
			screenshot = record["screenshot"] or ""
			summary_lines.append(
				f"| {record['name']} | {status} | {record['expected_message']} | "
				f"{record['actual_message']} | {screenshot} |"
			)
		summary_path.write_text("\n".join(summary_lines), encoding="utf-8")


@pytest.fixture(scope="session")
def base_url() -> str:
	return "https://example.com/login"  # TODO: replace with target login page


@pytest.fixture(scope="session")
def locators() -> Dict[str, tuple]:
	return {
		"username": (By.ID, "user-name"),
		"password": (By.ID, "password"),
		"submit": (By.CSS_SELECTOR, "button[type='submit']"),
		"banner": (By.CSS_SELECTOR, "#flash"),
	}


@pytest.fixture(scope="session")
def result_recorder() -> Iterable[ResultRecorder]:
	recorder = ResultRecorder()
	yield recorder
	recorder.write()


@pytest.fixture
def driver() -> Iterable[webdriver.Chrome]:
	chrome_options = Options()
	chrome_options.add_argument("--headless=new")
	chrome_options.add_argument("--window-size=1280,720")
	service = Service(ChromeDriverManager().install())
	driver_instance = webdriver.Chrome(service=service, options=chrome_options)
	yield driver_instance
	driver_instance.quit()


def perform_login(
	driver_instance: webdriver.Chrome,
	*,
	base_url: str,
	locators: Dict[str, tuple],
	username: str,
	password: str,
) -> str:
	driver_instance.get(base_url)
	driver_instance.find_element(*locators["username"]).clear()
	driver_instance.find_element(*locators["username"]).send_keys(username)
	driver_instance.find_element(*locators["password"]).clear()
	driver_instance.find_element(*locators["password"]).send_keys(password)
	driver_instance.find_element(*locators["submit"]).click()
	try:
		banner_element = driver_instance.find_element(*locators["banner"])
		return banner_element.text.strip()
	except NoSuchElementException:
		return ""


def capture_screenshot(driver_instance: webdriver.Chrome, *, test_name: str) -> Path:
	reports_dir = _build_reports_dir()
	screenshot_path = (
		reports_dir / "screenshots" / f"{test_name}_{datetime.utcnow().timestamp():.0f}.png"
	)
	driver_instance.save_screenshot(str(screenshot_path))
	return screenshot_path


@pytest.mark.parametrize("test_case", TEST_CASES, ids=lambda case: case.name)
def test_login_flow(
	test_case: LoginTestCase,
	driver: webdriver.Chrome,
	base_url: str,
	locators: Dict[str, tuple],
	result_recorder: ResultRecorder,
) -> None:
	actual_message = perform_login(
		driver,
		base_url=base_url,
		locators=locators,
		username=test_case.username,
		password=test_case.password,
	)
	expected_met = test_case.expected_message in actual_message
	passed = expected_met
	screenshot_path = None
	if not passed:
		screenshot_path = capture_screenshot(driver, test_name=test_case.name)
	result_recorder.add(
		case=test_case,
		actual_message=actual_message,
		passed=passed,
		screenshot_path=screenshot_path,
	)
	assert expected_met, (
		f"{test_case.name} expected message '{test_case.expected_message}' but got"
		f" '{actual_message}'"
	)

