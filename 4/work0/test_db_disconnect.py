import pytest
import requests
import subprocess
import time

def simulate_db_disconnect():
    subprocess.run(["docker", "stop", "your_database_container_name"])

def test_payment_request_with_db_disconnect():
    # Start the Flask app in a separate thread or process if needed
    response = requests.post("http://localhost:5000/payment", json={"amount": 100})
    assert response.status_code == 500  # Expecting an error due to DB disconnect

    simulate_db_disconnect()
    time.sleep(5)  # Wait for a moment to simulate the disconnect

    # Attempt to recover and check if the service is back
    response = requests.post("http://localhost:5000/payment", json={"amount": 100})
    assert response.status_code == 200  # Expecting success after recovery

    # Optionally, restart the database container if needed
    subprocess.run(["docker", "start", "your_database_container_name"])