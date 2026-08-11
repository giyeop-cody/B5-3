# B5-3 동료평가 시나리오 — 학습 → 고찰 → 시도 → 수정 → 선택 → 트러블슈팅

> **과제**: 로그인이 되고 회원끼리 연결되는 웹 서비스 만들기
> **과목**: 데이터베이스와 백엔드 | **난이도**: ★★★ | **과제번호**: 185014
> **GitHub**: giyeop-cody/B5-3 | **실행**: `uvicorn app.main:app --reload --port 8000`
> **테스트 계정**: testuser / test1234

---

## 1. 학습

### 1-1. 인증 (Authentication)과 인가 (Authorization)

인증은 "너 누구야?"를 확인하는 것이다. 로그인 시 아이디/비밀번호로 신원을 확인하고, 세션에 user_id를 저장한다. 인가는 "너 이거 해도 돼?"를 확인하는 것이다. 로그인한 사용자가 자신의 글만 수정할 수 있도록 권한을 검사한다. 이 둘은 다르다: 로그인됐다고 모든 것을 할 수 있는 게 아니다.

### 1-2. 세션 기반 인증

HTTP는 상태를 유지하지 않는다(stateless). 매 요청마다 서버는 "이 사람이 누군지" 잊어버린다. 세션은 이것을 해결한다: 로그인 성공 시 `request.session["user_id"] = user.id`로 저장하고, 이후 요청에서 쿠키의 세션 ID로 사용자를 식별한다. `itsdangerous`로 세션 값을 서명하여 변조를 방지한다.

### 1-3. 비밀번호 해싱 (bcrypt)

비밀번호를 평문으로 DB에 저장하면 DB 해킹 시 모든 사용자의 비밀번호가 노출된다. bcrypt로 해싱하면 원문을 되돌릴 수 없다. 회원가입 시 `hash_password("test1234")` → 해시값 저장, 로그인 시 `verify_password("test1234", 해시값)` → 일치 여부 확인. bcrypt는 의도적으로 느리게 동작하여 무차별 대입 공격을 어렵게 만든다.

### 1-4. FastAPI Depends (의존성 주입)

`Depends(get_current_user)`를 보호 경로에 붙이면, FastAPI가 엔드포인트 실행 전에 먼저 `get_current_user`를 실행한다. 이 함수가 세션에서 user_id를 확인하여 User 객체를 반환하면 엔드포인트가 실행되고, 인증 실패 시 예외를 발생시켜 엔드포인트가 실행되지 않는다. 라우터 코드는 변경하지 않고 Depends만 붙이면 된다.

### 1-5. SQLAlchemy 연관관계

`User`와 `Post`는 1:N 관계이다. `Post.author_id = Column(ForeignKey("users.id"))`로 외래키를 정의하고, `relationship("User", back_populates="posts")`로 객체 단위 접근을 가능하게 한다. `back_populates`로 양방향: `user.posts`로 사용자의 글 목록을, `post.author`로 글의 작성자를 바로 조회할 수 있다.

회원 간 팔로우 관계는 `Follow` 조인 테이블로 N:M 관계를 모델링한다. `follows` 테이블에 `follower_id`와 `followed_id` 두 개의 FK를 두어 User-User 간 연결을 표현한다. `User.following_assoc`(내가 팔로우하는 목록)과 `User.followers_assoc`(나를 팔로우하는 목록)으로 양방향 접근하며, `UniqueConstraint("follower_id", "followed_id")`로 중복 팔로우를 방지한다.

### 1-6. 상태 전이 (PostStatus)

게시글은 DRAFT(초안) → PUBLISHED(공개) → HIDDEN(비공개) 상태를 가진다. 상태 변경은 Service 계층에서 검증한다: 이미 공개된 글을 다시 공개하려 하면 `ValueError("이미 공개된 게시글입니다")`. 이것이 단순 CRUD가 아닌 비즈니스 로직이다.

---

## 2. 고찰

### 2-1. 인증과 인가의 차이

| | 인증 (Authentication) | 인가 (Authorization) |
|---|---|---|
| 질문 | "너 누구야?" | "너 이거 해도 돼?" |
| 시점 | 로그인할 때 | 모든 보호 경로 접근 시 |
| 구현 | `login_user()` 세션 저장 | `Depends(get_current_user)` 권한 검사 |
| 예시 | testuser로 로그인 | testuser는 자기 글만 수정 |

### 2-2. Depends vs 미들웨어

미들웨어는 모든 요청에 강제 적용된다. 공개 경로(`/`, `/login`, `/boards`)도 예외 처리해야 하므로 복잡해진다. Depends는 엔드포인트별로 선택적으로 적용할 수 있어 "이 경로는 인증 필요"를 코드에서 명시적으로 선언할 수 있다. 본 프로젝트는 Depends를 주 정책으로, 미들웨어는 세션 쿠키 파싱만 담당한다.

