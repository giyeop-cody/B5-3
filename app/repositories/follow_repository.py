"""팔로우 저장소 (DB CRUD만 담당)"""
from sqlalchemy.orm import Session
from app.models import Follow, User


class FollowRepository:
    def __init__(self, db: Session):
        self.db = db

    def is_following(self, follower_id: int, followed_id: int) -> bool:
        """이미 팔로우 중인지 확인"""
        return self.db.query(Follow).filter(
            Follow.follower_id == follower_id,
            Follow.followed_id == followed_id
        ).first() is not None

    def create(self, follower_id: int, followed_id: int) -> Follow:
        """팔로우 관계 생성"""
        follow = Follow(follower_id=follower_id, followed_id=followed_id)
        self.db.add(follow)
        self.db.commit()
        self.db.refresh(follow)
        return follow

    def delete(self, follower_id: int, followed_id: int) -> bool:
        """언팔로우 (팔로우 관계 삭제)"""
        follow = self.db.query(Follow).filter(
            Follow.follower_id == follower_id,
            Follow.followed_id == followed_id
        ).first()
        if follow:
            self.db.delete(follow)
            self.db.commit()
            return True
        return False

    def get_following(self, user_id: int) -> list[User]:
        """내가 팔로우 하는 사용자 목록"""
        follows = self.db.query(Follow).filter(Follow.follower_id == user_id).all()
        following_ids = [f.followed_id for f in follows]
        if not following_ids:
            return []
        return self.db.query(User).filter(User.id.in_(following_ids)).all()

    def get_followers(self, user_id: int) -> list[User]:
        """나를 팔로우 하는 사용자 목록"""
        follows = self.db.query(Follow).filter(Follow.followed_id == user_id).all()
        follower_ids = [f.follower_id for f in follows]
        if not follower_ids:
            return []
        return self.db.query(User).filter(User.id.in_(follower_ids)).all()

    def get_following_count(self, user_id: int) -> int:
        """내가 팔로우 하는 사람 수"""
        return self.db.query(Follow).filter(Follow.follower_id == user_id).count()

    def get_followers_count(self, user_id: int) -> int:
        """나를 팔로우 하는 사람 수"""
        return self.db.query(Follow).filter(Follow.followed_id == user_id).count()
