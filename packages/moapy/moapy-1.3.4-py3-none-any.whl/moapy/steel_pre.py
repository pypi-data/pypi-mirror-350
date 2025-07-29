from pydantic import Field, ConfigDict, validator
from typing import List, Annotated, Union   
from moapy.auto_convert import MBaseModel
from moapy.enum_pre import (
    enum_to_list, enConnectionType, enUnitLength, en_H_EN10365, enSteelMaterial_EN10025,
    enBoltName, enBoltMaterialEC, enSteelMaterial_ASTM, enUnitSystem,
    enAnchorType, enBoltMaterialASTM, enUnitStress, enInteractionFactor, enUnitForce, enAnchorBoltName,
    en_H_AISC05_US, en_T_AISC05_US, en_ANGLE_AISC05_US, en_BOX_AISC05_US, en_PIPE_AISC05_US, en_C_AISC05_US,
    en_H_AISC05_SI, en_T_AISC05_SI, en_ANGLE_AISC05_SI, en_BOX_AISC05_SI, en_PIPE_AISC05_SI, en_C_AISC05_SI,
    en_H_AISC16_US, en_T_AISC16_US, en_ANGLE_AISC16_US, en_BOX_AISC16_US, en_PIPE_AISC16_US, en_C_AISC16_US,
    en_H_AISC16_SI, en_T_AISC16_SI, en_ANGLE_AISC16_SI, en_BOX_AISC16_SI, en_PIPE_AISC16_SI, en_C_AISC16_SI,
    enStudBoltName, enAnchorBoltType
)
from moapy.data_pre import Length, BucklingLength, Stress, Percentage, Force, SectionShapeL, SectionShapeC, SectionShapeH, SectionShapeT, SectionShapeBox, SectionShapePipe, EffectiveLengthFactor_Torsion

# ==    == Steel DB ====
class SteelLength(BucklingLength):
    """
    Steel DB Length
    """
    l_b: Length = Field(default_factory=Length, title="Lb", description="Lateral unbraced length.")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        instance = super().create_default(unit_system)
        if unit_system == enUnitSystem.US:
            instance.l_b = Length(value=1.25, unit=enUnitLength.FT)
        else:
            instance.l_b = Length(value=3, unit=enUnitLength.M)

        return instance

    model_config = ConfigDict(
        title="Member Length",
        json_schema_extra={
            "description": "Buckling length is the length at which a structural member, such as a column or plate, can resist the phenomenon of buckling. Buckling is the sudden deformation of a long member under compressive load along its own center of gravity, which has a significant impact on the safety of a structure. Buckling length is an important factor in analyzing and preventing this phenomenon."
        }
    )

class InteractionFactorAnnex(MBaseModel):
    """
    Interaction Factor Annex
    """
    type: str = Field(default=enInteractionFactor.AnnexA, title="Method Type", description="These calculation methods are used to verify the global stability of a member under complex loading (compression and bending). These factors are included in the verification formulas (6.61 and 6.62) given in section 6.3.3.(4) of the EN 1993-1-3:2005 code.", enum=enum_to_list(enInteractionFactor))

    model_config = ConfigDict(
        title="Methods of Calculation of Interaction Factors kij",
        json_schema_extra={
            "description": "Contains the list of calculation methods of the interaction factors kij"
        }
    )

class SteelLength_Torsion(SteelLength):
    """
    Steel DB Length
    """
    l_t: Length = Field(default_factory=Length, title="Lt", description="Torsional Buckling Length")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        instance = super().create_default(unit_system)
        if unit_system == enUnitSystem.US:
            instance.l_t = Length(value=1.25, unit=enUnitLength.FT)
        else:
            instance.l_t = Length(value=3, unit=enUnitLength.M)
        return instance

    model_config = ConfigDict(
        title="Member Length",
        json_schema_extra={
            "description": "Buckling length is the length at which a structural member, such as a column or plate, can resist the phenomenon of buckling. Buckling is the sudden deformation of a long member under compressive load along its own center of gravity, which has a significant impact on the safety of a structure. Buckling length is an important factor in analyzing and preventing this phenomenon."
        }
    )

class SteelMomentModificationFactorLTB(MBaseModel):
    """
    Steel DB Moment Modification Factor
    """
    c_b: float = Field(default=1.0, title="Cb", description="Cb Modification Factor")

    model_config = ConfigDict(
        title="Steel Moment Modification Factor",
        json_schema_extra={
            "description": "It is calculated based on the moment distribution, using Mmax(the maximum moment within the unbraced length) and specific moments at certain points (Ma, Mb, Mc)"
        }
    )

class SteelMomentModificationFactor(MBaseModel):
    """
    Steel DB Moment Modification Factor
    """
    c_mx: float = Field(default=1.0, title="Cmx", description="Cmx Modification Factor")
    c_my: float = Field(default=1.0, title="Cmy", description="Cmy Modification Factor")

    model_config = ConfigDict(
        title="Steel Moment Modification Factor",
        json_schema_extra={
            "description": "A coefficient used in structural design to adjust the moments in a structure based on specific conditions or types of support. It is often applied to improve the assessment of loads and moments on columns, beams, or other structural elements. moment modification factor plays an important role in adjusting the moments to reflect the behavior and loading conditions of the structure."
        }
    )

class SteelMomentModificationFactor_EC(SteelMomentModificationFactor):
    """
    Steel DB Moment Modification Factor
    """
    c1: float = Field(default=1.0, title="C1", description="ratio between the critical bending moment and the critical constant bending moment for a member with hinged supports")
    c_mlt: float = Field(default=1.0, title="Cmlt", description="equivalent uniform moment factor for LTB")

    model_config = ConfigDict(
        title="Steel Moment Modification Factor",
        json_schema_extra={
            "description": "A coefficient used in structural design to adjust the moments in a structure based on specific conditions or types of support. It is often applied to improve the assessment of loads and moments on columns, beams, or other structural elements. moment modification factor plays an important role in adjusting the moments to reflect the behavior and loading conditions of the structure."
        }
    )

