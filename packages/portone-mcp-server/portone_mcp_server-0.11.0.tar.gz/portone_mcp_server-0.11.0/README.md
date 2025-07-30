# PortOne MCP Server

포트원 사용자를 위한 MCP (Model Context Protocol) 서버입니다. 포트원 개발자센터, 헬프센터 등 공식 문서 내용을 LLM(Large Language Model)에 제공해 정확한 정보를 바탕으로 사용자의 연동 및 질의를 돕도록 합니다.

## MCP 서버 등록하기

1. [uv](https://docs.astral.sh/uv/getting-started/installation/)가 설치되어 있어야 합니다.
1. 사용하는 AI 도구의 MCP 설정에서 아래 내용을 추가합니다. (Cursor, Windsurf, Claude Desktop, etc...)

   ```json
   "mcpServers": {

     // 기존 설정

     "portone-mcp-server": {
       "command": "uvx",
       "args": [
         "portone-mcp-server@latest"
       ]
     }
   }
   ```

1. 도구를 재시작해 portone-mcp-server 및 해당 서버가 제공하는 도구들이 잘 등록되었는지 확인합니다.

## 개발하기

### 요구사항

- Python 3.12 이상
- [uv (Python 패키지 관리 도구)](https://docs.astral.sh/uv/getting-started/installation/)

1. 저장소를 클론한 후 필요한 패키지 설치하기

   ```bash
   uv sync
   ```

1. MCP 서버 실행

   ```bash
   uv run portone-mcp-server
   ```

1. 테스트

   ```bash
   uv run pytest
   ```

1. 코드 린팅

   ```bash
   uv run ruff check .
   uv run ruff format .
   ```

1. 퍼블리싱

   ```bash
   # 먼저 pyproject.toml의 version을 변경합니다.
   rm -rf dist
   uv sync
   uv build
   uv publish
   ```

1. 로컬 환경의 MCP 서버 등록하기

   ```json
   "mcpServers": {
      "portone-mcp-server": {
      "command": "uv",
      "args": [
         "--directory",
         "/your/absolute/path/to/portone-mcp-server",
         "run",
         "portone-mcp-server"
      ]
      }
   }
   ```

1. 문서 업데이트하기

   요구사항:

   - 로컬에 developers.portone.io, help.portone.io 저장소가 클론되어 있어야 합니다.
   - nvm (Node Version Manager) 및 노드 20, 23 버전이 설치되어 있어야 합니다.
   - corepack이 설치되어 있어야 합니다.

   developers.portone.io 저장소에서 생성된 문서를 MCP 서버에 업데이트하려면 다음과 같이 실행합니다:

   ```bash
   # 환경 변수를 사용하는 방법
   export DEVELOPERS_PORTONE_IO_PATH="/path/to/developers.portone.io"
   export HELP_PORTONE_IO_PATH="/path/to/help.portone.io"
   uv run update_docs.py

   # 또는 대화형으로 실행
   uv run update_docs.py
   # 프롬프트가 표시되면 developers.portone.io, help.portone.io 저장소 경로 입력
   ```

   이 스크립트는 다음을 수행합니다:

   1. developers.portone.io, help.portone.io 저장소에서 `pnpm docs-for-llms` 명령을 실행 (로컬에 설정된 브랜치 기준으로 문서 생성)
   2. MCP 서버의 docs 디렉토리를 새로 생성된 내용으로 교체
   3. 개발자센터, 헬프센터 외 일부 문서 다운로드 및 교체

## 라이선스

[Apache License 2.0](LICENSE)
