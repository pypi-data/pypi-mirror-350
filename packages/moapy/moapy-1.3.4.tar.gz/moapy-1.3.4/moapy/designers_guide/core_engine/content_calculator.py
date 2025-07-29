import re
import sympy
import numpy as np
import warnings as warning_system
import random
from sympy import Eq, Symbol
from sympy.parsing.latex import parse_latex
from scipy.interpolate import interp1d, RegularGridInterpolator

import moapy.designers_guide.resource.defined_format.report_form as report_form
from moapy.designers_guide.resource_handler.content_component import Content, Component
from moapy.designers_guide.resource_handler import create_content_component_manager
from moapy.designers_guide.resource import contents, components
from moapy.designers_guide.resource_validator.error_format import ErrorWarning, ErrorType, ErrorCode, append_error_warning
from moapy.designers_guide.utils import run_only_once
from moapy.designers_guide.resource_handler.simple_mapping_manager import generate_mapping_data, append_mapping_data_only_symbol, get_symbol_mappings, get_simple_symbol_to_component_id, __NOT_DEFINED_ID__
from moapy.designers_guide.resource_validator.symbol_abstrator import abstract_symbols_from_component

__all__ = ["pre_process_before_calc", "get_function_tree_by_components", "get_report_bundles", "make_report_json", "set_isolated_test_mode", "reset_isolated_test_mode"]

########################################################
# Control Resource
resource_on_server = create_content_component_manager(
    content_list=contents,
    component_list=components,
)
resource_on_user = None
temp_merged_resource = None # TODO : resource&mapping data 관리 구조 구축 후 삭제 필요

########################################################
# isolated test mode
isolated_test_mode = False

def set_isolated_test_mode(mode: bool):
    global isolated_test_mode
    isolated_test_mode = mode

def reset_isolated_test_mode():
    global isolated_test_mode
    isolated_test_mode = False

# Func Desc. Generate mapping data and Replace LaTeX symbols to simple symbols in equations. Once time process.
@run_only_once()
def pre_process_before_calc():
    generate_mapping_data()
    for comp in replace_symbols_in_equations(resource_on_server.component_list):
        resource_on_server.update_component(comp['id'], comp)

def pre_process_before_calc_for_user(
    content: Content,
    components: list[Component]
):
    global resource_on_user
    resource_on_user = create_content_component_manager(
        content_list=[content],
        component_list=components
        )

    generate_mapping_data(resource_on_user.component_list)
    for comp in replace_symbols_in_equations(resource_on_user.component_list):
        resource_on_user.update_component(comp['id'], comp)

def set_temp_merged_resource(
    user_content: Content | None = None,
    user_components: list[Component] | None = None
    ):
    merged_content = contents.copy()
    if user_content is not None:
        merged_content.extend([user_content])
    merged_component = components.copy()
    if user_components is not None:
        merged_component.extend(user_components)
    
    global temp_merged_resource
    temp_merged_resource = create_content_component_manager(
        content_list=merged_content,
        component_list=merged_component
    )
    return temp_merged_resource.copy()

def reset_resource_on_user():
    global resource_on_user
    resource_on_user = None

def reset_temp_merged_resource():
    global temp_merged_resource
    temp_merged_resource = None

def current_resource():
    global temp_merged_resource
    global resource_on_user
    global resource_on_server
    if temp_merged_resource is not None:
        return temp_merged_resource
    if resource_on_user is not None:
        return resource_on_user
    return resource_on_server
########################################################

def temp_precess_exception(report):
    if report.id == "G18_COMP_9" and report.result_value == 0:
        report.result_value = r'no need'
        report.formula = []
        report.unit = ""
    if report.id == "G18_COMP_10" and report.result_value == 0:
        report.result_value = r'no need'
        report.formula = []
        report.unit = ""
    if report.id == "G33_COMP_3" and isinstance(report.result_value, sympy.Symbol) and report.result_value.name == "NA":
        report.result_value = r'NA'
        report.formula = []
        report.unit = ""
    return report

def replace_min_max(sympy_expr):
    """sympy_expr에서 min과 max를 SymPy의 Min과 Max로 변환합니다."""
    if sympy_expr.has(sympy.Function('min')):
        sympy_expr = sympy_expr.subs({
            sympy.Function('min'): sympy.Min,
        })
    if sympy_expr.has(sympy.Function('max')):
        sympy_expr = sympy_expr.subs({
            sympy.Function('max'): sympy.Max
        })

    return sympy_expr

