from fastapi import APIRouter
from controller import UserController

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def getUsers():
    return UserController.getUsers()