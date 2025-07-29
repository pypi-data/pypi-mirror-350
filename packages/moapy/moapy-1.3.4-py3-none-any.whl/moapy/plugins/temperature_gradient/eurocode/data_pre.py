from typing import Any, DefaultDict, List, TypeAlias
from pydantic import ConfigDict
from pydantic.dataclasses import Field
from moapy.auto_convert import MBaseModel
from moapy.data_pre import Length, Stress, ThermalExpansionCoeff
from moapy.enum_pre import enUnitLength, enUnitStress, enUnitThermalExpansion
from moapy.plugins.temperature_gradient.eurocode.shape_utils import (
    composite_steel_box,
    composite_steel_i,
    composite_steel_tub,
    psc_1cell,
    psc_2cell,
    psc_I,
    psc_T,
    steel_box,
    steel_i,
)

"""Coordeinate"""
OuterType: TypeAlias = DefaultDict[Any, List[Any]]
InnerType: TypeAlias = DefaultDict[Any, List[Any]]
CompType: TypeAlias = DefaultDict[Any, List[Any]]


# class Coordinate(Protocol):
#     outer: OuterType
#     inner: InnerType
#     comp: CompType


class SectionCoordinate(MBaseModel):
    outer: OuterType = Field(description="Outer")
    inner: InnerType = Field(description="Inner")
    comp: CompType = Field(description="Comp")


"""material"""


class SectionMaterial(MBaseModel):
    """
    Section Material
    """

    thermal_expansion: ThermalExpansionCoeff = Field(
        default=ThermalExpansionCoeff(
            value=12e-6, unit=enUnitThermalExpansion.PER_CELSIUS
        ),
        description="Thermal Expansion",
    )
    elastic_modulus: Stress = Field(
        default=Stress(value=210000.0, unit=enUnitStress.MPa),
        description="Elastic Modulus",
    )


"""shape"""


class BaseSectionShape(MBaseModel):
    pass


class CompositeSection(MBaseModel):
    pass


class SlabSectionShape(BaseSectionShape):
    """Slab Section Shape"""

    sg: Length = Field(
        default=Length(value=0.0, unit=enUnitLength.MM), description="Sg"
    )
    bc: Length = Field(
        default=Length(value=1800.0, unit=enUnitLength.MM), description="Bc"
    )
    tc: Length = Field(
        default=Length(value=150.0, unit=enUnitLength.MM), description="tc"
    )
    hh: Length = Field(
        default=Length(value=0.0, unit=enUnitLength.MM), description="Hh"
    )


class SteelBoxGirderSectionShape(BaseSectionShape):
    """Steel Box Girder Section Shape"""

    top: Length = Field(
        default=Length(value=0.0, unit=enUnitLength.MM), description="Top"
    )
    bot: Length = Field(
        default=Length(value=100.0, unit=enUnitLength.MM), description="Bot"
    )
    b1: Length = Field(
        default=Length(value=150.0, unit=enUnitLength.MM), description="B1"
    )
    b2: Length = Field(
        default=Length(value=900.0, unit=enUnitLength.MM), description="B2"
    )
    b3: Length = Field(
        default=Length(value=150.0, unit=enUnitLength.MM), description="B3"
    )
    b4: Length = Field(
        default=Length(value=150.0, unit=enUnitLength.MM), description="B4"
    )
    b5: Length = Field(
        default=Length(value=700.0, unit=enUnitLength.MM), description="B5"
    )
    b6: Length = Field(
        default=Length(value=150.0, unit=enUnitLength.MM), description="B6"
    )
    h: Length = Field(
        default=Length(value=1000.0, unit=enUnitLength.MM), description="H"
    )
    t1: Length = Field(
        default=Length(value=25.0, unit=enUnitLength.MM), description="T1"
    )
    t2: Length = Field(
        default=Length(value=25.0, unit=enUnitLength.MM), description="T2"
    )
    tw1: Length = Field(
        default=Length(value=30.0, unit=enUnitLength.MM), description="tw1"
    )
    tw2: Length = Field(
        default=Length(value=30.0, unit=enUnitLength.MM), description="tw2"
    )


class SteelIGirderSectionShape(BaseSectionShape):
    """Steel I Girder Section Shape"""

    model_config = ConfigDict(extra="forbid")

    top: Length = Field(
        default=Length(value=0.0, unit=enUnitLength.MM), description="Top"
    )
    bot: Length = Field(
        default=Length(value=100.0, unit=enUnitLength.MM), description="Bot"
    )
    b1: Length = Field(
        default=Length(value=150.0, unit=enUnitLength.MM), description="B1"
    )
    b2: Length = Field(
        default=Length(value=900.0, unit=enUnitLength.MM), description="B2"
    )
    b3: Length = Field(
        default=Length(value=150.0, unit=enUnitLength.MM), description="B3"
    )
    b4: Length = Field(
        default=Length(value=150.0, unit=enUnitLength.MM), description="B4"
    )
    h: Length = Field(
        default=Length(value=1000.0, unit=enUnitLength.MM), description="H"
    )
    t1: Length = Field(
        default=Length(value=25.0, unit=enUnitLength.MM), description="t1"
    )
    t2: Length = Field(
        default=Length(value=25.0, unit=enUnitLength.MM), description="t2"
    )
    tw: Length = Field(
        default=Length(value=30.0, unit=enUnitLength.MM), description="tw"
    )


