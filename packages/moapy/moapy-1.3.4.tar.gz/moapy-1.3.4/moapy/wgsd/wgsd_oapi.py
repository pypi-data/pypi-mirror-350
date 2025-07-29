import moapy.wgsd.wgsd_flow as wgsd_flow
import concreteproperties.results as res
import concreteproperties.utils as utils
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from moapy.mdreporter import ReportUtil
from moapy.data_pre import PMOptions, Lcom, DgnCode, AxialForceOpt, AngleOpt, ElasticModulusOpt, Length, Angle
from moapy.rc_pre import Material, Geometry, NeutralAxisDepth
from moapy.data_post import ResultMD
from moapy.auto_convert import auto_schema
from moapy.enum_pre import enUnitLength
from concreteproperties.concrete_section import ConcreteSection


matplotlib.use('Agg')  # Agg 백엔드 사용

@auto_schema(title="RC MM Interaction Curve", description="RC MM Interaction Curve")
def calc_rc_mm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, axialforce: AxialForceOpt) -> res.BiaxialBendingResults:
    """
    Moment Interaction Curve
    """
    pm = wgsd_flow.get_dgncode(opt.dgncode)
    comp = pm.calc_compound_section(material, geometry, opt)
    if type(comp) is ConcreteSection:
        return comp.biaxial_bending_diagram(n=axialforce.Nx.value)

    return ''

def get_markdownimg_base64(scale=1.0):
    """
    Get SVG Base64 Image for Markdown with specified scale ratio.
    
    :param scale: Ratio to scale the image, default is 1.0 (no scaling)
    """
    # 이미지 버퍼에 SVG 형식으로 저장
    buffer = io.BytesIO()
    plt.savefig(buffer, format='svg')
    buffer.seek(0)

    # SVG 데이터를 문자열로 읽어오기
    svg_data = buffer.getvalue().decode('utf-8')

    # SVG 데이터를 Base64로 인코딩
    img_base64 = base64.b64encode(svg_data.encode('utf-8')).decode('utf-8')
    
    # HTML 태그로 감싸서 비율 조정
    markdown_img = f'<img src="data:image/svg+xml;base64,{img_base64}" width="{int(scale * 100)}%" />'
    return markdown_img

@auto_schema(title="RC MM Interaction Curve", description="RC MM Interaction Curve")
def report_rc_mm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, axialforce: AxialForceOpt) -> ResultMD:
    """
    Report Moment Interaction Curve
    """
    rpt = ReportUtil("test.md", 'M-M Curve result')
    comp_sect = generate_defaultinfo_markdown_report(rpt, material, geometry)
    plt.clf()
    result = comp_sect.biaxial_bending_diagram(n=axialforce.Nx.value)
    result.plot_diagram()
    rpt.add_paragraph("Moment-Moment Interaction Curve")
    markdown_img = get_markdownimg_base64(0.6)

    rpt.add_line(markdown_img)
    return ResultMD(md=rpt.get_md_text())

@auto_schema(title="RC PM Interaction Curve", description="RC PM Interaction Curve")
def calc_rc_pm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, angle: AngleOpt):
    """
    Axial Moment Interaction Curve
    """
    pm = wgsd_flow.get_dgncode(opt.dgncode)
    comp = pm.calc_compound_section(material, geometry, opt)
    if type(comp) is ConcreteSection:
        return comp.moment_interaction_diagram(theta=angle.theta.value)

    return ''

@auto_schema(title="RC PM Interaction Curve", description="RC PM Interaction Curve")
def report_rc_pm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, angle: AngleOpt) -> ResultMD:
    """
    Axial Moment Interaction Curve
    """
    rpt = ReportUtil("test.md", 'P-M Interaction Result')
    comp_sect = generate_defaultinfo_markdown_report(rpt, material, geometry)
    plt.clf()
    result = comp_sect.moment_interaction_diagram(theta=angle.theta.value)
    result.plot_diagram()
    rpt.add_paragraph("Axial-Moment Interaction Curve")
    markdown_img = get_markdownimg_base64(0.7)

    rpt.add_line(markdown_img)
    return ResultMD(md=rpt.get_md_text())

@auto_schema(title="RC ULS Stress", description="RC ULS Stress")
def calc_rc_uls_stress(material: Material, geometry: Geometry, theta: AngleOpt, axialForce: AxialForceOpt):
    """
    reinforced concrete ultimate stress
    """
    sect = wgsd_flow.MSection(material, geometry)
    comp = sect.calc_compound_section()
    if type(comp) is ConcreteSection:
        ultimate_results = comp.ultimate_bending_capacity(theta=theta.theta.value, n=axialForce.Nx.value)
        return comp.calculate_ultimate_stress(ultimate_results)

    return ''

@auto_schema(title="RC ULS Stress", description="RC ULS Stress")
def calc_rc_uls_bending_capacity(material: Material, geometry: Geometry, theta: AngleOpt, axialForce: AxialForceOpt):
    """
    reinforced concrete ultimate bending capacity
    """
    sect = wgsd_flow.MSection(material, geometry)
    comp = sect.calc_compound_section()
    if type(comp) is ConcreteSection:
        return comp.ultimate_bending_capacity(theta=theta.theta.value, n=axialForce.Nx.value)

    return ''

