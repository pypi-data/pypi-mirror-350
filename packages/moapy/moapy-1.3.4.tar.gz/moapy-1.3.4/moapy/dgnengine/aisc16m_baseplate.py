import ctypes
import json
import base64
from moapy.auto_convert import auto_schema
from moapy.data_post import ResultBytes
from moapy.data_pre import SectionForce
from moapy.steel_pre import (
    BasePlateMaterials, BasePlateSection, BasePlateStrengthReductionFactor, BasePlateLayoutUS
)
from moapy.enum_pre import enum_to_list, enUnitSystem, enBoltName, enSteelMaterial_ASTM, en_H_AISC16_SI, enBoltMaterialASTM, enStudBoltName
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary



@auto_schema(
    title="AISC-LRFD16(SI) Base Plate Design",
    description=(
        "The AISC-LRFD16(SI) standard outlines the requirements for designing base plates that connect steel columns "
        "to foundations, emphasizing both safety and efficiency. The design process incorporates key considerations "
        "such as material properties, load conditions, and connection integrity. The analyses included are:\n\n"
        "- Verification of bearing and shear capacities based on material, thickness, and concrete contact\n"
        "- Design for axial, shear, and bending forces to maintain structural integrity\n"
        "- Analysis of bolt group effects and anchor design, ensuring resistance without excessive deformation\n"
        "- Incorporation of ductility and stability to accommodate misalignments and differential movements\n"
        "- Concrete bearing and punching checks to prevent failure or excessive cracking\n\n"
        "The AISC approach integrates these factors into a unified design methodology, providing engineers with reliable "
        "tools and recommendations for designing safe and effective base plate connections."
    ),
    std_type="AISC LRFD",
    design_code="AISC-LRFD16(SI)"
)
def report_aisc16m_baseplate(matl: BasePlateMaterials = BasePlateMaterials.create_default(unit_system=enUnitSystem.SI, bolt_name=enBoltMaterialASTM.A193_B7, bolt_enum_list=enum_to_list(enBoltMaterialASTM), code="ASTM", enum_list=enum_to_list(enSteelMaterial_ASTM)),
                             sect: BasePlateSection = BasePlateSection.create_default(unit_system=enUnitSystem.SI, name="W250X58", enum_list=enum_to_list(en_H_AISC16_SI)),
                             force: SectionForce = SectionForce.create_default(enUnitSystem.SI),
                             layout: BasePlateLayoutUS = BasePlateLayoutUS.create_default(unit_system=enUnitSystem.SI, name=enStudBoltName.M22, enum_list=enum_to_list(enStudBoltName)),
                             opt: BasePlateStrengthReductionFactor = BasePlateStrengthReductionFactor()) -> ResultBytes:
    dll = load_dll()
    anchor = layout.anchor
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), force.model_dump_json(), anchor.model_dump_json(), opt.model_dump_json()]
    file_path = call_func(dll, 'Report_AISC16M_BasePlate', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_aisc16m_baseplate(matl: BasePlateMaterials = BasePlateMaterials.create_default(unit_system=enUnitSystem.SI, bolt_name=enBoltMaterialASTM.A193_B7, bolt_enum_list=enum_to_list(enBoltMaterialASTM), code="ASTM", enum_list=enum_to_list(enSteelMaterial_ASTM)), 
                           sect: BasePlateSection = BasePlateSection.create_default(unit_system=enUnitSystem.SI, name="W250X58", enum_list=enum_to_list(en_H_AISC16_SI)),
                           force: SectionForce = SectionForce.create_default(enUnitSystem.SI),
                           layout: BasePlateLayoutUS = BasePlateLayoutUS.create_default(unit_system=enUnitSystem.SI, name=enStudBoltName.M22, enum_list=enum_to_list(enStudBoltName)),
                           opt: BasePlateStrengthReductionFactor = BasePlateStrengthReductionFactor()) -> dict:
    dll = load_dll()
    anchor = layout.anchor
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), force.model_dump_json(), anchor.model_dump_json(), opt.model_dump_json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_AISC16M_BasePlate', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


if __name__ == "__main__":
    res = report_aisc16m_baseplate()
    print(res)