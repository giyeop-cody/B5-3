"""앱 설정"""
import secrets

# 세션 비밀키 (개발용 - 운영에서는 환경변수로 관리)
SECRET_KEY = secrets.token_urlsafe(32)

# 세션 만료 시간 (초) - 24시간
SESSION_MAX_AGE = 24 * 60 * 60
