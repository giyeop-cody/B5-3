"""JWT 인증 API 라우터 (보너스: JWT 인증)

세션 기반 로그인/로그아웃을 JWT 기반으로 대체합니다.
- POST /api/jwt/login: 로그인 → access token + refresh token 발급
- POST /api/jwt/refresh: refresh token으로 access token 재발급
- POST /api/jwt/logout: 토큰 무효화 (블랙리스트)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from app.auth.service import AuthService
from app.auth.jwt_manager import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
    revoke_token,
)
from app.auth.jwt_dependencies import get_current_user_jwt
from app.repositories.user_repository import UserRepository
from app.database import get_db
from app.schemas import LoginRequest
from app.models import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/jwt", tags=["jwt-auth"])


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # 초 단위


class RefreshRequest(BaseModel):
    refresh_token: str


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repo = UserRepository(db)
    return AuthService(user_repo)


@router.post("/login", response_model=TokenResponse)
async def jwt_login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """JWT 로그인 — access token + refresh token 발급"""
    user = auth_service.authenticate(
        username=login_data.username,
        password=login_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다",
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    from app.config import JWT_ACCESS_EXPIRE
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=JWT_ACCESS_EXPIRE * 60,
    )


@router.post("/refresh", response_model=TokenResponse)
async def jwt_refresh(req: RefreshRequest):
    """Refresh Token으로 Access Token 재발급"""
    user_id = verify_refresh_token(req.refresh_token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh 토큰이 만료되었거나 유효하지 않습니다",
        )

    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id)

    from app.config import JWT_ACCESS_EXPIRE
    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        expires_in=JWT_ACCESS_EXPIRE * 60,
    )


@router.post("/logout")
async def jwt_logout(request: Request):
    """JWT 로그아웃 — 토큰을 블랙리스트에 추가하여 무효화"""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        revoke_token(token)
    return {"message": "로그아웃 완료 (토큰 무효화)"}


@router.get("/me")
async def jwt_me(current_user: User = Depends(get_current_user_jwt)):
    """현재 사용자 정보 (JWT 인증 필수)"""
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email}
