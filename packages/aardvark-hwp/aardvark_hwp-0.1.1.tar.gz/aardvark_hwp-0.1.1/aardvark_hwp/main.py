"""
Aardvark HWP MCP 서버 진입점
"""

import os
from .server import mcp


def main():
    """uvx 명령어로 실행될 메인 함수"""
    
    print("Starting Aardvark HWP MCP Server...")
    
    # 서버 실행
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()