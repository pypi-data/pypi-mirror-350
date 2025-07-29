"""
HWPML 파일 처리를 위한 유틸리티 모듈
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from typing import Dict, List, Optional, Any, Tuple, Union
import os


def parse_xml(xml_path: str) -> ET.ElementTree:
    """XML 파일을 파싱하여 ElementTree 객체로 반환합니다."""
    return ET.parse(xml_path)


def save_xml(tree: ET.ElementTree, xml_path: str) -> None:
    """ElementTree 객체를 XML 파일로 저장합니다."""
    # XML 문자열로 변환하고 정렬
    xml_str = ET.tostring(tree.getroot(), encoding='utf-8')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ", encoding='utf-8')
    
    # 파일에 저장
    with open(xml_path, 'wb') as f:
        f.write(pretty_xml)


def lint_xml(xml_path: str) -> Dict[str, Any]:
    """XML 파일의 문법을 검사합니다."""
    try:
        # XML 파싱 시도
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # 기본 유효성 검사 결과
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # HWPML 특화 유효성 검사
        if root.tag != "HWPML":
            result["warnings"].append("루트 태그가 'HWPML'이 아닙니다.")
        
        # HEAD, BODY 섹션 확인
        head = root.find("HEAD")
        body = root.find("BODY")
        
        if head is None:
            result["errors"].append("필수 'HEAD' 섹션이 없습니다.")
        
        if body is None:
            result["errors"].append("필수 'BODY' 섹션이 없습니다.")
        
        # 기타 검사 항목 추가 가능
        
        return result
    except ET.ParseError as e:
        # XML 파싱 오류 발생
        return {
            "valid": False,
            "errors": [f"XML 파싱 오류: {str(e)}"],
            "warnings": []
        }


def analyze_hwpml_styles(xml_path: str) -> Dict[str, Any]:
    """HWPML 문서의 스타일 정보를 분석합니다."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # 결과 초기화
        styles = {
            "paragraphStyles": [],
            "characterStyles": [],
            "tableStyles": []
        }
        
        # HEAD 섹션에서 스타일 정보 추출
        head = root.find("HEAD")
        if head is not None:
            # 단락 스타일
            para_styles = head.findall(".//PARASHAPE")
            for style in para_styles:
                style_id = style.get("Id", "")
                style_name = style.get("Name", f"스타일 {style_id}")
                styles["paragraphStyles"].append({
                    "id": style_id,
                    "name": style_name,
                    "properties": {prop.tag: prop.text for prop in style}
                })
            
            # 글자 스타일
            char_styles = head.findall(".//CHARSHAPE")
            for style in char_styles:
                style_id = style.get("Id", "")
                style_name = style.get("Name", f"글자 스타일 {style_id}")
                styles["characterStyles"].append({
                    "id": style_id,
                    "name": style_name,
                    "properties": {prop.tag: prop.text for prop in style}
                })
            
            # 표 스타일
            table_styles = head.findall(".//TABLESTYLE")
            for style in table_styles:
                style_id = style.get("Id", "")
                style_name = style.get("Name", f"표 스타일 {style_id}")
                styles["tableStyles"].append({
                    "id": style_id,
                    "name": style_name,
                    "properties": {prop.tag: prop.text for prop in style}
                })
        
        # BODY 섹션에서 사용된 스타일 수집
        body = root.find("BODY")
        if body is not None:
            # 단락 스타일 사용 수집
            used_para_styles = {}
            for p in body.findall(".//P"):
                para_shape = p.get("ParaShape", "")
                style = p.get("Style", "")
                key = f"ParaShape={para_shape}, Style={style}"
                used_para_styles[key] = used_para_styles.get(key, 0) + 1
            
            # 글자 스타일 사용 수집
            used_char_styles = {}
            for text in body.findall(".//TEXT"):
                char_shape = text.get("CharShape", "")
                if char_shape:
                    used_char_styles[char_shape] = used_char_styles.get(char_shape, 0) + 1
            
            # 사용된 스타일 정보 추가
            styles["usedStyles"] = {
                "paragraphStyles": used_para_styles,
                "characterStyles": used_char_styles
            }
        
        # 스타일 사용 통계 계산
        styles["statistics"] = {
            "paragraphStyles": len(styles["paragraphStyles"]),
            "characterStyles": len(styles["characterStyles"]),
            "tableStyles": len(styles["tableStyles"]),
            "usedParagraphStyleCombinations": len(used_para_styles) if 'used_para_styles' in locals() else 0,
            "usedCharacterStyles": len(used_char_styles) if 'used_char_styles' in locals() else 0
        }
        
        styles["summary"] = (
            f"문서는 총 {styles['statistics']['paragraphStyles']}개의 단락 스타일, "
            f"{styles['statistics']['characterStyles']}개의 글자 스타일, "
            f"{styles['statistics']['tableStyles']}개의 표 스타일을 사용합니다. "
            f"실제 사용된 단락 스타일 조합은 {styles['statistics']['usedParagraphStyleCombinations']}가지, "
            f"글자 스타일은 {styles['statistics']['usedCharacterStyles']}가지입니다."
        )
        
        return styles
    except Exception as e:
        return {
            "error": f"스타일 분석 중 오류 발생: {str(e)}"
        }

def get_element_structure(
    xml_path: str,
    xpath: str
) -> Dict[str, Any]:
    """
    HWPML 문서에서 요소의 구조 정보를 반환합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        xpath: 요소를 찾기 위한 XPath 표현식
    
    Returns:
        요소의 구조 정보 (태그 이름, 속성, 텍스트, 자식 요소 등)
    """
    try:
        element, _ = find_element(xml_path, xpath)
        
        if element is None:
            return {"success": False, "error": f"XPath '{xpath}'에 해당하는 요소를 찾을 수 없습니다."}
        
        # 요소의 기본 정보
        result = {
            "success": True,
            "tag": element.tag,
            "attributes": dict(element.attrib),
            "text": element.text.strip() if element.text else "",
            "children": []
        }
        
        # 자식 요소 정보
        for i, child in enumerate(element):
            child_info = {
                "index": i,
                "tag": child.tag,
                "attributes": dict(child.attrib),
                "text": child.text.strip() if child.text else ""
            }
            result["children"].append(child_info)
        
        return result
    
    except Exception as e:
        return {
            "success": False,
            "error": f"요소 구조 분석 중 오류 발생: {str(e)}"
        }


