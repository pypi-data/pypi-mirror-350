from pydantic import Field, ConfigDict
from moapy.auto_convert import MBaseModel
from moapy.steel_pre import SteelMomentModificationFactor, SteelLength
from moapy.enum_pre import enum_to_list, enAluminumMaterial_AA, enUnitLength, enUnitSystem
from moapy.data_pre import EffectiveLengthFactor, Length

class AluMaterial(MBaseModel):
    """
    Aluminum Material Specification
    """
    code: str = Field(
        default='AA(A)',
        description="The term AA(A) refers to a specific designation under the Aluminum Association standards, commonly used in North America to classify aluminum alloys.",
        readOnly=True,
        title="Aluminum Alloy Code"
    )
    matl: str = Field(
        default='2014-T6',
        description="This field allows the user to select a specific aluminum alloy material, with '2014-T6' being a common option. It represents a high-strength aluminum alloy used in various structural applications.",
        title="Material Selection",
        enum=enum_to_list(enAluminumMaterial_AA)
    )
    product: str = Field(
        default='Extrusions',
        description="Defines the product form of the aluminum material, such as extrusions, which is a process that shapes aluminum into specific profiles by forcing it through a die.",
        readOnly=True,
        title="Product Form"
    )

    model_config = ConfigDict(
        title="Material",
        json_schema_extra={
            "description": "This model defines key attributes of an aluminum material, including the alloy designation (code), selectable material type (matl), and product form (product). It provides structured information useful for categorizing and selecting aluminum materials for manufacturing processes."
        }
    )

class AluMomentModificationFactor(SteelMomentModificationFactor):
    """
    Steel DB Moment Modification Factor
    """
    cb: float = Field(default=1.0, title="Cb", description="Coefficient that accounts for moment gradient along a beam’s length")
    m: float = Field(default=0.67, gt=0, description="Constant determined from Table 4.8.1-1")

    model_config = ConfigDict(
        title="Aluminum Moment Modification Factor",
        json_schema_extra={
            "description": "A coefficient used in structural design to adjust the moments in a structure based on specific conditions or types of support. It is often applied to improve the assessment of loads and moments on columns, beams, or other structural elements."
        }
    )

class AluminumOptions(MBaseModel):
    length: SteelLength = Field(default_factory=SteelLength, title="Unbraced Length", description="Unbraced length for aluminum beam design")
    eff_len: EffectiveLengthFactor = Field(default_factory=EffectiveLengthFactor, title="Effective Length Factor", description="Effective length factor for aluminum beam design")
    factor: AluMomentModificationFactor = Field(default_factory=AluMomentModificationFactor, title="Moment Modification Factor", description="Moment modification factor for aluminum beam design")

    model_config = ConfigDict(
        title="Design Parameters",
        json_schema_extra={
            "description": "Design parameters for aluminum beam design"
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(length=SteelLength.create_default(enUnitSystem.US), eff_len=EffectiveLengthFactor(), factor=AluMomentModificationFactor())
        else:
            return cls(length=SteelLength.create_default(enUnitSystem.SI), eff_len=EffectiveLengthFactor(), factor=AluMomentModificationFactor())
