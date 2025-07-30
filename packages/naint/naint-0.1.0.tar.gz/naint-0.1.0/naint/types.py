from enum import Enum
from pydantic import BaseModel
from typing import Optional


class OutputFormat(str, Enum):
    wav_44100 = "wav_44100"


class VoiceSettings(BaseModel):
    speed: Optional[float] = 1.0
    # emotion: Optional[str] = "neutral" ### TODO: Add emotion
    reverb: Optional[bool] = False


class Voice(BaseModel):
    voice_id: str
    name: str
    description: Optional[str]
    settings: Optional[VoiceSettings]