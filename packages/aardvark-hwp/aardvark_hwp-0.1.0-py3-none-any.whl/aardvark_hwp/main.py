"""
Aardvark HWP MCP 서버 진입점
"""

import os
from .server import mcp


def main():
    """uvx 명령어로 실행될 메인 함수"""
    
    print("🏗️  Aardvark HWP MCP 서버를 시작합니다...")
    print("📄 PDF와 HWP 파일 간 변환을 지원합니다.")
    print("🔧 환경 설정:")
    print(f"   - HANGUL_API_BASE: {os.environ.get('HANGUL_API_BASE', '기본값 사용')}")
    print()
    
    # 서버 실행
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()