class SteelTubSectionShape(BaseSectionShape):
    top: Length = Field(
        default=Length(value=100.0, unit=enUnitLength.MM), description="Top"
    )
    bot: Length = Field(
        default=Length(value=250.0, unit=enUnitLength.MM), description="Bot"
    )
    b1: Length = Field(
        default=Length(value=300.0, unit=enUnitLength.MM), description="B1"
    )
    b2: Length = Field(
        default=Length(value=600.0, unit=enUnitLength.MM), description="B2"
    )
    b3: Length = Field(
        default=Length(value=300.0, unit=enUnitLength.MM), description="B3"
    )
    b4: Length = Field(
        default=Length(value=150.0, unit=enUnitLength.MM), description="B4"
    )
    b5: Length = Field(
        default=Length(value=600.0, unit=enUnitLength.MM), description="B5"
    )
    b6: Length = Field(
        default=Length(value=150.0, unit=enUnitLength.MM), description="B6"
    )
    h: Length = Field(
        default=Length(value=900.0, unit=enUnitLength.MM), description="H"
    )
    t1: Length = Field(
        default=Length(value=26.0, unit=enUnitLength.MM), description="t1"
    )
    t2: Length = Field(
        default=Length(value=26.0, unit=enUnitLength.MM), description="t2"
    )
    tw1: Length = Field(
        default=Length(value=28.0, unit=enUnitLength.MM), description="tw1"
    )
    tw2: Length = Field(
        default=Length(value=28.0, unit=enUnitLength.MM), description="tw2"
    )
    bf1: Length = Field(
        default=Length(value=200.0, unit=enUnitLength.MM), description="Bf1"
    )
    bf2: Length = Field(
        default=Length(value=200.0, unit=enUnitLength.MM), description="Bf2"
    )


class PSC1CellSectionShape(BaseSectionShape):
    jo1: bool = Field(default=True, description="JO1")
    jo2: bool = Field(default=True, description="JO2")
    jo3: bool = Field(default=True, description="JO3")
    ji1: bool = Field(default=True, description="JI1")
    ji2: bool = Field(default=True, description="JI2")
    ji3: bool = Field(default=True, description="JI3")
    ji4: bool = Field(default=True, description="JI4")
    ji5: bool = Field(default=True, description="JI5")

    ho1: Length = Field(
        default=Length(value=250.0, unit=enUnitLength.MM), description="HO1"
    )
    ho2: Length = Field(
        default=Length(value=420.0, unit=enUnitLength.MM), description="HO2"
    )
    ho2_1: Length = Field(
        default=Length(value=55.0, unit=enUnitLength.MM), description="HO2-1"
    )
    ho2_2: Length = Field(
        default=Length(value=180.0, unit=enUnitLength.MM), description="HO2-2"
    )
    ho3: Length = Field(
        default=Length(value=1680.0, unit=enUnitLength.MM), description="HO3"
    )
    ho3_1: Length = Field(
        default=Length(value=230.0, unit=enUnitLength.MM), description="HO3-1"
    )

    bo1: Length = Field(
        default=Length(value=1230.0, unit=enUnitLength.MM), description="BO1"
    )
    bo1_1: Length = Field(
        default=Length(value=440.0, unit=enUnitLength.MM), description="BO1-1"
    )
    bo1_2: Length = Field(
        default=Length(value=900.0, unit=enUnitLength.MM), description="BO1-2"
    )
    bo2: Length = Field(
        default=Length(value=600.0, unit=enUnitLength.MM), description="BO2"
    )
    bo2_1: Length = Field(
        default=Length(value=20.0, unit=enUnitLength.MM), description="BO2-1"
    )
    bo3: Length = Field(
        default=Length(value=1800.0, unit=enUnitLength.MM), description="BO3"
    )

    hi1: Length = Field(
        default=Length(value=220.0, unit=enUnitLength.MM), description="HI1"
    )
    hi2: Length = Field(
        default=Length(value=440.0, unit=enUnitLength.MM), description="HI2"
    )
    hi2_1: Length = Field(
        default=Length(value=50.0, unit=enUnitLength.MM), description="HI2-1"
    )
    hi2_2: Length = Field(
        default=Length(value=140.0, unit=enUnitLength.MM), description="HI2-2"
    )
    hi3: Length = Field(
        default=Length(value=1230.0, unit=enUnitLength.MM), description="HI3"
    )
    hi3_1: Length = Field(
        default=Length(value=880.0, unit=enUnitLength.MM), description="HI3-1"
    )
    hi4: Length = Field(
        default=Length(value=200.0, unit=enUnitLength.MM), description="HI4"
    )
    hi4_1: Length = Field(
        default=Length(value=25.0, unit=enUnitLength.MM), description="HI4-1"
    )
    hi4_2: Length = Field(
        default=Length(value=90.0, unit=enUnitLength.MM), description="HI4-2"
    )
    hi5: Length = Field(
        default=Length(value=210.0, unit=enUnitLength.MM), description="HI5"
    )

    bi1: Length = Field(
        default=Length(value=1910.0, unit=enUnitLength.MM), description="BI1"
    )
    bi1_1: Length = Field(
        default=Length(value=890.0, unit=enUnitLength.MM), description="BI1-1"
    )
    bi1_2: Length = Field(
        default=Length(value=1560.0, unit=enUnitLength.MM), description="BI1-2"
    )
    bi2_1: Length = Field(
        default=Length(value=1690.0, unit=enUnitLength.MM), description="BI2-1"
    )
    bi3: Length = Field(
        default=Length(value=1480.0, unit=enUnitLength.MM), description="BI3"
    )
    bi3_1: Length = Field(
        default=Length(value=570.0, unit=enUnitLength.MM), description="BI3-1"
    )
    bi3_2: Length = Field(
        default=Length(value=1100.0, unit=enUnitLength.MM), description="BI3-2"
    )


