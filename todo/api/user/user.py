from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, SecretStr
from sqlalchemy.orm import Session

from api.auth.utils import get_current_user, get_password_hash, verify_password
from app.user.models import User
from core.db import get_db
from exceptions.user import UserNotFoundException

user_router = APIRouter()


class ChangePasswordSchema(BaseModel):
    old_password: SecretStr
    old_password_confirm: SecretStr
    new_password: SecretStr = Field(title='Password', min_length=8, max_length=256)


@user_router.get('/')
async def get_all(db: Session = Depends(get_db)):
    return db.query(User).all()


@user_router.get('/query')
async def get_user_query_param(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        return user
    return UserNotFoundException()


@user_router.get('/{user_id}')
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        return user
    return UserNotFoundException()


@user_router.put('/change-password')
async def change_password(data: ChangePasswordSchema,
                          user: Any = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    if data.old_password.get_secret_value() != data.old_password_confirm.get_secret_value():
        return {'message': 'Old password and old password confirmation do not match'}
    if not verify_password(data.old_password.get_secret_value(), user.hashed_password):
        return {'message': 'Old password is incorrect'}
    user.hashed_password = get_password_hash(data.new_password.get_secret_value())
    db.commit()
    return {'message': 'Password changed successfully'}


@user_router.delete('/')
async def delete_user(user: Any = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(user)
    db.commit()
    return {'message': 'User deleted successfully'}
