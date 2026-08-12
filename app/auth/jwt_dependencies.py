"""JWT 인증 의존성 (보너스: JWT 인증)

세션 기반 get_current_user를 JWT 기반으로 대체합니다.
Authorization: Bearer {token} 헤더에서 토큰을 추출하여 검증합니다.
"""
from fastapi import Request, HTTPException, status
from app.auth.jwt_manager import verify_access_token, verify_refresh_token, create_access_token
from app.repositories.user_repository import UserRepository
from app.database import SessionLocal
from app.models import User
from typing import Optional


def _extract_token(request: Request) -> Optional[str]:
    """Authorization 헤더에서 Bearer 토큰 추출"""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None


async def get_current_user_jwt(request: Request) -> User:
    """JWT 토큰으로 현재 사용자 가져오기 (인증 필수)

    Authorization: Bearer {access_token} 헤더 필요.
    인증되지 않은 경우 401 Unauthorized 에러 발생.
    """
    token = _extract_token(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 토큰이 필요합니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었거나 유효하지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="존재하지 않는 사용자입니다",
            )
        return user
    finally:
        db.close()


async def get_optional_user_jwt(request: Request) -> Optional[User]:
    """JWT 토큰으로 현재 사용자 가져오기 (인증 선택)

    토큰이 없거나 유효하지 않으면 None 반환 (에러 없음).
    """
    token = _extract_token(request)
    if not token:
        return None

    user_id = verify_access_token(token)
    if user_id is None:
        return None

    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        return user_repo.get_by_id(user_id)
    finally:
        db.close()
