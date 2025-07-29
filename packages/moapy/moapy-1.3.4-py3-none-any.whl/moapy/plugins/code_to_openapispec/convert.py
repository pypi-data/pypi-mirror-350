import moapy.auto_convert as auto_convert
import json
import sys
import ast
import jsonref
import copy
import types
import importlib
from pydantic import Field
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from moapy.version import moapy_version
from moapy.api_url import API_PYTHON_EXECUTOR
from moapy.auto_convert import auto_schema, MBaseModel, ConfigDict

class AutoConvertFinder(ast.NodeVisitor):
    def __init__(self):
        self.auto_convert_funcs = []

    def visit_FunctionDef(self, node):
        # 데코레이터가 auto_schema인지 확인
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "auto_schema":
                self.auto_convert_funcs.append(node.name)
            elif (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Name)
                and decorator.func.id == "auto_schema"
            ):
                # auto_schema가 호출된 경우도 확인
                self.auto_convert_funcs.append(node.name)
        self.generic_visit(node)

def resolve_refs_and_merge(json_data):
    # 원본 데이터를 깊은 복사하여 변경되지 않도록 함
    resolved_json = copy.deepcopy(json_data)

    # jsonref로 참조를 해소함
    resolved_json = jsonref.JsonRef.replace_refs(resolved_json)

    # 원본 데이터를 순회하면서 $ref가 있던 곳의 추가 정보를 복사하여 병합
    def merge_refs(original, resolved):
        if isinstance(original, dict):
            for key, value in original.items():
                if isinstance(value, dict):
                    # $ref가 있는 경우
                    if "$ref" in value:
                        # resolved에서 병합
                        resolved_value = resolved.get(key, {})
                        # 모든 key-value 쌍을 병합
                        resolved[key] = {**resolved_value, **value}
                        # original에서 키를 가져와 병합
                        for k, v in original[key].items():
                            if k != "$ref":  # $ref는 제외
                                resolved[key][k] = v

                        # default가 있는 경우 특별 처리
                        if "default" in original[key] and isinstance(
                            original[key]["default"], dict
                        ):
                            # original의 default에서 value와 unit을 가져와 병합
                            default_value = original[key]["default"].get("value")
                            default_unit = original[key]["default"].get("unit")

                            if default_value is not None:
                                # value를 properties에 추가
                                resolved[key]["properties"]["value"]["default"] = (
                                    default_value
                                )

                            if default_unit is not None:
                                # unit을 properties에 추가
                                resolved[key]["properties"]["unit"]["default"] = (
                                    default_unit
                                )

                        resolved[key].pop("$ref", None)  # $ref 제거
                    else:
                        merge_refs(value, resolved.get(key, {}))
        elif isinstance(original, list):
            for index, item in enumerate(original):
                merge_refs(item, resolved[index])

    merge_refs(json_data, resolved_json)
    return resolved_json

def extract_auto_schema_functions(code: str):
    """주어진 코드에서 auto_schema 데코레이터가 붙은 함수 이름을 추출합니다."""
    try:
        parsed_code = ast.parse(code)  # 코드 파싱
        finder = AutoConvertFinder()  # 탐색기 인스턴스 생성
        finder.visit(parsed_code)  # AST 방문
        return finder.auto_convert_funcs  # 찾은 함수 이름 반환
    except Exception as e:
        print(f"Error parsing code: {e}")
        return []

