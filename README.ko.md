# Codex Harness Builder

Codex 프로젝트에 **토큰 절약형 개발 하네스**를 자동으로 구축하는 공개 프로젝트/플러그인입니다.

설치 후 프로젝트에서 다음처럼 요청하는 것을 목표로 합니다.

> 하네스 구성해줘

그러면 현재 저장소를 분석하여 프로젝트 규모와 기술 스택에 맞게 필요한 구성만 생성합니다.

## 핵심 기능

- 프로젝트 기술 스택 자동 감지
- SMALL / MEDIUM / LARGE 복잡도 분류
- 기존 `AGENTS.md` 보존 + 관리 블록 추가
- Codex 커스텀 Subagent 자동 구성
- 프로젝트 컨텍스트/설계결정/교훈/할일 파일 생성
- 복잡한 프로젝트만 실행계획 구조 생성
- 재실행 시 중복 생성 방지
- 하네스 점검 및 경량화
- 별도 MCP 서버 없이 동작하는 V1 구조

## GitHub에 바로 공개하기

Windows PowerShell에서 GitHub CLI 인증이 되어 있다면:

```powershell
./scripts/publish_github.ps1
```

스크립트가 `JEREMI-Oh/codex-harness-builder` 공개 저장소를 생성하고 `main`을 push합니다.

## 설치

GitHub에 `JEREMI-Oh/codex-harness-builder`로 공개한 뒤:

```bash
codex plugin marketplace add JEREMI-Oh/codex-harness-builder
```

이후 ChatGPT/Codex 데스크톱 앱의 Plugins Directory에서 **Codex Harness Builder**를 설치합니다.

로컬 테스트:

```bash
codex plugin marketplace add .
```

## 사용 명령

자연어:

- `하네스 구성해줘`
- `하네스 업데이트해줘`
- `하네스 점검해줘`
- `하네스 경량화해줘`

CLI:

```bash
python plugins/codex-harness-builder/scripts/harness.py analyze --project .
python plugins/codex-harness-builder/scripts/harness.py init --project .
python plugins/codex-harness-builder/scripts/harness.py audit --project .
```

## 생성 예시

```text
AGENTS.md
.codex/
  config.toml
  agents/
.project-context/
  PROJECT.md
  ARCHITECTURE.md
  DECISIONS.md
  MEMORY.md
  LESSONS.md
  TODO.md
.agent/
  PLANS.md
  plans/
```

작은 프로젝트에는 불필요한 Subagent와 Plan 구조를 만들지 않습니다.

## 핵심 원칙

1. 전체 저장소를 매번 읽지 않는다.
2. 관련 파일부터 찾는다.
3. 간단한 작업에는 멀티에이전트를 남발하지 않는다.
4. Subagent에는 필요한 컨텍스트만 전달한다.
5. 영구적으로 필요한 사실만 `MEMORY.md`에 기록한다.
6. 반복 가능한 문제 해결 경험은 `LESSONS.md`에 기록한다.
7. 기존 프로젝트 설정을 강제로 덮어쓰지 않는다.
8. 비밀번호, API Key, 토큰 등 비밀정보는 메모리에 기록하지 않는다.

## 공개 플러그인 디렉터리

이 저장소는 GitHub 기반 Codex marketplace source로 바로 사용할 수 있도록 구성되어 있습니다. OpenAI의 Universal Plugins Directory에 정식 공개하는 과정은 별도의 업로드/검토 절차가 필요합니다.

## 라이선스

MIT
