import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import ChatSession 

from model import Message, MessageBot
from controller import UserController
from model import UserUtils

from random import randint
from dotenv import load_dotenv
import os

load_dotenv()

class Controller:
    
    PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
    LOCATION = os.getenv("GOOGLE_LOCATION")
    MODEL_ID = os.getenv("GOOGLE_MODEL_ID")
    
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    TEMPLATE = "Eres un asesor financiero que deseas que tu cliente salde sus cuentas con la empresa. Tienes que ser pasivo pero firme. Limitate a conversar con el cliente sobre su vida crediticia, nada fuera de lo común. Antes de cada consulta del cliente se te compartira información sobre el, esta vendra en formato json. Apartir de la siguiente consulta hablaras con el cliente."
    
    MODEL = GenerativeModel(MODEL_ID, system_instruction=TEMPLATE)
    
    CHAT = MODEL.start_chat()
    
    @classmethod
    def getResponse(cls, message : Message) -> MessageBot:
        """Get the response from the chat bot

        Args:
            message (Message): Message to send to the bot

        Returns:
            MessageBot: Response from the bot
        """
        client = UserUtils.to_json(UserController.getUserById(message.userId))
        message =f"Información del cliente:\n{client}\nMensaje del cliente\n{message.message}"
        response = cls.CHAT.send_message()
        return MessageBot(id = randint(1,99999), createdAt = response.timestamp, userId = message.userId, response = response.text)
    
    
    
    
    
    