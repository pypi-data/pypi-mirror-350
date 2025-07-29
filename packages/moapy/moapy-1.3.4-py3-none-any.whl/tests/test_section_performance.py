import moapy.wgsd.wgsd_oapi as wgsd_oapi
from moapy.data_pre import SectionForce, PMOptions, AxialForceOpt, AngleOpt, DgnCode, Lcom, Moment
from moapy.rc_pre import Material, Geometry
from moapy.enum_pre import enUnitMoment

def test_calc_mm():
    res = wgsd_oapi.calc_rc_mm_interaction_curve(Material(), Geometry(), PMOptions(), AxialForceOpt())
    return res

def test_report_mm():
    res = wgsd_oapi.report_rc_mm_interaction_curve(Material(), Geometry(), PMOptions(), AxialForceOpt())
    return res

def test_calc_pm():
    res = wgsd_oapi.calc_rc_pm_interaction_curve(Material(), Geometry(), PMOptions(), AngleOpt())
    return res

def test_report_pm():
    res = wgsd_oapi.report_rc_pm_interaction_curve(Material(), Geometry(), PMOptions(), AngleOpt())
    return res

def test_calc_rc_uls_stress():
    res = wgsd_oapi.calc_rc_uls_stress(Material(), Geometry(), DgnCode(), AngleOpt(), AxialForceOpt())
    return res

def test_calc_rc_uls_bending_capacity():
    res = wgsd_oapi.calc_rc_uls_bending_capacity(Material(), Geometry(), AngleOpt(), AxialForceOpt())
    return res

def test_calc_calc_rc_cracked_stress():
    res = wgsd_oapi.calc_rc_cracked_stress(Material(), Geometry(), DgnCode(), Lcom())
    return res

def test_report_rc_cracked_stress():
    res = wgsd_oapi.report_rc_cracked_stress(Material(), Geometry(), DgnCode(), Lcom(name="lcom", f=SectionForce(Mx=Moment(value=10.0, unit=enUnitMoment.Nmm))))
    return res

def test_calc_rc_moment_curvature():
    res = wgsd_oapi.calc_rc_moment_curvature(Material(), Geometry())
    return res


if __name__ == "__main__":
    test_calc_mm()
    test_report_mm()
    test_calc_pm()
    test_report_pm()
    test_calc_rc_uls_stress()
    test_calc_rc_uls_bending_capacity()
    test_calc_calc_rc_cracked_stress()
    test_report_rc_cracked_stress()
    test_calc_rc_moment_curvature()