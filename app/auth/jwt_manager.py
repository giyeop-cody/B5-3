"""JWT 토큰 관리 유틸리티 (보너스: JWT 인증)

세션 기반 인증을 JWT 기반으로 전환한 모듈입니다.
- access token: 로그인 후 API 요청 시 사용 (만료 30분)
- refresh token: access token 만료 시 재발급 (만료 7일)
- 토큰 무효화: 블랙리스트 (메모리 기반, 운영에서는 Redis 권장)
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from app.config import SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_EXPIRE, JWT_REFRESH_EXPIRE

# 토큰 블랙리스트 (메모리 기반 — 운영에서는 Redis 사용 권장)
_blacklist: set[str] = set()


def create_access_token(user_id: int) -> str:
    """Access Token 생성 (만료 30분)"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_EXPIRE)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    """Refresh Token 생성 (만료 7일)"""
    expire = datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_EXPIRE)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """토큰 디코딩 (만료/변조 시 None 반환)"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_access_token(token: str) -> Optional[int]:
    """Access Token 검증 → user_id 반환, 실패 시 None"""
    if token in _blacklist:
        return None
    payload = decode_token(token)
    if payload is None:
        return None
    if payload.get("type") != "access":
        return None
    return int(payload.get("sub", 0)) or None


def verify_refresh_token(token: str) -> Optional[int]:
    """Refresh Token 검증 → user_id 반환, 실패 시 None"""
    if token in _blacklist:
        return None
    payload = decode_token(token)
    if payload is None:
        return None
    if payload.get("type") != "refresh":
        return None
    return int(payload.get("sub", 0)) or None


def revoke_token(token: str):
    """토큰 무효화 (블랙리스트 추가)"""
    _blacklist.add(token)


def is_revoked(token: str) -> bool:
    """토큰이 블랙리스트에 있는지 확인"""
    return token in _blacklist
