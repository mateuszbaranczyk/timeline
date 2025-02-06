import requests
import os


class ModelAdapter:
    domain = os.getenv("MODEL_DOMAIN", "http://localhost:3000")

    def summarize(self, text: str) -> str:
        endpoint = "/summarize"
        url = self.domain + endpoint
        if not text:
            return ""
        response = requests.post(url, json={"text": text})
        if response.status_code != 200:
            return ""
        return response.json()["summary"]
