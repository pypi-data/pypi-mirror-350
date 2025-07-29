from enum import StrEnum
from typing import Annotated, Literal, Union
from pydantic import ConfigDict, Field
from moapy.auto_convert import MBaseModel
from moapy.data_pre import Length
from moapy.enum_pre import enUnitLength
from moapy.plugins.temperature_gradient.eurocode.data_pre import (
    CompositeBoxGirderSection,
    CompositeIGirderSection,
    CompositeTubSection,
    PSC1CellSection,
    PSC2CellSection,
    SteelBoxGirderSection,
    SteelIGirderSection,
    PSC_ISection,
    PSC_TSection,
)


class SteelBoxGirderInput(MBaseModel):
    model_config = ConfigDict(title="Box Girder")
    deck_type: Literal["1a - Steel Decks"] = Field("1a - Steel Decks")
    section_type: Literal["Box Girder"] = Field("Box Girder")
    section: SteelBoxGirderSection = Field(default=SteelBoxGirderSection())


class SteelIGirderInput(MBaseModel):
    model_config = ConfigDict(title="I Girder")
    deck_type: Literal["1b - Steel Decks"] = Field("1b - Steel Decks")
    section_type: Literal["I Girder"] = Field("I Girder")
    section: SteelIGirderSection = Field(default=SteelIGirderSection())


class CompositeBoxGirderInput(MBaseModel):
    model_config = ConfigDict(title="Steel Box Girder")
    deck_type: Literal["2 - Composite Decks"] = Field("2 - Composite Decks")
    section_type: Literal["Steel Box Girder"] = Field("Steel Box Girder")
    section: CompositeBoxGirderSection = Field(default=CompositeBoxGirderSection())


class CompositeIGirderInput(MBaseModel):
    model_config = ConfigDict(title="Steel I Girder")
    deck_type: Literal["2 - Composite Decks"] = Field("2 - Composite Decks")
    section_type: Literal["Steel I Girder"] = Field("Steel I Girder")
    section: CompositeIGirderSection = Field(default=CompositeIGirderSection())


class CompositeTubGirderInput(MBaseModel):
    model_config = ConfigDict(title="Steel Tub Girder")
    deck_type: Literal["2 - Composite Decks"] = Field("2 - Composite Decks")
    section_type: Literal["Steel Tub Girder"] = Field("Steel Tub Girder")
    section: CompositeTubSection = Field(default=CompositeTubSection())


class PSC1CellInput(MBaseModel):
    model_config = ConfigDict(title="PSC-1Cell")
    deck_type: Literal["3 - Concrete Decks"] = Field("3 - Concrete Decks")
    section_type: Literal["PSC-1Cell"] = Field("PSC-1Cell")
    section: PSC1CellSection = Field(default=PSC1CellSection())


class PSC2CellInput(MBaseModel):
    model_config = ConfigDict(title="PSC-2Cell")
    deck_type: Literal["3 - Concrete Decks"] = Field("3 - Concrete Decks")
    section_type: Literal["PSC-2Cell"] = Field("PSC-2Cell")
    section: PSC2CellSection = Field(default=PSC2CellSection())


class PSC_I_Input(MBaseModel):
    model_config = ConfigDict(title="PSC-I")
    deck_type: Literal["3 - Concrete Decks"] = Field("3 - Concrete Decks")
    section_type: Literal["PSC-I"] = Field("PSC-I")
    section: PSC_ISection = Field(default=PSC_ISection())


class PSC_T_Input(MBaseModel):
    model_config = ConfigDict(title="PSC-T")
    deck_type: Literal["3 - Concrete Decks"] = Field("3 - Concrete Decks")
    section_type: Literal["PSC-T"] = Field("PSC-T")
    section: PSC_TSection = Field(default=PSC_TSection())


SectionInput = Annotated[
    Union[
        SteelBoxGirderInput,
        SteelIGirderInput,
        CompositeBoxGirderInput,
        CompositeIGirderInput,
        CompositeTubGirderInput,
        PSC1CellInput,
        PSC2CellInput,
        PSC_I_Input,
        PSC_T_Input,
    ],
    Field(
        default=CompositeBoxGirderInput(),
        title="Section Input",
        discriminator="section_type",
    ),
]

"""Surface Type"""


class SurfaceType(StrEnum):
    UNSURFACED = "Unsurfaced"
    WATERPROOFED = "Waterproofed"
    THICKNESS = "Thickness"


class UnSurfacedTypeInput(MBaseModel):
    model_config = ConfigDict(title="Unsurfaced")
    surfacing_type: Literal[SurfaceType.UNSURFACED] = Field(
        default=SurfaceType.UNSURFACED, description="Surfacing Type"
    )


class WaterProofedTypeInput(MBaseModel):
    model_config = ConfigDict(title="Waterproofed")
    surfacing_type: Literal[SurfaceType.WATERPROOFED] = Field(
        default=SurfaceType.WATERPROOFED, description="Surfacing Type"
    )


class SurfacedTypeInput(MBaseModel):
    model_config = ConfigDict(title="Thickness")
    surfacing_type: Literal[SurfaceType.THICKNESS] = Field(
        default=SurfaceType.THICKNESS, description="Surfacing Type"
    )
    surfacing_thickness: Length = Field(
        default=Length(value=30.0, unit=enUnitLength.MM),
        description="Surfacing Thickness",
    )


SurfacingTypeInput = Annotated[
    Union[
        UnSurfacedTypeInput,
        WaterProofedTypeInput,
        SurfacedTypeInput,
    ],
    Field(
        default=SurfacedTypeInput(),
        title="Surfacing Type",
        discriminator="surfacing_type",
    ),
]


class NonlinearTemperatureInput(MBaseModel):
    """Input"""

    section_input: SectionInput
    surfacing_input: SurfacingTypeInput
