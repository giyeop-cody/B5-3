"""팔로우 모델 (회원 간 연결 관계)

과제 요구사항: "회원 간 팔로우/연결 기능을 구현합니다"
- User 간 N:M 관계 (한 사용자가 여러 사용자를 팔로우, 여러 사용자에게 팔로우됨)
- follows 테이블: follower_id(팔로우 하는 사람) → followed_id(팔로우 당하는 사람)

순환참조 주의:
- User.following → [Follow → User] → User.following → ... 무한 순환
- Pydantic 응답에서는 follower_id, followed_id(int)만 포함
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Follow(Base):
    """팔로우 관계 모델 (회원 간 연결)

   follower_id: 팔로우를 하는 사용자 (주체)
    followed_id: 팔로우를 당하는 사용자 (대상)
    """
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    followed_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 동일한 (follower, followed) 쌍 중복 방지
    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="uq_follow_pair"),
    )

    # 관계 (순환참조 방지: 응답 모델에서는 ID만 사용)
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following_assoc")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers_assoc")

    def __repr__(self):
        return f"<Follow(follower={self.follower_id} → followed={self.followed_id})>"
