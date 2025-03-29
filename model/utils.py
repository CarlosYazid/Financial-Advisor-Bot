from model import User
from fastapi import HTTPException
import datetime
import json

class UserUtils:
    
    @classmethod
    def to_json(self, user : User) -> str:
        """Method to convert the object to a json string

        Args:
            user (User): user object
        
        Raises:
            HTTPException: 500 If the user object is not valid

        Returns:
            str: json string
        """
        
        try:
            json_ = json.dumps(user.__dict__, default=str)
        except Exception:
            raise HTTPException(status_code=500, detail=f"Internal error")
        #print(json_)
        return json_
    
    @classmethod
    def from_json(cls, data : dict):
        """Method to create a user from a json string

        Args:
            data (dict): json string
            
        Raises:
            HTTPException: 500 If the json string is not valid

        Returns:
            User: user object
        """
        
        try:
            user = User(id = data["id"], 
                   createdAt = datetime.datetime.fromisoformat(data["createdAt"][:-1]), 
                   name = data["name"], 
                   userName = data["userName"],
                   birthdate = datetime.date.fromisoformat(data["birthdate"][:10]), 
                   documentID = data["documentID"], 
                   email = data["email"], 
                   phone = data["phone"], 
                   password = data["password"],
                   debt = data["debt"], 
                   debtMaturityDate = datetime.date.fromisoformat(data["debtMaturityDate"][:10]), 
                   state = data["state"], 
                   paymentHistory = data["paymentHistory"]
                   )
        except Exception:
            raise HTTPException(status_code=500, detail=f"Internal error")
        return user