def query_elements(
    xml_path: str,
    xpath: str
) -> Dict[str, Any]:
    """
    HWPML 문서에서 XPath 쿼리에 맞는 모든 요소의 목록을 반환합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        xpath: 요소를 찾기 위한 XPath 표현식
    
    Returns:
        찾은 요소 목록
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # XML 네임스페이스 처리
        namespaces = {}
        if root.tag.startswith("{"):
            ns_uri = root.tag[1:].split("}")[0]
            namespaces['ns'] = ns_uri
            xpath = xpath.replace("/", "/ns:")
            xpath = xpath.replace("[", "[ns:")
            xpath = xpath.replace("@", "@ns:")
        
        # XPath로 요소 찾기
        elements = root.findall(xpath, namespaces)
        
        result = {
            "success": True,
            "count": len(elements),
            "elements": []
        }
        
        # 요소별 기본 정보
        for i, elem in enumerate(elements):
            elem_info = {
                "index": i,
                "tag": elem.tag,
                "attributes": dict(elem.attrib),
                "text": elem.text.strip() if elem.text else ""
            }
            result["elements"].append(elem_info)
        
        return result
    
    except Exception as e:
        return {
            "success": False,
            "error": f"요소 쿼리 중 오류 발생: {str(e)}"
        }


def add_child_element(
    xml_path: str,
    parent_xpath: str,
    tag_name: str,
    attributes: Optional[Dict[str, str]] = None,
    text: Optional[str] = None,
    position: Optional[int] = None
) -> Dict[str, Any]:
    """
    HWPML 문서에서 특정 요소의 자식으로 새 요소를 추가합니다.
    이 함수는 add_element와 동일한 기능을 하지만 이름이 더 직관적입니다.
    
    Args:
        xml_path: HWPML 파일 경로
        parent_xpath: 부모 요소를 찾기 위한 XPath 표현식
        tag_name: 추가할 요소의 태그 이름
        attributes: 설정할 속성 {이름: 값} 딕셔너리 (None이면 속성 없음)
        text: 설정할 텍스트 내용 (None이면 텍스트 없음)
        position: 삽입할 위치 인덱스 (None이면 마지막에 추가)
    
    Returns:
        추가 결과 정보
    """
    return add_element(xml_path, parent_xpath, tag_name, attributes, text, position)


def edit_hwpml_table(
    xml_path: str,
    section_id: str,
    table_position: Union[int, str],
    attributes: Optional[Dict[str, str]] = None,
    cell_data: Optional[Dict[str, Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    HWPML 문서의 표를 편집합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        section_id: 섹션 ID
        table_position: 표 위치 (인덱스) 또는 식별자
        attributes: 표의 속성 수정 (None이면 변경하지 않음)
        cell_data: 셀 데이터 수정 {셀위치: {속성: 값, 'text': 텍스트}} (None이면 변경하지 않음)
                   셀위치는 'row,col' 형식의 문자열(예: '0,0'은 첫 번째 행, 첫 번째 열)
    
    Returns:
        편집 결과 정보
    """
    try:
        # 섹션 찾기
        section_xpath = f"//SECTION[@Id='{section_id}']"
        section, tree = find_element(xml_path, section_xpath)
        
        if section is None:
            return {"success": False, "error": f"ID '{section_id}'의 섹션을 찾을 수 없습니다."}
        
        # 표 찾기
        table = None
        if isinstance(table_position, int):
            tables = section.findall(".//TABLE")
            if 0 <= table_position < len(tables):
                table = tables[table_position]
                table_xpath = f"//SECTION[@Id='{section_id}']//TABLE[{table_position + 1}]"
            else:
                return {"success": False, "error": f"위치 '{table_position}'에서 표를 찾을 수 없습니다."}
        else:
            # 문자열 식별자로 표 찾기
            table_xpath = f"//SECTION[@Id='{section_id}']//TABLE[{table_position}]"
            table, _ = find_element(xml_path, table_xpath)
        
        if table is None:
            return {"success": False, "error": f"위치 '{table_position}'에서 표를 찾을 수 없습니다."}
        
        # 표 속성 변경
        if attributes:
            for name, value in attributes.items():
                table.set(name, value)
        
        # 셀 데이터 변경
        if cell_data:
            for cell_pos, data in cell_data.items():
                try:
                    row, col = map(int, cell_pos.split(','))
                    cell_xpath = f"{table_xpath}/ROW[{row + 1}]/CELL[{col + 1}]"
                    cell, _ = find_element(xml_path, cell_xpath)
                    
                    if cell is None:
                        continue
                    
                    # 셀 속성 변경
                    cell_attrs = {k: v for k, v in data.items() if k != 'text'}
                    if cell_attrs:
                        for name, value in cell_attrs.items():
                            cell.set(name, value)
                    
                    # 셀 내용 변경
                    if 'text' in data and data['text'] is not None:
                        # PARALIST의 P > TEXT > CHAR를 찾거나 생성
                        paralist = cell.find("PARALIST")
                        if paralist is None:
                            paralist = ET.SubElement(cell, "PARALIST")
                        
                        # 첫 번째 P 요소 찾거나 생성
                        p = paralist.find("P")
                        if p is None:
                            p = ET.SubElement(paralist, "P")
                        
                        # TEXT 요소 찾거나 생성
                        text_elem = p.find("TEXT")
                        if text_elem is None:
                            text_elem = ET.SubElement(p, "TEXT")
                        
                        # CHAR 요소 찾거나 생성
                        char_elem = text_elem.find("CHAR")
                        if char_elem is None:
                            char_elem = ET.SubElement(text_elem, "CHAR")
                        
                        # 텍스트 내용 설정
                        char_elem.text = data['text']
                
                except (ValueError, IndexError) as e:
                    return {"success": False, "error": f"셀 '{cell_pos}' 처리 중 오류 발생: {str(e)}"}
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": "표 편집 완료",
            "section_id": section_id,
            "table_xpath": table_xpath
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"표 편집 중 오류 발생: {str(e)}"
        }


