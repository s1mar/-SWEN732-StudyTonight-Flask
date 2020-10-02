from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session

DB_URL = "sqlite:///./study.db"

db_engine = create_engine(DB_URL,connect_args={"check_same_thread":False})
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=db_engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=db_engine)