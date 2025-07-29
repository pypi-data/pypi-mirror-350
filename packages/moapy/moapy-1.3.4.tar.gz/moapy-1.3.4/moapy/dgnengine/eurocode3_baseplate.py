import ctypes
import json
import base64
from moapy.auto_convert import auto_schema
from moapy.data_post import ResultBytes
from moapy.data_pre import SectionForce, Stress, Length
from moapy.steel_pre import AnchorBolt, BasePlateMaterials, BasePlateSection, SteelMaterial, SteelSection, BasePlateLayout, BoltMaterial
from moapy.enum_pre import enum_to_list, en_H_EN10365, enSteelMaterial_EN10025, enBoltMaterialEC, enUnitStress, enUnitLength, enBoltName, enUnitSystem
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary
from pydantic import Field, ConfigDict
from moapy.steel_pre import BasePlateSectionConcrete, BasePlateSectionGrout, BasePlateSectionWing, BasePlateSectionRib
from typing import List
from moapy.auto_convert import auto_schema, MBaseModel

class WeldingSection(MBaseModel):
    """
    Welding Section
    """
    thick: Length = Field(default_factory=Length, title="Throat Thickness", description="Throat Thickness")
    len_x: Length = Field(default_factory=Length, title="Effective Length(x)", description="Effective Length(x)")    
    len_y: Length = Field(default_factory=Length, title="Effective Length(y)", description="Effective Length(y)")
    len_t: Length = Field(default_factory=Length, title="Effective Length(Tension)", description="Effective Length(Tension)")

    model_config = ConfigDict(
        title="Welding",
        json_schema_extra={
            "description": "Welding Throat Thickness and Effective Length"
        }
    )

    @classmethod
    def create_default(cls):
        return cls(thick=Length(value=0, unit=enUnitLength.MM), len_x=Length(value=10, unit=enUnitLength.MM), len_y=Length(value=10, unit=enUnitLength.MM), len_t=Length(value=10, unit=enUnitLength.MM))

class BasePlateSectionEC(MBaseModel):
    """
    Base Plate Section
    """
    steel: SteelSection = Field(default_factory=SteelSection, title="Steel Beam", description="Steel section profile used for the baseplate component. This parameter defines the geometric properties and structural characteristics of the baseplate section.")
    conc: BasePlateSectionConcrete = Field(default_factory=BasePlateSectionConcrete, title="Base Plate", description="Geometric specifications for the baseplate section, including width, height, thickness, and grout thickness. These dimensions are essential for the design and construction of baseplate connections in steel structures.")
    wing: BasePlateSectionWing = Field(default_factory=BasePlateSectionWing, title="Wing Plate", description="Wing Thickness and Height")
    rib: BasePlateSectionRib = Field(default_factory=BasePlateSectionRib, title="Rib Plate", description="Rib Thickness and Height")
    weld: WeldingSection = Field(default_factory=WeldingSection, title="Welding", description="Welding Throat Thickness and Effective Length")

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "Geometric specifications for the baseplate section, including width, height, thickness, and grout thickness. These dimensions are essential for the design and construction of baseplate connections in steel structures."
        }
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str], title: str = "", description: str = ""):
        return cls(steel=SteelSection.create_default(name=name, enum_list=enum_list, title=title, description=description), conc=BasePlateSectionConcrete.create_default(unit_system=enUnitSystem.SI),
                   wing=BasePlateSectionWing.create_default(unit_system=enUnitSystem.SI), rib=BasePlateSectionRib.create_default(unit_system=enUnitSystem.SI), weld=WeldingSection.create_default())

class DesignParameter(MBaseModel):
    """
    Design Parameter
    """
    method: str = Field(default="Finite Element Method", title="Design Method", description="Design Method", enum=["Equivalent T-stub Method", "Finite Element Method"])
    factor: float = Field(default_factory=float, title="Bearing Resistance Factor", description="Bearing Resistance Factor")

    model_config = ConfigDict(
        title="Design Parameter",
        json_schema_extra={
            "description": "Design parameters for baseplate design, including design method."
        }
    )

    @classmethod
    def create_default(cls):
        return cls(method="Finite Element Method", factor=1.0)
            
