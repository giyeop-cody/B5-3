"""앱 시작 시 DB 초기화"""
from app.database import SessionLocal, engine, Base
from app.models import User, Board
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_data():
    """데이터베이스 테이블 생성 및 초기 데이터 삽입"""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 테스트 사용자
        if not db.query(User).filter(User.username == "testuser").first():
            db.add(User(
                username="testuser",
                password_hash=pwd_context.hash("test1234"),
                email="test@example.com"
            ))
            print("✓ 테스트 사용자 생성: testuser / test1234")

        # 게시판
        if not db.query(Board).filter(Board.name == "자유게시판").first():
            db.add(Board(name="자유게시판", description="자유롭게 이야기를 나누는 공간입니다."))
            print("✓ 게시판 생성: 자유게시판")

        if not db.query(Board).filter(Board.name == "질문게시판").first():
            db.add(Board(name="질문게시판", description="궁금한 점을 질문하고 답변을 받는 공간입니다."))
            print("✓ 게시판 생성: 질문게시판")

        db.commit()
    finally:
        db.close()
