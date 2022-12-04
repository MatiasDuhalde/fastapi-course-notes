from datetime import datetime, timedelta
from typing import Any, Literal, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.user.models import User
from core.config import JWT_ALGORITH, JWT_EXPIRATION, JWT_SECRET_KEY
from core.db import get_db
from exceptions.auth import TokenException

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

from jose import JWTError, jwt


def get_password_hash(password) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: Session) -> Any | Literal[False]:
    user = db.query(User).filter_by(username=username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str,
                        user_id: int,
                        expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.utcnow()
    encode = {'sub': username, 'id': user_id, 'iat': now}
    if expires_delta is not None:
        encode['exp'] = now + expires_delta
    else:
        encode['exp'] = now + timedelta(seconds=JWT_EXPIRATION)
    return jwt.encode(encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITH)


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITH])


async def get_current_user(token: str = Depends(oauth2_bearer),
                           db: Session = Depends(get_db)) -> Any:
    try:
        payload = decode_token(token)
        username = payload.get('sub')
        user_id = payload.get('id')
        if username is None or user_id is None:
            raise TokenException()
        user_object = db.query(User).filter_by(username=username, id=user_id).first()
        if user_object is None:
            raise TokenException()
        return user_object
    except JWTError as exc:
        raise TokenException() from exc