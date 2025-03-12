from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class Notice(Base):
    __tablename__ = "notice_messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000))
    timestamp = Column(DateTime, server_default=func.now())