@auto_schema(title="RC cracked stress", description="RC cracked stress")
def calc_rc_cracked_stress(material: Material, geometry: Geometry, lcom: Lcom):
    """
    reinforced concrete cracked stress

    Args:
        material: Material
        geometry: Geometry
        lcom: Lcom

    Returns:
        res.StressResult
    """
    sect = wgsd_flow.MSection(material, geometry)
    comp = sect.calc_compound_section()
    if type(comp) is ConcreteSection:
        cracked_res = comp.calculate_cracked_properties(theta=0.0)
        return comp.calculate_cracked_stress(cracked_res, n=lcom.f.dir_x.axial.value, m=lcom.f.dir_x.bending.value)

    return res.StressResult

@auto_schema(title="RC cracked stress", description="RC cracked stress")
def report_rc_cracked_stress(material: Material, geometry: Geometry, lcom: Lcom) -> ResultMD:
    """
    Report Cracked Stress
    """
    rpt = ReportUtil("test.md", 'cracked stress result')
    comp_sect = generate_defaultinfo_markdown_report(rpt, material, geometry)
    cracked_res = comp_sect.calculate_cracked_properties(theta=0.0)
    result = comp_sect.calculate_cracked_stress(cracked_res, n=lcom.f.dir_x.axial.value, m=lcom.f.dir_x.bending.value)
    
    plt.clf()
    result.plot_stress()
    rpt.add_paragraph("Cracked Stress Contour")
    markdown_img = get_markdownimg_base64(0.8)
    rpt.add_line(markdown_img)
    return ResultMD(md=rpt.get_md_text())

@auto_schema(title="RC Uncracked Stress", description="RC Uncracked Stress")
def calc_rc_cracked_properties(material: Material, geometry: Geometry):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.calculate_cracked_properties()

@auto_schema(title="RC Uncracked Stress", description="RC Uncracked Stress")
def calc_rc_uncracked_stress(material: Material, geometry: Geometry, lcb: Lcom):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.calculate_uncracked_stress(n=lcb.f.dir_x.axial.value, m_x=lcb.f.dir_x.bending.value, m_y=lcb.f.dir_y.bending.value)

@auto_schema(title="RC moment curvature", description="RC moment curvature")
def calc_rc_moment_curvature(material: Material, geometry: Geometry) -> res.MomentCurvatureResults:
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.moment_curvature_analysis()

@auto_schema(title="Neutral Axis Calculator for RC Sections", description=(
        "The Neutral Axis Calculator for RC (Reinforced Concrete) sections is a tool "
        "designed to quickly and accurately calculate the neutral axis during the cross-"
        "sectional design of reinforced concrete structures. This calculator considers "
        "the placement of reinforcement in both compression and tension zones, along "
        "with the properties of the concrete, to determine the neutral axis position "
        "and assess structural efficiency.\n\n"
        "Key Features:\n"
        "- Input Section Data: Allows input of concrete compressive strength, reinforcement "
        "layout (position, area), and section dimensions.\n"
        "- Neutral Axis Calculation: Calculates the equilibrium point between reinforcement "
        "and concrete based on the provided data.")
)
def calc_rc_neutral_axis_depth(material: Material, geometry: Geometry) -> NeutralAxisDepth:
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return NeutralAxisDepth(depth=Length(value=prop.ultimate_bending_capacity(theta=0.0, n=0.0).d_n, unit=geometry.concrete.outerPolygon[0].x.unit))

def generate_comp_sect(material: Material, geometry: Geometry):
    sect = wgsd_flow.MSection(material, geometry)
    return sect.calc_compound_section()

def generate_markdown_table(prop, fmt: str = "8.6e") -> str:
    """Generates a markdown table for the gross concrete section properties."""
    table_md = "| Property                   | Value           |\n"
    table_md += "|----------------------------|-----------------|\n"

    rows = [
        ("Total Area", prop.total_area),
        ("Concrete Area", prop.concrete_area),
    ]

    if prop.reinf_meshed_area:
        rows.append(("Meshed Reinforcement Area", prop.reinf_meshed_area))

    rows.append(("Lumped Reinforcement Area", prop.reinf_lumped_area))

    if prop.strand_area:
        rows.append(("Strand Area", prop.strand_area))

    additional_rows = [
        ("Axial Rigidity (EA)", prop.e_a),
        ("Mass (per unit length)", prop.mass),
        ("Perimeter", prop.perimeter),
        ("E.Qx", prop.e_qx),
        ("E.Qy", prop.e_qy),
        ("x-Centroid", prop.cx),
        ("y-Centroid", prop.cy),
        ("x-Centroid (Gross)", prop.cx_gross),
        ("y-Centroid (Gross)", prop.cy_gross),
        ("E.Ixx_g", prop.e_ixx_g),
        ("E.Iyy_g", prop.e_iyy_g),
        ("E.Ixy_g", prop.e_ixy_g),
        ("E.Ixx_c", prop.e_ixx_c),
        ("E.Iyy_c", prop.e_iyy_c),
        ("E.Ixy_c", prop.e_ixy_c),
        ("E.I11", prop.e_i11),
        ("E.I22", prop.e_i22),
        ("Principal Axis Angle", prop.phi),
        ("E.Zxx+", prop.e_zxx_plus),
        ("E.Zxx-", prop.e_zxx_minus),
        ("E.Zyy+", prop.e_zyy_plus),
        ("E.Zyy-", prop.e_zyy_minus),
        ("E.Z11+", prop.e_z11_plus),
        ("E.Z11-", prop.e_z11_minus),
        ("E.Z22+", prop.e_z22_plus),
        ("E.Z22-", prop.e_z22_minus),
        ("Ultimate Concrete Strain", prop.conc_ultimate_strain),
    ]

    rows.extend(additional_rows)

    if prop.n_prestress:
        rows.append(("n_prestress", prop.n_prestress))
        rows.append(("m_prestress", prop.m_prestress))

    for property_name, value in rows:
        table_md += f"| {property_name:<26} | {value:{fmt}} |\n"

    return table_md