def add_hwpml_table(
    xml_path: str,
    section_id: str,
    rows: int,
    cols: int,
    cell_data: Optional[Dict[str, Dict[str, Any]]] = None,
    attributes: Optional[Dict[str, str]] = None,
    position: Optional[int] = None
) -> Dict[str, Any]:
    """
    HWPML 문서에 새 표를 추가합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        section_id: 표를 추가할 섹션 ID
        rows: 표의 행 수
        cols: 표의 열 수
        cell_data: 셀 데이터 {셀위치: {속성: 값, 'text': 텍스트}} (None이면 기본값)
                   셀위치는 'row,col' 형식의 문자열(예: '0,0'은 첫 번째 행, 첫 번째 열)
        attributes: 표 속성 (None이면 기본값)
        position: 삽입할 위치 (None이면 섹션 끝에 추가)
    
    Returns:
        추가 결과 정보
    """
    try:
        # 섹션 찾기
        section_xpath = f"//SECTION[@Id='{section_id}']"
        section, tree = find_element(xml_path, section_xpath)
        
        if section is None:
            return {"success": False, "error": f"ID '{section_id}'의 섹션을 찾을 수 없습니다."}
        
        # 단락 생성 및 추가
        p_result = add_element(xml_path, section_xpath, "P", None, None, position)
        if not p_result["success"]:
            return p_result
        
        # 표를 추가할 단락 찾기
        paragraphs = section.findall("P")
        if position is None or position >= len(paragraphs):
            p_index = len(paragraphs) - 1
        else:
            p_index = position
        
        para_xpath = f"//SECTION[@Id='{section_id}']/P[{p_index + 1}]"
        
        # TEXT 요소 추가
        text_result = add_element(xml_path, para_xpath, "TEXT", None)
        if not text_result["success"]:
            return text_result
        
        text_xpath = f"{para_xpath}/TEXT"
        
        # TABLE 요소 추가
        table_attrs = attributes or {}
        table_result = add_element(xml_path, text_xpath, "TABLE", table_attrs)
        if not table_result["success"]:
            return table_result
        
        table_xpath = f"{text_xpath}/TABLE"
        
        # 행과 셀 추가
        for i in range(rows):
            # ROW 요소 추가
            row_result = add_element(xml_path, table_xpath, "ROW", None)
            if not row_result["success"]:
                return row_result
            
            row_xpath = f"{table_xpath}/ROW[{i + 1}]"
            
            for j in range(cols):
                # CELL 요소 추가
                cell_attrs = None
                if cell_data and f"{i},{j}" in cell_data:
                    cell_attrs = {k: v for k, v in cell_data[f"{i},{j}"].items() if k != 'text'}
                
                cell_result = add_element(xml_path, row_xpath, "CELL", cell_attrs)
                if not cell_result["success"]:
                    return cell_result
                
                cell_xpath = f"{row_xpath}/CELL[{j + 1}]"
                
                # 셀 내용 추가
                paralist_result = add_element(xml_path, cell_xpath, "PARALIST", None)
                if not paralist_result["success"]:
                    return paralist_result
                
                paralist_xpath = f"{cell_xpath}/PARALIST"
                
                # P 요소 추가
                p_result = add_element(xml_path, paralist_xpath, "P", None)
                if not p_result["success"]:
                    return p_result
                
                p_xpath = f"{paralist_xpath}/P"
                
                # 셀 텍스트 추가
                if cell_data and f"{i},{j}" in cell_data and 'text' in cell_data[f"{i},{j}"]:
                    # TEXT 요소 추가
                    text_elem_result = add_element(xml_path, p_xpath, "TEXT", None)
                    if not text_elem_result["success"]:
                        return text_elem_result
                    
                    text_elem_xpath = f"{p_xpath}/TEXT"
                    
                    # CHAR 요소와 텍스트 추가
                    char_result = add_element(xml_path, text_elem_xpath, "CHAR", None, cell_data[f"{i},{j}"]['text'])
                    if not char_result["success"]:
                        return char_result
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": f"새 표 추가 완료",
            "section_id": section_id,
            "table_xpath": table_xpath
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"표 추가 중 오류 발생: {str(e)}"
        }


