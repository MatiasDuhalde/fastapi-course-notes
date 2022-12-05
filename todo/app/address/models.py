from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base, engine


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String, nullable=False)
    address2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    apt_num = Column(String, nullable=True)

    user = relationship('User', back_populates='address')


Base.metadata.create_all(bind=engine)
