# FastAPI 게시판 서비스

FastAPI로 만든 인증/인가 기반 게시판 웹 서비스입니다.

## 🎯 프로젝트 개요

- **인증**: 세션 기반 로그인/로그아웃
- **인가**: 로그인 사용자만 게시글 작성/수정/삭제 가능
- **연관관계**: User ↔ Post ↔ Board (1:N 관계)
- **상태 변경**: 게시글 상태 관리 (초안 → 공개 → 비공개)

## 🛠️ 개발 환경

- Python: 3.10 이상
- 데이터베이스: SQLite (개발), PostgreSQL (운영 권장)

### 주요 패키지

| 패키지 | 용도 |
|--------|------|
| fastapi | 웹 프레임워크 |
| uvicorn | ASGI 서버 |
| sqlalchemy | ORM |
| jinja2 | 템플릿 엔진 |
| python-jose | JWT (보너스) |
| passlib[bcrypt] | 비밀번호 해싱 |
| itsdangerous | 세션 서명 |
| python-multipart | 폼 데이터 처리 |

## 📦 설치 및 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/giyeop-cody/B5-3.git
cd B5-3
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

### 화면 경로

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
| 보호 | `/posts/{id}/publish` | 게시글 공개 (로그인 필수) |
| 보호 | `/posts/{id}/hide` | 게시글 비공개 (로그인 필수) |
| 보호 | `/my-posts` | 내 글 목록 (로그인 필수) |
| 보호 | `/logout` | 로그아웃 (로그인 필수) |

### API 경로

| 구분 | 경로 | 설명 |
|------|------|------|
| 공개 | `GET /api/boards/` | 게시판 목록 |
| 공개 | `GET /api/boards/{id}` | 게시판 상세 |
| 공개 | `GET /api/posts/` | 게시글 목록 |
| 공개 | `GET /api/posts/{id}` | 게시글 상세 |
| 보호 | `POST /api/posts/` | 게시글 생성 |
| 보호 | `PUT /api/posts/{id}` | 게시글 수정 |
| 보호 | `DELETE /api/posts/{id}` | 게시글 삭제 |
| 보호 | `POST /api/posts/{id}/publish` | 게시글 공개 |
| 보호 | `POST /api/posts/{id}/hide` | 게시글 비공개 |
| 공개 | `POST /api/auth/login` | 로그인 |
| 공개 | `POST /api/auth/logout` | 로그아웃 |
| 공개 | `POST /api/auth/register` | 회원가입 |

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

---

## 🔐 인증 아키텍처 상세

### 인증 흐름 (세션 기반)

```
[로그인 요청]
  POST /login (username, password)
    ↓
AuthService.authenticate()
    ↓  (비밀번호 bcrypt 검증)
  성공 → login_user(request, user.id)
         → request.session["user_id"] = user.id
         → Set-Cookie: session=<signed_value>
    ↓
  실패 → 에러 메시지 반환 ("아이디 또는 비밀번호가 올바르지 않습니다")

[보호 경로 접근]
  GET /posts/new
    ↓
get_current_user_from_session(request)
    ↓  (request.session["user_id"] 확인)
  인증됨 → User 객체 반환 → 페이지 렌더링
  미인증 → RedirectResponse("/login")  (화면)
        → HTTPException(401)           (API)

[로그아웃]
  POST /logout
    ↓
logout_user(request)
    ↓  (request.session.pop("user_id"))
  → RedirectResponse("/")

[세션 만료]
  - max_age: 24시간 (SESSION_MAX_AGE = 86400초)
  - 만료 시 자동으로 비인증 상태로 처리
  - 서버 재시작 시 SECRET_KEY 변경으로 모든 세션 무효화
```

### 비인증 접근 시 메시지 표준

| 접근 유형 | 응답 | 메시지 |
|-----------|------|--------|
| 화면 (GET) | 302 Redirect | `/login` 페이지로 이동 |
| API (GET/POST) | 401 JSON | `{"detail": "로그인이 필요합니다"}` |
| 권한 부족 | 403 JSON | `{"detail": "자신의 게시글만 수정할 수 있습니다"}` |