### 2-3. 순환참조 — 양방향 관계의 함정

`User → posts → [Post → author → User → posts → ...]` 무한 순환이 발생한다. JSON 직렬화 시 `RecursionError`가 발생하므로, Pydantic 응답 모델에서는 `author_id`(int)만 포함하고 `author`(User 객체)는 제외한다. Jinja2 템플릿에서는 `post.author.username`처럼 필요한 필드만 선택적 접근한다.

### 2-4. 상태 변경 로직의 위치

상태 전이 검증(DRAFT→PUBLISHED 가능, PUBLISHED→PUBLISHED 불가)은 비즈니스 로직이므로 Service 계층에 둔다. 라우터는 HTTP 요청/응답만 담당하고, Service의 `ValueError`/`PermissionError`를 `HTTPException`으로 변환한다.

---

## 3. 시도

### 3-1. 계층 구조

```
auth/          → 인증 모듈
  dependencies.py  → get_current_user (Depends용)
  password.py      → hash_password(), verify_password() (bcrypt)
  router.py        → POST /api/auth/login, /logout, /register
  service.py       → AuthService.authenticate(), .register()
  session.py       → login_user(), logout_user(), get_current_user_from_session()

models/        → SQLAlchemy ORM
  user.py           → User (id, username, password_hash, email, posts)
  board.py          → Board (id, name, description, posts)
  post.py           → Post (id, title, content, status, author_id, board_id) + PostStatus Enum

repositories/  → DB CRUD만
  user_repository.py   → get_by_id, get_by_username, create
  board_repository.py  → get_by_id, get_all, create
  post_repository.py   → CRUD + search + update_status

services/      → 비즈니스 로직
  board_service.py     → 게시판 관리
  post_service.py      → 권한 검사, 상태 전이 검증

routers/       → HTTP 요청/응답
  board_router.py      → /api/boards/* REST API
  post_router.py       → /api/posts/* REST API + 필터링
  view_router.py       → 화면 라우터 (Jinja2 SSR)

templates/     → Jinja2
  base.html, home.html, login.html, my_posts.html
  boards/list.html, boards/detail.html
  posts/detail.html, posts/create.html, posts/edit.html
```

### 3-2. 인증 흐름

```
[로그인] POST /login (username, password)
  → AuthService.authenticate() → bcrypt 검증
  → 성공: login_user(request, user.id) → session["user_id"] = user.id → Set-Cookie
  → 실패: "아이디 또는 비밀번호가 올바르지 않습니다"

[보호 경로] GET /posts/new
  → Depends(get_current_user) → 세션에서 user_id 확인
  → 인증됨: User 객체 주입 → 페이지 렌더링
  → 미인증: RedirectResponse("/login?next=/posts/new") (화면)
            HTTPException(401) (API)

[권한 검사] POST /posts/{id}/edit
  → Service: if post.author_id != user_id: raise PermissionError
  → Router: except PermissionError → HTTPException(403) or flash + redirect

[로그아웃] POST /logout
  → logout_user(request) → session.pop("user_id")
  → RedirectResponse("/")
```

### 3-3. 연관관계 및 cascade 정책

| 관계 | 방향 | cascade | 삭제 시 |
|------|------|---------|--------|
| User → Post | 1:N | `all, delete-orphan` | 사용자 탈퇴 → 글 자동 삭제 |
| Post → User | N:1 | - | 영향 없음 |
| Board → Post | 1:N | 없음 | 게시판 삭제 → FK 오류 (글 보호) |
| User → User (팔로우) | N:M | `all, delete-orphan` | 사용자 탈퇴 → 팔로우 관계 자동 삭제 |

### 3-4. 상태 전이

```
DRAFT (초안) ──publish──→ PUBLISHED (공개)
     │                        │
     └────── hide ──────→ HIDDEN (비공개) ←── hide ──┘
                            HIDDEN ──publish──→ PUBLISHED
```

| 엔드포인트 | 전이 | 권한 |
|-----------|------|------|
| `POST /api/posts/{id}/publish` | DRAFT/HIDDEN → PUBLISHED | 작성자만 |
| `POST /api/posts/{id}/hide` | DRAFT/PUBLISHED → HIDDEN | 작성자만 |

---

## 4. 수정

| 수정 항목 | 수정 전 | 수정 후 | 이유 |
|----------|--------|--------|------|
| 인증 방식 | JWT 계획 | 세션 기반 | 단일 서버, 즉시 로그아웃, 구현 단순 |
| 비밀번호 저장 | 평문 | bcrypt 해싱 | 보안 기본 — 평문 절대 금지 |
| 권한 검사 위치 | 라우터에서 직접 | Service에서 PermissionError → Router가 HTTPException 변환 | 역할 분리 |
| 순환참조 | 응답에 User 객체 포함 | PostResponse에 author_id(int)만 포함 | JSON 직렬화 무한 루프 방지 |
| 화면 에러 처리 | 빈 화면 | flash 메시지 + 리다이렉트 | 사용자에게 "왜 안 되는지" 알려줌 |
| SECRET_KEY | 매번 랜덤 생성 | 개발=랜덤, 운영=.env 고정값 | 서버 재시작 시 세션 유지 |
| 비인증 접근 | 401 빈 화면 | 화면=302 리다이렉트 `/login?next=..`, API=401 JSON | 화면은 UX, API는 명확한 코드 |

