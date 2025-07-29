import sectionproperties.pre.geometry as geometry
import sectionproperties.pre.pre as pre
import concreteproperties.stress_strain_profile as ssp
import concreteproperties.utils as utils
import concreteproperties.results
import numpy as np
import trimesh

from scipy.spatial import ConvexHull
from shapely import Polygon
from moapy.auto_convert import auto_schema
from abc import ABC, abstractmethod

from concreteproperties.pre import add_bar
from concreteproperties.concrete_section import ConcreteSection
from concreteproperties.prestressed_section import PrestressedSection
from concreteproperties.material import Concrete, SteelBar, SteelStrand
from moapy.data_pre import (
    Points, OuterPolygon, InnerPolygon, Lcb, Lcoms, PMOptions, Force, Lcom, Stress_Strain_Component,
    SectionForce, Moment, enUnitForce, enUnitMoment
)

from moapy.rc_pre import (
    ConcreteGrade, RebarProp, TendonProp, Concrete_General_Properties,
    Concrete_Stress_ULS_Options_ACI, Concrete_SLS_Options, Rebar_General_Properties, Rebar_Stress_ULS_Options_ACI,
    Rebar_Stress_SLS_Options, MaterialConcrete, MaterialRebar, Geometry, Material,
    ConcreteGeometry, RebarGeometry, TendonGeometry
)

from moapy.data_post import Result3DPM, Mesh3DPM

# ==== functions ====
@auto_schema(title="Concrete Coordinate", description="Concrete Coordinate")
def conc_properties_design(
    general: Concrete_General_Properties,
    uls: Concrete_Stress_ULS_Options_ACI,
    sls: Concrete_SLS_Options
) -> MaterialConcrete:
    """
    Return the concrete material properties based on the design code

    Args:
        general: general concrete properties
        uls: concrete stress options for ULS
        sls: concrete stress options for SLS

    return:
        MaterialConcrete: material properties of selected data
    """
    if general is None:
        general = Concrete_General_Properties()
    if uls is None:
        uls = Concrete_Stress_ULS_Options_ACI()
    if sls is None:
        sls = Concrete_SLS_Options()

    if uls.material_model == 'Rectangle':
        _uls_strains = [
            0,
            uls.compressive_failure_strain * (1 - uls.factor_b1),
            uls.compressive_failure_strain * (1 - uls.factor_b1),
            uls.compressive_failure_strain,
        ]
        _uls_stress = [
            0,
            0,
            uls.factor_b1 * general.strength,
            uls.factor_b1 * general.strength,
        ]

    if sls.material_model == 'Linear':
        _sls_strains = [
            0,
            sls.failure_compression_limit,
        ]
        _sls_stress = [
            0,
            general.strength,
        ]

    ss_uls_components = [Stress_Strain_Component(stress=_uls_stress[i], strain=_uls_strains[i]) for i in range(len(_uls_strains))]
    ss_sls_components = [Stress_Strain_Component(stress=_sls_stress[i], strain=_sls_strains[i]) for i in range(len(_sls_strains))]
    return MaterialConcrete(curve_uls=ss_uls_components, curve_sls=ss_sls_components)

@auto_schema(title="Rebar properties", description="Rebar properties")
def rebar_properties_design(
    general: Rebar_General_Properties,
    uls: Rebar_Stress_ULS_Options_ACI,
    sls: Rebar_Stress_SLS_Options
) -> MaterialRebar:
    """
    Return the material properties based on the design code

    Args:
        general: general rebar properties
        uls: rebar stress options for ULS
        sls: rebar stress options for SLS

    return:
        MaterialRebar: material properties of selected data
    """
    yield_strain = general.strength / general.elastic_modulus

    _sls_strains = [
        0,
        yield_strain,
        sls.failure_strain
    ]
    _sls_stress = [
        0,
        general.strength,
        general.strength,
    ]

    _uls_strains = [
        0,
        yield_strain,
        uls.failure_strain
    ]
    _uls_stress = [
        0,
        general.strength,
        general.strength
    ]

    ss_uls_components = [Stress_Strain_Component(stress=_uls_stress[i], strain=_uls_strains[i]) for i in range(len(_uls_strains))]
    ss_sls_components = [Stress_Strain_Component(stress=_sls_stress[i], strain=_sls_strains[i]) for i in range(len(_sls_strains))]

    return MaterialRebar(curve_uls=ss_uls_components, curve_sls=ss_sls_components)

