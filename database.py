from sqlalchemy import create_engine
from sqlalchemy import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

DB_URL = "sqlite:///./study.db"

engine = create_engine(DB_URL,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()