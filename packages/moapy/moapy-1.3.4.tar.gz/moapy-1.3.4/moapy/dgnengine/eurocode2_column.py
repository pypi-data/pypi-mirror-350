import ctypes
import json
import base64
from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import SectionRectangle, BucklingLength, ColumnMemberForce, EffectiveLengthFactor
from moapy.rc_pre import MaterialNative, ColumnRebarPattern
from moapy.enum_pre import enUnitSystem
from moapy.dgnengine.base import load_dll, call_func, read_file_as_binary
from moapy.data_post import ResultBytes


class DesignParameter(MBaseModel):
    """
    Design Parameters for column design.
    """
    length: BucklingLength = Field(default_factory=BucklingLength, title="Buckling Length", description="Buckling length for column design.")
    eff_len: EffectiveLengthFactor = Field(default_factory=EffectiveLengthFactor, title="Effective Length Factor", description="Effective length factor for column design.")

    model_config = ConfigDict(
        title="Design Parameter",
        json_schema_extra={
            "description": "Design Parameters for column design."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        return cls(length=BucklingLength.create_default(unit_system), eff_len=EffectiveLengthFactor())

@auto_schema(
    title="Eurocode 2 Column Design",
    description="Eurocode 2 provides a comprehensive review of reinforced concrete (RC) column design with a focus on strength assessment, available in Excel format.",
    std_type="EUROCODE",
    design_code="EN1992-1-1:2004"
)
def report_ec2_column(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                      sect: SectionRectangle = SectionRectangle.create_default(enUnitSystem.SI),
                      force: ColumnMemberForce = ColumnMemberForce.create_default(enUnitSystem.SI),
                      rebar: ColumnRebarPattern = ColumnRebarPattern.create_default(enUnitSystem.SI),
                      option: DesignParameter = DesignParameter.create_default(enUnitSystem.SI)) -> ResultBytes:
    dll = load_dll()
    eff_len = option.eff_len
    length = option.length
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), rebar.model_dump_json(), force.model_dump_json(), length.model_dump_json(), eff_len.model_dump_json()]
    file_path = call_func(dll, 'Report_EC2_Column', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec2_column(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                    sect: SectionRectangle = SectionRectangle.create_default(enUnitSystem.SI),
                    force: ColumnMemberForce = ColumnMemberForce.create_default(enUnitSystem.SI),
                    rebar: ColumnRebarPattern = ColumnRebarPattern.create_default(enUnitSystem.SI),
                    option: DesignParameter = DesignParameter.create_default(enUnitSystem.SI)) -> dict:
    dll = load_dll()
    eff_len = option.eff_len
    length = option.length
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), rebar.model_dump_json(), force.model_dump_json(), length.model_dump_json(), eff_len.model_dump_json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC2_Column', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


if __name__ == "__main__":
    res = report_ec2_column()
    print(res)