from itertools import count
from typing import Any, Dict

from locust import HttpUser, constant, task

_user_sequence = count(1)


class RegistrationUser(HttpUser):
    wait_time = constant(0)

    @task
    def register(self) -> None:
        sequence = next(_user_sequence)
        payload: Dict[str, Any] = {
            "username": f"loadtest_user_{sequence}",
            "password": "Passw0rd!",
        }
        self.client.post("/register", json=payload, name="register")
