
import httpx
from .text_to_speech import TextToSpeechClient, AsyncTextToSpeechClient
from .speech_to_text import SpeechToTextClient, AsyncSpeechToTextClient
from .voices import VoicesClient


class NAINT:
    def __init__(self, api_key: str, base_url: str = ""):
        self.api_key = api_key
        self.base_url = base_url
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"x-api-key": self.api_key}
        )
        self.text_to_speech = TextToSpeechClient(self._client)
        self.voices = VoicesClient(self._client)
        self.speech_to_text = SpeechToTextClient(self._client)


class AsyncNAINT:
    def __init__(self, api_key: str, base_url: str = ""):
        self.api_key = api_key
        self.base_url = base_url
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"x-api-key": self.api_key}
        )
        self.text_to_speech = AsyncTextToSpeechClient(self._client)
        self.speech_to_text = AsyncSpeechToTextClient(self._client)
        ### Sync
        self.voices = VoicesClient(httpx.Client(
            base_url=self.base_url,
            headers={"x-api-key": self.api_key}
        ))