def generate_openapi_spec(router, resolve_refs=True):
    temp_app = FastAPI(
        title="moapy", description="Schema for moapy", version=moapy_version
    )
    temp_app.include_router(router)
    openapi_spec = get_openapi(
        title=temp_app.title,
        version=temp_app.version,
        openapi_version=temp_app.openapi_version,
        description=temp_app.description,
        routes=temp_app.routes,
        servers=[
            {"url": API_PYTHON_EXECUTOR},
        ],
    )

    def handle_composite_keys(schema, key):
        if key in schema:
            for item in schema[key]:
                if "$ref" in item:
                    schema.update(item)
            del schema[key]

    def apply_camel_case_to_schema_keys(schema):
        if isinstance(schema, dict):
            return {auto_convert.to_camel(k): v for k, v in schema.items()}
        return schema

    def process_schema(schema):
        if isinstance(schema, dict):
            for key, value in list(schema.items()):
                if key == "schema":  # "schema" 키 내부의 Key만 변환
                    schema[key] = apply_camel_case_to_schema_keys(value)
                elif key in {"allOf"}:
                    handle_composite_keys(schema, key)
                else:
                    process_schema(value)
        elif isinstance(schema, list):
            for item in schema:
                process_schema(item)

    process_schema(openapi_spec)
    openapi_spec_ref = resolve_refs_and_merge(openapi_spec) if resolve_refs else openapi_spec

    return openapi_spec_ref

class InputCode(MBaseModel):
    script_code: str = Field(default="""from fastapi import APIRouter

router = APIRouter()
@auto_schema(title="python to openapi spec", description="This tool generates OpenAPI spec from Python code")
def hello_world():
    return {"message": "Hello, World!"}
""", title="Python Script Code", description="Python script code to generate OpenAPI spec")

    model_config = ConfigDict(title="Python Script Code Input")

def ensure_escaped(script_code: str) -> str:
    """
    입력된 코드가 이스케이프 처리되었는지 판단하고,
    필요 시 이스케이프 처리된 문자열로 변환합니다.

    :param script_code: 원본 코드 문자열
    :return: 이스케이프 처리된 코드 문자열
    """
    try:
        # 이스케이프된 코드라면 JSON 디코딩 가능
        json.loads(script_code)
        print("The input is already escaped.")
        return script_code  # 이미 이스케이프된 경우 그대로 반환
    except json.JSONDecodeError:
        # JSON 디코딩에 실패하면 이스케이프 처리가 필요함
        print("The input is not escaped. Escaping now.")
        return json.dumps(script_code)  # 이스케이프 처리 후 반환

@auto_schema(title="python to openapi spec", description="This tool generates OpenAPI spec from Python code")
def generate_openapi_spec_from_code(inp: InputCode) -> str:
    """
    Python 코드 문자열에서 정의된 함수들에 대해 OpenAPI 스펙을 생성합니다.

    매개변수:
        script_code (str): Python 코드 문자열
        app (FastAPI): FastAPI 애플리케이션 인스턴스
        resolve_refs (bool): 스키마에서 참조를 해석할지 여부
    """
    if not inp.script_code:
        raise ValueError("입력된 코드가 비어 있습니다.")
    app = FastAPI()

    module_name = "dynamic_module"
    dynamic_module = types.ModuleType(module_name)
    # 동적 모듈을 sys.modules에 등록
    sys.modules[module_name] = dynamic_module
    # 이제 importlib.import_module 사용 가능
    module = importlib.import_module(module_name)
    # 코드 실행 후 동적 모듈에 추가
    exec(inp.script_code, dynamic_module.__dict__)
    # 코드에서 함수들 추출
    functions = extract_auto_schema_functions(inp.script_code)

    if not functions:
        raise ValueError("입력된 코드에서 호출 가능한 함수가 없습니다.")

    # 각 함수에 대해 OpenAPI 스펙 생성
    for func in functions:
        # auto_convert.get_router_for_module()가 동적으로 불러온 함수에도 작동한다고 가정
        full_function_name = module_name + func
        router = auto_convert.get_router_for_module(full_function_name)
        app.include_router(router)

        return generate_openapi_spec(router)

