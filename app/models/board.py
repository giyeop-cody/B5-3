"""게시판 모델

Board-Post 관계 정책:
- Board → Post 관계에는 cascade가 설정되지 않았습니다.
- 이유: 게시판 삭제 시 게시글까지 자동 삭제하면 데이터 손실이 발생할 수 있음
- 게시판 삭제 시나리오:
  1. 게시글을 다른 게시판으로 이동 후 게시판 삭제 (권장)
  2. 게시글을 수동으로 모두 삭제 후 게시판 삭제
  3. FK 제약으로 게시글이 있으면 게시판 삭제 불가 (현재 기본 동작)
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # 양방향 관계: 게시판에 속한 게시글 목록
    #
    # cascade 없음 (의도적 선택):
    #   - 게시판 삭제 시 게시글은 자동 삭제되지 않음
    #   - 게시글이 존재하는 게시판은 FK 제약으로 삭제 불가
    #   - 게시판 삭제 전, 게시글을 다른 게시판으로 이동하거나 수동 삭제 필요
    #
    # 대안: 자동 삭제를 원하면 아래처럼 변경
    #   posts = relationship("Post", back_populates="board", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="board")

    def __repr__(self):
        return f"<Board(id={self.id}, name='{self.name}')>"
