from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.init_db()

class UserData(BaseModel):
    user_id: int

@app.post("/get_user")
async def get_user_data(data: UserData):
    return await database.get_user(data.user_id)

@app.post("/click")
async def click(data: UserData):
    return await database.add_click(data.user_id)

@app.get("/top")
async def get_top():
    return await database.get_top_players()