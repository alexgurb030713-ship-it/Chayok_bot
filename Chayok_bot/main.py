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

class ClickData(BaseModel):
    user_id: int
    clicks: int = 1

class UserData(BaseModel):
    user_id: int

@app.on_event("startup")
async def startup():
    await database.init_db()

@app.get("/api/profile/{user_id}")
async def get_profile(user_id: int):
    return await database.get_or_create_user(user_id)

@app.post("/api/click")
async def click(data: ClickData):
    return await database.process_click_db(data.user_id, data.clicks)

@app.post("/api/spin")
async def spin(data: UserData):
    return await database.spin_roulette_db(data.user_id)
from fastapi.responses import FileResponse

@app.get("/")
async def serve_index():
    return FileResponse("index.html")