from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os


curr_path = os.path.dirname(__file__)
db_path = os.path.join(curr_path, "database.db")

engine = create_engine(
    "sqlite:///"+db_path, connect_args={"check_same_thread": False}
)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()