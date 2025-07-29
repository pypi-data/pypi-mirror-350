import ctypes
import base64
import json
from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import SectionForce, EffectiveLengthFactor
from moapy.data_post import ResultBytes
from moapy.steel_pre import SteelMaterial, SteelSection, SteelLength_Torsion, SteelMomentModificationFactor_EC, InteractionFactorAnnex
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary
from moapy.enum_pre import enum_to_list, enSteelMaterial_EN10025, en_H_EN10365, enUnitSystem

class DesignParameter(MBaseModel):
    """
    Design Parameter for beam design.
    """
    length: SteelLength_Torsion = SteelLength_Torsion.create_default(enUnitSystem.SI)
    eff_len: EffectiveLengthFactor = Field(default_factory=EffectiveLengthFactor, title="Column Design Option", description="Effective length factor for column design.")
    factor: SteelMomentModificationFactor_EC = Field(default_factory=SteelMomentModificationFactor_EC, title="Moment Modification Factor", description="Moment modification factor for beam design.")
    inter_type: InteractionFactorAnnex = Field(default_factory=InteractionFactorAnnex, title="Interaction Factor", description="Interaction factor for beam design.")

    model_config = ConfigDict(
        title="Design Parameter",
        json_schema_extra={
            "description": "Design parameters for beam design, including effective length factor, moment modification factor, and interaction factor."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(length=SteelLength_Torsion.create_default(enUnitSystem.US), eff_len=EffectiveLengthFactor(), factor=SteelMomentModificationFactor_EC(), inter_type=InteractionFactorAnnex())
        else:
            return cls(length=SteelLength_Torsion.create_default(enUnitSystem.SI), eff_len=EffectiveLengthFactor(), factor=SteelMomentModificationFactor_EC(), inter_type=InteractionFactorAnnex())

@auto_schema(
    title="Eurocode 3 Beam Design",
    description="Steel column that is subjected to axial force, biaxial bending moment and shear force and steel beam that is subjected to the bending moment are designed. Automatic design or code check for load resistance capacity of cross-sections like H-beam depending on the form of member is conducted.",
    std_type="EUROCODE",
    design_code="EN1993-1-1:2005"
)
def report_ec3_beam_column(matl: SteelMaterial = SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025), description="EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type."),
                           sect: SteelSection = SteelSection.create_default(name="IPE 400", enum_list=enum_to_list(en_H_EN10365), description="EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."),
                           load: SectionForce = SectionForce.create_default(enUnitSystem.SI),
                           opt: DesignParameter = DesignParameter.create_default(enUnitSystem.SI)) -> ResultBytes:
    dll = load_dll()
    eff_len = opt.eff_len
    factor = opt.factor
    inter_type = opt.inter_type
    length = opt.length
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), load.model_dump_json(), length.model_dump_json(), eff_len.model_dump_json(), factor.model_dump_json(), inter_type.model_dump_json()]
    file_path = call_func(dll, 'Report_EC3_BeamColumn', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec3_beam_column(matl: SteelMaterial = SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025), description="EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type."),
                         sect: SteelSection = SteelSection.create_default(name="IPE 400", enum_list=enum_to_list(en_H_EN10365), description="EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."),
                         load: SectionForce = SectionForce.create_default(enUnitSystem.SI),
                         opt: DesignParameter = DesignParameter.create_default(enUnitSystem.SI)) -> dict:
    dll = load_dll()
    eff_len = opt.eff_len
    factor = opt.factor
    inter_type = opt.inter_type
    length = opt.length
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), load.model_dump_json(), length.model_dump_json(), eff_len.model_dump_json(), factor.model_dump_json(), inter_type.model_dump_json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC3_BeamColumn', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


if __name__ == "__main__":
    res = report_ec3_beam_column()
    print(res)