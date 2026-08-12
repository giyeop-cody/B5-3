"""OAuth2 소셜 로그인 라우터 (보너스: OAuth2)

GitHub OAuth2 소셜 로그인을 구현합니다.
- GET /api/oauth/github/login: GitHub 로그인 페이지로 리다이렉트
- GET /api/oauth/github/callback: GitHub에서 콜백 받아 사용자 인증

환경변수:
  GITHUB_CLIENT_ID: GitHub OAuth App Client ID
  GITHUB_CLIENT_SECRET: GitHub OAuth App Client Secret
  OAUTH_REDIRECT_URI: 콜백 URL (예: http://localhost:8000/api/oauth/github/callback)

GitHub OAuth App 생성:
  1. https://github.com/settings/developers → "New OAuth App"
  2. Application name: B5-3 OAuth
  3. Homepage URL: http://localhost:8000
  4. Authorization callback URL: http://localhost:8000/api/oauth/github/callback
  5. Client ID와 Client Secret을 .env에 설정
"""
import os
import httpx
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from app.auth.session import login_user
from app.auth.password import hash_password
from app.repositories.user_repository import UserRepository
from app.database import SessionLocal

router = APIRouter(prefix="/api/oauth", tags=["oauth"])

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "")
OAUTH_REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:8000/api/oauth/github/callback")

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


@router.get("/github/login")
async def github_login():
    """GitHub OAuth2 로그인 — GitHub 로그인 페이지로 리다이렉트"""
    if not GITHUB_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GITHUB_CLIENT_ID 환경변수가 설정되지 않았습니다",
        )

    redirect_url = (
        f"{GITHUB_AUTH_URL}"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={OAUTH_REDIRECT_URI}"
        f"&scope=user:email"
    )
    return RedirectResponse(url=redirect_url, status_code=302)


@router.get("/github/callback")
async def github_callback(request: Request, code: str = ""):
    """GitHub OAuth2 콜백 — 인증 코드로 토큰 교환 후 사용자 정보 조회"""
    if not code:
        raise HTTPException(status_code=400, detail="인증 코드가 없습니다")

    # 1. 인증 코드로 access token 교환
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": OAUTH_REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
        )

    token_data = token_resp.json()
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="GitHub 인증에 실패했습니다",
        )

    # 2. access token으로 GitHub 사용자 정보 조회
    async with httpx.AsyncClient() as client:
        user_resp = await client.get(
            GITHUB_USER_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    github_user = user_resp.json()
    github_id = github_user.get("id")
    github_login = github_user.get("login")
    github_email = github_user.get("email")

    if not github_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="GitHub 사용자 정보를 가져올 수 없습니다",
        )

    # 3. DB에서 사용자 찾기 또는 생성 (OAuth 사용자 자동 가입)
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)

        # GitHub 사용자명으로 찾기 (oauth_github_ 접두사)
        oauth_username = f"github_{github_login}"
        user = user_repo.get_by_username(oauth_username)

        if not user:
            # 자동 회원가입 (랜덤 비밀번호 — 소셜 로그인이므로 비밀번호 사용 안 함)
            import secrets as py_secrets
            random_password = py_secrets.token_urlsafe(32)
            user = user_repo.create(
                username=oauth_username,
                password_hash=hash_password(random_password),
                email=github_email,
            )

        # 4. 세션에 로그인 처리
        login_user(request, user.id)

        return {
            "message": f"GitHub 로그인 성공: {github_login}",
            "username": user.username,
        }
    finally:
        db.close()
