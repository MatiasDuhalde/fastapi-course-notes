from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    todos = relationship('Todo', back_populates='owner')


Base.metadata.create_all(bind=engine)