class PSC2CellSectionShape(BaseSectionShape):
    # joint = ["JO1", "JO2", "JO3", "JI1", "JI2", "JI3", "JI4", "JI5"]
    jo1: bool = Field(default=True, description="JO1")
    jo2: bool = Field(default=True, description="JO2")
    jo3: bool = Field(default=True, description="JO3")
    ji1: bool = Field(default=True, description="JI1")
    ji2: bool = Field(default=True, description="JI2")
    ji3: bool = Field(default=True, description="JI3")
    ji4: bool = Field(default=True, description="JI4")
    ji5: bool = Field(default=True, description="JI5")

    # vSizeA = ["HO1","HO2", "HO2-1", "HO2-2", "HO3", "HO3-1"]
    ho1: Length = Field(
        default=Length(value=230.0, unit=enUnitLength.MM), description="HO1"
    )
    ho2: Length = Field(
        default=Length(value=420.0, unit=enUnitLength.MM), description="HO2"
    )
    ho2_1: Length = Field(
        default=Length(value=55.0, unit=enUnitLength.MM), description="HO2-1"
    )
    ho2_2: Length = Field(
        default=Length(value=180.0, unit=enUnitLength.MM), description="HO2-2"
    )
    ho3: Length = Field(
        default=Length(value=1680.0, unit=enUnitLength.MM), description="HO3"
    )
    ho3_1: Length = Field(
        default=Length(value=230.0, unit=enUnitLength.MM), description="HO3-1"
    )

    # vSizeB = ["BO1", "BO1-1", "BO1-2", "BO2", "BO2-1", "BO3"]
    bo1: Length = Field(
        default=Length(value=1230.0, unit=enUnitLength.MM), description="BO1"
    )
    bo1_1: Length = Field(
        default=Length(value=440.0, unit=enUnitLength.MM), description="BO1-1"
    )
    bo1_2: Length = Field(
        default=Length(value=900.0, unit=enUnitLength.MM), description="BO1-2"
    )
    bo2: Length = Field(
        default=Length(value=600.0, unit=enUnitLength.MM), description="BO2"
    )
    bo2_1: Length = Field(
        default=Length(value=20.0, unit=enUnitLength.MM), description="BO2-1"
    )
    bo3: Length = Field(
        default=Length(value=1800.0, unit=enUnitLength.MM), description="BO3"
    )

    # vSizeC = ["HI1", "HI2", "HI2-1", "HI2-2", "HI3", "HI3-1", "HI4", "HI4-1", "HI4-2", "HI5"]
    hi1: Length = Field(
        default=Length(value=220.0, unit=enUnitLength.MM), description="HI1"
    )
    hi2: Length = Field(
        default=Length(value=440.0, unit=enUnitLength.MM), description="HI2"
    )
    hi2_1: Length = Field(
        default=Length(value=50.0, unit=enUnitLength.MM), description="HI2-1"
    )
    hi2_2: Length = Field(
        default=Length(value=140.0, unit=enUnitLength.MM), description="HI2-2"
    )
    hi3: Length = Field(
        default=Length(value=1230.0, unit=enUnitLength.MM), description="HI3"
    )
    hi3_1: Length = Field(
        default=Length(value=880.0, unit=enUnitLength.MM), description="HI3-1"
    )
    hi4: Length = Field(
        default=Length(value=200.0, unit=enUnitLength.MM), description="HI4"
    )
    hi4_1: Length = Field(
        default=Length(value=25.0, unit=enUnitLength.MM), description="HI4-1"
    )
    hi4_2: Length = Field(
        default=Length(value=90.0, unit=enUnitLength.MM), description="HI4-2"
    )
    hi5: Length = Field(
        default=Length(value=210.0, unit=enUnitLength.MM), description="HI5"
    )

    # vSizeD = ["BI1", "BI1-1", "BI1-2", "BI2-1", "BI3", "BI3-1", "BI3-2", "BI4"]
    bi1: Length = Field(
        default=Length(value=1910.0, unit=enUnitLength.MM), description="BI1"
    )
    bi1_1: Length = Field(
        default=Length(value=890.0, unit=enUnitLength.MM), description="BI1-1"
    )
    bi1_2: Length = Field(
        default=Length(value=1560.0, unit=enUnitLength.MM), description="BI1-2"
    )
    bi2_1: Length = Field(
        default=Length(value=1690.0, unit=enUnitLength.MM), description="BI2-1"
    )
    bi3: Length = Field(
        default=Length(value=1480.0, unit=enUnitLength.MM), description="BI3"
    )
    bi3_1: Length = Field(
        default=Length(value=570.0, unit=enUnitLength.MM), description="BI3-1"
    )
    bi3_2: Length = Field(
        default=Length(value=1100.0, unit=enUnitLength.MM), description="BI3-2"
    )
    bi4: Length = Field(
        default=Length(value=100.0, unit=enUnitLength.MM), description="BI4"
    )


