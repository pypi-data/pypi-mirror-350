
import base64
import numpy as np
from scipy.io.wavfile import write
from .types import OutputFormat, VoiceSettings


class TextToSpeechClient:
    def __init__(self, client):
        self.client = client

    def convert(self, text: str, voice_id: str, model_id: str = "naint-tts-v1",
                output_format: str = OutputFormat.wav_44100,
                voice_settings: VoiceSettings = VoiceSettings()) -> dict:
        payload = {
            "text": text,
            "model_id": model_id,
            "output_format": output_format,
            "voice_settings": voice_settings.dict()
        }
        response = self.client.post(f"/text-to-speech/{voice_id}", json=payload)
        response.raise_for_status()
        return response.json()

    def convert_to_file(self, text: str, voice_id: str, file_path: str, **kwargs):
        audio_base64 = self.convert(text, voice_id, **kwargs)['audio']
        audio_bytes = base64.b64decode(audio_base64)
        audio = np.frombuffer(audio_bytes, dtype=np.int16)
        write(file_path, 44100, audio)
        print(f"Audio saved to {file_path}")


class AsyncTextToSpeechClient:
    def __init__(self, client):
        self.client = client

    async def convert(self, text: str, voice_id: str, model_id: str = "naint-tts-v1",
                      output_format: str = OutputFormat.wav_44100,
                      voice_settings: VoiceSettings = VoiceSettings()) -> dict:
        payload = {
            "text": text,
            "model_id": model_id,
            "output_format": output_format,
            "voice_settings": voice_settings.dict()
        }
        response = await self.client.post(f"/text-to-speech/{voice_id}", json=payload)
        response.raise_for_status()
        return response.json()
    
    async def convert_to_file(self, text: str, voice_id: str, file_path: str, **kwargs):
        audio_base64 = (await self.convert(text, voice_id, **kwargs))['audio']
        audio_bytes = base64.b64decode(audio_base64)
        audio = np.frombuffer(audio_bytes, dtype=np.int16)
        write(file_path, 44100, audio)
        print(f"Audio saved to {file_path}")