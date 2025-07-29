import moapy.wgsd.wgsd_flow as wgsd_flow
import moapy.wgsd.wgsd_sectionproperty as wgsd_sectionproperty
import moapy.mdreporter as mdreporter

from moapy.auto_convert import auto_schema

@auto_schema(title="Generate 3D PM Report", description="Generate 3D PM Report")
def generate_report_3dpm(matl: wgsd_flow.Material, geom: wgsd_flow.Geometry, lcb: wgsd_flow.Lcb, opt: wgsd_flow.PMOptions, sectprop: wgsd_sectionproperty.SectionProperty):
    """
    Generate 3D PM report
    """
    rpt = mdreporter.ReportUtil("3dpm.md", "*3D PM Report*")
    rpt.add_chapter("Material")
    # rpt.add_line(f"Concrete : {matl.concrete.grade.grade}")
    # rpt.add_line_fvu("f_{ck}", matl.concrete.grade.fck, mdreporter.enUnit.STRESS)
    # rpt.add_line_fvu("E_{c}", matl.concrete.grade.Ec, mdreporter.enUnit.STRESS)
    # SS-curve에 대한 정보를 추가

    # rpt.add_line(f"Rebar : {matl.rebar.grade.grade}")
    # rpt.add_line_fvu("f_{yk}", matl.rebar.grade.fyk, mdreporter.enUnit.STRESS)
    # rpt.add_line_fvu("E_{s}", matl.rebar.grade.Es, mdreporter.enUnit.STRESS)
    # SS-curve에 대한 정보를 추가

    sect_data = sectprop.to_dict()
    rpt.add_chapter("Section")
    # 삽도?
    rpt.add_line_fvu("Area", sect_data['Area'], mdreporter.enUnit.AREA)
    rpt.add_line_fvu("Asy", sect_data['Asy'], mdreporter.enUnit.AREA)
    rpt.add_line_fvu("Asz", sect_data['Asz'], mdreporter.enUnit.AREA)
    rpt.add_line_fvu("Ixx", sect_data['Ixx'], mdreporter.enUnit.INERTIA)
    rpt.add_line_fvu("Iyy", sect_data['Iyy'], mdreporter.enUnit.INERTIA)
    rpt.add_line_fvu("Izz", sect_data['Izz'], mdreporter.enUnit.INERTIA)
    rpt.add_line_fvu("Cy", sect_data['Cy'], mdreporter.enUnit.LENGTH)
    rpt.add_line_fvu("Cz", sect_data['Cz'], mdreporter.enUnit.LENGTH)
    rpt.add_line_fvu("Syp", sect_data['Syp'], mdreporter.enUnit.VOLUME)
    rpt.add_line_fvu("Sym", sect_data['Sym'], mdreporter.enUnit.VOLUME)
    rpt.add_line_fvu("Szp", sect_data['Szp'], mdreporter.enUnit.VOLUME)
    rpt.add_line_fvu("Szm", sect_data['Szm'], mdreporter.enUnit.VOLUME)
    rpt.add_line_fvu("Ipyy", sect_data['Ipyy'], mdreporter.enUnit.INERTIA)
    rpt.add_line_fvu("Ipzz", sect_data['Ipzz'], mdreporter.enUnit.INERTIA)
    rpt.add_line_fvu("Zy", sect_data['Zy'], mdreporter.enUnit.VOLUME)
    rpt.add_line_fvu("Zz", sect_data['Zz'], mdreporter.enUnit.VOLUME)
    rpt.add_line_fvu("ry", sect_data['ry'], mdreporter.enUnit.LENGTH)
    rpt.add_line_fvu("rz", sect_data['rz'], mdreporter.enUnit.LENGTH)

    rpt.add_chapter("Load Combination")
    rpt.add_line("| Name  | Fx   | My   | Mz   |")
    rpt.add_line("|-------|------|------|------|")
    for lcb in lcb.uls.DATA:
        rpt.add_line(f"| {lcb[0]} | {lcb[1]} | {lcb[2]} | {lcb[3]} |")

    return rpt.get_md_text()


# matl = wgsd_flow.gsdMaterial()
# geom = wgsd_flow.gsdGeometry()
# lcb = wgsd_flow.gsdLcb()
# opt = wgsd_flow.gsdOptions()
# sectprop = wgsd_sectionproperty.MSectionProperty()

# md = generate_report_3dpm(matl, geom, lcb, opt, sectprop)
# print(md)