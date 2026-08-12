# FastAPI 게시판 서비스

FastAPI로 만든 인증/인가 + 회원 간 팔로우 기반 게시판 웹 서비스입니다.

## 🎯 프로젝트 개요

- **인증**: 세션 기반 로그인/로그아웃
- **인가**: 로그인 사용자만 게시글 작성/수정/삭제 가능
- **회원 간 팔로우**: 사용자가 다른 사용자를 팔로우/언팔로우 (N:M 관계)
- **연관관계**: User ↔ Post ↔ Board (1:N), User ↔ User (N:M 팔로우)
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

### 4. 환경변수 설정 (운영)

```bash
cp .env.example .env
# .env 파일을 편집하여 실제 값으로 변경
```

> 📄 `.env.example` 파일에 모든 환경변수 항목이 정리되어 있습니다.

### 5. 데이터베이스 초기화

```bash
python -m app.init_db
```

### 5. 서버 실행

```bash
uvicorn app.main:app --reload --port 8000
```

브라우저에서 http://localhost:8000 접속

## 🔑 테스트 계정

| 계정 | 비밀번호 | 용도 |
|------|---------|------|
| `testuser` | `test1234` | 기본 테스트 계정 |
| `demo_user` | `demo1234` | 팔로우 데모용 (testuser가 이 계정을 팔로우) |

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
| 공개 | `/users/{id}` | 사용자 프로필 (팔로우 통계 + 팔로우/언팔로우 버튼) |
| 보호 | `/users/{id}/follow` | 팔로우 (로그인 필수) |
| 보호 | `/users/{id}/unfollow` | 언팔로우 (로그인 필수) |
| 공개 | `/users/{id}/following` | 팔로잉 목록 |
| 공개 | `/users/{id}/followers` | 팔로워 목록 |
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
| 보호 | `POST /api/users/{id}/follow` | 팔로우 (회원 간 연결) |
| 보호 | `DELETE /api/users/{id}/follow` | 언팔로우 |
| 공개 | `GET /api/users/{id}/following` | 팔로잉 목록 |
| 공개 | `GET /api/users/{id}/followers` | 팔로워 목록 |

## 🚀 주요 기능

### 인증/인가
- 세션 기반 로그인/로그아웃
- 보호된 경로 접근 제어
- 인증 상태에 따른 UI 변화
- 로그인 상태 표시: 네비게이션에 `OOO님` 표시 (향후 만료 예정 알림, 역할 표시 확장 가능)

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

### 회원 간 팔로우 (과제 핵심 요구)
- 사용자가 다른 사용자를 팔로우/언팔로우
- 팔로우 시 자기 자신 팔로우 금지, 중복 팔로우 방지 (UniqueConstraint)
- 사용자 프로필 페이지에서 팔로잉/팔로워 수 및 목록 확인
- Follow 조인 테이블로 User-User 간 N:M 관계 모델링
- 사용자 탈퇴 시 팔로우 관계 자동 삭제 (cascade)

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

### 비인증 접근 시 메시지 표준 (#2)

| 접근 유형 | 응답 코드 | 메시지 형식 | 실제 값 |
|-----------|----------|------------|---------|
| 화면 (GET) | 302 Redirect | `RedirectResponse` + flash | `/login?next={원래URL}` + flash category: "error" |
| API (GET/POST) | 401 JSON | `{"detail": "..."}` | `{"detail": "로그인이 필요합니다"}` |
| 권한 부족 (화면) | 302 Redirect | flash category: "error" | `"자신의 게시글만 수정할 수 있습니다"` |
| 권한 부족 (API) | 403 JSON | `{"detail": "..."}` | `{"detail": "자신의 게시글만 수정할 수 있습니다"}` |

### 직접 URL 보호 시 API vs 화면 동작 차이 (#3)

| 보호 경로 직접 접근 | 화면 (View) | API |
|---------------------|------------|-----|
| 미인증 사용자 | `302 → /login?next={URL}` | `401 {"detail": "로그인이 필요합니다"}` |
| 권한 없는 사용자 | `302 → /posts/{id}` + flash error | `403 {"detail": "자신의 게시글만..."}` |
| 존재하지 않는 리소스 | `302 → /boards` + flash error | `404 {"detail": "게시글을 찾을 수 없습니다"}` |

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

User (N) ──── Follow ──── (N) User  (회원 간 팔로우)
 │                            │
 ├─ follower_id (FK)          ├─ followed_id (FK)
 └─ created_at                └─ UniqueConstraint(follower_id, followed_id)