class PSC_ISectionShape(BaseSectionShape):
    # joint = ["J1", "JL1", "JL2", "JL3", "JL4", "JR1", "JR2", "JR3", "JR4"]
    # joint = [True, True, True, True, True, True, True, True, True]
    j1: bool = Field(default=True, description="J1")
    jl1: bool = Field(default=True, description="JL1")
    jl2: bool = Field(default=True, description="JL2")
    jl3: bool = Field(default=True, description="JL3")
    jl4: bool = Field(default=True, description="JL4")
    jr1: bool = Field(default=True, description="JR1")
    jr2: bool = Field(default=True, description="JR2")
    jr3: bool = Field(default=True, description="JR3")
    jr4: bool = Field(default=True, description="JR4")
    # vSizeA = ["H1", "HL1", "HL2", "HL2-1", "HL2-2", "HL3", "HL4", "HL4-1", "HL4-2", "HL5"]
    # vSizeA = [2450, 260, 440, 50, 200, 1130, 400, 70, 220, 270]
    h1: Length = Field(
        default=Length(value=2450.0, unit=enUnitLength.MM), description="H1"
    )
    hl1: Length = Field(
        default=Length(value=260.0, unit=enUnitLength.MM), description="HL1"
    )
    hl2: Length = Field(
        default=Length(value=440.0, unit=enUnitLength.MM), description="HL2"
    )
    hl2_1: Length = Field(
        default=Length(value=50.0, unit=enUnitLength.MM), description="HL2-1"
    )
    hl2_2: Length = Field(
        default=Length(value=200.0, unit=enUnitLength.MM), description="HL2-2"
    )
    hl3: Length = Field(
        default=Length(value=1130.0, unit=enUnitLength.MM), description="HL3"
    )
    hl4: Length = Field(
        default=Length(value=400.0, unit=enUnitLength.MM), description="HL4"
    )
    hl4_1: Length = Field(
        default=Length(value=70.0, unit=enUnitLength.MM), description="HL4-1"
    )
    hl4_2: Length = Field(
        default=Length(value=220.0, unit=enUnitLength.MM), description="HL4-2"
    )
    hl5: Length = Field(
        default=Length(value=270.0, unit=enUnitLength.MM), description="HL5"
    )
    # vSizeB = ["BL1", "BL2", "BL2-1", "BL2-2","BL4", "BL4-1", "BL4-2"]
    # vSizeB = [160, 1360, 440, 900, 800, 290, 520]
    bl1: Length = Field(
        default=Length(value=160.0, unit=enUnitLength.MM), description="BL1"
    )
    bl2: Length = Field(
        default=Length(value=1360.0, unit=enUnitLength.MM), description="BL2"
    )
    bl2_1: Length = Field(
        default=Length(value=440.0, unit=enUnitLength.MM), description="BL2-1"
    )
    bl2_2: Length = Field(
        default=Length(value=900.0, unit=enUnitLength.MM), description="BL2-2"
    )
    bl4: Length = Field(
        default=Length(value=800.0, unit=enUnitLength.MM), description="BL4"
    )
    bl4_1: Length = Field(
        default=Length(value=290.0, unit=enUnitLength.MM), description="BL4-1"
    )
    bl4_2: Length = Field(
        default=Length(value=520.0, unit=enUnitLength.MM), description="BL4-2"
    )
    # vSizeC = ["HR1", "HR2", "HR2-1", "HR2-2", "HR3", "HR4", "HR4-1", "HR4-2", "HR5"]
    # vSizeC = [260, 480, 30, 220, 1090, 440, 50, 240, 250]
    hr1: Length = Field(
        default=Length(value=260.0, unit=enUnitLength.MM), description="HR1"
    )
    hr2: Length = Field(
        default=Length(value=480.0, unit=enUnitLength.MM), description="HR2"
    )
    hr2_1: Length = Field(
        default=Length(value=30.0, unit=enUnitLength.MM), description="HR2-1"
    )
    hr2_2: Length = Field(
        default=Length(value=220.0, unit=enUnitLength.MM), description="HR2-2"
    )
    hr3: Length = Field(
        default=Length(value=1090.0, unit=enUnitLength.MM), description="HR3"
    )
    hr4: Length = Field(
        default=Length(value=440.0, unit=enUnitLength.MM), description="HR4"
    )
    hr4_1: Length = Field(
        default=Length(value=50.0, unit=enUnitLength.MM), description="HR4-1"
    )
    hr4_2: Length = Field(
        default=Length(value=240.0, unit=enUnitLength.MM), description="HR4-2"
    )
    hr5: Length = Field(
        default=Length(value=250.0, unit=enUnitLength.MM), description="HR5"
    )
    # vSizeD = ["BR1", "BR2", "BR2-1", "BR2-2", "BR4", "BR4-1", "BR4-2"]
    # vSizeD = [180, 1340, 460, 850, 820, 350, 570]
    br1: Length = Field(
        default=Length(value=180.0, unit=enUnitLength.MM), description="BR1"
    )
    br2: Length = Field(
        default=Length(value=1340.0, unit=enUnitLength.MM), description="BR2"
    )
    br2_1: Length = Field(
        default=Length(value=460.0, unit=enUnitLength.MM), description="BR2-1"
    )
    br2_2: Length = Field(
        default=Length(value=850.0, unit=enUnitLength.MM), description="BR2-2"
    )
    br4: Length = Field(
        default=Length(value=820.0, unit=enUnitLength.MM), description="BR4"
    )
    br4_1: Length = Field(
        default=Length(value=350.0, unit=enUnitLength.MM), description="BR4-1"
    )
    br4_2: Length = Field(
        default=Length(value=570.0, unit=enUnitLength.MM), description="BR4-2"
    )


