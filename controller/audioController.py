"""Synthesizes speech from the input string of text."""
from google.cloud import texttospeech, speech
from google.oauth2 import service_account

from fastapi import HTTPException

from datetime import datetime
import os
from dotenv import load_dotenv
from random import randint

from model import Audio, Message

load_dotenv()

path = os.getenv("GOOGLE_APPLICATION_VERTEX_AI_CREDENTIALS")

credentials = service_account.Credentials.from_service_account_file(path)


class Controller:
    
    CLIENT_TEXT = texttospeech.TextToSpeechClient()
    CLIENT_SPEECH = speech.SpeechClient()
    LANGUAGE_CODE = "es-US"
    LANGUAGE_CODE2 = "es-419"
    DEFAULT_VOICE = "es-US-Studio-B"
    SPEAKING_RATE = 1
    AUDIO_CHANNEL_COUNT = 1
    MODEL = "default"
    
    def saveAudio(bytes_ : bytes, message : str, userId : int) -> Audio:
        """Save audio from text

        Args:
            bytes (bytes): audio to save
            message (str): text to get audio
            userId (int): user id
        
        Raises:
            HTTPException: 500 if error saving audio
        
        Returns:
            Audio: audio object
        """
        
        now = datetime.now().date()
        os.makedirs(f"./static/media/audio/{userId}", exist_ok=True)
        path = f"./static/media/audio/{userId}/{now}-{randint(1,9999)}.mp3"
        audio = Audio(id=randint(1,9999),
            createdAt=now,
            message=message,
            userId=userId,
            audioPath=path
        )
        try:
            with open(path, "wb") as out:
                out.write(bytes_)
        except Exception as e:
            return HTTPException(status_code=500, detail=f"{e}")
        
        return audio
    
    def getAudio(message : Message) -> Audio:
        """Get audio from text

        Args:
            message (Message): message to get audio

        Returns:
            Audio: audio
        """
        
        input_text = texttospeech.SynthesisInput(text=message.message)

        voice = texttospeech.VoiceSelectionParams(
            language_code=Controller.LANGUAGE_CODE,
            name=Controller.DEFAULT_VOICE,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=Controller.SPEAKING_RATE
        )

        response = Controller.CLIENT_TEXT.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        return Controller.saveAudio(response.audio_content, message.message, message.userId)

    def getMessage(audio : Audio) -> Message:
        """Get message from audio

        Args:
            audio (Audio): audio to get message

        Returns:
            Message: message
        """

        with open(audio.audioPath, "rb") as audio_file:
            content = audio_file.read()

        audio_ = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=24000,
            language_code=Controller.LANGUAGE_CODE2,
            model=Controller.MODEL,
            audio_channel_count=Controller.AUDIO_CHANNEL_COUNT,
            enable_word_confidence=True,
            enable_word_time_offsets=True
            )

        operation = Controller.CLIENT_SPEECH.long_running_recognize(config=config, audio=audio_)

        response = operation.result(timeout=90)
        
        message =" ".join(result.alternatives[0].transcript for result in response.results)

        return Message(id=randint(1,99999), createdAt=datetime.now(), message=message, userId=audio.userId)