def calculate_elastic_modulus(stresses, strains):
    """
    주어진 철근 응력-변형률 곡선 데이터로부터 탄성계수를 계산하는 함수.

    Parameters:
    - rebar_curve: 철근 응력-변형률 곡선 (리스트 형태의 (변형률, 응력) 쌍)

    Returns:
    - E: 탄성계수 (N/mm²)
    """
    # 선형 구간에서 응력-변형률의 기울기를 계산
    strains = np.array(strains)
    stresses = np.array(stresses)
    
    # 탄성영역에서의 기울기(탄성계수) 계산
    # 일반적으로 초기 구간의 기울기를 사용
    # 예를 들어, 변형률이 0에 가까운 구간에서 계산
    elastic_region_indices = np.where(strains < 0.003)[0]  # 예: 변형률이 0.2% 이하인 부분
    if len(elastic_region_indices) < 2:
        raise ValueError("Not enough data points in the elastic region.")

    # 첫 번째와 두 번째 포인트에서 탄성계수 계산
    E = (stresses[elastic_region_indices[-1]] - stresses[elastic_region_indices[0]]) / \
        (strains[elastic_region_indices[-1]] - strains[elastic_region_indices[0]])
    
    return E

class MSection:
    def __init__(self, matl=Material, geom=Geometry):
        if hasattr(matl, "concrete"):
            self.conc = matl.concrete
            if self.conc is not None:
                self.concrete_material_uls = self.conc.curve_uls
                self.concrete_material_sls = self.conc.curve_sls

        if hasattr(matl, "rebar"):
            self.rebar = matl.rebar
            if self.rebar is not None:
                self.rebar_material_uls = self.rebar.curve_uls
                self.rebar_material_sls = self.rebar.curve_sls

        if hasattr(matl, "tendon"):
            self.tendon = matl.tendon
            if self.tendon is not None:
                self.tendon_material_uls = self.tendon.curve_uls
                self.tendon_material_sls = self.tendon.curve_sls

        self.geom = geom
        if self.geom is not None:
            self.concrete_geom = self.geom.concrete
            if hasattr(self.geom, "rebar"):
                self.rebar_geom = self.geom.rebar

            if hasattr(self.geom, "tendon"):
                self.tendon_geom = self.geom.tendon

    def get_concrete_material_curve(self, type_):
        if type_ == "uls":
            curve_data = self.concrete_material_uls
        elif type_ == "sls":
            curve_data = self.concrete_material_sls

        return [component.stress for component in curve_data], [component.strain for component in curve_data]

    def get_rebar_material_curve(self, type_):
        if type_ == "uls":
            curve_data = self.rebar_material_uls
        elif type_ == "sls":
            curve_data = self.rebar_material_sls

        return [component.stress for component in curve_data], [component.strain for component in curve_data]

    def get_tendon_material_curve(self, type_):
        if type_ == "uls":
            curve_data = self.tendon_material_uls
        elif type_ == "sls":
            curve_data = self.tendon_material_sls

        return [component.stress for component in curve_data], [component.strain for component in curve_data]

    def get_concrete_geom(self):
        return self.concrete_geom

    def get_rebar_geom(self):
        if hasattr(self, 'rebar_geom'):
            return self.rebar_geom
        return None

    def get_tendon_geom(self):
        # if hasattr(self, 'tendon_geom'):
        #     if (self.tendon_geom.points is not None) and (len(self.tendon_geom.points) > 0):
        #         return self.tendon_geom

        return None

    def check_data(self):
        if self.conc is None or self.geom is None:
            return "Data is not enough."

        return True

    def compound_section(
        self,
        concrete: list[dict],
        rebar: list[dict],
        tendon: list[dict],
        conc_mat: pre.Material = pre.DEFAULT_MATERIAL,
        steel_mat: pre.Material = pre.DEFAULT_MATERIAL,
        tendon_mat: pre.Material = pre.DEFAULT_MATERIAL
    ) -> geometry.CompoundGeometry:
        def convert_points_to_list(points):
            return [[point.x.value, point.y.value] for point in points]

        outpolygon = Polygon(convert_points_to_list(concrete.outerPolygon))
        outer = geometry.Geometry(geom=outpolygon, material=conc_mat)
        if (concrete.innerPolygon is not None) and (len(concrete.innerPolygon) > 0):
            inpolygon = Polygon(convert_points_to_list(concrete.innerPolygon))
            inner = geometry.Geometry(geom=inpolygon).align_center(align_to=outer)
            concrete_geometry = outer - inner
        else:
            concrete_geometry = outer

        # cnosider rebar
        if rebar is not None:
            for reb in rebar:
                if reb is not None:
                    area = reb.prop.area.value
                    posi = reb.points
                    trans_pos = convert_points_to_list(posi)

                    for x, y in trans_pos:
                        concrete_geometry = add_bar(
                            geometry=concrete_geometry,
                            area=area,
                            material=steel_mat,
                            x=x,
                            y=y,
                            n=4
                        )

        # consider tendon
        if tendon is not None:
            for tend in tendon:
                if tend is not None:
                    t_area = tend.prop.area.value
                    t_posi = tend.points
                    t_trans_pos = convert_points_to_list(t_posi)

                    for x, y in t_trans_pos:
                        concrete_geometry = add_bar(
                            geometry=concrete_geometry,
                            area=t_area,
                            material=tend,
                            x=x,
                            y=y,
                        )

        if isinstance(concrete_geometry, geometry.CompoundGeometry):
            return concrete_geometry
        else:
            raise ValueError("Concrete section generation failed.")

    def has_rebar(self):
        hasRebar = True if self.get_rebar_geom() is not None else False
        return hasRebar

    def calc_compound_section(self):
        ss_uls = self.get_concrete_material_curve("uls")
        ss_sls = self.get_concrete_material_curve("sls")

        max_value = np.max(ss_uls[0])
        indices = np.where(ss_uls[0] == max_value)[0]
        ecu = ss_uls[1][indices[-1]]
        fck = max(ss_uls[0])

        ss_conc_uls = ssp.ConcreteUltimateProfile(stresses=ss_uls[0], strains=ss_uls[1], compressive_strength=fck)
        ss_conc_ser = ssp.ConcreteServiceProfile(stresses=ss_sls[0], strains=ss_sls[1], ultimate_strain=ecu)

        # ss_rebar_uls = ssp.StressStrainProfile(self.get_rebar_material_curve("uls")["Strain"], self.get_rebar_material_curve("uls")["Stress"])
        # ss_rebar_sls = ssp.StressStrainProfile(self.get_rebar_material_curve("sls")["Strain"], self.get_rebar_material_curve("sls")["Stress"])

        concrete_matl = Concrete(
            name="concrete",
            density=2.4e-6,
            stress_strain_profile=ss_conc_ser,
            ultimate_stress_strain_profile=ss_conc_uls,
            flexural_tensile_strength=0.6 * np.sqrt(fck),  # 기준에 따라 다르게 설정
            colour="lightgrey",
        )

        if hasattr(self, 'rebar'):
            rebar_ss_uls = self.get_rebar_material_curve("uls")
            fy = max(rebar_ss_uls[0])
            Es = calculate_elastic_modulus(rebar_ss_uls[0], rebar_ss_uls[1])
            max_value = np.max(rebar_ss_uls[0])
            indices = np.where(rebar_ss_uls[0] == max_value)[0]
            esu = rebar_ss_uls[1][indices[-1]]
            steel_matl = SteelBar(
                name="rebar",
                density=7.85e-6,
                stress_strain_profile=ssp.SteelElasticPlastic(
                    yield_strength=fy,
                    elastic_modulus=Es,
                    fracture_strain=esu,
                ),
                colour="grey",
            )
        else:
            steel_matl = None

        # prestressing stress를 텐던별로 줘야할텐데?
        # if hasattr(self, 'tendon_geom'):
        #     tendon_matl = SteelStrand(
        #         name="1830 MPa Strand",
        #         density=7.85e-6,
        #         stress_strain_profile=ssp.StrandHardening(
        #             yield_strength=1500,
        #             elastic_modulus=200e3,
        #             fracture_strain=0.035,
        #             breaking_strength=1830,
        #         ),
        #         colour="slategrey",
        #         prestress_stress=self.tendon_geom.prop.prestress,
        #     )
        # else:
        tendon_matl = None

        # reference geometry
        compound_sect = self.compound_section(self.get_concrete_geom(), self.get_rebar_geom(), self.get_tendon_geom(), concrete_matl, steel_matl, tendon_matl)
        if self.get_tendon_geom() is not None:
            compSect = PrestressedSection(compound_sect)
        else:
            compSect = ConcreteSection(compound_sect)

        return compSect