class SteelSectionAISC16US(MBaseModel):
    """
    Steel DB Section
    """
    shape: str = Field(
        default='H',
        title="Section Shape",
        description="Structural steel section profile type (e.g., H-shape, T-shape, Channel, Angle). This parameter defines the fundamental cross-sectional geometry of the steel member.",
        enum=["H", "T", "Box", "Channel", "Angle", "Pipe"]
    )

    name: str = Field(
        default=None,
        title="Section Name",
        description="Standardized designation of the steel section based on industry specifications. This identifier corresponds to specific dimensional and structural properties in the steel section database.",
        enum=[]
    )

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "Database specifications for structural steel sections including section shape and standardized member designations. This configuration provides essential cross-sectional properties for structural steel design and analysis.",
            "dependencies": {
                "shape": {
                    "oneOf": [
                        {
                            "properties": {
                                "shape": {"const": "H"},
                                "name": {
                                    "enum": [e.value for e in en_H_AISC16_US],
                                    "default" : en_H_AISC16_US.W40X183.value
                                }
                            },
                            "required": ["name"]
                        },
                        {
                            "properties": {
                                "shape": {"const": "T"},
                                "name": {
                                    "enum": [e.value for e in en_T_AISC16_US],
                                    "default" : en_T_AISC16_US.WT10_5X22.value
                                },
                            },
                            "required": ["name"]
                        },
                        {
                            "properties": {
                                "shape": {"const": "Angle"},
                                "name": {
                                    "enum": [e.value for e in en_ANGLE_AISC16_US],
                                    "default" : en_ANGLE_AISC16_US.L3X2X1_2.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Box"},
                                "name": {
                                    "enum": [e.value for e in en_BOX_AISC16_US],
                                    "default" : en_BOX_AISC16_US.HSS10X3X_125.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Pipe"},
                                "name": {
                                    "enum": [e.value for e in en_PIPE_AISC16_US],
                                    "default" : en_PIPE_AISC16_US.HSS18X_500.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Channel"},
                                "name": {
                                    "enum": [e.value for e in en_C_AISC16_US],
                                    "default" : en_C_AISC16_US.C6X8_2.value
                                },
                            }
                        }
                    ]
                }
            },
        }
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str], title: str = "", description: str = ""):
        """
        Creates an instance of SteelSection with a specific enum list and dynamic description for the name field.
        """
        section = cls()
        # Dynamically set the enum for the name field
        section.model_fields['name'].json_schema_extra['enum'] = enum_list
        section.model_fields['name'].json_schema_extra['default'] = name
        # Set default name if enum_list is provided
        section.name = name
        # Change description dynamically
        if title:
            cls.model_config["title"] = title
        if description:
            cls.model_config["description"] = description
        return section

InputSection = Annotated[
    Union[
        SectionShapeL,
        SectionShapeC,
        SectionShapeH,
        SectionShapeT,
        SectionShapeBox,
        SectionShapePipe,
    ],
    Field(default=SectionShapeH(), title="Section Input", discriminator="section_type"),
]

class SteelSectionAISC16SI(MBaseModel):
    """
    Steel DB Section
    """
    # use_db: bool = Field(default=True, title="Use DB", description="Whether to use the database to select the section name.")
    shape: str = Field(
        default='H',
        title="Section Shape",
        description="Structural steel section profile type (e.g., H-shape, T-shape, Channel, Angle). This parameter defines the fundamental cross-sectional geometry of the steel member.",
        enum=["H", "T", "Box", "Channel", "Angle", "Pipe"]
    )

    name: str = Field(
        default=None,
        title="Section Name",
        description="Standardized designation of the steel section based on industry specifications. This identifier corresponds to specific dimensional and structural properties in the steel section database.",
        enum=[]
    )

    # section: InputSection = Field(default=SectionShapeH(), title="Section Input", discriminator="section_type")

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "Database specifications for structural steel sections including section shape and standardized member designations. This configuration provides essential cross-sectional properties for structural steel design and analysis.",
            "dependencies": {
                "shape": {
                    "oneOf": [
                        {
                            "properties": {
                                "shape": {"const": "H"},
                                "name": {
                                    "enum": [e.value for e in en_H_AISC16_SI],
                                    "default": en_H_AISC16_SI.W1000X272.value
                                }
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "T"},
                                "name": {
                                    "enum": [e.value for e in en_T_AISC16_SI],
                                    "default": en_T_AISC16_SI.WT180X32.value
                                }
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Angle"},
                                "name": {
                                    "enum": [e.value for e in en_ANGLE_AISC16_SI],
                                    "default": en_ANGLE_AISC16_SI.L51X51X3_2.value
                                }
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Box"},
                                "name": {
                                    "enum": [e.value for e in en_BOX_AISC16_SI],
                                    "default": en_BOX_AISC16_SI.HSS50_8X25_4X3_2.value
                                }
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Pipe"},
                                "name": {
                                    "enum": [e.value for e in en_PIPE_AISC16_SI],
                                    "default": en_PIPE_AISC16_SI.HSS101_6X3_2.value
                                }
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Channel"},
                                "name": {
                                    "enum": [e.value for e in en_C_AISC16_SI],
                                    "default": en_C_AISC16_SI.C75X5_2.value
                                }
                            }
                        }
                    ]
                }
            },
        }
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str], title: str = "", description: str = ""):
        """
        Creates an instance of SteelSection with a specific enum list and dynamic description for the name field.
        """
        section = cls()
        # Dynamically set the enum for the name field
        section.model_fields['name'].json_schema_extra['enum'] = enum_list
        section.model_fields['name'].json_schema_extra['default'] = name
        # Set default name if enum_list is provided
        section.name = name
        # Change description dynamically
        if title:
            cls.model_config["title"] = title
        if description:
            cls.model_config["description"] = description
        return section

class SteelSectionAISC05US(MBaseModel):
    """
    Steel DB Section
    """
    shape: str = Field(
        default='H',
        title="Section Shape",
        description="Structural steel section profile type (e.g., H-shape, T-shape, Channel, Angle). This parameter defines the fundamental cross-sectional geometry of the steel member.",
        enum=["H", "T", "Box", "Channel", "Angle", "Pipe"]
    )

    name: str = Field(
        default=None,
        title="Section Name",
        description="Standardized designation of the steel section based on industry specifications. This identifier corresponds to specific dimensional and structural properties in the steel section database.",
        enum=[]
    )

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "Database specifications for structural steel sections including section shape and standardized member designations. This configuration provides essential cross-sectional properties for structural steel design and analysis.",
            "dependencies": {
                "shape": {
                    "oneOf": [
                        {
                            "properties": {
                                "shape": {"const": "H"},
                                "name": {
                                    "enum": [e.value for e in en_H_AISC05_US],
                                    "default" : en_H_AISC05_US.W40X183.value
                                }
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "T"},
                                "name": {
                                    "enum": [e.value for e in en_T_AISC05_US],
                                    "default" : en_T_AISC05_US.WT10_5X22.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Angle"},
                                "name": {
                                    "enum": [e.value for e in en_ANGLE_AISC05_US],
                                    "default" : en_ANGLE_AISC05_US.L3X2X1_2.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Box"},
                                "name": {
                                    "enum": [e.value for e in en_BOX_AISC05_US],
                                    "default" : en_BOX_AISC05_US.HSS12X6X5_8.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Pipe"},
                                "name": {
                                    "enum": [e.value for e in en_PIPE_AISC05_US],
                                    "default" : en_PIPE_AISC05_US.PIPE1_2XS.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Channel"},
                                "name": {
                                    "enum": [e.value for e in en_C_AISC05_US],
                                    "default" : en_C_AISC05_US.C6X8_2.value
                                },
                            }
                        }
                    ]
                }
            },
        }
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str], title: str = "", description: str = ""):
        """
        Creates an instance of SteelSection with a specific enum list and dynamic description for the name field.
        """
        section = cls()
        # Dynamically set the enum for the name field
        section.model_fields['name'].json_schema_extra['enum'] = enum_list
        section.model_fields['name'].json_schema_extra['default'] = name
        # Set default name if enum_list is provided
        section.name = name
        # Change description dynamically
        if title:
            cls.model_config["title"] = title
        if description:
            cls.model_config["description"] = description
        return section