# @cache_result # TODO : 중간 계산식 문제로 임시 비활성화
def custom_parse_latex(latex_str: str) -> str:
    def preprocess_log(latex_str):
        processed = []
        i = 0
        while i < len(latex_str):
            if latex_str[i:i + 4] == r"\log":  # \log 발견
                processed.append(r"\log")  # 기본적으로 추가
                i += 4

                if i < len(latex_str) and latex_str[i] == "_": # 밑이 있다면 그대로 추가                    
                    processed.append("_")
                    i += 1
                    if i < len(latex_str) and latex_str[i] == "{":  # 밑의 시작
                        processed.append("{")
                        i += 1
                        brace_level = 1
                        while i < len(latex_str) and brace_level > 0:
                            processed.append(latex_str[i])
                            if latex_str[i] == "{":
                                brace_level += 1
                            elif latex_str[i] == "}":
                                brace_level -= 1
                            i += 1
                else: # 밑이 없는 경우 log_{10}으로 치환
                    processed.append(r"_{10}")
            else:
                processed.append(latex_str[i])
                i += 1

        return "".join(processed)
    
    def preprocess_frac(latex_str):
        result = ""
        i = 0
        while i < len(latex_str):
            if latex_str[i:i+5] == r"\frac":  # \frac 발견
                result += r"\frac"
                i += 5
                
                # 첫 번째 인자 확인
                if i < len(latex_str) and latex_str[i] == '{':  # 이미 중괄호가 있는 경우
                    result += latex_str[i]  # '{' 추가
                    i += 1
                    brace_level = 1
                    while i < len(latex_str) and brace_level > 0:
                        result += latex_str[i]
                        if latex_str[i] == '{':
                            brace_level += 1
                        elif latex_str[i] == '}':
                            brace_level -= 1
                        i += 1
                else:  # 중괄호가 없는 경우
                    result += '{'
                    # 공백을 건너뛰고 실제 문자열을 만날 때까지 진행
                    while i < len(latex_str) and latex_str[i].isspace():
                        i += 1
                    # 문자열의 끝까지 또는 다음 공백을 만날 때까지 진행
                    while i < len(latex_str) and not latex_str[i].isspace():
                        result += latex_str[i]
                        i += 1
                    result += '}'
                
                # 두 번째 인자 확인
                while i < len(latex_str) and latex_str[i].isspace():
                    i += 1  # 공백 건너뛰기
                    
                if i < len(latex_str) and latex_str[i] == '{':  # 이미 중괄호가 있는 경우
                    result += latex_str[i]  # '{' 추가
                    i += 1
                    brace_level = 1
                    while i < len(latex_str) and brace_level > 0:
                        result += latex_str[i]
                        if latex_str[i] == '{':
                            brace_level += 1
                        elif latex_str[i] == '}':
                            brace_level -= 1
                        i += 1
                else:  # 중괄호가 없는 경우
                    result += '{'
                    # 공백을 건너뛰고 실제 문자열을 만날 때까지 진행
                    while i < len(latex_str) and latex_str[i].isspace():
                        i += 1
                    # 문자열의 끝까지 또는 다음 공백을 만날 때까지 진행
                    while i < len(latex_str) and not latex_str[i].isspace():
                        result += latex_str[i]
                        i += 1
                    result += '}'
            else:
                result += latex_str[i]
                i += 1
            
        return result
    
    preprocessed_latex = preprocess_log(latex_str) # parse_latex 이전에 log(x) 형식 전처리
    preprocessed_latex = preprocess_frac(preprocessed_latex) # parse_latex 이전에 \frac(x) 형식 전처리
    preprocessed_latex = convert_format_latex_to_sympy(preprocessed_latex) # parse_latex 이전에 |x| 형식 전처리

    sympy_expr: sympy.Equality = parse_latex(preprocessed_latex)
    
    sympy_expr = replace_min_max(sympy_expr)

    return sympy_expr

# Func Desc. Insert spaces around operators in LaTeX
def insert_spaces(latex_expr):
    curr_resource = current_resource()
    operators = curr_resource.binary_operators + curr_resource.relation_operators + curr_resource.function_operators

    for op in operators:
        latex_expr = re.sub(f'({op})([^ ])', r'\1 \2', latex_expr)
        latex_expr = re.sub(f'([^ ])({op})', r'\1 \2', latex_expr)
    return re.sub(r'\s+', ' ', latex_expr).strip()

def is_latex_equation(expr):
    curr_resource = current_resource()
    operators = curr_resource.binary_operators + curr_resource.relation_operators + curr_resource.function_operators

    for op in operators:
        if re.search(op, expr):
            return True
    return False

def replace_latex_to_simple(
        latex_str: str,
        required_comps: list[str] |None = None,
        required_symbols: list[str] | None = None
        ):
    def re_sym_to_simple(str, sym, simple_sym):
        return re.sub(rf'(?<!\w){re.escape(sym)}(?!\w)', simple_sym, str)
    
    def find_main_equality(latex_str):
        stack = []
        sum_depth = 0
        for i, char in enumerate(latex_str):
            if char == '{':
                stack.append(i)
            elif char == '}':
                if stack:
                    stack.pop()
            elif char == '\\' and latex_str[i:i+4] == '\\sum':
                sum_depth += 1
            elif char == '=' and not stack and sum_depth == 0:
                if latex_str[i-1:i+1] in ['<=', '<=']:
                    continue
                return i
        return -1
    
    def replace_process(expr, is_lhs=False):
        curr_resource = current_resource()
        symbol_mappings = get_symbol_mappings()
        result = expr
        if required_symbols and isolated_test_mode:
            append_mapping_data_only_symbol(required_symbols)
            symbol_mappings = get_symbol_mappings()
            for sym in required_symbols:
                result = re_sym_to_simple(result, sym, symbol_mappings[(sym, __NOT_DEFINED_ID__)])
        elif required_comps:
            req_comp_list = [comp for comp in (curr_resource.find_component_by_id(req_id) for req_id in required_comps) if comp is not None]
            req_comp_list = sorted(req_comp_list, key=lambda x: len(x['latexSymbol']), reverse=True)
            for req_comp in req_comp_list:
                sym = req_comp['latexSymbol']
                if sym in expr and (is_lhs and sym == expr.strip()):
                    result = re_sym_to_simple(result, sym, symbol_mappings[(sym, req_comp['id'])])
                elif not is_lhs:
                    result = re_sym_to_simple(result, sym, symbol_mappings[(sym, req_comp['id'])])
        
        if not required_comps or is_lhs:
            for (sym, id), simple_symbol in symbol_mappings.items():
                result = re_sym_to_simple(result, sym, simple_symbol)
        
        return result
    
    latex_str = latex_str.replace(r'\cdot', r' \times ')
    
    splited_str = re.split(r'(?<!<)(?<!>)=(?!=)', latex_str)
    if len(splited_str) > 1:
        eq_pos = find_main_equality(latex_str)
        if eq_pos != -1:
            # 등호를 기준으로 좌변과 우변 분리
            lhs = latex_str[:eq_pos].strip()
            rhs = latex_str[eq_pos + 1:].strip()
            
            # 좌변과 우변 각각 처리
            processed_lhs = replace_process(lhs, is_lhs=True)
            processed_rhs = replace_process(rhs, is_lhs=False)
            
            return f"{processed_lhs} = {processed_rhs}"
        else:
            return replace_process(latex_str)
    else:
        return replace_process(latex_str)

