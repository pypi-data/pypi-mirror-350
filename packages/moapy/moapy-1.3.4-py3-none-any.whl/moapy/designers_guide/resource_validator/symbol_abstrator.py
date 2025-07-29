import re
from sympy.parsing.latex import parse_latex

# LaTeX 예약어 및 수식 기호 목록
reserved_words = {
    'times', 'div', 'pm', 'mp', 'cdot',
    'exp', 'frac', 'dfrac', 'tfrac',
    'sqrt', 'root', 'sum', 'prod',
    'int', 'oint', 'iint',
    'log', 'ln', 'lim',
    'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'sinh', 'cosh', 'tanh', 'cot', 'sec', 'csc',
    'min', 'max', 'pi',
    'sup', 'inf', 'Abs',
    'leq', 'geq', 'neq', 'approx', 'equiv',
    'cap', 'cup', 'in', 'notin', 'subset', 'supset',
    'to', 'rightarrow', 'leftarrow',
    'partial', 'infty', 'nabla',
    'left', 'right', 'lfloor', 'rfloor', 'land', 'lor',
}

# 전체 심볼 패턴 수정
symbol_pattern = re.compile(
    r'(?:\\?[a-zA-Z]+[0-9]*)'  # 기본 심볼 시작
    r'(?:_[a-zA-Z0-9]|_{(?:[^{}()]|(?:\([^()]*\))|(?:\{[^{}]*\}))+})?'  # 하첨자 부분
    r'(?:\^(?![-0-9.])[a-zA-Z]|\^{(?![-0-9.])[^{}]+})?'  # 윗첨자 부분
    r'(?:\\prime(?:_[a-zA-Z0-9]|_{[^{}]+})?(?:\([^()]*\))?)*'  # prime 패턴
    r'(?:\([^()]*\))?'  # 선택적 괄호 그룹
)

# 함수형 심볼 패턴 수정
function_pattern = re.compile(
    r'(?:\\?[a-zA-Z]+[0-9]*)'  # 기본 심볼 시작
    r'(?:_[a-zA-Z0-9]|_{(?:[^{}]+)})?'  # 하첨자
    r'(?:\^(?![-0-9.])[a-zA-Z]|\^{(?![-0-9.])[^{}]+})?'  # 윗첨자
    r'(?:\\prime)?'  # prime 패턴 추가
    r'\([^()]+\)'  # 괄호와 그 내용
)

