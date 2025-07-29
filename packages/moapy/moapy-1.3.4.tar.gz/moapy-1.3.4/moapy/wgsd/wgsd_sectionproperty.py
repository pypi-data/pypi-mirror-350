import requests
from urllib.parse import quote
from moapy.api_url import API_SECTION_DATABASE
from pydantic import Field, ConfigDict
from typing import List, Tuple, Annotated, Union
from sectionproperties.analysis.section import Section
from sectionproperties.pre.geometry import Polygon, Geometry, CompoundGeometry
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.enum_pre import enUnitLength, enUnitSystem
from moapy.data_post import SectionProperty
from moapy.mdreporter import ReportUtil
from moapy.data_pre import (
    Point, Points, OuterPolygon, SectionShapeL, SectionShapeC, SectionShapeT, SectionShapeH, SectionRectangle, SectionShapeBox, SectionShapePipe,
    Area, Length, Inertia, Volume, UnitPropertyMixin
)
from shapely.validation import explain_validity
from shapely.geometry import Point as shapely_point
from enum import Enum

InputSectionProperty = Annotated[
    Union[
        SectionShapeL,
        SectionShapeC,
        SectionShapeH,
        SectionRectangle,
        SectionShapeT,
        SectionShapeBox,
        SectionShapePipe,
    ],
    Field(default=SectionShapeH(), title="Section Input", discriminator="section_type"),
]

class enMeshDensity(Enum):
    coarse = "Coarse"
    standard = "Standard"
    fine = "Fine"
    very_fine = "Very Fine"

class SectionDBInfo(MBaseModel):
    standard: str = Field(default="", description="Standard name")
    section_name: str = Field(default="", description="Section name")

class SectionPropertyInput(MBaseModel):
    db_info: SectionDBInfo = Field(default_factory=SectionDBInfo, description="Section DB Info")
    input: InputSectionProperty
    mesh_density: enMeshDensity = Field(default=enMeshDensity.standard, description="Mesh Density")