class SteelSectionAISC05SI(MBaseModel):
    """
    Steel DB Section
    """
    shape: str = Field(
        default='H',
        title="Section Shape",
        description="Structural steel section profile type (e.g., H-shape, T-shape, Channel, Angle). This parameter defines the fundamental cross-sectional geometry of the steel member.",
        enum=["H", "T", "Box", "Channel", "Angle", "Pipe"]
    )

    name: str = Field(
        default=None,
        title="Section Name",
        description="Standardized designation of the steel section based on industry specifications. This identifier corresponds to specific dimensional and structural properties in the steel section database.",
        enum=[]
    )

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "Database specifications for structural steel sections including section shape and standardized member designations. This configuration provides essential cross-sectional properties for structural steel design and analysis.",
            "dependencies": {
                "shape": {
                    "oneOf": [
                        {
                            "properties": {
                                "shape": {"const": "H"},
                                "name": {
                                    "enum": [e.value for e in en_H_AISC05_SI],
                                    "default" : en_H_AISC05_SI.W920X201.value
                                }
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "T"},
                                "name": {
                                    "enum": [e.value for e in en_T_AISC05_SI],
                                    "default" : en_T_AISC05_SI.WT180X32.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Angle"},
                                "name": {
                                    "enum": [e.value for e in en_ANGLE_AISC05_SI],
                                    "default" : en_ANGLE_AISC05_SI.L51X51X3_2.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Box"},
                                "name": {
                                    "enum": [e.value for e in en_BOX_AISC05_SI],
                                    "default" : en_BOX_AISC05_SI.HSS50_8X25_4X3_2.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Pipe"},
                                "name": {
                                    "enum": [e.value for e in en_PIPE_AISC05_SI],
                                    "default" : en_PIPE_AISC05_SI.PIPE102STD.value
                                },
                            }
                        },
                        {
                            "properties": {
                                "shape": {"const": "Channel"},
                                "name": {
                                    "enum": [e.value for e in en_C_AISC05_SI],
                                    "default" : en_C_AISC05_SI.C75X5_2.value
                                },
                            }
                        }
                    ]
                }
            },
        }
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str], title: str = "", description: str = ""):
        """
        Creates an instance of SteelSection with a specific enum list and dynamic description for the name field.
        """
        section = cls()
        # Dynamically set the enum for the name field
        section.model_fields['name'].json_schema_extra['enum'] = enum_list
        section.model_fields['name'].json_schema_extra['default'] = name
        # Set default name if enum_list is provided
        section.name = name
        # Change description dynamically
        if title:
            cls.model_config["title"] = title
        if description:
            cls.model_config["description"] = description
        return section

class SteelSection(MBaseModel):
    """
    Steel DB Section
    """
    shape: str = Field(
        default='H',
        title="Section Shape",
        description="Structural steel section profile type (e.g., H-shape, T-shape, Channel, Angle). This parameter defines the fundamental cross-sectional geometry of the steel member.",
        readOnly=True
    )

    name: str = Field(
        default=None,
        title="Section Name",
        description="Standardized designation of the steel section based on industry specifications. This identifier corresponds to specific dimensional and structural properties in the steel section database.",
        enum=[]
    )

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "Database specifications for structural steel sections including section shape and standardized member designations. This configuration provides essential cross-sectional properties for structural steel design and analysis."
        }
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str], title: str = "", description: str = ""):
        """
        Creates an instance of SteelSection with a specific enum list and dynamic description for the name field.
        """
        section = cls()
        # Dynamically set the enum for the name field
        section.model_fields['name'].json_schema_extra['enum'] = enum_list
        section.model_fields['name'].json_schema_extra['default'] = name
        # Set default name if enum_list is provided
        section.name = name
        # Change description dynamically
        if title:
            cls.model_config["title"] = title
        if description:
            cls.model_config["description"] = description
        return section

class SteelSection_EN10365(SteelSection):
    """
    Steel DB Section wit
    """
    shape: str = Field(default='H', description="Shape of member section", readOnly=True)
    name: str = Field(default='HD 260x54.1', description="Use DB stored in EN10365", enum=enum_to_list(en_H_EN10365))

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."
        }
    )

class SteelMaterial(MBaseModel):
    """
    Steel Material for structural design.
    
    This model represents a steel material used in structural applications. It includes 
    information about the material code, its name, and the available material options 
    from a predefined list. This information is crucial for steel material selection 
    and ensuring that the correct material is used in structural design calculations.
    """
    # Material code for the steel, usually assigned based on industry standards
    code: str = Field(default_factory=str, description="Unique code for the material as defined in the material database. This is used to identify the specific steel material.", readOnly=True)

    # Name of the steel material, selected from a predefined list of available materials
    name: str = Field(default_factory=str, description="Name of the steel material. The material name is selected from a list of available materials.", enum=[])

    @classmethod
    def create_default(cls, code: str, enum_list: List[str], description: str = "Steel DB Material"):
        """
        Create a SteelMaterial instance with customizable values including description.
        
        This method allows for the creation of a SteelMaterial instance by specifying 
        the material code, a list of available material names (enum list), and an optional 
        description to provide additional context for the material.
        """
        material = cls()
        # Dynamically set the description for the material
        material.model_config["description"] = description
        # Dynamically set the enum options for the 'name' field
        material.model_fields['name'].json_schema_extra['enum'] = enum_list
        material.model_fields['name'].json_schema_extra['default'] = enum_list[0] if enum_list else None
        material.code = code
        material.name = enum_list[0] if enum_list else None
        return material

    model_config = ConfigDict(
        title="Material",
        json_schema_extra={
            "description": "A steel material used in structural design, with customizable options for material code and name. The material properties are selected from a predefined list."
        }
    )

class SteelMaterial_EC(SteelMaterial):
    """
    Steel DB Material
    """
    code: str = Field(default='EN10025', description="Material code", readOnly=True)
    name: str = Field(default=enSteelMaterial_EN10025.S275, description="Material of steel member", enum=enum_to_list(enSteelMaterial_EN10025))

    model_config = ConfigDict(
        title="Steel DB Material",
        json_schema_extra={
            "description": "EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type."
        }
    )

class BoltMaterial(MBaseModel):
    """
    Bolt Material
    """
    # Material name, representing the type or grade of the bolt material


    @classmethod
    def create_default(cls, name: str, enum_list: List[str]):
        """
        Creates a default instance of BoltMaterial with a dynamic material name and enum list.
        """
        material = cls()
        material.model_fields['name'].json_schema_extra['enum'] = enum_list
        material.model_fields['name'].json_schema_extra['default'] = name
        material.name = name
        return material

    model_config = ConfigDict(
        title="Bolt Material Specifications",
        json_schema_extra={
            "description": "This model defines the properties of the bolt material, including its type and mechanical characteristics. The material type affects the bolt's strength, durability, and suitability for specific applications."
        }
    )

class BoltMaterial_EC(BoltMaterial):
    """
    Bolt Material
    """
    name: str = Field(default='4.8', description="Bolt Material Name", enum=enum_to_list(enBoltMaterialEC))

    model_config = ConfigDict(
        title="Bolt Material",
        json_schema_extra={
            "description": "Bolt Material"
        }
    )

