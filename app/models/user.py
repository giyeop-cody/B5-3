"""사용자 모델

양방향 관계 주의사항:
- User.posts와 Post.author는 양방향 관계(back_populates)입니다.
- JSON 직렬화 시 순환참조(User → Post → User → ...)가 발생할 수 있으므로,
  Pydantic 응답 모델에서는 관계 객체 전체가 아닌 FK ID만 포함해야 합니다.
  (schemas.py의 PostResponse 참고)
"""
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
    #
    # cascade="all, delete-orphan" 정책:
    #   - 사용자 삭제 시 해당 사용자의 모든 게시글도 자동 삭제
    #   - "orphan" 옵션: 부모(User)가 없는 자식(Post)은 자동 삭제
    #
    # 삭제 시나리오:
    #   1. 사용자 탈퇴 → 해당 사용자의 모든 게시글 자동 삭제
    #   2. 게시글을 다른 사용자에게 이동 불가 (cascade 정책 상)
    #   3. 이동이 필요하다면 cascade를 제거하고 수동 처리 필요
    #
    # 순환참조 주의:
    #   User.posts[0].author.posts[0].author... → 무한 순환
    #   → Pydantic 응답 모델에서 author_id만 포함하여 해결 (schemas.py 참고)
    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    # 회원 간 팔로우 관계 (과제 요구사항: "회원 간 팔로우/연결")
    # following_assoc: 내가 팔로우 하는 관계 목록 (follower_id = 나)
    # followers_assoc: 나를 팔로우 하는 관계 목록 (followed_id = 나)
    following_assoc = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan"
    )
    followers_assoc = relationship(
        "Follow",
        foreign_keys="Follow.followed_id",
        back_populates="followed",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