def edit_hwpml_image(
    xml_path: str, 
    section_id: str, 
    image_position: Union[int, str],
    attributes: Optional[Dict[str, str]] = None,
    bin_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    HWPML 문서의 이미지를 편집합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        section_id: 섹션 ID
        image_position: 이미지 위치 (인덱스) 또는 식별자
        attributes: 이미지의 속성 수정 (None이면 변경하지 않음)
        bin_data: 이미지 바이너리 데이터 정보 (None이면 변경하지 않음)
                 {'BinData': 바이너리ID, 'Format': 'jpg'/'bmp'/'gif'} 또는
                 {'APath': 절대경로, 'RPath': 상대경로}
    
    Returns:
        편집 결과 정보
    """
    try:
        # 섹션 찾기
        section_xpath = f"//SECTION[@Id='{section_id}']"
        section, tree = find_element(xml_path, section_xpath)
        
        if section is None:
            return {"success": False, "error": f"ID '{section_id}'의 섹션을 찾을 수 없습니다."}
        
        # 이미지 찾기
        image = None
        if isinstance(image_position, int):
            images = section.findall(".//PICTURE")
            if 0 <= image_position < len(images):
                image = images[image_position]
                image_xpath = f"//SECTION[@Id='{section_id}']//PICTURE[{image_position + 1}]"
            else:
                return {"success": False, "error": f"위치 '{image_position}'에서 이미지를 찾을 수 없습니다."}
        else:
            # 문자열 식별자로 이미지 찾기
            image_xpath = f"//SECTION[@Id='{section_id}']//PICTURE[{image_position}]"
            image, _ = find_element(xml_path, image_xpath)
        
        if image is None:
            return {"success": False, "error": f"위치 '{image_position}'에서 이미지를 찾을 수 없습니다."}
        
        # 이미지 속성 변경
        if attributes:
            for name, value in attributes.items():
                image.set(name, value)
        
        # 이미지 데이터 변경
        if bin_data:
            binitem = image.find("BINITEM")
            if binitem is None:
                binitem = ET.SubElement(image, "BINITEM")
            
            # 외부 파일 참조 또는 내장 이미지
            if 'APath' in bin_data and 'RPath' in bin_data:
                binitem.set("Type", "Link")
                binitem.set("APath", bin_data['APath'])
                binitem.set("RPath", bin_data['RPath'])
                
                # 내장 데이터 속성 제거
                if 'BinData' in binitem.attrib:
                    del binitem.attrib['BinData']
                if 'Format' in binitem.attrib:
                    del binitem.attrib['Format']
                    
            elif 'BinData' in bin_data and 'Format' in bin_data:
                binitem.set("Type", "Embedding")
                binitem.set("BinData", bin_data['BinData'])
                binitem.set("Format", bin_data['Format'])
                
                # 외부 파일 참조 속성 제거
                if 'APath' in binitem.attrib:
                    del binitem.attrib['APath']
                if 'RPath' in binitem.attrib:
                    del binitem.attrib['RPath']
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": "이미지 편집 완료",
            "section_id": section_id,
            "image_xpath": image_xpath
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"이미지 편집 중 오류 발생: {str(e)}"
        }


def add_hwpml_image(
    xml_path: str, 
    section_id: str, 
    bin_data: Dict[str, Any],
    attributes: Optional[Dict[str, str]] = None,
    position: Optional[int] = None
) -> Dict[str, Any]:
    """
    HWPML 문서에 새 이미지를 추가합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        section_id: 이미지를 추가할 섹션 ID
        bin_data: 이미지 바이너리 데이터 정보
                 {'BinData': 바이너리ID, 'Format': 'jpg'/'bmp'/'gif'} 또는
                 {'APath': 절대경로, 'RPath': 상대경로}
        attributes: 이미지 속성 (None이면 기본값)
        position: 삽입할 위치 (None이면 섹션 끝에 추가)
    
    Returns:
        추가 결과 정보
    """
    try:
        # 섹션 찾기
        section_xpath = f"//SECTION[@Id='{section_id}']"
        section, tree = find_element(xml_path, section_xpath)
        
        if section is None:
            return {"success": False, "error": f"ID '{section_id}'의 섹션을 찾을 수 없습니다."}
        
        # 단락 생성 및 추가
        p_result = add_element(xml_path, section_xpath, "P", None, None, position)
        if not p_result["success"]:
            return p_result
        
        # 이미지를 추가할 단락 찾기
        paragraphs = section.findall("P")
        if position is None or position >= len(paragraphs):
            p_index = len(paragraphs) - 1
        else:
            p_index = position
        
        para_xpath = f"//SECTION[@Id='{section_id}']/P[{p_index + 1}]"
        
        # TEXT 요소 추가
        text_result = add_element(xml_path, para_xpath, "TEXT", None)
        if not text_result["success"]:
            return text_result
        
        text_xpath = f"{para_xpath}/TEXT"
        
        # PICTURE 요소 추가
        pic_attrs = attributes or {}
        pic_result = add_element(xml_path, text_xpath, "PICTURE", pic_attrs)
        if not pic_result["success"]:
            return pic_result
        
        picture_xpath = f"{text_xpath}/PICTURE"
        
        # BINITEM 요소 추가
        binitem_attrs = {}
        
        if 'APath' in bin_data and 'RPath' in bin_data:
            binitem_attrs = {
                "Type": "Link",
                "APath": bin_data['APath'],
                "RPath": bin_data['RPath']
            }
        elif 'BinData' in bin_data and 'Format' in bin_data:
            binitem_attrs = {
                "Type": "Embedding",
                "BinData": bin_data['BinData'],
                "Format": bin_data['Format']
            }
        else:
            return {"success": False, "error": "잘못된 이미지 데이터 형식입니다."}
        
        binitem_result = add_element(xml_path, picture_xpath, "BINITEM", binitem_attrs)
        if not binitem_result["success"]:
            return binitem_result
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": "새 이미지 추가 완료",
            "section_id": section_id,
            "picture_xpath": picture_xpath
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"이미지 추가 중 오류 발생: {str(e)}"
        }


def edit_hwpml_shape(
    xml_path: str,
    section_id: str,
    shape_type: str,
    shape_position: Union[int, str],
    attributes: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    HWPML 문서의 도형을 편집합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        section_id: 섹션 ID
        shape_type: 도형 유형 ('LINE', 'RECTANGLE', 'ELLIPSE', 'ARC', 'POLYGON', 'CURVE' 등)
        shape_position: 도형 위치 (인덱스) 또는 식별자
        attributes: 도형의 속성 수정 (None이면 변경하지 않음)
    
    Returns:
        편집 결과 정보
    """
    try:
        # 섹션 찾기
        section_xpath = f"//SECTION[@Id='{section_id}']"
        section, tree = find_element(xml_path, section_xpath)
        
        if section is None:
            return {"success": False, "error": f"ID '{section_id}'의 섹션을 찾을 수 없습니다."}
        
        # 도형 찾기
        shape = None
        shape_xpath = ""
        
        if isinstance(shape_position, int):
            shapes = section.findall(f".//{shape_type}")
            if 0 <= shape_position < len(shapes):
                shape = shapes[shape_position]
                shape_xpath = f"//SECTION[@Id='{section_id}']//{shape_type}[{shape_position + 1}]"
            else:
                return {"success": False, "error": f"위치 '{shape_position}'에서 {shape_type} 도형을 찾을 수 없습니다."}
        else:
            # 문자열 식별자로 도형 찾기
            shape_xpath = f"//SECTION[@Id='{section_id}']//{shape_type}[{shape_position}]"
            shape, _ = find_element(xml_path, shape_xpath)
        
        if shape is None:
            return {"success": False, "error": f"위치 '{shape_position}'에서 {shape_type} 도형을 찾을 수 없습니다."}
        
        # 도형 속성 변경
        if attributes:
            for name, value in attributes.items():
                shape.set(name, value)
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": f"{shape_type} 도형 편집 완료",
            "section_id": section_id,
            "shape_xpath": shape_xpath
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"도형 편집 중 오류 발생: {str(e)}"
        }


def add_hwpml_shape(
    xml_path: str,
    section_id: str,
    shape_type: str,
    attributes: Optional[Dict[str, str]] = None,
    position: Optional[int] = None
) -> Dict[str, Any]:
    """
    HWPML 문서에 새 도형을 추가합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        section_id: 도형을 추가할 섹션 ID
        shape_type: 도형 유형 ('LINE', 'RECTANGLE', 'ELLIPSE', 'ARC', 'POLYGON', 'CURVE' 등)
        attributes: 도형의 속성 (None이면 기본값)
        position: 삽입할 위치 (None이면 섹션 끝에 추가)
    
    Returns:
        추가 결과 정보
    """
    try:
        # 섹션 찾기
        section_xpath = f"//SECTION[@Id='{section_id}']"
        section, tree = find_element(xml_path, section_xpath)
        
        if section is None:
            return {"success": False, "error": f"ID '{section_id}'의 섹션을 찾을 수 없습니다."}
        
        # 단락 생성 및 추가
        p_result = add_element(xml_path, section_xpath, "P", None, None, position)
        if not p_result["success"]:
            return p_result
        
        # 도형을 추가할 단락 찾기
        paragraphs = section.findall("P")
        if position is None or position >= len(paragraphs):
            p_index = len(paragraphs) - 1
        else:
            p_index = position
        
        para_xpath = f"//SECTION[@Id='{section_id}']/P[{p_index + 1}]"
        
        # TEXT 요소 추가
        text_result = add_element(xml_path, para_xpath, "TEXT", None)
        if not text_result["success"]:
            return text_result
        
        text_xpath = f"{para_xpath}/TEXT"
        
        # 도형 요소 추가
        shape_attrs = attributes or {}
        shape_result = add_element(xml_path, text_xpath, shape_type, shape_attrs)
        if not shape_result["success"]:
            return shape_result
        
        shape_xpath = f"{text_xpath}/{shape_type}"
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": f"새 {shape_type} 도형 추가 완료",
            "section_id": section_id,
            "shape_xpath": shape_xpath
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"도형 추가 중 오류 발생: {str(e)}"
        }