### 요청 차단 정책: 미들웨어 vs Depends

본 프로젝트는 **Depends 기반 차단**을 주 정책으로 사용합니다.

| 방식 | 사용처 | 이유 |
|------|--------|------|
| **Depends** (주 정책) | 개별 라우터 | 엔드포인트별 세밀한 제어 가능 |
| **SessionMiddleware** (보조) | 전체 앱 | 세션 쿠키 파싱/저장만 담당 |

**선택 이유:**
- 미들웨어는 모든 요청에 적용되어 세밀한 제어가 어려움
- Depends는 라우터 단위로 인증 필요 여부를 명시적으로 선언 가능
- 공개/보호 경로를 코드에서 한눈에 파악 가능

### 인증 실패 시나리오

| 시나리오 | 처리 | 사용자 경험 |
|----------|------|-------------|
| 잘못된 아이디/비번 | 로그인 페이지에 에러 표시 | "아이디 또는 비밀번호가 올바르지 않습니다" |
| 세션 만료 | 자동 로그아웃 → 로그인 페이지 | 자연스럽게 로그인 유도 |
| 보호 경로 직접 접근 | 리다이렉트 또는 401 | 로그인 후 원래 페이지로 이동 |
| 타인 게시글 수정/삭제 | 403 Forbidden | "자신의 게시글만 수정할 수 있습니다" |
| 존재하지 않는 게시글 | 404 Not Found | 게시판 목록으로 리다이렉트 |

---

## 🔗 연관관계 설계 상세

### 모델 관계도

```
User (1) ──────< (N) Post (N) >────── (1) Board
 │                    │                    │
 ├─ id                ├─ id                ├─ id
 ├─ username          ├─ title             ├─ name
 ├─ password_hash     ├─ content           └─ description
 ├─ email             ├─ status
 └─ created_at        ├─ author_id (FK)
                      ├─ board_id (FK)
                      ├─ created_at
                      └─ updated_at
```

### 관계 설계 의도 및 삭제 정책

| 관계 | 방향 | cascade 정책 | 이유 |
|------|------|-------------|------|
| User → Post | 1:N | `cascade="all, delete-orphan"` | 사용자 탈퇴 시 작성한 글도 함께 삭제 |
| Post → User | N:1 | - (자식 측) | FK로 참조만 함 |
| Board → Post | 1:N | cascade 없음 | 게시판 삭제 시 게시글은 별도 처리 필요 |
| Post → Board | N:1 | - (자식 측) | FK로 참조만 함 |

**Board 삭제 시나리오:**
- 게시판 삭제 전, 해당 게시판의 게시글을 다른 게시판으로 이동하거나 수동 삭제
- 자동 삭제를 원하면 `cascade="all, delete-orphan"` 추가 가능
- 현재 정책: 게시판 삭제 시 FK 제약으로 인해 게시글이 있으면 삭제 불가 (안전 장치)

### ⚠️ 양방향 관계 주의사항 (순환참조 및 직렬화)

양방향 관계(`back_populates`) 사용 시 **순환참조** 문제가 발생할 수 있습니다.

**문제:**
```python
# User → posts → [Post → author → User → posts → ...] 무한 순환!
user.posts[0].author.posts[0].author...  # 무한 참조
```

**해결 방법 1: Pydantic `model_config` 활용**
```python
class PostResponse(BaseModel):
    id: int
    title: str
    author_id: int   # author 객 전체가 아닌 ID만 포함
    board_id: int    # board 객체 전체가 아닌 ID만 포함

    model_config = {"from_attributes": True}
```

**해결 방법 2: 중첩 응답 시 명시적 필드 선택**
```python
# user 응답에 posts 포함하되, post에는 author 포함하지 않음
class UserWithPostsResponse(BaseModel):
    id: int
    username: str
    posts: List[PostResponse]  # PostResponse에는 author 객체 없음

    model_config = {"from_attributes": True}
```

