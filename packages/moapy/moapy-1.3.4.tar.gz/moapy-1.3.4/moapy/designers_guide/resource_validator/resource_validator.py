from sympy.parsing.latex.errors import LaTeXParsingError

from moapy.designers_guide.resource import Content, Component
from moapy.designers_guide.resource_handler import create_content_component_manager
from moapy.designers_guide.core_engine.content_calculator import resource_on_server
from moapy.designers_guide.resource_validator.symbol_abstrator import abstract_symbols_from_component
from moapy.designers_guide.resource_handler import ContentComponentManager
from moapy.designers_guide.resource_validator.error_format import ErrorWarning, ErrorType, ErrorCode, append_error_warning

def examine_component_using_symbols(component: Component, current_resource: ContentComponentManager) -> tuple[dict, dict]:
    '''
    latexEquation 및 table condition/point에 사용 된 symbol 검사
    - 연산에 필요한 symbol이 required에 정의 되어 있지 않음 > ERROR
    - required에 정의된 symbol이 실제 연산에 사용되지 않음 > WARNING
    '''
    errors = {}
    warnings = {}
    using_symbols = set()
    abstract_symbols_from_component(component)
    using_symbols.update(set(component['abstractedSymbols']))

    # NOTE : latex 자체 추출 방식 폐기
    # org_latex_expr = component.get("latexEquation", "")
    # if org_latex_expr != "":
    #     try:
    #         extracted_symbols = extract_symbols_from_latex(org_latex_expr)
    #         using_symbols.update(extracted_symbols)
    #         # print(f"{org_latex_expr} ==> {extracted_symbols}")
    #     except LaTeXParsingError  as e:
    #         new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.LATEX_SYNTAX_ERROR)
    #         new_error.occurred_equation = org_latex_expr
    #         append_error_warning(errors, component['id'], new_error)
    #         # print(f"LaTeX Parsing Error details: {str(e)}")  # 디버깅용
    #         # print(f"Error occurred at position: {e.position if hasattr(e, 'position') else 'unknown'}")  # 디버깅용
    #     except Exception as e:
    #         new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.LATEX_UNCALCULABLE)
    #         new_error.occurred_equation = org_latex_expr
    #         append_error_warning(errors, component['id'], new_error)
    #         # print(f"Unexpected error type: {type(e)}")  # 디버깅용
    #         # print(f"Error details: {str(e)}")  # 디버깅용

    # table_type = current_resource.get_table_type(component)
    # if table_type != "None":
    #     table_data = current_resource.get_table_by_component(component)
    #     if table_data is None:
    #         new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_COMPONENT_ESSENTIAL)
    #         new_error.occurred_property = "tableDetail"
    #         append_error_warning(errors, component['id'], new_error)
    #     else:
    #         if table_type == "formula" or table_type == "text":
    #             if "criteria" not in table_data or "data" not in table_data:
    #                 new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_COMPONENT_ESSENTIAL)
    #                 new_error.occurred_property = "criteria"
    #                 append_error_warning(errors, component['id'], new_error)
    #             else:
    #                 criteria_list = table_data["criteria"]
    #                 is_matrix = (len(criteria_list) >= 2 and criteria_list[1][0] != "")
    #                 for idx_criteria in range(len(criteria_list)):
    #                     criteria = criteria_list[idx_criteria]

    #                     for idx_criterion in range(len(criteria)):
    #                         org_criterion = criteria[idx_criterion]
    #                         try:
    #                             extracted_symbols = extract_symbols_from_criteria(org_criterion)
    #                             using_symbols.update(extracted_symbols)
    #                             # print(f"{org_criterion} ==> {extracted_symbols}")
    #                         except LaTeXParsingError as e:
    #                             new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.LATEX_SYNTAX_ERROR)
    #                             new_error.occurred_condition = org_criterion
    #                             append_error_warning(errors, component['id'], new_error)
    #                         except Exception as e:
    #                             new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.LATEX_UNCALCULABLE)
    #                             new_error.occurred_condition = org_criterion
    #                             append_error_warning(errors, component['id'], new_error)

    #                         if table_type == "text":
    #                             continue # NOTE: text 타입은 data 검사 생략
                            
    #                         data = ""
    #                         if is_matrix:
    #                             data = table_data["data"][idx_criterion][idx_criteria]
    #                         else:
    #                             data = table_data["data"][idx_criterion]

    #                         try:
    #                             extracted_symbols = extract_symbols_from_latex(data)
    #                             using_symbols.update(extracted_symbols)
    #                             # print(f"{data} ==> {extracted_symbols}")
    #                         except LaTeXParsingError as e:
    #                             new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.LATEX_SYNTAX_ERROR)
    #                             new_error.occurred_data = data
    #                             append_error_warning(errors, component['id'], new_error)
    #                         except Exception as e:
    #                             new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.LATEX_UNCALCULABLE)
    #                             new_error.occurred_data = data
    #                             append_error_warning(errors, component['id'], new_error)
    #         if table_type == "interpolation" or table_type == "bi-interpolation":
    #             if "point" not in table_data or "data" not in table_data:
    #                 new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_COMPONENT_ESSENTIAL)
    #                 new_error.occurred_property = "point"
    #                 append_error_warning(errors, component['id'], new_error)
    #             else:
    #                 for point in table_data["point"]:
    #                     using_symbols.add(point["symbol"])


    req_symbols = set()
    if "required" in component:
        for req_id in component["required"]:
            req_comp = current_resource.find_component_by_id(req_id)
            if req_comp is None:
                req_comp = resource_on_server.find_component_by_id(req_id)
            if req_comp is None:
                new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_REQUIRED_COMPONENTS)
                new_error.occurred_property = "required"
                append_error_warning(errors, component['id'], new_error)
            if req_comp is None:
                continue
            req_symbols.add(str(req_comp.get("latexSymbol")))


    using_symbols.discard(component['latexSymbol'])
    unused_symbols = list(using_symbols.difference(req_symbols))
    unused_req_symbols = list(req_symbols.difference(using_symbols))

    if len(unused_symbols) > 0:
        new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_REQUIRED_COMPONENTS)
        new_error.occurred_property = "required"
        append_error_warning(errors, component['id'], new_error)

    if len(unused_req_symbols) > 0:
        new_warning = ErrorWarning(ErrorType.WARNING, ErrorCode.UNUSED_REQUIRED_SYMBOLS)
        new_warning.occurred_property = "required"
        append_error_warning(warnings, component['id'], new_warning)
    
    return errors, warnings

