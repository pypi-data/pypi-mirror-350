import ctypes
import json
import base64
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import SectionRectangle, SectionForce, Moment, enUnitMoment, BucklingLength, MemberForce, EffectiveLengthFactor, Length, Force, OuterPolygon
from moapy.rc_pre import MaterialNative, ColumnRebarPattern, GeneralRebarPattern, EquivalentAreaGeneralSect
from moapy.enum_pre import enUnitSystem, enUnitLength
from moapy.dgnengine.base import load_dll, call_func, read_file_as_binary
from moapy.data_post import ResultBytes

# rjsf table 완성되면 다시 열자.
# @auto_schema(
#     title="Eurocode 2 General Column Design",
#     description="Eurocode 2 provides a comprehensive review of reinforced concrete (RC) General column design with a focus on strength assessment, available in Excel format.",
#     std_type="EUROCODE",
#     design_code="EN1992-1-1:2004"
# )
# def report_ec2_generalcolumn(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
#                              sect: OuterPolygon = OuterPolygon(),
#                              eff_area: EquivalentAreaGeneralSect = EquivalentAreaGeneralSect.create_default(enUnitSystem.SI),
#                              rebar: GeneralRebarPattern = GeneralRebarPattern.create_default(enUnitSystem.SI),
#                              force: MemberForce = MemberForce.create_default(enUnitSystem.SI),
#                              length: BucklingLength = BucklingLength.create_default(enUnitSystem.SI),
#                              eff_len: EffectiveLengthFactor = EffectiveLengthFactor()) -> ResultBytes:
#     dll = load_dll()
#     json_data_list = [matl.model_dump_json(), sect.model_dump_json(), eff_area.model_dump_json(), rebar.model_dump_json(), force.model_dump_json(), length.model_dump_json(), eff_len.model_dump_json()]
#     file_path = call_func(dll, 'Report_EC2_GeneralColumn', json_data_list)
#     if file_path is None:
#         return ResultBytes(type="md", result="Error: Failed to generate report.")
#     return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

# def calc_ec2_generalcolumn(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
#                            sect: OuterPolygon = OuterPolygon(),
#                            eff_area: EquivalentAreaGeneralSect = EquivalentAreaGeneralSect.create_default(enUnitSystem.SI),
#                            rebar: GeneralRebarPattern = GeneralRebarPattern.create_default(enUnitSystem.SI),
#                            force: MemberForce = MemberForce.create_default(enUnitSystem.SI),
#                            length: BucklingLength = BucklingLength.create_default(enUnitSystem.SI),
#                            eff_len: EffectiveLengthFactor = EffectiveLengthFactor()) -> dict:
#     dll = load_dll()
#     json_data_list = [matl.model_dump_json(), sect.model_dump_json(), eff_area.model_dump_json(), rebar.model_dump_json(), force.model_dump_json(), length.model_dump_json(), eff_len.model_dump_json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
#     jsondata = call_func(dll, 'Calc_EC2_GeneralColumn', json_data_list)
#     dict = json.loads(jsondata)
#     print(dict)


# if __name__ == "__main__":
#     res = report_ec2_generalcolumn()
#     print(res)