class PSC_TSectionShape(BaseSectionShape):
    # joint = ["J1", "JL1", "JL2", "JL3", "JL4", "JR1", "JR2", "JR3", "JR4"]
    # joint = [True, True, True, True, True, True, True, True, True]
    j1: bool = Field(default=True, description="J1")
    jl1: bool = Field(default=True, description="JL1")
    jl2: bool = Field(default=True, description="JL2")
    jl3: bool = Field(default=True, description="JL3")
    jl4: bool = Field(default=True, description="JL4")
    jr1: bool = Field(default=True, description="JR1")
    jr2: bool = Field(default=True, description="JR2")
    jr3: bool = Field(default=True, description="JR3")
    jr4: bool = Field(default=True, description="JR4")
    # vSizeA = ["H1", "HL1", "HL2", "HL3", "BL1", "BL2", "BL3", "BL4"]
    # vSizeA = [2170, 290, 130, 1800, 210, 130, 1630, 1830]
    h1: Length = Field(
        default=Length(value=2170.0, unit=enUnitLength.MM), description="H1"
    )
    hl1: Length = Field(
        default=Length(value=290.0, unit=enUnitLength.MM), description="HL1"
    )
    hl2: Length = Field(
        default=Length(value=130.0, unit=enUnitLength.MM), description="HL2"
    )
    hl3: Length = Field(
        default=Length(value=1800.0, unit=enUnitLength.MM), description="HL3"
    )
    bl1: Length = Field(
        default=Length(value=210.0, unit=enUnitLength.MM), description="BL1"
    )
    bl2: Length = Field(
        default=Length(value=130.0, unit=enUnitLength.MM), description="BL2"
    )
    bl3: Length = Field(
        default=Length(value=1630.0, unit=enUnitLength.MM), description="BL3"
    )
    bl4: Length = Field(
        default=Length(value=1830.0, unit=enUnitLength.MM), description="BL4"
    )
    # vSizeB = ["HL2-1", "HL2-2", "HL3-1", "HL3-2", "BL2-1", "BL2-2",  "BL3-1", "BL3-2"]
    # vSizeB = [25, 80, 1430, 850, 60, 30, 810, 1420]
    hl2_1: Length = Field(
        default=Length(value=25.0, unit=enUnitLength.MM), description="HL2-1"
    )
    hl2_2: Length = Field(
        default=Length(value=80.0, unit=enUnitLength.MM), description="HL2-2"
    )
    hl3_1: Length = Field(
        default=Length(value=1430.0, unit=enUnitLength.MM), description="HL3-1"
    )
    hl3_2: Length = Field(
        default=Length(value=850.0, unit=enUnitLength.MM), description="HL3-2"
    )
    bl2_1: Length = Field(
        default=Length(value=60.0, unit=enUnitLength.MM), description="BL2-1"
    )
    bl2_2: Length = Field(
        default=Length(value=30.0, unit=enUnitLength.MM), description="BL2-2"
    )
    bl3_1: Length = Field(
        default=Length(value=810.0, unit=enUnitLength.MM), description="BL3-1"
    )
    bl3_2: Length = Field(
        default=Length(value=1420.0, unit=enUnitLength.MM), description="BL3-2"
    )
    # vSizeC = ["HR1", "HR2", "HR3", "BR1", "BR2", "BR3", "BR4"]
    # vSizeC = [290, 280, 1700, 190, 160, 1600, 1850]
    hr1: Length = Field(
        default=Length(value=290.0, unit=enUnitLength.MM), description="HR1"
    )
    hr2: Length = Field(
        default=Length(value=280.0, unit=enUnitLength.MM), description="HR2"
    )
    hr3: Length = Field(
        default=Length(value=1700.0, unit=enUnitLength.MM), description="HR3"
    )
    br1: Length = Field(
        default=Length(value=190.0, unit=enUnitLength.MM), description="BR1"
    )
    br2: Length = Field(
        default=Length(value=160.0, unit=enUnitLength.MM), description="BR2"
    )
    br3: Length = Field(
        default=Length(value=1600.0, unit=enUnitLength.MM), description="BR3"
    )
    br4: Length = Field(
        default=Length(value=1850.0, unit=enUnitLength.MM), description="BR4"
    )
    # vSizeD = ["HR2-1", "HR2-2", "HR3-1", "HR3-2", "BR2-1", "BR2-2", "BR3-1", "BR3-2"]
    # vSizeD = [50, 160, 1400, 850, 60, 20, 800, 1390]
    hr2_1: Length = Field(
        default=Length(value=50.0, unit=enUnitLength.MM), description="HR2-1"
    )
    hr2_2: Length = Field(
        default=Length(value=160.0, unit=enUnitLength.MM), description="HR2-2"
    )
    hr3_1: Length = Field(
        default=Length(value=1400.0, unit=enUnitLength.MM), description="HR3-1"
    )
    hr3_2: Length = Field(
        default=Length(value=850.0, unit=enUnitLength.MM), description="HR3-2"
    )
    br2_1: Length = Field(
        default=Length(value=60.0, unit=enUnitLength.MM), description="BR2-1"
    )
    br2_2: Length = Field(
        default=Length(value=20.0, unit=enUnitLength.MM), description="BR2-2"
    )
    br3_1: Length = Field(
        default=Length(value=800.0, unit=enUnitLength.MM), description="BR3-1"
    )
    br3_2: Length = Field(
        default=Length(value=1390.0, unit=enUnitLength.MM), description="BR3-2"
    )


