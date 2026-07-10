"""게시글 모델"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class PostStatus(str, enum.Enum):
    """게시글 상태"""
    DRAFT = "draft"           # 초안
    PUBLISHED = "published"   # 공개
    HIDDEN = "hidden"         # 비공개


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    status = Column(
        Enum(PostStatus),
        default=PostStatus.DRAFT,
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # 외래키: 작성자
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 외래키: 게시판
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)

    # 양방향 관계: 작성자
    author = relationship("User", back_populates="posts")
    # 양방향 관계: 게시판
    board = relationship("Board", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', status={self.status})>"
