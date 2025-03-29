"""Module to define the data model for the system
"""

import datetime
from pydantic import BaseModel
from typing import Optional

# Data class

class UserP(BaseModel):
    """Class to represent a user public in the system
    """

    id : int
    name : str
    userName : str
    email : str
    phone : Optional[str]

class User(UserP):
    """Class to represent a user in the system
    """
    
    createdAt : datetime.datetime
    birthdate : datetime.datetime
    documentID : int
    password : str
    debt : float
    debtMaturityDate : datetime.datetime
    state : bool
    paymentHistory : list
    
    class Config:
        """Config class to allow the use of datetime objects
        """
        json_encoders = {
            datetime.datetime: lambda v: v.isoformat(),
            datetime.date: lambda v: v.isoformat()
        }  
        
        schema_extra = {
            "example": {
                "id": 59,
                "createdAt": "2024-01-01T00:00:00Z",
                "name": "James Smith",
                "birthdate": "1990-01-01T00:00:00Z",
                "documentID": 10371973,
                "email": "XXXXXXXXXXXXXXXX",
                "phone": "(794) 8297 -3702",
                "debt": 1000.8,
                "debtMaturityDate": "2027-01-01T00:00:00Z",
                "state": True,
                "paymentHistory": []
            }
        }
    
class Audio(BaseModel):
    """Class to represent an audio in the system
    """

    id : int
    createdAt : datetime.datetime
    userId : int
    message : str
    audioPath : str

    class Config:
        """Config class to allow the use of datetime objects
        """
        json_encoders = {
            datetime.datetime: lambda v: v.isoformat(),
            datetime.date: lambda v: v.isoformat()
        }

        schema_extra = {
            "example": {
                "id": 59,
                "createdAt": "2024-01-01T00:00:00Z",
                "message": "Hello, how are you?",
                "userId": 93,
                "audioPath": ".\..\audio.mp3"
            }
        }

class Message(BaseModel):
    """Class to represent a message in the system
    """

    id : int
    createdAt : datetime.datetime
    userId : int
    message : str

    class Config:
        """Config class to allow the use of datetime objects
        """
        json_encoders = {
            datetime.datetime: lambda v: v.isoformat(),
            datetime.date: lambda v: v.isoformat()
        }

        schema_extra = {
            "example": {
                "id": 59,
                "createdAt": "2024-01-01T00:00:00Z",
                "message": "Hello, how are you?",
                "userId ": 56
            }
        }

class MessageBot(BaseModel):
    
    id : int
    createdAt : datetime.datetime
    userId : int
    response : str
    
    class Config:
        """Config class to allow the use of datetime objects
        """
        json_encoders = {
            datetime.datetime: lambda v: v.isoformat(),
            datetime.date: lambda v: v.isoformat()
        }

        schema_extra = {
            "example": {
                "id": 59,
                "createdAt": "2024-01-01T00:00:00Z",
                "userId ": 6,
                "response": "Hello, how are you? I am a bot"
            }
        }