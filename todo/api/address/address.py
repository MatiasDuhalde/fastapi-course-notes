from typing import Any, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from api.auth.utils import (get_current_user, get_db)
from app.address.models import Address

address_router = APIRouter()


class CreateAddressSchema(BaseModel):
    address1: str = Field(max_length=500)
    address2: Optional[str] = Field(None, max_length=500)
    city: str = Field(max_length=100)
    state: str = Field(max_length=100)
    country: str = Field(max_length=100)
    postal_code: str = Field(max_length=100)
    apt_num: str = Field(max_length=10)


@address_router.post('/')
async def create_address(address: CreateAddressSchema,
                         user: Any = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.flush()

    user.address_id = db_address.id

    db.commit()
    print(db_address.__dict__)
    return db_address
