from typing import Literal

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.user.models import User as UserModel

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: Session) -> UserModel | Literal[False]:
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    return data