class PM3DCurve:
    """
    Class for PM3D Curve Calculation

    Args:
        matl (Material): Material properties
        geom (Geometry): Geometry properties
        opt (PMOptions
    """
    def __init__(self, matl=Material, geom=Geometry, opt=PMOptions):
        self.sect = MSection(matl, geom)
        self.option = opt

    def get_option_by_ecc_pu(self):
        return self.option.by_ecc_pu

    # TODO Tendon 만 있을 경우 Cb값에 대해 처리해줘야되나?
    def get_Cb(self, sect, theta_rad, ecu, esu):
        d_ext, _ = sect.extreme_bar(theta=theta_rad)
        return (ecu / (ecu + esu)) * d_ext

    def calc_compound_section(self):
        return self.sect.calc_compound_section()

    def make_3dpm_data(self):
        # TODO 이 변수들 지걸로 맞춰줘야되!!
        beta1 = 0.8
        ecu = 0.003
        esu = 0.05
        comp_sect = self.calc_compound_section()

        hasRebar = self.sect.has_rebar()

        results = []
        theta_range = np.arange(0.0, 361.0, 15.0).tolist()

        for theta in theta_range:
            theta_rad = np.radians(theta)
            x11_max, x11_min, y22_max, y22_min = utils.calculate_local_extents( 
                geometry=comp_sect.compound_geometry,
                cx=comp_sect.gross_properties.cx,
                cy=comp_sect.gross_properties.cy,
                theta=theta_rad
            )

            C_Max = abs(y22_max - y22_min) / beta1
            d_n_range = np.linspace(0.01, C_Max * 1.1, 10).tolist()  # numpy 배열을 float 리스트로 변환

            if hasRebar is True:
                Cb = self.get_Cb(comp_sect, theta_rad, ecu, esu)
                d_n_range.append(Cb)

            for d_n in d_n_range:
                res = concreteproperties.results.UltimateBendingResults(theta_rad)
                res = comp_sect.calculate_ultimate_section_actions(d_n, res)
                results.append(res)

        return results

