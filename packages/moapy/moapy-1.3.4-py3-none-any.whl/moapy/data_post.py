import json
from pydantic import Field, ConfigDict
from moapy.auto_convert import MBaseModel
from moapy.data_pre import Force, Lcom, Area, Length, Inertia, Volume, UnitPropertyMixin
from moapy.enum_pre import enUnitLength, enUnitArea, enUnitSystem, enUnitVolume, enUnitInertia

class ResultMD(MBaseModel):
    """
    Result Markdown
    """
    md: str = Field(default="", description="Markdown")

    model_config = ConfigDict(title="Markdown")

class ResultBytes(MBaseModel):
    """
    Result Bytes
    """
    type: str = Field(default="xlsx", description="Type")
    result: str = Field(default="", description="have to base64 to binary data")

    model_config = ConfigDict(title="Bytes")
                
class Mesh3DPM(MBaseModel):
    """
    3D P-M onion mesh result class

    Args:
        mesh3dpm (list[Force]): onion mesh result
    """
    mesh3dpm : list[Force] = Field(default=[], description="onion mesh result")

    model_config = ConfigDict(title="3DPM onion mesh result")

class Result3DPM(MBaseModel):
    """
    GSD 3DPM result class
    
    Args:
        meshes (Mesh3DPM): 3DPM onion result
        lcbs (list[Lcom]): Load combination
        strength (list[Lcom]): Strength result
    """
    meshes: Mesh3DPM = Field(default=Mesh3DPM(), description="3DPM onion result")
    lcbs: list[Lcom] = Field(default=[], description="Load combination")
    strength: list[Lcom] = Field(default=[], description="Strength result")

    model_config = ConfigDict(title="3DPM Result")