class SteelMember(MBaseModel):
    """
    Steel Member class representing a structural steel member, consisting of a section and material. 

    Args:
        sect (SteelSection): The cross-sectional shape and properties of the steel member.
        matl (SteelMaterial): The material properties of the steel member, including strength and durability.
    """
    sect: SteelSection = Field(default_factory=SteelSection, title="Section", description="The cross-sectional shape and properties of the steel member.")
    matl: SteelMaterial = Field(default_factory=SteelMaterial, title="Material", description="The material properties, including strength, durability, and composition, of the steel member.")

    model_config = ConfigDict(
        title="Steel Member",
        json_schema_extra={
            "description": "A steel member consists of both the section (cross-sectional shape) and material (material properties). Proper selection of the section and material is critical for ensuring the strength, stability, and durability of the structure. This contributes to the design of a safe and efficient steel structure."
        }
    )

class BoltConnectionMaterial(MBaseModel):
    matl: SteelMaterial = Field(default_factory=SteelMaterial, title="Material", description="The material properties, including strength, durability, and composition, of the steel member.")

class SteelConnectMember(MBaseModel):
    """
    Steel Connect Member class representing the relationship between supporting and supported members in a connection.
    
    Args:
        supporting (SteelMember): The supporting member that provides resistance to forces.
        supported (SteelMember): The supported member that receives the load from the supporting member.
    """
    supporting: SteelMember = Field(default_factory=SteelMember, title="Supporting Member", description="The member that supports and resists forces.")
    supported: SteelMember = Field(default_factory=SteelMember, title="Supported Member", description="The member that is supported and carries the load from the supporting member.")

    model_config = ConfigDict(
        title="Steel Connect Member",
        json_schema_extra={
            "description": "Defines the connection between two steel members: one acting as the supporting member, and the other as the supported member. This connection is crucial in bolted joints, contributing to load transfer and ensuring the stability and safety of the structure."
        }
    )

class SteelBoltConnectionForce(MBaseModel):
    """
    Steel Bolt Connection Force class for defining the percentage of the member strength used in the steel bolt connection.

    Args:
        percent (float): The percentage of member strength considered for the steel bolt connection.
    """
    percent: Percentage = Field(default_factory=Percentage, title="Strength Design Percentage", description="The strength design percentage for the steel bolt connection. By default, shear is assumed to be 30% of the member strength, as it generally does not cause issues. If a higher percentage is required, adjust the value accordingly.")

    model_config = ConfigDict(
        title="Force",
        json_schema_extra={
            "description": "Defines the percentage of member strength assumed for the steel bolt connection, typically 30% for shear. This value can be adjusted based on design requirements."
        }
    )

class BoltLayoutComponent(MBaseModel):
    """
    Bolt Layout Component
    """
    dist: Length = Field(default_factory=Length, title="Edge Dist.", description="The distance from the edge of the steel member to the center of the bolt.")
    no: int = Field(default=2, title="No.", description="The number of anchor bolts arranged along the axis.")

    model_config = ConfigDict(
        title="Bolt Layout Component",
        json_schema_extra={
            "description": "Defines the layout of anchor bolts in a connection, specifying the number of bolts and their positions along the axis."
        }
    )