class SlabSection(MBaseModel):
    shape: SlabSectionShape = Field(default=SlabSectionShape())
    material: SectionMaterial = Field(default=SectionMaterial())


"""Section"""
"""
Deck Type: 1a - Steel Decks
Section Shape: Box Girder
"""


class SteelBoxGirderSection(MBaseModel):
    shape: SteelBoxGirderSectionShape = Field(
        default=SteelBoxGirderSectionShape()
    )
    material: SectionMaterial = Field(default=SectionMaterial())

    @staticmethod
    def get_group():
        return 1

    def calc_section_coordinate(self) -> SectionCoordinate:
        shape = self.shape

        ref_size = [shape.top.value, shape.bot.value]
        v_size = [
            shape.b1.value,
            shape.b2.value,
            shape.b3.value,
            shape.b4.value,
            shape.b5.value,
            shape.b6.value,
            shape.h.value,
            shape.t1.value,
            shape.t2.value,
            shape.tw1.value,
            shape.tw2.value,
        ]

        outer, inner, comp = steel_box(vSize=v_size, refSize=ref_size)
        return SectionCoordinate(outer=outer, inner=inner, comp=comp)


"""
Deck Type: 1b - SteelDecks
Section Shape: Box Girder
"""


class SteelIGirderSection(MBaseModel):
    shape: SteelIGirderSectionShape = Field(
        default=SteelIGirderSectionShape()
    )
    material: SectionMaterial = Field(default=SectionMaterial())

    @staticmethod
    def get_group():
        return 2

    def calc_section_coordinate(self) -> SectionCoordinate:
        shape = self.shape

        ref_size = [shape.top.value, shape.bot.value]
        v_size = [
            shape.b1.value,
            shape.b2.value,
            shape.b3.value,
            shape.b4.value,
            shape.h.value,
            shape.t1.value,
            shape.t2.value,
            shape.tw.value,
        ]

        # Calculate the self cooridnates
        outer, inner, comp = steel_i(vSize=v_size, refSize=ref_size)
        return SectionCoordinate(outer=outer, inner=inner, comp=comp)


"""
Section for Composite Section
"""


class SteelTubSection(MBaseModel):
    shape: SteelTubSectionShape = Field(default=SteelTubSectionShape())
    material: SectionMaterial = Field(default=SectionMaterial())


"""Composite section"""
"""
Deck Type: 2 - Composite Decks
Section Shape: Steel Box Girder
"""


class CompositeBoxGirderSection(CompositeSection):
    girder_section: SteelBoxGirderSection = Field(
        default=SteelBoxGirderSection()
    )
    slab_section: SlabSection = Field(default=SlabSection())

    @staticmethod
    def get_group():
        return 3

    def calc_section_coordinate(self) -> SectionCoordinate:
        girder_shape = self.girder_section.shape
        slab_shape = self.slab_section.shape

        ref_size = [slab_shape.sg.value, girder_shape.top.value, girder_shape.bot.value]
        slab = [slab_shape.bc.value, slab_shape.tc.value, slab_shape.hh.value]
        v_size = [
            girder_shape.b1.value,
            girder_shape.b2.value,
            girder_shape.b3.value,
            girder_shape.b4.value,
            girder_shape.b5.value,
            girder_shape.b6.value,
            girder_shape.h.value,
            girder_shape.t1.value,
            girder_shape.t2.value,
            girder_shape.tw1.value,
            girder_shape.tw2.value,
        ]
        outer, inner, comp = composite_steel_box(
            vSize=v_size, slab=slab, refSize=ref_size
        )
        return SectionCoordinate(outer=outer, inner=inner, comp=comp)


