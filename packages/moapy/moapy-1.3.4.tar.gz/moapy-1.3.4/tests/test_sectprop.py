import pytest
import moapy.wgsd.wgsd_sectionproperty as wgsd_sectionproperty

def test_sectprop_calc():
    inp = wgsd_sectionproperty.OuterPolygon()
    res_data = wgsd_sectionproperty.calc_sectprop(inp)
    assert pytest.approx(res_data.area.value) == 240000.0
    assert pytest.approx(res_data.asy.value) == 200000.0
    assert pytest.approx(res_data.asz.value) == 200000.0
    assert pytest.approx(res_data.ixx.value) == 7517216331.957718
    assert pytest.approx(res_data.iyy.value) == 7200000000.0
    assert pytest.approx(res_data.izz.value) == 3200000000.0
    assert pytest.approx(res_data.cyp.value) == 200.0
    assert pytest.approx(res_data.czp.value) == 300.0
    assert pytest.approx(res_data.syp.value) == 24000000.
    assert pytest.approx(res_data.sym.value) == 24000000.
    assert pytest.approx(res_data.szp.value) == 16000000.
    assert pytest.approx(res_data.szm.value) == 16000000.
    assert pytest.approx(res_data.ipyy.value) == 7200000000.
    assert pytest.approx(res_data.ipzz.value) == 3200000000.
    assert pytest.approx(res_data.zy.value) == 36000000.
    assert pytest.approx(res_data.zz.value) == 24000000.
    assert pytest.approx(res_data.ry.value) == 173.2050807568887
    assert pytest.approx(res_data.rz.value) == 115.47005383792664


if __name__ == "__main__":
    test_sectprop_calc()