# Func Desc. Replace LaTeX symbols with simple symbols in Component list
def replace_symbols_in_equations(comp_list: list):
    for comp in comp_list:
        abstract_symbols_from_component(comp) # TODO : 여기에서 \sym{}을 변환하는 과정에 기존 symbol이 깨지는 현상 발생. 추출할 때 양 옆 띄어쓰기 하는게 원인.
    for comp in (m for m in comp_list if "latexEquation" in m):
        required_comps = comp['required'] if 'required' in comp else None
        preprocessed_eq = comp['latexEquation']
        if isolated_test_mode and "abstractedSymbols" in comp:
            preprocessed_eq = replace_latex_to_simple(latex_str=preprocessed_eq, required_symbols=comp['abstractedSymbols'])
        else:
            preprocessed_eq = replace_latex_to_simple(latex_str=preprocessed_eq, required_comps=required_comps)
        comp['sympy_expr'] = custom_parse_latex(preprocessed_eq)
    return comp_list

class TreeNode:
    def __init__(self, symbol, operation=None, children=None):
        self.symbol = symbol  # 노드의 심볼 (변수 또는 함수명)
        self.operation = operation  # 노드의 연산자 또는 함수 정의
        self.children = children if children is not None else []  # 자식 노드 리스트

    def add_child(self, child_node):
        self.children.append(child_node)

def replace_log_to_ln(equation):
    stack = []
    replaced_equation = []

    i = 0
    while i < len(equation):
        if equation[i:i+4] == "log(":
            stack.append(len(replaced_equation))
            replaced_equation.append("ln(")
            i += 4
        elif len(stack) > 0 and equation[i:i+4] == ", E)":
            replaced_equation.append(")")
            stack.pop()
            i += 4
        else:
            replaced_equation.append(equation[i])
            i += 1

    return ''.join(replaced_equation)

def get_child_components_from_required(comp):
    if 'required' in comp:
        return comp['required']
    return []

def get_calc_tree(target_comp_id):
    curr_resource = current_resource()
    target_comp = curr_resource.find_component_by_id(target_comp_id)
    if target_comp is None:
        return None
    
    target_symbol = target_comp['latexSymbol']
    tree_node = TreeNode(target_symbol, target_comp)
    
    child_comps = set(get_child_components_from_required(target_comp))
    for child in child_comps:
        child_comp = get_calc_tree(child)
        if child_comp is not None:
            tree_node.add_child(child_comp)
        else:
            tree_node.add_child(TreeNode(target_symbol, target_comp))
        
    return tree_node

def get_function_tree_by_components(target_comps_id):
    params_tree = []
    for target_comp_id in target_comps_id:
        content_tree = get_calc_tree(target_comp_id)
        if content_tree is not None:
            params_tree.append(content_tree)
    return params_tree

def is_calcuated_symbol(stack_reports, id):
    if id is None:
        warning_system.warn(f"ID is None.", RuntimeWarning)
        return False
    return any(report.id == id for report in stack_reports)

def unique_merge_report(stack_reports, sub_reports): 
    symbols_stack = {report.symbol for report in stack_reports}
    symbols_sub = {report.symbol for report in sub_reports}
    duplicates = symbols_stack & symbols_sub
    unique_sub_reports = [report for report in sub_reports if report.symbol not in duplicates]
    return unique_sub_reports

def sympy_post_replace_symbols(expr):
    if r'pi' in str(expr): # pi
        pi = sympy.symbols(r'pi')
        expr = expr.subs(pi, sympy.pi.evalf())
    return expr

def sympy_post_processing(expr): # 단순 계산이 안되는 연산식 처리
    expr_rhs_str = str(expr.rhs)
    res_value = sympy.parse_expr(expr_rhs_str)
    expr = sympy.Eq(expr.lhs, res_value)
    # rhs_value = 0
    # min_match = re.search(r'min\(([\d\.]+),\s*([\d\.]+)\)', expr_rhs_str)
    # max_match = re.search(r'max\(([\d\.]+),\s*([\d\.]+)\)', expr_rhs_str)
    # if min_match:
    #     rhs_value = sympy.Min(*map(float, min_match.groups()))
    # elif max_match:
    #     rhs_value = sympy.Max(*map(float, max_match.groups()))
    # else:
    #     return None
    # expr_rhs_str = expr_rhs_str.replace(min_match.group(), str(rhs_value))
    # expr_rhs_simbol = sympy.parse_expr(expr_rhs_str)
    # expr = sympy.Eq(expr.lhs, expr_rhs_simbol)
    # recursion_expr = sympy_post_processing(expr)
    # if recursion_expr is not None:
    #     expr = recursion_expr
    return expr

def replace_frac_to_division(latex_expr):
    def process_frac(expr):
        result = ""
        i = 0
        while i < len(expr):
            if expr[i:i+5] == r"\frac":  # Detect \frac
                start = i + 5
                numerator, end = extract_braces(expr, start)
                denominator, end = extract_braces(expr, end)
                # Recursively process numerator and denominator
                numerator = process_frac(numerator)
                denominator = process_frac(denominator)
                result += f"({numerator})/({denominator})"
                i = end
            else:
                result += expr[i]
                i += 1
        return result

    def extract_braces(expr, start):
        if expr[start] != '{':
            raise ValueError("Expected '{' at position {}".format(start))
        stack = []
        i = start
        content = ""
        while i < len(expr):
            if expr[i] == '{':
                stack.append(i)
                if len(stack) > 1:
                    content += expr[i]
            elif expr[i] == '}':
                stack.pop()
                if not stack:
                    return content, i + 1
                content += expr[i]
            else:
                if stack:
                    content += expr[i]
            i += 1
        raise ValueError("Unmatched '{' in expression")
    
    return process_frac(latex_expr)

