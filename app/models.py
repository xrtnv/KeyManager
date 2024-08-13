from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class Secret(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    secret_data: str
    hashed_passphrase: str
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    secret_key: str

    class Config:
        arbitrary_types_allowed = True


class SecretInDB(Secret):
    pass


class SecretIn(BaseModel):
    secret_data: str
    passphrase: str
    ttl: int
