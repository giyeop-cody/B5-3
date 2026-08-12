"""인증 서비스"""
from app.repositories.user_repository import UserRepository
from app.auth.password import verify_password
from app.models import User
from typing import Optional


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """사용자 인증
        
        Args:
            username: 사용자명
            password: 평문 비밀번호
            
        Returns:
           인증 성공 시 User 객체, 실패 시 None
        """
        # 사용자 조회
        user = self.user_repo.get_by_username(username)
        if not user:
            return None

        # 비밀번호 검증
        if not verify_password(password, user.password_hash):
            return None

        return user

    def register(self, username: str, password: str, email: str = None) -> User:
        """새 사용자 등록
        
        Args:
            username: 사용자명
            password: 평문 비밀번호
            email: 이메일 (선택)
            
        Returns:
            생성된 User 객체
            
        Raises:
            ValueError: 사용자명 또는 이메일 중복 시
        """
        from app.auth.password import hash_password

        # 사용자명 중복 체크
        if self.user_repo.get_by_username(username):
            raise ValueError(f"'{username}'은(는) 이미 사용 중인 아이디입니다")

        # 이메일 중복 체크
        if email and self.user_repo.get_by_email(email):
            raise ValueError(f"'{email}'은(는) 이미 사용 중인 이메일입니다")

        # 비밀번호 해싱
        password_hash = hash_password(password)

        # 사용자 생성
        return self.user_repo.create(
            username=username,
            password_hash=password_hash,
            email=email
        )
