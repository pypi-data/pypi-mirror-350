from typing import List
from .types import Voice

class VoicesClient:
    def __init__(self, client):
        self.client = client

    def get_all(self) -> List[Voice]:
        response = self.client.get("/voices")
        response.raise_for_status()
        data = response.json()
        return [Voice(**v) for v in data.get("voices", [])]