def examine_content_essentials(content: Content) -> tuple[dict, dict]:
    '''
    content 필수 요소 검사
    '''
    errors = {}
    warnings = {}

    if "targetComponents" not in content or len(content['targetComponents']) == 0:
        new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_CONTENT_ESSENTIAL)
        new_error.occurred_property = "targetComponents"
        append_error_warning(errors, content['id'], new_error)

    return errors, warnings

def examine_component_essentials(component: Component) -> tuple[dict, dict]:
    '''
    component 필수 요소 검사
    '''
    errors = {}
    warnings = {}

    # TODO : 세분화 필요한지 논의 필요
    if "id" not in component or component['id'] == "":
        new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_COMPONENT_ESSENTIAL)
        new_error.occurred_property = "id"
        append_error_warning(errors, component['id'], new_error)

    if "codeName" not in component or component['codeName'] == "":
        new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_COMPONENT_ESSENTIAL)
        new_error.occurred_property = "codeName"
        append_error_warning(errors, component['id'], new_error)

    if "reference" not in component or len(component['reference']) == 0:
        new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_COMPONENT_ESSENTIAL)
        new_error.occurred_property = "reference"
        append_error_warning(errors, component['id'], new_error)

    if "latexSymbol" not in component or len(component['latexSymbol']) == 0:
        new_error = ErrorWarning(ErrorType.ERROR, ErrorCode.MISSING_COMPONENT_ESSENTIAL)
        new_error.occurred_property = "latexSymbol"
        append_error_warning(errors, component['id'], new_error)

    return errors, warnings
    
