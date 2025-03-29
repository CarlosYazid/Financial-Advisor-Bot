from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import userRouter, usersRouter, authRouter, audioRouter, chatRouter

app = FastAPI()

app.include_router(userRouter)
app.include_router(usersRouter)
app.include_router(authRouter)
app.include_router(audioRouter)
app.include_router(chatRouter)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"status": "Ok"}