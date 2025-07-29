import requests
import json
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.wgsd.wgsd_sectionproperty import SectionProperty
from pydantic import Field
from typing import Union
from sectionproperties.analysis.section import Section
from sectionproperties.pre.geometry import Polygon, Geometry

url = "https://moa.rpm.kr-dv-midasit.com/backend/function-executor/vertices-execute"

class SectShape_H(MBaseModel):
    """Section Shape H

    Args:
        H (float): H
        B1 (float): B1
        tw (float): tw
        tf1 (float): tf1
        B2 (float): B2
        tf2 (float): tf2
        r1 (float): r1
        r2 (float): r2
    """
    h: float = Field(default=300.0, description="H")
    b1: float = Field(default=300.0, description="B1")
    tw: float = Field(default=10.0, description="tw")
    tf1: float = Field(default=10.0, description="tf1")
    b2: float = Field(default=300.0, description="B2")
    tf2: float = Field(default=10.0, description="tf2")
    r1: float = Field(default=0.0, description="r1")
    r2: float = Field(default=0.0, description="r2")

class SectShape_SolidRectangle(MBaseModel):
    """Section Shape Solid Rectangle

    Args:
        B (float): B
        H (float): H
    """
    b: float = Field(default=300.0, description="B")
    h: float = Field(default=300.0, description="H")

def calc_sectprop(polygon: Polygon) -> SectionProperty:
    geom = Geometry(polygon)
    geom.create_mesh(mesh_sizes=10.0)

    section = Section(geom)
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()
    return SectionProperty(Area=section.get_area(), Asy=section.get_as()[0], Asz=section.get_as()[1], Ixx=section.get_j(), Iyy=section.get_ic()[0], Izz=section.get_ic()[1],
                           Cy=section.get_c()[0], Cz=section.get_c()[1], Syp=section.get_z()[0], Sym=section.get_z()[1], Szp=section.get_z()[2], Szm=section.get_z()[3],
                           Ipyy=section.get_ip()[0], Ipzz=section.get_ip()[1], Zy=section.get_s()[0], Zz=section.get_s()[1], ry=section.get_rc()[0], rz=section.get_rc()[1]
                           )

@auto_schema(title="Typical Section Property", description="Typical Section Property")
def calc_typicalsection_prop(shape: Union[SectShape_H, SectShape_SolidRectangle]) -> SectionProperty:
    """calc_typicalsection_prop

    Args:
        shape (Union[SectShape_H, SectShape_SolidRectangle]): Section Shape

    Returns:
        SectionProperty: Section Property
    """
    if isinstance(shape, SectShape_H):
        body = {
            "type": "HSection",
            "properties": shape.dict(),
        }
    elif isinstance(shape, SectShape_SolidRectangle):
        body = {
            "type": "SRSection",
            "properties": shape.dict(),
        }
    else:
        return SectionProperty(Area=1000.0, Asy=100.0, Asz=100.0, Ixx=100.0, Iyy=100.0, Izz=100.0, Cy=100.0, Cz=100.0, Syp=100.0, Sym=100.0, Szp=100.0, Szm=100.0, Ipyy=100.0, Ipzz=100.0, Zy=100.0, Zz=100.0, ry=100.0, rz=100.0)

    response = requests.post(url, json=body)
    data = json.loads(response.text)
    coordinates = data[0]
    tuple_coordinates = Polygon([(point["x"], point["y"]) for point in coordinates])
    res = calc_sectprop(tuple_coordinates)
    return res

# res = calc_typicalsection_prop(SectShape_H())
# print(res)