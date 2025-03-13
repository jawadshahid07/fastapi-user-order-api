from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User

# Load environment variables
load_dotenv()

# Load secret key & settings from .env
import jwt
from cryptography.hazmat.primitives import serialization

# Load Private Key (for signing JWTs)
with open(".ssh/jwtRS256", "rb") as key_file:
    PRIVATE_KEY = serialization.load_pem_private_key(key_file.read(), password=None)

# Load Public Key (for verifying JWTs)
with open(".ssh/jwtRS256.pem", "rb") as key_file:
    PUBLIC_KEY = serialization.load_pem_public_key(key_file.read())

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the provided password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Generate a JWT token using RS256 private key."""
    to_encode = data.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])  # Convert user ID to string
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())})  # Expiration in UNIX timestamp
    token = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str) -> dict:
    """Decode and verify a JWT token using RS256 public key."""
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        # Convert "sub" back to an integer if it contains digits only
        if "sub" in payload and payload["sub"].isdigit():
            payload["sub"] = int(payload["sub"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