def extract_symbols_from_latex(latex_expr):
    """LaTeX 표현식 -> 심볼 추출 함수"""
    try:
        # 1️⃣ SymPy 변환 시도 (기본적인 Symbol 추출)
        sympy_expr = parse_latex(latex_expr)
        extracted_symbols = {str(sym) for sym in sympy_expr.free_symbols}
    except Exception:
        extracted_symbols = set()

    # 2️⃣ LaTeX에서 함수 및 서브스크립트 변수 패턴 추출

    def find_matching_brace(text, start):
        """주어진 위치에서 시작하는 중괄호의 매칭되는 닫는 중괄호 위치를 찾음"""
        if start >= len(text) or text[start] != '{':
            return -1
        
        brace_level = 1
        pos = start + 1
        
        while pos < len(text) and brace_level > 0:
            if text[pos] == '{':
                brace_level += 1
            elif text[pos] == '}':
                brace_level -= 1
            pos += 1
            
        return pos - 1 if brace_level == 0 else -1

    def extract_from_text(text):
        symbols = set()
        original_text = text  # 원본 텍스트 보관
        pos = 0
        
        # Delta 패턴
        delta_pattern = re.compile(
            r'\\Delta{[^{}]*(?:{[^{}]*})*[^{}]*}'  # \Delta{...} 형태 (중첩된 중괄호 허용)
        )
        
        # 괄호+하첨자 패턴 (명시적으로 추가)
        bracket_pattern = re.compile(
            r'\([^()]+\)_{[^{}]+}'  # (...)_{...} 형태
        )
        
        # 연속된 심볼 패턴 (변경 없음)
        consecutive_pattern = re.compile(
            r'[a-zA-Z]+[0-9]*_{[^{}]+}'  # 첫 번째 심볼
            r'(?:(?![\s\\])'  # 공백이나 \가 뒤따르지 않음
            r'[a-zA-Z]+[0-9]*_{[^{}]+})+' # 두 번째 이후 심볼들 (1개 이상 반복)
        )
        
        # 처리된 함수형 심볼 위치 저장
        processed_functions = set()
        
        # 1. 함수형 심볼 먼저 처리
        for match in function_pattern.finditer(text):
            symbol = original_text[match.start():match.end()]
            # 괄호 내용이 공백인지 확인
            bracket_content = symbol[symbol.find('(')+1:symbol.rfind(')')]
            if bracket_content.strip() == '':
                continue
            
            # 예약어로 시작하는지 먼저 확인
            base_symbol = symbol[:symbol.find('(')].strip()
            if base_symbol.startswith('\\'):
                base_symbol = base_symbol[1:]
            
            # 예약어인 경우 괄호 안의 내용만 처리하고 전체 표현식은 건너뛰기
            if base_symbol in reserved_words:
                inner_symbols = extract_from_text(bracket_content)
                symbols.update(inner_symbols)
                # 처리된 부분을 공백으로 대체하여 중복 처리 방지
                text = text[:match.start()] + ' ' * len(symbol) + text[match.end():]
                continue
            
            # 예약어가 아닌 경우 함수형 심볼로 처리
            if not any(symbol[1:].startswith(word) for word in reserved_words):
                symbols.add(symbol)
                processed_functions.add((match.start(), match.end()))
                text = text[:match.start()] + ' ' * len(symbol) + text[match.end():]
        
        # 2. 괄호+하첨자 패턴 처리
        for match in bracket_pattern.finditer(text):
            symbol = original_text[match.start():match.end()]
            symbols.add(symbol)
            text = text[:match.start()] + ' ' * len(symbol) + text[match.end():]
        
        # 3. Delta 패턴 처리
        for match in delta_pattern.finditer(original_text):  # 원본 텍스트에서 검색
            symbol = original_text[match.start():match.end()]
            if not any(symbol[1:].startswith(word) for word in reserved_words):
                symbols.add(symbol)
                text = text[:match.start()] + ' ' * len(symbol) + text[match.end():]
        
        # 4. 연속된 심볼 패턴 처리
        for match in consecutive_pattern.finditer(text):
            symbol = original_text[match.start():match.end()]  # 원본 텍스트에서 심볼 가져오기
            if '\\times' not in symbol:
                symbols.add(symbol)
                text = text[:match.start()] + ' ' * len(symbol) + text[match.end():]
        
        # 4. 기존 심볼 패턴 처리
        matches = list(symbol_pattern.finditer(text))
        matches.sort(key=lambda x: len(x.group(0)), reverse=True)
        
        processed_positions = set()
        
        for match in matches:
            start, end = match.span()
            # 이미 처리된 함수형 심볼 영역은 건너뛰기
            if any(start >= func_start and end <= func_end 
                  for func_start, func_end in processed_functions):
                continue
            
            if any(start >= pos_start and end <= pos_end 
                  for pos_start, pos_end in processed_positions):
                continue
            
            symbol = original_text[match.start():match.end()]
            # 공백만 있는 괄호를 포함하는 심볼 필터링
            if '(' in symbol and ')' in symbol:
                bracket_content = symbol[symbol.find('(')+1:symbol.rfind(')')]
                if bracket_content.strip() == '':
                    continue
            
            if not symbol.startswith('\\') or not any(symbol[1:].startswith(word) for word in reserved_words):
                symbols.add(symbol)
                processed_positions.add((start, end))
        
        # LaTeX 명령어와 중괄호 처리
        while pos < len(text):
            if text[pos:].startswith('\\'):
                cmd_end = pos + 1
                while cmd_end < len(text) and text[cmd_end].isalpha():
                    cmd_end += 1
                cmd = text[pos:cmd_end]
                
                if cmd == '\\prime':
                    pos = cmd_end
                    continue
                
                if cmd_end < len(text):
                    if text[cmd_end] == '{':
                        brace_end = find_matching_brace(text, cmd_end)
                        if brace_end != -1:
                            inner_content = text[cmd_end+1:brace_end]
                            symbols.update(extract_from_text(inner_content))
                            pos = brace_end + 1
                            continue
                    elif text[cmd_end] == '(':
                        # 이미 처리된 함수형 심볼인지 확인
                        is_processed = any(pos >= start and cmd_end <= end 
                                        for start, end in processed_functions)
                        if is_processed:
                            # 함수형 심볼이면 건너뛰기
                            pos = cmd_end
                            continue
                        else:
                            # 일반 괄호 처리 (기존 로직)
                            brace_level = 1
                            brace_end = cmd_end + 1
                            while brace_end < len(text) and brace_level > 0:
                                if text[brace_end] == '(':
                                    brace_level += 1
                                elif text[brace_end] == ')':
                                    brace_level -= 1
                                brace_end += 1
                            
                            if brace_level == 0:
                                inner_content = text[cmd_end+1:brace_end-1]
                                inner_matches = list(symbol_pattern.finditer(inner_content))
                                for match in inner_matches:
                                    symbol = match.group(0)
                                    if not symbol.startswith('\\') or not any(symbol[1:].startswith(word) for word in reserved_words):
                                        symbols.add(symbol)
                                symbols.update(extract_from_text(inner_content))
                                pos = brace_end
                                continue
                
                pos = cmd_end
                continue
            
            pos += 1
        
        return symbols

    # 전체 표현식에서 심볼 추출
    extracted_symbols = extract_from_text(latex_expr)

    # 3️⃣ 불필요한 기호 제거 및 형식 정리
    filtered_symbols = set()
    for sym in extracted_symbols:
        # 수식의 일부가 아닌 실제 연산자 제외
        if not re.match(r'^[+\-=*/^]+$', sym):
            if sym.startswith('\\'):
                # LaTeX 명령어에서 백슬래시 제거
                bare_symbol = sym[1:]
                # 예약어가 아닌 경우에만 추가
                if not any(bare_symbol.startswith(word) for word in reserved_words):
                    filtered_symbols.add(sym)
            else:
                # 알파벳으로 시작하는 심볼인 경우 원형 유지
                filtered_symbols.add(sym)

    return filtered_symbols

