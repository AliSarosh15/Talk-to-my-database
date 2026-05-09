from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
#postgresql://postgres:ali123@localhost:5432/mydb
DATABASE_URL=os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set")

engine= create_engine(DATABASE_URL,echo= False)

SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
