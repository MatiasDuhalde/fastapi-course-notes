from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base, engine


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(Integer, nullable=False, default=1)
    completed = Column(Boolean, nullable=False, default=False)

    owner = relationship('User', back_populates='todos')


Base.metadata.create_all(bind=engine)
