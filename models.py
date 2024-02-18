from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class StatusChoises(Enum):
    alive = 'alive'
    dead = 'dead'
    finished = 'finished'

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    sended_at = Column(DateTime, default=datetime.now)
    next_message_number = Column(Integer, default=1)
    telegram_id = Column(String)
    telegram_username = Column(String)
    status = Column(String, default=StatusChoises.alive.value, nullable=False)
    status_updated_at = Column(DateTime, default=datetime.now)
