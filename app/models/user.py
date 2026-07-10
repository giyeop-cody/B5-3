"""사용자 모델"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 양방향 관계: 사용자가 작성한 게시글 목록
    # cascade="all, delete-orphan": 사용자 삭제 시 게시글도 함께 삭제
    # 이유: 사용자가 탈퇴하면 해당 사용자의 모든 게시글도 삭제하는 것이 자연스러움
    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
