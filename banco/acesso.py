import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

db = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=db)
session = Session()

Base = declarative_base()