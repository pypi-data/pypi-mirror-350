from moapy.wgsd.wgsd_oapi import (
    calc_rc_mm_interaction_curve, calc_rc_pm_interaction_curve, calc_rc_uls_stress, calc_rc_uls_bending_capacity, calc_rc_cracked_stress,
    calc_rc_cracked_properties, calc_rc_uncracked_stress, calc_rc_moment_curvature, calc_rc_neutral_axis_depth, calc_extreme_bar,
    calc_cracking_moment, calc_gross_properties, calc_transformed_gross_properties
)
from moapy.data_pre import AxialForceOpt, PMOptions, AngleOpt, DgnCode, Lcom, ElasticModulusOpt
from moapy.rc_pre import Geometry, Material
import inspect

def test_calc_rc_mm_interaction_curve():
    return calc_rc_mm_interaction_curve(Material(), Geometry(), PMOptions(), AxialForceOpt())

def test_calc_rc_pm_interaction_curve():
    return calc_rc_pm_interaction_curve(Material(), Geometry(), PMOptions(), AngleOpt())

def test_calc_rc_uls_stress():
    return calc_rc_uls_stress(Material(), Geometry(), DgnCode(name="ACI318M-19"), AngleOpt(), AxialForceOpt())

def test_calc_rc_uls_bending_capacity():
    return calc_rc_uls_bending_capacity(Material(), Geometry(), DgnCode(name="ACI318M-19"), AngleOpt(), AxialForceOpt())

def test_calc_rc_cracked_stress():
    return calc_rc_cracked_stress(Material(), Geometry(), DgnCode(name="ACI318M-19"), Lcom())

def test_calc_rc_cracked_properties():
    return calc_rc_cracked_properties(Material(), Geometry())

def test_calc_rc_uncracked_stress():
    return calc_rc_uncracked_stress(Material(), Geometry(), Lcom())

def test_calc_rc_moment_curvature():
    return calc_rc_moment_curvature(Material(), Geometry())

def test_calc_rc_neutral_axis_depth():
    return calc_rc_neutral_axis_depth(Material(), Geometry())

def test_calc_extreme_bar():
    return calc_extreme_bar(Material(), Geometry(), AngleOpt())

def test_calc_cracking_moment():
    return calc_cracking_moment(Material(), Geometry(), AngleOpt())

def test_calc_gross_properties():
    return calc_gross_properties(Material(), Geometry())

def test_calc_transformed_gross_properties():
    return calc_transformed_gross_properties(Material(), Geometry(), ElasticModulusOpt())

def run_all_tests():
    # �재 모듈 �의 모든 �수 �'test_'로작�는 �수매행
    for name, func in inspect.getmembers(__import__(__name__), inspect.isfunction):
        if name.startswith("test_"):
            print(f"Running {name}...")
            func()


if __name__ == "__main__":
    run_all_tests()
