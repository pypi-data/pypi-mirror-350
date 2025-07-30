
import httpx
from .text_to_speech import TextToSpeechClient
from .speech_to_text import SpeechToTextClient
from .voices import VoicesClient

class AsyncNAINT:
    def __init__(self, api_key: str, base_url: str = "http://0.0.0.0:8010/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"x-api-key": self.api_key}
        )
        self.text_to_speech = TextToSpeechClient(self._client)
        self.voices = VoicesClient(self._client)
        self.speech_to_text = SpeechToTextClient(self._client)
