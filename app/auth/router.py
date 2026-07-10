"""인증 API 라우터"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.auth.service import AuthService
from app.auth.session import login_user, logout_user
from app.schemas import LoginRequest, LoginResponse, UserCreate, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """AuthService 의존성 주입"""
    user_repo = UserRepository(db)
    return AuthService(user_repo)


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    """로그인"""
    user = auth_service.authenticate(
        username=login_data.username,
        password=login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다"
        )

    # 세션에 사용자 ID 저장
    login_user(request, user.id)

    return LoginResponse(
        message="로그인 성공",
        username=user.username
    )


@router.post("/logout")
async def logout(request: Request):
    """로그아웃"""
    logout_user(request)
    return {"message": "로그아웃 완료"}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """회원가입"""
    try:
        user = auth_service.register(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
