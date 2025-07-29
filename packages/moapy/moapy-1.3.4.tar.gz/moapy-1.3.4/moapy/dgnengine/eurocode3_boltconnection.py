import ctypes
import json
import base64
from typing import List
from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_post import ResultBytes
from moapy.steel_pre import SteelConnectMember, SteelMember, SteelSection, SteelMaterial, SteelPlateMember_EC, ConnectType, SteelBolt_EC, Welding_EC, SteelBoltConnectionForce, BoltMaterial_EC
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary
from moapy.enum_pre import enum_to_list, en_H_EN10365, enSteelMaterial_EN10025, enUnitPercentage, enUnitLength, enBoltName, enConnectionType
from moapy.data_pre import Percentage, Length

class BoltConnectBeamMaterial(MBaseModel):
    supporting_beam: str = Field(default_factory=str, title="Supporting Beam Material", description="Name of the steel material. The material name is selected from a list of available materials.", enum=[])
    supported_beam: str = Field(default_factory=str, title="Supported Beam Material", description="Name of the steel material. The material name is selected from a list of available materials.", enum=[])

class BoltConnectPlateMaterial(MBaseModel):
    plate: str = Field(default_factory=str, title="Plate Material", description="Name of the steel material. The material name is selected from a list of available materials.", enum=[])

class BoltConnectBoltMaterial(MBaseModel):
    bolt: str = Field(default_factory=str, title="Bolt Material", description="Name of the bolt material. The material name is selected from a list of available materials.", enum=[])

class BoltConnectWeldMaterial(MBaseModel):
    weld: str = Field(default_factory=str, title="Weld Material", description="Name of the weld material. The material name is selected from a list of available materials.", enum=[])

class BoltConnectMaterial(MBaseModel):
    code: str = Field(default="EN10025", title="Material Code", readOnly=True, description="The material code for the steel used in the bolt connection, which determines the mechanical properties and performance of the material.")
    steel_beam: BoltConnectBeamMaterial = Field(default_factory=BoltConnectBeamMaterial, title="Steel Beam", description="Defines the material properties used in the bolt connection, including the supporting and supported beams.")
    plate_material: BoltConnectPlateMaterial = Field(default_factory=BoltConnectPlateMaterial, title="Plate", description="Defines the material properties used in the bolt connection, including the plate material.")
    bolt_material: BoltMaterial_EC = Field(default_factory=BoltMaterial_EC, title="Bolt", description="Defines the material properties used in the bolt connection, including the bolt material.")
    weld_material: BoltConnectWeldMaterial = Field(default_factory=BoltConnectWeldMaterial, title="Weld", description="Defines the material properties used in the bolt connection, including the weld material.")

    model_config = ConfigDict(
        title="Material",
        json_schema_extra={
            "description": "Defines the material properties used in the bolt connection, including the steel sections, plates, bolts, and welds."
        }
    )

    @classmethod
    def create_default(cls, code: str, name: str, enum_list: List[str]):
        material = cls()
        material.code = code

        material.steel_beam.model_fields['supporting_beam'].json_schema_extra['enum'] = enum_list
        material.steel_beam.model_fields['supporting_beam'].json_schema_extra['default'] = name
        material.steel_beam.supporting_beam = name

        material.steel_beam.model_fields['supported_beam'].json_schema_extra['enum'] = enum_list
        material.steel_beam.model_fields['supported_beam'].json_schema_extra['default'] = name
        material.steel_beam.supported_beam = name

        material.plate_material.model_fields['plate'].json_schema_extra['enum'] = enum_list
        material.plate_material.model_fields['plate'].json_schema_extra['default'] = name
        material.plate_material.plate = name

        # material.bolt_material.model_fields['bolt'].json_schema_extra['enum'] = enum_list
        # material.bolt_material.model_fields['bolt'].json_schema_extra['default'] = name
        # material.bolt_material.bolt = name

        material.weld_material.model_fields['weld'].json_schema_extra['enum'] = enum_list
        material.weld_material.model_fields['weld'].json_schema_extra['default'] = name
        material.weld_material.weld = name
        return material

class BoltConnectBeam(MBaseModel):
    supporting_beam: str = Field(default_factory=str, title="Supporting Member Section", description="Name of the steel section. The section name is selected from a list of available sections.", enum=[])
    supported_beam: str = Field(default_factory=str, title="Supported Member Section", description="Name of the steel section. The section name is selected from a list of available sections.", enum=[])

class BoltConnectPlate(MBaseModel):
    plate_thick: Length = Field(default=Length(value=6.0, unit=enUnitLength.MM), title="Plate Thickness", description="The thickness of the plate in millimeters, which affects the strength and stability of the connection.")

class BoltConnectWeld(MBaseModel):
    weld_length: Length = Field(default=Length(value=6.0, unit=enUnitLength.MM), title="Weld Leg Length", description="The leg length of the weld, which affects its strength and capacity")

class BoltConnectLevelGap(MBaseModel):
    level: Length = Field(default=Length(value=0.0, unit=enUnitLength.MM), title="Diffrence of Level", description="The difference in level between the supporting and supported beams.")
    gap: Length = Field(default=Length(value=0.0, unit=enUnitLength.MM), title="Gap", description="The gap between the supporting and supported beams.")    

