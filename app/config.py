import os
import dotenv

from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Settings(BaseSettings):
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"


settings = Settings()