```

### 관계 설계 의도 및 삭제 정책 (#9)

#### Cascade 정책 다이어그램

```
┌──────────────┐                          ┌──────────────┐
│     User     │                          │    Board     │
│              │                          │              │
│ cascade=     │   1 : N                  │ cascade=     │   1 : N
│ "all,        │────────────────────┐     │ 없음         │────────────────┐
│ delete-      │                    │     │              │                │
│ orphan"      │                    │     │              │                │
└──────────────┘                    │     └──────────────┘                │
                                    │                                     │
     사용자 삭제 시                  ↓                                     ↓
     → 게시글 자동 삭제        ┌──────────────┐                    ┌──────────────┐
                              │     Post     │                    │     Post     │
                              │              │                    │              │
                              │ author_id(FK)│                    │ board_id(FK) │
                              │ board_id(FK) │                    │ author_id(FK)│
                              └──────────────┘                    └──────────────┘

삭제 동작:
  User 삭제 → Post 자동 삭제 ✅   (cascade="all, delete-orphan")
  Board 삭제 → Post 삭제 불가 ❌  (FK 제약 → 수동 처리 필요)
  Post 삭제 → User/Board 영향 없음
```

| 관계 | 방향 | cascade 정책 | 삭제 시 동작 | 이유 |
|------|------|-------------|-------------|------|
| User → Post | 1:N | `cascade="all, delete-orphan"` | 사용자 삭제 → 글 자동 삭제 | 탈퇴 시 데이터 정리 |
| Post → User | N:1 | - (자식 측) | 영향 없음 | FK로 참조만 |
| Board → Post | 1:N | cascade 없음 | 게시판 삭제 → FK 오류 | 게시글 보호 |
| Post → Board | N:1 | - (자식 측) | 영향 없음 | FK로 참조만 |

**Board 삭제 시 권장 절차 (#11):**
1. 게시판에 속한 게시글이 있는지 확인 (`board.posts` 확인)
2. 게시글이 있으면:
   - **옵션 A**: 다른 게시판으로 이동 (`UPDATE posts SET board_id = <새ID> WHERE board_id = <삭제ID>`)
   - **옵션 B**: 수동으로 게시글 모두 삭제 후 게시판 삭제
3. 게시글이 없으면: 게시판 바로 삭제 가능
4. 현재 정책: FK 제약으로 게시글이 있으면 게시판 삭제 불가 → `IntegrityError` 발생 → 사용자에게 "게시글이 존재하는 게시판은 삭제할 수 없습니다" flash 표시

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

**관계 필드 제외 방법 (#17):**
```python
# 방법 1: 응답 모델에서 관계 필드를 아예 선언하지 않음 (현재 방식)
class PostResponse(BaseModel):
    id: int
    title: str
    author_id: int   # author 객체가 아닌 ID만
    board_id: int    # board 객체가 아닌 ID만
    # author: User  ← 선언하지 않으면 자동 제외

# 방법 2: model_config에서 exclude 사용
class PostResponse(BaseModel):
    id: int
    title: str
    author: Optional[UserResponse] = None  # 필요시만 포함

    model_config = {"from_attributes": True}

# 응답 시 exclude
PostResponse.model_validate(post, from_attributes=True).model_dump(exclude={"author"})
```

**로딩 전략 권장 사항 (#9):**
- 기본 `lazy="select"` (지연 로딩): 현재 프로젝트에 적합, 접근 시 쿼리 실행
- N+1 쿼리 발생 시 `joinedload()` 사용: `db.query(Post).options(joinedload(Post.author))`
- 대량 조회 시 `selectinload()` 권장: IN 쿼리 하나로 관계 데이터 일괄 로딩

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

### 계층 간 인터페이스 및 예외 계약 (#8)

각 계층은 명확한 인터페이스와 예외 계약을 가집니다:

```
Router (HTTP 요청/응답)
  ↓ Depends
Service (비즈니스 로직)
  ↓ 호출
Repository (DB CRUD)
  ↓ 호출
