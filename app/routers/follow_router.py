"""팔로우 API 라우터 (회원 간 연결)"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models import User
from app.services.follow_service import FollowService

router = APIRouter(prefix="/api/users", tags=["follow"])


@router.post("/{user_id}/follow")
def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """팔로우 (회원 간 연결 생성) — 로그인 필요"""
    service = FollowService(db)
    try:
        service.follow(follower_id=current_user.id, followed_id=user_id)
        return {"message": f"사용자 {user_id}를 팔로우했습니다.", "following": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}/follow")
def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """언팔로우 (회원 간 연결 해제) — 로그인 필요"""
    service = FollowService(db)
    try:
        service.unfollow(follower_id=current_user.id, followed_id=user_id)
        return {"message": f"사용자 {user_id}를 언팔로우했습니다.", "following": False}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}/following")
def get_following(user_id: int, db: Session = Depends(get_db)):
    """내가 팔로우 하는 사용자 목록"""
    service = FollowService(db)
    following = service.get_following(user_id)
    return [
        {"id": u.id, "username": u.username, "email": u.email}
        for u in following
    ]


@router.get("/{user_id}/followers")
def get_followers(user_id: int, db: Session = Depends(get_db)):
    """나를 팔로우 하는 사용자 목록"""
    service = FollowService(db)
    followers = service.get_followers(user_id)
    return [
        {"id": u.id, "username": u.username, "email": u.email}
        for u in followers
    ]
