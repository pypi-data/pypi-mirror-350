from agentutil.helper.sql_client import Base

from sqlalchemy import Column, Integer, String, DateTime
from agentutil.helper.sql_client import get_local_time
from pydantic import BaseModel, model_validator
from enum import Enum


class NewsStatus(str, Enum):
    PUBLISHED = "published"
    NEW = "new"
    FAILED = "failed"


class NewsORM(Base):
    __tablename__ = "news"

    id = Column(String, primary_key=True, autoincrement=True)
    pipeline = Column(String, nullable=True)
    title = Column(String)
    news_id = Column(String, nullable=True)
    cost = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, nullable=False, default=get_local_time)
    updated_at = Column(DateTime, nullable=False, default=get_local_time, onupdate=get_local_time)


class News(BaseModel):
    title: str
    summary: str = ""
    content: str = ""
    status: NewsStatus = NewsStatus.NEW

    @model_validator(mode='before')
    @classmethod
    def remove_non_bmp(cls, values):
        for field in ['title', 'summary', 'content']:
            if field in values:
                values[field] = ''.join(
                    c for c in values[field] if ord(c) <= 0xFFFF
                )
        return values
