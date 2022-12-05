from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field, SecretStr
from sqlalchemy.orm import Session

from api.auth.utils import (authenticate_user, create_access_token, get_db, get_password_hash)
from app.user.models import User
from exceptions.auth import AuthenticationErrorException

auth_router = APIRouter()


class CreateUser(BaseModel):
    username: str = Field(title='Username', max_length=50)
    password: SecretStr = Field(title='Password', min_length=8, max_length=256)
    email: EmailStr = Field(title='Email')
    first_name: Optional[str] = Field(None, title='First Name', max_length=100)
    last_name: Optional[str] = Field(None, title='Last Name', max_length=100)
    phone_number: Optional[str] = Field(None, title='Phone Number', max_length=30)

    class Config:
        schema_extra = {
            'example': {
                'username': 'john_doe',
                'password': 'password',
                'email': 'johndoe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '1234567890'
            }
        }


class CreateUserResponse(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]


@auth_router.post('/users')
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user_model = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        hashed_password=get_password_hash(user.password.get_secret_value()),
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model


@auth_router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AuthenticationErrorException()
    access_token = create_access_token(user.username, user.id)
    return {'access_token': access_token, 'token_type': 'bearer'}
