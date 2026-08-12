"""커스텀 예외 클래스 (보너스: 전역 예외 처리)

FastAPI의 기본 예외 외에 도메인별 커스텀 예외를 정의합니다.
이 예외들은 app/main.py의 exception_handler에서 공통으로 처리됩니다.
"""


class AppException(Exception):
    """애플리케이션 기본 예외 (모든 커스텀 예외의 부모)"""
    def __init__(self, message: str, status_code: int = 400, error_code: str = "APP_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class NotFoundError(AppException):
    """리소스를 찾을 수 없음 (404)"""
    def __init__(self, resource: str, resource_id=None):
        msg = f"{resource}을(를) 찾을 수 없습니다" if resource_id is None else f"{resource} #{resource_id}을(를) 찾을 수 없습니다"
        super().__init__(msg, status_code=404, error_code="NOT_FOUND")


class PermissionDeniedError(AppException):
    """권한 없음 (403)"""
    def __init__(self, message: str = "이 작업을 수행할 권한이 없습니다"):
        super().__init__(message, status_code=403, error_code="PERMISSION_DENIED")


class ConflictError(AppException):
    """데이터 충돌 (409) — 중복, 이미 존재함"""
    def __init__(self, message: str):
        super().__init__(message, status_code=409, error_code="CONFLICT")


class ValidationError(AppException):
    """입력값 검증 실패 (422)"""
    def __init__(self, message: str):
        super().__init__(message, status_code=422, error_code="VALIDATION_ERROR")
