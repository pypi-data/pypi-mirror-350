import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext


SECRET_KEY = os.getenv("SECRET_KEY", "e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_secret(secret: str) -> str:
    return pwd_context.hash(secret)

def verify_secret(secret: str, hashed: str) -> bool:
    return pwd_context.verify(secret, hashed)

def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM), expire

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
