import re
from moapy.version import moapy_version
from moapy.designers_guide.resource_handler.content_component import Content, Component
from moapy.designers_guide.resource_handler import create_content_component_manager
import moapy.designers_guide.core_engine.content_calculator as calc_util
import moapy.designers_guide.resource.defined_format.report_form as report_form

__py_executor_url_rel__ = [{"url": "https://moa.midasit.com/backend/python-executor/"}]
__py_executor_url_dev__ = [
    {"url": "https://moa.rpm.kr-dv-midasit.com/backend/python-executor/"},
    {"url": "https://moa.rpm.kr-st-midasit.com/backend/function-executor/python-execute/"},
]

# TODO : resource&mapping data 관리 구조 구축 후 global 변수 정리 필요
resource_handler = None
target_content = None
target_components = None

def set_user_resource_handler():
    global user_resource_handler
    user_resource_handler = user_resource_handler

def reset_resource_handler():
    global resource_handler
    global target_content
    global target_components
    resource_handler = create_content_component_manager(
        content_list=[target_content],
        component_list=target_components
    )
    return resource_handler

def get_resource_handler():
    global resource_handler
    if resource_handler is None:
        resource_handler = reset_resource_handler()
    return resource_handler

def generate_json_schema_content(target_content):
    handler = get_resource_handler()
    schema = {
        "standardType": target_content.get("standardType", ""),
        "codeName": target_content.get("codeName", ""),
        "codeTitle": target_content.get("codeTitle", ""),
        "title": target_content.get("title", "None Title"),
        "description": target_content.get("description", "None Description"),
        "edition": target_content.get("edition", ""),
        "figurePath": f"{handler.get_figure_server_url()}/{target_content['figureFile']}"
        if (target_content.get("figureFile", None) != None)
        else None,
    }
    return schema

def generate_json_schema_component(comp):
    handler = get_resource_handler()

    schema = {
        "title": comp.get("title", ""),
        "type": comp.get("type", "string"),
        "description": comp.get("description", ""),
        "default": comp.get("default", ""),
    }

    if "table" in comp and comp["table"] == "dropdown":
        table_enum = handler.get_table_enum_by_component(comp)
        if table_enum is not None:
            schema["enum"] = table_enum
            if "default" not in schema or schema["default"] == "":
                schema['default'] = table_enum[0]

    # NOTE : limits 다른 방식 적용
    # limits_minimum = {
    #     "type": "number",
    #     "exclusive": False,
    #     "value": None,
    # }
    # limits_maximum = {
    #     "type": "number",
    #     "exclusive": False,
    #     "value": None,
    # }
    # limits = comp.get("limits", {})
    # if limits:
    #     if "inMin" in limits:
    #         limits_minimum["value"] = limits.get("inMin", 0)
    #         limits_minimum["exclusive"] = False
    #     if "exMin" in limits:
    #         limits_minimum["value"] = limits.get("exMin", 0)
    #         limits_minimum["exclusive"] = True
    #     if "exMax" in limits:
    #         limits_maximum["value"] = limits.get("exMax", 0)
    #         limits_maximum["exclusive"] = True
    #     if "inMax" in limits:
    #         limits_maximum["value"] = limits.get("inMax", 0)
    #         limits_maximum["exclusive"] = False

    limits = comp.get("limits", {})
    if limits:
        if "inMin" in limits:
            schema["minimum"] = limits.get("inMin", None)
        if "exMin" in limits:
            schema["exclusiveMinimum"] = limits.get("exMin", None)
        if "exMax" in limits:
            schema["exclusiveMaximum"] = limits.get("exMax", None)
        if "inMax" in limits:
            schema["maximum"] = limits.get("inMax", None)

    figure_file_path = comp.get("figureFile", None)
    if figure_file_path:
        figure_file_path = f"{handler.get_figure_server_url()}/{figure_file_path}"

    sub_module_detail = {
        "codeName": {
            "type": "string",
            "default": comp.get("codeName", ""),  # 설계 기준 번호 (string)
        },
        "reference": {
            "type": "array",
            "default": comp.get("reference", []),  # 포함 section (string)
        },
        "compType": {
            "type": "string",
            "default": comp.get("compType", ""),  # component type (string)
        },
        "symbol": {
            "type": "string",
            "default": comp.get("latexSymbol", ""),  # latex symbol (raw string)
        },
        "unit": {
            "type": "string",
            "default": comp.get("unit", ""),  # unit (string)
        },
        "notation": {
            "type": "string",
            "default": comp.get(
                "notation", ""
            ),  # UI 표시 형식. "standard", "scientific"(XeY), "percentage"(X%), "text"
        },
        "decimal": {
            "type": "number",
            "default": comp.get("decimal", None),  # UI 표시 소수점 자리수 (number)
        },
        # NOTE : limits 다른 방식 적용
        # "limits": { # 결과 값 제한 (number, object)
        #     "type": "object",
        #     "properties": {
        #         "minimum": limits_minimum,
        #         "maximum": limits_maximum,
        #     }
        # },
        # TODO : required component 필요 시 추가
        # "req_component": {
        #     "type": "array",
        #     "defalut": comp.get("required", []), # related/required component id list (string)
        # },
        "figurePath": {
            "type": "string",
            "value": figure_file_path,  # figure file path (string)
        },
        "descriptTable": {
            "type": "array",
            "value": handler.convert_enum_table_to_detail(comp),
        },
    }
    
    if "refStd" in comp:
        sub_module_detail["refStd"] = {
            "type": "string",
            "default": comp.get("refStd", ""),
            "description": "",
        }
    elif comp.get("useStd", False):
        sub_module_detail["refStd"] = {
            "type": "string",
            "default": "NDPs",  # 설계 기준 반영 여부 (boolean)
            "description": "Nationally Determined Parameters",
        }
    if comp.get("compType", "") == "":
        comp["compType"] = handler.get_component_type(comp)

    schema["x-component-detail"] = sub_module_detail

    return {comp["id"]: schema}

