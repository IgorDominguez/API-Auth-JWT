from sqlalchemy import Column, String
from database.connection import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, nullable=False)
    senha = Column(String, nullable=False)