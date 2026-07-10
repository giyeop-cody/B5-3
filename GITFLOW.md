# Gitflow 브랜칭 전략

이 프로젝트는 **Gitflow** 브랜칭 전략을 따릅니다.

## 🌿 브랜치 구조

```
main (프로덕션)
  │
  ├─→ release/1.0.0 (릴리즈 준비)
  │     │
  │     └── develop (개발 통합)
  │           │
  │           ├── feature/step1-init (초기 구조)
  │           ├── feature/step2-database (DB 모델)
  │           ├── feature/step3-crud-api (CRUD API)
  │           ├── feature/step4-auth (인증 시스템)
  │           ├── feature/step5-templates (화면 구현)
  │           └── feature/step6-relationships (연관관계)
  │
  └─→ hotfix/* (긴급 수정 - 필요시)
```

## 📋 브랜치 설명

### 영구 브랜치 (Permanent Branches)

#### `main`
- **용도**: 프로덕션 배포 브랜치
- **특징**: 항상 배포 가능한 상태 유지
- **현재 상태**: 초기 프로젝트 구조 (b667221)
- **머지 시점**: release 브랜치에서 테스트 완료 후

#### `develop`
- **용도**: 개발 통합 브랜치
- **특징**: 모든 기능 개발이 통합되는 브랜치
- **현재 상태**: 모든 기능 구현 완료 (6f68b33)
- **머지 대상**: feature 브랜치들이 머지됨

### 임시 브랜치 (Temporary Branches)

#### `feature/*`
- **용도**: 새로운 기능 개발
- **생성 시점**: develop에서 분기
- **머지 시점**: 기능 완료 후 develop으로 머지
- **네이밍 규칙**: `feature/<기능명>`

**현재 feature 브랜치:**

| 브랜치명 | 설명 | 커밋 |
|---------|------|------|
| `feature/step1-init` | 초기 프로젝트 구조 | b667221 |
| `feature/step2-database` | 데이터베이스 모델 설계 | aa5f558 |
| `feature/step3-crud-api` | 기본 CRUD API 구현 | e245395 |
| `feature/step4-auth` | 세션 기반 인증 시스템 | fbc3430 |
| `feature/step5-templates` | Jinja2 템플릿 화면 | 694508b |
| `feature/step6-relationships` | 연관관계 활용 | a8002ee |

#### `release/*`
- **용도**: 릴리즈 준비 및 테스트
- **생성 시점**: develop에서 분기 (기능 개발 완료 후)
- **머지 시점**: main과 develop 양쪽으로 머지
- **네이밍 규칙**: `release/<버전>`

**현재 release 브랜치:**
- `release/1.0.0`: 첫 번째 릴리즈 준비 (6f68b33)

#### `hotfix/*` (필요시 생성)
- **용도**: 프로덕션 긴급 버그 수정
- **생성 시점**: main에서 분기
- **머지 시점**: main과 develop 양쪽으로 머지
- **네이밍 규칙**: `hotfix/<버그명>`

## 🔄 워크플로우

### 1. 기능 개발 (Feature Development)

```bash
# 1. develop에서 feature 브랜치 생성
git checkout develop
git checkout -b feature/new-feature

# 2. 기능 개발 및 커밋
git add .
git commit -m "feat: 새로운 기능 추가"

# 3. develop으로 머지
git checkout develop
git merge --no-ff feature/new-feature

# 4. feature 브랜치 삭제
git branch -d feature/new-feature
```

### 2. 릴리즈 준비 (Release)

```bash
# 1. develop에서 release 브랜치 생성
git checkout develop
git checkout -b release/1.0.0

# 2. 릴리즈 준비 (버그 수정, 문서 업데이트 등)
git commit -m "docs: 릴리즈 노트 업데이트"

# 3. main으로 머지 및 태그
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0

# 4. develop으로 머지 (릴리즈 중 수정사항 반영)
git checkout develop
git merge --no-ff release/1.0.0

# 5. release 브랜치 삭제
git branch -d release/1.0.0
```

### 3. 긴급 수정 (Hotfix)

```bash
# 1. main에서 hotfix 브랜치 생성
git checkout main
git checkout -b hotfix/critical-bug

# 2. 버그 수정
git commit -m "fix: 치명적인 버그 수정"

# 3. main으로 머지 및 태그
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.0.1

# 4. develop으로 머지
git checkout develop
git merge --no-ff hotfix/critical-bug

# 5. hotfix 브랜치 삭제
git branch -d hotfix/critical-bug
```

## 📊 현재 프로젝트 상태

### 브랜치별 커밋 수

| 브랜치 | 커밋 수 | 최신 커밋 |
|--------|---------|----------|
| main | 1 | b667221 (초기 구조) |
| develop | 8 | 6f68b33 (구현 완료) |
| release/1.0.0 | 8 | 6f68b33 (구현 완료) |

### 개발 히스토리

```
develop: b667221 → aa5f558 → e245395 → fbc3430 → 694508b → a8002ee → 6f68b33
         (Step 1)  (Step 2)  (Step 3)  (Step 4)  (Step 5)  (Step 6)  (완료)
```

## 🎯 Gitflow의 장점

1. **명확한 브랜치 역할**
   - 각 브랜치의 목적과 수명이 명확
   - 팀원 간 협업 시 혼란 최소화

2. **안정적인 프로덕션**
   - main 브랜치는 항상 배포 가능
   - develop에서 충분히 테스트 후 머지

3. **체계적인 릴리즈 관리**
   - release 브랜치로 릴리즈 준비
   - 버전 태깅으로 릴리즈 추적

4. **긴급 대응 가능**
   - hotfix 브랜치로 빠른 버그 수정
   - main과 develop 모두에 반영

## 📝 커밋 메시지 규칙

Gitflow에서는 커밋 메시지도 중요합니다:

```
<타입>: <간단한 설명>

<상세 설명 (선택)>

- 변경 사항 1
- 변경 사항 2
```

### 타입
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅
- `refactor`: 리팩토링
- `test`: 테스트 코드
- `chore`: 빌드, 패키지 등

## 🔍 유용한 Git 명령어

```bash
# 모든 브랜치 보기
git branch -a

# 브랜치별 커밋 히스토리 보기
git log --oneline --graph --all

# 특정 브랜치의 최신 커밋 보기
git log <branch-name> --oneline -1

# 브랜치 간 차이점 보기
git diff develop..main

# 브랜치 머지 그래프 보기
git log --graph --oneline --decorate --all
```

## 📚 참고 자료

- [A successful Git branching model (Vincent Driessen)](https://nvie.com/posts/a-successful-git-branching-model/)
- [Gitflow Workflow (Atlassian)](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

---

**이 프로젝트는 Gitflow 전략을 통해 체계적으로 개발되었습니다!** 🚀
