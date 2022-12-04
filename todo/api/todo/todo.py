from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from api.auth.utils import get_current_user
from app.todo.models import Todo
from app.user.models import User
from core.db import SessionLocal
from exceptions.todo import TodoNotFoundException

todo_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CreateTodoSchema(BaseModel):
    title: str = Field(title='Title of Todo', max_length=200)
    description: Optional[str] = Field(None, title='Description', max_length=500)
    priority: int = Field(title='Priority of Todo', ge=0, le=5)


class UpdateTodoSchema(BaseModel):
    title: Optional[str] = Field(title='Title of Todo', max_length=200)
    description: Optional[str] = Field(title='Description', max_length=500)
    priority: Optional[int] = Field(title='Priority of Todo', ge=0, le=5)
    completed: Optional[bool] = Field(title='Whether the Todo is completed or not', default=False)


@todo_router.get('/')
async def get_all(db: Session = Depends(get_db)):
    return db.query(Todo).all()


@todo_router.get('/user')
async def get_user_todos(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Todo).filter_by(owner_id=user.id).all()


@todo_router.get('/{todo_id}')
async def get_todo(todo_id: int,
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):

    todo_model = db.query(Todo).filter_by(id=todo_id, owner_id=user.id).first()
    if todo_model:
        return todo_model
    raise TodoNotFoundException()


@todo_router.post('/')
async def create_todo(todo: CreateTodoSchema,
                      user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    todo_model = Todo(
        **todo.dict(),
        owner_id=user.id,
        completed=False,
    )
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@todo_router.put('/{todo_id}')
async def update_todo(todo_id: int,
                      todo: UpdateTodoSchema,
                      user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    todo_model = db.query(Todo).filter_by(id=todo_id, owner_id=user.id).first()
    if todo_model:
        for key, value in todo.dict(exclude_unset=True).items():
            setattr(todo_model, key, value)
        db.commit()
        db.refresh(todo_model)
        return todo_model
    raise TodoNotFoundException()


@todo_router.delete('/{todo_id}')
async def delete_todo(todo_id: int,
                      user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    todo_model = db.query(Todo).filter_by(id=todo_id, owner_id=user.id).first()
    if todo_model:
        db.delete(todo_model)
        db.commit()
        return todo_model
    raise TodoNotFoundException()
