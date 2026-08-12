"""데이터베이스 설정 및 세션 관리

SQLite(개발)와 PostgreSQL(운영)을 자동으로 전환합니다.
DATABASE_URL 환경변수에 따라 엔진 설정이 자동으로 달라집니다.

개발 (기본):
  DATABASE_URL=sqlite:///./app.db

운영 (PostgreSQL / Supabase):
  DATABASE_URL=postgresql://user:password@host:port/dbname

Supabase 연결:
  1. https://supabase.com에서 프로젝트 생성
  2. Settings → Database → Connection string 복사
  3. .env에 설정:
     DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL, DB_TYPE

# DB 타입별 엔진 설정
if DB_TYPE == "postgresql":
    # PostgreSQL: connection pool 설정 (운영 환경)
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # 연결이 살아있는지 확인 (Supabase空闲会话 종료 대응)
        pool_recycle=1800,   # 30분마다 연결 재사용 (Supabase 60분 타임아웃 대응)
    )
else:
    # SQLite: 개발 환경 (check_same_thread=False로 멀티스레드 허용)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI 의존성 주입용 DB 세션"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
