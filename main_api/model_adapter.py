import requests
import os


class ModelAdapter:
    domain = os.getenv("MODEL_DOMAIN")

    def summarize(self, text: str) -> str:
        endpoint = "/summarize"
        url = self.domain + endpoint
        response = requests.get(url, json={"text": text})
        if response.status_code != 200:
            raise Exception(f"Failed to summarize text: {response.text}")
        return response.json()["summary"]
