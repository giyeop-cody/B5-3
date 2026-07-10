"""데이터베이스 초기화 스크립트"""
from app.database import SessionLocal, engine, Base
from app.models import User, Board
from passlib.context import CryptContext

# 비밀번호 해싱 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_db():
    """데이터베이스 테이블 생성 및 초기 데이터 삽입"""
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("✓ 데이터베이스 테이블 생성 완료")

    db = SessionLocal()

    try:
        # 테스트 사용자 생성
        if not db.query(User).filter(User.username == "testuser").first():
            test_user = User(
                username="testuser",
                password_hash=pwd_context.hash("test1234"),
                email="test@example.com"
            )
            db.add(test_user)
            print("✓ 테스트 사용자 생성: testuser / test1234")
        else:
            print("- 테스트 사용자 이미 존재")

        # 기본 게시판 생성
        if not db.query(Board).filter(Board.name == "자유게시판").first():
            board1 = Board(
                name="자유게시판",
                description="자유롭게 이야기를 나누는 공간입니다."
            )
            db.add(board1)
            print("✓ 게시판 생성: 자유게시판")
        else:
            print("- 자유게시판 이미 존재")

        if not db.query(Board).filter(Board.name == "질문게시판").first():
            board2 = Board(
                name="질문게시판",
                description="궁금한 점을 질문하고 답변을 받는 공간입니다."
            )
            db.add(board2)
            print("✓ 게시판 생성: 질문게시판")
        else:
            print("- 질문게시판 이미 존재")

        db.commit()
        print("\n✅ 데이터베이스 초기화 완료!")

    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
