# B5-3 학습 노트: 로그인이 되고 회원끼리 연결되는 웹 서비스 만들기

> **문과 중졸도 이해할 수 있게** — 전에 코딩을 한 번도 해본 적 없는 사람이 읽어도 이해할 수 있도록 쓴 학습 노트입니다.

---

## 📖 목차

1. [초심자를 위한 용어집](#1-초심자를-위한-용어집)
2. [과제 해석 및 분석](#2-과제-해석-및-분석)
3. [과제를 진행하기 위한 기초](#3-과제를-진행하기-위한-기초)
4. [각 기초를 익히기 위한 간단한 체험 예제](#4-각-기초를-익히기-위한-간단한-체험-예제)
5. [과제를 작게 쪼개기: 잡 → 워크 → 워크플로우](#5-과제를-작게-쪼개기-잡--워크--워크플로우)
6. [워크플로우별 트레이드오프, 이슈, 트러블슈팅](#6-워크플로우별-트레이드오프-이슈-트러블슈팅)
7. [과제 완료 후 학습한 내용 정리](#7-과제-완료-후-학습한-내용-정리)

---

## 1. 초심자를 위한 용어집

> "이 단어들이 전부 외계어처럼 보여도 괜찮습니다. 하나씩, 일상어로 풀어 설명합니다."

### 🌐 웹 서비스의 기본

| 용어 | 쉬운 설명 | 비유 |
|------|-----------|------|
| **프론트엔드** | 사용자가 브라우저에서 보는 화면 | 식당의 홀 (손님이 보는 곳) |
| **백엔드** | 사용자가 보지 못하는 서버 쪽. 데이터를 저장하고 처리 | 식당의 주방 |
| **서버** | 인터넷에서 요청을 받아서 응답을 주는 컴퓨터/프로그램 | 식당의 접수 데스크 |
| **클라이언트** | 서버에 요청을 보내는 쪽 (브라우저, 앱) | 식당의 손님 |
| **HTTP** | 클라이언트와 서버가 대화하는 규칙 | 식당에서 메뉴판 보고 주문하는 규칙 |
| **요청 (Request)** | 클라이언트가 서버에 보내는 메시지 | "불고기 1인분 주세요" |
| **응답 (Response)** | 서버가 클라이언트에게 돌려주는 메시지 | "불고기 1인분 나왔습니다" |

### 🐍 Python / FastAPI 관련

| 용어 | 쉬운 설명 | 비유 |
|------|-----------|------|
| **Python** | 프로그래밍 언어의 한 종류. 문법이 간단해서 배우기 쉬움 | 읽고 쓰기 쉬운 언어 |
| **FastAPI** | Python으로 웹 서버를 빠르게 만들게 해주는 도구(프레임워크) | 레시피 키트 (재료와 순서가 준비되어 있어 빠르게 요리 가능) |
| **uvicorn** | FastAPI 앱을 실행하는 서버 프로그램 | 전자레인지 (요리를 실제로 돌리는 기계) |
| **ASGI** | 비동기 웹 서버 규격. FastAPI가 따르는 표준 | 식당의 동시 주문 처리 규칙 |
| **엔드포인트 (Endpoint)** | 서버가 요청을 받는 주소. URL 하나 = 엔드포인트 하나 | 식당의 메뉴 하나 (`/login`, `/posts/new` 등) |
| **라우터 (Router)** | 주소(URL)와 처리 함수를 연결해주는 역할 | 주문 접수 → 주방 배정 안내판 |

### 🔐 인증 / 인가 관련

| 용어 | 쉬운 설명 | 비유 |
|------|-----------|------|
| **인증 (Authentication)** | "너 누구야?"를 확인하는 것. 로그인 | 출입증 확인 (신분 확인) |
| **인가 (Authorization)** | "너 이거 해도 돼?"를 확인하는 것. 권한 검사 | 출입증의 층별 권한 (3층은 가능, 5층은 불가) |
| **세션 (Session)** | 로그인 후 서버가 "이 사람은 로그인됨"이라고 기억하는 상태 | 식당에서 손님에게 테이블 번호표를 주는 것 |
| **쿠키 (Cookie)** | 브라우저에 저장되는 작은 데이터. 세션 ID 등을 담음 | 식당의 번호표 (다음에 올 때 보여주면 알아봄) |
| **JWT (JSON Web Token)** | 로그인 정보를 암호화해서 토큰 하나에 담는 방식 | 본인이 직접 들고 다니는 전자 출입증 |
| **비밀번호 해싱 (Hashing)** | 비밀번호를 되돌릴 수 없는 형태로 변환하여 저장 | 지문 (원래 손가락을 되돌릴 수 없듯이 해시도 복원 불가) |
| **bcrypt** | 비밀번호 해싱에 쓰는 도구. 느리게 만들어서 해킹을 어렵게 함 | 안전 금고 (열기 어렵게 만들어 도둑을 막음) |
| **로그인** | 아이디/비밀번호로 신원을 확인하고 세션을 만드는 행동 | 출입증 발급 |
| **로그아웃** | 세션을 종료하는 행동 | 출입증 반납 |

### 💾 데이터베이스 관련

| 용어 | 쉬운 설명 | 비유 |
|------|-----------|------|
| **데이터베이스 (DB)** | 데이터를 체계적으로 저장하는 공간 | 큰 서랍장 |
| **테이블 (Table)** | DB 안에서 같은 종류의 데이터를 모아둔 곳 | 서랍장의 한 칸 (사용자 칸, 게시글 칸) |
| **컬럼 (Column)** | 테이블의 항목. "이름", "이메일", "비밀번호" 등 | 서랍 칸 안의 구획 (이름 구획, 이메일 구획) |
| **행 (Row / Record)** | 테이블의 데이터 한 줄. 한 사람의 정보 전체 | 서랍 칸에 들어있는 카드 한 장 |
| **SQL** | 데이터베이스에 명령을 내리는 언어 | 서랍장 관리사에게 주문하는 말 ("3번 카드 꺼내 줘") |
| **SQLite** | 파일 하나로 되는 가벼운 데이터베이스. 설치 불필요 | USB 메모리 (파일 하나에 데이터 저장) |
| **PostgreSQL** | 규모가 큰 서비스에 쓰는 데이터베이스. 설치 필요 | 대형 창고 (여러 서버에서 동시 접근 가능) |
| **ORM** | SQL을 직접 쓰지 않고 Python 코드로 DB를 조작하게 해주는 도구 | 통역사 (Python 말을 SQL로 번역해 줌) |
| **SQLAlchemy** | Python에서 가장 많이 쓰는 ORM | 가장 유명한 통역사 |
| **모델 (Model)** | DB 테이블을 Python 클래스로 표현한 것 | 서랍 칸의 설계도 (구획이 뭔지 정의) |
| **마이그레이션 (Migration)** | DB 구조가 바뀔 때 변경사항을 기록하고 적용하는 작업 | 서랍장을 개조할 때 공사 기록을 남기는 것 |

### 🔗 관계 / 구조 관련

| 용어 | 쉬운 설명 | 비유 |
|------|-----------|------|
| **외래키 (FK, Foreign Key)** | 다른 테이블의 데이터를 가리키는 표시 | 게시글에 "작성자: 홍길동"이라고 적힌 것 (홍길동이라는 사람을 가리킴) |
| **1:N 관계** | 한 쪽이 하나, 다른 쪽이 여럿인 관계 | 한 명의 작성자 → 여러 개의 게시글 |
| **연관관계** | 테이블 간의 연결 관계 | 가족 관계도 (부모-자식 연결) |
| **cascade** | 부모가 지워지면 자식도 자동으로 지워지는 정책 | 가계약 취소 시 약정 서비스도 자동 취소 |
| **순환참조 (Circular Reference)** | A가 B를 가리키고 B가 다시 A를 가리키는 무한 반복 | 거울 두 개를 마주 보면 끝없이 반사되는 것 |
| **양방향 관계** | A에서 B를 볼 수도, B에서 A를 볼 수도 있는 관계 | 양방향 거울 (양쪽에서 서로를 볼 수 있음) |

### 🏗️ 계층 구조 관련

| 용어 | 쉬운 설명 | 비유 |
|------|-----------|------|
| **계층 분리 (Layered Architecture)** | 역할별로 코드를 나누는 것. 각 계층은 자기 역할만 함 | 식당의 역할 분담 (접수 → 주방 → 재료 창고) |
| **라우터 계층** | HTTP 요청을 받고 응답을 돌려주는 역할 | 접수 데스크 (주문 받고 음식 내줌) |
| **서비스 계층** | 비즈니스 규칙을 처리하는 역할 (권한 검사, 유효성 검증) | 주방장 (요리 규칙에 따라 조리) |
| **레포지토리 계층** | 데이터베이스 CRUD만 담당하는 역할 | 재료 창고 담당자 (재료 넣고 빼기만 함) |
| **모델 계층** | 데이터 구조를 정의하는 역할 | 재료의 종류와 규격을 정한 설계도 |
| **Depends** | FastAPI의 기능. "이 함수 실행 전에 먼저 이걸 확인해라" | "주방 들어가기 전에 위생모 먼저 쓰세요" 규칙 |
| **미들웨어 (Middleware)** | 모든 요청에 공통으로 적용되는 처리. 요청이 라우터에 도달하기 전에 실행 | 식당 입구의 안내 데스크 (모든 손님이 거쳐 감) |

### 📄 화면 / 템플릿 관련

| 용어 | 쉬운 설명 | 비유 |
|------|-----------|------|
| **SSR (Server-Side Rendering)** | 서버에서 HTML을 만들어서 브라우저에 보내는 방식 | 주방에서 요리를 완성해서 손님에게 내놓는 것 |
| **템플릿 엔진** | HTML 틀에 데이터를 끼워 넣어 완성된 HTML을 만드는 도구 | 편지 양식에 이름, 날짜를 채워 넣는 도구 |
| **Jinja2** | Python에서 가장 많이 쓰는 템플릿 엔진 | 가장 유명한 편지 양식 도구 |
| **Pydantic** | 데이터 형식을 검증하고 변환하는 도구. FastAPI의 핵심 | 우편물 검사원 (주소 형식이 맞는지 확인) |
| **스키마 (Schema)** | 데이터의 형식을 정의한 것. "이 데이터는 이런 항목들을 가진다" | 우편물의 표준 양식 (수신인, 주소, 내용 필드 정의) |
| **flash 메시지** | "한 번만" 표시되는 알림 메시지. 리다이렉트 후에도 전달됨 | 점심시간 알림방에 한 번 뜨고 사라지는 공지 |

---

## 2. 과제 해석 및 분석

> "이 과제가 도대체 뭘 만들라는 건지, 처음부터 끝까지 풀어서 설명합니다."

### 2.1 한 줄 요약

**FastAPI로 "로그인이 되고, 회원 간에 연결 관계가 있는" 웹 서비스를 만들어라.**

### 2.2 과제가 원하는 것

인터넷에서 회원가입/로그인이 되는 사이트를 만들어본 적이 없다면, 이 과제가 그 첫 경험입니다:

```
회원가입          로그인/로그아웃         접근 제어
(아이디 만들기)   (출입증 발급/반납)       (출입증 있어야 글 쓰기)

     ↓                ↓                    ↓

  인증(Auth)       세션 관리            인가(권한)

                    회원 간 연결            상태 변경
                    (작성자 ↔ 게시글)      (초안 → 공개 → 비공개)
```

### 2.3 반드시 해야 하는 것 (필수)

| # | 요구사항 | 왜 필요한가? |
|---|---------|-------------|
| 1 | **로그인/로그아웃 기능** | 인증의 기본. "누가 쓰는지" 알아야 모든 서비스가 의미 있음 |
| 2 | **회원가입** | 새 사용자 가입. 비밀번호는 해싱해서 저장 (평문 금지) |
| 3 | **로그인한 사용자만 글 쓰기/수정/삭제** | 인가의 기본. 권한이 있는 사람만 행동 가능 |
| 4 | **로그인 전/후 UI 변화** | 인증 상태가 화면에 반영되어야 함 |
| 5 | **3개 이상 모델 + 연관관계** | 데이터베이스 관계 모델링 학습 |
| 6 | **상태 전이 로직** | 비즈니스 규칙 (초안 → 공개 → 비공개) |
| 7 | **계층 분리** | 역할별 코드 분리 (Router → Service → Repository → Model) |
| 8 | **민감정보 .env 관리** | 보안 기본 (SECRET_KEY 등) |
| 9 | **README에 실행 방법 + 인증 방식 설명** | 설명 능력 평가 |

### 2.4 선택 사항 (안 해도 됨)

| 항목 | 비고 |
|------|------|
| 복잡한 권한 체계 (다단계 역할) | "요구하지 않음" — 로그인/비로그인 구분만으로 충분 |
| OAuth2 소셜 로그인 | 보너스 과제에서 선택적 |
| JWT 인증 | 본 프로젝트에서는 세션 기반 구현, JWT는 보너스로 문서화 |

### 2.5 평가 기준 분석

이 과제의 평가는 **동료 평가(3명, 30분)**로 진행됩니다. 평가자가 물어볼 수 있는 핵심 질문들:

| 질문 범주 | 예상 질문 | 우리의 대비 |
|-----------|----------|------------|
| **인증 개념** | "인증과 인가의 차이?" | README에 정의 + 구현 예시 |
| **세션 vs JWT** | "왜 세션을 선택했나? JWT는?" | README에 비교 + 전환 가이드 |
| **비밀번호 해싱** | "비밀번호를 어떻게 저장하나?" | bcrypt 해싱, 평문 저장 안 함 |
| **연관관계** | "User와 Post의 관계는?" | 1:N, cascade 정책, 순환참조 방지 |
| **계층 분리** | "각 계층의 역할은?" | Router/Service/Repository/Model 설명 |
| **상태 전이** | "초안 → 공개는 어떻게?" | 상태 전이 다이어그램 + API |
| **접근 제어** | "비로그인 사용자가 /posts/new에 접근하면?" | 302 리다이렉트 / 401 JSON |

### 2.6 핵심 도전: 인증 흐름의 전체 사이클

이 과제의 핵심은 다음 흐름을 구현하는 것입니다:

```
[회원가입]
  사용자가 아이디/비밀번호 입력
    ↓
  비밀번호 해싱 (bcrypt) → DB에 저장
    ↓
  회원가입 완료

[로그인]
  아이디/비밀번호 입력
    ↓
  DB에서 사용자 조회 → 비밀번호 해시 비교 (bcrypt verify)
    ↓
  성공 → 세션에 user_id 저장 → 쿠키에 세션 ID 발급
  실패 → "아이디 또는 비밀번호가 올바르지 않습니다"

[보호 경로 접근]
  GET /posts/new (로그인 필요)
    ↓
  Depends(get_current_user) → 세션에서 user_id 확인
    ↓
  인증됨 → User 객체 반환 → 페이지 렌더링
  미인증 → /login 으로 리다이렉트 (화면) / 401 (API)

[글 작성]
  로그인된 사용자가 글 작성
    ↓
  Service: 권한 확인 (로그인됨?) + 유효성 검증 (제목 필수?)
    ↓
  Repository: DB에 저장 (author_id = 현재 사용자)
    ↓
  상태: draft(초안) → publish → published(공개)

[로그아웃]
  세션에서 user_id 제거 → 쿠키 만료
```

---

## 3. 과제를 진행하기 위한 기초

> "이 과제를 하려면 무엇을 알아야 하는지, 그리고 그것이 왜 필요한지 설명합니다."

### 3.1 기초 1: HTTP 요청과 응답

**무엇을 아야 하나?** 클라이언트(브라우저)가 서버에 어떻게 요청을 보내고, 서버가 어떻게 응답하는지

**왜 필요한가?** FastAPI는 HTTP 요청을 받아서 응답을 주는 프레임워크입니다. 이 흐름을 모르면 모든 코드가 이해되지 않습니다.

**핵심 개념:**

| HTTP 메서드 | 의미 | 본 과제 예시 |
|------------|------|-------------|
| **GET** | 데이터 가져오기 | 게시글 목록 조회 |
| **POST** | 데이터 만들기 | 회원가입, 로그인, 글 작성 |
| **PUT** | 데이터 수정하기 | 게시글 수정 |
| **DELETE** | 데이터 삭제하기 | 게시글 삭제 |

```
요청: POST /login  (body: username=testuser, password=test1234)
                ↓
서버 처리: AuthService.authenticate() → 세션 생성
                ↓
응답: 200 OK  (body: {"message": "로그인 성공"})  + Set-Cookie: session=xxx
```

### 3.2 기초 2: 인증과 인가의 구분

**무엇을 아야 하나?** "너 누구야?"(인증)와 "너 이거 해도 돼?"(인가)의 차이

**왜 필요한가?** 이 두 개념을 섞으면 보안 구멍이 생깁니다. 로그인은 됐지만 남의 글을 지우면 안 되기 때문입니다.

**핵심 개념:**

| 구분 | 인증 (Authentication) | 인가 (Authorization) |
|------|----------------------|---------------------|
| 질문 | "너 누구야?" | "너 이거 해도 돼?" |
| 시점 | 로그인할 때 | 모든 보호 경로에 접근할 때 |
| 구현 | 세션에 user_id 저장 | Depends로 사용자 확인 + 권한 검사 |
| 예시 | testuser로 로그인 | testuser는 자기 글만 수정 가능 |

**본 프로젝트의 구현:**
- 인증: `login_user(request, user_id)` → `request.session["user_id"] = user_id`
- 인가: `get_current_user(request)` → 세션에서 user_id 확인 → User 객체 반환
- 권한: `post_service.update_post(post_id, user_id, ...)` → `if post.author_id != user_id: raise PermissionError`

### 3.3 기초 3: 비밀번호 해싱

**무엇을 아야 하나?** 비밀번호를 안전하게 저장하는 방법

**왜 필요한가?** 비밀번호를 그대로(평문) DB에 저장하면, DB가 해킹당했을 때 모든 사용자의 비밀번호가 그대로 노출됩니다.

**핵심 개념:**

```
[회원가입 시]
  입력: "test1234"
    ↓
  bcrypt 해싱: "$2b$12$N9qo8uLOickgx2ZMRZoMy..."
    ↓
  DB에 해시값 저장 (평문 "test1234"는 저장하지 않음!)

[로그인 시]
  입력: "test1234"
    ↓
  DB에서 해시값 조회: "$2b$12$N9qo8uLOickgx2ZMRZoMy..."
    ↓
  bcrypt verify: 입력값과 해시값이 일치하는지 확인
    ↓
  일치 → 로그인 성공 / 불일치 → 실패
```

**중요:** 해싱은 **단방향**입니다. 해시값에서 원래 비밀번호를 되돌릴 수 없습니다.

### 3.4 기초 4: 세션 기반 인증

**무엇을 아야 하나?** 로그인 후 서버가 "이 사람은 로그인됨"을 기억하는 방법

**왜 필요한가?** HTTP는 "상태 없음(stateless)" 프로토콜입니다. 매 요청마다 서버는 "이 사람이 누군지" 잊어버립니다. 세션은 이것을 해결합니다.

**핵심 개념:**

```
[1단계: 로그인]
  브라우저: POST /login (username, password)
  서버: 검증 성공 → 세션에 user_id=1 저장
  서버: 응답에 Set-Cookie: session=<서명된_값> 추가
  브라우저: 쿠키 저장

[2단계: 이후 요청]
  브라우저: GET /posts/new (Cookie: session=<서명된_값> 자동 첨부)
  서버: 쿠키의 세션값 복호화 → user_id=1 확인
  서버: "이 사람은 1번 사용자, 로그인됨" → 페이지 제공

[3단계: 로그아웃]
  브라우저: POST /logout
  서버: 세션에서 user_id 제거
  서버: 쿠키 만료
```

**본 프로젝트의 도구:**
- `itsdangerous`: 세션 값을 서명 (변조 방지)
- `SessionMiddleware`: FastAPI 미들웨어, 쿠키 파싱/저장 담당
- `request.session["user_id"]`: 세션 데이터에 접근하는 방법

### 3.5 기초 5: 데이터베이스 모델과 관계

**무엇을 아야 하나?** 테이블 간의 관계를 Python 코드(SQLAlchemy)로 표현하는 방법

**왜 필요한가?** "이 사용자가 이 글을 썼다"라는 관계를 DB에 저장하고, 조회할 때 "글 → 작성자 이름"처럼 관계된 데이터를 함께 가져와야 합니다.

**핵심 개념:**

```
User (사용자)          Post (게시글)         Board (게시판)
┌──────────┐          ┌──────────────┐      ┌──────────┐
│ id       │←─FK──────│ author_id    │      │ id       │
│ username │          │ board_id     │──FK─→│ name     │
│ password │          │ title        │      │ description│
│ email    │          │ content      │      └──────────┘
└──────────┘          │ status       │
     ↑                └──────────────┘
     │                     ↑
     └── 1:N 관계 ─────────┘
     (한 사용자가 여러 글을 작성)
```

**SQLAlchemy 표현:**
```python
# User 모델
class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

# Post 모델
class Post(Base):
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))  # 외래키
    author = relationship("User", back_populates="posts")  # 관계
```

- `ForeignKey("users.id")`: "이 컬럼은 users 테이블의 id를 가리킨다"
- `relationship(...)`: "이 모델에서 저 모델로 객체 단위로 접근할 수 있다"
- `back_populates`: 양방향 관계 (User.posts ↔ Post.author)

### 3.6 기초 6: 계층 분리 (Layered Architecture)

**무엇을 아야 하나?** 코드를 역할별로 나누는 방법

**왜 필요한가?** 모든 코드를 한 파일에 넣으면 수정하기 어렵고, 테스트하기 어렵고, 이해하기 어렵습니다. 계층을 나누면 각 계층이 자기 역할만 담당합니다.

**핵심 개념:**

```
요청 →  [라우터]  →  [서비스]  →  [레포지토리]  →  [DB]
         HTTP I/F    비즈니스 로직    DB CRUD        저장소
            ↑             ↑              ↑
         응답 변환     권한/검증      commit/rollback
```

| 계층 | 역할 | 본 프로젝트 파일 |
|------|------|-----------------|
| **라우터** | HTTP 요청/응답 처리 | `routers/post_router.py`, `routers/view_router.py` |
| **서비스** | 비즈니스 로직 (권한, 검증, 상태 전이) | `services/post_service.py` |
| **레포지토리** | DB CRUD만 담당 | `repositories/post_repository.py` |
| **모델** | 데이터 구조 정의 | `models/post.py` |

**핵심 원칙:** 각 계층은 **자기 바로 아래 계층만** 호출합니다. 라우터가 레포지토리를 직접 호출하면 안 됩니다.

### 3.7 기초 7: FastAPI의 Depends (의존성 주입)

**무엇을 아야 하나?** "이 함수 실행 전에 먼저 이걸 확인해라"라고 선언하는 방법

**왜 필요한가?** 모든 보호 경로마다 "로그인 확인" 코드를 복사하는 대신, Depends로 한 번 선언하면 FastAPI가 자동으로 실행해 줍니다.

**핵심 개념:**

```python
# 인증 확인 함수
async def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(401, "로그인이 필요합니다")
    return get_user_by_id(user_id)

# 보호 경로: Depends로 인증 확인 자동 실행
@router.post("/posts")
async def create_post(user: User = Depends(get_current_user)):
    # 여기에 도달하면 이미 인증됨 (user에 User 객체가 들어 있음)
    return post_service.create_post(user.id, ...)
```

- `Depends(get_current_user)`: 이 엔드포인트 실행 전에 `get_current_user`를 먼저 실행
- 인증 실패 시 `get_current_user`가 예외를 발생시키면 엔드포인트 함수는 실행되지 않음
- 인증 성공 시 반환값(User)이 `user` 매개변수에 자동 주입

---

## 4. 각 기초를 익히기 위한 간단한 체험 예제

> "이론만 읽으면 잊어버립니다. 직접 타이핑해 보면 남습니다."

### 4.1 체험 1: FastAPI 첫 엔드포인트 (기초 1)

**목표:** 가장 간단한 웹 서버를 만들어 본다.

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "안녕하세요!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"안녕하세요, {name}님!"}
```

```bash
# 실행
uvicorn main:app --reload --port 8000

# 브라우저에서 http://localhost:8000 접속 → {"message": "안녕하세요!"}
# http://localhost:8000/hello/홍길동 → {"message": "안녕하세요, 홍길동님!"}
```

**체험 포인트:**
- `@app.get("/")`: 주소 `/`로 GET 요청이 오면 아래 함수 실행
- `{name}`: URL의 일부를 변수로 받음 (`/hello/홍길동` → name="홍길동")
- 반환값이 자동으로 JSON으로 변환되어 응답

### 4.2 체험 2: 비밀번호 해싱 (기초 3)

**목표:** 비밀번호를 해싱하고 검증해 본다.

```python
# hash_test.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 회원가입: 비밀번호 해싱
password = "test1234"
hashed = pwd_context.hash(password)
print(f"원본: {password}")
print(f"해시: {hashed}")
# 해시: $2b$12$N9qo8uLOickgx2ZMRZoMy...

# 로그인: 해시 검증
is_correct = pwd_context.verify("test1234", hashed)  # True
is_wrong = pwd_context.verify("wrongpass", hashed)   # False
print(f"올바른 비번: {is_correct}")  # True
print(f"틀린 비번: {is_wrong}")     # False
```

**체험 포인트:**
- `hash()`: 평문 → 해시값 (되돌릴 수 없음)
- `verify()`: 평문과 해시값이 일치하는지 확인
- 같은 비밀번호를 해싱해도 **매번 다른 해시값**이 나옴 (salt 때문) — 하지만 verify는 정상 작동
- 본 프로젝트의 `auth/password.py`가 이 코드를 그대로 사용

### 4.3 체험 3: SQLAlchemy 모델 만들기 (기초 5)

**목표:** DB 테이블을 Python 클래스로 정의해 본다.

```python
# model_test.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///test.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

# 모델 정의 = DB 테이블 설계도
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)

# 테이블 생성
Base.metadata.create_all(engine)

# 데이터 넣기 (INSERT)
db = SessionLocal()
user = User(username="hong", email="hong@test.com")
db.add(user)
db.commit()

# 데이터 조회 (SELECT)
users = db.query(User).all()
for u in users:
    print(f"ID: {u.id}, 이름: {u.username}, 이메일: {u.email}")
# ID: 1, 이름: hong, 이메일: hong@test.com

db.close()
```

**체험 포인트:**
- `Column(Integer, primary_key=True)`: 이 컬럼은 숫자이고 기본키
- `db.add(user)` + `db.commit()`: DB에 데이터 저장
- `db.query(User).all()`: DB에서 모든 데이터 조회
- SQL을 직접 쓰지 않고 Python 코드로 DB 조작 → 이것이 ORM
- 본 프로젝트의 `models/user.py`, `database.py`가 이 패턴의 확장

### 4.4 체험 4: 세션 로그인 흐름 (기초 4)

**목표:** 세션 기반 로그인의 핵심 흐름을 만들어 본다.

```python
# session_test.py
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="my-secret-key")

# 가짜 사용자 DB
fake_users = {"testuser": {"id": 1, "password": "test1234"}}

@app.post("/login")
async def login(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    user = fake_users.get(username)
    if not user or user["password"] != password:
        return JSONResponse({"error": "로그인 실패"}, status_code=401)

    # 세션에 user_id 저장 → 이것이 "로그인됨"의 증거
    request.session["user_id"] = user["id"]
    return {"message": f"{username}님 로그인 성공"}

@app.get("/me")
async def me(request: Request):
    # 세션에서 user_id 확인
    user_id = request.session.get("user_id")
    if not user_id:
        return JSONResponse({"error": "로그인이 필요합니다"}, status_code=401)
    return {"user_id": user_id, "message": "로그인된 사용자"}

@app.post("/logout")
async def logout(request: Request):
    # 세션에서 user_id 제거
    request.session.pop("user_id", None)
    return {"message": "로그아웃 완료"}
```

**체험 포인트:**
- `request.session["user_id"] = user_id`: 세션에 데이터 저장 (로그인)
- `request.session.get("user_id")`: 세션에서 데이터 조회 (인증 확인)
- `request.session.pop("user_id", None)`: 세션에서 데이터 제거 (로그아웃)
- 본 프로젝트의 `auth/session.py`가 이 패턴을 실제 구현

### 4.5 체험 5: Depends로 인증 확인 (기초 7)

**목표:** Depends로 인증을 자동화해 본다.

```python
# depends_test.py (체험 4에 이어서)
from fastapi import HTTPException

# 인증 함수: 이 함수가 먼저 실행됨
async def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(401, "로그인이 필요합니다")
    return {"user_id": user_id}

# 보호 경로: Depends가 get_current_user를 자동 실행
@app.get("/protected")
async def protected(user = Depends(get_current_user)):
    # 여기에 도달하면 이미 인증됨
    return {"message": f"안전한 페이지, user_id={user['user_id']}"}

# 공개 경로: Depends 없음 → 누구나 접근 가능
@app.get("/public")
async def public():
    return {"message": "누구나 볼 수 있는 페이지"}
```

**체험 포인트:**
- `/public`: Depends 없음 → 로그인 없이 접근 가능
- `/protected`: `Depends(get_current_user)` → 로그인 확인 후에만 실행
- 인증 실패 시 HTTPException(401) → 자동으로 401 응답
- 인증 성공 시 반환값이 `user`에 주입 → 엔드포인트에서 사용 가능
- 본 프로젝트의 `auth/dependencies.py`가 이 패턴의 실제 적용

### 4.6 체험 6: 모델 간 관계 만들기 (기초 5)

**목표:** 1:N 관계를 SQLAlchemy로 표현해 본다.

```python
# relationship_test.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///rel_test.db")
SessionLocal = sessionmaker(bind=engine)

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # 1:N 관계 — 한 명의 작성자가 여러 책을 가짐
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    # N:1 관계 — 여러 책이 한 명의 작성자를 가리킴
    author = relationship("Author", back_populates="books")

Base.metadata.create_all(engine)
db = SessionLocal()

# 데이터 넣기
author = Author(name="홍길동")
author.books = [Book(title="첫 번째 책"), Book(title="두 번째 책")]
db.add(author)
db.commit()

# 관계 조회: 작성자 → 책 목록
a = db.query(Author).first()
print(f"작성자: {a.name}")
for book in a.books:
    print(f"  책: {book.title}")

# 관계 조회: 책 → 작성자
b = db.query(Book).first()
print(f"책: {b.title}, 작성자: {b.author.name}")

db.close()
```

**체험 포인트:**
- `relationship("Book", back_populates="author")`: Author에서 Book으로 접근
- `ForeignKey("authors.id")`: Book이 Author의 id를 가리킴
- `author.books`: 관계를 통해 "이 작성자의 책 목록"을 바로 조회 (SQL 안 써도 됨)
- `book.author.name`: 관계를 통해 "이 책의 작성자 이름"을 바로 조회
- 본 프로젝트의 User → Post, Board → Post 관계가 이 패턴의 실제 적용

### 4.7 체험 7: Jinja2 템플릿으로 화면 만들기

**목표:** 서버에서 HTML을 만들어 브라우저에 보내본다.

```python
# template_test.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/welcome", response_class=HTMLResponse)
async def welcome(request: Request):
    # 템플릿에 데이터를 넘겨서 HTML 생성
    return templates.TemplateResponse("welcome.html", {
        "request": request,
        "username": "홍길동",
        "items": ["사과", "바나나", "체리"]
    })
```

```html
<!-- templates/welcome.html -->
<html>
<body>
  <h1>안녕하세요, {{ username }}님!</h1>
  <ul>
    {% for item in items %}
      <li>{{ item }}</li>
    {% endfor %}
  </ul>
</body>
</html>
```

**체험 포인트:**
- `{{ username }}`: 변수 출력 (Python에서 넘긴 값)
- `{% for %}` ... `{% endfor %}`: 반복문
- `{% if %}` ... `{% endif %}`: 조건문
- 서버에서 HTML을 완성해서 보냄 → SSR (Server-Side Rendering)
- 본 프로젝트의 모든 화면이 이 방식으로 구현

---

## 5. 과제를 작게 쪼개기: 잡 → 워크 → 워크플로우

> "큰 산을 한 번에 오르지 말고, 캠프 → 베이스캠프 → 정상으로 나누듯이, 과제도 잡(Job) → 워크(Work) → 워크플로우(Workflow)로 나눕니다."

### 5.1 쪼개기 원칙

```
과제 (전체)
  └── 잡 (Job): 큰 단위의 작업. "이 잡이 끝나면 의미 있는 결과물이 나온다"
       └── 워크 (Work): 잡 안의 작은 단위. "이 워크가 끝나면 한 가지가 완성된다"
            └── 워크플로우 (Workflow): 워크를 실행하는 구체적 순서
```

### 5.2 전체 잡 분해도

```
과제: FastAPI 인증 + 회원 연결 웹 서비스 만들기
│
├── Job 1: 프로젝트 기반 잡기 (Setup)
├── Job 2: 데이터베이스 모델 설계 (Models)
├── Job 3: 레포지토리 계층 구현 (Repository)
├── Job 4: 인증 시스템 구축 (Auth)
├── Job 5: 서비스 계층 구현 (Service)
├── Job 6: 라우터 계층 구현 (Router)
├── Job 7: 화면 템플릿 구현 (Templates)
├── Job 8: 통합 및 초기 데이터 (Integration)
└── Job 9: 문서화 및 평가 대비 (Docs)
```

### 5.3 각 잡별 워크 분해

#### Job 1: 프로젝트 기반 잡기 (Setup)

| 워크 | 내용 | 워크플로우 |
|------|------|-----------|
| W1-1 | 프로젝트 구조 생성 | `app/` 디렉토리 + 하위 패키지 (auth, models, repositories, services, routers, templates) |
| W1-2 | 의존성 설치 | `pip install fastapi uvicorn sqlalchemy jinja2 passlib bcrypt itsdangerous python-multipart` |
| W1-3 | 설정 파일 | `config.py` (SECRET_KEY, SESSION_MAX_AGE), `.env.example`, `.gitignore` |
| W1-4 | DB 연결 설정 | `database.py` (engine, SessionLocal, get_db, Base) |

#### Job 2: 데이터베이스 모델 설계 (Models)

| 워크 | 내용 | 워크플로우 |
|------|------|-----------|
| W2-1 | User 모델 | id, username, password_hash, email, created_at + posts 관계 (cascade) |
| W2-2 | Board 모델 | id, name, description + posts 관계 |
| W2-3 | Post 모델 | id, title, content, status(Enum), author_id(FK), board_id(FK) + author/board 관계 |
| W2-4 | PostStatus Enum | DRAFT, PUBLISHED, HIDDEN 정의 |
| W2-5 | 관계 설정 | back_populates로 양방향 관계 + cascade 정책 |

#### Job 3: 레포지토리 계층 구현 (Repository)

| 워크 | 내용 | 워크플로우 |
|------|------|-----------|
| W3-1 | UserRepository | get_by_id, get_by_username, create |
| W3-2 | BoardRepository | get_by_id, get_all, create |
| W3-3 | PostRepository | CRUD + search + update_status + get_by_author |

#### Job 4: 인증 시스템 구축 (Auth)

| 워크 | 내용 | 워크플로우 |
|------|------|-----------|
| W4-1 | 비밀번호 해싱 | `password.py`: hash_password(), verify_password() (passlib + bcrypt) |
| W4-2 | 세션 관리 | `session.py`: login_user(), logout_user(), get_current_user_from_session() |
| W4-3 | 인증 의존성 | `dependencies.py`: get_current_user (Depends용), get_optional_user |
| W4-4 | 인증 서비스 | `service.py`: AuthService.authenticate(), AuthService.register() |
| W4-5 | 인증 라우터 | `router.py`: POST /api/auth/login, /logout, /register |

#### Job 5: 서비스 계층 구현 (Service)

| 워크 | 내용 | 워크플로우 |
|------|------|-----------|
| W5-1 | PostService | create_post (권한+검증), update_post (권한), delete_post (권한) |
| W5-2 | 상태 전이 | publish_post (DRAFT/HIDDEN → PUBLISHED), hide_post (→ HIDDEN) |
| W5-3 | BoardService | get_boards, get_board_with_posts |

#### Job 6: 라우터 계층 구현 (Router)

| 워크 | 내용 | 워크플로우 |
|------|------|-----------|
| W6-1 | API 라우터 (post) | GET/POST/PUT/DELETE /api/posts/* + Depends(get_current_user) |
| W6-2 | API 라우터 (board) | GET /api/boards/* |
| W6-3 | 화면 라우터 (view) | SSR: /, /login, /boards, /posts/new, /posts/{id}, /my-posts 등 |
| W6-4 | 보호 경로 설정 | 화면은 리다이렉트, API는 401/403 |
| W6-5 | flash 메시지 | set_flash(), get_flash() — 리다이렉트 후 알림 표시 |

#### Job 7: 화면 템플릿 구현 (Templates)

| 워크 | 내용 | 워크플로우 |
|------|------|-----------|
| W7-1 | base.html | 공통 레이아웃 (네비게이션, flash 표시, CSS) |
| W7-2 | home.html | 홈페이지 (로그인 전/후 분기) |
| W7-3 | login.html | 로그인 폼 + 에러 메시지 |
| W7-4 | boards/ | list.html (게시판 목록), detail.html (게시판 상세 + 게시글 목록) |
| W7-5 | posts/ | create.html, detail.html (상태 배지), edit.html |
| W7-6 | my_posts.html | 내 글 목록 (연관관계 활용) |

#### Job 8: 통합 및 초기 데이터 (Integration)

| 워크 | 내용 | 워크플로우 |
|------|------|-----------|
| W8-1 | main.py | FastAPI 앱 생성 + 미들웨어 + 라우터 등록 + 템플릿 설정 |
| W8-2 | init_db.py | 초기 데이터 생성 (testuser, 2개 게시판, 샘플 게시글) |
| W8-3 | schemas.py | Pydantic 요청/응답 스키마 (PostResponse, PostCreate 등) |
| W8-4 | 통합 테스트 | 회원가입 → 로그인 → 글 작성 → 공개 → 수정 → 삭제 → 로그아웃 |

#### Job 9: 문서화 및 평가 대비 (Docs)

| 워크 | 내용 | 워크플로우 |
|------|------|-----------|
| W9-1 | README | 실행 방법, 인증 방식, API 목록, 연관관계 설명 |
| W9-2 | GITFLOW | 브랜칭 전략 문서 |
| W9-3 | IMPLEMENTATION_REPORT | 구현 완료 보고서 |
| W9-4 | eval 가이드 | 사전평가 결과 + 동료평가 예상 질문 (verbal-qa.md) |

### 5.4 워크플로우 실행 순서 (의존성 그래프)

```
Job 1 (Setup)
  ↓
Job 2 (Models) ← 모든 것의 기초
  ↓
Job 3 (Repository) ← Model이 있어야 DB 조작
  ↓
Job 4 (Auth) ← Repository가 있어야 사용자 조회/생성
  ↓
Job 5 (Service) ← Auth + Repository가 있어야 권한+CRUD
  ↓
Job 6 (Router) ← Service가 있어야 엔드포인트 구성
  ↓
Job 7 (Templates) ← Router가 있어야 화면 연결
  ↓
Job 8 (Integration) ← 전부 있어야 통합
  ↓
Job 9 (Docs) ← 완성 후 문서화
```

> **왜 이 순서인가?** 데이터 구조(2)가 먼저 정해져야 DB 조작(3)이 가능합니다. 사용자 조회(4)가 있어야 권한 검사(5)를 할 수 있습니다. 비즈니스 로직(5)이 있어야 HTTP 엔드포인트(6)를 만들 수 있습니다. 엔드포인트가 있어야 화면(7)을 연결할 수 있습니다. 이것이 **의존성 역순**으로 진행하는 이유입니다.

---

## 6. 워크플로우별 트레이드오프, 이슈, 트러블슈팅

> "길을 걷다 보면 갈림길을 만납니다. 왜 이 길을 선택했는지, 다른 길은 왜 포기했는지, 그리고 길에서 넘어졌을 때 어떻게 일어났는지를 기록합니다."

### 6.1 Job 4 (인증): 세션 vs JWT

#### 🤔 선택의 기로

| 기준 | 세션 (Session) | JWT (JSON Web Token) |
|------|---------------|---------------------|
| 상태 저장 위치 | 서버 (서버가 기억) | 클라이언트 (토큰이 모든 정보를 가짐) |
| 로그아웃 | 즉시 (세션 삭제) | 어려움 (토큰이 만료될 때까지 유효) |
| 확장성 | 서버 여러 대면 세션 공유 필요 | 좋음 (서버가 상태를 안 가짐) |
| 구현 난이도 | 낮음 (미들웨어 한 줄) | 중간 (토큰 생성/검증 로직) |
| 보안 | 쿠키 HttpOnly + 서명 | 토큰 탈취 시 만료 전까지 유효 |

#### ✅ 선택: 세션 기반

**이유:**
1. 과제가 "세션 **또는** JWT"를 허용 → 더 간단한 세션 먼저 구현
2. 단일 서버(SQLite) 환경에서 세션이 적합
3. 로그아웃이 즉시 처리됨 (세션에서 user_id만 제거하면 끝)
4. `SessionMiddleware` 한 줄로 세션 기능 추가 가능

#### ⚖️ 트레이드오프

- **포기한 것:** 수평 확장의 용이성 (서버 여러 대일 때 세션 공유 필요)
- **얻은 것:** 구현 단순성, 즉시 로그아웃, 과제 요구사항 충족
- **판단:** 과제 규모(단일 서버, 학습 목적)에서는 세션이 최적

#### 📝 JWT 전환 대비

README에 세션 → JWT 전환 가이드를 문서화:
- 변경 지점 5곳 명시 (session.py → jwt.py, dependencies.py, main.py, router.py, config.py)
- `get_current_user` 인터페이스를 유지하면 라우터 코드는 변경 불필요
- 구현 우선순위 정리 (P0: 토큰 만료, HTTPS / P1: Refresh Token / P2: CSRF, XSS)

---

### 6.2 Job 2 (모델): cascade 정책 — "사용자 삭제 시 게시글은?"

#### 🤔 선택의 기로

| 정책 | 동작 | 장점 | 단점 |
|------|------|------|------|
| `cascade="all, delete-orphan"` | 사용자 삭제 → 글 자동 삭제 | 데이터 정리 자동화 | 작성자가 바뀌어야 하는 글도 삭제됨 |
| cascade 없음 | 사용자 삭제 → FK 오류 | 글 보존 | 수동 처리 필요 |
| `SET NULL` | 사용자 삭제 → 글의 author_id = NULL | 글 보존 | 글이 "익명"이 됨 |

#### ✅ 선택: `cascade="all, delete-orphan"` (User → Post)

**이유:**
1. 사용자 탈퇴 시 해당 사용자의 글도 자동 삭제 → 데이터 정리 자동화
2. "orphan" 옵션: 부모(User)가 없는 자식(Post)을 자동 삭제
3. 과제 요구사항에 "회원 탈퇴 시 데이터 처리" 암시

#### Board → Post: cascade 없음

**이유:**
1. 게시판 삭제 시 게시글이 자동 삭제되면 안 됨 (글 보호)
2. FK 제약으로 게시글이 있으면 게시판 삭제 불가 → IntegrityError
3. 사용자에게 "게시글이 있는 게시판은 삭제할 수 없습니다" flash 메시지로 안내

#### ⚖️ 트레이드오프

- **포기한 것:** 게시판 삭제의 자동화 (수동 확인 필요)
- **얻은 것:** 데이터 보호 (게시판을 지워도 글은 안 사라짐)
- **판단:** 사용자 탈퇴는 글 삭제가 자연스럽지만, 게시판 삭제는 글 보존이 자연스러움

---

### 6.3 Job 2 (모델): 양방향 관계의 순환참조 — 🔥 트러블슈팅

#### 🐛 발생한 문제

양방향 관계(`back_populates`)를 사용하면, JSON 응답을 만들 때 무한 순환참조가 발생:

```
User → posts → [Post → author → User → posts → [Post → author → ... 무한 반복
```

이 상태에서 `json.dumps(user)`를 호출하면 `RecursionError` 발생.

#### 🔍 원인 분석

SQLAlchemy의 `relationship`은 객체를 직접 참조합니다. User.posts는 Post 객체의 리스트이고, 각 Post.author는 다시 User 객체를 가리킵니다. 이것을 JSON으로 직렬화하려면 끝없이 따라가야 합니다.

#### 💡 해결책: Pydantic 응답 모델에서 FK ID만 포함

```python
# ❌ 순환참조 발생: 관계 객체 전체 포함
class PostResponse(BaseModel):
    author: User      # User → posts → Post → author → ... 무한 순환

# ✅ 순환참조 방지: FK ID만 포함
class PostResponse(BaseModel):
    author_id: int    # 순호 없음, ID만 반환
    board_id: int     # 순환 없음, ID만 반환
    model_config = {"from_attributes": True}
```

**3가지 해결 전략:**

| 전략 | 방법 | 사용처 |
|------|------|--------|
| FK ID만 포함 | `author_id: int` (관계 객체 제외) | API 응답 (현재 방식) |
| 중첩 응답 제한 | `UserWithPostsResponse`에 `posts: List[PostResponse]` (PostResponse에는 author 없음) | 사용자 + 글 목록 동시 응답 |
| 템플릿에서 선택적 접근 | `post.author.username` (필요한 필드만) | Jinja2 화면 |

#### ⚖️ 트레이드오프

- **포기한 것:** API 응답에 관계 객체 전체 포함 (프론트엔드에서 한 번에 모든 정보)
- **얻은 것:** 순환참조 방지, 응답 크기 최소화, 명확한 응답 구조
- **판단:** API는 ID만 반환하고, 상세 정보가 필요하면 별도 요청 → RESTful 원칙에 부합

---

### 6.4 Job 6 (라우터): 미들웨어 vs Depends로 인증 처리

#### 🤔 선택의 기로

| 기준 | 미들웨어 | Depends |
|------|---------|---------|
| 적용 범위 | 모든 요청에 자동 적용 | 엔드포인트별 선택적 적용 |
| 세밀한 제어 | 어려움 (공개/보호 구분 복잡) | 쉬움 (Depends 붙이고 떼고) |
| 가시성 | 숨어 있음 (한눈에 안 보임) | 명시적 (코드에서 바로 보임) |
| 예외 처리 | 전역 핸들러 필요 | 자동 (HTTPException 즉시 응답) |

#### ✅ 선택: Depends를 주 정책, 미들웨어는 보조

**이유:**
1. 본 프로젝트는 공개 경로(`/`, `/login`, `/boards`)와 보호 경로(`/posts/new`)가 섞여 있음
2. 미들웨어로 모든 요청에 인증을 강제하면, 공개 경로도 "예외 처리"해야 함 → 복잡
3. Depends는 "이 엔드포인트는 인증 필요"를 코드에서 한눈에 파악 가능

**분담:**
- `SessionMiddleware`: 세션 쿠키 파싱/저장 **만** 담당 (인증 판단 안 함)
- `Depends(get_current_user)`: 보호 경로에만 붙임 (인증 판단)

#### ⚖️ 트레이드오프

- **포기한 것:** "잊고 Depends 안 붙인 경로"가 노출될 위험
- **얻은 것:** 공개/보호 경로를 코드에서 명시적으로 구분, 세밀한 제어
- **판단:** 공개/보호가 섞인 서비스에서는 Depends가 더 안전하고 명확

---

### 6.5 Job 6 (라우터): 화면 라우터의 예외 처리 — flash vs JSON

#### 🤔 선택의 기로

화면 라우터(view_router.py)에서 에러가 발생했을 때:

| 방식 | 동작 | 사용자 경험 |
|------|------|------------|
| HTTPException | 에러 페이지 (빈 화면 + 상태 코드) | "뭔가 잘못됐다"는 느낌 |
| flash + 리다이렉트 | 이전 페이지로 돌아감 + 알림 메시지 | "왜 안 됐는지" 알 수 있음 |

#### ✅ 선택: flash + 리다이렉트

**이유:**
1. 사용자가 "왜 안 되는지" 이해할 수 있어야 함 (flash 메시지)
2. 에러 페이지(빈 화면)보다 이전 페이지로 돌아가는 것이 자연스러운 UX
3. "자신의 게시글만 수정할 수 있습니다"라는 구체적 메시지 전달

**구현:**
```python
# 화면 라우터: flash + 리다이렉트
except PermissionError:
    set_flash(request, "error", "자신의 게시글만 삭제할 수 있습니다.")
    return RedirectResponse(url=f"/posts/{post_id}", status_code=302)

# API 라우터: JSON 에러
except PermissionError as e:
    raise HTTPException(status_code=403, detail=str(e))
```

#### ⚖️ 트레이드오프

- **포기한 것:** HTTP 상태 코드의 명확성 (리다이렉트는 302로 에러와 성공이 구분 안 됨)
- **얻은 것:** 사용자 친화적 에러 메시지, 자연스러운 화면 전환
- **판단:** 화면은 사용자 경험이 우선, API는 명확한 상태 코드가 우선 → 두 방식을 상황에 맞게 분리

---

### 6.6 Job 5 (서비스): 트랜잭션 관리를 어디서? — 🐛 이슈

#### 🤔 선택의 기로

| 기준 | Repository에서 commit | Service에서 commit |
|------|----------------------|-------------------|
| 단일 CRUD | 적합 (한 번에 commit) | 오버헤드 |
| 복합 작업 (여러 Repository 호출) | 어려움 (각각 commit → 중간 실패 시 일관성 깨짐) | 적합 (한 번에 commit/rollback) |
| 책임 명확성 | Repository가 DB 책임 | Service가 비즈니스 트랜잭션 책임 |

#### ✅ 선택: 단일 CRUD는 Repository, 복합 작업은 Service

**현재 프로젝트 (단일 CRUD 중심):**
```python
# Repository: 단일 CRUD 내부에서 commit
def create(self, ...) -> Post:
    post = Post(...)
    self.db.add(post)
    self.db.commit()      # ← 여기서 commit
    self.db.refresh(post)
    return post
```

**복합 작업이 필요한 경우 (권장 패턴):**
```python
# Service: 여러 Repository 호출 후 한 번에 commit
def place_order(self, user_id, items):
    try:
        order = self.order_repo.create(user_id, items)
        for item in items:
            self.stock_repo.decrease(item.product_id, item.quantity)
        self.db.commit()     # ← Service에서 commit
    except Exception:
        self.db.rollback()   # ← 전체 롤백
        raise
```

#### ⚖️ 트레이드오프

- **포기한 것:** 단일 패턴의 일관성 (Repository와 Service가 섞임)
- **얻은 것:** 각 상황에 맞는 최적의 트랜잭션 관리
- **판단:** 현재 프로젝트는 단일 CRUD이므로 Repository commit이 적합, 복합 작업이 추가되면 Service에서 관리

---

### 6.7 Job 4 (인증): 비밀번호 해싱 — 왜 bcrypt인가?

#### 🤔 선택의 기로

| 해시 방식 | 속도 | 보안 | 비고 |
|----------|------|------|------|
| MD5 | 매우 빠름 | ❌ 깨짐 | 사용 금지 |
| SHA-256 | 빠름 | △ 레인보우 테이블 공격 가능 | 단독 사용 부적절 |
| bcrypt | 느림 (의도적) | ✅ 안전 | salt 자동 생성, 비용 조절 가능 |

#### ✅ 선택: bcrypt (passlib)

**이유:**
1. **의도적으로 느림**: 해커가 무차별 대입(brute force)할 때 시간이 오래 걸림
2. **salt 자동 생성**: 같은 비밀번호도 매번 다른 해시값 → 레인보우 테이블 공격 방어
3. **비용 조절**: 컴퓨터가 빨라지면 비용 파라미터를 높여 보안 유지
4. **과제 권장**: `passlib[bcrypt]`가 제약 사항에 명시됨

#### ⚖️ 트레이드오프

- **포기한 것:** 로그인 속도 (bcrypt는 약 100ms 소요)
- **얻은 것:** 해킹 시도 시 시간이 기하급수적으로 증가 → 보안
- **판단:** 로그인에 100ms는 사용자가 체감하지 못하지만, 해커에게는 치명적 → bcrypt 승

---

### 6.8 Job 8 (통합): SECRET_KEY 관리 — 🐛 이슈

#### 🐛 발생한 문제

개발 환경에서 `SECRET_KEY`를 `secrets.token_urlsafe(32)`로 매번 생성하면, 서버 재시작 시마다 모든 세션이 무효화됨 → 로그인한 사용자가 갑자기 로그아웃됨.

#### 🔍 원인 분석

세션 쿠키는 SECRET_KEY로 서명됩니다. SECRET_KEY가 바뀌면 이전에 서명된 쿠키를 복호화할 수 없어, 모든 세션이 무효화됩니다.

#### 💡 해결책: 환경에 따른 분기

```python
# config.py
import secrets, os

# 개발: 환경변수가 없으면 랜덤 생성 (서버 재시작 시 세션 초기화 — 개발 중이라 상관없음)
# 운영: 환경변수에서 고정값 로드 (서버 재시작해도 세션 유지)
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
```

#### ⚖️ 트레이드오프

- **포기한 것:** 개발 중 서버 재시작 시 로그인 풀림 (불편하지만 개발 중이라 감수)
- **얻은 것:** 운영 환경에서 고정된 SECRET_KEY → 세션 안정성
- **판단:** 개발과 운영을 분리하여 각 환경에 맞는 동작 → .env로 관리

---

## 7. 과제 완료 후 학습한 내용 정리

> "과제를 끝내고 나서, 무엇을 알게 되었는지, 무엇이 바뀌었는지 정리합니다."

### 7.1 배운 것: 백엔드의 사고방식

**과제 전:** "화면을 어떻게 꾸밀까?" (프론트엔드 중심)
**과제 후:** "데이터를 어떻게 저장하고, 누가 접근할 수 있게 할까?" (백엔드 중심)

백엔드의 핵심은 "데이터를 안전하게 저장하고, 올바른 사람만 접근하게 하는 것"입니다. 이 과제를 하면서 인증, 인가, 데이터 모델링, 계층 분리의 전체 흐름을 경험했습니다.

### 7.2 배운 것: 인증의 전체 사이클

```
회원가입 (비밀번호 해싱 → DB 저장)
    ↓
로그인 (해시 검증 → 세션 생성 → 쿠키 발급)
    ↓
보호 경로 접근 (Depends → 세션 확인 → User 객체 주입)
    ↓
권한 검사 (Service → author_id == user_id?)
    ↓
데이터 처리 (Repository → DB CRUD)
    ↓
로그아웃 (세션 제거 → 쿠키 만료)
```

이 흐름을 **한 줄 한 줄 추적**할 수 있게 되었습니다. "로그인이 되면 왜 다른 페이지에서도 로그인 상태가 유지되나?"라는 질문에, "쿠키에 세션 ID가 저장되어 매 요청마다 자동 전송되고, 서버가 세션에서 user_id를 확인하기 때문"이라고 설명할 수 있습니다.

### 7.3 배운 것: 계층 분리의 중요성

| 원칙 | 이 과제에서의 적용 |
|------|------------------|
| **단일 책임** | Router는 HTTP만, Service는 비즈니스만, Repository는 DB만 |
| **의존성 방향** | 상위 계층이 하위 계층을 호출 (Router → Service → Repository) |
| **예외 계약** | Service는 ValueError/PermissionError, Router는 HTTPException으로 변환 |
| **테스트 용이성** | Repository를 mock하면 Service 테스트 가능, Service를 mock하면 Router 테스트 가능 |

### 7.4 배운 것: 데이터베이스 관계 모델링

- **외래키(FK)**: "이 데이터가 누구의 것인지" 표시
- **관계(relationship)**: 객체 단위로 관계된 데이터에 접근 (SQL 안 써도 됨)
- **cascade**: 부모 삭제 시 자식 처리 정책 (삭제 vs 보존)
- **순환참조**: 양방향 관계의 함정 → FK ID만 응답하여 해결

### 7.5 배운 것: 보안의 기본

| 보안 원칙 | 이 과제에서의 적용 |
|----------|------------------|
| **비밀번호 평문 저장 금지** | bcrypt 해싱 (되돌릴 수 없는 변환) |
| **민감정보 코드에서 분리** | SECRET_KEY를 .env로 관리 |
| **세션 변조 방지** | itsdangerous로 세션 값 서명 |
| **최소 권한** | 로그인/비로그인 구분 + 작성자만 수정/삭제 |
| **에러 메시지 주의** | "아이디 또는 비밀번호가 올바르지 않습니다" (어느 것이 틀렸는지 알려주지 않음) |

### 7.6 핵심 인사이트 3가지

1. **"인증은 출입증, 인가는 층별 권한"**: 인증은 "누구인지" 확인하고, 인가는 "무엇을 할 수 있는지" 확인한다. 둘은 다르다. 로그인됐다고 모든 것을 할 수 있는 게 아니다.

2. **"계층 분리는 테스트와 변경을 쉽게 한다"**: Repository가 DB CRUD만 담당하면, DB를 SQLite에서 PostgreSQL로 바꿀 때 Repository만 수정하면 된다. Service가 비즈니스 로직만 담당하면, HTTP 없이도 로직을 테스트할 수 있다.

3. **"양방향 관계는 양날검"**: `post.author.username`처럼 편리하게 관계 데이터에 접근할 수 있지만, JSON 직렬화 시 순환참조가 발생한다. 편리함과 안전성 사이에서 균형을 잡아야 한다 (FK ID만 응답).

### 7.7 다음 단계로 나아가기 위한 메모

| 주제 | 이 과제에서 | 다음에 배울 것 |
|------|-----------|---------------|
| 인증 | 세션 (서버 기억) | JWT (토큰 기반), OAuth2 (소셜 로그인) |
| 권한 | 로그인/비로그인 2단계 | RBAC (역할 기반: user, admin, manager) |
| DB | SQLite + SQLAlchemy | PostgreSQL, Alembic (마이그레이션) |
| API | REST + Jinja2 SSR | GraphQL, 프론트엔드 분리 (React + API) |
| 캐싱 | 없음 | Redis (세션 공유, 캐싱) |
| 테스트 | 수동 (curl) | pytest, TestClient (자동화) |
| 배포 | 로컬 (uvicorn) | Docker, AWS, Gunicorn + Nginx |

---

> *이 학습 노트는 Codyssey AI/SW 기초 과정 B5-3 과제를 수행하며 학습한 내용을 정리한 것입니다.*
