from fastapi import APIRouter

from model import Message, Audio
from controller import AudioController

router = APIRouter(prefix="/audio", tags=["audio"])

@router.post("/")
async def getAudio(message: Message):
    return AudioController.getAudio(message)

@router.post("/transcribe")
async def getMessage(audio: Audio):
    return AudioController.getMessage(audio)