def validate_components(component_list: list[Component]) -> tuple[dict, dict]:
    resource_current = create_content_component_manager(
        component_list=component_list
        )
    errors_list = {}
    warnings_list = {}
    for component in component_list:
        # component 필수 요소 검사
        errors, warnings = examine_component_essentials(component)
        errors_list.update(errors)
        warnings_list.update(warnings)

        # using symbol 검사
        errors, warnings = examine_component_using_symbols(component, resource_current)
        errors_list.update(errors)
        warnings_list.update(warnings)

    return errors_list, warnings_list

def validate_single_component(component: Component) -> tuple[dict, dict]:
    errors_list = {}
    warnings_list = {}

    errors, warnings = examine_component_essentials(component)
    errors_list.update(errors)
    warnings_list.update(warnings)

    return errors_list, warnings_list

def validate_content(content: Content) -> tuple[dict, dict]:
    errors_list = {}
    warnings_list = {}

    errors, warnings = examine_content_essentials(content)
    errors_list.update(errors)
    warnings_list.update(warnings)

    return errors_list, warnings_list


########################################################################################
# # TODO : 테스트 코드 삭제

# from moapy.designers_guide.design_editor_functions import generate_user_content

# def test_validate_component():
#     errors_list = []
#     warnings_list = []
#     sym_to_temp_list = []

#     temp_user_content = {
#         "id": "temp_content",
#         "targetComponents": [],
#         # "targetComponents": ['G4_COMP_4', 'G4_COMP_5', 'G4_COMP_6', 'G4_COMP_7', 'G4_COMP_8', 'G4_COMP_9'], # content 1 target. # TODO : table(result)에 대해서 추출 보완 필요
#         # "targetComponents": ['G3_COMP_24'], # content 2 target.
#         # "targetComponents": ['G1_COMP_16', 'G1_COMP_17'], # content 3 target.
#         # "targetComponents": ['G2_COMP_1', 'G2_COMP_5', 'G2_COMP_6'] # content 4 target.
#         # "targetComponents": ['G5_COMP_1', 'G5_COMP_13', 'G5_COMP_16'], # content 5 target.
#         # "targetComponents": ['G6_COMP_1'], # content 6 target.
#         # "targetComponents": ['G7_COMP_1', 'G7_COMP_2', 'G7_COMP_7', 'G7_COMP_9'], # content 7 target.
#         # "targetComponents": ['G8_COMP_1', 'G8_COMP_2', 'G8_COMP_10', 'G8_COMP_11', 'G8_COMP_12', 'G8_COMP_13'], # content 8 target.
#         # "targetComponents": ['G9_COMP_1', 'G9_COMP_2', 'G9_COMP_11', 'G9_COMP_13', 'G9_COMP_14'], # content 9 target.
#         # "targetComponents": ['G10_COMP_1'], # content 10 target.
#         # "targetComponents": ['G11_COMP_2', 'G11_COMP_3'], # content 11 target.
#         # "targetComponents": ['G15_COMP_6', 'G15_COMP_8', 'G15_COMP_9'], # content 15 target.
#     }
#     for idx, server_content in enumerate(resource_on_server.content_list):
#         if idx >= 1 and idx <= 30:
#         # if idx == 18:
#             temp_user_content["targetComponents"].extend(server_content["targetComponents"])
#     temp_user_content["targetComponents"] = list(set(temp_user_content["targetComponents"]))
    
#     errors, warnings, json_schema, using_components = generate_user_content(user_content=temp_user_content, user_components=[])
#     for comp in using_components[1]: # NOTE : 하나의 content에 대해서 테스트
#     # for comp in resource_on_server.component_list:
#         errors, warnings = validate_components([comp])
#         errors_list.extend(errors)
#         warnings_list.extend(warnings)
        
#     TEST_DIRECTORY_PATH = "workspace/designers_guide/res_files"
#     import json
#     json_data = {
#         "errors": errors_list,
#         "warnings": warnings_list,
#         "sym_to_temp": sym_to_temp_list
#     }
#     json_text = json.dumps(json_data, indent=4)
#     with open(f"{TEST_DIRECTORY_PATH}/validate_components.json", "w", encoding="utf-8") as report_json_file:
#         report_json_file.write(json_text)

# test_validate_component()