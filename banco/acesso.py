from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:Tudoecomosera1#@localhost:3306/integra_maker"

db = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=db)
session = Session()

Base = declarative_base()