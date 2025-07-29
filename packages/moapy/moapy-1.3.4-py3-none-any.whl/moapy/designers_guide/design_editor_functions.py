from moapy.auto_convert import MBaseModel
from pydantic import Field
from moapy.designers_guide.resource import components, Content, Component
from moapy.designers_guide.resource_handler import create_content_component_manager
from moapy.designers_guide.core_engine.execute_calc_general import DG_Result_Reports, execute_calc_user_content
from moapy.designers_guide.core_engine.schema_function_creator import get_function_tree_schema

########################################################
# Get a component list (in server)
class DG_Component_List(MBaseModel):
    res_components: dict = Field(default_factory=dict)
    
def get_component_list() -> DG_Component_List:
    temp_resource = create_content_component_manager(
        content_list=[],
        component_list=components
    )
    tune_components = temp_resource.component_list
    for component in tune_components:
        if "table" in component:
            component["tableDetail"] = temp_resource.get_table_by_component(component)
            if "id" in component["tableDetail"]:
                del component["tableDetail"]["id"]
            if (component["table"] == 'formula' or component["table"] == 'text') and 'latexEquation' in component:
                del component["latexEquation"]
            elif component["table"] == 'dropdown':
                if "default" not in component:
                    if "data" not in component["tableDetail"] or len(component["tableDetail"]["data"]) < 2:
                        component["default"] = ""
                    else:
                        component["default"] = component["tableDetail"]["data"][1][0]

        if "compType" not in component:
            compType = temp_resource.get_component_type(component)
            if compType is None:
                print(f'{component["id"]} : is not have a compType ')
            else:
                component["compType"] = compType

    res = {
      "result": tune_components
    }
    return DG_Component_List(res_components = res)

########################################################
# Apply a component to a content
class DG_Response_Component(MBaseModel):
    error_list: list[str] = Field(default_factory=list)
    warning_list: list[str] = Field(default_factory=list),
    id: str = Field(default="")

def apply_component(
        target_component: Component,
) -> DG_Response_Component:
    # TODO : component 유효성 검사 추가 -> error_list, warning_list
    # TODO : component 유효성 통과 시 component id generator 추가 -> id
    return DG_Response_Component(error_list = [], warning_list = [], id = "")

########################################################
# Generate a content for User defined
class DG_User_Content(MBaseModel):
    error_list: list[str] = Field(default_factory=list)
    warning_list: list[str] = Field(default_factory=list),
    json_schema: dict = Field(default_factory=dict),
    # schema_function: str = Field(default=""), # NOTE : 저장하지 않음
    using_components: list[dict] = Field(default_factory=list),

from moapy.designers_guide.core_engine.content_calculator import pre_process_before_calc_for_user, reset_resource_on_user
from moapy.designers_guide.core_engine.schema_function_creator import get_function_tree
from moapy.designers_guide.resource_handler.simple_mapping_manager import reset_temp_mapping_data

def generate_user_content(
          user_content: Content,
          user_components: list[Component]
) -> DG_User_Content:
    def get_using_components_by_tree(content_trees, merged_resource):
        used_comp = []
        def get_components(node):
            current_components = []
            if node.children:
                for child in node.children:
                    current_components.extend(get_components(child))
            current_components.append(node.operation)
            return current_components

        for content_tree in content_trees:
            for component in get_components(content_tree):
                table = merged_resource.get_table_by_component(component)
                if table:
                    component['tableDetail'] = table
                    if "id" in component["tableDetail"]:
                        del component["tableDetail"]["id"]
                used_comp.append(component)
        return used_comp
    
    def get_unique_components(component_list: list[Component]):
        seen_keys = set()
        unique_components = []
        for component in component_list:
            key = component.get('id')
            if key not in  seen_keys:
                seen_keys.add(key)
                unique_components.append(component)
        return unique_components
    
    content_trees, merged_resource = get_function_tree(target_content=user_content, user_component=user_components) # 얘는 handler가 세팅되어 있어야하고
    using_components = get_unique_components(get_using_components_by_tree(content_trees, merged_resource))
    pre_process_before_calc_for_user(user_content, using_components) # 얘는 현재 목록만 세팅할 수 있다.
    [trees, schema, required] = get_function_tree_schema(content=user_content, components=using_components, generated_tree=content_trees)
    reset_temp_mapping_data()
    reset_resource_on_user()
    return DG_User_Content(error_list=[], warning_list=[], json_schema=schema, using_components=using_components)

########################################################
# Calculate a content for User defined
from moapy.designers_guide.resource_validator.resource_validator import validate_components, validate_content, validate_single_component, append_error_warning
def calc_user_content(
        target_content: Content,
        using_components: list[Component],
        req_inputs: dict
) -> DG_Result_Reports:
    result_info = DG_Result_Reports(error_list={}, warning_list={}, res_report={})
    errors, warnings = validate_content(target_content)
    result_info.error_list.update(errors)
    result_info.warning_list.update(warnings)

    errors, warnings = validate_components(using_components)
    result_info.error_list.update(errors)
    result_info.warning_list.update(warnings)

    if len(result_info.error_list) > 0:
        return result_info
    
    res_report = execute_calc_user_content(target_content=target_content, using_components=using_components, req_inputs=req_inputs) # NOTE : 상황에 따라서는 한번 더 가공 해야 될 수도 있음.
    result_info.error_list.update(res_report.error_list)
    result_info.warning_list.update(res_report.warning_list)
    result_info.res_report.update(res_report.res_report)

    return result_info

########################################################
# Health Check
from moapy.designers_guide.core_engine.content_calculator import set_isolated_test_mode, reset_isolated_test_mode
def validate_user_content(
        content: Content,
        components: list[Component]
) -> DG_Result_Reports:
    error_list, warning_list = {}, {}
            
    try:
        set_isolated_test_mode(True)
        validate_result = DG_Result_Reports(res_report={})

        if content is not None:
            errors, warnings = validate_content(content)
            for id, err_context in errors.items():
                append_error_warning(error_list, id, err_context)
            for id, warn_context in warnings.items():
                append_error_warning(warning_list, id, warn_context)

        occured_essential_error_comp = []
        for component in components:
            errors, warnings = validate_single_component(component)
            for id, err_context in errors.items():
                occured_essential_error_comp.append(id) # NOTE : Essential 오류 발생 시 연산 검사 할 수 없는 상황 발생
                append_error_warning(error_list, id, err_context)
            for id, warn_context in warnings.items():
                append_error_warning(warning_list, id, warn_context)

        valid_test_equataion_components = [component for component in components if component['id'] not in occured_essential_error_comp]
        temp_content = {
            "id": "validation_content",
            "standardType": "",
            "codeName": "",
            "codeTitle": "",
            "title": "",
            "description": "",
            "targetComponents": [component['id'] for component in valid_test_equataion_components]
        }
        calc_result = execute_calc_user_content(target_content=temp_content, using_components=valid_test_equataion_components, req_inputs={})
        for id, context in calc_result.error_list.items():
            append_error_warning(error_list, id, context)
        for id, context in calc_result.warning_list.items():
            append_error_warning(warning_list, id, context)

        validate_result.error_list = error_list
        validate_result.warning_list = warning_list

        return validate_result
    finally:
        reset_isolated_test_mode()