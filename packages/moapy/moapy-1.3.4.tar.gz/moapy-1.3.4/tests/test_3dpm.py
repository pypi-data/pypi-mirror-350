import pytest
import moapy.wgsd.wgsd_flow as wgsd_3dpm
from moapy.data_pre import Lcb, Lcoms, Lcom, Force, PMOptions, SectionForce, Moment, enUnitForce, enUnitMoment
from moapy.rc_pre import Material, Geometry

def test_3dpm_conc_rebar():
    material = Material()
    geom = Geometry()
    lcb = Lcb
    lcb.uls = Lcoms(lcoms=[Lcom(name="uls1", f=SectionForce(Fz=Force(value=100.0, unit=enUnitForce.N),
                                                           Mx=Moment(value=10.0, unit=enUnitMoment.Nmm),
                                                           My=Moment(value=50.0, unit=enUnitMoment.Nmm))),
                           Lcom(name="uls2", f=SectionForce(Fz=Force(value=100.0, unit=enUnitForce.N),
                                                           Mx=Moment(value=15.0, unit=enUnitMoment.Nmm),
                                                           My=Moment(value=50.0, unit=enUnitMoment.Nmm))),
                           Lcom(name="uls3", f=SectionForce(Fz=Force(value=100.0, unit=enUnitForce.N),
                                                           Mx=Moment(value=0.0, unit=enUnitMoment.Nmm),
                                                           My=Moment(value=0.0, unit=enUnitMoment.Nmm))),
                           Lcom(name="uls4", f=SectionForce(Fz=Force(value=-100.0, unit=enUnitForce.N),
                                                           Mx=Moment(value=0.0, unit=enUnitMoment.Nmm),
                                                           My=Moment(value=0.0, unit=enUnitMoment.Nmm)))])
    opt = PMOptions()
    res = wgsd_3dpm.calc_3dpm(material, geom, lcb, opt)
    assert pytest.approx(res.strength[0].name) == 'uls1'
    assert pytest.approx(res.strength[0].f.Mx.value) == 495152.21186695714
    assert pytest.approx(res.strength[0].f.My.value) == 2475761.0593347857
    assert pytest.approx(res.strength[0].f.Fz.value) == 4951522.118669571
    assert pytest.approx(res.strength[1].name) == 'uls2'
    assert pytest.approx(res.strength[1].f.Mx.value) == 742728.3178004358
    assert pytest.approx(res.strength[1].f.My.value) == 2475761.0593347857
    assert pytest.approx(res.strength[1].f.Fz.value) == 4951522.118669571
    assert pytest.approx(res.strength[2].name) == 'uls3'
    assert pytest.approx(res.strength[2].f.Mx.value) == 0.0
    assert pytest.approx(res.strength[2].f.My.value) == 0.0
    assert pytest.approx(res.strength[2].f.Fz.value) == 4951522.118669571
    assert pytest.approx(res.strength[3].name) == 'uls4'
    assert pytest.approx(res.strength[3].f.Mx.value) == 0.0
    assert pytest.approx(res.strength[3].f.My.value) == 0.0
    assert pytest.approx(res.strength[3].f.Fz.value) == -574000.0435605047


if __name__ == "__main__":
    test_3dpm_conc_rebar()