def find_exclusive_result_symbols(expr) -> set[str]:
    exclusive_symbols = set()
    
    def extract_sigma_lower_bound_symbol(latex_expr):
        sigma_pattern = r'\\sum_\{([^{}]*(?:\{[^{}]*\})*[^{}]*)\}'
        match = re.search(sigma_pattern, latex_expr)
        if match:
            eq_1 = match.group(1)
            if '=' in eq_1:
                return eq_1.split('=')[0].strip()
        return None
    
    sigma_index_symbol = extract_sigma_lower_bound_symbol(expr)
    if sigma_index_symbol is not None:
        exclusive_symbols.add(sigma_index_symbol)

    return exclusive_symbols

def validate_criteria(criteria_str, symbol_result, required_comps, used_symbols):
    def replace_latex_for_criteria(expr):
        # Replace logical operators
        # expr = expr.replace(r'\land', 'and').replace(r'\lor', 'or')
        expr = expr.replace(r'\leq', '<=').replace(r'\geq', '>=')
        expr = expr.replace(r'\lt', '<').replace(r'\gt', '>')
        # Replace fractions (\frac{a}{b} -> (a)/(b))
        expr = replace_frac_to_division(expr)
        return expr

    def evaluate_mathematical_expression(expr):
        try:
            parse_expr = custom_parse_latex(expr)
            return bool(parse_expr)
            # return bool(parse_expr.evalf())
        except Exception:
            try:
                return bool(sympy.sympify(expr))
            except Exception:
                return None  # Fall back to other methods if math evaluation fails
        
    def evaluate_string_comparison(expr):
        # Handles expressions like 'A = B'
        parts = [part.strip() for part in re.split(r'==|=', expr)]
        if len(parts) == 2:
            return parts[0] == parts[1]
        return False
    
    def parse_and_evaluate_criteria(expr):
        """Parse logical expressions involving 'and', 'or', and evaluate each condition."""
        conditions = re.split(r'\\land|\\lor', expr)
        operators = re.findall(r'\\land|\\lor', expr)

        results = []
        for condition in conditions:
            is_comparison_str = False
            for sym, disp_sym, res, ref_type in symbol_result:
                if sym in condition:
                    condition = condition.replace(sym, str(res))
                    used_symbols.add(disp_sym)
                    if ref_type == "string":
                        is_comparison_str = True

            condition = condition.strip()
            if is_comparison_str:
                try:
                    results.append(evaluate_string_comparison(condition))
                except Exception as e_evaluate_string_comparison:
                    warning_system.warn(f"Failed to compare in string: {criteria_str} - {e_evaluate_string_comparison}", RuntimeWarning)
                    results.append(False)
            else:
                try:
                    if_found = evaluate_mathematical_expression(condition)
                    if if_found is not None:
                        results.append(if_found)
                        continue
                    warning_system.warn(f"Failed to evaluate criteria: {criteria_str}", RuntimeWarning)
                except Exception as e_evaluate_mathematical_expression:
                    warning_system.warn(f"Failed to evaluate criteria: {criteria_str} - {e_parse_and_evaluate_criteria}", RuntimeWarning)
                    return False

        # Combine results based on logical operators
        result = results[0]
        for i, operator in enumerate(operators):
            if operator == r"\land":
                result = result and results[i + 1]
            elif operator == r"\or":
                result = result or results[i + 1]
        return result
    
    # Step 1: Replace symbols with their values
    if "abstractedSymbols" in criteria_str:
        criteria = replace_latex_to_simple(latex_str=criteria_str, required_symbols=criteria_str['abstractedSymbols'])
    else:
        criteria = replace_latex_to_simple(latex_str=criteria_str, required_comps=required_comps)
    criteria = convert_format_latex_to_sympy(criteria)

    # Step 2: Convert LaTeX operators to Python equivalents
    criteria_expr = replace_latex_for_criteria(criteria)

    # Step 3: Evaluate the criteria
    try:
        is_found = parse_and_evaluate_criteria(criteria_expr)
        return is_found
    except Exception as e_parse_and_evaluate_criteria:
        warning_system.warn(f"Failed to evaluate criteria: {criteria_str} - {e_parse_and_evaluate_criteria}", RuntimeWarning)
        return False

def format_log(base_expr, inner_expr, is_natural):
    log_func = r'\ln' if is_natural else r'\log' # 자연로그 여부에 따라 함수명을 결정
    if inner_expr.is_Mul and inner_expr.args[0] == -1: # 음수 표현이 포함된 경우 '-' 기호만 추가
        return f'{log_func}\\left(-{convert_latex_formula(inner_expr.args[1])}\\right)'
    if not is_natural: # 밑이 있는 로그인 경우
        return f'{log_func}_{{{convert_latex_formula(base_expr)}}}\\left({convert_latex_formula(inner_expr)}\\right)'
    return f'{log_func}\\left({convert_latex_formula(inner_expr)}\\right)' # 기본 로그 출력

