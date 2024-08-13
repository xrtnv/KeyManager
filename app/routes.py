from typing import Optional

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from app.auth import get_password_hash, verify_password, encrypt_secret, decrypt_secret
from app.config import settings
from app.models import Secret
import hashlib
import base64

router = APIRouter()

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client.secrets_db


class SecretRequest(BaseModel):
    secret: str
    passphrase: str
    ttl: Optional[int] = None


class SecretResponse(BaseModel):
    secret_key: str


@router.post("/generate", response_model=SecretResponse)
async def generate_secret(secret_request: SecretRequest):
    secret_key = base64.urlsafe_b64encode(hashlib.sha256(secret_request.secret.encode()).digest()).decode()
    hashed_passphrase = get_password_hash(secret_request.passphrase)
    encrypted_secret = encrypt_secret(secret_request.secret)
    expires_at = datetime.now() + timedelta(seconds=secret_request.ttl) if secret_request.ttl else None
    secret = Secret(secret_data=encrypted_secret, hashed_passphrase=hashed_passphrase, expires_at=expires_at,
                    secret_key=secret_key)
    await db.secrets.insert_one(secret.dict(by_alias=True))
    return {"secret_key": secret_key}


@router.get("/secrets/{secret_key}")
async def get_secret(secret_key: str, passphrase: str = Query(...)):
    secret = await db.secrets.find_one({"secret_key": secret_key})
    if not secret or not verify_password(passphrase, secret["hashed_passphrase"]) or secret['expires_at'] < datetime.now():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found or incorrect passphrase")

    decrypted_secret = decrypt_secret(secret["secret_data"])
    await db.secrets.delete_one({"_id": secret["_id"]})
    return {"secret": decrypted_secret}