if __name__ == "__main__":
    # 예시로 사용할 코드 (스크립트 코드 자체를 문자열로 입력)
    data = {
  "inp": {
    "script_code": "from pydantic import Field, ConfigDict\nfrom moapy.auto_convert import auto_schema, MBaseModel\nfrom moapy.designers_guide.resource.report_form import ReportForm\nfrom moapy.designers_guide.func_general import DG_Result_Reports\nfrom moapy.data_post import print_result_data\nfrom typing import List, Dict, Optional\nfrom pydantic import Field, BaseModel, field_validator\nimport math\n\nclass ExposureCategory(str):\n    B = \"B\"\n    C = \"C\"\n    D = \"D\"\n\ndef get_kd_value(selection: str) -> float:\n    if selection == \"Buildings-Main wind force resisting system\":\n        return 0.85\n    elif selection == \"Buildings-Components and Cladding\":\n        return 0.85\n    elif selection == \"Arched roofs\":\n        return 0.85\n    elif selection == \"Circle domes\":\n        return 1.0\n    elif selection == \"Chimneys, tanks, and similar Structures-Square\":\n        return 0.9\n    elif selection == \"Chimneys, tanks, and similar Structures-Hexagonal\":\n        return 0.95\n    elif selection == \"Chimneys, tanks, and similar Structures-Octagonal\":\n        return 1.0\n    elif selection == \"Chimneys, tanks, and similar Structures-Round\":\n        return 1.0\n    elif selection == \"Solid freestanding walls, roof top equipment, and solid freestanding and attached signs\":\n        return 0.85\n    elif selection == \"Open Signs and single-plane open frames\":\n        return 0.85\n    elif selection == \"Trussed towers - Triangular, square, or rectangular\":\n        return 0.95\n    elif selection == \"Trussed towers - All other cross sections\":\n        return 0.95\n    else:\n        raise ValueError(f\"Invalid kd selection: {selection}\")\n\nclass Inputdata(MBaseModel):\n    wind_speed: float = Field(default=120, title=\"Wind Speed\", description=\"Basic wind speed obtained from ASCE7-22  [ft/s]\")\n    Height_ft: float = Field(default=120, title=\"Mean roof height\", description=\"Mean roof height of a building or height of other structure [ft]\")\n    exposure: str = Field(default=\"C\", title=\"Exposure\", description=\"Exposure\", enum=[\"B\", \"C\", \"D\"])\n    Lh: float = Field(default=60, title=\"Distandce upwind, Lh\", description=\"Distance upwind of crest of hill, ridge, or escarpment to where the difference in ground elevation is half the height of the hill, ridge, or escarpment, ft\")\n    topo_K1_multi: str = Field(default=\"2D Ridge\", title=\"Topographic Factor K1 Multiplier\", description=\"Topographic Factor K1 Multiplier\", enum=[\"2D Ridge\", \"2D Escarpment\", \"3D Axisymmetrical Hill\"])\n    topo_K2_x: float = Field(default=30, title=\"Topographic K2 Multiplier x\", description=\"Topographic K2 Multiplier x value to obtain Kzt\")\n    topo_K2_multi: str = Field(default=\"All Other Cases\", title=\"Topographic Factor K2 Multiplier\", description=\"Topographic Factor K2 Multiplier\", enum=[\"2D Escarpment\", \"All Other Cases\"])\n    topo_K3_z: float = Field(default=30, title=\"Topographic K3 Multiplie z\", description=\"Topographic K3 Multiplier z value to obtain Kzt\")\n    topo_K3_multi: str = Field(default=\"2D Ridge\", title=\"Topographic Factor K3 Multiplier\", description=\"Topographic Factor K3\", enum=[\"2D Ridge\", \"2D Escarpment\", \"3D Axisymmetrical Hill\"])\n    ke: float = Field(default=\"0\", title=\"Sea Level, Ke\", description=\"Ground elevation factor\", enum=[\"<0\", \"0\", \"1000\", \"2000\", \"3000\", \"4000\", \"5000\", \"6000\", \">6000\"])\n    kd: str = Field(\n        default=\"Buildings-Main wind force resisting system\",\n        title=\"Wind Directionality Factor, Kd\",\n        description=\"Wind Directionality Factor\",\n        enum=[\n            \"Buildings-Main wind force resisting system\",\n            \"Buildings-Components and Cladding\",\n            \"Arched roofs\",\n            \"Circle domes\",\n            \"Chimneys, tanks, and similar Structures-Square\",\n            \"Chimneys, tanks, and similar Structures-Hexagonal\",\n            \"Chimneys, tanks, and similar Structures-Octagonal\",\n            \"Chimneys, tanks, and similar Structures-Round\",\n            \"Solid freestanding walls, roof top equipment, and solid freestanding and attached signs\",\n            \"Open Signs and single-plane open frames\",\n            \"Trussed towers - Triangular, square, or rectangular\",\n            \"Trussed towers - All other cross sections\"\n        ]\n    )\n    kz: float = Field(default=0.85, title=\"Velocity Pressure Exposure Coefficient, kz(kh)\", description=\"Velocity pressure exposure coefficient evaluated at height z = h\")\n    model_config = ConfigDict(\n        title=\"ASCE 7-22 Wind Velocity Pressure Calculation Input\",\n        description=\"Standard for wind Velocity Pressure on buildings and structures\"\n    )\n    def get_kd_value(self) -> float:\n        return get_kd_value(self.kd)\n\n@auto_schema(\n    title=\"Wind load pressure calculation\",\n    description=(\n        \"This tool calculates the wind load pressure on a structure according to the ASCE 7-22 standard.\"\n    )\n)\ndef wind_load_pressure_calculator(input_data: Inputdata) -> DG_Result_Reports:\n    print(\"Starting wind load pressure calculation...\")\n    k1 = calculate_topo_K1(input_data.Height_ft, input_data.Lh, input_data.topo_K1_multi)\n    k2 = calculate_topo_K2(\n        topo_K2_x=input_data.topo_K2_x, Lh=input_data.Lh, topo_K2_multi=input_data.topo_K2_multi, exposure=input_data.exposure, Height_ft=input_data.Height_ft)\n    k3 = calculate_topo_K3(input_data.topo_K3_z, input_data.Lh, input_data.topo_K3_multi)\n    kzt = (1 + k1 * k2 * k3) ** 2\n    kd = input_data.get_kd_value()\n    ke = calculate_ke(input_data.ke)\n    kz = calculate_kz(input_data.Height_ft, input_data.exposure)\n    V = input_data.wind_speed\n    q = 0.00256 * kz * kzt * ke * (V ** 2)\n    res_k1 = ReportForm(title='k1', description=\"K1 Multipliers from ASCE7-22 Figure 26.8-1 to obtain Kzt\", result=k1, symbol=\"K_{1}\", decimal=2)\n    res_k2 = ReportForm(title='k2', description=\"K2 Multipliers from ASCE7-22 Figure 26.8-1 to obtain Kzt\", result=k2, symbol=\"K_{2}\", decimal=2)\n    res_k3 = ReportForm(title='k3', description=\"K3 Multipliers from ASCE7-22 Figure 26.8-1 to obtain Kzt\", result=k3, symbol=\"K_{3}\", decimal=2)\n    res_kzt = ReportForm(title='kzt', description=\"Topographic Factor\", formula=[\"(1+ k_{1} \\\\times k_{2} \\\\times k_{3})^2 \", f\"(1 + {k1} \\\\times {k2} \\\\times {k3})^2\"], result=kzt, symbol=\"K_{zt}\", decimal=2)\n    res_q = ReportForm(title='qz', description=\"Velocity pressure at height z\", formula=[\"0.00256 \\\\times k_{z} \\\\times k_{zt} \\\\times k_{e}\\\\times V^2 \", f\"0.00256 \\\\times {kz} \\\\times {kzt} \\\\times {ke}\\\\times {V}^2\"], result=q, symbol=\"q_{z}\", unit=\"psi\", decimal=5)\n    results = {\n        \"result\": [\n            [\n                res_k1.to_dict(),\n                res_k2.to_dict(),\n                res_k3.to_dict(),\n                res_kzt.to_dict(),\n                res_q.to_dict()\n            ]\n        ]\n    }\n    return DG_Result_Reports(res_report=results)\n\nif __name__ == \"__main__\":\n    res = wind_load_pressure_calculator(Inputdata())\n    print_result_data(res)"
  }
}
    
    print(str(generate_openapi_spec_from_code(**data)))