def generate_defaultinfo_markdown_report(rpt: ReportUtil, material: Material, geometry: Geometry):
    rpt.add_paragraph("Material")
    # rpt.add_line(f" - Concrete: {material.concrete.grade.design_code} {material.concrete.grade.grade}")
    plt.plot([component.strain for component in material.concrete.curve_sls], [component.stress for component in material.concrete.curve_sls], label='SLS')
    plt.plot([component.strain for component in material.concrete.curve_uls], [component.stress for component in material.concrete.curve_uls], label='ULS')
    plt.xlabel('Strain')
    plt.ylabel('Stress')
    plt.title('Concrete Stress-Strain Curve')
    plt.legend()
    plt.show(block=False)
    markdown_img = get_markdownimg_base64(0.6)
    rpt.add_line("")
    rpt.add_line(markdown_img)

    plt.clf()
    rpt.add_line("")
    # rpt.add_line(f" - Rebar: {material.rebar.grade.design_code} {material.rebar.grade.grade}")
    plt.plot([component.strain for component in material.rebar.curve_sls], [component.stress for component in material.rebar.curve_sls], label='SLS')
    plt.plot([component.strain for component in material.rebar.curve_uls], [component.stress for component in material.rebar.curve_uls], label='ULS')
    plt.xlabel('Strain')
    plt.ylabel('Stress')
    plt.title('Rebar Stress-Strain Curve')
    plt.legend()
    plt.show(block=False)
    markdown_img = get_markdownimg_base64(0.6)
    rpt.add_line("")
    rpt.add_line(markdown_img)

    plt.clf()
    comp_sect = generate_comp_sect(material, geometry)
    rpt.add_paragraph("Geometry")
    comp_sect.plot_section()
    plt.show(block=False)
    markdown_img = get_markdownimg_base64(0.7)
    rpt.add_line(markdown_img)
    gross_props = comp_sect.get_gross_properties()
    md = generate_markdown_table(prop=gross_props)
    rpt.add_line(md)
    return comp_sect

@auto_schema(title="RC Moment Curvature", description="RC Moment Curvature")
def report_rc_moment_curvature(material: Material, geometry: Geometry) -> ResultMD:
    rpt = ReportUtil("test.md", 'Moment Curvature result')

    comp_sect = generate_defaultinfo_markdown_report(rpt, material, geometry)

    rpt.add_line("")
    plt.clf()
    rpt.add_paragraph("Moment-Curvature Analysis")
    mphi_res = comp_sect.moment_curvature_analysis()
    mphi_res.plot_results()
    markdown_img = get_markdownimg_base64(0.6)

    rpt.add_line(markdown_img)
    return ResultMD(md=rpt.get_md_text())

@auto_schema(title="RC extream bar", description="RC extream bar")
def calc_extreme_bar(material: Material, geometry: Geometry, angle: AngleOpt):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.extreme_bar(theta=angle.theta.value)

@auto_schema(title="RC cracking moment", description="RC cracking moment")
def calc_cracking_moment(material: Material, geometry: Geometry, angle: AngleOpt):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.calculate_cracking_moment(theta=angle.theta.value)

@auto_schema(title="gross properties", description="gross properties")
def calc_gross_properties(material: Material, geometry: Geometry):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.get_gross_properties()

@auto_schema(title="transformed gross properties", description="transformed gross properties")
def calc_transformed_gross_properties(material: Material, geometry: Geometry, m: ElasticModulusOpt):
    sect = wgsd_flow.MSection(material, geometry)
    prop = sect.calc_compound_section()
    return prop.get_transformed_gross_properties(m.E.value)


if __name__ == "__main__":
    # res = report_rc_cracked_stress(Material(), Geometry(), DgnCode(), Lcom())
    # res = calc_rc_cracked_stress(Material(), Geometry(), DgnCode(), Lcom())
    # print(res)
    res = calc_rc_uls_bending_capacity(Material(), Geometry(), AngleOpt(), AxialForceOpt())
    print(res)