from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from app.auth.key_manager import PRIVATE_KEY, PUBLIC_KEY  # Import keys

# Load environment variables
load_dotenv()

ALGORITHM = os.getenv("ALGORITHM", "RS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

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
    to_encode["sub"] = str(to_encode.get("sub", ""))  # Convert user ID to string
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = int(expire.timestamp())  # Expiration in UNIX timestamp
    return jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """Decode and verify a JWT token using RS256 public key."""
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        if "sub" in payload and payload["sub"].isdigit():
            payload["sub"] = int(payload["sub"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
