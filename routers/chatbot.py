from fastapi import APIRouter

from controller import ChatBotController
from model import Message

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/talk")
async def talk(message: Message):
    return ChatBotController.getResponse(message)