def convert_latex_formula(expr):
    def is_polynomial(expr):
        return '+' in str(expr) or ('-' in str(expr) and str(expr)[0] != '-')

    symbol_mul = r' \times '
    if expr.is_Atom: # basic atom
        return sympy.latex(expr, mul_symbol=symbol_mul)
    
    elif expr.func == sympy.Sum: # Summation(sigma)
        if len(expr.args) == 2:
            inner_expr, (sym, start, end) = expr.args[0], expr.args[1]
            return r'\sum_{' + f'{sym}' + '=' + f'{start}' + r'}^{' + f'{end}' + r'}' + convert_latex_formula(inner_expr)
        else:
            warning_system.warn(f"invalid summation : {expr}", RuntimeWarning)
            return sympy.latex(expr, mul_symbol=symbol_mul)

    elif expr.func == sympy.log: # Logs(로그)
        if len(expr.args) == 2: # with a base: log(a, E), log(a, b) 
            base_expr, inner_expr = expr.args[1], expr.args[0]
            return format_log(base_expr, inner_expr, is_natural=(base_expr == sympy.E))
        else: # without a base: log(a)
            return format_log(sympy.Integer(10), expr.args[0], is_natural=False)
        
    elif expr.func == sympy.Mul: # Multiple(곱셈)
        numerators = []
        denominators = []
        for arg in expr.args:
            if arg == -1: # `-1` 단독 : 기호만 추가
                numerators.append('-')
            elif arg.func == sympy.Pow and arg.args[1] == -1: # 음수 지수
                denominators.append(convert_latex_formula(arg.args[0]))
            elif arg.func == sympy.log: # log
                numerators.append(convert_latex_formula(arg))
            elif arg.is_negative:  # 음수 : 분자로 취급하되, 기호를 -로 처리
                numerators.append(f"-{convert_latex_formula(-arg)}")
            else:
                numerators.append(convert_latex_formula(arg))

        if numerators[0] == "-":  # '-' 기호가 단독으로 나온 경우 공백 제거
            expr_numerator = "-" + symbol_mul.join(num for num in numerators[1:])
        else:
            expr_numerator = symbol_mul.join(numerators)
            
        if denominators: # 분자와 분모를 구분하여 출력
            return r'\frac{' + expr_numerator + r'}{' + symbol_mul.join(denominators) + r'}'
        else:
            return expr_numerator
        
    elif expr.func == sympy.Pow: # Power(거듭제곱): b^a
        base, exp = expr.args
        if exp == -1: # x^{-1}
            return r'\frac{1}{' + convert_latex_formula(base) + r'}'
        elif isinstance(exp, sympy.Rational) and 0 < exp < 1 and exp.p == 1: # x^{1/n}
            denominator = exp.q
            if denominator == 2:  # x^(1/2): 제곱근
                return r'\sqrt{' + convert_latex_formula(base) + r'}'
            else:  # x^(1/n): 일반적인 n제곱근
                return r'\sqrt[' + str(denominator) + r']{' + convert_latex_formula(base) + r'}'
        else: # x^{y}
            if is_polynomial(base):
                return r'\left(' + convert_latex_formula(base) + r'\right)^{' + convert_latex_formula(exp) + r'}'
            else:
                return convert_latex_formula(base) + "^{" + convert_latex_formula(exp) + r'}'
        
    elif expr.func == sympy.exp:  # Exponential: e^x
        exponent = expr.args[0]
        return r'e^{' + convert_latex_formula(exponent) + r'}'
    
    elif expr.is_Add: # Addition(덧셈)
        numerators = []
        for arg in expr.args:
            if arg.is_negative:  # 음수인 기호 -로 별도 처리
                numerators.append(f"-{convert_latex_formula(-arg)}")
            else:
                numerators.append(convert_latex_formula(arg))
        return f'({numerators[0]} ' + ' '.join(f"+ {num}" if num[0] != '-' else num for num in numerators[1:]) + ')'
    
    elif expr.func == sympy.Max: # Max
        return r'\max\left(' + ', '.join(convert_latex_formula(arg) for arg in expr.args) + r'\right)'
    elif expr.func == sympy.Min: # Min
        return r'\min\left(' + ', '.join(convert_latex_formula(arg) for arg in expr.args) + r'\right)'

    else: # Etc.
        return sympy.latex(expr, mul_symbol=symbol_mul)

def convert_format_latex_to_sympy(latex_str: str):
    LATEX_TO_SYMPY_RULES = {
        # \Abs{x}, \Abs(x) -> Abs(x)
        r'\\\\?Abs\(([^()]*(?:\([^()]*\))*[^()]*)\)': r'Abs(\1)', 
        r'\\\\?Abs\{([^{}]*(?:\{[^{}]*\})*[^{}]*)\}': r'Abs(\1)',
        # \times -> *
        r'\\\\?times': r'*',
    }
    converted_str = latex_str
    for latex_pattern, sympy_pattern in LATEX_TO_SYMPY_RULES.items():
        converted_str = re.sub(latex_pattern, sympy_pattern, converted_str)
    return converted_str

def convert_format_sympy_to_latex(sympy_str: str):
    SYMPY_TO_LATEX_RULES = {
        # Abs(x) -> \Abs{x}
        r'Abs\(([^()]*(?:\([^()]*\))*[^()]*)\)': r'\\Abs{\1}',
    }
    converted_str = sympy_str
    for sympy_pattern, latex_pattern in SYMPY_TO_LATEX_RULES.items():
        converted_str = re.sub(sympy_pattern, latex_pattern, converted_str)
    return converted_str
    
def post_tune_latex(latex_str):
    latex_str = latex_str.replace(r'\operatorname', '').replace(r'\frac', r'\dfrac')
    latex_str = latex_str.replace('--', '+').replace('+-', '-').replace('-+', '-').replace('- -', '+').replace('- +', '-').replace('+ -', '-')

    def remove_outer_parentheses(str):
        if str.startswith('(') and str.endswith(')'):
            # 내부에 괄호 쌍을 제대로 닫았는지 확인
            stack = 0
            for i, char in enumerate(str[1:-1], start=1):
                if char == '(':
                    stack += 1
                elif char == ')':
                    stack -= 1
                    if stack < 0: # 스택이 0보다 작아지면, 최외곽이 아닌 괄호가 닫힌 것
                        return str
            if stack == 0: # 스택이 0이면 최외곽의 ()를 제거
                return str[1:-1]
        return str
    latex_str = remove_outer_parentheses(latex_str)
    latex_str = convert_format_sympy_to_latex(latex_str)
    
    return latex_str

