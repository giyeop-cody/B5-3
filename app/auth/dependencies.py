"""인증 의존성 (Depends)"""
from fastapi import Request, HTTPException, status
from app.auth.session import get_current_user_from_session
from app.models import User
from typing import Optional


async def get_current_user(request: Request) -> User:
    """현재 로그인한 사용자 가져오기 (인증 필수)
    
    인증되지 않은 경우 401 Unauthorized 에러 발생
    """
    user = get_current_user_from_session(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요합니다"
        )
    return user


async def get_optional_user(request: Request) -> Optional[User]:
    """현재 사용자 가져오기 (인증 선택)
    
    인증되지 않은 경우 None 반환 (에러 없음)
    """
    return get_current_user_from_session(request)
