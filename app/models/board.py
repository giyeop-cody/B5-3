"""게시판 모델"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # 양방향 관계: 게시판에 속한 게시글 목록
    # cascade 없음: 게시판 삭제 시 게시글은 별도 처리 필요
    # 이유: 게시판이 삭제된다고 게시글까지 자동 삭제할 필요는 없음
    # (다른 게시판으로 이동하거나 수동 삭제하는 것이 더 안전)
    posts = relationship("Post", back_populates="board")

    def __repr__(self):
        return f"<Board(id={self.id}, name='{self.name}')>"
