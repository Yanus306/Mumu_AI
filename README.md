## 🤝 Mumu AI 협업 가이드라인

### 🌿 1. 브랜치 (Branch Strategy)
**`main` 브랜치는 배포 및 기준 브랜치입니다. `main` 브랜치로의 직접 커밋 및 푸시(Push)는 시스템적으로 차단되어 있음..** 
모든 작업은 용도에 맞는 새로운 브랜치를 생성하여 진행

#### 📌 브랜치 네이밍 규칙
* `feature/기능명`: 새로운 기능 추가
* `fix/이슈명`: 버그 및 오류 수정
* `refactor/내용`: 코드 리팩토링 (기능 변화 없음)
* `hotfix/긴급수정`: 배포 후 발생한 긴급 버그 수정

#### 💻 작업 시작 명령어 예시
```bash
# 로그인 UI 기능을 개발할 때
git checkout -b feature/login-ui

### 💬 커밋 메시지 형식
```text
<type>(<scope>): <subject>

🏷️ Type 목록
feat: 새로운 기능 추가

fix: 버그 수정

docs: 문서 수정 (README.md 등)

style: 코드 포맷팅, 세미콜론 누락 수정 (코드 로직 변경 없음)

refactor: 코드 리팩토링

perf: 성능 개선

test: 테스트 코드 추가 및 수정

build: 빌드 시스템 또는 의존성(패키지) 관련 변경

ci: CI 설정 파일 및 스크립트 변경

chore: 기타 자잘한 작업 (빌드 업무 수정 등)