def edit_hwpml_section(
    xml_path: str,
    section_id: str,
    attributes: Optional[Dict[str, str]] = None,
    section_properties: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    HWPML 문서의 구역 속성을 편집합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        section_id: 섹션 ID
        attributes: 섹션의 기본 속성 수정 (None이면 변경하지 않음)
        section_properties: 섹션의 속성 요소 수정 
            {
                'SECDEF': {속성: 값}, 
                'STARTNUMBER': {속성: 값},
                'PAGEDEF': {속성: 값},
                'PAGEMARGIN': {속성: 값}
            } 
            (None이면 변경하지 않음)
    
    Returns:
        편집 결과 정보
    """
    try:
        # 섹션 찾기
        section_xpath = f"//SECTION[@Id='{section_id}']"
        section, tree = find_element(xml_path, section_xpath)
        
        if section is None:
            return {"success": False, "error": f"ID '{section_id}'의 섹션을 찾을 수 없습니다."}
        
        # 섹션 속성 변경
        if attributes:
            for name, value in attributes.items():
                section.set(name, value)
        
        # 섹션 속성 요소 변경
        if section_properties:
            # SECDEF 요소
            if 'SECDEF' in section_properties:
                secdef_xpath = f"{section_xpath}//SECDEF"
                secdef, _ = find_element(xml_path, secdef_xpath)
                
                if secdef is not None:
                    for name, value in section_properties['SECDEF'].items():
                        secdef.set(name, value)
            
            # STARTNUMBER 요소
            if 'STARTNUMBER' in section_properties:
                startnumber_xpath = f"{section_xpath}//SECDEF/STARTNUMBER"
                startnumber, _ = find_element(xml_path, startnumber_xpath)
                
                if startnumber is not None:
                    for name, value in section_properties['STARTNUMBER'].items():
                        startnumber.set(name, value)
            
            # PAGEDEF 요소
            if 'PAGEDEF' in section_properties:
                pagedef_xpath = f"{section_xpath}//SECDEF/PAGEDEF"
                pagedef, _ = find_element(xml_path, pagedef_xpath)
                
                if pagedef is not None:
                    for name, value in section_properties['PAGEDEF'].items():
                        pagedef.set(name, value)
            
            # PAGEMARGIN 요소
            if 'PAGEMARGIN' in section_properties:
                pagemargin_xpath = f"{section_xpath}//SECDEF/PAGEDEF/PAGEMARGIN"
                pagemargin, _ = find_element(xml_path, pagemargin_xpath)
                
                if pagemargin is not None:
                    for name, value in section_properties['PAGEMARGIN'].items():
                        pagemargin.set(name, value)
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": "구역 편집 완료",
            "section_id": section_id
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"구역 편집 중 오류 발생: {str(e)}"
        }


def add_hwpml_section(
    xml_path: str,
    section_properties: Optional[Dict[str, Any]] = None,
    position: Optional[int] = None
) -> Dict[str, Any]:
    """
    HWPML 문서에 새 구역을 추가합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        section_properties: 섹션의 속성
            {
                'SECTION': {속성: 값},
                'SECDEF': {속성: 값}, 
                'STARTNUMBER': {속성: 값},
                'PAGEDEF': {속성: 값},
                'PAGEMARGIN': {속성: 값}
            } 
            (None이면 기본값)
        position: 삽입할 위치 (None이면 맨 끝에 추가)
    
    Returns:
        추가 결과 정보
    """
    try:
        # BODY 요소 찾기
        body_xpath = "//BODY"
        body, tree = find_element(xml_path, body_xpath)
        
        if body is None:
            return {"success": False, "error": "BODY 요소를 찾을 수 없습니다."}
        
        # 섹션 ID 생성 (기존 섹션의 최대 ID + 1)
        section_id = "s1"  # 기본값
        sections = body.findall("SECTION")
        
        if sections:
            max_id = 0
            for section in sections:
                id_str = section.get("Id", "")
                if id_str.startswith("s"):
                    try:
                        id_num = int(id_str[1:])
                        max_id = max(max_id, id_num)
                    except ValueError:
                        pass
            
            section_id = f"s{max_id + 1}"
        
        # 섹션 속성 설정
        section_attrs = {"Id": section_id}
        if section_properties and 'SECTION' in section_properties:
            section_attrs.update(section_properties['SECTION'])
        
        # 섹션 요소 추가
        section_result = add_element(xml_path, body_xpath, "SECTION", section_attrs, None, position)
        if not section_result["success"]:
            return section_result
        
        section_xpath = f"//SECTION[@Id='{section_id}']"
        
        # SECDEF 요소 추가
        secdef_attrs = {}
        if section_properties and 'SECDEF' in section_properties:
            secdef_attrs = section_properties['SECDEF']
        
        secdef_result = add_element(xml_path, section_xpath, "SECDEF", secdef_attrs)
        if not secdef_result["success"]:
            return secdef_result
        
        secdef_xpath = f"{section_xpath}/SECDEF"
        
        # STARTNUMBER 요소 추가
        if section_properties and 'STARTNUMBER' in section_properties:
            startnumber_attrs = section_properties['STARTNUMBER']
            startnumber_result = add_element(xml_path, secdef_xpath, "STARTNUMBER", startnumber_attrs)
            if not startnumber_result["success"]:
                return startnumber_result
        
        # PAGEDEF 요소 추가
        pagedef_attrs = {}
        if section_properties and 'PAGEDEF' in section_properties:
            pagedef_attrs = section_properties['PAGEDEF']
        
        pagedef_result = add_element(xml_path, secdef_xpath, "PAGEDEF", pagedef_attrs)
        if not pagedef_result["success"]:
            return pagedef_result
        
        pagedef_xpath = f"{secdef_xpath}/PAGEDEF"
        
        # PAGEMARGIN 요소 추가
        pagemargin_attrs = {
            "Left": "8504",
            "Right": "8504",
            "Top": "5668",
            "Bottom": "4252",
            "Header": "4252",
            "Footer": "4252",
            "Gutter": "0"
        }
        
        if section_properties and 'PAGEMARGIN' in section_properties:
            pagemargin_attrs.update(section_properties['PAGEMARGIN'])
        
        pagemargin_result = add_element(xml_path, pagedef_xpath, "PAGEMARGIN", pagemargin_attrs)
        if not pagemargin_result["success"]:
            return pagemargin_result
        
        # 첫 번째 빈 단락 추가
        p_result = add_element(xml_path, section_xpath, "P", {"ParaShape": "0", "Style": "0"})
        if not p_result["success"]:
            return p_result
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": f"새 구역 추가 완료",
            "section_id": section_id
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"구역 추가 중 오류 발생: {str(e)}"
        }


def get_hwpml_document_structure(xml_path: str) -> Dict[str, Any]:
    """
    HWPML 문서의 구조를 분석합니다.
    
    Args:
        xml_path: HWPML 파일 경로
    
    Returns:
        문서 구조 정보
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        structure = {
            "documentInfo": {},
            "sections": [],
            "totalParagraphs": 0,
            "totalTables": 0,
            "totalImages": 0
        }
        
        # 문서 정보 추출
        head = root.find("HEAD")
        if head is not None:
            doc_info = head.find("DOCSUMMARY")
            if doc_info is not None:
                for info in doc_info:
                    structure["documentInfo"][info.tag] = info.text
        
        # 섹션 정보 추출
        body = root.find("BODY")
        if body is not None:
            for i, section in enumerate(body.findall("SECTION")):
                section_info = {
                    "id": section.get("Id", ""),
                    "index": i,
                    "paragraphs": [],
                    "tables": []
                }
                
                # 단락 정보
                for j, para in enumerate(section.findall("P")):
                    para_shape = para.get("ParaShape", "")
                    style = para.get("Style", "")
                    
                    # 텍스트 요소 찾기
                    text_elems = para.findall("TEXT")
                    char_shapes = [text.get("CharShape", "") for text in text_elems]
                    
                    # 텍스트 내용 추출 (첫 100자만)
                    text_content = ""
                    for text in text_elems:
                        for char in text.findall("CHAR"):
                            if char.text:
                                text_content += char.text
                    
                    if len(text_content) > 100:
                        text_content = text_content[:97] + "..."
                    
                    section_info["paragraphs"].append({
                        "index": j,
                        "paraShape": para_shape,
                        "style": style,
                        "charShapes": char_shapes,
                        "preview": text_content
                    })
                    
                    structure["totalParagraphs"] += 1
                
                # 테이블 정보
                for k, table in enumerate(section.findall(".//TABLE")):
                    table_id = table.get("Id", "")
                    section_info["tables"].append({
                        "index": k,
                        "id": table_id,
                        "rows": len(table.findall(".//ROW")),
                        "cols": len(table.findall(".//CELL")) // max(1, len(table.findall(".//ROW")))
                    })
                    
                    structure["totalTables"] += 1
                
                structure["sections"].append(section_info)
                
                # 이미지 카운트
                structure["totalImages"] += len(section.findall(".//PICTURE"))
        
        # 추가 스타일 사용 정보
        style_analysis = analyze_hwpml_styles(xml_path)
        if "error" not in style_analysis:
            structure["styleAnalysis"] = {
                "summary": style_analysis.get("summary", ""),
                "statistics": style_analysis.get("statistics", {})
            }
        
        return structure
    
    except Exception as e:
        return {
            "error": f"문서 구조 분석 중 오류 발생: {str(e)}"
        }


def find_element(
    xml_path: str, 
    xpath: str,
) -> Tuple[Optional[ET.Element], ET.ElementTree]:
    """
    XPath를 사용하여 HWPML 문서에서 특정 요소를 찾습니다.
    
    Args:
        xml_path: HWPML 파일 경로
        xpath: 요소를 찾기 위한 XPath 표현식
    
    Returns:
        (찾은 요소, ElementTree) 튜플 또는 (None, ElementTree)
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # XML 네임스페이스 처리
        namespaces = {}
        if root.tag.startswith("{"):
            ns_uri = root.tag[1:].split("}")[0]
            namespaces['ns'] = ns_uri
            xpath = xpath.replace("/", "/ns:")
            xpath = xpath.replace("[", "[ns:")
            xpath = xpath.replace("@", "@ns:")
        
        # XPath로 요소 찾기
        elements = root.findall(xpath, namespaces)
        
        if elements:
            return elements[0], tree
        return None, tree
    
    except Exception as e:
        print(f"요소 찾기 중 오류 발생: {str(e)}")
        return None, None


def find_element_by_text(
    xml_path: str,
    text: str,
    tag: Optional[str] = None,
    exact_match: bool = False
) -> List[Tuple[ET.Element, str]]:
    """
    텍스트 내용을 기준으로 HWPML 문서에서 요소를 찾습니다.
    
    Args:
        xml_path: HWPML 파일 경로
        text: 찾을 텍스트
        tag: 특정 태그만 검색 (None이면 모든 태그)
        exact_match: 정확한 텍스트 일치 여부 (False면 부분 일치도 검색)
    
    Returns:
        (찾은 요소, XPath) 튜플 목록
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # 결과 목록
        results = []
        
        # 요소 탐색
        for elem in root.iter(tag):
            # 직접 텍스트 내용이 있는지 확인
            if elem.text is not None:
                if exact_match and elem.text.strip() == text:
                    xpath = get_xpath(root, elem)
                    results.append((elem, xpath))
                elif not exact_match and text in elem.text:
                    xpath = get_xpath(root, elem)
                    results.append((elem, xpath))
            
            # CHAR 요소의 경우 특별히 처리 (HWPML 문서의 실제 텍스트 내용)
            if elem.tag == "CHAR" and elem.text is not None:
                if exact_match and elem.text.strip() == text:
                    xpath = get_xpath(root, elem)
                    results.append((elem, xpath))
                elif not exact_match and text in elem.text:
                    xpath = get_xpath(root, elem)
                    results.append((elem, xpath))
        
        return results
    
    except Exception as e:
        print(f"텍스트로 요소 찾기 중 오류 발생: {str(e)}")
        return []


def get_xpath(root: ET.Element, element: ET.Element) -> str:
    """
    주어진 요소의 XPath를 생성합니다.
    
    Args:
        root: XML 루트 요소
        element: XPath를 생성할 요소
    
    Returns:
        요소의 XPath 문자열
    """
    # 요소의 경로 추적
    path = []
    current = element
    
    # 부모 맵 생성
    parent_map = {c: p for p in root.iter() for c in p}
    
    # 루트에 도달할 때까지 경로 추적
    while current != root:
        parent = parent_map.get(current)
        if parent is None:
            break
        
        # 현재 요소의 태그 이름과 동일한 형제 요소 중 인덱스 찾기
        siblings = [c for c in parent if c.tag == current.tag]
        idx = siblings.index(current) + 1
        
        # 인덱스가 1보다 크면 태그 이름에 인덱스 추가
        if idx > 1 or len(siblings) > 1:
            path.append(f"{current.tag}[{idx}]")
        else:
            path.append(current.tag)
        
        current = parent
    
    # 경로 뒤집기 (루트에서 요소로)
    path.reverse()
    
    # XPath 문자열 반환
    return "//" + "/".join(path)


def edit_element(
    xml_path: str,
    xpath: str,
    attributes: Optional[Dict[str, str]] = None,
    text: Optional[str] = None,
) -> Dict[str, Any]:
    """
    HWPML 문서의 특정 요소를 편집합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        xpath: 편집할 요소를 찾기 위한 XPath 표현식
        attributes: 설정할 속성 {이름: 값} 딕셔너리 (None이면 속성 변경 없음)
        text: 설정할 텍스트 내용 (None이면 텍스트 변경 없음)
    
    Returns:
        편집 결과 정보
    """
    try:
        element, tree = find_element(xml_path, xpath)
        
        if element is None:
            return {"success": False, "error": f"XPath '{xpath}'에 해당하는 요소를 찾을 수 없습니다."}
        
        # 요소의 기본 정보
        result = {
            "success": True,
            "tag": element.tag,
            "attributes": dict(element.attrib),
            "text": element.text.strip() if element.text else "",
            "children": []
        }
        
        # 자식 요소 정보
        for i, child in enumerate(element):
            child_info = {
                "index": i,
                "tag": child.tag,
                "attributes": dict(child.attrib),
                "text": child.text.strip() if child.text else ""
            }
            result["children"].append(child_info)
        
        # 요소 속성 변경
        if attributes:
            for name, value in attributes.items():
                element.set(name, value)
        
        # 요소 텍스트 변경
        if text is not None:
            element.text = text
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return result
    
    except Exception as e:
        return {
            "success": False,
            "error": f"요소 편집 중 오류 발생: {str(e)}"
        }

def add_element(
    xml_path: str,
    parent_xpath: str,
    tag_name: str,
    attributes: Optional[Dict[str, str]] = None,
    text: Optional[str] = None,
    position: Optional[int] = None
) -> Dict[str, Any]:
    """
    HWPML 문서에 새 요소를 추가합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        parent_xpath: 부모 요소를 찾기 위한 XPath 표현식
        tag_name: 추가할 요소의 태그 이름
        attributes: 설정할 속성 {이름: 값} 딕셔너리 (None이면 속성 없음)
        text: 설정할 텍스트 내용 (None이면 텍스트 없음)
        position: 삽입할 위치 인덱스 (None이면 마지막에 추가)
    
    Returns:
        추가 결과 정보
    """
    try:
        parent, tree = find_element(xml_path, parent_xpath)
        
        if parent is None:
            return {"success": False, "error": f"XPath '{parent_xpath}'에 해당하는 부모 요소를 찾을 수 없습니다."}
        
        # 새 요소 생성
        new_element = ET.Element(tag_name)
        
        # 속성 설정
        if attributes:
            for name, value in attributes.items():
                new_element.set(name, value)
        
        # 텍스트 설정
        if text is not None:
            new_element.text = text
        
        # 위치에 삽입 또는 마지막에 추가
        if position is not None:
            children = list(parent)
            if position >= len(children):
                parent.append(new_element)
            else:
                parent.insert(position, new_element)
        else:
            parent.append(new_element)
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": f"요소 추가 완료",
            "parent_xpath": parent_xpath,
            "tag": tag_name
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"요소 추가 중 오류 발생: {str(e)}"
        }

