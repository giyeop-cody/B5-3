"""앱 설정"""
import os
import secrets

# 세션 비밀키 (세션 인증 + JWT 서명 공용)
# 운영: 환경변수 SECRET_KEY에서 고정값 로드
# 개발: 환경변수 없으면 랜덤 생성 (재시작 시 세션 초기화 — 개발 중이라 감수)
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))

# 세션 만료 시간 (초) - 24시간
SESSION_MAX_AGE = int(os.getenv("SESSION_MAX_AGE", 24 * 60 * 60))

# 데이터베이스 URL (기본: SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# JWT 설정 (보너스: JWT 인증)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_EXPIRE = int(os.getenv("JWT_ACCESS_EXPIRE", 30))  # 30분
JWT_REFRESH_EXPIRE = int(os.getenv("JWT_REFRESH_EXPIRE", 7))  # 7일
