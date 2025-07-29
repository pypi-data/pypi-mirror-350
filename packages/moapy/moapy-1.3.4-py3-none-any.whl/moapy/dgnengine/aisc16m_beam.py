import ctypes
import base64
import json
from moapy.auto_convert import auto_schema
from moapy.data_pre import SectionForce, enUnitSystem
from moapy.data_post import ResultBytes
from moapy.steel_pre import SteelMaterial, SteelSectionAISC16SI, SteelOptions
from moapy.enum_pre import en_H_AISC16_SI, enum_to_list, enSteelMaterial_ASTM
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary

@auto_schema(
    title="AISC-LRFD16(SI) Beam Design",
    description="Steel column that is subjected to axial force, biaxial bending moment and shear force and steel beam that is subjected to the bending moment are designed. Automatic design or code check for load resistance capacity of cross-sections like H-beam depending on the form of member is conducted.",
    std_type="AISC LRFD",
    design_code="AISC-LRFD16(SI)"
)
def report_aisc16si_beam_column(matl: SteelMaterial = SteelMaterial.create_default(code="ASTM09(S)", enum_list=enum_to_list(enSteelMaterial_ASTM)),
                                sect: SteelSectionAISC16SI = SteelSectionAISC16SI.create_default(name="W1000X272", enum_list=enum_to_list(en_H_AISC16_SI)),
                                load: SectionForce = SectionForce.create_default(enUnitSystem.SI),
                                opt: SteelOptions = SteelOptions.create_default(enUnitSystem.SI)) -> ResultBytes:
    dll = load_dll()
    eff_len = opt.eff_len
    factor = opt.factor
    length = opt.length
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), load.model_dump_json(), length.model_dump_json(), eff_len.model_dump_json(), factor.model_dump_json()]
    file_path = call_func(dll, 'Report_AISC16SI_BeamColumn', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_aisc16si_beam_column(matl: SteelMaterial = SteelMaterial.create_default(code="ASTM09(S)", enum_list=enum_to_list(enSteelMaterial_ASTM)),
                              sect: SteelSectionAISC16SI = SteelSectionAISC16SI.create_default(name="W1000X272", enum_list=enum_to_list(en_H_AISC16_SI)),
                              load: SectionForce = SectionForce.create_default(enUnitSystem.SI),
                              opt: SteelOptions = SteelOptions.create_default(enUnitSystem.SI)) -> dict:
    dll = load_dll()
    eff_len = opt.eff_len
    factor = opt.factor
    length = opt.length
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), load.model_dump_json(), length.model_dump_json(), eff_len.model_dump_json(), factor.model_dump_json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_AISC16SI_BeamColumn', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


if __name__ == "__main__":
    res = report_aisc16si_beam_column()
    print(res)
    # load = SectionForce.create_default(enUnitSystem.SI)
    # load.Fz.value = 500
    # load.Mx.value = 600
    # load.My.value = 700
    # load.Vx.value = 300
    # load.Vy.value = 900
    # res = report_aisc16si_beam_column(matl = SteelMaterial.create_default(code="ASTM09(S)", enum_list=enum_to_list(enSteelMaterial_ASTM)),
    #                                     sect = SteelSectionAISC10SI.create_default(name="W1000X272", enum_list=enum_to_list(en_H_AISC10_SI)),
    #                                     length = SteelLength.create_default(enUnitSystem.SI),
    #                                     eff_len = EffectiveLengthFactor(),
    #                                     factor = SteelMomentModificationFactorLTB(),
    #                                     load = load)
    # print(res)