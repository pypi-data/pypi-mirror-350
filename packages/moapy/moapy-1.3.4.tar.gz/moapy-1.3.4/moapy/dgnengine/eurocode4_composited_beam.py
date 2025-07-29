import ctypes
import json
import base64
from typing import List
from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import UnitLoads, Length, Stress
from moapy.rc_pre import CompositedParam
from moapy.steel_pre import ShearConnector_EC, SteelSection, SteelMaterial
from moapy.dgnengine.base import load_dll, call_func, read_file_as_binary
from moapy.data_post import ResultBytes
from moapy.enum_pre import enUnitSystem, enum_to_list, en_H_EN10365, enSteelMaterial_EN10025, enUnitLength, enUnitStress

class CompositedParameter(MBaseModel):
    leng: CompositedParam = Field(default_factory=CompositedParam, title="Girder", description="Length of the girder in meters, representing the span of the composite beam.")

    model_config = ConfigDict(
        title="Design Parameter",
        json_schema_extra={
            "description": "Defines the design parameters for the composite beam, including the length of the girder."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        return cls(leng=CompositedParam.create_default(unit_system))

class CompositedSlab(MBaseModel):
    shape: str = Field(default="T-Shape", title="Slab Shape", description="Shape of the slab", enum=["T-Shape", "Half T-Shape"])
    thickness: Length = Field(default_factory=Length, title="Slab Thickness", description="Thickness of the slab in millimeters, representing the depth of the concrete slab section.")

    model_config = ConfigDict(
        title="Slab",
        json_schema_extra={
            "description": "Defines the cross-sectional properties of the composite beam, including the steel girder and concrete slab."
        }
    )
    
    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(shape="T-Shape", thickness=Length(value=6, unit=enUnitLength.IN))
        else:
            return cls(shape="T-Shape", thickness=Length(value=150, unit=enUnitLength.MM))

class CompositedGirderSpacing(MBaseModel):
    shape: str = Field(
        default='H',
        title="Section Shape",
        description="Structural steel section profile type (e.g., H-shape, T-shape, Channel, Angle). This parameter defines the fundamental cross-sectional geometry of the steel member.",
        readOnly=True
    )

    name: str = Field(
        default=None,
        title="Section Name",
        description="Standardized designation of the steel section based on industry specifications. This identifier corresponds to specific dimensional and structural properties in the steel section database.",
        enum=[]
    )

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "Database specifications for structural steel sections including section shape and standardized member designations. This configuration provides essential cross-sectional properties for structural steel design and analysis."
        }
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str], title: str = "", description: str = ""):
        """
        Creates an instance of SteelSection with a specific enum list and dynamic description for the name field.
        """
        section = cls()
        # Dynamically set the enum for the name field
        section.model_fields['name'].json_schema_extra['enum'] = enum_list
        section.model_fields['name'].json_schema_extra['default'] = name
        # Set default name if enum_list is provided
        section.name = name       
        # Change description dynamically
        if title:
            cls.model_config["title"] = title
        if description:
            cls.model_config["description"] = description
        return section

class CompositedSect(MBaseModel):
    slab: CompositedSlab = Field(default_factory=CompositedSlab, title="Slab", description="Defines the concrete slab properties used in the composite beam, including the thickness of the slab.")
    girder: CompositedGirderSpacing = Field(default_factory=CompositedGirderSpacing, title="Girder", description="Defines the steel girder properties used in the composite beam, including the spacing of the girder.")

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "Defines the cross-sectional properties of the composite beam, including the steel girder and concrete slab."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        return cls(slab=CompositedSlab.create_default(unit_system),
                   girder=CompositedGirderSpacing.create_default(name="IPE 400", enum_list=enum_to_list(en_H_EN10365), description="EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."))