class DgnCode(ABC):
    """
    Class for Design Code
    """
    def __init__(self) -> None:
        pass

    @abstractmethod
    def make_3dpm_data(self, material: Material, geometry: Geometry, opt: PMOptions):
        pm = PM3DCurve(material, geometry, opt)
        return pm.make_3dpm_data()

    def get_option_by_ecc_pu(self, opt: PMOptions):
        return opt.by_ecc_pu

    def calc_compound_section(self, material: Material, geometry: Geometry, opt: PMOptions = None):
        if opt is None:
            opt = PMOptions()

        pm = PM3DCurve(material, geometry, opt)
        return pm.calc_compound_section()

class DgnCodeUS(DgnCode):
    """
    Class for Design Code US
    """
    def __init__(self) -> None:
        super().__init__()

    def make_3dpm_data(self, material: Material, geometry: Geometry, opt: PMOptions):
        res = super().make_3dpm_data(material, geometry, opt)
        # 원래 데이터를 갖고 있는게 좋을지는 기획 내용에 따라 다를 수 있음
        pnmax = max(res, key=lambda x: x.n).n
        pnmax *= 0.8
        for result in res:
            _et = 0.003 * (result.k_u**-1 - 1.0)
            _phi_tens = 0.85
            _phi_comp = 0.65
            _e_tens = 0.005
            _e_comp = 0.002
            if _et >= _e_tens:
                phi = _phi_tens
            elif _et <= _e_comp:
                phi = _phi_comp
            else:
                phi = _phi_comp + (_phi_tens - _phi_comp) * (_e_tens - _e_comp) / (_e_tens - _e_comp)

            _tmp = result.n * phi
            result.n = min(_tmp, pnmax)
            result.m_x *= phi
            result.m_y *= phi
            result.m_xy *= phi

        return res

