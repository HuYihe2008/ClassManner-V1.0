from sqlalchemy.orm import sessionmaker
#from .engine import engine
from main import engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)