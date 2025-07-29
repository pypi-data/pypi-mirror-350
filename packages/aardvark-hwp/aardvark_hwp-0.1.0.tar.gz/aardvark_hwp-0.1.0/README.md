# Aardvark HWP 📄

PDF와 HWP(한글) 파일 간 변환을 지원하는 Model Context Protocol (MCP) 서버입니다.

## 🚀 설치 및 실행

### uvx로 바로 실행 (권장)

```bash
# API 키 설정 후 실행
uvx aardvark-hwp
```

또는 Windows에서:

```cmd
uvx aardvark-hwp
```

### pip로 설치

```bash
pip install aardvark-hwp
```

## 🔧 필수 설정

### 환경 변수

- `HANGUL_API_BASE`: 한글 API 서버 URL (선택적, 기본값: https://hangul.ngrok.app/api)


## 📋 주요 기능

- **PDF → HWP 변환**: PDF 문서를 한글 파일로 변환
- **HWP → XML 변환**: 한글 파일을 XML 형식으로 변환
- **문서 서식 학습**: 기존 HWP 파일의 서식을 학습하여 새 문서에 적용
- **텍스트 편집**: XML 문서의 내용을 수정하고 편집
- **문법 검사**: HWPML 문서의 구조와 문법 검증

## 🛠️ 지원 도구

### 변환 도구
- `convert_pdf_to_hwp()`: PDF를 HWP로 변환하는 워크플로우 시작
- `convert_pdf_to_html()`: PDF를 HTML로 변환
- `convert_hwp_to_xml_and_xsl()`: HWP를 XML과 XSL로 변환
- `convert_xml_and_xsl_to_hwp()`: XML과 XSL을 HWP로 변환

### 편집 도구
- `create_xml()`: 빈 XML 파일 생성
- `add_lines()`: 파일 끝에 내용 추가
- `insert_lines()`: 특정 위치에 내용 삽입
- `patch_lines()`: 특정 범위의 내용 대체
- `read_lines()`: 파일의 특정 범위 읽기

### 검증 도구
- `lint_xml()`: XML 문법 및 구조 검증

## 💡 사용 예시

### Claude Desktop에서 사용

`claude_desktop_config.json`에 다음과 같이 추가:

```json
{
  "mcpServers": {
    "aardvark-hwp": {
      "command": "uvx",
      "args": ["aardvark-hwp"]
    }
  }
}
```

### 기본 워크플로우

1. **PDF를 HWP로 변환**:
   - `convert_pdf_to_hwp()` 실행
   - 활성화 코드 입력
   - 템플릿 HWP 파일 경로 제공
   - PDF 파일 경로 제공
   - 저장할 위치 지정

2. **문서 편집**:
   - 생성된 XML 파일을 `read_lines()`로 확인
   - `patch_lines()` 또는 `insert_lines()`로 내용 수정
   - `lint_xml()`로 문법 검증

## 🏗️ 개발

```bash
git clone https://github.com/your-username/aardvark-hwp
cd aardvark-hwp
pip install -e .
```

## 📄 라이선스

MIT License

## 🤝 기여

Issue 및 Pull Request를 환영합니다!

## 📞 지원

문제가 있으시면 GitHub Issues에 등록해주세요.