class SlabMaterial(MBaseModel):
    conc: Stress = Field(default_factory=Stress, title="Concrete Strength (fck)", description="Compressive strength of the concrete in MPa, representing its ability to resist axial load.")

    model_config = ConfigDict(
        title="Slab Material",
        json_schema_extra={
            "description": "Defines the material properties of the concrete slab."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        return cls(conc=Stress(value=24.0, unit=enUnitStress.MPa))

class RebarMaterial(MBaseModel):
    prop: Stress = Field(default_factory=Stress, title="Rebar Strength (fsk)", description="Yield strength of the rebar in MPa")

    model_config = ConfigDict(
        title="Rebar Material",
        json_schema_extra={
            "description": "Defines the material properties of the rebar."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        return cls(prop=Stress(value=400.0, unit=enUnitStress.MPa))


class CompositedMaterial(MBaseModel):
    girder: SteelMaterial = Field(default_factory=SteelMaterial, title="Girder", description="Defines the steel girder properties used in the composite beam, including the material properties.")
    slab: SlabMaterial = Field(default_factory=SlabMaterial, title="Slab", description="Defines the concrete slab properties used in the composite beam, including the material properties.")
    rebar: RebarMaterial = Field(default_factory=RebarMaterial, title="Rebar", description="Defines the rebar properties used in the composite beam, including the material properties.")
    shear_conn: SteelMaterial = Field(default_factory=SteelMaterial, title="Shear Connector", description="Defines the shear connector properties used in the composite beam, including the material properties.")

    model_config = ConfigDict(
        title="Material",
        json_schema_extra={
            "description": "Defines the material properties of the composite beam, including the steel girder and concrete slab."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        return cls(girder=SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025), description="EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type."),
                   slab=SlabMaterial.create_default(unit_system),
                   rebar=RebarMaterial.create_default(unit_system),
                   shear_conn=SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025), description="EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type."))

@auto_schema(
    title="Eurocode 4 Steel Composite Beam Design",
    description="Composite beam that resists bending moment by integrally connecting to reinforced concrete slab and steel beam supporting it by shear connector is designed. Depending on the data that  is entered by users, results of deflection checking, shear connector estimation and Heel drop vibration checking as well as design stress checking applied to each part of composite beam and is automatically calculated.",
    std_type="EUROCODE",
    design_code="EN1994-1-1:2005"
)
def report_ec4_composited_beam(matl: CompositedMaterial = CompositedMaterial.create_default(enUnitSystem.SI),
                               sect: CompositedSect = CompositedSect.create_default(enUnitSystem.SI),
                               load: UnitLoads = UnitLoads.create_default(enUnitSystem.SI),
                               shear_conn: ShearConnector_EC = ShearConnector_EC.create_default(enUnitSystem.SI),
                               param: CompositedParameter = CompositedParameter.create_default(enUnitSystem.SI)) -> ResultBytes:
    dll = load_dll()
    leng = param.leng
    json_data_list = [sect.model_dump_json(), matl.model_dump_json(), shear_conn.model_dump_json(), leng.model_dump_json(), load.model_dump_json()]
    file_path = call_func(dll, 'Report_EC4_CompositedBeam', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec4_composited_beam(matl: CompositedMaterial = CompositedMaterial.create_default(enUnitSystem.SI),
                             sect: CompositedSect = CompositedSect.create_default(enUnitSystem.SI),
                             load: UnitLoads = UnitLoads.create_default(enUnitSystem.SI),
                             shear_conn: ShearConnector_EC = ShearConnector_EC.create_default(enUnitSystem.SI),
                             param: CompositedParameter = CompositedParameter.create_default(enUnitSystem.SI)) -> dict:
    dll = load_dll()
    leng = param.leng
    json_data_list = [sect.model_dump_json(), matl.model_dump_json(), shear_conn.model_dump_json(), leng.model_dump_json(), load.model_dump_json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC4_CompositedBeam', json_data_list)
    dict = json.loads(jsondata)
    print(dict)

def save_result_to_json(result: ResultBytes, file_name: str) -> None:
    """ResultBytes 객체를 JSON 파일로 저장"""
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(result.dict(), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    res = report_ec4_composited_beam()
    print(res)
    # steel = SteelMember(
    #     sect=SteelSection.create_default(name="IPE 400", enum_list=enum_to_list(en_H_EN10365), description="EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."),
    #     matl=SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025), description="EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type.")
    # )
    # shear_conn = ShearConnector_EC()
    # slab = SlabMember_EC()
    # leng = GirderLength.create_default(enUnitSystem.SI)
    # load = UnitLoads.create_default(enUnitSystem.SI)
    # load.construction.value = 1
    # load.live.value = 5
    # load.finish.value = 3
    # res = report_ec4_composited_beam(steel=steel, shear_conn=shear_conn, slab=slab, leng=leng, load=load)
    # print(res)