class BoltLayout(MBaseModel):
    dir_x: BoltLayoutComponent = Field(default_factory=BoltLayoutComponent, title="X", description="The layout of anchor bolts along the X-axis.")
    dir_y: BoltLayoutComponent = Field(default_factory=BoltLayoutComponent, title="Y", description="The layout of anchor bolts along the Y-axis.")

    model_config = ConfigDict(
        title="Bolt Layout",
        json_schema_extra={
            "description": "Defines the layout of anchor bolts in a connection, specifying the number of bolts and their positions along the X and Y axes."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(dir_x=BoltLayoutComponent(dist=Length(value=1.5, unit=enUnitLength.IN), no=2), dir_y=BoltLayoutComponent(dist=Length(value=1.5, unit=enUnitLength.IN), no=2))
        else:
            return cls(dir_x=BoltLayoutComponent(dist=Length(value=50, unit=enUnitLength.MM), no=2), dir_y=BoltLayoutComponent(dist=Length(value=50, unit=enUnitLength.MM), no=2))

class AnchorBolt(MBaseModel):
    """
    Anchor Bolt

    This class represents anchor bolts used to secure structures to concrete foundations. 
    Anchor bolts are designed to withstand applied forces and loads, providing stability and support to the structure. 
    Anchor bolts come in various sizes, materials, and configurations to meet different structural requirements.
    """
    type: str = Field(
        default=enAnchorType.CIP,
        title="Anchor Bolt Installation Type",
        description="Type of anchor bolt installation method. Options include Cast-in-Place (CIP) or Post-Installed types, defining how the anchor bolt is embedded into the foundation.",
        enum=enum_to_list(enAnchorType),
        readOnly=True
    )

    bolt_name: str = Field(
        default_factory=str,
        title="Bolt Size",
        description="The size or type of the steel bolt, represented by its designation (e.g., M16). This defines the dimensions and thread specifications of the bolt.",
        enum=enum_to_list(enBoltName)
    )

    length: float = Field(
        default_factory=float,
        title="Anchor Bolt Length (D)",
        description="The length of the anchor bolt, typically specified as the total length including both the embedded length in the foundation and the exposed portion. Length is critical for proper installation and load transfer. The input value will be multiplied by D to determine the actual physical length."
    )

    layout: BoltLayout = Field(default_factory=BoltLayout, title="Bolt Layout", description="The layout of the anchor bolts in the connection.")

    model_config = ConfigDict(
        title="Anchor Bolt Design",
        json_schema_extra={
            "description": "Anchor bolts are critical for securing structures to concrete foundations. They are designed to withstand large forces and loads applied to the structure, offering essential support. The design of anchor bolts varies based on the application, foundation material, and structural needs."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem, name: str, enum_list: List[str]):
        bolt = cls()
        bolt.model_fields['bolt_name'].json_schema_extra['enum'] = enum_list
        bolt.model_fields['bolt_name'].json_schema_extra['default'] = name
        bolt.bolt_name = name
        bolt.layout = BoltLayout.create_default(unit_system)
        if unit_system == enUnitSystem.US:
            bolt.length = 5.91
        else:
            bolt.length = 25

        return bolt

class AnchorBolt_US(MBaseModel):
    """
    Anchor Bolt for US Standards

    This class extends the AnchorBolt class, incorporating additional parameters specific to US standards.
    It adds the parameter Np to define the number of anchor bolts in the vertical direction (Z-axis).
    """
    """
    Anchor Bolt

    This class represents anchor bolts used to secure structures to concrete foundations. 
    Anchor bolts are designed to withstand applied forces and loads, providing stability and support to the structure. 
    Anchor bolts come in various sizes, materials, and configurations to meet different structural requirements.
    """
    type: str = Field(
        default=enAnchorType.CIP,
        title="Anchor Bolt Installation Type",
        description="Type of anchor bolt installation method. Options include Cast-in-Place (CIP) or Post-Installed types, defining how the anchor bolt is embedded into the foundation.",
        enum=enum_to_list(enAnchorType),
        readOnly=True
    )

    bolt_name: str = Field(
        default_factory=str,
        title="Bolt Size",
        description="The size or type of the steel bolt, represented by its designation (e.g., M16). This defines the dimensions and thread specifications of the bolt.",
        enum=enum_to_list(enBoltName)
    )

    length: Length = Field(
        default_factory=Length,
        title="Anchor Bolt Length",
        description="The length of the anchor bolt, typically specified as the total length including both the embedded length in the foundation and the exposed portion. Length is critical for proper installation and load transfer. The input value will be multiplied by D to determine the actual physical length."
    )

    layout: BoltLayout = Field(default_factory=BoltLayout, title="Bolt Layout", description="The layout of the anchor bolts in the connection.")
    
    Np: Force = Field(
        default_factory=Force,
        title="Pullout Strength",
        description="The pullout strength of an anchor bolt refers to the maximum tensile force the bolt can resist before being pulled out from the foundation material. This value depends on factors such as the embedment depth, diameter of the bolt, type and strength of the foundation material, and the quality of installation. Proper assessment of pullout strength is crucial to ensure safety and structural integrity under tensile loads."
    )

    anchor_type: str = Field(default=enAnchorBoltType.STUD, title="Anchor Bolt Type", description="Type of anchor bolt used in the base plate connection. This includes the number of anchor bolts, their positions, and the overall arrangement of the base plate components. Proper layout design is essential for ensuring structural stability and load distribution in steel connections.", enum=enum_to_list(enAnchorBoltType))
    hooked_bolt_dist: Length = Field(default_factory=Length, title="Dist. of J/L-Bolt(eH)", description="Distance between the anchor bolt and the edge of the base plate. This parameter is essential for ensuring proper anchor bolt placement and load distribution in steel connections.")

    model_config = ConfigDict(
        title="Anchor Bolt Design for US Standards",
        json_schema_extra={
            "description": "Anchor bolts designed for US standards include additional considerations for vertical force distribution. This is achieved through the Np parameter, which defines the number of bolts along the Z-axis."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem, name: str, enum_list: List[str]):
        bolt = cls()
        bolt.model_fields['bolt_name'].json_schema_extra['enum'] = enum_list
        bolt.model_fields['bolt_name'].json_schema_extra['default'] = name
        bolt.bolt_name = name
        bolt.layout = BoltLayout.create_default(unit_system)
        if unit_system == enUnitSystem.US:
            bolt.length = Length(value=5.91, unit=enUnitLength.IN)
            bolt.Np = Force(value=6.74, unit=enUnitForce.kip)
            bolt.anchor_type = enAnchorBoltType.STUD
            bolt.hooked_bolt_dist = Length(value=1, unit=enUnitLength.IN)
        else:
            bolt.length = Length(value=25, unit=enUnitLength.MM)
            bolt.Np = Force(value=30, unit=enUnitForce.kN)
            bolt.anchor_type = enAnchorBoltType.STUD
            bolt.hooked_bolt_dist = Length(value=30, unit=enUnitLength.MM)

        return bolt

class BasePlateStrengthReductionFactorConcrete(MBaseModel):
    conc_tension: float = Field(
        default=0.65, gt=0,
        title="Concrete Tension Strength Factor",
        description="The reduction factor applied to the nominal strength of concrete under tension. It accounts for uncertainties and ensures a conservative design."
    )
    conc_shear: float = Field(
        default=0.75, gt=0,
        title="Concrete Shear Strength Factor",
        description="The reduction factor applied to the nominal strength of concrete under shear. It helps provide safety by accounting for material and load variability."
    )

    model_config = ConfigDict(
        title="Concrete Strength Reduction Factors",
        json_schema_extra={
            "description": "Strength reduction factors are applied to adjust the nominal strength of concrete and anchors to ensure safety in structural design. These factors account for uncertainties in material properties, loads, and design conditions, providing a conservative approach to structural safety."
        }
    )

class BasePlateStrengthReductionFactorAnchor(MBaseModel):
    anchor_tension: float = Field(
        default=0.75, gt=0,
        title="Anchor Tension Strength Factor",
        description="The reduction factor used for calculating the tension strength of anchor bolts. It ensures a safe and reliable design under tension loads."
    )
    anchor_shear: float = Field(
        default=0.65, gt=0,
        title="Anchor Shear Strength Factor",
        description="The reduction factor used for calculating the shear strength of anchor bolts. It helps address uncertainties and variability in shear forces."
    )

    model_config = ConfigDict(
        title="Anchor Strength Reduction Factors",
        json_schema_extra={
            "description": "Strength reduction factors are applied to adjust the nominal strength of anchor bolts to ensure safety in structural design. These factors account for uncertainties in material properties, loads, and design conditions, providing a conservative approach to structural safety."
        }
    )

class BasePlateStrengthReductionFactor(MBaseModel):
    """
    Strength Reduction Factor
    """
    conc: BasePlateStrengthReductionFactorConcrete = Field(default=BasePlateStrengthReductionFactorConcrete(), title="Concrete Strength Reduction Factors", description="Strength reduction factors for concrete")
    anchor: BasePlateStrengthReductionFactorAnchor = Field(default=BasePlateStrengthReductionFactorAnchor(), title="Anchor Strength Reduction Factors", description="Strength reduction factors for anchor bolts")

    model_config = ConfigDict(
        title="Design Parameter",
        json_schema_extra={
            "description": (
                "Strength reduction factors are applied to adjust the nominal strength of concrete and anchors "
                "to ensure safety in structural design. These factors account for uncertainties in material properties, "
                "loads, and design conditions, providing a conservative approach to structural safety."
            )
        }
    )

class SteelBolt_EC(MBaseModel):
    """
    Steel Bolt class representing a mechanical element used for connecting structural members.

    Args:
        name (str): The size of the bolt (e.g., M20, M10).
        matl (BoltMaterial_EC): The material of the bolt.
    """
    name: str = Field(default='M20', title="Bolt Size", description="The size of the bolt, typically denoted by the outer diameter (e.g., M20, M10)", enum=enum_to_list(enBoltName))
    matl: BoltMaterial_EC = Field(default=BoltMaterial_EC(), title="Bolt Material", description="The material used for the bolt, determining its strength and durability")

    model_config = ConfigDict(
        title="Steel Bolt",
        json_schema_extra={
            "description": """A bolt is a mechanical element that connects members of a structure and is used to transfer loads.
                \nDiameter: The outer diameter of a bolt, usually expressed in a metric system such as M6, M8, M10, etc.
                \nLength: The overall length of the bolt, determined by the thickness of the connecting members.
                \nClass: The strength rating, expressed as a class, for example 8.8, 10.9, etc., where higher numbers indicate greater strength.
            """
        }
    )

class SteelStudBolt_EC(MBaseModel):
    """
    Steel Bolt class representing a mechanical element used for connecting structural members.

    Args:
        name (str): The size of the bolt (e.g., M20, M10).
        matl (BoltMaterial_EC): The material of the bolt.
    """
    name: str = Field(default='M6', title="Bolt Size", description="The size of the bolt, typically denoted by the outer diameter (e.g., M20, M10)", enum=enum_to_list(enStudBoltName))
    matl: BoltMaterial_EC = Field(default=BoltMaterial_EC(), title="Bolt Material", description="The material used for the bolt, determining its strength and durability")

    model_config = ConfigDict(
        title="Steel Bolt",
        json_schema_extra={
            "description": """A bolt is a mechanical element that connects members of a structure and is used to transfer loads.
                \nDiameter: The outer diameter of a bolt, usually expressed in a metric system such as M6, M8, M10, etc.
                \nLength: The overall length of the bolt, determined by the thickness of the connecting members.
                \nClass: The strength rating, expressed as a class, for example 8.8, 10.9, etc., where higher numbers indicate greater strength.
            """
        }
    )

class ShearConnector_EC(MBaseModel):
    """
    Shear Connector class for defining the specifications of shear connectors used in structural connections.

    Args:
        name (str): The size of the shear connector (e.g., M20, M10).
        num (int): Number of shear connectors.
        space (Length): Spacing between shear connectors.
        length (Length): Length of the shear connector (stud).
    """
    name: str = Field(default="M19", title="Bolt Size", description="The size of the bolt, typically denoted by the outer diameter (e.g., M20, M10)", enum=enum_to_list(enStudBoltName))
    num: int = Field(default=1, ge=0, le=3, title="Number of Shear Connectors", description="Number of shear connectors (stud bolts) used in the connection.", enum=[1, 2, 3])
    space: Length = Field(default_factory=Length, title="Shear Connector Spacing", description="Spacing between adjacent shear connectors (studs).")
    length: Length = Field(default_factory=Length, title="Shear Connector Length", description="Length of each shear connector (stud).")

    model_config = ConfigDict(
        title="Shear Connector",
        json_schema_extra={
            "description": "Shear connectors are critical in transferring forces between connected structural elements. They play a key role in ensuring the strength and stability of a structure, and are designed to meet specific requirements based on the materials, configuration, and design load. Proper selection and placement of shear connectors enhance the safety, strength, and durability of the structure."
        }
    )
    
    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(space=Length(value=12, unit=enUnitLength.IN), length=Length(value=10, unit=enUnitLength.IN))
        else:
            return cls(space=Length(value=300, unit=enUnitLength.MM), length=Length(value=100, unit=enUnitLength.MM))

class Welding(MBaseModel):
    """
    Welding
    """
    matl: SteelMaterial = Field(default_factory=SteelMaterial, description="Material")
    length: Length = Field(default_factory=Length, description="Leg of Length")

    model_config = ConfigDict(
        title="Welding",
        json_schema_extra={
            "description": "Welding"
        }
    )

class Welding_EC(Welding):
    """
    Welding class for reviewing welds on supporting members.

    Args:
        matl (SteelMaterial_EC): The material of the welding.
        length (Length): The length of the weld leg.
    """
    matl: SteelMaterial_EC = Field(default=SteelMaterial_EC(), title="Weld Material", description="The material used for the weld, determining its strength and compatibility with the connected materials")
    length: Length = Field(default=Length(value=6.0, unit=enUnitLength.MM), title="Weld Leg Length", description="The leg length of the weld, which affects its strength and capacity")

    model_config = ConfigDict(
        title="Welding",
        json_schema_extra={
            "description": "Information related to the welds used in connecting supporting members. This includes the material and length of the weld leg, both crucial for ensuring the strength and stability of the welded connections."
        }
    )

class SteelPlateMember(MBaseModel):
    """
    Steel Plate Member
    """
    matl: SteelMaterial = Field(default_factory=SteelMaterial, title="Plate material", description="Material")
    bolt_num: int = Field(default=4, ge=0, title="Number of bolt", description="Number of Bolts")
    thk: Length = Field(default_factory=Length, title="Thickness", description="Thickness")

    model_config = ConfigDict(
        title="Steel Plate Member",
        json_schema_extra={
            "description": "Steel Plate Member"
        }
    )

class SteelPlateMember_EC(SteelPlateMember):
    """
    Steel Plate Member class representing a steel plate element with material properties, thickness, and bolt details.

    Args:
        matl (SteelMaterial_EC): Material properties for the steel plate.
        bolt_num (int): The number of bolts used in the plate connection.
        thk (Length): The thickness of the steel plate.
    """
    matl: SteelMaterial_EC = Field(default=SteelMaterial_EC(), title="Plate Material", description="The material properties of the steel plate, including strength and durability.")
    bolt_num: int = Field(default=4, ge=0, title="Number of Bolts", description="The number of bolts used in the connection of the steel plate.")
    thk: Length = Field(default=Length(value=6.0, unit=enUnitLength.MM), title="Thickness", description="The thickness of the steel plate.")

    model_config = ConfigDict(
        title="Steel Plate Member",
        json_schema_extra={
            "description": "A steel plate member, typically used for load-bearing or connection purposes in structural design. It includes material properties, bolt count, and plate thickness for complete specification."
        }
    )

class ConnectType(MBaseModel):
    """
    Connect Type class representing different types of bolted connections.

    Args:
        type (str): The type of connection.
    """
    type: str = Field(default="Fin Plate - Beam to Beam", title="Connection Type", description="The type of bolted connection between structural elements", enum=enum_to_list(enConnectionType))

    model_config = ConfigDict(
        title="Connection Type",
        json_schema_extra={
            "description": """
                The four types of bolted connections mentioned are described below:
                \n
                1. Fin Plate - Beam to Beam (Fin_B_B) \n
                This is the use of a fin plate to connect two beams, where a fin plate is attached to the end of each beam to connect them together.
                \n\n
                2. Fin Plate - Beam to Column (Fin_B_C)\n
                A method of connecting beams to columns, where fin plates are attached to the sides of the columns and the ends of the beams to create a solid connection.
                \n\n
                3. End Plate - Beam to Beam (End_B_B)\n
                A method of connecting two beams using end plates at the ends. An end plate is attached to the end of each beam and connected via bolts.
                \n\n
                4. End Plate - Beam to Column (End_B_C)\n
                This method of connecting beams to columns uses end plates attached to the sides of the columns to connect with the ends of the beams. Bolts are secured to the column through the end plate.
            """
        }
    )

class BasePlateSectionGrout(MBaseModel):
    """
    Base Plate Section Grout
    """
    grout: Length = Field(default_factory=Length, title="Grout Thickness", description="Thickness of grout material used in the baseplate connection. This parameter defines the depth of the grout layer and is essential for ensuring proper bonding and load transfer between the baseplate and the foundation.")
    
    model_config = ConfigDict(
        title="Grout",
        json_schema_extra={
            "description": "Grout is a material used in the baseplate connection. This parameter defines the depth of the grout layer and is essential for ensuring proper bonding and load transfer between the baseplate and the foundation."
        }
    )
    
    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(grout=Length(value=0.24, unit=enUnitLength.IN))
        else:
            return cls(grout=Length(value=6, unit=enUnitLength.MM))

class BasePlateSectionConcrete(MBaseModel):
    """
    Base Plate Section Concrete
    """
    width: Length = Field(default_factory=Length, title="Base Plate Width", description="Horizontal width measurement of the baseplate component. This dimension represents the lateral span of the plate and is essential for determining the overall footprint and load distribution capabilities.")
    height: Length = Field(default_factory=Length, title="Base Plate Height", description="Vertical height measurement of the baseplate component. This dimension defines the upward extension of the plate and is critical for ensuring proper component fitment and structural support requirements.")
    thk: Length = Field(default_factory=Length, title="Base Plate Thickness", description="Physical thickness dimension of the baseplate component. This parameter defines the vertical depth of the plate material and is crucial for structural integrity and load-bearing capacity.")

    model_config = ConfigDict(
        title="Concrete",
        json_schema_extra={
            "description": "Geometric specifications for the baseplate section, including width, height, thickness, and grout thickness. These dimensions are essential for the design and construction of baseplate connections in steel structures."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(width=Length(value=18, unit=enUnitLength.IN), height=Length(value=18, unit=enUnitLength.IN), thk=Length(value=0.24, unit=enUnitLength.IN))
        else:
            return cls(width=Length(value=390, unit=enUnitLength.MM), height=Length(value=400, unit=enUnitLength.MM), thk=Length(value=6, unit=enUnitLength.MM))

class BasePlateSectionWing(MBaseModel):
    """
    Base Plate Section Wing
    """
    thick: Length = Field(default_factory=Length, title="Thickness", description="Setting the Wing Thickness to 0 indicates that it is not used.")
    height: Length = Field(default_factory=Length, title="Height", description="Wing Height")

    model_config = ConfigDict(
        title="Wing Plate",
        json_schema_extra={
            "description": "Wing Plate Thickness and Height"
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(thick=Length(value=0, unit=enUnitLength.IN), height=Length(value=4, unit=enUnitLength.IN))
        else:
            return cls(thick=Length(value=0, unit=enUnitLength.MM), height=Length(value=100, unit=enUnitLength.MM))

class BasePlateSectionRibComponent(MBaseModel):
    height: Length = Field(default_factory=Length, title="Height", description="Rib Height")
    length: Length = Field(default_factory=Length, title="Length", description="Rib Length")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(height=Length(value=4, unit=enUnitLength.IN), length=Length(value=0.39, unit=enUnitLength.IN))
        else:
            return cls(height=Length(value=100, unit=enUnitLength.MM), length=Length(value=10, unit=enUnitLength.MM))

class BasePlateSectionRibPlateSect(MBaseModel):
    bp: BasePlateSectionRibComponent = Field(default_factory=BasePlateSectionRibComponent, title="BP Face", description="BP Face")
    col: BasePlateSectionRibComponent = Field(default_factory=BasePlateSectionRibComponent, title="Col Face", description="Col Face")
    
    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(bp=BasePlateSectionRibComponent.create_default(unit_system=enUnitSystem.US), col=BasePlateSectionRibComponent.create_default(unit_system=enUnitSystem.US))
        else:
            return cls(bp=BasePlateSectionRibComponent.create_default(unit_system=enUnitSystem.SI), col=BasePlateSectionRibComponent.create_default(unit_system=enUnitSystem.SI))

class BasePlateSectionRib(MBaseModel):
    """
    Rib Plate
    """
    thick: Length = Field(default_factory=Length, title="Thickness", description="Setting the Rib Plate Thickness to 0 indicates that it is not used.")
    sect: BasePlateSectionRibPlateSect = Field(default_factory=BasePlateSectionRibPlateSect, title="Dimension", description="Rib Plate Section")
    num_x: int = Field(default=1, title="Number(x)", description="Number of Ribs in the x-direction")
    num_y: int = Field(default=1, title="Number(y)", description="Number of Ribs in the y-direction")

    model_config = ConfigDict(
        title="Rib Plate",
        json_schema_extra={
            "description": "Rib Thickness and Height"
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(thick=Length(value=0, unit=enUnitLength.IN), sect=BasePlateSectionRibPlateSect.create_default(unit_system=enUnitSystem.US), num_x=1, num_y=1)
        else:
            return cls(thick=Length(value=0, unit=enUnitLength.MM), sect=BasePlateSectionRibPlateSect.create_default(unit_system=enUnitSystem.SI), num_x=1, num_y=1)

class BasePlateSection(MBaseModel):
    """
    Base Plate Section
    """
    steel: SteelSection = Field(default_factory=SteelSection, title="Steel Beam", description="Steel section profile used for the baseplate component. This parameter defines the geometric properties and structural characteristics of the baseplate section.")
    conc: BasePlateSectionConcrete = Field(default_factory=BasePlateSectionConcrete, title="Base Plate", description="Geometric specifications for the baseplate section, including width, height, thickness, and grout thickness. These dimensions are essential for the design and construction of baseplate connections in steel structures.")
    grout: BasePlateSectionGrout = Field(default_factory=BasePlateSectionGrout, title="Grout", description="Grout is a material used in the baseplate connection. This parameter defines the depth of the grout layer and is essential for ensuring proper bonding and load transfer between the baseplate and the foundation.")
    wing: BasePlateSectionWing = Field(default_factory=BasePlateSectionWing, title="Wing Plate", description="Wing Thickness and Height")
    rib: BasePlateSectionRib = Field(default_factory=BasePlateSectionRib, title="Rib Plate", description="Rib Thickness and Height")

    model_config = ConfigDict(
        title="Section",
        json_schema_extra={
            "description": "Geometric specifications for the baseplate section, including width, height, thickness, and grout thickness. These dimensions are essential for the design and construction of baseplate connections in steel structures."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem, name: str, enum_list: List[str], title: str = "", description: str = ""):
        if unit_system == enUnitSystem.US:
            return cls(
                steel=SteelSection.create_default(name=name, enum_list=enum_list, title=title, description=description), conc=BasePlateSectionConcrete.create_default(unit_system=enUnitSystem.US), grout=BasePlateSectionGrout.create_default(unit_system=enUnitSystem.US),
                wing=BasePlateSectionWing.create_default(unit_system=enUnitSystem.US), rib=BasePlateSectionRib.create_default(unit_system=enUnitSystem.US))
        else:
            return cls(steel=SteelSection.create_default(name=name, enum_list=enum_list, title=title, description=description), conc=BasePlateSectionConcrete.create_default(unit_system=enUnitSystem.SI), grout=BasePlateSectionGrout.create_default(unit_system=enUnitSystem.SI),
                       wing=BasePlateSectionWing.create_default(unit_system=enUnitSystem.SI), rib=BasePlateSectionRib.create_default(unit_system=enUnitSystem.SI))

class BasePlateMaterialConcrete(MBaseModel):
    """
    Base Plate Material Concrete
    """
    fck: Stress = Field(default_factory=Stress, title="Concrete Strength", description="Characteristic compressive strength of concrete at 28 days. This parameter represents the structural concrete's design strength and is essential for determining the foundation's load-bearing capacity and structural performance.")

    model_config = ConfigDict(
        title="Base Plate Material Concrete",
        json_schema_extra={
            "description": "Material properties for base plate design, including concrete strength and steel material characteristics. These properties are essential for ensuring the structural integrity, load-bearing capacity, and durability of base plate connections in steel structures."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(fck=Stress(value=3, unit=enUnitStress.ksi))
        else:
            return cls(fck=Stress(value=24, unit=enUnitStress.MPa))

class BasePlateMaterialBolt(MBaseModel):
    """
    Base Plate Material Bolt
    """
    bolt_name: str = Field(default_factory=str, title="Bolt Material Type", description="The type or grade of the material used for the bolt. This determines the bolt's mechanical properties, such as strength, ductility, and corrosion resistance.", enum=[])

    model_config = ConfigDict(
        title="Bolt",
        json_schema_extra={
            "description": "Material properties for base plate design, including concrete strength and steel material characteristics. These properties are essential for ensuring the structural integrity, load-bearing capacity, and durability of base plate connections in steel structures."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem, bolt_name: str, bolt_enum_list: List[str]):
        return cls(bolt_name=bolt_name)

class BasePlateMaterials(MBaseModel):
    """
    Base Plate Materials
    """
    conc: BasePlateMaterialConcrete = Field(default_factory=BasePlateMaterialConcrete, title="Concrete", description="Concrete material properties")
    matl: SteelMaterial = Field(default_factory=SteelMaterial, title="Base Plate", description="Input specification for baseplate material properties. This data includes detailed material composition and characteristics of the base component. The specification outlines essential material parameters for baseplate construction and assembly.")
    bolt: BasePlateMaterialBolt = Field(default_factory=BasePlateMaterialBolt, title="Bolt", description="Bolt material properties")
    rib_wing: SteelMaterial = Field(default_factory=SteelMaterial, title="Rib/Wing", description="Rib/Wing material properties")

    model_config = ConfigDict(
        title="Material",
        json_schema_extra={
            "description": "Material properties for base plate design, including concrete strength and steel material characteristics. These properties are essential for ensuring the structural integrity, load-bearing capacity, and durability of base plate connections in steel structures."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem, bolt_name: str, bolt_enum_list: List[str], code: str, enum_list: List[str], description: str = "Steel DB Material"):
        """
        Create a BasePlateMaterials instance with customizable values including description.
        """
        material = cls()
        material.bolt.model_fields['bolt_name'].json_schema_extra['enum'] = bolt_enum_list
        material.bolt.model_fields['bolt_name'].json_schema_extra['default'] = bolt_name
        material.bolt.bolt_name = bolt_name
        material.matl = SteelMaterial.create_default(code=code, enum_list=enum_list, description=description)
        material.rib_wing = SteelMaterial.create_default(code=code, enum_list=enum_list, description=description)
        if unit_system == enUnitSystem.US:
            material.conc.fck = Stress(value=3, unit=enUnitStress.ksi)
        else:
            material.conc.fck = Stress(value=24, unit=enUnitStress.MPa)

        return material

class BasePlateLayout(MBaseModel):
    """
    Base Plate Layout
    """
    anchor: AnchorBolt = Field(default_factory=AnchorBolt, title="Anchor Bolt Layout", description="Layout and configuration of anchor bolts in the base plate connection. This includes the number of anchor bolts, their positions, and the overall arrangement of the base plate components. Proper layout design is essential for ensuring structural stability and load distribution in steel connections.")

    model_config = ConfigDict(
        title="Bolt",
        json_schema_extra={
            "description": "Layout and configuration of anchor bolts in the base plate connection. This includes the number of anchor bolts, their positions, and the overall arrangement of the base plate components. Proper layout design is essential for ensuring structural stability and load distribution in steel connections."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem, name: str, enum_list: List[str]):
        if unit_system == enUnitSystem.US:
            return cls(anchor=AnchorBolt.create_default(unit_system=enUnitSystem.US, name=name, enum_list=enum_list))
        else:
            return cls(anchor=AnchorBolt.create_default(unit_system=enUnitSystem.SI, name=name, enum_list=enum_list))

class BasePlateLayoutUS(MBaseModel):
    """
    Base Plate Layout
    """
    anchor: AnchorBolt_US = Field(default_factory=AnchorBolt_US, title="Anchor Bolt Layout", description="Layout and configuration of anchor bolts in the base plate connection. This includes the number of anchor bolts, their positions, and the overall arrangement of the base plate components. Proper layout design is essential for ensuring structural stability and load distribution in steel connections.")

    model_config = ConfigDict(
        title="Bolt",
        json_schema_extra={
            "description": "Layout and configuration of anchor bolts in the base plate connection. This includes the number of anchor bolts, their positions, and the overall arrangement of the base plate components. Proper layout design is essential for ensuring structural stability and load distribution in steel connections."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem, name: str, enum_list: List[str]):
        if unit_system == enUnitSystem.US:
            return cls(anchor=AnchorBolt_US.create_default(unit_system=enUnitSystem.US, name=name, enum_list=enum_list))
        else:
            return cls(anchor=AnchorBolt_US.create_default(unit_system=enUnitSystem.SI, name=name, enum_list=enum_list))

class BasePlateOptions(MBaseModel):
    """
    Base Plate Options
    """
    strength_reduction: BasePlateStrengthReductionFactor = Field(default_factory=BasePlateStrengthReductionFactor, title="Strength Reduction Factors", description="Strength reduction factors used in the design of base plate connections. These factors adjust the nominal strength of concrete and anchors to ensure safety and reliability in structural design.")

    model_config = ConfigDict(
        title="Base Plate Design Parameters",
        json_schema_extra={
            "description": "Design options for base plate connections, including strength reduction factors. These parameters are essential for adjusting the nominal strength of concrete and anchors to ensure safety and reliability in structural design."
        }
    )

class SteelOptions(MBaseModel):
    length: SteelLength_Torsion = Field(default_factory=SteelLength_Torsion, title="Unbraced Length", description="Unbraced length of the steel member, which affects the buckling behavior and load-carrying capacity of the member. The length is a critical parameter in determining the effective length factor and the structural stability of the member.")
    eff_len: EffectiveLengthFactor_Torsion = Field(default_factory=EffectiveLengthFactor_Torsion, title="Effective Length Factor", description="Effective Length Factor")
    factor: SteelMomentModificationFactorLTB = Field(default_factory=SteelMomentModificationFactorLTB, title="Moment Modification Factor", description="Moment Modification Factor")

    model_config = ConfigDict(
        title="Design Parameters",
        json_schema_extra={
            "description": "Options for steel beam design, including effective length factors and moment modification factors. These parameters are essential for determining the structural behavior and load-carrying capacity of steel beams in various applications."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(length=SteelLength_Torsion.create_default(unit_system=enUnitSystem.US), eff_len=EffectiveLengthFactor_Torsion(), factor=SteelMomentModificationFactorLTB())
        else:
            return cls(length=SteelLength_Torsion.create_default(unit_system=enUnitSystem.SI), eff_len=EffectiveLengthFactor_Torsion(), factor=SteelMomentModificationFactorLTB())