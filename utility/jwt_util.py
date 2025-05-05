import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

load_dotenv()

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login")

class JWTUtil:
    def __init__(self):
        self.secret_key = bytes.fromhex(os.getenv("SECRET_KEY"))
        self.algorithm = "HS512"
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encode_jwt(self, username: str) -> str:
        payload = {
            "sub": username,
            "iss": "Cards and Payment System",
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_jwt(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_current_user(self, token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            current_user = self.decode_jwt(token)["sub"]
            if current_user is None:
                raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
            return current_user
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

if __name__ == "__main__":
    print(secrets.token_bytes(64).hex().upper())