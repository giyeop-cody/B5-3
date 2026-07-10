"""세션 관리 유틸리티"""
from fastapi import Request
from app.repositories.user_repository import UserRepository
from app.database import SessionLocal
from app.models import User
from typing import Optional


def get_current_user_from_session(request: Request) -> Optional[User]:
    """세션에서 현재 사용자 정보 가져오기"""
    user_id = request.session.get("user_id")
    if not user_id:
        return None

    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        return user_repo.get_by_id(user_id)
    finally:
        db.close()


def login_user(request: Request, user_id: int):
    """사용자 로그인 (세션에 사용자 ID 저장)"""
    request.session["user_id"] = user_id


def logout_user(request: Request):
    """사용자 로그아웃 (세션에서 사용자 ID 제거)"""
    request.session.pop("user_id", None)


def is_authenticated(request: Request) -> bool:
    """인증 여부 확인"""
    return "user_id" in request.session
