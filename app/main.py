from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(router)
client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client.secrets_db


@asynccontextmanager
async def lifespan(application: FastAPI):
    await db.secrets.create_index("expires_at", expireAfterSeconds=0)
