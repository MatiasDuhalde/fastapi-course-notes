from enum import Enum

SQLITE_DATABASE_URI = 'sqlite:///./todos.db'

POSTGRES_DATABASE_URI = 'postgresql://fastapi_admin@localhost:5432/fastapi_todos'

JWT_SECRET_KEY = 'nn5QDKAUKzUyiuQeh48a+bVyHguw8AkciXrgTND1YXcW/FuvATRo1YPeUbj2ypKa'
JWT_ALGORITH = 'HS256'
JWT_EXPIRATION = 3600


class DB_ENGINES(str, Enum):
    SQLITE = 'sqlite'
    POSTGRES = 'postgres'


DB_ENGINE = DB_ENGINES.POSTGRES