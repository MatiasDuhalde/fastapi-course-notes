from typing import Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, Header, HTTPException, Request, status
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

app = FastAPI()


class NegativeNumberException(Exception):

    def __init__(self, books_to_return) -> None:
        self.books_to_return = books_to_return


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(title='Title of the book', min_length=3, max_length=100)
    author: str = Field(title='Author of the book', min_length=1, max_length=100)
    description: Optional[str] = Field(title='Description of the book',
                                       min_length=1,
                                       max_length=1000)


class Book(BaseModel):
    id: UUID
    title: str = Field(title='Title of the book', min_length=3, max_length=100)
    author: str = Field(title='Author of the book', min_length=1, max_length=100)
    description: Optional[str] = Field(title='Description of the book',
                                       min_length=1,
                                       max_length=1000)
    rating: int = Field(title='Rating of the book', ge=1, le=100)

    class Config:
        schema_extra = {
            'example': {
                'id': uuid4(),
                'title': 'Example Title',
                'author': 'Example Author',
                'description': 'Example Description',
                'rating': 50
            }
        }


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(_req: Request, exc: NegativeNumberException):
    return JSONResponse(status_code=418,
                        content={'message': f'You cannot return {exc.books_to_return} books'})


@app.post('/login')
async def book_login(book_id: UUID, username: str = Header(), password: str = Header()):
    if username == 'FastAPIUser' and password == 'test124!':
        found_book = next((book for book in BOOKS if book.id == book_id), None)
        if found_book:
            return found_book
        raise_item_cannot_be_found_exception()
    return 'Invalid user'


@app.get('/header')
async def read_header(random_header: Optional[str] = Header(None)):
    return {'Random-Header': random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None) -> list[Book]:
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return)
    if len(BOOKS) == 0:
        create_books_no_api()
    if books_to_return:
        return BOOKS[:books_to_return]
    return BOOKS


@app.get('/{book_id}')
async def read_book(book_id: UUID) -> Book:
    found_book = next((book for book in BOOKS if book.id == book_id), None)
    if found_book:
        return found_book
    raise_item_cannot_be_found_exception()


@app.get('/rating/{book_id}', response_model=BookNoRating)
async def read_book_no_reading(book_id: UUID) -> BookNoRating:
    found_book = next((book for book in BOOKS if book.id == book_id), None)
    if found_book:
        return found_book
    raise_item_cannot_be_found_exception()


@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book) -> Book:
    BOOKS.append(book)
    return book


@app.put('/{book_id}')
async def update_book(book_id: UUID, book: Book) -> Book | None:
    book_to_update = next((book for book in BOOKS if book.id == book_id), None)
    if book_to_update:
        book_to_update.title = book.title
        book_to_update.author = book.author
        book_to_update.description = book.description
        book_to_update.rating = book.rating
        return book_to_update
    raise_item_cannot_be_found_exception()


@app.delete('/{book_id}')
async def delete_book(book_id: UUID) -> Book:
    book_to_delete = next((book for book in BOOKS if book.id == book_id), None)
    if book_to_delete:
        BOOKS.remove(book_to_delete)
        return book_to_delete
    raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id=uuid4(),
                  title='Title 1',
                  author='Author 1',
                  description='Description 1',
                  rating=60)
    book_2 = Book(id=uuid4(),
                  title='Title 2',
                  author='Author 2',
                  description='Description 2',
                  rating=70)
    book_3 = Book(id=uuid4(),
                  title='Title 3',
                  author='Author 3',
                  description='Description 3',
                  rating=80)
    book_4 = Book(id=uuid4(),
                  title='Title 4',
                  author='Author 4',
                  description='Description 4',
                  rating=90)
    BOOKS.extend([book_1, book_2, book_3, book_4])


def raise_item_cannot_be_found_exception():
    raise HTTPException(status_code=404, detail='Item not found')