from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
import datetime

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500, collation='utf8mb4_unicode_ci'))
    user_id = Column(Integer, ForeignKey("users.id"))
    user_name = Column(String(50, collation='utf8mb4_unicode_ci'))
    user_email = Column(String(50))
    target_id = Column(Integer)
    target_type = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
