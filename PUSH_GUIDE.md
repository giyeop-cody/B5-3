# 🚀 GitHub PR 보내기 가이드

원격 저장소가 추가되었습니다! 이제 GitHub에 push하고 PR을 생성하는 절차를 안내합니다.

---

## 📋 현재 상태

✅ **원격 저장소 추가 완료**
```
origin  https://github.com/giyeop-cody/B5-3.git (fetch)
origin  https://github.com/giyeop-cody/B5-3.git (push)
```

✅ **Gitflow 브랜치 구조 완성**
- main: 프로덕션 브랜치
- develop: 개발 통합 브랜치 (모든 기능 완료)
- release/1.0.0: 릴리즈 준비 브랜치
- feature/*: 6개의 기능 개발 브랜치

---

## 🔐 1단계: GitHub 인증 설정

### 방법 A: SSH 키 사용 (권장)

```bash
# 1. SSH 키 생성 (이미 있으면 스킵)
ssh-keygen -t ed25519 -C "giyeop kim"

# 2. SSH 키 복사
cat ~/.ssh/id_ed25519.pub

# 3. GitHub Settings > SSH and GPG keys > New SSH key
# 복사한 키를 붙여넣기

# 4. SSH 연결 테스트
ssh -T git@github.com
```

### 방법 B: Personal Access Token 사용

```bash
# 1. GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
# 2. Generate new token (classic)
# 3. repo 권한 선택 후 생성
# 4. 생성된 토큰을 안전하게 저장

# 5. 원격 URL을 HTTPS + 토큰으로 변경
git remote set-url origin https://<USERNAME>:<TOKEN>@github.com/giyeop-cody/B5-3.git
```

### 방법 C: GitHub CLI 사용 (가장 간단)

```bash
# 1. GitHub CLI 설치
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# 2. GitHub 로그인
gh auth login

# 3. 프롬프트에 따라 로그인 진행
```

---

## 📤 2단계: GitHub에 Push

### Option 1: develop 브랜치만 push (권장)

```bash
# develop 브랜치를 원격으로 push
git push -u origin develop

# 모든 브랜치와 태그도 함께 push하려면
git push origin --all
git push origin --tags
```

### Option 2: 모든 브랜치 push

```bash
# 모든 브랜치 push
git push origin --all

# 모든 태그 push
git push origin --tags
```

### Option 3: 특정 브랜치만 push

```bash
# develop 브랜치
git push -u origin develop

# main 브랜치
git push -u origin main

# release 브랜치
git push -u origin release/1.0.0
```

---

## 🔀 3단계: Pull Request 생성

### GitHub 웹 인터페이스에서 PR 생성

1. **GitHub 저장소 접속**
   ```
   https://github.com/giyeop-cody/B5-3
   ```

2. **Pull requests 탭 클릭**
   - 상단 메뉴에서 "Pull requests" 클릭

3. **New pull request 버튼 클릭**

4. **브랜치 선택**
   ```
   base: main (또는 대상 브랜치)
   compare: develop
   ```

5. **PR 정보 작성**

   **Title:**
   ```
   feat: FastAPI 게시판 서비스 구현 (Gitflow 전략 적용)
   ```

   **Description:**
   ```markdown
   ## 🎯 구현 내용
   
   FastAPI를 사용한 게시판 웹 서비스를 Gitflow 브랜칭 전략으로 구현했습니다.
   
   ## ✨ 주요 기능
   
   ### 🔐 인증/인가
   - 세션 기반 로그인/로그아웃
   - 보호된 경로 접근 제어
   - 인증 상태별 UI 변화
   
   ### 📋 게시판 & 게시글
   - 게시판 목록/상세
   - 게시글 CRUD (작성/조회/수정/삭제)
   - 작성자만 수정/삭제 가능
   
   ### 🔄 상태 변경
   - 초안 → 공개 → 비공개
   - 상태별 배지 표시
   
   ### 🔗 연관관계
   - User ↔ Post (1:N 양방향)
   - Board ↔ Post (1:N 양방향)
   - "내 글" 페이지
   
   ## 🌿 Gitflow 브랜치 구조
   
   - **main**: 프로덕션 브랜치
   - **develop**: 개발 통합 브랜치
   - **release/1.0.0**: 릴리즈 준비
   - **feature/***: 6개의 기능 개발 브랜치
   
   ## 📊 프로젝트 통계
   
   - Python 파일: 27개
   - HTML 템플릿: 9개
   - 총 코드: 1,968줄
   - Git 커밋: 10개
   
   ## 🚀 실행 방법
   
   ```bash
   # 1. 저장소 클론
   git clone https://github.com/giyeop-cody/B5-3.git
   cd B5-3
   
   # 2. 가상환경 활성화
   source venv/bin/activate
   
   # 3. DB 초기화
   python -m app.init_db
   
   # 4. 서버 실행
   uvicorn app.main:app --reload --port 8000
   ```
   
   ## 🔑 테스트 계정
   
   - **ID**: testuser
   - **PW**: test1234
   
   ## 📚 문서
   
   - `README.md`: 프로젝트 사용법
   - `GITFLOW.md`: Gitflow 브랜칭 전략 가이드
   - `GITFLOW_SUMMARY.md`: Gitflow 적용 완료 보고서
   - `IMPLEMENTATION_REPORT.md`: 구현 완료 보고서
   
   ## ✅ 체크리스트
   
   - [x] FastAPI 기반 사용자 인증
   - [x] 로그인 상태에 따른 UI 변화
   - [x] 접근 제어 (인가)
   - [x] 최소 3개 모델 (User, Board, Post)
   - [x] 1:N 연관관계 2개 이상
   - [x] 양방향 연관관계
   - [x] 상태 변경 기능
   - [x] SQLAlchemy + 관계형 DB
   - [x] Jinja2 템플릿 SSR
   - [x] 코드 구조 분리
   - [x] README 문서화
   - [x] Gitflow 브랜칭 전략 적용
   ```

6. **Create pull request 버튼 클릭**

---

## 🎯 4단계: PR 머지 (승인 후)

PR이 승인되면:

### GitHub 웹에서 머지

1. PR 페이지에서 "Merge pull request" 버튼 클릭
2. "Confirm merge" 클릭
3. 머지 완료!

### 로컬에서 동기화

```bash
# develop 브랜치로 이동
git checkout develop

# 원격 변경사항 가져오기
git pull origin develop

# main 브랜치로 이동
git checkout main

# develop을 main으로 머지
git merge develop

# 원격에 push
git push origin main
```

---

## 🔧 문제 해결

### 문제 1: 인증 실패

```bash
# SSH 키 확인
ssh-add -l

# SSH 키 추가
ssh-add ~/.ssh/id_ed25519

# 또는 HTTPS 토큰 재설정
git remote set-url origin https://<USERNAME>:<TOKEN>@github.com/giyeop-cody/B5-3.git
```

### 문제 2: 원격 브랜치가 이미 존재

```bash
# 강제 push (주의: 원격 변경사항 덮어씀)
git push -f origin develop

# 또는 원격 브랜치 삭제 후 재-push
git push origin --delete develop
git push -u origin develop
```

### 문제 3: 머지 충돌

```bash
# 충돌 해결 후
git add .
git commit -m "fix: 머지 충돌 해결"
git push origin develop
```

---

## 📝 Git 설정 (선택사항)

### 사용자 정보 설정

```bash
# 전역 설정
git config --global user.name "giyeop kim"
git config --global user.email "your-email@example.com"

# 또는 로컬 저장소만 설정
git config user.name "giyeop kim"
git config user.email "your-email@example.com"
```

### 기본 에디터 설정

```bash
# VS Code
git config --global core.editor "code --wait"

# Vim
git config --global core.editor "vim"
```

---

## 🎉 완료 후

PR이 머지되면:

1. ✅ GitHub 저장소에 코드가 통합됨
2. ✅ Gitflow 브랜치 구조가 원격에 반영됨
3. ✅ 팀원들이 코드를 리뷰하고 사용할 수 있음

---

## 📚 추가 자료

- [GitHub Pull Request 가이드](https://docs.github.com/ko/pull-requests)
- [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [SSH 키 설정](https://docs.github.com/ko/authentication/connecting-to-github-with-ssh)

---

**성공적인 PR을 기원합니다!** 🚀✨