Database (SQLAlchemy Session)
```

| 계층 | 공개 메서드 | 발생 예외 | 처리 주체 | 트랜잭션 책임 |
|------|------------|-----------|----------|-------------|
| **Repository** | `get_by_id()`, `create()`, `update()`, `delete()`, `get_all()`, `search()` | 없음 (None 반환) | Service | 단일 CRUD: 내부 `commit()` |
| **Service** | `get_post()`, `create_post()`, `update_post()`, `delete_post()`, `publish_post()`, `hide_post()` | `ValueError`, `PermissionError` | Router | 단일 호출 위임, 복합 작업 시 직접 관리 |
| **Router** | HTTP 엔드포인트 | `HTTPException(400/401/403/404)` | FastAPI | 관여 안 함 |

```python
# Router: Service 예외를 HTTP 응답으로 변환
@router.post("/posts/{id}/publish")
async def publish_post(post_id: int, user = Depends(get_current_user)):
    try:
        return post_service.publish_post(post_id, user.id)
    except ValueError as e:           # Service → ValueError
        raise HTTPException(400, str(e))  # Router → HTTP 400
    except PermissionError as e:      # Service → PermissionError
        raise HTTPException(403, str(e))  # Router → HTTP 403
```

### 화면 라우터의 예외 처리 전략 (#16)

화면 라우터(view_router.py)는 **flash message** 패턴을 사용합니다:

```python
# 성공 시: flash 메시지 저장 + 리다이렉트
set_flash(request, "success", "게시글이 작성되었습니다.")
return RedirectResponse(url=f"/posts/{post.id}", status_code=302)

# 실패 시: flash 에러 메시지 저장 + 리다이렉트
except PermissionError:
    set_flash(request, "error", "자신의 게시글만 삭제할 수 있습니다.")
    return RedirectResponse(url=f"/posts/{post_id}", status_code=302)
```

모든 템플릿은 `base.html`에서 flash 메시지를 자동으로 표시합니다:
```html
{% if flash %}
    <div class="alert alert-{{ flash.category }}" role="alert">
        {{ flash.message }}
    </div>
{% endif %}
```

---

### 권한별 메뉴 확장 가이드 (#4)

현재는 로그인/비로그인만 구분하지만, 역할(Role) 기반 확장이 가능합니다:

```python
# models/user.py에 role 필드 추가
class User(Base):
    role = Column(String, default="user")  # "user", "admin"

# templates/base.html에서 역할별 분기
{% if user %}
    {% if user.role == 'admin' %}
        <a href="/admin">관리자</a>
    {% endif %}
    <a href="/my-posts">내 글</a>
{% endif %}
```

**확장 시 주의사항:**
- 역할은 Enum으로 정의 권장 (`UserRole.USER`, `UserRole.ADMIN`)
- 관리자 전용 라우터는 별도 `admin_router.py`로 분리
- Depends에서 역할 검증 추가: `get_admin_user()`

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

### curl 기반 전체 흐름 테스트 (#5, #7, #17)

```bash
# 1. 서버 시작
uvicorn app.main:app --reload --port 8000

# 2. 로그인 (세션 쿠키 저장)
$ curl -c cookies.txt -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "test1234"}'
# 응답: {"message":"로그인 성공","username":"testuser"}

# 3. 게시판 목록 조회 (공개)
$ curl -s http://localhost:8000/api/boards/
# 응답:
[
  {"name":"자유게시판","description":"자유롭게 이야기를 나누는 공간입니다.","id":1},
  {"name":"질문게시판","description":"궁금한 점을 질문하고 답변을 받는 공간입니다.","id":2}
]

# 4. 게시글 작성 (인증 필수 - 쿠키 사용)
$ curl -b cookies.txt -X POST http://localhost:8000/api/posts/ \
    -H "Content-Type: application/json" \
    -d '{"title": "첫 번째 글", "content": "안녕하세요!", "board_id": 1}'
