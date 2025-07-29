import base64
from moapy.auto_convert import auto_schema
from moapy.data_pre import SectionForce
from moapy.steel_pre import SteelSectionAISC05US, SteelLength
from moapy.alu_pre import AluMaterial, AluminumOptions
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary
from moapy.data_post import ResultBytes
from moapy.enum_pre import enUnitSystem, en_H_AISC05_US, enum_to_list

@auto_schema(
    title="AA-LRFD05(US) Aluminum Beam Design",
    description=(
        "This functionality performs the design and verification of aluminum beam members "
        "in accordance with the AA-LRFD05(US) standard. The design process incorporates key "
        "parameters such as cross-sectional properties, material characteristics, and load "
        "combinations. The analyses included are:\n\n"
        "- Verification of cross-sectional strength and stability\n"
        "- Design for bending moments, shear forces, and axial forces\n"
        "- Check for local buckling and overall stability\n"
        "- Application of safety factors and load combinations\n\n"
        "The functionality provides detailed design results, including assessments and "
        "recommendations for each design scenario."
    ),
    std_type="AA.ADM",
    design_code="AA-LRFD05(US)"
)
def report_aa_lrfd05_beam(matl: AluMaterial = AluMaterial(), sect: SteelSectionAISC05US = SteelSectionAISC05US.create_default(name="W40X183", enum_list=enum_to_list(en_H_AISC05_US)),
                          load: SectionForce = SectionForce.create_default(enUnitSystem.US), option: AluminumOptions = AluminumOptions.create_default(enUnitSystem.US)) -> ResultBytes:
    dll = load_dll()
    eff_len = option.eff_len
    factor = option.factor
    length = option.length
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), load.model_dump_json(), length.model_dump_json(), eff_len.model_dump_json(), factor.model_dump_json()]
    file_path = call_func(dll, 'Report_AA_LRFD05_Beam', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

if __name__ == "__main__":
    res = report_aa_lrfd05_beam(**{
  "matl": {
    "code": "AA(A)",
    "matl": "2014-T6",
    "product": "Extrusions"
  },
  "sect": {
    "shape": "H",
    "name": "W40X183"
  },
  "load": {
    "dirX": {
      "axial": {
        "unit": "kip",
        "value": 0
      },
      "bending": {
        "unit": "kip.ft",
        "value": 0
      },
      "shear": {
        "unit": "kip",
        "value": 0
      }
    },
    "dirY": {
      "axial": {
        "unit": "kip",
        "value": 0
      },
      "bending": {
        "unit": "kip.ft",
        "value": 0
      },
      "shear": {
        "unit": "kip",
        "value": 0
      }
    }
  },
  "option": {
    "length": {
      "lB": {
        "unit": "in",
        "value": 15
      },
      "lX": {
        "unit": "in",
        "value": 15
      },
      "lY": {
        "unit": "in",
        "value": 15
      }
    },
    "effLen": {
      "kx": 1,
      "ky": 1
    },
    "factor": {
      "cMx": 1,
      "cMy": 1,
      "cb": 1,
      "m": 0.67
    }
  }
})
    print(res)