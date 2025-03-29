from fastapi import APIRouter
from controller import UserController
from model import User

router = APIRouter(prefix="/user", tags=["User"])

def getUser(id: int):
    return UserController.getUserById(id)

def deleteUser(id: int):
    return UserController.deleteUser(id)

@router.get("/{id}")
async def getUserPath(id: int):
    return getUser(id)

@router.get("/")
async def getUserQuery(id: int):
    return getUser(id)

@router.post("/", response_model = User,status_code=201)
async def postUser(user: User):
    return UserController.postUser(user)

@router.put("/", response_model = User, status_code=200)
async def putUser(user: User):
    return UserController.putUser(user)

@router.delete("/{id}")
async def deleteUserPath(id: int):
    return deleteUser(id)

@router.delete("/")
async def deleteUserQuery(id: int):
    return deleteUser(id)