# 응답:
{
  "title": "첫 번째 글",
  "content": "안녕하세요!",
  "id": 1,
  "status": "draft",
  "author_id": 1,        ← FK ID만 포함 (author 객체 X → 순환참조 방지 #17)
  "board_id": 1,         ← FK ID만 포함 (board 객체 X → 순환참조 방지 #17)
  "created_at": "2026-07-10T13:24:00",
  "updated_at": "2026-07-10T13:24:00"
}

# 5. 비인증 접근 시도 → 401
$ curl -X POST http://localhost:8000/api/posts/ \
    -H "Content-Type: application/json" \
    -d '{"title": "테스트", "content": "", "board_id": 1}'
# 응답: {"detail":"로그인이 필요합니다"}  (HTTP 401)

# 6. 게시글 공개 (상태 변경)
$ curl -b cookies.txt -X POST http://localhost:8000/api/posts/1/publish
# 응답: {"title":"첫 번째 글", ..., "status":"published", ...}

# 7. 내 글 목록 조회 (연관관계 활용)
$ curl -b cookies.txt http://localhost:8000/api/posts/?author_id=1
# 응답: [{"id":1, "title":"첫 번째 글", "status":"published", "author_id":1, ...}]

# 8. 로그아웃
$ curl -b cookies.txt -X POST http://localhost:8000/api/auth/logout
# 응답: {"message":"로그아웃 완료"}
```

### 순환참조 없음 증명 (#17)

위 API 응답에서 `PostResponse`는 `author_id`(int)와 `board_id`(int)만 포함합니다.  
`author`(User 객체)나 `board`(Board 객체) 전체를 포함하지 않으므로 JSON 직렬화 시 순환참조가 발생하지 않습니다.

```json
// ✅ 안전: ID만 포함
{"id": 1, "title": "글", "author_id": 1, "board_id": 1}

// ❌ 순환참조 발생: 객체 전체 포함 시
{"id": 1, "title": "글", "author": {"id": 1, "username": "test", "posts": [{"id": 1, "author": {"id": 1, "posts": [...]}}]}}
```

### 엔드투엔드 통합 테스트 순서 (#16)

```bash
# 전체 흐름: 로그인 → 게시글 작성 → 상태 변경 → 조회 → 로그아웃

# 1. 로그인
curl -c cookies.txt -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test1234"}'
# → {"message":"로그인 성공","username":"testuser"}

# 2. 게시글 작성 + 상태 변경
curl -b cookies.txt -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title":"통합테스트","content":"내용","board_id":1}'
# → {"id":1, "status":"draft", ...}
curl -b cookies.txt -X POST http://localhost:8000/api/posts/1/publish
# → {"status":"published", ...}

# 3. 결과 확인 + 로그아웃
curl -b cookies.txt http://localhost:8000/api/posts/1
# → {"status":"published", ...}
curl -b cookies.txt -X POST http://localhost:8000/api/auth/logout
# → {"message":"로그아웃 완료"}
```

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

### 상태 전이 후 UI 변화 (#6)

상태 변경 시 버튼/배지가 즉시 업데이트됩니다:

| 상태 | 배지 | 표시 버튼 | flash 메시지 |
|------|------|----------|-------------|
| `draft` | `🔘 초안` (회색) | [공개하기] | "게시글이 공개되었습니다." |
| `published` | `🟢 공개` (초록) | [비공개로 변경] | "게시글이 비공개로 변경되었습니다." |
| `hidden` | `🟡 비공개` (노랑) | [공개하기] | "게시글이 공개되었습니다." |

```html
<!-- posts/detail.html: 상태별 조건부 버튼 렌더링 -->
{% if post.status.value == 'draft' or post.status.value == 'hidden' %}
    <button type="submit" class="btn btn-success">공개하기</button>
{% endif %}
{% if post.status.value == 'published' %}
    <button type="submit" class="btn btn-secondary">비공개로 변경</button>
{% endif %}
```

### 복합 작업 트랜잭션 패턴 (#10, #15)

여러 Repository를 호출하는 복합 작업의 권장 패턴:

```python
# 권장: Service에서 Session을 직접 관리
from sqlalchemy.orm import Session

class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.stock_repo = StockRepository(db)

    def place_order(self, user_id: int, items: list):
        """복합 작업: 주문 생성 + 재고 감소 (원자적 처리)"""
        try:
            # 1. 모든 검증 먼저 수행
            for item in items:
                stock = self.stock_repo.get_by_product(item.product_id)
                if not stock or stock.quantity < item.quantity:
                    raise ValueError(f"재고 부족: {item.product_id}")

            # 2. 트랜잭션 내에서 모든 DB 조작
            order = self.order_repo.create(user_id=user_id, items=items)
            for item in items:
                self.stock_repo.decrease(item.product_id, item.quantity)

            self.db.commit()  # 한 번에 커밋
            return order

        except Exception:
            self.db.rollback()  # 실패 시 전체 롤백
            raise
```

**트랜잭션 패턴 요약:**

| 패턴 | 사용 시기 | 방법 |
|------|----------|------|
| 단일 Repository | 현재 프로젝트 | 각 repo에서 `commit()` |
| 다중 Repository | 복합 작업 | Service에서 `db.commit()` / `db.rollback()` |
| 중첩 트랜잭션 | 부분 실패 허용 | `db.begin_nested()` (savepoint) |

### 미들웨어 + Depends 조합 시 우선순위 (#13)

```
요청 → SessionMiddleware (세션 쿠키 파싱)
        → [라우터 매칭]
        → Depends(get_current_user) (인증 확인)
        → 엔드포인트 함수 실행
```

| 시나리오 | 처리 위치 | 이유 |
|----------|----------|------|
| 세션 쿠키 파싱 | SessionMiddleware | 모든 요청에서 공통 |
| 인증 필요 여부 | Depends | 엔드포인트별로 다름 |
| CORS 처리 | CORSMiddleware | 모든 요청에서 공통 |
| 로깅 | 커스텀 미들웨어 | 모든 요청에서 공통 |

**권장 조합:**
- 미들웨어: 모든 요청에 공통으로 적용할 것 (세션, CORS, 로깅)
- Depends: 엔드포인트별로 다르게 적용할 것 (인증, 권한, 유효성 검증)
- 충돌 방지: 미들웨어에서 인증을 강제하지 말 것 (Depends와 중복)
- 예외 사례: IP 차단, Rate Limiting은 미들웨어로 적용 (모든 요청에 공통 차단 필요)

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

### 전환 시 변경 지점 (#12)

| 파일 | 변경 내용 |
|------|----------|
| `auth/session.py` | → `auth/jwt.py`로 교체 (토큰 생성/검증) |
| `auth/dependencies.py` | `get_current_user` 내부 로직만 교체 (인터페이스 유지) |
| `main.py` | `SessionMiddleware` 제거 |
| `auth/router.py` | 로그인 응답에 `access_token` 포함 |
| `config.py` | `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` 추가 |

**장점:** `dependencies.py`의 `get_current_user` 인터페이스를 유지하면, **라우터 코드는 변경 불필요**

### JWT 버전 의존성 코드 예시 (#12)

```python
# auth/jwt.py (auth/session.py 대체)
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return int(payload["sub"])

# auth/dependencies.py (세션 버전 → JWT 버전 교체)
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """인터페이스는 동일! 라우터 코드 변경 불필요"""
    try:
        user_id = decode_access_token(credentials.credentials)
        db = SessionLocal()
        user = UserRepository(db).get_by_id(user_id)
        db.close()
        if not user:
            raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")
```

### JWT 전환 구현 우선순위 (#18)

| 우선순위 | 항목 | 이유 |
|----------|------|------|
| **P0 (필수)** | Access Token 만료 설정 | 보안 기본 요건 (15분~1시간 권장) |
| **P0 (필수)** | HTTPS 적용 | 토큰 탈취 방지 |
| **P1 (권장)** | Refresh Token | UX 개선 (재로그인 없이 토큰 갱신) |
| **P1 (권장)** | 토큰 무효화 (블랙리스트) | 로그아웃/비밀번호 변경 시 즉시 무효화 |
| **P2 (선택)** | CSRF 보호 | 쿠키에 JWT 저장 시 필수 |
| **P2 (선택)** | XSS 방어 | localStorage 저장 시 주의 |
| **P3 (최적화)** | 토큰 크기 최소화 | 네트워크 효율 |

### JWT 전환 체크리스트 (권장 값 포함) (#18)

- [x] 전환 시 변경 지점 문서화
- [x] JWT 버전 `get_current_user` 코드 예시
- [x] 구현 우선순위 정리
- [ ] Access Token 만료: **15분~30분** (짧을수록 안전, `ACCESS_TOKEN_EXPIRE_MINUTES=30`)
- [ ] Refresh Token 만료: **7일~14일** (`REFRESH_TOKEN_EXPIRE_DAYS=7`)
- [ ] HTTPS 필수: 프로덕션에서는 `Secure` 쿠키 + `HSTS` 헤더
- [ ] Refresh Token 회전: 사용 시 새 토큰 발급 + 이전 토큰 무효화
- [ ] 토큰 무효화: Redis 블랙리스트 또는 DB revocation 테이블
- [ ] CSRF 보호: `SameSite=Strict` 쿠키 또는 CSRF 토큰 (`csrfProtect`)
- [ ] XSS 방어: HttpOnly 쿠키에 JWT 저장 (`document.cookie` 접근 불가)
- [ ] 알고리즘 고정: `HS256` 또는 `RS256` 명시 (algorithm confusion 방지)

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
