# FastAPI 게시판 서비스

FastAPI로 만든 인증/인가 기반 게시판 웹 서비스입니다.

## 🎯 프로젝트 개요

- **인증**: 세션 기반 로그인/로그아웃
- **인가**: 로그인 사용자만 게시글 작성/수정/삭제 가능
- **연관관계**: User ↔ Post ↔ Board (1:N 관계)
- **상태 변경**: 게시글 상태 관리 (초안 → 공개 → 비공개)

## 🛠️ 개발 환경

- Python: 3.10 이상
- 데이터베이스: SQLite

### 주요 패키지

- fastapi: 웹 프레임워크
- uvicorn: ASGI 서버
- sqlalchemy: ORM
- jinja2: 템플릿 엔진
- python-jose: JWT (보너스)
- passlib[bcrypt]: 비밀번호 해싱

## 📦 설치 및 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-auth-service.git
cd fastapi-auth-service
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 데이터베이스 초기화

```bash
python -m app.init_db
```

### 5. 서버 실행

```bash
uvicorn app.main:app --reload --port 8000
```

브라우저에서 http://localhost:8000 접속

## 🔑 테스트 계정

- **ID**: `testuser`
- **PW**: `test1234`

## 📋 공개/보호 경로 정책

| 구분 | 경로 | 설명 |
|------|------|------|
| 공개 | `/` | 홈페이지 |
| 공개 | `/login` | 로그인 페이지 |
| 공개 | `/boards` | 게시판 목록 |
| 공개 | `/boards/{id}` | 게시판 상세 |
| 공개 | `/posts/{id}` | 게시글 상세 (읽기) |
| 보호 | `/posts/new` | 게시글 작성 (로그인 필수) |
| 보호 | `/posts/{id}/edit` | 게시글 수정 (로그인 필수) |
| 보호 | `/posts/{id}/delete` | 게시글 삭제 (로그인 필수) |
| 보호 | `/logout` | 로그아웃 (로그인 필수) |

## 🚀 주요 기능

### 인증/인가
- 세션 기반 로그인/로그아웃
- 보호된 경로 접근 제어
- 인증 상태에 따른 UI 변화

### 게시판
- 여러 게시판 관리 (자유게시판, 질문게시판 등)
- 게시판별 게시글 목록 조회

### 게시글
- 게시글 CRUD (생성/조회/수정/삭제)
- 게시글 상태 관리 (초안/공개/비공개)
- 작성자만 수정/삭제 가능

### 연관관계
- 사용자별 작성한 게시글 목록
- 게시판별 게시글 필터링
- 양방향 관계 (User ↔ Post ↔ Board)

## 🏗️ 프로젝트 구조

```
fastapi-auth-service/
├── app/
│   ├── auth/           # 인증/인가 로직
│   │   ├── dependencies.py
│   │   ├── password.py
│   │   ├── router.py
│   │   ├── service.py
│   │   └── session.py
│   ├── models/         # SQLAlchemy ORM 모델
│   │   ├── board.py
│   │   ├── post.py
│   │   └── user.py
│   ├── repositories/   # 데이터 접근 계층
│   │   ├── board_repository.py
│   │   ├── post_repository.py
│   │   └── user_repository.py
│   ├── routers/        # API 라우터
│   │   ├── board_router.py
│   │   ├── post_router.py
│   │   └── view_router.py
│   ├── services/       # 비즈니스 로직
│   │   ├── board_service.py
│   │   └── post_service.py
│   ├── templates/      # Jinja2 템플릿
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── boards/
│   │   └── posts/
│   ├── static/         # 정적 파일 (CSS, JS)
│   ├── config.py       # 설정
│   ├── database.py     # DB 설정
│   ├── init_db.py      # DB 초기화 스크립트
│   ├── main.py         # FastAPI 앱
│   └── schemas.py      # Pydantic 스키마
├── requirements.txt
└── README.md
```

## 🔐 인증 방식 선택 사유

**세션 기반 인증**을 선택한 이유:

1. **학습 목적에 적합**: 구현이 상대적으로 간단하여 핵심 개념 이해에 집중 가능
2. **서버 제어**: 세션을 서버에서 직접 관리하므로 강제 로그아웃 등 세밀한 제어 가능
3. **보안성**: JWT보다 토큰 유출 시 대응이 용이 (즉시 세션 무효화 가능)
4. **SSR 친화적**: Jinja2 템플릿 기반 SSR과 잘 어울림

나중에 JWT 방식으로 전환할 수 있도록 인증 로직을 `auth/` 모듈로 분리하여 구현했습니다.

## 📝 개발 과정

이 프로젝트는 FitFlow 전략을 따라 단계별로 구현되었습니다:

1. **Step 1**: 프로젝트 구조 잡기
2. **Step 2**: 데이터베이스 모델 설계
3. **Step 3**: 기본 CRUD API 구현
4. **Step 4**: 인증 시스템 구축
5. **Step 5**: 화면 구현
6. **Step 6**: 연관관계 활용
7. **Step 7**: 상태 변경 비즈니스 로직
8. **Step 8**: 마무리 및 배포

각 단계별 상세 내용은 Git 커밋 히스토리를 참고하세요.

## 📄 라이선스

MIT License