def delete_element(
    xml_path: str,
    xpath: str
) -> Dict[str, Any]:
    """
    HWPML 문서에서 요소를 삭제합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        xpath: 삭제할 요소를 찾기 위한 XPath 표현식
    
    Returns:
        삭제 결과 정보
    """
    try:
        element, tree = find_element(xml_path, xpath)
        
        if element is None:
            return {"success": False, "error": f"XPath '{xpath}'에 해당하는 요소를 찾을 수 없습니다."}
        
        # 부모 요소 찾기
        root = tree.getroot()
        parent_map = {c: p for p in root.iter() for c in p}
        
        if element in parent_map:
            parent = parent_map[element]
            parent.remove(element)
            
            # 변경사항 저장
            save_xml(tree, xml_path)
            
            return {
                "success": True,
                "message": f"요소 삭제 완료",
                "xpath": xpath
            }
        else:
            return {"success": False, "error": f"XPath '{xpath}'에 해당하는 요소의 부모를 찾을 수 없습니다."}
    
    except Exception as e:
        return {
            "success": False,
            "error": f"요소 삭제 중 오류 발생: {str(e)}"
        }

def create_empty_hwpml(output_path: str, xsl_path: str = None) -> Dict[str, Any]:
    """
    빈 HWPML 문서를 생성합니다.
    
    Args:
        output_path: 생성할 HWPML 파일 경로
        xsl_path: 참조할 XSL 파일 경로 (None이면 스타일시트 참조를 추가하지 않음)
    
    Returns:
        생성 결과 정보
    """
    try:
        # HWPML 문서 기본 구조 생성
        root = ET.Element("HWPML")
        root.set("Version", "2.91")
        root.set("SubVersion", "10.0.0.0")
        root.set("Style", "export")
        
        # XML 스타일시트 참조 설정
        if xsl_path:
            # 파일명만 추출
            xsl_filename = os.path.basename(xsl_path)
            pi = ET.ProcessingInstruction("xml-stylesheet", f'type="text/xsl" href="{xsl_filename}"')
            
        # HEAD 섹션 추가
        head = ET.SubElement(root, "HEAD")
        
        # BODY 섹션 추가
        body = ET.SubElement(root, "BODY")
        
        # 첫 번째 섹션 추가
        section = ET.SubElement(body, "SECTION")
        section.set("Id", "0")
        

        
        # HWPML을 문자열로 변환
        tree = ET.ElementTree(root)
        
        # XML 스타일시트 참조 추가 (존재하는 경우)
        if xsl_path:
            # XML 선언과 스타일시트 참조를 문자열로 설정
            xml_declaration = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>'
            stylesheet_ref = f'<?xml-stylesheet type="text/xsl" href="{xsl_filename}"?>'
            
            # ElementTree를 문자열로 변환
            xml_str = ET.tostring(root, encoding='utf-8', xml_declaration=False)
            
            # XML 선언과 스타일시트 참조를 추가
            full_xml = xml_declaration + stylesheet_ref + xml_str.decode('utf-8')
            
            # 파일에 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_xml)
        else:
            # 스타일시트 참조 없이 저장
            save_xml(tree, output_path)
        
        return {
            "success": True,
            "message": "빈 HWPML 문서 생성 완료",
            "path": output_path
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"빈 HWPML 문서 생성 중 오류 발생: {str(e)}"
        }


