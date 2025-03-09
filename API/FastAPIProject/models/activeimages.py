from sqlalchemy import Column, Integer, String, JSON
from database import Base

class ActiveImage(Base):
    __tablename__ = "active_images"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(1000))
    images = Column(JSON)
