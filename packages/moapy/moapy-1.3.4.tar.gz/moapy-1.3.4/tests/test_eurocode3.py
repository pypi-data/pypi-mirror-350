import sys
import pytest
import moapy.dgnengine.eurocode3_beam as eurocode3_beam
import moapy.dgnengine.eurocode3_boltconnection as eurocode3_boltconnection
import moapy.dgnengine.eurocode4_composited_beam as eurocode4_composited_beam
from moapy.data_pre import (
    SectionForce, UnitLoads, EffectiveLengthFactor, Force, Moment, Length, enUnitForce, enUnitLength, enUnitMoment
)

from moapy.steel_pre import (
    SteelMaterial_EC, SteelSection_EN10365, SteelPlateMember_EC, ConnectType, SteelConnectMember,
    SteelBolt_EC, Welding_EC, SteelMember, ShearConnector_EC, SteelLength_Torsion, SteelMomentModificationFactor_EC, SteelBoltConnectionForce,
)
from moapy.rc_pre import CompositedParam, SlabMember_EC

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_calc_EC3_beamcolumn():
    return eurocode3_beam.calc_ec3_beam_column()

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_report_EC3_beamcolumn():
    return eurocode3_beam.report_ec3_beam_column()

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_calc_boltconnection():
    return eurocode3_boltconnection.calc_ec3_bolt_connection()

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_report_boltconnection():
    return eurocode3_boltconnection.report_ec3_bolt_connection()

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_calc_composited_beam():
    return eurocode4_composited_beam.calc_ec4_composited_beam()

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_report_composited_beam():
    return eurocode4_composited_beam.report_ec4_composited_beam()


if __name__ == "__main__":
    test_calc_EC3_beamcolumn()
    test_report_EC3_beamcolumn()
    test_calc_boltconnection()
    test_report_boltconnection()
    test_calc_composited_beam()
    test_report_composited_beam()