**해결 방법 3: Jinja2 템플릿에서 선택적 접근**
```html
<!-- 순환 없이 필요한 필드만 접근 -->
{% for post in user.posts %}
    <p>{{ post.title }} - {{ post.board.name }}</p>
{% endfor %}
```

**본 프로젝트의 적용:**
- API 응답에서는 `PostResponse`에 `author_id`, `board_id`만 포함 (객체 전체 X)
- Jinja2 템플릿에서는 `post.author.username` 등 필요한 필드만 선택적 접근
- JSON 직렬화 시 순환참조 발생하지 않도록 설계

### Pydantic ↔ SQLAlchemy 매핑 주의사항

```python
# SQLAlchemy 모델 → Pydantic 응답 변환 시
class PostResponse(BaseModel):
    id: int
    title: str
    status: PostStatus
    author_id: int    # FK 값만 포함 (관계 객체 X)
    board_id: int

    model_config = {"from_attributes": True}
    # from_attributes=True: SQLAlchemy 객체의 속성을 Pydantic 필드로 자동 매핑
    # 주의: 관계 필드(author, board)를 포함하면 순환참조 발생 가능
```

**주의사항:**
- `from_attributes=True`는 SQLAlchemy 객체를 dict처럼 접근
- 관계 객체 전체를 응답에 포함하면 JSON 직렬화 시 순환참조 발생
- FK ID만 포함하거나, 별도 응답 모델로 중첩 깊이 제한

---

## 💼 트랜잭션 관리

### 트랜잭션 경계

본 프로젝트는 **Repository 계층**에서 트랜잭션을 관리합니다.

```
Router → Service → Repository → DB
                    ↑
              commit/rollback here
```

| 계층 | 트랜잭션 책임 |
|------|--------------|
| Router | 트랜잭션 관여 안 함 |
| Service | 비즈니스 로직 수행, 예외 발생 시 Repository에 위임 |
| Repository | `db.commit()` / `db.rollback()` 책임 |

### 단일 작업 트랜잭션

```python
# repository/post_repository.py
def create(self, ...) -> Post:
    post = Post(...)
    self.db.add(post)
    self.db.commit()       # 성공 시 커밋
    self.db.refresh(post)
    return post
```

### 복합 작업 롤백 정책

여러 DB 조작이 포함된 비즈니스 작업의 경우:

```python
# services/post_service.py
def create_post(self, ...):
    # 1. 유효성 검증 (DB 접근 전)
    if not title:
        raise ValueError("제목은 필수입니다")  # DB 접근 없이 실패

    # 2. 단일 Repository 호출 (내부에서 commit)
    return self.post_repo.create(...)
```

**현재 정책:**
- 각 Service 메서드는 단일 Repository 호출로 구성
- 복합 작업이 필요한 경우, Repository 내에서 여러 조작 후 한 번에 commit
- 예외 발생 시 Repository의 `db.rollback()`으로 자동 롤백
- 추후 복잡한 트랜잭션이 필요하면 `db.begin()` 컨텍스트 매니저 사용 권장

---

## 🏗️ 프로젝트 구조 및 모듈별 역할

