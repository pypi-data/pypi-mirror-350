import io
import librosa
import soundfile as sf


class SpeechToTextClient:
    def __init__(self, client):
        self.client = client
        self.target_sample_rate = 16000

    def transcribe(self, file_path: str, model: str = "english") -> str:
        """
        Transcribe audio file to text using the specified model.

        Args:
            file_path (str): Path to the audio file to transcribe. ### MP3 is not supported
            model (str, optional): The model to use for transcription. Defaults to "english".

        Returns:
            str: The transcribed text.
        """
        audio_data, sample_rate = sf.read(file_path, dtype="float64")

        if len(audio_data.shape) > 1:
            audio_data = librosa.to_mono(audio_data.T)

        if sample_rate > self.target_sample_rate:
            audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=self.target_sample_rate)
            sample_rate = self.target_sample_rate

        buffer = io.BytesIO()
        sf.write(buffer, audio_data, samplerate=self.target_sample_rate, format="WAV")
        buffer.seek(0)

        files = {"file": ("audio.wav", buffer, "audio/wav")}
        data = {"model": model}

        response = self.client.post("/stt", files=files, data=data)
        response.raise_for_status()
        return response.json()["text"]
    

class AsyncSpeechToTextClient:
    def __init__(self, client):
        self.client = client
        self.target_sample_rate = 16000

    async def transcribe(self, file_path: str, model: str = "english") -> str:
        """
        Transcribe audio file to text using the specified model.

        Args:
            file_path (str): Path to the audio file to transcribe. ### MP3 is not supported
            model (str, optional): The model to use for transcription. Defaults to "english".

        Returns:
            str: The transcribed text.
        """
        audio_data, sample_rate = sf.read(file_path, dtype="float64")

        if len(audio_data.shape) > 1:
            audio_data = librosa.to_mono(audio_data.T)

        if sample_rate > self.target_sample_rate:
            audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=self.target_sample_rate)
            sample_rate = self.target_sample_rate

        buffer = io.BytesIO()
        sf.write(buffer, audio_data, samplerate=self.target_sample_rate, format="WAV")
        buffer.seek(0)

        files = {"file": ("audio.wav", buffer, "audio/wav")}
        data = {
            "model": model,
            "sample_rate": str(sample_rate)
        }

        response = await self.client.post("/stt", files=files, data=data)
        response.raise_for_status()
        return response.json()["text"] 