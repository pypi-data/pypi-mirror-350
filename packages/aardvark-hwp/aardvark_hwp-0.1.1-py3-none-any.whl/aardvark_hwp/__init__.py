"""
Aardvark HWP - 한글 파일 변환 및 처리를 위한 MCP 서버

PDF와 HWP 파일 간 상호 변환을 지원하는 Model Context Protocol 서버입니다.
"""

__version__ = "0.1.0"

from .server import mcp

__all__ = ["mcp"] 