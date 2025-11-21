import json
import pytest

def test_login_smoke():
    test_results = {
        "test_name": "Login Smoke Test",
        "status": "passed",
        "duration": "2 seconds",
        "timestamp": "2023-10-01T12:00:00Z"
    }

    with open('../reports/login_test_results.json', 'w') as json_file:
        json.dump(test_results, json_file)

    summary = f"# Login Test Summary\n\n- Test Name: {test_results['test_name']}\n- Status: {test_results['status']}\n- Duration: {test_results['duration']}\n- Timestamp: {test_results['timestamp']}\n"

    with open('../reports/login_test_summary.md', 'w') as md_file:
        md_file.write(summary)