def func_sort_comp(id):
    return [int(text) if text.isdigit() else text for text in re.split(r"(\d+)", id)]

def get_auto_func_name(target_content):
    return f"calc_content_{target_content['id']}"

def get_function_tree(
        target_content: Content,
        user_component: list[Component] | None = None
        ):
    
    merged_resource = None
    if user_component is not None:
        merged_resource = calc_util.set_temp_merged_resource(user_content=target_content, user_components=user_component)

    target_comps_id = target_content.get("targetComponents", [])
    res_tree = calc_util.get_function_tree_by_components(target_comps_id)

    if user_component is not None:
        calc_util.reset_temp_merged_resource()

    return res_tree, merged_resource

def get_leaf_nodes(node):
    leaf_nodes = []
    if node.children:  # 자식이 있는 경우, 재귀적으로 자식들을 탐색
        for child in node.children:
            leaf_nodes.extend(get_leaf_nodes(child))
    else:  # 만약 자식이 없는 노드면 (리프 노드)
        leaf_nodes.append(node)

    return leaf_nodes

def get_function_tree_schema(
    content: Content,
    components: list[Component],
    generated_tree: list[calc_util.TreeNode] | None = None,
    ):

    global target_content
    global target_components
    target_content = content
    target_components = components
    reset_resource_handler()
    handler = get_resource_handler()

    def is_const(comp):
        return comp.get("const", False) == True

    params_tree = []
    req_properties = {}
    required = set()
    res_properties = {}

    if generated_tree:
        params_tree = generated_tree
    else:
        params_tree, _ = get_function_tree(target_content)

    for content_tree in params_tree:
        params_comp = []
        leafs = get_leaf_nodes(content_tree)
        for leaf in leafs:
            param = handler.find_component_by_id(leaf.operation["id"])
            params_comp.append(param)

        for param_comp in params_comp:
            if is_const(param_comp):
                continue
            req_properties.update(generate_json_schema_component(param_comp))
            if is_const(param_comp) == False:
                required.add(param_comp["id"])

        comp = handler.find_component_by_id(content_tree.operation["id"])
        res_properties.update(generate_json_schema_component(comp))

    req_properties = dict(
        sorted(req_properties.items(), key=lambda item: func_sort_comp(item[0]))
    )
    req_required = sorted(list(required), key=lambda item: func_sort_comp(item))

    res_properties = dict(
        sorted(res_properties.items(), key=lambda item: func_sort_comp(item[0]))
    )

    post = {
        "summary": target_content.get("title", ""),
        "description": target_content.get("description", ""),
        "x-content-info": generate_json_schema_content(target_content),
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        # "x-content-info": generate_json_schema_content(target_content),
                        "type": "object",
                        "properties": req_properties,
                        "required": req_required,
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Successful response",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": report_form.ReportForm().to_dict(),
                        }
                    }
                },
            }
        },
    }

    path = f"/execute?functionId=moapy-designers_guide-func_execute-{get_auto_func_name(target_content)}"
    schema = {
        # "$ref": f"#/paths/{path.replace("/", "~1")}/post/requestBody/content/application~1json/schema", # NOTE : rjsf 테스트 시 주석 해제
        "openapi": "3.1.0",
        "info": {
            "title": "moapy",
            "description": "Schema for moapy",
            "version": moapy_version,
        },
        "servers": __py_executor_url_dev__,
        # "servers": __py_executor_url_rel__,
        "paths": {
            path: {
                "post": post,
            }
        },
    }

    return [params_tree, schema, req_required]

def get_auto_function(target_content, required):
    handler = get_resource_handler()
    func_name = get_auto_func_name(target_content)
    target_comps = target_content.get("targetComponents", [])

    func_params = ""
    func_input = "inputs = {"
    for req in required:
        func_input += f'"{req}": {req}'
        curr_comp = handler.find_component_by_id(req)
        if curr_comp is None:
            continue
        datatype = curr_comp.get("type", "number")
        func_params += f"{req}: "
        if datatype == "number":
            func_params += "float"
        elif datatype == "string":
            func_params += "str"
        elif datatype == "array":
            func_params += "list"
        if req != required[-1]:
            func_params += ", "
            func_input += ", "
    func_input += "}"

    func_code = f"""from moapy.designers_guide.core_engine.execute_calc_general import execute_calc_content, DG_Result_Reports

def {func_name}({func_params}) -> DG_Result_Reports:
    target_components = {target_comps}
    {func_input}
    return execute_calc_content(target_components, inputs)
"""
    return func_code

__all__ = ["get_function_tree_schema", "get_auto_func_name", "get_auto_function"]