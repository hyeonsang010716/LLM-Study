from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABACE_URL = "sqlite:///./myapi.db" # db path

engine = create_engine( # 커넥션 풀을 생성
    SQLALCHEMY_DATABACE_URL, connect_args={"check_same_thread": False}
)
# 데이터 베이스에 접근하기 위한 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #autocommit False는 commit을 해야 저장이 됨
#데이터베이스 모델 구성을 위한 클래스
Base = declarative_base()