def copy_styles_from_template(source_xml_path: str, target_xml_path: str) -> Dict[str, Any]:
    """
    템플릿 HWPML 파일에서 스타일 정보를 추출하여 타겟 HWPML 파일에 복사합니다.
    
    Args:
        source_xml_path: 스타일을 복사할 소스 HWPML 파일 경로
        target_xml_path: 스타일을 적용할 타겟 HWPML 파일 경로
    
    Returns:
        복사 결과 정보
    """
    try:
        # 소스 파일 파싱
        source_tree = ET.parse(source_xml_path)
        source_root = source_tree.getroot()
        source_head = source_root.find("HEAD")
        
        if source_head is None:
            return {
                "success": False,
                "error": "소스 파일에서 HEAD 섹션을 찾을 수 없습니다."
            }
        
        # 타겟 파일 파싱
        target_tree = ET.parse(target_xml_path)
        target_root = target_tree.getroot()
        target_head = target_root.find("HEAD")
        
        if target_head is None:
            # HEAD 섹션이 없으면 생성
            target_head = ET.SubElement(target_root, "HEAD")
            # BODY 섹션을 찾아서 HEAD 이전에 배치
            body = target_root.find("BODY")
            if body is not None:
                target_root.remove(body)
                target_root.append(body)
        
        # 스타일 요소 복사 (기존 요소 삭제 후 새로 추가)
        style_elements = ["CHARSHAPES", "PARASHAPES", "STYLES", "BORDERFILLS", "NUMBERINGS"]
        
        for style_elem in style_elements:
            # 타겟에서 기존 요소 삭제
            existing = target_head.find(style_elem)
            if existing is not None:
                target_head.remove(existing)
            
            # 소스에서 요소 복사
            source_elem = source_head.find(style_elem)
            if source_elem is not None:
                # 요소 복제
                target_elem = ET.fromstring(ET.tostring(source_elem, encoding='utf-8'))
                target_head.append(target_elem)
        
        # 변경사항 저장
        save_xml(target_tree, target_xml_path)
        
        return {
            "success": True,
            "message": "스타일 복사 완료",
            "source": source_xml_path,
            "target": target_xml_path
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"스타일 복사 중 오류 발생: {str(e)}"
        }