def extract_symbols_from_criteria(criteria):
    """조건식에서 심볼을 추출하는 함수
    
    Args:
        criteria (str): LaTeX 형식의 조건식
        
    Returns:
        set: 추출된 심볼들의 집합
    """
    # 비교 연산자 패턴 (LaTeX 및 일반 연산자)
    comparison_pattern = (
        r'(?:\\leq|\\geq|\\neq|\\eq|\\land|\\lor|'  # LaTeX 연산자
        r'<=|>=|==|!=|=|<|>)'  # 일반 연산자
    )
    
    # 순수 영문자 패턴
    pure_english_pattern = re.compile(r'^[a-zA-Z]+$')
    
    # 논리 연산자로 분리
    logical_parts = re.split(r'(\\land|\\lor)', criteria)
    extracted_symbols = set()
    
    for part in logical_parts:
        if part in ['\\land', '\\lor']:  # 논리 연산자는 건너뜀
            continue
            
        # 비교 연산자로 분리
        comparison_parts = re.split(f'({comparison_pattern})', part.strip())
        
        if len(comparison_parts) >= 3:  # 비교 연산자가 있는 경우
            left_expr = comparison_parts[0].strip()
            operator = comparison_parts[1].strip()
            
            # 좌변이 순수 영문자이고 연산자가 등호인 경우
            if pure_english_pattern.match(left_expr) and operator in ['=', '==']:
                extracted_symbols.add(left_expr)
                # 우변은 값으로 처리하므로 심볼 추출하지 않음
                continue
                
            # 그 외의 경우는 기존 방식대로 좌변과 우변 모두 처리
            try:
                left_symbols = extract_symbols_from_latex(left_expr)
                extracted_symbols.update(left_symbols)
            except:
                pass  # 문자열 비교 등으로 파싱 실패할 수 있음
                
            try:
                right_expr = comparison_parts[2].strip()
                right_symbols = extract_symbols_from_latex(right_expr)
                extracted_symbols.update(right_symbols)
            except:
                pass  # 문자열 비교 등으로 파싱 실패할 수 있음
                
        else:  # 단일 표현식인 경우
            try:
                symbols = extract_symbols_from_latex(part)
                extracted_symbols.update(symbols)
            except:
                pass
                
    return extracted_symbols

