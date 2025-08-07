import jwt
import secrets
from bcrypt import hashpw, checkpw, gensalt
from datetime import datetime, timedelta,timezone
from fastapi import HTTPException
from typing import Optional
from ..config.env import JWT_SECRET

JWT_ALGORITHM = "HS256"

def hash_password(password):
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')


def verify_password(password:str, hashed_password:str):
    return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=1)

    to_encode["exp"] = expire

    token = jwt.encode(to_encode, JWT_SECRET, JWT_ALGORITHM)

    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET,[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def generate_verification_code():
    return ''.join(secrets.choice('0123456789') for _ in range(5))