import ctypes
import json
import base64
from moapy.auto_convert import auto_schema
from moapy.data_pre import SectionRectangle, NativeForce
from moapy.rc_pre import BeamRebarPattern, MaterialNative
from moapy.dgnengine.base import load_dll, call_func, read_file_as_binary
from moapy.data_post import ResultBytes
from moapy.enum_pre import enUnitSystem, enum_to_list, enRebar_UNI

@auto_schema(
    title="Eurocode 2 Beam Design",
    description="Eurocode 2 provides a comprehensive review of reinforced concrete (RC) beam design with a focus on strength assessment, available in Excel format.",
    std_type="EUROCODE",
    design_code="EN1992-1-1:2004"
)
def report_ec2_beam(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                    sect: SectionRectangle = SectionRectangle.create_default(enUnitSystem.SI),
                    force: NativeForce = NativeForce.create_default(enUnitSystem.SI),
                    rebar: BeamRebarPattern = BeamRebarPattern.create_default("P26", "P10", enum_to_list(enRebar_UNI), enUnitSystem.SI)
                    ) -> ResultBytes:
    dll = load_dll()
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), rebar.model_dump_json(), force.model_dump_json()]
    file_path = call_func(dll, 'Report_EC2_Beam', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec2_beam(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                  sect: SectionRectangle = SectionRectangle.create_default(enUnitSystem.SI),
                  force: NativeForce = NativeForce.create_default(enUnitSystem.SI),
                  rebar: BeamRebarPattern = BeamRebarPattern.create_default("P26", "P10", enum_to_list(enRebar_UNI), enUnitSystem.SI)
                  ) -> dict:
    dll = load_dll()
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), rebar.model_dump_json(), force.model_dump_json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC2_Beam', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


if __name__ == "__main__":
    res = report_ec2_beam()
    print(res)