---

## 5. 선택과 선정

| 선택 기로 | 선택 | 포기한 것 | 근거 |
|----------|------|----------|------|
| 세션 vs JWT | 세션 | 수평 확장 용이성 | 단일 서버, 즉시 로그아웃, 구현 단순 |
| cascade 정책 | User→Post cascade, Board→Post 없음 | 일관성 | 탈퇴 시 글 삭제 vs 게시판 삭제 시 글 보호 |
| Depends vs 미들웨어 | Depends 주 정책 | 전역 강제 | 공개/보호 경로 명시적 구분, 세밀한 제어 |
| 화면 Flash vs API JSON | 화면=Flash+리다이렉트, API=HTTPException | 일관성 | 화면은 UX, API는 명확한 상태 코드 |
| 상태 전이 검증 위치 | Service 계층 | 라우터 | 비즈니스 로직은 Service 책임 |
| 트랜잭션 commit 위치 | 단일 CRUD는 Repository, 복합은 Service | 일관성 | 현재는 단일 CRUD → Repository에서 commit |

---

## 6. 트러블슈팅

### 6-1. 비로그인 사용자가 보호 경로 직접 접근

**문제**: 로그인 안 한 사용자가 `/posts/new`를 직접 URL로 접근하면 빈 화면
**원인**: Depends 없이 라우터가 실행됨
**해결**: `Depends(get_current_user)` 추가 → 미인증 시 화면은 302 리다이렉트 `/login?next=/posts/new`, API는 401 JSON

### 6-2. 타인 게시글 수정 시도

**문제**: 사용자 A가 사용자 B의 글을 수정할 수 있었음
**원인**: 권한 검사 없이 수정 처리
**해결**: Service에서 `if post.author_id != user_id: raise PermissionError("자신의 게시글만 수정할 수 있습니다")` → Router가 403 또는 flash 에러로 변환

### 6-3. 양방향 관계 JSON 직렬화 에러

**문제**: API 응답에서 `RecursionError` 또는 무한 JSON
**원인**: `User → posts → [Post → author → User → ...]` 순환
**해결**: `PostResponse`에 `author_id: int`만 포함, `author: User`는 선언하지 않음 → 순환 끊음

### 6-4. 세션 서버 재시작 시 초기화

**문제**: 서버 재시작하면 모든 로그인이 풀림
**원인**: `SECRET_KEY = secrets.token_urlsafe(32)`로 매번 새 키 생성 → 이전 세션 쿠키 복호화 불가
**해결**: 개발은 랜덤 허용, 운영은 `.env`에서 고정값 로드: `SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))`

### 6-5. 게시판 삭제 시 FK 오류

**문제**: 게시글이 있는 게시판을 삭제하려 하면 `IntegrityError`
**원인**: Board→Post에 cascade 없음 (의도적 — 글 보호)
**해결**: FK 제약으로 삭제 불가 → "게시글이 존재하는 게시판은 삭제할 수 없습니다" flash 메시지로 안내

---

## 7. 평가 예상 질문 대비

| 질문 | 답변 방향 | 코드 근거 |
|------|----------|-----------|
| 인증 vs 인가 차이? | 인증=신원 확인(로그인), 인가=권한 검사(접근 제어) | `login_user()` vs `Depends(get_current_user)` |
| 세션 vs JWT? | 세션=서버 기억(즉시 로그아웃), JWT=토큰 자체(만료 전 유효) | `request.session["user_id"]` |
| 비밀번호 어떻게 저장? | bcrypt 해싱, 평문 금지, verify로 검증 | `passlib.CryptContext(schemes=["bcrypt"])` |
| Depends vs 미들웨어? | Depends=엔드포인트별 선택, 미들웨어=전역 강제 | 보호 경로에만 Depends 부착 |
| 연관관계 설명? | User 1:N Post(cascade), Post N:1 Board(cascade 없음), User N:M User 팔로우(Follow 조인) | `back_populates`, `ForeignKey` |
| 순환참조 해결? | 응답 모델에 FK ID만 포함, 객체 제외 | `PostResponse.author_id: int` |
| 상태 변경 로직 어디에? | Service 계층 (권한 검사 + 전이 검증) | `post_service.publish_post()` |
| 전체 구조 설명? | 인증→도메인→화면: 로그인→글작성→공개→상태변경→결과 | README 전체 흐름도 |
| Board 삭제 시? | FK 제약 → "게시글이 있으면 삭제 불가" flash | Board cascade 없음 (의도적) |
