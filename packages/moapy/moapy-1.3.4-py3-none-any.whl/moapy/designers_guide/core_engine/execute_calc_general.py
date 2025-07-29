import moapy.designers_guide.core_engine.content_calculator as calc_logic
from moapy.designers_guide.resource import Content
from moapy.auto_convert import MBaseModel
from pydantic import Field
from moapy.designers_guide.resource_handler.simple_mapping_manager import reset_temp_mapping_data

class DG_Result_Reports(MBaseModel):
    error_list: dict = Field(default_factory=dict)
    warning_list: dict = Field(default_factory=dict),
    res_report: dict = Field(default_factory=dict)

def execute_calc_content(target_components: list, req_inputs: dict) -> DG_Result_Reports:
    symbol_to_value = []
    for id, val in req_inputs.items():
        symbol_to_value.append({"component": id, "value": val})

    calc_logic.pre_process_before_calc()
    content_trees = calc_logic.get_function_tree_by_components(target_components)
    report_bundles, _, _ = calc_logic.get_report_bundles(content_trees, target_components, symbol_to_value)
    report_json = calc_logic.make_report_json(report_bundles)

    return DG_Result_Reports(res_report=report_json)

def execute_calc_user_content(target_content: Content, using_components: list, req_inputs: dict) -> DG_Result_Reports:
    symbol_to_value = []
    for id, val in req_inputs.items():
        symbol_to_value.append({"component": id, "value": val})

    if "targetComponents" not in target_content or target_content["targetComponents"] is []:
        return DG_Result_Reports(error_list=["targetComponents is not found"])
    
    calc_logic.pre_process_before_calc_for_user(target_content, using_components)
    target_components = target_content["targetComponents"]
    content_trees = calc_logic.get_function_tree_by_components(target_components)
    report_bundles, error_bundles, warning_bundles = calc_logic.get_report_bundles(content_trees, target_components, symbol_to_value)
    report_json = calc_logic.make_report_json(report_bundles)

    reset_temp_mapping_data()
    calc_logic.reset_resource_on_user()
    
    return DG_Result_Reports(error_list=error_bundles, warning_list=warning_bundles, res_report=report_json)