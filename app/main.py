"""FastAPI 게시판 서비스 - 메인 앱"""
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import board_router, post_router
import app.models  # 모델을 임포트해야 테이블이 생성됨

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI 게시판 서비스",
    description="인증/인가 기반 게시판 웹 서비스",
    version="0.1.0"
)

# API 라우터 등록
app.include_router(board_router.router)
app.include_router(post_router.router)


@app.get("/")
async def root():
    """홈페이지 API"""
    return {
        "message": "Hello, FastAPI!",
        "service": "게시판 서비스",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "ok"}