class SectionProperty(MBaseModel):
    """
    Section Property
    """
    area: Area = Field(default_factory=Area, description="the cross-section area")
    asy: Area = Field(default_factory=Area, description="y-dir. the cross-section centroidal axis shear area")
    asz: Area = Field(default_factory=Area, description="z-dir. the cross-section centroidal axis shear area")
    ixx: Inertia = Field(default_factory=Inertia, description="x-dir. Torsional Resistance")
    iyy: Inertia = Field(default_factory=Inertia, description="y-dir. Moment of Inertia")
    izz: Inertia = Field(default_factory=Inertia, description="z-dir. Moment of Inertia")
    cyp: Length = Field(default_factory=Length, description="(+)y-dir. Neutral Axis")
    cym: Length = Field(default_factory=Length, description="(-)y-dir. Neutral Axis")
    czp: Length = Field(default_factory=Length, description="(+)z-dir. Neutral Axis")
    czm: Length = Field(default_factory=Length, description="(-)z-dir. Neutral Axis")
    qyb: Area = Field(default_factory=Area, description="y-dir. Shear Factor for Shear Stress")
    qzb: Area = Field(default_factory=Area, description="z-dir. Shear Factor for Shear Stress")
    periO: Length = Field(default_factory=Length, description="Outer Perimeter")
    periI: Length = Field(default_factory=Length, description="Inner Perimeter")
    syp: Volume = Field(default_factory=Volume, description="(+)y-dir. the cross-section centroidal elastic section moduli")
    sym: Volume = Field(default_factory=Volume, description="(-)y-dir. the cross-section centroidal elastic section moduli")
    szp: Volume = Field(default_factory=Volume, description="(+)z-dir. the cross-section centroidal elastic section moduli")
    szm: Volume = Field(default_factory=Volume, description="(-)z-dir. the cross-section centroidal elastic section moduli")
    ipyy: Inertia = Field(default_factory=Inertia, description="y-dir. the cross-section principal second moments of area")
    ipzz: Inertia = Field(default_factory=Inertia, description="z-dir. the cross-section principal second moments of area")
    zy: Volume = Field(default_factory=Volume, description="y-dir. the cross-section centroidal plastic section moduli")
    zz: Volume = Field(default_factory=Volume, description="z-dir. the cross-section centroidal plastic section moduli")
    ry: Length = Field(default_factory=Length, description="y-dir. the cross-section centroidal radii of gyration")
    rz: Length = Field(default_factory=Length, description="z-dir. the cross-section centroidal radii of gyration")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(area=Area(unit=enUnitArea.IN2), asy=Area(unit=enUnitArea.IN2), asz=Area(unit=enUnitArea.IN2), ixx=Inertia(unit=enUnitInertia.IN4), iyy=Inertia(unit=enUnitInertia.IN4), izz=Inertia(unit=enUnitInertia.IN4),
                       cyp=Length(unit=enUnitLength.IN), cym=Length(unit=enUnitLength.IN), czp=Length(unit=enUnitLength.IN), czm=Length(unit=enUnitLength.IN),
                       qyb=Area(unit=enUnitArea.IN2), qzb=Area(unit=enUnitArea.IN2), periO=Length(unit=enUnitLength.IN), periI=Length(unit=enUnitLength.IN),
                       syp=Volume(unit=enUnitVolume.IN3), sym=Volume(unit=enUnitVolume.IN3), szp=Volume(unit=enUnitVolume.IN3), szm=Volume(unit=enUnitVolume.IN3),
                       ipyy=Inertia(unit=enUnitInertia.IN4), ipzz=Inertia(unit=enUnitInertia.IN4), zy=Volume(unit=enUnitVolume.IN3), zz=Volume(unit=enUnitVolume.IN3),
                       ry=Length(unit=enUnitLength.IN), rz=Length(unit=enUnitLength.IN))
        else:
            return cls(area=Area(unit=enUnitArea.MM2), asy=Area(unit=enUnitArea.MM2), asz=Area(unit=enUnitArea.MM2), ixx=Inertia(unit=enUnitInertia.MM4), iyy=Inertia(unit=enUnitInertia.MM4), izz=Inertia(unit=enUnitInertia.MM4),
                       cyp=Length(unit=enUnitLength.MM), cym=Length(unit=enUnitLength.MM), czp=Length(unit=enUnitLength.MM), czm=Length(unit=enUnitLength.MM),
                       qyb=Area(unit=enUnitArea.MM2), qzb=Area(unit=enUnitArea.MM2), periO=Length(unit=enUnitLength.MM), periI=Length(unit=enUnitLength.MM),
                       syp=Volume(unit=enUnitVolume.MM3), sym=Volume(unit=enUnitVolume.MM3), szp=Volume(unit=enUnitVolume.MM3), szm=Volume(unit=enUnitVolume.MM3),
                       ipyy=Inertia(unit=enUnitInertia.MM4), ipzz=Inertia(unit=enUnitInertia.MM4), zy=Volume(unit=enUnitVolume.MM3), zz=Volume(unit=enUnitVolume.MM3),
                       ry=Length(unit=enUnitLength.MM), rz=Length(unit=enUnitLength.MM))

    def update_property(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if isinstance(value, (int, float)):  # 값만 전달된 경우
                    attr.update_value(value)
                elif isinstance(value, UnitPropertyMixin):  # 전체 객체 전달된 경우
                    setattr(self, key, value)

    # Model configuration using ConfigDict
    model_config = ConfigDict(title="Section Property")

    def dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        result = {}

        for field, value in base_dict.items():
            # Get the field's description
            description = getattr(self.model_fields[field], "description", None)

            # Check if the field is already a dictionary with 'value' and 'unit'
            if isinstance(value, dict) and "value" in value and "unit" in value:
                # Add the description to the dictionary
                result[field] = {
                    "value": value["value"],
                    "unit": value["unit"],
                    "description": description
                }
            else:
                result[field] = value

        return result

# 플레이 그라운드에서 result 확인하기 위한 함수
def print_result_data(result):
    # Get the type of the result as a string
    result_type = f"{type(result).__module__}.{type(result).__qualname__}"

    # Check if result is a subclass of MBaseModel
    if issubclass(type(result), MBaseModel):
        data = result.dict()
    else:
        data = str(result)

    # Format the data for printing
    data = {
        "json": {
            result_type: data
        }
    }
    json_data = json.dumps(data)
    # Print the final data
    print(json_data)
    return json_data