from moapy.designers_guide.resource import contents, components
from moapy.designers_guide.resource_handler import create_content_component_manager

def abstract_symbols_from_component(component):
    """컴포넌트의 각종 속성에서 예약된 심볼을 추출
    
    Args:
        component (dict): 컴포넌트 정보
        
    Returns:
        set: 추출된 심볼들의 집합
    """

    def abstract_symbols(latex_str):
        if not isinstance(latex_str, str):
            return latex_str, set()
        if '\\sym{' not in latex_str:
            return latex_str, set()
        try:
            extracted_symbols = set()
            result_str = latex_str
            pos = 0
            
            while True:
                # \sym{ 찾기
                pos = latex_str.find('\\sym{', pos)
                if pos == -1:
                    break
                    
                # 중괄호 매칭을 위한 카운터
                brace_level = 1
                start = pos + 5  # \sym{ 다음 위치
                current = start
                
                # 매칭되는 닫는 중괄호 찾기
                while current < len(latex_str) and brace_level > 0:
                    if latex_str[current] == '{':
                        brace_level += 1
                    elif latex_str[current] == '}':
                        brace_level -= 1
                    current += 1
                
                if brace_level == 0:
                    # \sym{...}에서 \sym{}만 제거하고 내부 내용 유지
                    symbol_content = latex_str[start:current-1]
                    result_str = result_str.replace(latex_str[pos:current], f" {symbol_content} ")
                    extracted_symbols.add(symbol_content)
                    pos = current
                else:
                    # 매칭되는 중괄호를 찾지 못한 경우
                    pos = start
            
            return result_str, extracted_symbols
        except:
            return latex_str, set()
    
    server_resource = create_content_component_manager(
        content_list=contents,
        component_list=components
    )

    extracted_symbols = set()
    if "latexSymbol" in component:
        extracted_symbols.add(component["latexSymbol"])
        
    if "latexEquation" in component:
        replacecd_latex_str, symbols = abstract_symbols(component["latexEquation"])
        extracted_symbols.update(symbols)
        if replacecd_latex_str:
            if "originalLatexEquation" not in component:
                component["originalLatexEquation"] = component["latexEquation"]
            component["latexEquation"] = replacecd_latex_str

    if "table" in component or "tableDetail" in component:
        server_table = server_resource.get_table_by_component(component)
        if server_table is not None:
            component["tableDetail"] = server_table
        elif "tableDetail" not in component:
            return extracted_symbols

        originTableData = []
        if "criteria" in component["tableDetail"]:
            for i, criteria_list in enumerate(component["tableDetail"]["criteria"]):
                for j, criteria in enumerate(criteria_list):
                    replacecd_criteria, symbols = abstract_symbols(criteria)
                    component["tableDetail"]["criteria"][i][j] = replacecd_criteria
                    extracted_symbols.update(symbols)
        if "point" in component["tableDetail"]:
            for point in component["tableDetail"]["point"]:
                extracted_symbols.update(point["symbol"])
        if "data" in component["tableDetail"]:
            for i, data_row in enumerate(component["tableDetail"]["data"]):
                if isinstance(component["tableDetail"]["data"][i], list):
                    originTableRowData = []
                    for j, data_col in enumerate(data_row):
                        originTableRowData.append(data_col)
                        replacecd_data, symbols = abstract_symbols(data_col)
                        component["tableDetail"]["data"][i][j] = replacecd_data
                        if len(symbols) > 0 :
                            extracted_symbols.update(symbols)
                    originTableData.append(originTableRowData)
                else:
                    originTableData.append(data_row)
                    replacecd_data, symbols = abstract_symbols(data_row)
                    component["tableDetail"]["data"][i] = replacecd_data
                    if len(symbols) > 0 :
                        extracted_symbols.update(symbols)

        if "originTableData" not in component:
            component["originTableData"] = originTableData
    if len(extracted_symbols) > 0:
        component["abstractedSymbols"] = list(extracted_symbols)