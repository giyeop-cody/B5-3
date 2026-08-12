"""앱 설정"""
import os
import secrets

# 세션 비밀키
# 운영: 환경변수 SECRET_KEY에서 고정값 로드
# 개발: 환경변수 없으면 랜덤 생성 (재시작 시 세션 초기화 — 개발 중이라 감수)
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))

# 세션 만료 시간 (초) - 24시간
SESSION_MAX_AGE = int(os.getenv("SESSION_MAX_AGE", 24 * 60 * 60))

# 데이터베이스 URL
# 개발: SQLite (기본값, 별도 설치 불필요)
# 운영: PostgreSQL (환경변수로 URL 설정)
#   예: postgresql://user:password@host:port/dbname
#   Supabase: postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# 현재 DB 타입 (자동 감지)
DB_TYPE = "postgresql" if DATABASE_URL.startswith("postgresql") else "sqlite"
