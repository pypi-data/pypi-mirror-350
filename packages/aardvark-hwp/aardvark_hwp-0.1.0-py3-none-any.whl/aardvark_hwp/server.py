from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.resources import TextResource
import base64
import os
import tempfile
from lxml import etree


# FastMCP 서버 초기화
mcp = FastMCP("aardvark-hwp")

# 한글 API 서버 URL 및 API 키 설정
HANGUL_API_BASE = os.environ.get("HANGUL_API_BASE", "https://hangul.ngrok.app/api")
PDF_TO_HTML_API_URL = os.environ.get("PDF_TO_HTML_API_URL", "https://pdf-to-html-1005510057464.asia-northeast1.run.app/pdf-to-html")


async def call_pdf_to_html_api(file_path) -> str:
    """
    Convert PDF file to HTML using GCP Cloud Run function
    
    Args:
        file_path (str): Path to PDF file
        
    Returns:
        str: HTML content from API response
    """
    api_url = PDF_TO_HTML_API_URL
    
    # 파일 읽기
    with open(file_path, "rb") as f:
        file_content = f.read()
    
    # httpx 비동기 클라이언트 사용
    async with httpx.AsyncClient() as client:
        files = {"document": file_content}
        request_data = {
            "ocr": "force", 
            "base64_encoding": "['table']", 
            "model": "document-parse"
        }
        
        response = await client.post(api_url, files=files, data=request_data)
        response_data = response.json()
        try:
            return response_data['content']['html']
        except Exception as e:
            raise e


async def call_hwp_to_xml_api(hwp_data: bytes, activation_code: str) -> dict:
    """한글 API 서버에 HWP 파일을 XML로 변환 요청을 보냅니다.
    
    Args:
        hwp_data: HWP 파일 바이너리 데이터
        activation_code: API 활성화 코드
    
    Returns:
        변환 결과 정보가 담긴 딕셔너리
    """
    url = f"{HANGUL_API_BASE}/convert/hwp-to-xml"
    
    # HWP 데이터 base64 인코딩
    hwp_data_base64 = base64.b64encode(hwp_data).decode('utf-8')
    
    # JSON 데이터 준비
    json_data = {
        'hwp_data': hwp_data_base64,
        'activation_code': activation_code
    }
    
    # API 요청 전송
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json_data)
        
        if response.status_code != 200:
            raise ValueError(f"API 요청 실패: {response.status_code} - {response.text}")
        
        # 응답 처리
        result = response.json()
        print(result)
        return result


#############

    # 그 다음, 변환된 xsl 파일을 300줄씩 읽어가면서 스타일을 분석하고, 아래 양식에 맞게 정리해서 add_to_memory()로 기억에 저장해.
    # [유저가 제공한 hwp 파일에서 추출한 xsl 스타일시트 위치]
    # ...
    # [문서 작성 AI를 위한 HWPML 스타일 가이드라인]
    # ...

@mcp.tool()
async def init_guideline() -> Dict[str, Any]:
    """가이드라인 파일을 초기화합니다.
    
    Returns:
        초기화 결과 정보
    """
    try:
        guideline_path = os.path.join(tempfile.gettempdir(), "guideline.txt")
        
        # 빈 파일 생성
        with open(guideline_path, 'w', encoding='utf-8') as f:
            f.write("")
        
        return {
            "success": True,
            "message": "가이드라인 파일이 초기화되었습니다.",
            "file_path": guideline_path
        }
    
    except Exception as e:
        return {"success": False, "error": f"가이드라인 초기화 오류: {str(e)}"}


@mcp.tool()
async def add_to_guideline(text_to_add: str):
    """가이드라인 텍스트를 추가합니다.
    
    Args:
        text_to_add: 추가할 텍스트
    """
    guideline_path = os.path.join(tempfile.gettempdir(), "guideline.txt")
    
    # 파일이 존재하면 내용을 읽고, 없으면 빈 문자열로 시작
    current_guideline = ""
    if os.path.exists(guideline_path):
        with open(guideline_path, 'r', encoding='utf-8') as f:
            current_guideline = f.read()
    
    # 새 내용 추가
    updated_guideline = current_guideline + text_to_add
    
    # 파일에 저장
    with open(guideline_path, 'w', encoding='utf-8') as f:
        f.write(updated_guideline)
    
    return {"success": True, "message": "가이드라인이 업데이트되었습니다."}

