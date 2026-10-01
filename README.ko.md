# Universal Agent Harness Builder v0.2.0

기존 **Codex Harness Builder**를 확장한 범용 개발 에이전트 하네스 빌더입니다.

한 프로젝트의 지식은 한 번만 관리하고, 사용하는 개발 에이전트 런타임에 맞는 어댑터만 생성합니다.

지원 대상:

- OpenAI Codex
- Google Antigravity IDE / Antigravity CLI (Claude를 reasoning model로 선택해도 동일)
- Anthropic Claude Code

## 핵심 구조

```text
PROJECT/
├─ AGENTS.md
├─ .project-context/
│  ├─ PROJECT.md
│  ├─ ARCHITECTURE.md
│  ├─ DECISIONS.md
│  ├─ MEMORY.md
│  ├─ LESSONS.md
│  └─ TODO.md
├─ .harness/
│  ├─ manifest.json
│  └─ plans/
├─ .codex/                 # Codex 사용 시
├─ .agents/                # Antigravity 사용 시
└─ .claude/ + CLAUDE.md    # Claude Code 사용 시
```

`AGENTS.md`와 `.project-context/`는 공통입니다. 플랫폼 전용 설정만 분리됩니다.

## 왜 이렇게 구성했나

- 프로젝트 전체 PRD와 모든 문서를 매 작업마다 읽지 않도록 합니다.
- 검색/조사 결과가 메인 대화 Context를 과도하게 차지하지 않도록 Subagent에 위임합니다.
- SMALL 프로젝트에는 불필요한 역할을 만들지 않습니다.
- 기존 코드, API, DB schema, 설정을 기본적으로 보존합니다.
- `MEMORY.md`를 작게 유지하고 장기 정보만 남깁니다.
- Claude Code에서는 `CLAUDE.md`가 `@AGENTS.md`를 import하여 공통 규칙을 중복 관리하지 않습니다.
- Antigravity에서 Claude 모델을 선택해도 Antigravity Runtime의 `.agents/` 설정을 사용합니다.

## 자연어 명령

설치 후 각 IDE/CLI에서 다음과 같이 요청할 수 있습니다.

```text
하네스 구성해줘
하네스 업데이트해줘
하네스 점검해줘
하네스 경량화해줘
기존 하네스를 유니버설로 전환해줘
```

## 1. Codex 설치

```powershell
codex plugin marketplace add JEREMI-Oh/codex-harness-builder --ref main
codex plugin marketplace list
```

Codex에서 `/plugins`를 열고 **Universal Agent Harness Builder**를 설치합니다.

실제 프로젝트 폴더에서 새 Codex 세션을 시작하고:

```text
하네스 구성해줘
```

## 2. Antigravity IDE 설치

### 전역 설치 (모든 프로젝트)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install_antigravity.ps1 -Scope Global
```

설치 위치:

```text
%USERPROFILE%\.gemini\config\plugins\universal-agent-harness-builder\
```

### 특정 프로젝트만

```powershell
.\scripts\install_antigravity.ps1 -Scope Workspace -ProjectPath "C:\work\my-project"
```

설치 위치:

```text
C:\work\my-project\.agents\plugins\universal-agent-harness-builder\
```

Antigravity IDE에서 Claude 모델을 선택한 상태에서도 그대로 사용할 수 있습니다. 실행 주체는 Antigravity Runtime이므로 생성 대상은 `.agents/`입니다.

프로젝트를 열고:

```text
하네스 구성해줘
```

## 3. Claude Code 설치

```powershell
claude plugin marketplace add JEREMI-Oh/codex-harness-builder
claude plugin install universal-agent-harness-builder@universal-agent-harness
```

필요 시 Claude Code 안에서 `/reload-plugins`를 실행합니다.

그 다음 프로젝트에서:

```text
하네스 구성해줘
```

Claude Code용 하네스는 `CLAUDE.md`에서 `@AGENTS.md`를 가져오고 `.claude/agents/`에 역할별 Subagent를 구성합니다.

## 직접 CLI로 사용

플러그인 없이도 사용할 수 있습니다.

### 분석

```powershell
python .\src\harness.py analyze --project "C:\work\my-project"
```

### Codex만

```powershell
python .\src\harness.py init --project "C:\work\my-project" --target codex --dry-run
python .\src\harness.py init --project "C:\work\my-project" --target codex
```

### Antigravity만

```powershell
python .\src\harness.py init --project "C:\work\my-project" --target antigravity
```

### Claude Code만

```powershell
python .\src\harness.py init --project "C:\work\my-project" --target claude-code
```

### 세 환경 모두

```powershell
python .\src\harness.py init --project "C:\work\my-project" --target all
```

## 기존 진행 중 프로젝트에 적용

기존 프로젝트에서 먼저 Git 상태를 정리하는 것을 권장합니다.

```powershell
cd C:\work\existing-project
git status
```

그 다음 사용하는 플랫폼에서 `하네스 구성해줘`라고 요청합니다.

빌더는 다음을 하지 않습니다.

- 애플리케이션 소스코드 수정
- 기존 `AGENTS.md` 전체 덮어쓰기
- 기존 사용자 작성 Agent/Rule 파일 덮어쓰기
- DB schema 임의 변경
- MCP 서버 자동 추가

충돌이 있으면 `conflict`로 보고하고 기존 파일을 보존합니다.

## V0.1 Codex Harness Builder에서 마이그레이션

```powershell
python .\src\harness.py migrate --project "C:\work\existing-project" --target all --dry-run
python .\src\harness.py migrate --project "C:\work\existing-project" --target all
python .\src\harness.py audit --project "C:\work\existing-project" --target all
```

기존 `CODEX-HARNESS` managed block은 `UNIVERSAL-HARNESS` block으로 교체되며 기존 사용자 내용은 보존됩니다.

## 역할 정책

| 프로젝트 | 역할 |
|---|---|
| SMALL | 기본적으로 Main Agent만 사용 |
| MEDIUM | researcher, developer, tester, reviewer |
| LARGE | architect + MEDIUM 역할 |

플랫폼별 역할 파일:

```text
Codex       .codex/agents/*.toml
Antigravity .agents/agents/*.md
Claude Code .claude/agents/*.md
```

Antigravity agent의 `model`은 `inherit`로 설정하므로 IDE에서 Claude를 선택했다면 해당 모델 계열을 그대로 따릅니다.

## 안전 원칙

- Secret을 `.project-context/`에 기록하지 않습니다.
- `MEMORY.md`는 작게 유지합니다.
- 관련 파일부터 조사합니다.
- 단순 작업에 불필요한 Multi-Agent를 사용하지 않습니다.
- 위험한 변경은 계획 → 구현 → 테스트 → 리뷰 순서로 진행합니다.
- 기존 사용자 파일은 generator sentinel이 없는 경우 덮어쓰지 않습니다.

## 테스트

```powershell
python -m unittest discover -s tests -v
```

## 라이선스

MIT
