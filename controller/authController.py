from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, Depends

from passlib.context import CryptContext
from jose import jwt, JWTError

import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from controller import UserController
from model import User


load_dotenv()

class Controller:

    ALGORITHM = os.getenv("ALGORITHM")
    BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS"))
    ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    SECRET = os.getenv("SECRET")
    
    OAUTH2 = OAuth2PasswordBearer(tokenUrl="login")
    CRYPT = CryptContext(schemes=["bcrypt"], bcrypt__rounds=BCRYPT_ROUNDS)
    
    def authentication(data : OAuth2PasswordRequestForm) -> dict:
        """Authenticate user

        Args:
            data (OAuth2PasswordRequestForm): data from form
            
        Raises:
            HTTPException: 400 if user not found or password is incorrect

        Returns:
            dict: access token and token type
        """
        user = UserController.getUserByEmail(data.username)
        user = UserController.getUserByUserName(data.username) if not user else user
        
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        elif not Controller.CRYPT.verify(data.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        
        access_token = {
            "sub": user.id,
            "userName": user.userName,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=Controller.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        
        return {"access_token": jwt.encode(access_token, key = Controller.SECRET,algorithm = Controller.ALGORITHM), "token_type": "bearer"}
    
    def authUser(token : str = Depends(OAUTH2)) -> User:
        """Authenticate user
        
        Args:
            token (str): token from header
            
        Raises:
            HTTPException: 401 if token is null or invalid
            HTTPException: 400 if user not found
            
        Returns:
            User: user object
        """
        
        
        if not token:
            raise HTTPException(status_code=401, detail="Token null")

        #print(token)
        
        try:            
            userData = jwt.decode(token, key=Controller.SECRET, algorithms=[Controller.ALGORITHM])
        
            user = UserController.getUserById(userData.get("sub"))
            user = UserController.getUserByUserName(userData.get("userName")) if not user else user 
        
            if not user:
                raise HTTPException(status_code=400, detail="User not found")
        
        
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
        return user