class DgnCodeEU(DgnCode):
    """
    Class for Design Code EU
    """
    def __init__(self) -> None:
        super().__init__()

    def make_3dpm_data(self, material: Material, geometry: Geometry, opt: PMOptions):
        return super().make_3dpm_data(material, geometry, opt)

def get_dgncode(dgncode: str):
    if dgncode == "ACI318M-19":
        return DgnCodeUS()
    else:
        return DgnCodeEU()

@auto_schema(title="3D PM Curve", description="3D PM Curve")
def make_3dpm(material: Material, geometry: Geometry, opt: PMOptions):
    """
    3D Axial-Moment Curvature Analysis
    
    Args:
        material: Material
        geometry: Geometry
        opt: PMOptions
        
    Returns:
        list[UltimateBendingResults]: 3D Axial-Moment Curvature Analysis results
    """
    pm = get_dgncode(opt.dgncode)
    results = pm.make_3dpm_data(material, geometry, opt)
    return results

@auto_schema(title="3D PM Curve", description="3D PM Curve")
def calc_3dpm(material: Material, geometry: Geometry, lcb: Lcb, opt: PMOptions) -> Result3DPM:
    """
    Return the 3D PM Curve & norminal strength points

    Args:
        material: Material
        geometry: Geometry
        lcb: Lcb
        opt: PMOptions

    return:
        Result3DPM: 3DPM curve & norminal strength points about lcom
    """
    results = make_3dpm(material, geometry, opt)

    d_n_values = [result.n for result in results]
    m_x_values = [result.m_x for result in results]
    m_y_values = [result.m_y for result in results]

    points = np.column_stack((m_x_values, m_y_values, d_n_values))
    hull = ConvexHull(points)
    mesh1 = trimesh.Trimesh(vertices=hull.points, faces=hull.simplices)
    ray = trimesh.ray.ray_pyembree.RayMeshIntersector(mesh1)

    result_lcom_uls = []
    lcoms_uls = []
    for lcom in lcb.uls.lcoms:
        lcom_name = lcom.name
        lcom_point = [lcom.f.Mx.value, lcom.f.My.value, lcom.f.Fz.value]

        if opt.by_ecc_pu == "ecc":
            origin = np.array([0, 0, 0])
        else:
            origin = np.array([0, 0, lcom_point[2]])

        direction = lcom_point - origin
        direction = direction / np.linalg.norm(direction)

        locations, index_ray, index_tri = ray.intersects_location(
            ray_origins=np.array([origin]),
            ray_directions=np.array([direction])
        )

        lcoms_uls.append(lcom)
        result_lcom_uls.append(Lcom(name=lcom_name, f=SectionForce(Fz=Force(value=locations[0, 2], unit=enUnitForce.N), 
                                                                  Mx=Moment(value=locations[0, 0], unit=enUnitMoment.Nmm), 
                                                                  My=Moment(value=locations[0, 1], unit=enUnitMoment.Nmm))))

    meshres = []
    for i in range(len(hull.points)):
        meshres.append(Force(Mx=hull.points[i][0], My=hull.points[i][1], Nz=hull.points[i][2]))

    meshData = Mesh3DPM(mesh3dpm=meshres)
    return Result3DPM(meshes=meshData, lcbs=lcoms_uls, strength=result_lcom_uls)

