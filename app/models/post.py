"""게시글 모델

양방향 관계 및 직렬화 주의사항:
- Post는 User, Board와 양방향 관계를 가집니다.
- JSON 직렬화 시 순환참조 방지를 위해:
  1. Pydantic 응답 모델(PostResponse)에서는 author_id, board_id만 포함
  2. 관계 객체(author, board) 전체는 응답에 포함하지 않음
  3. Jinja2 템플릿에서는 post.author.username 등 필요한 필드만 선택적 접근

상태 전이 정책:
- DRAFT (초안) → PUBLISHED (공개): publish_post()
- DRAFT (초안) → HIDDEN (비공개): hide_post()
- PUBLISHED (공개) → HIDDEN (비공개): hide_post()
- HIDDEN (비공개) → PUBLISHED (공개): publish_post()
- 상태 변경은 작성자만 가능 (Service 계층에서 권한 검증)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class PostStatus(str, enum.Enum):
    """게시글 상태

    상태 전이 다이어그램:
        DRAFT ←→ PUBLISHED
           ↓         ↓
         HIDDEN ←→ HIDDEN
    """
    DRAFT = "draft"           # 초안 (기본값)
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
    #
    # 순환참조 주의:
    #   Post → User(author) → Post(posts) → User(author) → ... 무한 순환
    #   → Pydantic PostResponse에서는 author_id만 포함 (author 객체 X)
    #   → Jinja2에서는 post.author.username 등 필요한 필드만 접근
    author = relationship("User", back_populates="posts")

    # 양방향 관계: 게시판
    #
    # 순환참조 주의:
    #   Post → Board(board) → Post(posts) → Board(board) → ... 무한 순환
    #   → Pydantic PostResponse에서는 board_id만 포함 (board 객체 X)
    #   → Jinja2에서는 post.board.name 등 필요한 필드만 접근
    board = relationship("Board", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', status={self.status})>"