```
fastapi-auth-service/
├── app/
│   ├── auth/                    # 인증/인가 모듈
│   │   ├── dependencies.py      # Depends 함수 (get_current_user, get_optional_user)
│   │   ├── password.py          # hash_password(), verify_password()
│   │   ├── router.py            # /api/auth/* 엔드포인트 (login, logout, register)
│   │   ├── service.py           # AuthService.authenticate(), .register()
│   │   └── session.py           # login_user(), logout_user(), get_current_user_from_session()
│   │
│   ├── models/                  # SQLAlchemy ORM 모델
│   │   ├── user.py              # User 모델 + Post 양방향 관계
│   │   ├── board.py             # Board 모델 + Post 양방향 관계
│   │   └── post.py              # Post 모델 + PostStatus Enum + 관계 정의
│   │
│   ├── repositories/            # 데이터 접근 계층 (DB CRUD만 담당)
│   │   ├── user_repository.py   # get_by_id, get_by_username, create
│   │   ├── board_repository.py  # get_by_id, get_all, create
│   │   └── post_repository.py   # CRUD + search + update_status
│   │
│   ├── services/                # 비즈니스 로직 (유효성 검증, 권한 확인)
│   │   ├── board_service.py     # 게시판 관리 (중복 체크 등)
│   │   └── post_service.py      # 게시글 관리 (권한, 상태 변경 등)
│   │
│   ├── routers/                 # 요청/응답 처리 (HTTP 인터페이스)
│   │   ├── board_router.py      # /api/boards/* REST API
│   │   ├── post_router.py       # /api/posts/* REST API + 필터링/검색
│   │   └── view_router.py       # 화면 라우터 (Jinja2 SSR)
│   │
│   ├── templates/               # Jinja2 HTML 템플릿
│   │   ├── base.html            # 공통 레이아웃 (네비게이션, CSS)
│   │   ├── home.html            # 홈페이지
│   │   ├── login.html           # 로그인 페이지
│   │   ├── my_posts.html        # 내 글 목록
│   │   ├── boards/
│   │   │   ├── list.html        # 게시판 목록
│   │   │   └── detail.html      # 게시판 상세 + 게시글 목록
│   │   └── posts/
│   │       ├── detail.html      # 게시글 상세 + 상태 배지
│   │       ├── create.html      # 게시글 작성 폼
│   │       └── edit.html        # 게시글 수정 폼
│   │
│   ├── config.py                # SECRET_KEY, SESSION_MAX_AGE
│   ├── database.py              # SQLAlchemy engine, SessionLocal, get_db
│   ├── init_db.py               # 초기 데이터 생성 스크립트
│   ├── main.py                  # FastAPI 앱 + 미들웨어 + 라우터 등록
│   └── schemas.py               # Pydantic 요청/응답 스키마
│
├── requirements.txt
├── README.md
├── GITFLOW.md                   # Gitflow 브랜칭 전략 가이드
├── GITFLOW_SUMMARY.md           # Gitflow 적용 완료 보고서
└── IMPLEMENTATION_REPORT.md     # 구현 완료 보고서
```

---

## 📊 API 응답 예시 (연관관계 데이터)

### 게시글 상세 조회 (연관관계 포함)

```json
// GET /api/posts/1
{
  "id": 1,
  "title": "첫 번째 글",
  "content": "안녕하세요!",
  "status": "published",
  "author_id": 1,
  "board_id": 1,
  "created_at": "2026-07-10T13:24:00",
  "updated_at": "2026-07-10T13:25:00"
}
```

### 게시판 상세 조회 (게시글 목록 포함)

```json
// GET /api/boards/1
{
  "id": 1,
  "name": "자유게시판",
  "description": "자유롭게 이야기를 나누는 공간입니다."
}
```

### 템플릿에서의 연관 데이터 출력

```html
<!-- boards/detail.html: 게시판 → 게시글 목록 -->
{% for post in board.posts %}
    <li>
        <a href="/posts/{{ post.id }}">{{ post.title }}</a>
        <span class="badge badge-{{ post.status.value }}">{{ post.status.value }}</span>
        <small>by {{ post.author.username }}</small>
    </li>
{% endfor %}

<!-- posts/detail.html: 게시글 → 작성자 + 게시판 -->
<h2>{{ post.title }}</h2>
<p>작성자: {{ post.author.username }}</p>
<p>게시판: <a href="/boards/{{ post.board.id }}">{{ post.board.name }}</a></p>
```

### 상태 배지 표시 템플릿

```html
<!-- 상태별 배지 출력 -->
<span class="badge badge-{{ post.status.value }}">
    {% if post.status.value == 'draft' %}초안
    {% elif post.status.value == 'published' %}공개
    {% elif post.status.value == 'hidden' %}비공개
    {% endif %}
</span>

<!-- CSS -->
.badge-draft { background-color: #95a5a6; color: white; }
.badge-published { background-color: #27ae60; color: white; }
.badge-hidden { background-color: #f39c12; color: white; }
```

