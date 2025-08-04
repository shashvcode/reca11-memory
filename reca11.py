import requests
BASE_URL = "https://reca11-memory.onrender.com"

class Reca11:
    def __init__(self, api_key: str, openai_key: str, project_name: str):
        self.api_key = api_key
        self.openai_key = openai_key
        self.project_name = project_name
        self._create_project_or_fail()

    def _create_project_or_fail(self):
        payload = {
            "api_key": self.api_key,
            "project_name": self.project_name
        }
        response = requests.post(f"{BASE_URL}/project/create", json=payload)

        if response.status_code == 400:
            detail = response.json().get("detail", "")
            if "already exists" in detail.lower():
                raise ValueError("Duplicate project name. Please choose a unique name.")
            raise RuntimeError(f"Project creation failed: {detail}")

        elif response.status_code != 200:
            raise RuntimeError(f"Unexpected error during project creation: {response.text}")

    def recall(self, chat_pair: dict):
        payload = {
            "api_key": self.api_key,
            "openai_key": self.openai_key,
            "project_name": self.project_name,
            "chat_pair": chat_pair
        }
        response = requests.post(f"{BASE_URL}/recall", json=payload)

        if response.status_code == 400:
            detail = response.json().get("detail", "Bad request.")
            raise ValueError(f"Recall failed: {detail}")
        elif response.status_code != 200:
            raise RuntimeError(f"Unexpected recall failure: {response.status_code} - {response.text}")

        return response.json()