"""
Deck Type: 2 - Composite Decks
Section Shape: Steel I Girder
"""


class CompositeIGirderSection(CompositeSection):
    girder_section: SteelIGirderSection = Field(default=SteelIGirderSection())
    slab_section: SlabSection = Field(default=SlabSection())

    @staticmethod
    def get_group():
        return 3

    def calc_section_coordinate(self) -> SectionCoordinate:
        girder_shape = self.girder_section.shape
        slab_shape = self.slab_section.shape

        ref_size = [slab_shape.sg.value, girder_shape.top.value, girder_shape.bot.value]
        slab = [slab_shape.bc.value, slab_shape.tc.value, slab_shape.hh.value]
        v_size = [
            girder_shape.b1.value,
            girder_shape.b2.value,
            girder_shape.b3.value,
            girder_shape.b4.value,
            girder_shape.h.value,
            girder_shape.t1.value,
            girder_shape.t2.value,
            girder_shape.tw.value,
        ]

        outer, inner, comp = composite_steel_i(
            vSize=v_size, slab=slab, refSize=ref_size
        )
        return SectionCoordinate(outer=outer, inner=inner, comp=comp)


"""
Deck Type: 2 - Composite Decks
Section Shape: Steel Tub
"""


class CompositeTubSection(CompositeSection):
    girder_section: SteelTubSection = Field(default=SteelTubSection())
    slab_section: SlabSection = Field(default=SlabSection())

    @staticmethod
    def get_group():
        return 3

    def calc_section_coordinate(self) -> SectionCoordinate:
        girder_shape = self.girder_section.shape
        slab_shape = self.slab_section.shape

        ref_size = [slab_shape.sg.value, girder_shape.top.value, girder_shape.bot.value]
        slab = [slab_shape.bc.value, slab_shape.tc.value, slab_shape.hh.value]
        v_size = [
            girder_shape.b1.value,
            girder_shape.b2.value,
            girder_shape.b3.value,
            girder_shape.b4.value,
            girder_shape.b5.value,
            girder_shape.b6.value,
            girder_shape.h.value,
            girder_shape.t1.value,
            girder_shape.t2.value,
            girder_shape.tw1.value,
            girder_shape.tw2.value,
            girder_shape.bf1.value,
            girder_shape.bf2.value,
        ]

        outer, inner, comp = composite_steel_tub(
            vSize=v_size, slab=slab, refSize=ref_size
        )
        return SectionCoordinate(outer=outer, inner=inner, comp=comp)


"""Concrete"""
"""
Deck Type: 3 - Concrete Decks
Section Shape: PSC-1Cell
"""


class PSC1CellSection(MBaseModel):
    shape: PSC1CellSectionShape = Field(default=PSC1CellSectionShape())
    material: SectionMaterial = Field(default=SectionMaterial())

    @staticmethod
    def get_group():
        return 4

    def calc_section_coordinate(self) -> SectionCoordinate:
        shape = self.shape

        joint = [
            shape.jo1,
            shape.jo2,
            shape.jo3,
            shape.ji1,
            shape.ji2,
            shape.ji3,
            shape.ji4,
            shape.ji5,
        ]
        v_size_a = [
            shape.ho1.value,
            shape.ho2.value,
            shape.ho2_1.value,
            shape.ho2_2.value,
            shape.ho3.value,
            shape.ho3_1.value,
        ]
        v_size_b = [
            shape.bo1.value,
            shape.bo1_1.value,
            shape.bo1_2.value,
            shape.bo2.value,
            shape.bo2_1.value,
            shape.bo3.value,
        ]
        v_size_c = [
            shape.hi1.value,
            shape.hi2.value,
            shape.hi2_1.value,
            shape.hi2_2.value,
            shape.hi3.value,
            shape.hi3_1.value,
            shape.hi4.value,
            shape.hi4_1.value,
            shape.hi4_2.value,
            shape.hi5.value,
        ]
        v_size_d = [
            shape.bi1.value,
            shape.bi1_1.value,
            shape.bi1_2.value,
            shape.bi2_1.value,
            shape.bi3.value,
            shape.bi3_1.value,
            shape.bi3_2.value,
        ]

        outer, inner, comp = psc_1cell(
            vSizeA=v_size_a,
            vSizeB=v_size_b,
            vSizeC=v_size_c,
            vSizeD=v_size_d,
            joint=joint,
        )
        return SectionCoordinate(outer=outer, inner=inner, comp=comp)


"""
Deck Type: 3 - Concrete Decks
Section Shape: PSC-2Cell
"""


