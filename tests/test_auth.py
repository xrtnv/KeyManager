import pytest
from app.auth import get_password_hash, verify_password, encrypt_secret, decrypt_secret


def test_get_password_hash():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert verify_password(password, hashed_password)


def test_verify_password():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)


def test_encrypt_decrypt_secret():
    secret = "mysecret"
    encrypted_secret = encrypt_secret(secret)
    decrypted_secret = decrypt_secret(encrypted_secret)
    assert secret == decrypted_secret