# dummy functions
@auto_schema(title="concrete geometry", description="concrete geometry")
def concrete_geometry(outerPolygon: OuterPolygon, innerPolygon: InnerPolygon, matl: ConcreteGrade) -> ConcreteGeometry:
    """Return the concrete geometry
    
    Args:
        outerPolygon (OuterPolygon): outer polygon of the concrete
        innerPolygon (InnerPolygon): inner polygon of the concrete
        matl (ConcreteGrade): material of the concrete
    """
    return ConcreteGeometry(outerPolygon=outerPolygon.points, innerPolygon=innerPolygon.points, material=matl)

@auto_schema(title="rebar geometry", description="rebar geometry")
def rebar_geometry(position: Points, prop: RebarProp) -> RebarGeometry:
    """Return the rebar geometry
    
    Args:
        position (Points): rebar position
        prop (RebarProp): rebar properties
    
    Returns:
        RebarGeometry: rebar geometry
    """
    return RebarGeometry(position=position.points, prop=prop)

@auto_schema(title="tendon geometry", description="tendon geometry")
def tendon_geometry(points: Points, prop: TendonProp) -> TendonGeometry:
    """Return the tendon geometry
    
    Args:
        position (Points): tendon position
        prop (TendonProp): tendon properties
        
    Returns:
        TendonGeometry: tendon geometry
    """
    return TendonGeometry(points=points.points, prop=prop)

@auto_schema(title="geometry design", description="geometry design")
def geometry_design(concrete: ConcreteGeometry, rebar: RebarGeometry) -> Geometry:
    """Return the geometry
    
    Args:
        concrete (ConcreteGeometry): concrete geometry
        rebar (RebarGeometry): rebar geometry
    
    Returns:
        Geometry: geometry
    """
    return Geometry(concrete=concrete, rebar=rebar)

@auto_schema(title="material properties design", description="material properties design")
def material_properties_design(conc: MaterialConcrete, rebar: MaterialRebar) -> Material:
    """Return the material properties
    
    Args:
        conc (MaterialConcrete): concrete properties
        rebar (MaterialRebar): rebar properties
    
    Returns:
        Material: material properties
    """
    return Material(concrete=conc, rebar=rebar)

@auto_schema(title="lcom design", description="lcom design")
def lcom_design(uls: Lcoms) -> Lcb:
    """Return the load combination
    
    Args:
        uls (Lcoms): uls load combination
    Returns:
        Lcb: load combination
    """
    return Lcb(uls=uls)

@auto_schema(title="3d pm option", description="3d pm option")
def options_design(opt: PMOptions) -> PMOptions:
    """Return the options
    
    Args:
        opt (PMOptions): options
    
    Returns:
        PMOptions: options
    """
    return PMOptions(dgncode=opt.dgncode, by_ecc_pu=opt.by_ecc_pu)

# res = rebar_geometry(**{
#   "position": {
#     "points": [
#       {
#         "x": 0,
#         "y": 0
#       },
#       {
#         "x": 400,
#         "y": 0
#       },
#       {
#         "x": 400,
#         "y": 600
#       },
#       {
#         "x": 0,
#         "y": 600
#       }
#     ]
#   },
#   "prop": {
#     "area": 287,
#     "material": {
#       "design_code": "ACI318M-19",
#       "grade": "Grade 420"
#     }
#   }
# })

# print(res)

# _material = Material()
# _geometry = Geometry()
# _lcb = Lcb()
# res=calc_uncracked_stress(_material, _geometry,_lcb)
# print(res)

# from dataclasses import dataclass, asdict
# res = MaterialRebar()
# data_dict = [component.__dict__ for component in res.curve_uls]
# print(data_dict)

# res = calc_3dpm(Material(), Geometry(), Lcb(), PMOptions())
# print(res)