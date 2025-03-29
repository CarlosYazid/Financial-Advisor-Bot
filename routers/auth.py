from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from controller import AuthController
from model import User

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return AuthController.authentication(form_data)


@router.get("/users/me")
async def me(user: User  = Depends(AuthController.authUser)):
    return user