class PSC2CellSection(MBaseModel):
    shape: PSC2CellSectionShape = Field(default=PSC2CellSectionShape())
    material: SectionMaterial = Field(default=SectionMaterial())

    @staticmethod
    def get_group():
        return 4

    def calc_section_coordinate(self) -> SectionCoordinate:
        shape = self.shape

        joint = [
            shape.jo1,
            shape.jo2,
            shape.jo3,
            shape.ji1,
            shape.ji2,
            shape.ji3,
            shape.ji4,
            shape.ji5,
        ]
        v_size_a = [
            shape.ho1.value,
            shape.ho2.value,
            shape.ho2_1.value,
            shape.ho2_2.value,
            shape.ho3.value,
            shape.ho3_1.value,
        ]
        v_size_b = [
            shape.bo1.value,
            shape.bo1_1.value,
            shape.bo1_2.value,
            shape.bo2.value,
            shape.bo2_1.value,
            shape.bo3.value,
        ]
        v_size_c = [
            shape.hi1.value,
            shape.hi2.value,
            shape.hi2_1.value,
            shape.hi2_2.value,
            shape.hi3.value,
            shape.hi3_1.value,
            shape.hi4.value,
            shape.hi4_1.value,
            shape.hi4_2.value,
            shape.hi5.value,
        ]
        v_size_d = [
            shape.bi1.value,
            shape.bi1_1.value,
            shape.bi1_2.value,
            shape.bi2_1.value,
            shape.bi3.value,
            shape.bi3_1.value,
            shape.bi3_2.value,
            shape.bi4.value,
        ]

        outer, inner, comp = psc_2cell(
            vSizeA=v_size_a,
            vSizeB=v_size_b,
            vSizeC=v_size_c,
            vSizeD=v_size_d,
            joint=joint,
        )
        return SectionCoordinate(outer=outer, inner=inner, comp=comp)


"""
Deck Type: 3 - Concrete Decks
Section Shape: PSC-I
"""


class PSC_ISection(MBaseModel):
    shape: PSC_ISectionShape = Field(default=PSC_ISectionShape())
    material: SectionMaterial = Field(default=SectionMaterial())

    @staticmethod
    def get_group():
        return 4

    def calc_section_coordinate(self) -> SectionCoordinate:
        shape = self.shape

        joint = [
            shape.j1,
            shape.jl1,
            shape.jl2,
            shape.jl3,
            shape.jl4,
            shape.jr1,
            shape.jr2,
            shape.jr3,
            shape.jr4,
        ]
        v_size_a = [
            shape.h1.value,
            shape.hl1.value,
            shape.hl2.value,
            shape.hl2_1.value,
            shape.hl2_2.value,
            shape.hl3.value,
            shape.hl4.value,
            shape.hl4_1.value,
            shape.hl4_2.value,
            shape.hl5.value,
        ]
        v_size_b = [
            shape.bl1.value,
            shape.bl2.value,
            shape.bl2_1.value,
            shape.bl2_2.value,
            shape.bl4.value,
            shape.bl4_1.value,
            shape.bl4_2.value,
        ]
        v_size_c = [
            shape.hr1.value,
            shape.hr2.value,
            shape.hr2_1.value,
            shape.hr2_2.value,
            shape.hr3.value,
            shape.hr4.value,
            shape.hr4_1.value,
            shape.hr4_2.value,
            shape.hr5.value,
        ]
        v_size_d = [
            shape.br1.value,
            shape.br2.value,
            shape.br2_1.value,
            shape.br2_2.value,
            shape.br4.value,
            shape.br4_1.value,
            shape.br4_2.value,
        ]

        outer, inner, comp = psc_I(
            vSizeA=v_size_a,
            vSizeB=v_size_b,
            vSizeC=v_size_c,
            vSizeD=v_size_d,
            joint=joint,
        )
        return SectionCoordinate(outer=outer, inner=inner, comp=comp)


"""
Deck Type: 3 - Concrete Decks
Section Shape: PSC-T
"""


class PSC_TSection(MBaseModel):
    shape: PSC_TSectionShape = Field(default=PSC_TSectionShape())
    material: SectionMaterial = Field(default=SectionMaterial())

    @staticmethod
    def get_group():
        return 4

    def calc_section_coordinate(self) -> SectionCoordinate:
        shape = self.shape

        joint = [
            shape.j1,
            shape.jl1,
            shape.jl2,
            shape.jl3,
            shape.jl4,
            shape.jr1,
            shape.jr2,
            shape.jr3,
            shape.jr4,
        ]
        v_size_a = [
            shape.h1.value,
            shape.hl1.value,
            shape.hl2.value,
            shape.hl3.value,
            shape.bl1.value,
            shape.bl2.value,
            shape.bl3.value,
            shape.bl4.value,
        ]
        v_size_b = [
            shape.hl2_1.value,
            shape.hl2_2.value,
            shape.hl3_1.value,
            shape.hl3_2.value,
            shape.bl2_1.value,
            shape.bl2_2.value,
            shape.bl3_1.value,
            shape.bl3_2.value,
        ]
        v_size_c = [
            shape.hr1.value,
            shape.hr2.value,
            shape.hr3.value,
            shape.br1.value,
            shape.br2.value,
            shape.br3.value,
            shape.br4.value,
        ]
        v_size_d = [
            shape.hr2_1.value,
            shape.hr2_2.value,
            shape.hr3_1.value,
            shape.hr3_2.value,
            shape.br2_1.value,
            shape.br2_2.value,
            shape.br3_1.value,
            shape.br3_2.value,
        ]

        outer, inner, comp = psc_T(
            vSizeA=v_size_a,
            vSizeB=v_size_b,
            vSizeC=v_size_c,
            vSizeD=v_size_d,
            joint=joint,
        )
        return SectionCoordinate(outer=outer, inner=inner, comp=comp)
