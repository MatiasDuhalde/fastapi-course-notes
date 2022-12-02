from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(required=True, title='Title of the book', min_length=3, max_length=100)
    author: str = Field(required=True, title='Author of the book', min_length=1, max_length=100)
    description: Optional[str] = Field(None, title='Description of the book', min_length=1, max_length=1000)
    rating: int


BOOKS = []


@app.get("/")
async def read_all_books():
    return BOOKS

@app.post('/')
async def create_book(book: Book):
    BOOKS.append(book)
    return book
