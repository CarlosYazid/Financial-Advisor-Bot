"""Module to control the data User flow between the model and the view

    Raises:
        Exception: Error getting users
        Exception: User not found
        Exception: Error getting user
        Exception: Error posting user
        Exception: Error putting user
        Exception: Error deleting user

    Returns:
        _type_: 
"""

from fastapi import HTTPException

import requests
import json
from datetime import datetime
import os
from typing import Optional
from dotenv import load_dotenv

from model import User , UserUtils


load_dotenv()



class Controller:
    """Class to control the data flow between the model and the view
    
    """
    URL_DB_ENDPOINT = os.getenv("DB_ENDPOINT")
    ENDPOINT_USER =  URL_DB_ENDPOINT + os.getenv("DB_USER_ENDPOINT")

    def getUsers() -> list[User]:
        """Get all users from the endpoint

        Raises:
            HTTPException: 404 Users not found
            HTTPException: 500 Internal error

        Returns:
            list[User]: list of users
        """
        response = requests.get(Controller.ENDPOINT_USER)
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Users not found")
        
        elif response.status_code == 500:
            raise HTTPException(status_code=500, detail="Internal error")
        
        users = response.json()
        
        return [UserUtils.from_json(user) for user in users]

    def getUserById(id : int) -> User:
        """Get a user by id

        Args:
            id (int): id of the user

        Raises:
            HTTPException: 404 User not found
            HTTPException: 500 Internal error
            HTTPException: 400 Bad request

        Returns:
            User: user
        """
        response = requests.get(Controller.ENDPOINT_USER + f"/{id}")
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        elif response.status_code == 500:
            raise HTTPException(status_code=500, detail="Internal error")
        elif response.status_code == 400:
            raise HTTPException(status_code=400, detail="Bad request")
        
        user = response.json()
        
        return UserUtils.from_json(user)
        
    def postUser(user : User) -> User:
        """Post a user

        Args:
            user (User): user to post

        Raises:
            HTTPException: 500 Internal error
            HTTPException: 400 Bad request
            HTTPException: 409 User already exists
            
        Returns:
            User: user
        """       
        try:
            json_ = json.loads(UserUtils.to_json(user = user))
            
        except Exception:
            raise HTTPException(status_code=500, detail="Internal error")
        
        response = requests.post(Controller.ENDPOINT_USER, json=json_)

        if response.status_code == 500:
            raise HTTPException(status_code=500, detail="Internal error")
        elif response.status_code == 400:
            raise HTTPException(status_code=400, detail="Bad request")
        elif response.status_code == 409:
            raise HTTPException(status_code=409, detail="User already exists")
        elif response.status_code == 201:
            return UserUtils.from_json(response.json())
    
    def putUser(user : User) -> User:
        """Put a user

        Args:
            user (User): user to put

        Raises:
            HTTPException: 500 Internal error
            HTTPException: 400 Bad request
            HTTPException: 404 User not found
        
        Returns:
            User: user
        """
        try:
            json = json.loads(UserUtils.to_json(user = user))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal error")
        
        response = requests.put(Controller.ENDPOINT_USER + f"/{user.id}", json=json)

        if response.status_code == 500:
            raise HTTPException(status_code=500, detail="Internal error")
        elif response.status_code == 400:
            raise HTTPException(status_code=400, detail="Bad request")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        elif response.status_code == 200:
            return user
        
        
    def deleteUser(id : int) -> None:
        """Delete a user

        Args:
            id (int): id of the user

        Raises:
            HTTPException: 500 Internal error
            HTTPException: 400 Bad request
            HTTPException: 404 User not found
            HTTPException: 204 No content
        """
        response = requests.delete(Controller.ENDPOINT_USER + f"/{id}")

        if response.status_code == 500:
            raise HTTPException(status_code=500, detail="Internal error")
        elif response.status_code == 400:
            raise HTTPException(status_code=400, detail="Bad request")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        elif response.status_code == 200 or response.status_code == 204:
            return HTTPException(status_code=204, detail="No content")
    
    def getUserByEmail(email : str) -> Optional[User]:
        """get user by email

        Args:
            endpoint_users (str): endpoint to filter users by email
            email (str): email of the user

        Returns:
            list[data.User]: list of users
        """
        users = Controller.getUsers()

        list_ = list(filter(lambda  user: user.email == email, users))

        user : Optional[User] = None if len(list_) <= 0 else list_[0] 
        
        return user if user is not None else None
        
    def getUserByUserName(userName : str) -> Optional[User]:
        """Filter users by user name

        Args:
            endpoint_users (str): endpoint to filter users by user name
            userName (str): user name of the user

        Returns:
            list[data.User]: list of users
        """
        users = Controller.getUsers()

        list_ = list(filter(lambda  user: user.userName == userName, users))

        user : Optional[User] = None if len(list_) <= 0 else list_[0] 
        
        return user if user is not None else None