class SectionCentroid(MBaseModel):
    """
    Section Centroid
    """
    elasticx: Length = Field(default=0.0, description="x-dir. Elastic Centroid")
    elasticy: Length = Field(default=0.0, description="y-dir. Elastic Centroid")
    shearx: Length = Field(default=0.0, description="x-dir. Shear Centroid")
    sheary: Length = Field(default=0.0, description="y-dir. Shear Centroid")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(elasticx=Length(unit=enUnitLength.IN), elasticy=Length(unit=enUnitLength.IN), shearx=Length(unit=enUnitLength.IN), sheary=Length(unit=enUnitLength.IN))
        else:
            return cls(elasticx=Length(unit=enUnitLength.MM), elasticy=Length(unit=enUnitLength.MM), shearx=Length(unit=enUnitLength.MM), sheary=Length(unit=enUnitLength.MM))

    def update_property(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if isinstance(value, (int, float)):  # 값만 전달된 경우
                    attr.update_value(value)
                elif isinstance(value, UnitPropertyMixin):  # 전체 객체 전달된 경우
                    setattr(self, key, value)

    model_config = ConfigDict(title="Section Centroid")

class SectionPropertyResult(MBaseModel):
    """
    Section Property Result
    """
    section_property: SectionProperty = Field(default_factory=SectionProperty, description="Section Property")
    section_centroid: SectionCentroid = Field(default_factory=SectionCentroid, description="Section Centroid")

    vertices: List[tuple[float, float]] = Field(default_factory=list, description="Mesh Vertices of the polygon")
    triangles: List[Tuple[int, int, int]] = Field(default_factory=list, description="Mesh Triangles of the polygon")

    model_config = ConfigDict(title="Section Property Result")

    def dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        result = {}

        # Handle section_property field with nested descriptions
        if hasattr(self.section_property, "dict"):
            result["section_property"] = self.section_property.dict(**kwargs)

        # Handle section_centroid field with nested descriptions
        if hasattr(self.section_centroid, "dict"):
            result["section_centroid"] = self.section_centroid.dict(**kwargs)

        # Merge the base dictionary with the detailed field outputs
        return {**base_dict, **result}

@auto_schema(title="Input Polygon", description="Input Polygon")
def input_polygon(points: Points) -> OuterPolygon:
    return OuterPolygon(outerPolygon=points.points)

def convert_points_to_tuple(points: list[Point]) -> Tuple[Tuple[float, float], ...]:
    return tuple((point.x.value, point.y.value) for point in points)

@auto_schema(title="Calculate Section Property", description="Calculate Section Property")
def calc_sectprop(polygon: OuterPolygon) -> SectionProperty:
    polygon = Polygon(convert_points_to_tuple(polygon.points))
    geom = Geometry(polygon)
    geom.create_mesh(mesh_sizes=100.0)
    section = Section(geom)
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()
    res = section.calculate_stress(n=0.0, vx=1.0, vy=1.0)
    qyb = max(res.material_groups[0].stress_result.sig_zy_vy) * section.get_ic()[0]
    qzb = max(res.material_groups[0].stress_result.sig_zx_vx) * section.get_ic()[1]
    cx = section.get_c()[0]
    cy = section.get_c()[1]
    return SectionProperty(area=Area(value=section.get_area()), asy=Area(value=section.get_as()[0]), asz=Area(value=section.get_as()[1]), ixx=Inertia(value=section.get_j()), iyy=Inertia(value=section.get_ic()[0]), izz=Inertia(value=section.get_ic()[1]),
                           cyp=Length(value=polygon.bounds[2] - cx), cym=Length(value=cx - polygon.bounds[0]),
                           czp=Length(value=polygon.bounds[3] - cy), czm=Length(value=cy - polygon.bounds[1]),
                           syp=Volume(value=section.get_z()[0]), sym=Volume(value=section.get_z()[1]), szp=Volume(value=section.get_z()[2]), szm=Volume(value=section.get_z()[3]),
                           ipyy=Inertia(value=section.get_ip()[0]), ipzz=Inertia(value=section.get_ip()[1]), zy=Volume(value=section.get_s()[0]), zz=Volume(value=section.get_s()[1]), ry=Length(value=section.get_rc()[0]), rz=Length(value=section.get_rc()[1]),
                           qyb=Area(value=qyb), qzb=Area(value=qzb), periO=Length(value=section.get_perimeter())
                           )

def get_minimum_distance(coords):
    """
    Calculate the minimum distance between consecutive points in a polygon.

    Parameters:
    coords (list): List of coordinate tuples (x, y).

    Returns:
    float: Minimum distance between consecutive points.
    """
    min_distance = float('inf')
    
    for i in range(len(coords) - 1):
        p1 = coords[i]
        p2 = coords[i + 1]
        
        # Ensure p1 and p2 are tuples
        if not isinstance(p1, tuple):
            p1 = tuple(p1)
        if not isinstance(p2, tuple):
            p2 = tuple(p2)

        # Calculate distance
        distance = shapely_point(p1).distance(shapely_point(p2))
        min_distance = min(min_distance, distance)
    
    return min_distance

def validate_geometry_for_mesh(geom: Geometry):
    """
    Enhanced validation for geometry to ensure mesh generation compatibility.

    Parameters:
    geom: Geometry object (Polygon or similar)

    Returns:
    dict: Validation result containing 'is_valid', 'errors', and 'warnings'.
    """
    result = {
        "is_valid": True,
        "errors": [],
        "warnings": []
    }

    # Check if the geometry is valid
    validity_check = explain_validity(geom.geom)
    if validity_check != "Valid Geometry":
        result["is_valid"] = False
        result["errors"].append(f"Invalid geometry: {validity_check}")

    # Check if the polygon is self-intersecting
    if not geom.geom.is_valid or geom.geom.is_simple is False:
        result["is_valid"] = False
        result["errors"].append("Geometry contains self-intersections.")

    # Check if the area is positive
    if geom.geom.area <= 0:
        result["is_valid"] = False
        result["errors"].append("Geometry area must be positive.")

    # Remove duplicate points and check collinearity
    unique_points = list(set(geom.geom.exterior.coords))
    if len(unique_points) < 3:
        result["is_valid"] = False
        result["errors"].append("Polygon must have at least three unique, non-collinear points.")

    # Check for inner and outer polygon consistency
    if hasattr(geom, "inner") and geom.inner and not geom.outer.contains(geom.inner):
        result["is_valid"] = False
        result["errors"].append("Inner geometry must be fully contained within the outer geometry.")

    # Check relative areas of inner and outer polygons
    if hasattr(geom, "inner") and geom.inner:
        if geom.inner.area / geom.outer.area > 0.95:  # Adjust threshold as needed
            result["is_valid"] = False
            result["errors"].append("Inner polygon is too close in area to the outer polygon.")

    return result

def do_section_properties_from_api(base_url, codes, types, sect_name):
    # Construct the API URL
    encoded_codes = quote(codes, safe='')
    encoded_types = quote(types, safe='')
    encoded_sect_name = quote(sect_name, safe='')

    # API URL 생성
    api_url = f"{base_url}codes/{encoded_codes}/types/{encoded_types}/names/{encoded_sect_name}"
 
    
    # Make the API request
    response = requests.get(api_url)
    
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        
        # Extract 'sectionProperty' and 'sectionCentroid' data
        section_property = data.get("sectionProperty", [])
        
        # Return the extracted data
        return {
            "sectionProperty": section_property
        }
    else:
        # Raise an exception for a failed request
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

@auto_schema(title="Typical Section Property", description="Typical Section Property")
def calc_sectionproperties_typical(sect: SectionPropertyInput) -> SectionPropertyResult:
    # DB단면인경우 API를 통해 결과 가져온다.
    if sect.db_info.section_name != "":
        response = do_section_properties_from_api(API_SECTION_DATABASE, sect.db_info.standard, sect.input.section_type, sect.db_info.section_name)
        unitsystem = sect.input.get_unitsystem()
        _section_property = SectionProperty.create_default(unitsystem)
        _section_centroid = SectionCentroid.create_default(unitsystem)
        _section_property.area.value = response["sectionProperty"]["area"]
        _section_property.asy.value = response["sectionProperty"]["asy"]
        _section_property.asz.value = response["sectionProperty"]["asz"]
        _section_property.ixx.value = response["sectionProperty"]["ixx"]
        _section_property.iyy.value = response["sectionProperty"]["iyy"]
        _section_property.izz.value = response["sectionProperty"]["izz"]
        _section_property.cyp.value = response["sectionProperty"]["cyp"]
        _section_property.cym.value = response["sectionProperty"]["cym"]
        _section_property.czp.value = response["sectionProperty"]["czp"]
        _section_property.czm.value = response["sectionProperty"]["czm"]
        _section_property.syp.value = response["sectionProperty"]["syp"]
        _section_property.sym.value = response["sectionProperty"]["sym"]
        _section_property.szp.value = response["sectionProperty"]["szp"]
        _section_property.szm.value = response["sectionProperty"]["szm"]
        _section_property.ipyy.value = response["sectionProperty"]["ipyy"]
        _section_property.ipzz.value = response["sectionProperty"]["ipzz"]
        _section_property.zy.value = response["sectionProperty"]["zy"]
        _section_property.zz.value = response["sectionProperty"]["zz"]
        _section_property.ry.value = response["sectionProperty"]["ry"]
        _section_property.rz.value = response["sectionProperty"]["rz"]
        _section_property.qyb.value = response["sectionProperty"]["qyb"]
        _section_property.qzb.value = response["sectionProperty"]["qzb"]
        _section_property.periO.value = response["sectionProperty"]["perio"]
        _section_property.periI.value = response["sectionProperty"]["perii"]
        _section_centroid.elasticx.value = response["sectionProperty"]["elasticx"]
        _section_centroid.elasticy.value = response["sectionProperty"]["elasticy"]
        _section_centroid.shearx.value = response["sectionProperty"]["shearx"]
        _section_centroid.sheary.value = response["sectionProperty"]["sheary"]
        return SectionPropertyResult(section_property=_section_property, section_centroid=_section_centroid)

    points = sect.input.do_convert_point()
    unitsystem = sect.input.get_unitsystem()
    periInner = 0.0
    if len(points) == 2:
        polygon = Polygon(points[0])
        outer = Geometry(geom=polygon)
        inpolygon = Polygon(points[1])
        inner = Geometry(geom=inpolygon).align_center(align_to=outer)
        geom = outer - inner
        periInner = inpolygon.length
    else:
        polygon = Polygon(points)
        geom = Geometry(polygon)

    checkdata = validate_geometry_for_mesh(geom)
    if checkdata["is_valid"] == False:
        return SectionPropertyResult(section_property=SectionProperty(), section_centroid=SectionCentroid())

    x_coords = [point[0] for point in geom.control_points]
    y_coords = [point[1] for point in geom.control_points]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2

    # 세로 중심선에서 분리
    g1, g2 = geom.split_section(point_i=(x_center, y_min), vector=(0, 1))
    geom = CompoundGeometry(geoms=g1 + g2)

    # 가로 중심선에서 분리
    g1, g2 = geom.split_section(point_i=(x_min, y_center), vector=(1, 0))
    geom = CompoundGeometry(geoms=g1 + g2)

    coarse_mesh = False
    mesh_size = polygon.area / 100
    if sect.mesh_density == enMeshDensity.coarse:
        coarse_mesh = True
    elif sect.mesh_density == enMeshDensity.standard:
        mesh_size = polygon.area / 100
    elif sect.mesh_density == enMeshDensity.fine:
        mesh_size = polygon.area / 200
    elif sect.mesh_density == enMeshDensity.very_fine:
        mesh_size = polygon.area / 400

    # 3. 분리된 Geometry의 영역별 메시 크기 설정 및 메시 생성
    mesh_sizes = [mesh_size, mesh_size, mesh_size, mesh_size]  # 각 영역별 메시 크기
    geom.create_mesh(mesh_sizes=mesh_sizes, coarse=coarse_mesh)
    section = Section(geom)
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()
    x_c, y_c = section.get_c()
    x_s, y_s = section.get_sc()
    cyp = polygon.bounds[2] - x_c
    cym = x_c - polygon.bounds[0]
    czp = polygon.bounds[3] - y_c
    czm = y_c - polygon.bounds[1]
    qyb, qzb = sect.input.calculate_qb_values(cym, czm)
    section_property = SectionProperty.create_default(unitsystem)
    section_property.update_property(area=section.get_area(), asy=section.get_as()[0], asz=section.get_as()[1], ixx=section.get_j(), iyy=section.get_ic()[0], izz=section.get_ic()[1],
                                     cyp=cyp, cym=cym,
                                     czp=czp, czm=czm,
                                     syp=section.get_z()[0], sym=section.get_z()[1], szp=section.get_z()[2], szm=section.get_z()[3],
                                     ipyy=section.get_ip()[0], ipzz=section.get_ip()[1], zy=section.get_s()[0], zz=section.get_s()[1], ry=section.get_rc()[0], rz=section.get_rc()[1],
                                     qyb=qyb, qzb=qzb, periO=section.get_perimeter(), periI=periInner)
    section_centroid = SectionCentroid.create_default(unitsystem)
    section_centroid.update_property(elasticx=x_c, elasticy=y_c, shearx=x_s, sheary=y_s)
    return SectionPropertyResult(section_property=section_property, section_centroid=section_centroid, vertices=geom.mesh['vertices'], triangles=geom.mesh['triangles'][:, :3])

@auto_schema(title="Report Section Property", description="Report Section Property")
def report_sectprop(sectprop: SectionProperty) -> str:
    rpt = ReportUtil("sectprop.md", "*Section Properties*")
    rpt.add_line_fvu("A_{rea}", sectprop.area.value, sectprop.area.unit)
    rpt.add_line_fvu("A_{sy}", sectprop.asy.value, sectprop.asy.unit)
    rpt.add_line_fvu("A_{sz}", sectprop.asz.value, sectprop.asz.unit)
    rpt.add_line_fvu("I_{xx}", sectprop.ixx.value, sectprop.ixx.unit)
    rpt.add_line_fvu("I_{yy}", sectprop.iyy.value, sectprop.iyy.unit) 
    rpt.add_line_fvu("I_{zz}", sectprop.izz.value, sectprop.izz.unit)
    rpt.add_line_fvu("C_y", sectprop.cyp.value, sectprop.cyp.unit)
    rpt.add_line_fvu("C_z", sectprop.czp.value, sectprop.czp.unit)
    rpt.add_line_fvu("S_{yp}", sectprop.syp.value, sectprop.syp.unit)
    rpt.add_line_fvu("S_{ym}", sectprop.sym.value, sectprop.sym.unit)
    rpt.add_line_fvu("S_{zp}", sectprop.szp.value, sectprop.szp.unit)
    rpt.add_line_fvu("S_{zm}", sectprop.szm.value, sectprop.szm.unit)
    rpt.add_line_fvu("I_{pyy}", sectprop.ipyy.value, sectprop.ipyy.unit)
    rpt.add_line_fvu("I_{pzz}", sectprop.ipzz.value, sectprop.ipzz.unit)
    rpt.add_line_fvu("Z_y", sectprop.zy.value, sectprop.zy.unit)
    rpt.add_line_fvu("Z_z", sectprop.zz.value, sectprop.zz.unit)
    rpt.add_line_fvu("r_y", sectprop.ry.value, sectprop.ry.unit)
    rpt.add_line_fvu("r_z", sectprop.rz.value, sectprop.rz.unit)
    return rpt.get_md_text()


if __name__ == "__main__":
    data2 = {
        "sect": {
            "input": {
            "sectionType": "Channel",
            "h": {
                "value": 10,
                "unit": "in"
            },
            "b1": {
                "value": 2.6,
                "unit": "in"
            },
            "tw": {
                "value": 0.24,
                "unit": "in"
            },
            "tf1": {
                "value": 0.436,
                "unit": "in"
            },
            "b2": {
                "value": 2.6,
                "unit": "in"
            },
            "tf2": {
                "value": 0.436,
                "unit": "in"
            },
            "r1": {
                "value": 0.23,
                "unit": "in"
            },
            "r2": {
                "value": 0.12,
                "unit": "in"
            }
            }
        }
        }
    data = { "sect" : {
        "input": {
            "sectionType": "Solid_Rectangle",
            "h": {
            "value": 10,
            "unit": "mm"
            },
            "b": {
            "value": 10,
            "unit": "mm"
            }
        }
        }
    }
    data3 = {
        "sect" : {
        "input": {
            "sectionType": "H_Section",
            "h": {
            "value": 600,
            "unit": "mm"
            },
            "b1": {
            "value": 190,
            "unit": "mm"
            },
            "tw": {
            "value": 10,
            "unit": "mm"
            },
            "tf1": {
            "value": 30,
            "unit": "mm"
            },
            "b2": {
            "value": 190,
            "unit": "mm"
            },
            "tf2": {
            "value": 30,
            "unit": "mm"
            },
            "r1": {
            "value": 30,
            "unit": "mm"
            },
            "r2": {
            "value": 30,
            "unit": "mm"
            }
        }
        }
    }
    data4 = {
    "sect": {
        "input": {
        "sectionType": "Angle",
        "h": {
            "value": 200,
            "unit": "mm"
        },
        "b": {
            "value": 200,
            "unit": "mm"
        },
        "tw": {
            "value": 20,
            "unit": "mm"
        },
        "tf": {
            "value": 20,
            "unit": "mm"
        }
        },
        "meshDensity": "Fine",
        "dbInfo": {
        "standard": "AISC10(US)",
        "sectionName": "L2X2X1/4"
        }
    }
    }
    res = calc_sectionproperties_typical(**{
  "sect": {
    "dbInfo": {
      "standard": "",
      "sectionName": ""
    },
    "input": {
      "sectionType": "H_Section",
      "b1": {
        "unit": "mm",
        "value": 300
      },
      "b2": {
        "unit": "mm",
        "value": 300
      },
      "h": {
        "unit": "mm",
        "value": 300
      },
      "tw": {
        "unit": "mm",
        "value": 10
      },
      "tf1": {
        "unit": "mm",
        "value": 10
      },
      "tf2": {
        "unit": "mm",
        "value": 10
      },
      "r1": {
        "unit": "mm",
        "value": 0
      },
      "r2": {
        "unit": "mm",
        "value": 0
      }
    },
    "meshDensity": "Standard"
  }
})
    print(res.dict())
    print(res.section_property.qyb.value, res.section_property.qzb.value)