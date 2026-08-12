"""팔로우 서비스 (비즈니스 로직)"""
from sqlalchemy.orm import Session
from app.repositories.follow_repository import FollowRepository
from app.repositories.user_repository import UserRepository


class FollowService:
    def __init__(self, db: Session):
        self.db = db
        self.follow_repo = FollowRepository(db)
        self.user_repo = UserRepository(db)

    def follow(self, follower_id: int, followed_id: int):
        """팔로우 (회원 간 연결 생성)

        비즈니스 규칙:
        1. 자기 자신을 팔로우할 수 없음
        2. 대상 사용자가 존재해야 함
        3. 이미 팔로우 중이면 중복 생성하지 않음
        """
        if follower_id == followed_id:
            raise ValueError("자기 자신을 팔로우할 수 없습니다.")

        target = self.user_repo.get_by_id(followed_id)
        if not target:
            raise ValueError("존재하지 않는 사용자입니다.")

        if self.follow_repo.is_following(follower_id, followed_id):
            raise ValueError("이미 팔로우하고 있는 사용자입니다.")

        return self.follow_repo.create(follower_id, followed_id)

    def unfollow(self, follower_id: int, followed_id: int):
        """언팔로우 (회원 간 연결 해제)"""
        if not self.follow_repo.is_following(follower_id, followed_id):
            raise ValueError("팔로우하고 있지 않은 사용자입니다.")

        self.follow_repo.delete(follower_id, followed_id)

    def is_following(self, follower_id: int, followed_id: int) -> bool:
        """팔로우 여부 확인"""
        return self.follow_repo.is_following(follower_id, followed_id)

    def get_following(self, user_id: int):
        """내가 팔로우 하는 사용자 목록"""
        return self.follow_repo.get_following(user_id)

    def get_followers(self, user_id: int):
        """나를 팔로우 하는 사용자 목록"""
        return self.follow_repo.get_followers(user_id)

    def get_follow_stats(self, user_id: int) -> dict:
        """팔로우 통계 (팔로잉 수, 팔로워 수)"""
        return {
            "following_count": self.follow_repo.get_following_count(user_id),
            "followers_count": self.follow_repo.get_followers_count(user_id),
        }