class BoltConnectSection(MBaseModel):
    beam: BoltConnectBeam = Field(default_factory=BoltConnectBeam, title="Steel Beam", description="Defines the beam properties used in the bolt connection, including the supporting and supported beams.")
    plate: BoltConnectPlate = Field(default_factory=BoltConnectPlate, title="Plate", description="Defines the plate properties used in the bolt connection, including the plate thickness.")
    weld: BoltConnectWeld = Field(default_factory=BoltConnectWeld, title="Weld", description="Defines the weld properties used in the bolt connection, including the weld leg length.")
    level_gap: BoltConnectLevelGap = Field(default_factory=BoltConnectLevelGap, title="Level/Gap", description="Defines the level gap properties used in the bolt connection, including the level and gap.")

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "Defines the cross-sectional properties used in the bolt connection, including the steel sections and plate."
        }
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str]):
        section = cls()
        section.beam.model_fields['supporting_beam'].json_schema_extra['enum'] = enum_list
        section.beam.model_fields['supporting_beam'].json_schema_extra['default'] = name
        section.beam.supporting_beam = name

        section.beam.model_fields['supported_beam'].json_schema_extra['enum'] = enum_list
        section.beam.model_fields['supported_beam'].json_schema_extra['default'] = name
        section.beam.supported_beam = name

        return section

class BoltConnectLayout(MBaseModel):
    bolt_name: str = Field(default_factory=str, title="Bolt Name", description="Name of the bolt used in the connection. The bolt name is selected from a list of available bolt types.", enum=[])
    bolt_num: int = Field(default=4, title="Number of Bolts", description="The total number of bolts used in the connection, which affects the load distribution and capacity of the connection.")

    model_config = ConfigDict(
        title="Bolt",
        json_schema_extra={
            "description": "Defines the layout properties used in the bolt connection, including the number of bolts."
        }
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str]):
        layout = cls()
        layout.model_fields['bolt_name'].json_schema_extra['enum'] = enum_list
        layout.model_fields['bolt_name'].json_schema_extra['default'] = name
        layout.bolt_name = name
        layout.bolt_num = 4
        return layout

class BoltConnectType(MBaseModel):
    type: str = Field(default="Fin Plate - Beam to Beam", title="Connection Type", description="The type of bolted connection between structural elements", enum=enum_to_list(enConnectionType))

class SupportingPosition(MBaseModel):
    position: str = Field(default="Flange", title="Position", description="The position of the supporting beam", enum=["Flange", "Web"])

class BoltType(MBaseModel):
    type: str = Field(default="Ordinary", title="Bolt Type", description="Bolt type", enum=["Ordinary", "Countersunk"])

class EndFinPlate(MBaseModel):
    depth: str = Field(default="Partial", title="Depth", description="The depth of the end fin plate", enum=["Partial", "Full"])

class DesignParameter(MBaseModel):
    connect_type: BoltConnectType = Field(default_factory=BoltConnectType, title="Connection Type", description="The type of bolted connection between structural elements")
    supporting_position: SupportingPosition = Field(default_factory=SupportingPosition, title="Supporting Member", description="The position of the supporting beam")
    bolt_type: BoltType = Field(default_factory=BoltType, title="Bolt Type", description="Bolt type ")
    end_fin_plate: EndFinPlate = Field(default_factory=EndFinPlate, title="End/Fin Plate", description="End/Fin plate")

    model_config = ConfigDict(
        title="Design Parameter",
        json_schema_extra={
            "description": "Design parameters for the bolt connection, including the connection type and weld leg length."
        }
    )

    @classmethod
    def create_default(cls):
        return cls()

@auto_schema(
    title="Eurocode 3 Steel Bolt Connection Design",
    description=(
        "This functionality performs the design and verification of steel bolt connections "
        "in accordance with Eurocode 3 (EN 1993-1-8). The design process considers key "
        "parameters such as bolt properties, connection geometry, and applied loads, "
        "including the following analyses:\n\n"
        "- Verification of bearing and shear capacities\n"
        "- Design for tensile and shear forces\n"
        "- Check for bolt group effects and slip resistance\n"
        "- Consideration of connection ductility and stability\n\n"
        "The functionality provides detailed design results, including assessments and "
        "recommendations for each connection scenario."
    ),
    std_type="EUROCODE",
    design_code="EN1993-1-1:2005"
)
def report_ec3_bolt_connection(matl: BoltConnectMaterial = BoltConnectMaterial.create_default(code="EN10025", name=enSteelMaterial_EN10025.S275, enum_list=enum_to_list(enSteelMaterial_EN10025)),
                               sect: BoltConnectSection = BoltConnectSection.create_default(name="IPE 400", enum_list=enum_to_list(en_H_EN10365)),
                               force: SteelBoltConnectionForce = SteelBoltConnectionForce(percent=Percentage(value=30, unit=enUnitPercentage.pct)),
                               layout: BoltConnectLayout = BoltConnectLayout.create_default(name="M20", enum_list=enum_to_list(enBoltName)),
                               param: DesignParameter = DesignParameter()) -> ResultBytes:
    dll = load_dll()
    json_data_list = [matl.model_dump_json(), sect.model_dump_json(), layout.model_dump_json(), param.model_dump_json(), force.model_dump_json()]
    file_path = call_func(dll, 'Report_EC3_BoltConnection', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))


if __name__ == "__main__":
    res = report_ec3_bolt_connection()
    print(res)