@auto_schema(
    title="Eurocode 3 Base Plate Design",
    description=( 
        "The Eurocode 3 (EN 1993-1-8) standard for base plate design ensures the stability and safety of steel structures "
        "by analyzing and verifying key design factors for the connection between the base plate and anchor bolts. "
        "This design process involves assessing the performance of the base plate under various load conditions to ensure "
        "that the loads are securely transferred to the supporting foundation.\n\n"
        
        "- Verification of Bearing and Shear Capacities: Evaluates whether the load is safely transferred through the plate "
        "and bolts, assessing bearing strength based on the material and thickness of the plate.\n"
        
        "- Design for Compression and Shear Forces: Calculates the resistance to applied vertical and horizontal loads to "
        "maintain structural stability.\n"
        
        "- Check for Bolt Group Effects and Slip Resistance: Assesses the effects of bolt groups and slip resistance under "
        "concentrated loads to ensure compliance with design requirements.\n"
        
        "- Consideration of Ductility and Stability: Ensures that the base plate provides the necessary flexibility and "
        "stability to distribute loads safely.\n\n"
        
        "This functionality provides detailed design results and recommendations for each connection scenario, offering "
        "structural engineers reliable guidance in making design decisions."
    ),
    std_type="EUROCODE",
    design_code="EN1993-1-1:2005"
)
def report_ec3_baseplate(matl: BasePlateMaterials = BasePlateMaterials.create_default(unit_system=enUnitSystem.SI, bolt_name=enBoltMaterialEC.Class48, bolt_enum_list=enum_to_list(enBoltMaterialEC),
                                                                                      code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025)),
                         sect: BasePlateSectionEC = BasePlateSectionEC.create_default(name="HE 200 A", enum_list=enum_to_list(en_H_EN10365)),
                         force: SectionForce = SectionForce.create_default(enUnitSystem.SI),
                         layout: BasePlateLayout = BasePlateLayout.create_default(unit_system=enUnitSystem.SI, name=enBoltName.M16, enum_list=enum_to_list(enBoltName)),
                         opt: DesignParameter = DesignParameter.create_default()) -> ResultBytes:
    dll = load_dll()
    anchor = layout.anchor
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), force.model_dump_json(), anchor.model_dump_json(), opt.model_dump_json()]
    file_path = call_func(dll, 'Report_EC3_BasePlate', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec3_baseplate(matl: BasePlateMaterials = BasePlateMaterials.create_default(unit_system=enUnitSystem.SI, bolt_name=enBoltMaterialEC.Class48, bolt_enum_list=enum_to_list(enBoltMaterialEC),
                                                                                    code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025)),
                       sect: BasePlateSectionEC = BasePlateSectionEC.create_default(name="HE 200 A", enum_list=enum_to_list(en_H_EN10365)),
                       force: SectionForce = SectionForce.create_default(enUnitSystem.SI),
                       layout: BasePlateLayout = BasePlateLayout.create_default(unit_system=enUnitSystem.SI, name=enBoltName.M16, enum_list=enum_to_list(enBoltName)),
                       opt: DesignParameter = DesignParameter.create_default()) -> ResultBytes:
    dll = load_dll()
    anchor = layout.anchor
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), force.model_dump_json(), anchor.model_dump_json(), opt.model_dump_json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC3_BasePlate', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


if __name__ == "__main__":
    data = {
  "matl": {
    "conc": {
      "fck": {
        "value": 24,
        "unit": "MPa"
      }
    },
    "matl": {
      "code": "EN10025",
      "name": "S275"
    },
    "bolt": {
      "boltName": "4.6"
    },
    "ribWing": {
      "code": "EN10025",
      "name": "S275"
    }
  },
  "sect": {
    "steel": {
      "shape": "H",
      "name": "HE 200 A"
    },
    "conc": {
      "width": {
        "value": 390,
        "unit": "mm"
      },
      "height": {
        "value": 400,
        "unit": "mm"
      },
      "thk": {
        "value": 6,
        "unit": "mm"
      }
    },
    "wing": {
      "thick": {
        "value": "12",
        "unit": "mm"
      },
      "height": {
        "value": 100,
        "unit": "mm"
      }
    },
    "rib": {
      "thick": {
        "value": "12",
        "unit": "mm"
      },
      "sect": {
        "col": {
          "height": {
            "value": "100",
            "unit": "mm"
          },
          "length": {
            "value": "20",
            "unit": "mm"
          }
        },
        "bp": {
          "height": {
            "value": "10",
            "unit": "mm"
          },
          "length": {
            "value": "30",
            "unit": "mm"
          }
        }
      },
      "numX": 1,
      "numY": 1
    },
    "weld": {
      "thick": {
        "value": "6",
        "unit": "mm"
      },
      "lenX": {
        "value": 10,
        "unit": "mm"
      },
      "lenY": {
        "value": 10,
        "unit": "mm"
      },
      "lenT": {
        "value": 10,
        "unit": "mm"
      }
    }
  },
  "force": {
    "dirX": {
      "axial": {
        "value": "100",
        "unit": "kN"
      },
      "bending": {
        "value": "50",
        "unit": "kN.m"
      },
      "shear": {
        "value": "70",
        "unit": "kN"
      }
    },
    "dirY": {
      "axial": {
        "value": 0,
        "unit": "kN"
      },
      "bending": {
        "value": "60",
        "unit": "kN.m"
      },
      "shear": {
        "value": "80",
        "unit": "kN"
      }
    }
  },
  "layout": {
    "anchor": {
      "type": "Cast-In-Place",
      "boltName": "M20",
      "length": 5,
      "layout": {
        "dirX": {
          "dist": {
            "value": "75",
            "unit": "mm"
          },
          "no": 2
        },
        "dirY": {
          "dist": {
            "value": "75",
            "unit": "mm"
          },
          "no": 2
        }
      }
    }
  },
  "opt": {
    "method": "Finite Element Method",
    "factor": 1
  }
}
    res = report_ec3_baseplate(**data)
    print(res)