from enum import Enum
from typing import Optional

from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    'book_1': {
        'title': 'Title One',
        'author': 'Author One'
    },
    'book_2': {
        'title': 'Title Two',
        'author': 'Author Two'
    },
    'book_3': {
        'title': 'Title Three',
        'author': 'Author Three'
    },
    'book_4': {
        'title': 'Title Four',
        'author': 'Author Four'
    },
    'book_5': {
        'title': 'Title Five',
        'author': 'Author Five'
    },
}


class DirectionName(str, Enum):
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.get('/{book_id}')
async def read_book(book_id: str):
    return BOOKS[book_id]


@app.get('/directions/{direction_name}')
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.NORTH:
        return {'direction': direction_name, 'sub': 'Up'}
    if direction_name == DirectionName.SOUTH:
        return {'direction': direction_name, 'sub': 'Down'}
    if direction_name == DirectionName.EAST:
        return {'direction': direction_name, 'sub': 'Right'}
    if direction_name == DirectionName.WEST:
        return {'direction': direction_name, 'sub': 'Left'}


@app.post('/')
async def create_book(book_title, book_author):
    book_id = 'book_' + str(len(BOOKS) + 1)
    BOOKS[book_id] = {'title': book_title, 'author': book_author}
    return BOOKS[book_id]


@app.put('/{book_id}')
async def update_book(book_id: str, book_title: str, book_author: str):
    BOOKS[book_id] = {'title': book_title, 'author': book_author}
    return BOOKS[book_id]


@app.delete('/{book_id}')
async def delete_book(book_id: str):
    del BOOKS[book_id]
    return {'message': 'Book deleted'}


@app.get('/assignment/')
async def read_book_assignment(book_id: str):
    return BOOKS[book_id]


@app.delete('/assignment/')
async def delete_book_assignment(book_id: str):
    del BOOKS[book_id]
    return {'message': 'Book deleted'}