def add_hwpml_paragraph(
    xml_path: str,
    section_id: str,
    text: str,
    para_shape: str = "0",
    style: str = "0",
    char_shape: str = "0",
    position: Optional[int] = None
) -> Dict[str, Any]:
    """
    HWPML 문서에 새 단락을 추가합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        section_id: 단락을 추가할 섹션 ID
        text: 단락에 포함할 텍스트 내용
        para_shape: 단락 모양 ID (기본값: "0")
        style: 단락 스타일 ID (기본값: "0")
        char_shape: 글자 모양 ID (기본값: "0")
        position: 삽입할 위치 (None이면 섹션 끝에 추가)
    
    Returns:
        추가 결과 정보
    """
    try:
        # 섹션 찾기
        section_xpath = f"//SECTION[@Id='{section_id}']"
        section, tree = find_element(xml_path, section_xpath)
        
        if section is None:
            return {"success": False, "error": f"ID '{section_id}'의 섹션을 찾을 수 없습니다."}
        
        # 단락 속성 설정
        p_attrs = {
            "ParaShape": para_shape,
            "Style": style
        }
        
        # 단락 요소 추가
        p_result = add_element(xml_path, section_xpath, "P", p_attrs, None, position)
        if not p_result["success"]:
            return p_result
        
        # 단락을 추가할 위치 찾기
        paragraphs = section.findall("P")
        if position is None or position >= len(paragraphs):
            p_index = len(paragraphs) - 1
        else:
            p_index = position
        
        para_xpath = f"//SECTION[@Id='{section_id}']/P[{p_index + 1}]"
        
        # TEXT 요소 속성 설정
        text_attrs = {
            "CharShape": char_shape
        }
        
        # TEXT 요소 추가
        text_result = add_element(xml_path, para_xpath, "TEXT", text_attrs)
        if not text_result["success"]:
            return text_result
        
        text_xpath = f"{para_xpath}/TEXT"
        
        # CHAR 요소 추가
        char_result = add_element(xml_path, text_xpath, "CHAR", None, text)
        if not char_result["success"]:
            return char_result
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": "새 단락 추가 완료",
            "section_id": section_id,
            "paragraph_index": p_index
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"단락 추가 중 오류 발생: {str(e)}"
        }

def edit_hwpml_paragraph(
    xml_path: str,
    paragraph_xpath: str,
    text: Optional[str] = None,
    para_shape: Optional[str] = None,
    style: Optional[str] = None,
    char_shape: Optional[str] = None
) -> Dict[str, Any]:
    """
    HWPML 문서의 단락을 편집합니다.
    
    Args:
        xml_path: HWPML 파일 경로
        paragraph_xpath: 편집할 단락의 XPath
        text: 변경할 텍스트 내용 (None이면 유지)
        para_shape: 변경할 단락 모양 ID (None이면 유지)
        style: 변경할 단락 스타일 ID (None이면 유지)
        char_shape: 변경할 글자 모양 ID (None이면 유지)
    
    Returns:
        편집 결과 정보
    """
    try:
        # 단락 찾기
        p, tree = find_element(xml_path, paragraph_xpath)
        
        if p is None:
            return {"success": False, "error": f"XPath '{paragraph_xpath}'에 해당하는 단락을 찾을 수 없습니다."}
        
        # 단락 속성 변경
        if para_shape is not None:
            p.set("ParaShape", para_shape)
        
        if style is not None:
            p.set("Style", style)
        
        # TEXT 요소 찾기 또는 생성
        text_elem = p.find("TEXT")
        if text_elem is None and (char_shape is not None or text is not None):
            # TEXT 요소가 없으면 생성
            text_elem = ET.SubElement(p, "TEXT")
        
        # TEXT 요소 속성 변경
        if char_shape is not None and text_elem is not None:
            text_elem.set("CharShape", char_shape)
        
        # 텍스트 내용 변경
        if text is not None and text_elem is not None:
            # CHAR 요소 찾기 또는 생성
            char_elem = text_elem.find("CHAR")
            if char_elem is None:
                # CHAR 요소가 없으면 생성
                char_elem = ET.SubElement(text_elem, "CHAR")
            
            # 텍스트 설정
            char_elem.text = text
        
        # 변경사항 저장
        save_xml(tree, xml_path)
        
        return {
            "success": True,
            "message": "단락 편집 완료",
            "paragraph_xpath": paragraph_xpath
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"단락 편집 중 오류 발생: {str(e)}"
        } 