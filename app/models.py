from datetime import date
from sqlalchemy import Column, Integer, String, Date

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(16), unique=True, index=True)
    email = Column(String(256), unique=True, index=True)
    password = Column(String(16))
    register_date = Column(Date, default=date.today())
