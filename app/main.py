"""FastAPI 게시판 서비스 - 메인 앱"""
from fastapi import FastAPI, Request, Response
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import engine, Base
from app.routers import board_router, post_router, view_router, follow_router
from app.auth import router as auth_router
from app.auth.jwt_router import router as jwt_router
from app.config import SECRET_KEY, SESSION_MAX_AGE
import app.models
from app.startup import init_data

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI 게시판 서비스",
    description="인증/인가 기반 게시판 웹 서비스",
    version="0.3.0"
)


class NoCacheMiddleware(BaseHTTPMiddleware):
    """모든 HTML 응답에 캐시 방지 헤더 추가

    문제: 로그아웃 후 뒤로 가기 시 브라우저가 캐시된 HTML을 표시하여
    비공개 글, 수정/삭제 버튼, 마이페이지 등이 노출되는 버그 방지.
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


# 미들웨어 (순서 중요: NoCacheMiddleware가 가장 바깥)
app.add_middleware(NoCacheMiddleware)

# 세션 미들웨어 추가 (인증에 필요)
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=SESSION_MAX_AGE
)

# 라우터 등록
app.include_router(auth_router.router)
app.include_router(board_router.router)
app.include_router(post_router.router)
app.include_router(view_router.router)  # 화면 라우터
app.include_router(follow_router.router)  # 팔로우 API (회원 간 연결)
app.include_router(jwt_router)  # 보너스: JWT 인증 API


@app.on_event("startup")
async def startup_event():
    """앱 시작 시 DB 초기화"""
    init_data()  # 화면 라우터


@app.get("/api")
async def root():
    """API 정보"""
    return {
        "message": "Hello, FastAPI!",
        "service": "게시판 서비스",
        "docs": "/docs",
        "version": "0.3.0"
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "ok"}