@mcp.tool()
async def read_guideline() -> str:
    """가이드라인 텍스트를 읽어옵니다.
    
    Returns:
        가이드라인 텍스트
    """
    guideline_path = os.path.join(tempfile.gettempdir(), "guideline.txt")
    
    if not os.path.exists(guideline_path):
        return {"success": False, "error": "가이드라인 파일이 아직 생성되지 않았습니다."}
    
    with open(guideline_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {"success": True, "content": content}

@mcp.tool(
        description="PDF를 한글 파일로 변환하는 워크플로우를 시작합니다."
        )
def convert_pdf_to_hwp() -> str:
    content = """
    지금부터 너는 내가 정해준 대로 대답해야 해.

    1. "활성화 코드를 입력해주세요." 라고 해. 내가 활성화 코드를 입력하면 다음으로 진행해.

    2. "한글 파일을 작성하기 전에, 먼저 서식을 학습해야 합니다. 한글 파일의 경로를 하나 알려주시면, 그 파일의 서식을 학습해 문서를 작성하겠습니다. (ex. '다운로드' 폴더에 있는 '템플릿.hwp')"라고 이야기해.
    한글 파일이 없으면 다음으로 진행할 수 없어.

    3. 내가 한글파일 경로를 알려주면, convert_hwp_to_xml_and_xsl tool을 사용해서 xml, xsl 파일로 변환해. 
    ===
    지금부터 위 단계를 정확하게 따르고, 절대로 뛰어넘거나 생략하지 마.
    """
    return content

@mcp.tool()
async def convert_hwp_to_xml_and_xsl(hwp_file_path: str, activation_code: str, context: Context) -> dict:
    # HWP 파일 읽기
    try:
        with open(hwp_file_path, "rb") as f:
            hwp_data = f.read()
    except FileNotFoundError:
        raise ValueError(f"파일을 찾을 수 없습니다. TIP: filesystem을 사용해 디렉토리를 탐색해보세요. 비슷한 파일이 있을 수 있습니다.")
    except Exception as e:
        raise ValueError(f"파일 읽기 오류: {str(e)}")

    await context.debug(f"파일 읽기 완료: {hwp_file_path}")
    
    # API 호출하여 HWP를 XML로 변환
    response = await call_hwp_to_xml_api(hwp_data, activation_code)

    await context.debug(f"HWP -> XML, XSL API 호출 완료: {response}")
    
    # 응답에서 XML 및 XSL 콘텐츠 추출 및 디코딩
    xml_content_base64 = response.get("xml_content")
    xsl_content_base64 = response.get("xsl_content")
    
    if not xml_content_base64 or not xsl_content_base64:
        raise ValueError("API 응답에 XML 또는 XSL 콘텐츠가 없습니다")
    
    xml_content = base64.b64decode(xml_content_base64).decode('utf-8')
    xsl_content = base64.b64decode(xsl_content_base64).decode('utf-8')
    
    # 임시 디렉토리에 파일 저장
    import os
    import tempfile
    
    tmp_dir = tempfile.gettempdir()
    hwp_file_name = os.path.basename(hwp_file_path).split('.')[0]
    
    xml_path = os.path.join(tmp_dir, f"{hwp_file_name}.xml")
    xsl_path = os.path.join(tmp_dir, f"{hwp_file_name}.xsl")
    
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    with open(xsl_path, 'w', encoding='utf-8') as f:
        f.write(xsl_content)
    
    await context.debug(f"임시 파일 저장 완료: {xml_path} / {xsl_path}")

    ANALYSIS_RESULT = f"""
    ## 파일 분석 결과
이 파일은 HWP(한컴 한글 워드프로세서)와 호환되는 HWPML 표준의 XML 파일입니다.

HWPML은 다음과 같은 계층 구조를 가집니다:
- 최상위 요소: `<HWPML>`
- 본문 구조: `<BODY>` → `<SECTION>` → `<P>` (문단) → `<TEXT>` (텍스트) → `<CHAR>` (문자)
- 문단 속성: ParaShape, Style, ColumnBreak, PageBreak 등
- 텍스트 속성: CharShape

특수 요소:
- 표: `<TABLE>` → `<ROW>` → `<CELL>` → `<PARALIST>` → `<P>`
- 도형: `<POLYGON>`, `<RECTANGLE>`, `<PICTURE>` 등
- 컨테이너: `<CONTAINER>` (여러 도형 요소를 그룹화)
- 특수 문자: `<NBSPACE>` (줄바꿈 없는 공백), `<FWSPACE>` (고정폭 공백)

## HWPML 주요 문법 규칙:

1. **XML 선언과 스타일시트 참조**
   ```xml
   <?xml version="1.0" encoding="UTF-8" standalone="no" ?>
   <?xml-stylesheet type="text/xsl" href="{hwp_file_name}.xsl"?>
   <HWPML Style="export" SubVersion="10.0.0.0" Version="2.91">

2. **문단 구조 생성**

모든 텍스트는 <P> → <TEXT> → <CHAR> 계층 구조로 표현
문단은 반드시 ParaShape과 Style 속성을 가져야 함

```xml<P ParaShape="23" Style="19">
  <TEXT CharShape="16">
    <CHAR>내용</CHAR>
  </TEXT>
</P>

3. **텍스트 스타일 변경**

동일 문단 내에서도 스타일이 다른 텍스트는 별도의 <TEXT> 요소로 분리

```xml<P ParaShape="45" Style="0">
  <TEXT CharShape="15">
    <CHAR>일반 텍스트</CHAR>
  </TEXT>
  <TEXT CharShape="63">
    <CHAR>강조 텍스트</CHAR>
  </TEXT>
  <TEXT CharShape="15">
    <CHAR>다시 일반 텍스트</CHAR>
  </TEXT>
</P>

4. **특수 문자 처리**

공백: <NBSPACE/>, <FWSPACE/>
빈 텍스트: <CHAR/>


5. **빈 텍스트 처리**

내용이 없는 경우에도 <CHAR/> 태그 필요

```xml<TEXT CharShape="50">
  <CHAR/>
</TEXT>

6. **InstId 속성**

대부분의 요소는 고유 식별자인 InstId 속성을 가짐
참조용 HWPML의 InstId 값을 유지할 것

```xml<P InstId="2366748896" ParaShape="23" Style="19">

7. **테이블 구조**

테이블은 복잡한 중첩 구조를 가짐
셀 내부에는 <PARALIST> 요소가 필요하며, 그 안에 <P> 요소가 포함됨

```xml<TABLE BorderFill="4" CellSpacing="0" ColCount="1" RowCount="1">
  <SHAPEOBJECT InstId="2047192202"/>
  <ROW>
    <CELL BorderFill="7" ColAddr="0" RowAddr="0" Width="66616" Height="11058">
      <CELLMARGIN Bottom="141" Left="141" Right="141" Top="141"/>
      <PARALIST LineWrap="Break" TextDirection="0" VertAlign="Top">
        <P ParaShape="28" Style="0">
          <!-- 셀 내용 -->
        </P>
      </PARALIST>
    </CELL>
  </ROW>
</TABLE>


**구현 시 주의사항:**

1. XML 문법 준수
- 모든 태그는 올바르게 닫혀야 함
- 속성값은 따옴표로 묶어야 함


2. HWPML 특수 규칙
스타일 속성은 숫자 ID로 참조 (ID에 해당하는 스타일은 xsl에 정의되어 있음)


3. 문서 구조 일관성

문단, 텍스트 블록의 계층 구조 유지
스타일 변경 시 새로운 TEXT 요소 생성


4. 특수 문자 처리

공백, 줄바꿈 등 특수 문자는 전용 태그 사용
일반 텍스트와 혼합하지 않음


5. 복잡한 구조 처리

표, 이미지 등은 완전한 구조를 갖추어야 함
누락된 속성이나 하위 요소가 없어야 함
"""

    INSTRUCTION = """
    1. '분석이 끝났습니다! 서식을 완벽하게 학습했습니다. PDF 파일의 경로를 알려주시면, 한글파일 변환을 시작하겠습니다.' 라고 유저에게 말해.
    
    2. 유저가 PDF 경로를 알려주면, convert_pdf_to_html tool을 사용해. 
    ===
    위 단계를 정확히 따르고, 절대로 뛰어넘거나 생략하지 마."""

    if len(xml_content) > 10000:
        xml_content = xml_content[:10000] + "...(생략)"
    if len(xsl_content) > 10000:
        xsl_content = xsl_content[:10000] + "...(생략)"

    return {"xml_path": xml_path, "xsl_path": xsl_path, "xml_content": xml_content, "xsl_content": xsl_content, "analysis_result": ANALYSIS_RESULT, "instruction_for_next_step": INSTRUCTION}


@mcp.tool(description="""PDF 파일을 HTML로 변환합니다.
    
    Args:
        pdf_file_path: PDF 파일 경로
        
    Returns:
        변환된 HTML 파일 경로가 포함된 딕셔너리
    """)
async def convert_pdf_to_html(pdf_file_path: str) -> Dict[str, str]:
    try:
        # PDF 파일이 존재하는지 확인
        if not os.path.exists(pdf_file_path):
            raise ValueError(f"PDF 파일을 찾을 수 없습니다: {pdf_file_path}")
        
        # 임시 디렉토리 생성
        tmp_dir = tempfile.gettempdir()
        pdf_name = os.path.basename(pdf_file_path).split('.')[0]
        
        
        # 디렉토리 생성
        os.makedirs(tmp_dir, exist_ok=True)
        
        # pdf to html api 호출
        html_content = await call_pdf_to_html_api(pdf_file_path)

        # HTML 파일 저장
        html_file_path = os.path.join(tmp_dir, f"{pdf_name}.html")
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        INSTRUCTION = f"""
이제 html 파일을 참고해서 temp dir에 xml을 작성해.

## 작성 시 요구사항:
- 분석된 XML의 구조를 기반으로 하되, 내용만 HTML에서 추출한 시험 문제로 교체
- 분석된 XML의 모든 요소 ID 속성(ParaShape, CharShape 등) 그대로 유지
- 특수 요소(FOOTER, TABLE, POLYGON, RECTANGLE 등) 모두 보존

## 변환 과정:
1. 분석된 XML 구조에서 다음 요소들을 그대로 유지:
   - HEAD 섹션 전체 (스타일 정의 포함)
   - BODY 섹션의 기본 구조
   - 모든 특수 요소(FOOTER, TABLE, POLYGON 등)
   - 모든 ID 속성값 (ParaShape, CharShape 등)

2. XSL 파일은 참고용으로만 활용:
   - XSL 파일의 내용이 최종 HWPML에 직접 포함되지 않도록 주의
   - XSL 파일은 ID 체계와 스타일 정의를 이해하는 데만 활용

3. HTML 내용에서 시험 문제 텍스트만 추출하여:
   - 분석된 XML 구조에 대응하는 위치에 삽입
   - 분석된 XPML과 동일한 ParaShape, CharShape 속성 적용
   - 원본 문서의 레이아웃과 서식 유지

    (작성 팁)
    - 우선 create_xml을 사용해. 이 때, file_name에는 유저가 요청한 PDF 파일의 제목을 입력해.
    - create_xml이 완료되면, 기본적으로 xml 버전, 스타일시트, 루트 엘리먼트 등은 설정되어 있으니 그 부분은 수정하지 마.
    - 분량이 많으므로, add_lines를 사용해서 여러 줄로 나눠서 작성해.
    """
        
        
        return {
            "html_path": html_file_path, "html_content": html_content, "instruction_for_next_step": INSTRUCTION
        }
    
    except Exception as e:
        raise ValueError(f"PDF 변환 오류: {str(e)}")


@mcp.tool(description="""빈 XML 파일을 생성합니다.
    
    Args:
        file_name: 생성할 XML 파일 이름 (경로, 확장자 제외)
        
    Returns:
        생성된 XML 파일 경로가 포함된 딕셔너리, 생성된 파일 내용
    """)
async def create_xml(file_name: str) -> Dict[str, str]:
    
    try:
        tmp_dir = tempfile.gettempdir()
        xml_path = os.path.join(tmp_dir, f"{file_name}.xml")
        
        # 기본 HWPML 템플릿
        default_template = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?><?xml-stylesheet type="text/xsl" href="doc.xsl"?>
<HWPML Style="export" SubVersion="10.0.0.0" Version="2.91">
"""
        
        # 파일 생성
        with open(xml_path, 'w', encoding='utf-8') as f:
            f.write(default_template)
        
        return {"xml_path": xml_path, "xml_content": default_template}
    
    except Exception as e:
        raise ValueError(f"XML 파일 생성 오류: {str(e)}")


@mcp.tool(description="""파일 끝에 내용을 추가합니다. content는 5000자 이하여야 합니다.
    
    Args:
        file_path: 파일 경로
        content: 추가할 내용
        
    Returns:
        작업 결과 정보""")
async def add_lines(file_path: str, content: str, line_number: Optional[int] = None) -> Dict[str, Any]:
    """파일 끝에 내용을 추가합니다. content는 5000자 이하여야 합니다.
    
    Args:
        file_path: 파일 경로
        content: 추가할 내용
        line_number: 추가할 위치 (선택적, 기본값은 파일 끝)
        
    Returns:
        작업 결과 정보
    """
    # 내용 길이 검사
    if len(content) > 5000:
        excess_percentage = (len(content) - 5000) / 5000 * 100
        return {
            "success": False, 
            "error": f"내용이 5000자를 초과합니다. 현재 {len(content)}자로, 제한을 {excess_percentage:.1f}% 초과했습니다."
        }
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"파일을 찾을 수 없습니다: {file_path}"}
        
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 줄 끝에 개행 문자가 없다면 추가
        if content and not content.endswith('\n'):
            content += '\n'
        
        # 내용 추가
        if line_number is None:
            # 파일 끝에 추가
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)
        else:
            # 지정된 위치에 추가
            line_idx = min(max(0, line_number - 1), len(lines))
            lines.insert(line_idx, content)
            
            # 파일 쓰기
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        
        return {
            "success": True,
            "message": f"내용이 추가되었습니다.",
            "file_path": file_path,
            "line_number": line_number or len(lines) + 1
        }
    
    except Exception as e:
        return {"success": False, "error": f"파일 수정 오류: {str(e)}"}


@mcp.tool(description="""파일의 특정 라인 뒤에 내용을 삽입합니다. content는 5000자 이하여야 합니다.
    
    Args:
        file_path: 파일 경로
        after_line: 이 라인 뒤에 내용이 삽입됩니다 (1부터 시작)
        content: 삽입할 내용
        
    Returns:
        작업 결과 정보
    """)
async def insert_lines(file_path: str, after_line: int, content: str) -> Dict[str, Any]:
    # 내용 길이 검사
    if len(content) > 5000:
        excess_percentage = (len(content) - 5000) / 5000 * 100
        return {
            "success": False, 
            "error": f"내용이 5000자를 초과합니다. 현재 {len(content)}자로, 제한을 {excess_percentage:.1f}% 초과했습니다."
        }
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"파일을 찾을 수 없습니다: {file_path}"}
        
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 줄 번호 확인
        if after_line < 0 or after_line > len(lines):
            return {
                "success": False,
                "error": f"유효하지 않은 라인 번호: {after_line}. 파일은 총 {len(lines)}줄입니다."
            }
        
        # 내용 분할
        content_lines = content.split('\n')
        if content.endswith('\n'):
            content_lines = content_lines[:-1]
        
        # 각 줄에 개행 문자 추가
        content_lines = [line + '\n' for line in content_lines]
        
        # 내용 삽입
        insert_pos = after_line  # after_line 다음에 삽입
        new_lines = lines[:insert_pos] + content_lines + lines[insert_pos:]
        
        # 파일 쓰기
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return {
            "success": True,
            "message": f"라인 {after_line} 뒤에 내용이 삽입되었습니다.",
            "file_path": file_path,
            "inserted_lines": len(content_lines)
        }
    
    except Exception as e:
        return {"success": False, "error": f"파일 수정 오류: {str(e)}"}

@mcp.tool(description="""파일의 특정 라인 범위를 대체합니다. content는 5000자 이하여야 합니다.
    
    Args:
        file_path: 파일 경로
        start_line: 대체 시작 라인 번호 (1부터 시작)
        end_line: 대체 종료 라인 번호
        content: 대체할 내용
        
    Returns:
        작업 결과 정보
    """)
async def patch_lines(file_path: str, start_line: int, end_line: int, content: str) -> Dict[str, Any]:
    # 내용 길이 검사
    if len(content) > 5000:
        excess_percentage = (len(content) - 5000) / 5000 * 100
        return {
            "success": False, 
            "error": f"내용이 5000자를 초과합니다. 현재 {len(content)}자로, 제한을 {excess_percentage:.1f}% 초과했습니다."
        }
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"파일을 찾을 수 없습니다: {file_path}"}
        
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 줄 번호 확인
        if start_line < 1 or start_line > len(lines) or end_line < start_line or end_line > len(lines):
            return {
                "success": False,
                "error": f"유효하지 않은 라인 범위: {start_line}-{end_line}. 파일은 총 {len(lines)}줄입니다."
            }
        
        # 내용 분할 및 개행 문자 처리
        content_lines = content.split('\n')
        if content.endswith('\n'):
            content_lines = content_lines[:-1]
        
        # 각 줄에 개행 문자 추가
        content_lines = [line + '\n' for line in content_lines]
        
        # 라인 대체
        new_lines = lines[:start_line-1] + content_lines + lines[end_line:]
        
        # 파일 쓰기
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return {
            "success": True,
            "message": f"라인 {start_line}부터 {end_line}까지의 내용이 대체되었습니다.",
            "file_path": file_path,
            "replaced_lines": end_line - start_line + 1,
            "inserted_lines": len(content_lines)
        }
    
    except Exception as e:
        return {"success": False, "error": f"파일 수정 오류: {str(e)}"}


@mcp.tool(description="""파일의 특정 범위의 줄을 읽습니다.
    
    Args:
        file_path: 파일 경로
        start_line: 시작 줄 번호 (1부터 시작)
        end_line: 종료 줄 번호 (기본값: 파일 끝까지)
        
    Returns:
        파일 내용 정보
    """)
async def read_lines(file_path: str, start_line: int = 1, end_line: Optional[int] = None) -> Dict[str, Any]:
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"파일을 찾을 수 없습니다: {file_path}"}
        
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 줄 범위 조정
        start_idx = max(0, start_line - 1)
        end_idx = len(lines) if end_line is None else min(end_line, len(lines))
        
        # 줄 번호와 함께 내용 구성
        formatted_lines = []
        for i in range(start_idx, end_idx):
            line_num = i + 1
            line_content = lines[i].rstrip('\n')
            formatted_lines.append(f"{line_num}: {line_content}")
        
        # 결과 반환
        return {
            "success": True,
            "line_count": len(lines),
            "start_line": start_line,
            "end_line": end_idx,
            "content": '\n'.join(formatted_lines),
            "file_path": file_path
        }
    
    except Exception as e:
        return {"success": False, "error": f"파일 읽기 오류: {str(e)}"}

@mcp.tool()
async def lint_xml(xml_path: str) -> Dict[str, Any]:
    """HWPML 문서의 문법을 검사합니다.
    
    Args:
        xml_path: 검사할 HWPML 파일 경로
        
    Returns:
        검사 결과 정보
    """

    INSTRUCTION = """'변환이 거의 다 끝났습니다. 어디에 저장할까요?'라고 유저에게 물어봐.

    유저가 경로(output_path)를 알려주면, convert_xml_and_xsl_to_hwp tool을 사용해서 한글파일을 저장해.
    """

    if not os.path.exists(xml_path):
        return {"success": False, "error": f"파일을 찾을 수 없습니다: {xml_path}"}
    

    # XML 파일 파싱 시도
    try:
        parser = etree.XMLParser()
        
        try:
            tree = etree.parse(xml_path, parser)
            root = tree.getroot()
            
            # 기본 HWPML 구조 확인
            if root.tag != "HWPML":
                return {
                    "success": False, 
                    "error": f"루트 요소가 'HWPML'이 아닙니다: {root.tag}",
                    "file_path": xml_path
                }
            
            # 필수 섹션 확인
            body = root.find("BODY")
            
                
            if body is None:
                return {
                    "success": False, 
                    "error": "BODY 섹션이 없습니다",
                    "file_path": xml_path
                }
            
            # CHAR 요소 검사 - 부모가 TEXT인지 확인
            errors = []
            for i, char_elem in enumerate(root.xpath(".//CHAR")):
                parent = char_elem.getparent()
                if parent is None or parent.tag != "TEXT":
                    # 요소의 라인 번호 가져오기
                    elem_path = tree.getpath(char_elem)
                    errors.append(f"CHAR 요소(경로: {elem_path})의 부모가 TEXT가 아닙니다")
                
            # TEXT 요소 검사 - 부모가 P인지 확인
            for i, text_elem in enumerate(root.xpath(".//TEXT")):
                parent = text_elem.getparent()
                if parent is None or parent.tag != "P":
                    # 요소의 경로 가져오기
                    elem_path = tree.getpath(text_elem)
                    errors.append(f"TEXT 요소(경로: {elem_path})의 부모가 P가 아닙니다")
            
            # 오류가 있으면 보고
            if errors:
                return {
                    "success": False,
                    "error": "구조 검증 오류: " + "; ".join(errors),
                    "file_path": xml_path,
                    "errors": errors
                }
            
            # 검사 통과
            return {
                "success": True,
                "message": "XML 문법 검사 통과",
                "file_path": xml_path,
                "instruction_for_next_step": INSTRUCTION
            }
            
        except etree.XMLSyntaxError as e:
            return {
                "success": False,
                "error": f"XML 문법 오류 (줄 {e.lineno}, 열 {e.position[1] if e.position else 0}): {e.msg}",
                "file_path": xml_path,
                "line": e.lineno,
                "column": e.position[1] if e.position else 0,
                "instruction_for_next_step": "문서를 처음부터 다시 작성하지 말고, 문서를 넓은 범위에서 천천히 읽어본 다음 수정해."
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"XML 검증 중 오류 발생: {str(e)}",
            "file_path": xml_path
        }
                

@mcp.tool(description="""XML 및 XSL 파일을 HWP로 변환합니다.
    
    Args:
        xml_path: XML 파일 경로
        xsl_path: XSL 파일 경로
        output_path: 출력 HWP 파일 경로
        activation_code: API 활성화 코드
        
    Returns:
        변환된 HWP 파일 경로가 포함된 딕셔너리
    """)
async def convert_xml_and_xsl_to_hwp(xml_path: str, xsl_path:str, output_path: str, activation_code: str = None) -> Dict[str, str]:

    try:
        # XML 파일 확인
        if not os.path.exists(xml_path):
            raise ValueError(f"XML 파일을 찾을 수 없습니다: {xml_path}")
        
        # XSL 파일 확인
        if not os.path.exists(xsl_path):
            raise ValueError(f"XSL 파일을 찾을 수 없습니다: {xsl_path}")
        
        # XML 및 XSL 파일 읽기
        with open(xml_path, 'rb') as f:
            xml_data = f.read()
        
        with open(xsl_path, 'rb') as f:
            xsl_data = f.read()
        
        # Base64로 인코딩
        xml_data_base64 = base64.b64encode(xml_data).decode('utf-8')
        xsl_data_base64 = base64.b64encode(xsl_data).decode('utf-8')
        
        # API 요청 URL
        url = f"{HANGUL_API_BASE}/convert/xml-to-hwp"
        
        # 요청 데이터 준비
        json_data = {
            'activation_code': activation_code,
            'xml_data': xml_data_base64,
            'xsl_data': xsl_data_base64
        }
        
        # API 요청 전송
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=json_data)
            
            if response.status_code != 200:
                raise ValueError(f"API 요청 실패: {response.status_code} - {response.text}")
            
            # 응답 처리
            result = response.json()
            
            # HWP 콘텐츠 가져오기
            hwp_content_base64 = result.get("hwp_base64")
            if not hwp_content_base64:
                raise ValueError("API 응답에 HWP 콘텐츠가 없습니다")
            
            hwp_content = base64.b64decode(hwp_content_base64)
            
            # 출력 디렉토리 확인
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # HWP 파일 저장
            with open(output_path, 'wb') as f:
                f.write(hwp_content)

            INSTRUCTION = """ '기다려주셔서 감사합니다! 변환이 완료되었습니다. 혹시 수정하고 싶으신 부분이 있으신가요?' 라고 유저에게 얘기해.
                만약 유저가 수정하고 싶은 부분을 이야기하면, add, insert, patch를 사용해서 xml을 수정하거나 아예 새로 쓴 뒤, lint_xml을 사용해."""
            
            return {
                "success": True,
                "hwp_path": output_path,
                "instruction_for_next_step": INSTRUCTION
            }
    
    except Exception as e:
        raise ValueError(f"변환 오류: {str(e)}")


if __name__ == "__main__":
    # 서버 초기화 및 실행
    mcp.run(transport='stdio')