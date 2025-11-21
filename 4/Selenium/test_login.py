from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
import time
import os

# Function to test login with a browser
def test_login(browser_name):
    if browser_name == 'chrome':
        # Assume chromedriver.exe is in the current directory or PATH
        service = ChromeService(executable_path=os.path.join(os.getcwd(), 'chromedriver.exe'))
        driver = webdriver.Chrome(service=service)
    elif browser_name == 'firefox':
        # Assume geckodriver.exe is in the current directory or PATH
        service = FirefoxService(executable_path=os.path.join(os.getcwd(), 'geckodriver.exe'))
        driver = webdriver.Firefox(service=service)
    else:
        print("Unsupported browser")
        return

    driver.get("file:///c:/Users/lvpei/Desktop/test/4/Selenium/login.html")
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    username.send_keys("testuser")
    password.send_keys("testpass")
    password.send_keys(Keys.RETURN)
    time.sleep(2)
    # Check if login successful (for simplicity, just print title)
    print(f"Page title after login: {driver.title}")
    driver.quit()

# Test with Chrome
try:
    test_login('chrome')
except Exception as e:
    print(f"Chrome test failed: {e}")

# Test with Firefox
# try:
#     test_login('firefox')
# except Exception as e:
#     print(f"Firefox test failed: {e}")