---

## 🔄 상태 변경 비즈니스 로직

### 상태 전이 다이어그램

```
  ┌─────────┐    publish     ┌───────────┐
  │  DRAFT  │ ─────────────→ │ PUBLISHED │
  │ (초안)  │ ←───────────── │  (공개)    │
  └─────────┘      hide      └───────────┘
       │                         │
       │  hide                   │  hide
       ↓                         ↓
  ┌─────────┐              ┌──────────┐
  │ HIDDEN  │ ←─────────── │ HIDDEN   │
  │ (비공개) │              │ (비공개)  │
  └─────────┘              └──────────┘
```

### 상태 변경 API

| 엔드포인트 | 전이 | 권한 |
|-----------|------|------|
| `POST /api/posts/{id}/publish` | DRAFT/HIDDEN → PUBLISHED | 작성자만 |
| `POST /api/posts/{id}/hide` | DRAFT/PUBLISHED → HIDDEN | 작성자만 |

---

## 🔧 운영 가이드

### SECRET_KEY 관리

```bash
# 개발 환경: config.py에 하드코딩 (현재 방식)
SECRET_KEY = secrets.token_urlsafe(32)

# 운영 환경: 환경변수로 관리 (권장)
# .env 파일
SECRET_KEY=your-production-secret-key-here

# main.py에서 로드
import os
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
```

**주의:**
- SECRET_KEY 변경 시 모든 기존 세션이 무효화됨
- 운영 환경에서는 반드시 고정된 안전한 키 사용
- Git에 커밋하지 말 것 (.env를 .gitignore에 추가)

### DB 마이그레이션 권장 절차

현재는 `Base.metadata.create_all()`로 테이블을 생성하지만, 운영 환경에서는 **Alembic** 사용을 권장합니다:

```bash
# Alembic 설치
pip install alembic

# 초기화
alembic init alembic

# 마이그레이션 생성
alembic revision --autogenerate -m "initial schema"

# 마이그레이션 적용
alembic upgrade head
```

---

## 🔐 세션 → JWT 전환 가이드

### 전환 시 변경 지점

| 파일 | 변경 내용 |
|------|----------|
| `auth/session.py` | → `auth/jwt.py`로 교체 (토큰 생성/검증) |
| `auth/dependencies.py` | `get_current_user` 내부 로직만 교체 (인터페이스 유지) |
| `main.py` | `SessionMiddleware` 제거 |
| `auth/router.py` | 로그인 응답에 `access_token` 포함 |
| `config.py` | `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` 추가 |

**장점:** `dependencies.py`의 `get_current_user` 인터페이스를 유지하면, 라우터 코드는 변경 불필요

### JWT 전환 시 고려사항 체크리스트

- [ ] 토큰 만료 시간 설정 (보통 15분~1시간)
- [ ] 리프레시 토큰 구현 (만료 후 재인증)
- [ ] 토큰 무효화 전략 (블랙리스트 또는 짧은 만료시간)
- [ ] CSRF 보호 (쿠키에 JWT 저장 시 필수)
- [ ] XSS 방어 (localStorage 저장 시 주의)
- [ ] 토큰 크기 관리 (페이로드 최소한으로)
- [ ] HTTPS 필수 (토큰 탈취 방지)

---

## 📝 개발 과정

이 프로젝트는 **Gitflow 브랜칭 전략**을 따라 단계별로 구현되었습니다:

1. **feature/step1-init**: 프로젝트 구조 잡기
2. **feature/step2-database**: 데이터베이스 모델 설계
3. **feature/step3-crud-api**: 기본 CRUD API 구현
4. **feature/step4-auth**: 인증 시스템 구축
5. **feature/step5-templates**: 화면 구현
6. **feature/step6-relationships**: 연관관계 활용
7. **release/1.0.0**: 릴리즈 준비
8. **main**: 프로덕션 배포

각 단계별 상세 내용은 Git 커밋 히스토리와 `GITFLOW_SUMMARY.md`를 참고하세요.

## 📄 라이선스

MIT License
