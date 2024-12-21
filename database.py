from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQL_ALCHEMY_DATABASE_URL = 'postgres://postgres:mouad1233@localhost/fastapi'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()