def get_report(node, comp_to_value):
    errors, warnings = {}, {}
    curr_resource = current_resource()
    symbol_mappings = get_symbol_mappings()
    simple_id_mappings = get_simple_symbol_to_component_id()
    params_report = []
    sym_res_list = []
    for chlid in node.children:
        if isolated_test_mode:
            break # NOTE : 개별 테스트 시 탐색 X
        if is_calcuated_symbol(params_report, chlid.operation.get('id', None)):
            continue
        sub_reports, sub_errors, sub_warnings = get_report(chlid, comp_to_value)
        if sub_reports is None:
            continue
        for sub_report in sub_reports:
            sym_res_list.append(tuple([symbol_mappings[(f"{sub_report.symbol}", f"{sub_report.id}")], sub_report.symbol, sub_report.result_value, curr_resource.get_ref_type(sub_report.id)]))
            if len(sub_errors) > 0:
                append_error_warning(errors, sub_report.id, sub_errors)
            if len(sub_warnings) > 0:
                append_error_warning(warnings, sub_report.id, sub_warnings)
        unique_sub_reports = unique_merge_report(params_report, sub_reports)
        params_report.extend(unique_sub_reports)

    if isolated_test_mode:
        for sym in node.operation.get('abstractedSymbols', []):
            if sym == node.operation['latexSymbol']:
                continue
            random_value = random.randrange(1, 20)
            simple_sym = symbol_mappings.get((sym, __NOT_DEFINED_ID__), None)
            if simple_sym is None:
                continue
            sym_res_list.append(tuple([simple_sym, sym, random_value, 'number']))
    else:
        for comp_val in comp_to_value:
            if isolated_test_mode:
                break # NOTE : 개별 테스트 시 탐색 X
            matched = next(((sym, id) for (sym, id) in symbol_mappings if id == comp_val.get('component')), None)
            if matched is None:
                continue # TODO : Wraning 처리
            simple_symbol = matched[0]
            if next((item for item in sym_res_list if item[0] == simple_symbol), None):
                continue
            required = node.operation.get('required', [])
            if required == []:
                continue
            req_id = next((req_param for req_param in required if req_param == comp_val['component']), None)
            if req_id:
                sym = curr_resource.find_component_by_id(req_id)['latexSymbol']
                sym_res_list.append(tuple([symbol_mappings[(sym, req_id)], sym, comp_val['value'], curr_resource.get_ref_type(req_id)]))
            
    sym_res_list = sorted(sym_res_list, key=lambda item: -len(item[1]))
    symbol_result = list(dict.fromkeys(sym_res_list))

    current_comp_id = node.operation['id']
    current_comp = curr_resource.find_component_by_id(current_comp_id)
    
    current_report = report_form.ReportForm()
    current_report.id = current_comp_id
    current_report.is_used = False
    current_report.code_name = current_comp.get('codeName', '')
    current_report.reference = current_comp.get('reference', [''])
    current_report.title = current_comp.get('title', '')
    current_report.description = current_comp.get('description', '')
    current_report.figure_path = f"{curr_resource.get_figure_server_url()}/{current_comp.get('figureFile', None)}" if (current_comp.get('figureFile', None) != None) else None
    current_report.descript_table = curr_resource.convert_enum_table_to_detail(current_comp)
    current_report.comp_type = curr_resource.get_component_type(current_comp)
    current_report.symbol = current_comp.get('latexSymbol', '')
    current_report.formula = []
    current_report.unit = current_comp.get('unit', '')
    current_report.notation = current_comp.get('notation', '')
    current_report.decimal = current_comp.get('decimal', 0)
    current_report.use_std = current_comp.get('useStd', False)
    current_report.ref_std = current_comp.get('refStd', '')
    current_report.limits = current_comp.get('limits', {})
    current_report.result_table = []
    if 'default' in current_comp:
        current_report.result_value = current_comp['default']

    required_comps = current_comp['required'] if 'required' in current_comp else None

    input_value = next((item for item in comp_to_value if item['component'] == current_comp_id), None)
    if input_value:
            current_report.is_user_input = True
            current_report.result_value = input_value['value']
    
    if 'latexEquation' in current_comp and 'sympy_expr' not in current_comp:
        required_comps = current_comp['required'] if 'required' in current_comp else None
        preprocessed_eq = current_comp['latexEquation']
        if "abstractedSymbols" in current_comp:
            preprocessed_eq = replace_latex_to_simple(latex_str=preprocessed_eq, required_symbols=current_comp['abstractedSymbols'])
        else:
            preprocessed_eq = replace_latex_to_simple(latex_str=preprocessed_eq, required_comps=required_comps)
        current_comp['sympy_expr'] = custom_parse_latex(preprocessed_eq)

    used_symbols = set()
    table_type = curr_resource.get_table_type(current_comp)
    if table_type != "None":
        if table_type == 'dropdown': # 'table' : 'dropdown'
            table_enum = curr_resource.get_table_enum_by_component(current_comp)
            if table_enum is None:
                new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_COMPONENT_ESSENTIAL)
                new_error.occurred_property = "tableDetail"
                append_error_warning(errors, current_comp_id, new_error)
                warning_system.warn(f"table_enum is not in table_data : {current_comp_id} / {current_report.symbol}", RuntimeWarning)
            elif isolated_test_mode:
                enum_data = table_enum[0]
            else:
                for enum_data in table_enum if table_enum else []:
                    if input_value is None:
                        new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_INPUT_VALUES)
                        append_error_warning(errors, current_comp_id, new_error)
                        warning_system.warn(f"Unable to determine table enumeration due to missing input value: {current_comp_id} / {current_report.symbol}", RuntimeWarning)
                        break
                    elif enum_data == input_value['value']:
                        current_report.result_value = enum_data
        if table_type == 'text' or table_type == 'formula'or table_type == 'matrix': # 'table' : 'text' or 'formula' or 'matrix'
            ref_table = curr_resource.get_table_by_component(current_comp)
            if 'criteria' not in ref_table or 'data' not in ref_table:
                new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_COMPONENT_ESSENTIAL)
                new_error.occurred_property = "criteria"
                append_error_warning(errors, current_comp_id, new_error)
                warning_system.warn(f"criteria or data is not in table_data : {expr} / {current_comp_id} / {current_report.symbol}", RuntimeWarning)
            
            criteria_table = ref_table.get('criteria', [])
            num_criteria = len(criteria_table)
            if num_criteria == 2 and (criteria_table[1] == [] or criteria_table[1][0] == ""):
                num_criteria = 1

            matched_cr = []
            for group_cr in range(num_criteria):
                for idx_cr, cr_expr in enumerate(criteria_table[group_cr]):
                    if validate_criteria(cr_expr, symbol_result, required_comps, used_symbols):
                        matched_cr.append(idx_cr)
                        break

            if matched_cr != [] and len(matched_cr) == num_criteria:
                if num_criteria == 1:
                    if isinstance(ref_table['data'][0], list):
                        table_data = ref_table['data'][matched_cr[0]][0]
                        node.operation['originalLatexEquation'] = node.operation['originTableData'][[matched_cr[0]][0]]
                    else:
                        table_data = ref_table['data'][matched_cr[0]]
                        node.operation['originalLatexEquation'] = node.operation['originTableData'][matched_cr[0]]
                elif num_criteria == 2:
                    table_data = ref_table['data'][matched_cr[0]][matched_cr[1]]
                    node.operation['originalLatexEquation'] = node.operation['originTableData'][matched_cr[0]][matched_cr[1]]

                if table_type == 'text':
                    current_report.result_value = table_data
                elif table_type == 'formula' or table_type == 'matrix':
                    if "abstractedSymbols" in table_data:
                        node.operation['sympy_expr'] = custom_parse_latex(replace_latex_to_simple(latex_str=table_data, required_symbols=table_data['abstractedSymbols']))
                    else:
                        node.operation['sympy_expr'] = custom_parse_latex(replace_latex_to_simple(latex_str=table_data, required_comps=required_comps))
            else:
                if not isolated_test_mode:
                    new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.NOT_MATCHED_CONDITION)
                    new_error.occurred_property = "criteria"
                    append_error_warning(errors, current_comp_id, new_error)
                    warning_system.warn(f"criteria is not matched in table_data : {current_comp_id} / {current_report.symbol}", RuntimeWarning)

        if table_type == 'result': # 'table' : 'result'
            table_data = curr_resource.get_table_data_by_component(current_comp)
            for row, row_data in enumerate(table_data) if table_data else []:
                if row == 0:
                    current_report.result_table.append(row_data)
                else:
                    row_list = []
                    for col_data in row_data:
                        res_value = ""
                        process_latex_equation = False
                        if is_latex_equation(str(col_data)):
                            process_latex_equation = True
                        elif 'abstractedSymbols' in current_comp:
                            for abs_symbol in current_comp['abstractedSymbols']:
                                if abs_symbol == col_data.strip():
                                    process_latex_equation = True
                                    break
                        
                        if process_latex_equation:
                            calc_expr = insert_spaces(col_data)
                            expr_parts = re.split(r'\\text\{([^}]*)\}', str(calc_expr))
                            for i, part in enumerate(expr_parts):
                                if i % 2 == 0:
                                    if "abstractedSymbols" in part:
                                        part_expr = custom_parse_latex(replace_latex_to_simple(latex_str=part, required_symbols=part['abstractedSymbols']))
                                    else:
                                        part_expr = custom_parse_latex(replace_latex_to_simple(latex_str=part, required_comps=required_comps))
                                    for sym, disp_sym, res, ref_type in symbol_result:
                                        x = sympy.symbols(f"{sym}")
                                        if part_expr.has(x):
                                            part_expr = part_expr.subs(x, res)
                                            used_symbols.add(disp_sym)
                                    res_value += f"{str(part_expr.evalf())} "
                                else:
                                    res_value += f"{part} "
                        else:
                            res_value = str(col_data)
                        row_list.append(res_value)
                    current_report.result_table.append(row_list)
        if table_type == 'interpolation' or table_type == 'bi-interpolation':
            table_itrpl = curr_resource.get_table_by_component(current_comp)
            point_data = table_itrpl.get('point', {})
            dimension = len(point_data)
            if dimension == 1:
                x_symbol = point_data[0].get('symbol')
                x_value = next((item[2] for item in symbol_result if item[1] == x_symbol), None)
                if x_value is not None and isinstance(x_value, str):
                    try:
                        x_value = float(x_value)
                    except ValueError:
                        warning_system.warn(f"x_value를 숫자로 변환할 수 없습니다: {x_value}", RuntimeWarning)
                        x_value = None
                if x_value != None:
                    x_point = np.array(point_data[0].get('value'))
                    z_value = np.array(table_itrpl['data'])
                    if x_value < x_point.min(): x_value = x_point.min()
                    elif x_value > x_point.max(): x_value = x_point.max()
                    f_linear = interp1d(x_point, z_value, kind='linear')
                    current_report.result_value = f_linear(float(x_value)).item()
                used_symbols.add(x_symbol)
            elif dimension == 2:
                x_symbol = point_data[0].get('symbol')
                y_symbol = point_data[1].get('symbol')

                x_value = next((item[2] for item in symbol_result if item[1] == x_symbol), None)
                y_value = next((item[2] for item in symbol_result if item[1] == y_symbol), None)
                if x_value is not None and isinstance(x_value, str):
                    try:
                        x_value = float(x_value)
                    except ValueError:
                        warning_system.warn(f"x_value를 숫자로 변환할 수 없습니다: {x_value}", RuntimeWarning)
                        x_value = None
                if y_value is not None and isinstance(y_value, str):
                    try:
                        y_value = float(y_value)
                    except ValueError:
                        warning_system.warn(f"y_value를 숫자로 변환할 수 없습니다: {y_value}", RuntimeWarning)
                        y_value = None
                if x_value != None and y_value != None:
                    x_point = np.array(point_data[0].get('value'))
                    y_point = np.array(point_data[1].get('value'))
                    z_value = np.array(table_itrpl['data'])
                    if x_value < x_point.min(): x_value = x_point.min()
                    elif x_value > x_point.max(): x_value = x_point.max()
                    if y_value < y_point.min(): y_value = y_point.min()
                    elif y_value > y_point.max(): y_value = y_point.max()
                    xy_point = (float(x_value), float(y_value))

                    interp_func = RegularGridInterpolator((x_point, y_point), z_value)
                    current_report.result_value = interp_func(xy_point).item()
                used_symbols.add(x_symbol)
                used_symbols.add(y_symbol)
            else:
                new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.LATEX_UNCALCULABLE)
                new_error.occurred_property = 'point'
                append_error_warning(errors, current_comp_id, new_error)
                warning_system.warn(f"point data is not in table of interpolation : {current_comp_id} / {current_comp.symbol}", RuntimeWarning)
    
    if 'sympy_expr' in current_comp: # fomula
        expr = node.operation['sympy_expr']
        if not isinstance(expr, Eq):  # 이미 Eq 형태면 그대로 반환
            expr = Eq(Symbol(node.operation['latexSymbol']), expr)  # 아니면 Eq 변환

        org_formula = convert_latex_formula(expr.rhs)
        mid_formula = org_formula

        exclusive_symbols = find_exclusive_result_symbols(org_formula)
        for sym, disp_sym, res, ref_type in symbol_result:
            x = sympy.symbols(f"{sym}")
            if expr.has(x):
                expr = expr.subs(x, res)
                used_symbols.add(disp_sym)
            if sym in org_formula:
                simple_id = simple_id_mappings[sym]
                if sym not in exclusive_symbols:
                    if simple_id == __NOT_DEFINED_ID__:
                        current_report.result_variable[str(f"{disp_sym}")] = {
                            "value": str(res),
                            "unit": '',
                            "notation": '',
                            "decimal": '',}
                        used_symbols.add(disp_sym)
                    else:
                        sym_comp = curr_resource.find_component_by_id(simple_id)
                        if sym_comp:
                            current_report.result_variable[str(f"{disp_sym}")] = {
                                "value": str(res),
                                "unit": sym_comp.get('unit', ''),
                                "notation": sym_comp.get('notation', 'standard'),
                                "decimal": sym_comp.get('decimal', 0), }
                            used_symbols.add(disp_sym)
                        else:
                            new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.INVALID_REQUIRED_COMPONENTS)
                            new_error.invalid_required = disp_sym
                            append_error_warning(errors, current_comp_id, new_error)
                            warning_system.warn(f"reference symbol not found : {disp_sym}", RuntimeWarning)
            org_formula = org_formula.replace(sym, disp_sym)
            mid_formula = mid_formula.replace(sym, str(res))
        expr = sympy_post_replace_symbols(expr)

        org_formula = post_tune_latex(org_formula)
        mid_formula = post_tune_latex(mid_formula)
        
        try:
            current_report.result_value = expr.doit().evalf().rhs
        except Exception as e:
            new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.LATEX_UNCALCULABLE)
            new_error.occurred_equation = org_formula
            append_error_warning(errors, current_comp_id, new_error)
            warning_system.warn(f"latex equation is not calculable : {current_comp_id} / {current_report.symbol}", RuntimeWarning)
            current_report.result_value = 0 # TODO : 일단 0 처리. 추후 문제 발생 여부 확인
        
        if 'originalLatexEquation' in current_comp:
            origin_equation = current_comp['originalLatexEquation']
            if '=' in origin_equation:
                lhs, rhs = origin_equation.split('=', 1)
                if current_comp['latexSymbol'] == lhs.strip() or f"\\sym{{{current_comp['latexSymbol']}}}" == lhs.strip():
                    origin_equation = rhs.strip()
            if origin_equation != current_report.result_value:
                current_report.formula.append(origin_equation)
        else:
            # NOTE : 수식 출력 형태 변경 위해 후처리 formula 사용 하지 않음.
            if org_formula != current_report.result_value:
                current_report.formula.append(org_formula)
            if org_formula != mid_formula:
                current_report.formula.append(mid_formula)


        if 'min' in str(expr) or 'max' in str(expr):
            expr = sympy_post_processing(expr)
            current_report.result_value = expr.evalf().rhs
    
    if used_symbols:
        set_is_used_by_symbol(params_report, used_symbols)

    params_report.append(current_report)
    
    temp_precess_exception(current_report) # TODO : 현재 미개발 항목에 의해 의도하지 않은 결과 값을 임시로 처리. 개발 완료 후 삭제 필요

    return params_report, errors, warnings

