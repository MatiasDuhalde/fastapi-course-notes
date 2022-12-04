from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.todo.models import Todo
from core.db import SessionLocal
from exceptions.todo import TodoNotFoundException

todo_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TodoSchema(BaseModel):
    title: str = Field(title='Title of Todo', max_length=200)
    description: Optional[str] = Field(None, title='Description', max_length=500)
    priority: int = Field(title='Priority of Todo', ge=0, le=5)
    completed: bool = Field(title='Whether the Todo is completed or not', default=False)


@todo_router.get('/')
async def get_all(db: Session = Depends(get_db)):
    return db.query(Todo).all()


@todo_router.get('/{todo_id}')
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model:
        return todo_model
    raise TodoNotFoundException()


@todo_router.post('/')
async def create_todo(todo: TodoSchema, db: Session = Depends(get_db)):
    todo_model = Todo(**todo.dict())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@todo_router.put('/{todo_id}')
async def update_todo(todo_id: int, todo: TodoSchema, db: Session = Depends(get_db)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model:
        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.completed = todo.completed
        db.commit()
        db.refresh(todo_model)
        return todo_model
    raise TodoNotFoundException()


@todo_router.delete('/{todo_id}')
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model:
        db.delete(todo_model)
        db.commit()
        return todo_model
    raise TodoNotFoundException()
