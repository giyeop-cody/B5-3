"""FastAPI 게시판 서비스 - 메인 앱"""
from fastapi import FastAPI

app = FastAPI(
    title="FastAPI 게시판 서비스",
    description="인증/인가 기반 게시판 웹 서비스",
    version="0.1.0"
)


@app.get("/")
async def root():
    """홈페이지 API"""
    return {"message": "Hello, FastAPI!", "service": "게시판 서비스"}


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "ok"}