def set_is_used_by_symbol(params_report, used_symbols):
    for report in params_report:
        if report.symbol in used_symbols:
            report.is_used = True

def get_report_bundles(content_trees, target_comps, symbol_to_value):
    report_bundles = []
    error_bundles, warning_bundles = {}, {}
    for content_tree in content_trees:
        report, errors, warnings = get_report(content_tree, symbol_to_value)
        report_bundles.append(report)
        error_bundles.update(errors)
        warning_bundles.update(warnings)

    report_bundles = get_unique_report_bundles(report_bundles, target_comps)
    return report_bundles, error_bundles, warning_bundles

def get_unique_report_bundles(report_bundles, target_comps):
    processed_symbols = []
    report_bundle_unique = []
    for report_bundle in report_bundles:
        report_unique = []
        for report in report_bundle:
            if report.id in target_comps:
                if report != report_bundle[-1]:
                    continue
            else: # report.id not in target_comps
                if report.symbol in processed_symbols or (report != report_bundle[-1] and report.is_used == False):
                    continue
            report_unique.append(report)
            processed_symbols.append(report.symbol)
        report_bundle_unique.append(report_unique)
    return report_bundle_unique

def make_report_json(report_bundles):
    report_bundle_json = []
    for report_bundle in report_bundles:
        report_json = []
        for report in report_bundle:
            report_json.append(report.to_dict())
        report_bundle_json.append(report_json)
    return {"result": report_bundle_json}