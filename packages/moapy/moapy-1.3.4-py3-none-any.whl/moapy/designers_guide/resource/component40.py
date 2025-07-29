import re

def fill_dummy(*, criteria: list[list[str]], data: list[list[str]]):
    G0_COMP_ESACPE = r'\mathit{NA}'
    dummy_value = 0
    expoclass_values = [
        r'XC1',
        r'XC2',
        r'XC3',
        r'XC4',
        r'XD1',
        r'XD2',
        r'XD3',
        r'XS1',
        r'XS2',
        r'XS3',
    ]
    target_symbol = r'expoclass'
    criteria_list = criteria[1]
    result_symbol = data[0][0].split("=")[0].strip()

    def dummy_eq_str(lhs: str, rhs: list[str]):
        return f"{lhs} = {rhs}"

    def match_criteria(criteria: str) -> str | None:
        pattern = rf"^\\sym{{{target_symbol}}} = (?P<value>.*)$"
        match = re.search(pattern, criteria)
        return match.group("value") if match is not None else None

    exist_index = {}
    for i, criterition in enumerate(criteria_list):
        value = match_criteria(criterition)
        if value is None:
            raise ValueError(f"criteria {criterition} is not matched")
        exist_index[expoclass_values.index(value)] = i

    dummy_criteria_list = [
        criteria_list[exist_index[i]]
        if i in exist_index
        else dummy_eq_str(target_symbol, expoclass_values[i])
        for i, value in enumerate(expoclass_values)
    ]

    dummy_data = []
    for data_list in data:
        dummy_data_list = [
            data_list[exist_index[i]]
            if i in exist_index
            else dummy_eq_str(result_symbol, dummy_value)
            for i, value in enumerate(expoclass_values)
        ]
        dummy_data.append(dummy_data_list)

    return {
        'criteria': [criteria[0], dummy_criteria_list],
        'data': dummy_data,
    }

component_list = [
    {
        "id": "G40_COMP_1",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.3(Table6.1)"
        ],
        "title": "Exposure classes based on environmental conditions",
        "description": "This table categorizes exposure classes that define the environmental conditions affecting concrete structures. These classifications help determine durability requirements, including resistance to carbonation, chlorides, freeze-thaw cycles, and chemical attacks, ensuring appropriate design for various environments.",
        "figureFile": "detail_g40_comp_1.png",
        "latexSymbol": "expoclass",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description",
                    "Informative examples where exposure classes can occur (NDP)"
                ],
                [
                    "XC1",
                    "Dry",
                    "Concrete inside buildings with low air humidity, where the corrosion rate will be insignificant."
                ],
                [
                    "XC2",
                    "Wet or permanent high humidity, rarely dry.",
                    "Concrete surfaces subject to long-term water contact or permanently submerged in water or permanently exposed to high humidity; many foundations; water containments (not external). NOTE 1 Leaching could also cause corrosion (see (5), and (6), XA classes)."
                ],
                [
                    "XC3",
                    "Moderate humidity.",
                    "Concrete inside buildings with moderate humidity and not permanent high humidity; External concrete sheltered from rain."
                ],
                [
                    "XC4",
                    "Cyclic wet and dry.",
                    "Concrete surfaces subject to cyclic water contact (e.g. external concrete not sheltered from rain as walls and facades)."
                ],
                [
                    "XD1",
                    "Moderate humidity",
                    "Concrete surfaces exposed to airborne chlorides."
                ],
                [
                    "XD2",
                    "Wet, rarely dry.",
                    "Swimming pools; Concrete components exposed to industrial waters containing chlorides. NOTE 2 If the chloride content of the water is sufficiently low then XD1 applies."
                ],
                [
                    "XD3",
                    "Cyclic wet and dry.",
                    "Parts of bridges exposed to water containing chlorides; Concrete roads, pavements and car park slabs in areas where de-icing agents are frequently used."
                ],
                [
                    "XS1",
                    "Exposed to airborne salt but not in direct contact with sea water.",
                    "Structures near to or on the coast."
                ],
                [
                    "XS2",
                    "Permanently submerged.",
                    "Parts of marine structures and structures in seawater."
                ],
                [
                    "XS3",
                    "Tidal, splash and spray zones.",
                    "Parts of marine structures and structures temporarily or permanently directly over sea water."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_2",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.1(6.1)"
        ],
        "title": "Nominal concrete cover",
        "description": "Nominal concrete cover is the designated thickness of concrete over reinforcement, calculated to protect against environmental impacts and ensure structural durability. This thickness includes the minimum cover required for durability as well as an additional margin to account for construction tolerances.",
        "latexSymbol": "c_{nom}",
        "latexEquation": "\\sym{c_{min}} + \\sym{\\Delta{c_{dev}}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G40_COMP_3",
            "G40_COMP_5"
        ]
    },
    {
        "id": "G40_COMP_3",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.1(6.2)"
        ],
        "title": "Minimum concrete cover based on ERC",
        "description": "Minimum concrete cover based on ERC is determined using Exposure Resistance Classes, considering environmental exposure and durability requirements to protect reinforcement and ensure structural integrity.",
        "latexSymbol": "c_{min}",
        "latexEquation": "\\max(\\sym{c_{min,dur}} + \\sym{\\Sigma\\Delta{c}} , \\sym{c_{min,b}} , 10)",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G40_COMP_28",
            "G40_COMP_6",
            "G40_COMP_21"
        ]
    },
    {
        "id": "G40_COMP_4",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.3(Table6.7)"
        ],
        "title": "Options for determining allowance for deviation in cover",
        "description": "($$\\Delta{c_{dev}}$$) Select the case that applies to your construction scenario to calculate the appropriate allowance for deviation in cover. This ensures accurate adjustments based on construction practices, surface conditions, and quality assurance measures.",
        "latexSymbol": "devioption",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "In general: for execution in tolerance class 1 according to EN 13670",
                    "Standard construction tolerances (Class 1): Typical for general construction projects. Example: Residential or commercial buildings."
                ],
                [
                    "For execution in tolerance class 2 according to EN 13670",
                    "Higher precision tolerances (Class 2): For projects requiring tight construction control. Example: Bridges or industrial facilities."
                ],
                [
                    "Where fabrication is subjected to a quality assurance system",
                    "Systematic monitoring with quality assurance, including cover measurements. Example: Precast concrete elements with certification."
                ],
                [
                    "Where it can be assured that an accurate measurement device is used for monitoring",
                    "High-precision monitoring with non-conforming elements being rejected. Example: Factory-manufactured concrete panels."
                ],
                [
                    "For concrete members in exposure class XC1",
                    "Minimal risk of corrosion due to mild exposure. Example: Indoor concrete structures not exposed to significant moisture."
                ],
                [
                    "For concrete cast against surfaces with exposed aggregate",
                    "Cast against roughened or aggregate-exposed surfaces. Example: Interfaces between concrete layers."
                ],
                [
                    "For concrete cast against unevenness due to formwork or excavation sheeting",
                    "Cast against irregular surfaces, such as ribbed finishes or architectural textures. Example: Decorative concrete walls."
                ],
                [
                    "Concrete cast against prepared ground",
                    "Cast against prepared but uneven ground. Example: Concrete cast on a leveled but rough blinding layer."
                ],
                [
                    "Concrete cast directly against unprepared soil",
                    "Cast directly against unprepared soil, requiring higher allowances. Example: Footings or foundations poured on natural soil."
                ],
                [
                    "Post-installed reinforcing bars",
                    "Bars installed after the concrete is cast, requiring specific tolerances. Example: Retrofitting structures with drilled anchors."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_5",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.3(Table6.7)"
        ],
        "title": "Allowance for deviation in cover",
        "description": "Allowance for deviation in cover accounts for possible negative deviations from the specified concrete cover during construction. It is added to the minimum cover to ensure the nominal cover meets design requirements despite construction tolerances. The specific value for the allowance is defined in project specifications or the applicable standards.",
        "latexSymbol": "\\Delta{c_{dev}}",
        "latexEquation": "10",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{devioption} = In general: for execution in tolerance class 1 according to EN 13670",
                    "\\sym{devioption} = For execution in tolerance class 2 according to EN 13670",
                    "\\sym{devioption} = Where fabrication is subjected to a quality assurance system",
                    "\\sym{devioption} = Where it can be assured that an accurate measurement device is used for monitoring",
                    "\\sym{devioption} = For concrete members in exposure class XC1",
                    "\\sym{devioption} = For concrete cast against surfaces with exposed aggregate",
                    "\\sym{devioption} = For concrete cast against unevenness due to formwork or excavation sheeting",
                    "\\sym{devioption} = Concrete cast against prepared ground",
                    "\\sym{devioption} = Concrete cast directly against unprepared soil",
                    "\\sym{devioption} = Post-installed reinforcing bars"
                ]
            ],
            "data": [
                [
                    "10"
                ],
                [
                    "5"
                ],
                [
                    "5"
                ],
                [
                    "0"
                ],
                [
                    "5"
                ],
                [
                    "5"
                ],
                [
                    "10"
                ],
                [
                    "40"
                ],
                [
                    "75"
                ],
                [
                    "5"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_6",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2(1)"
        ],
        "title": "Summation of minimum cover adjustments",
        "description": "Summation of minimum cover adjustments represents the total adjustments to the minimum concrete cover, taking into account factors such as reduced design service life, improved compaction, prestressing requirements, additional concrete protection, special measures, and abrasion resistance.",
        "latexSymbol": "\\Sigma\\Delta{c}",
        "latexEquation": "\\sym{\\Delta{c_{min}}} + \\sym{\\Delta{c_{min,30}}} + \\sym{\\Delta{c_{min,exc}}} + \\sym{\\Delta{c_{min,p}}} + \\sym{\\Delta{c_{dur,red1}}} + \\sym{\\Delta{c_{dur,red2}}} + \\sym{\\Delta{c_{dur,abr}}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_8",
            "G40_COMP_10",
            "G40_COMP_12",
            "G40_COMP_14",
            "G40_COMP_16",
            "G40_COMP_19",
            "G40_COMP_18"
        ]
    },
    {
        "id": "G40_COMP_7",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.1(2)"
        ],
        "title": "Casting against soil conditions for minimum cover adjustments",
        "description": "Choose the type of surface against which concrete will be cast to determine whether additional concrete cover is required. For surfaces directly in contact with soil, adjustments are made based on orientation to ensure adequate compaction and durability.",
        "latexSymbol": "castsoil",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Not cast against soil",
                    "Concrete is cast against a surface that does not come into contact with soil, such as formwork or other concrete elements."
                ],
                [
                    "Horizontal soil surface",
                    "Concrete is cast against a horizontal soil ground surface, such as the bottom of a foundation or underground structure. Easier compaction."
                ],
                [
                    "Vertical soil surface",
                    "Concrete is cast against a vertical soil surface, such as the side of a foundation or underground wall. Compaction is harder, requiring additional cover."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_8",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.1(2)"
        ],
        "title": "Minimum cover adjustments for concrete cast against soil",
        "description": "Minimum cover adjustments for concrete cast against soil are determined based on the type of soil contact, addressing variability and compaction challenges for different soil surface orientations during construction.",
        "latexSymbol": "\\Delta{c_{min}}",
        "latexEquation": "0",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_7"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{castsoil} = Not cast against soil",
                    "\\sym{castsoil} = Horizontal soil surface",
                    "\\sym{castsoil} = Vertical soil surface"
                ]
            ],
            "data": [
                [
                    "0"
                ],
                [
                    "0"
                ],
                [
                    "5"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_9",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(2)"
        ],
        "title": "Design service life",
        "description": "($$\\Delta{c_{min,30}}$$) Design service life refers to the intended period during which a structure or component is expected to perform its required functions without significant maintenance or repair. It is a key factor in determining durability requirements, including concrete cover thickness and material selection, to ensure the structure meets its performance criteria throughout its lifespan.",
        "latexSymbol": "T_{lf}",
        "type": "string",
        "unit": "years",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "100 years",
                    "Monumental building structures, Bridges, other civil engineering structures supporting road or railway traffic"
                ],
                [
                    "50 years",
                    "Building structures not covered by another category, Bridges where the main structural members have reduced protection"
                ],
                [
                    "25 years",
                    "Agricultural, and similar structures Replaceable structural parts Replaceable structural parts other than tension components"
                ],
                [
                    "10 years or less",
                    "Temporary structures"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_10",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(2)"
        ],
        "title": "Minimum cover adjustment for reduced design service life",
        "description": "Minimum cover adjustment for reduced design service life is the reduction applied to the concrete cover when the design service life of a structure is 30 years or less, or for temporary structures. The adjustment typically allows a reduction of up to 5 mm unless specified otherwise by the National Annex.",
        "latexSymbol": "\\Delta{c_{min,30}}",
        "latexEquation": "0",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_9"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{T_{lf}} = 100 years",
                    "\\sym{T_{lf}} = 50 years",
                    "\\sym{T_{lf}} = 25 years",
                    "\\sym{T_{lf}} = 10 years or less"
                ]
            ],
            "data": [
                [
                    "0"
                ],
                [
                    "0"
                ],
                [
                    "-5"
                ],
                [
                    "-5"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_11",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(3)"
        ],
        "title": "Execution conditions for minimum cover adjustment",
        "description": "($$\\Delta{c_{min,exc}}$$) Select the execution condition that applies to your project to determine whether the minimum cover adjustment can be applied. This ensures accurate adjustments based on construction quality and curing practices.",
        "latexSymbol": "excucond",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Standard practices without enhanced measures",
                    "No specific measures for enhanced compaction or curing below Class 3 standards; typical construction methods are followed."
                ],
                [
                    "Enhanced compaction ensured",
                    "Concrete compaction is achieved through geometry, placement, and curing, such as slab geometries where reinforcement positions are unaffected."
                ],
                [
                    "Compliance with curing Class 3 or higher",
                    "Curing meets at least Class 3 requirements as per EN 13670, ensuring improved curing quality."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_12",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(3)"
        ],
        "title": "Minimum cover adjustment for enhanced execution",
        "description": "Minimum cover adjustment for enhanced execution refers to the reduction in the required concrete cover when improved compaction and curing measures are applied during construction. This adjustment recognizes superior construction quality that ensures better durability performance with reduced cover thickness.",
        "latexSymbol": "\\Delta{c_{min,exc}}",
        "latexEquation": "0",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_11"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{excucond} = Standard practices without enhanced measures",
                    "\\sym{excucond} = Enhanced compaction ensured",
                    "\\sym{excucond} = Compliance with curing Class 3 or higher"
                ]
            ],
            "data": [
                [
                    "0"
                ],
                [
                    "-5"
                ],
                [
                    "-5"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_13",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(4)"
        ],
        "title": "Prestressing conditions for minimum cover adjustment",
        "description": "($$\\Delta{c_{min,p}}$$)Select the prestressing condition that applies to your structure to determine if the additional minimum cover adjustment for prestressing tendons is required. This ensures proper concrete cover is applied based on the reinforcement type and protection measures.",
        "latexSymbol": "prescond",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Non-prestressed reinforcement or other conditions",
                    "The structure does not include prestressing tendons, making additional cover for prestressing unnecessary."
                ],
                [
                    "Pre-tensioned or post-tensioned tendons",
                    "Additional concrete cover is required for prestressing tendons to ensure durability and protection."
                ],
                [
                    "Internal bonded post-tensioning with protection level 2 or 3",
                    "Prestressing tendons are already protected according to high-level durability standards."
                ],
                [
                    "Internal unbonded prestressing tendons with corrosion-resistant sheaths",
                    "Tendons are enclosed in corrosion-resistant sheaths, providing sufficient protection."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_14",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(4)"
        ],
        "title": "Minimum cover adjustment for prestressing",
        "description": "Minimum cover adjustment for prestressing is an additional concrete cover applied to ensure adequate protection for prestressing tendons in pre-tensioned or post-tensioned structures. This adjustment accounts for the unique durability and safety requirements of prestressed concrete elements.",
        "latexSymbol": "\\Delta{c_{min,p}}",
        "latexEquation": "14",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_13"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{prescond} = Non-prestressed reinforcement or other conditions",
                    "\\sym{prescond} = Pre-tensioned or post-tensioned tendons",
                    "\\sym{prescond} = Internal bonded post-tensioning with protection level 2 or 3",
                    "\\sym{prescond} = Internal unbonded prestressing tendons with corrosion-resistant sheaths"
                ]
            ],
            "data": [
                [
                    "0"
                ],
                [
                    "10"
                ],
                [
                    "0"
                ],
                [
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_15",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(5)"
        ],
        "title": "Additional protection conditions for minimum cover reduction",
        "description": "($$\\Delta{c_{dur,red1}}$$) Select whether additional protection measures, such as surface coatings, have been applied to your concrete structure. This will determine if the minimum cover reduction can be applied.",
        "latexSymbol": "addprotec",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Concrete without additional protection",
                    "No additional measures are applied, so the minimum cover remains unchanged."
                ],
                [
                    "Concrete with additional protection applied",
                    "Additional protection, such as surface coatings, is provided, allowing a reduction in required cover."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_16",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(5)"
        ],
        "title": "Minimum cover reduction for additional concrete protection",
        "description": "Minimum cover reduction for additional concrete protection is the decrease in required concrete cover when additional protection measures, such as surface coatings, are applied. The specific reduction value is determined by testing or experience and typically does not exceed 10 mm unless otherwise specified by the National Annex.",
        "latexSymbol": "\\Delta{c_{dur,red1}}",
        "latexEquation": "16",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_15"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{addprotec} = Concrete without additional protection",
                    "\\sym{addprotec} = Concrete with additional protection applied"
                ]
            ],
            "data": [
                [
                    "0"
                ],
                [
                    "-10"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_17",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(6)"
        ],
        "title": "Abrasion exposure conditions for minimum cover addition",
        "description": "($$\\Delta{c_{dur,abr}}$$)Select the abrasion exposure condition that applies to your structure to determine if additional concrete cover is required for abrasion resistance. This ensures the structure is properly designed for durability under specific abrasion conditions.",
        "latexSymbol": "abraexpo",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "No significant abrasion exposure",
                    "Abrasion is negligible, so no additional cover for abrasion resistance is required."
                ],
                [
                    "XM1: Low abrasion exposure",
                    "Concrete subjected to minor abrasion, requiring an additional cover for durability."
                ],
                [
                    "XM2: Moderate abrasion exposure",
                    "Concrete subjected to moderate abrasion, requiring an additional cover for durability."
                ],
                [
                    "XM3: Severe abrasion exposure",
                    "Concrete subjected to severe abrasion, requiring an additional cover for durability."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_18",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(6)"
        ],
        "title": "Minimum cover addition for abrasion resistance",
        "description": "Minimum cover addition for abrasion resistance is an increase in the required concrete cover to account for wear and tear caused by abrasive forces, such as moving objects or mechanical impacts. The additional cover depends on the abrasion exposure class (XM) and ensures durability under specified conditions.",
        "latexSymbol": "\\Delta{c_{dur,abr}}",
        "latexEquation": "0",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_17"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{abraexpo} = No significant abrasion exposure",
                    "\\sym{abraexpo} = XM1: Low abrasion exposure",
                    "\\sym{abraexpo} = XM2: Moderate abrasion exposure",
                    "\\sym{abraexpo} = XM3: Severe abrasion exposure"
                ]
            ],
            "data": [
                [
                    "0"
                ],
                [
                    "5"
                ],
                [
                    "10"
                ],
                [
                    "15"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_19",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(9)"
        ],
        "title": "Minimum cover reduction for special protection measures",
        "description": "Minimum cover reduction for special protection measures is the decrease in required concrete cover when additional protective actions, other than surface coatings, are implemented. These measures, determined by project-specific requirements or testing, reduce the risk of reinforcement corrosion and enhance durability, allowing for a reduction in concrete cover.",
        "latexSymbol": "\\Delta{c_{dur,red2}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "default": 0.0,
        "const": True
    },
    {
        "id": "G40_COMP_20",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.3(Table6.5)"
        ],
        "title": "Reinforcement type for minimum cover calculation",
        "description": "($$c_{min,b}$$) Select the type of reinforcement used in your structure to determine the appropriate method for calculating the minimum concrete cover for bond. This ensures the correct cover is applied based on the reinforcement configuration.",
        "latexSymbol": "rebartype",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Separated bars",
                    "Individual reinforcement bars that are not bundled together."
                ],
                [
                    "Bundled bars",
                    "Reinforcement bars grouped into a single bundle, requiring an equivalent diameter for calculations."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_21",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.3(Table6.5)"
        ],
        "title": "Minimum concrete cover for bond",
        "description": "Minimum concrete cover for bond ensures safe load transfer between concrete and reinforcement. For separated bars, the minimum cover is calculated based on the diameter of the individual bar. For bundled bars, the minimum cover is determined using the equivalent diameter, which represents the total area of the bundled bars as a single equivalent cross-section.",
        "latexSymbol": "c_{min,b}",
        "latexEquation": "\\sym{\\phi}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G40_COMP_20",
            "G40_COMP_22",
            "G40_COMP_23"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{rebartype} = Separated bars",
                    "\\sym{rebartype} = Bundled bars"
                ]
            ],
            "data": [
                [
                    "\\sym{\\phi}"
                ],
                [
                    "\\sym{\\phi_{b}}"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_22",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "11.4.3(1)"
        ],
        "title": "Diameter of a single reinforcement bar",
        "description": "The diameter of a single reinforcement bar represents the thickness of an individual bar used in concrete structures. It is a key parameter for calculating the cross-sectional area, determining spacing, and assessing bond strength in structural design.",
        "latexSymbol": "\\phi",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "default": 32.0,
        "limits": {
            "inMin": 0
        }
    },
    {
        "id": "G40_COMP_23",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "11.4.3(11.6)"
        ],
        "title": "Equivalent diameter of bundled bar",
        "description": "The equivalent diameter of bundled bars is a calculated value used to represent a bundle of reinforcement bars as a single bar for design purposes. It is determined based on the total cross-sectional area of the bundled bars and ensures accurate calculations for anchorage and spacing requirements.",
        "latexSymbol": "\\phi_{b}",
        "latexEquation": "\\sqrt{(\\frac{4}{\\pi} \\times \\sym{A_{s}})}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G40_COMP_24"
        ]
    },
    {
        "id": "G40_COMP_24",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "11.4.3(1)"
        ],
        "title": "Cross-sectional area of reinforcement",
        "description": "The cross-sectional area of reinforcement refers to the total area of all steel bars in a specific section of a concrete structure. It is a critical parameter for structural design, determining the capacity of reinforcement to resist forces such as tension, compression, or shear.",
        "latexSymbol": "A_{s}",
        "latexEquation": "\\frac{(\\pi \\times \\sym{\\phi}^{2})}{4} \\times \\sym{n_{b}}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G40_COMP_22",
            "G40_COMP_25"
        ]
    },
    {
        "id": "G40_COMP_25",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "11.4.3(1)"
        ],
        "title": "Number of bars in a bundle",
        "description": "Select the number of bars in a bundle to ensure proper arrangement and spacing based on structural and design requirements. The number of bars directly impacts the required contact and clear distance between bundles.",
        "latexSymbol": "n_{b}",
        "type": "string",
        "unit": "ea",
        "notation": "standard",
        "decimal": 0,
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "2",
                    "Two bars arranged in parallel contact, suitable for standard configurations."
                ],
                [
                    "3",
                    "Three bars in parallel contact, the maximum for general cases."
                ],
                [
                    "4",
                    "Four bars in parallel contact, allowed only for vertical bars in compression or bars in a lapped joint."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_26",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(Table6.3)"
        ],
        "title": "Carbonation resistance classification",
        "description": "The carbonation resistance classification defines the levels of concrete's resistance to corrosion caused by carbonation. These classes (XRC0.5 to XRC7) indicate increasing levels of durability, with higher numbers representing greater resistance required in environments with significant carbonation exposure.",
        "latexSymbol": "ercxrc",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "XRC0.5",
                    "Very low carbonation resistance, suitable for non-structural elements in low exposure environments. Example: Interior walls in dry areas."
                ],
                [
                    "XRC1",
                    "Low carbonation resistance, applicable to mild exposure conditions with limited risk of carbonation. Example: Sheltered concrete in temperate climates."
                ],
                [
                    "XRC2",
                    "Moderate carbonation resistance, appropriate for structures in environments with moderate carbonation exposure. Example: Residential buildings in urban areas."
                ],
                [
                    "XRC3",
                    "Standard carbonation resistance, designed for typical structural applications under normal exposure conditions. Example: Office buildings in cities."
                ],
                [
                    "XRC4",
                    "High carbonation resistance, used in structures exposed to significant carbonation risks. Example: Concrete facades in industrial areas."
                ],
                [
                    "XRC5",
                    "Very high carbonation resistance, suitable for critical structures requiring enhanced protection. Example: Bridge elements in high traffic zones."
                ],
                [
                    "XRC6",
                    "Extreme carbonation resistance, applied in structures with severe carbonation risks and long service life. Example: Underground metro tunnels."
                ],
                [
                    "XRC7",
                    "Maximum carbonation resistance, used in highly demanding environments with extreme exposure conditions. Example: Historical monuments in polluted urban environments."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_27",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(Table6.4)"
        ],
        "title": "Chloride resistance classification",
        "description": "The chloride resistance classification defines the levels of concrete's resistance to corrosion caused by chloride ingress. These classes (XRDS0.5 to XRDS10) indicate increasing levels of protection, with higher numbers representing greater resistance required for environments with higher chloride exposure risks, such as marine or de-icing salt conditions.",
        "latexSymbol": "ercxrd",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "XRDS0.5",
                    "Very low chloride resistance, suitable for non-structural elements in environments with minimal chloride exposure. Example: Interior concrete elements in dry environments."
                ],
                [
                    "XRDS1",
                    "Low chloride resistance, applicable for mild exposure conditions with limited chloride penetration. Example: Sheltered concrete surfaces in low chloride areas."
                ],
                [
                    "XRDS1.5",
                    "Slightly increased chloride resistance, suitable for environments with moderate chloride risks. Example: Residential structures in urban areas with minor road salt exposure."
                ],
                [
                    "XRDS2",
                    "Moderate chloride resistance, designed for structural applications in areas with noticeable chloride exposure. Example: Parking garages or bridges in regions using de-icing salts."
                ],
                [
                    "XRDS3",
                    "High chloride resistance, appropriate for structures exposed to significant chloride risks. Example: Coastal buildings exposed to airborne chlorides."
                ],
                [
                    "XRDS4",
                    "Very high chloride resistance, used for critical structures requiring enhanced chloride protection. Example: Marine piers or structures partially submerged in seawater."
                ],
                [
                    "XRDS5",
                    "Extreme chloride resistance, for structures in severe chloride exposure environments. Example: Offshore platforms exposed to constant seawater splashing."
                ],
                [
                    "XRDS6",
                    "Maximum chloride resistance, applied to highly demanding environments with prolonged chloride risks. Example: Underwater tunnels fully immersed in seawater."
                ],
                [
                    "XRDS8",
                    "Ultra-high chloride resistance, suitable for specialized structures with extreme durability requirements. Example: Nuclear waste storage in chloride-prone environments."
                ],
                [
                    "XRDS10",
                    "Superior chloride resistance, used in the most challenging environments where maximum protection is critical. Example: Subsea structures exposed to aggressive chloride environments for extended service life."
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_28",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(1)"
        ],
        "title": "Minimum concrete cover for durability requirement",
        "description": "Minimum concrete cover for durability requirement is the specified thickness of concrete over reinforcement needed to ensure durability under environmental conditions. This requirement protects against factors such as corrosion and structural degradation.",
        "latexSymbol": "c_{min,dur}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_1",
            "G40_COMP_9",
            "G40_COMP_29",
            "G40_COMP_30",
            "G40_COMP_33",
            "G40_COMP_34",
            "G40_COMP_31",
            "G40_COMP_32"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{expoclass} = XC1",
                    "\\sym{expoclass} = XC2",
                    "\\sym{expoclass} = XC3",
                    "\\sym{expoclass} = XC4",
                    "\\sym{expoclass} = XD1",
                    "\\sym{expoclass} = XD2",
                    "\\sym{expoclass} = XD3",
                    "\\sym{expoclass} = XS1",
                    "\\sym{expoclass} = XS2",
                    "\\sym{expoclass} = XS3"
                ],
                [
                    "\\sym{T_{lf}} = 10 years or less",
                    "\\sym{T_{lf}} = 25 years",
                    "\\sym{T_{lf}} = 50 years",
                    "\\sym{T_{lf}} = 100 years"
                ]
            ],
            "data": [
                [
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,100}}"
                ],
                [
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,100}}"
                ],
                [
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,100}}"
                ],
                [
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,50}}",
                    "\\sym{c_{min,dur,XC,100}}"
                ],
                [
                    "\\sym{c_{min,dur,XD,50}}",
                    "\\sym{c_{min,dur,XD,50}}",
                    "\\sym{c_{min,dur,XD,50}}",
                    "\\sym{c_{min,dur,XD,100}}"
                ],
                [
                    "\\sym{c_{min,dur,XD,50}}",
                    "\\sym{c_{min,dur,XD,50}}",
                    "\\sym{c_{min,dur,XD,50}}",
                    "\\sym{c_{min,dur,XD,100}}"
                ],
                [
                    "\\sym{c_{min,dur,XD,50}}",
                    "\\sym{c_{min,dur,XD,50}}",
                    "\\sym{c_{min,dur,XD,50}}",
                    "\\sym{c_{min,dur,XD,100}}"
                ],
                [
                    "\\sym{c_{min,dur,XS,50}}",
                    "\\sym{c_{min,dur,XS,50}}",
                    "\\sym{c_{min,dur,XS,50}}",
                    "\\sym{c_{min,dur,XS,100}}"
                ],
                [
                    "\\sym{c_{min,dur,XS,50}}",
                    "\\sym{c_{min,dur,XS,50}}",
                    "\\sym{c_{min,dur,XS,50}}",
                    "\\sym{c_{min,dur,XS,100}}"
                ],
                [
                    "\\sym{c_{min,dur,XS,50}}",
                    "\\sym{c_{min,dur,XS,50}}",
                    "\\sym{c_{min,dur,XS,50}}",
                    "\\sym{c_{min,dur,XS,100}}"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_29",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(Table6.3)"
        ],
        "title": "Minimum concrete cover for carbonation resistance, 50-year design life",
        "description": "This table specifies the minimum concrete cover required for durability against carbonation in environments classified by exposure classes (XC1 to XC4) and carbonation resistance levels (XRC0.5 to XRC7) for a design service life of 50 years. Higher exposure and resistance levels require greater cover to protect reinforcement from corrosion.",
        "latexSymbol": "c_{min,dur,XC,50}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_26",
            "G40_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{ercxrc} = XRC0.5",
                    "\\sym{ercxrc} = XRC1",
                    "\\sym{ercxrc} = XRC2",
                    "\\sym{ercxrc} = XRC3",
                    "\\sym{ercxrc} = XRC4",
                    "\\sym{ercxrc} = XRC5",
                    "\\sym{ercxrc} = XRC6",
                    "\\sym{ercxrc} = XRC7"
                ],
                [
                    "\\sym{expoclass} = XC1",
                    "\\sym{expoclass} = XC2",
                    "\\sym{expoclass} = XC3",
                    "\\sym{expoclass} = XC4",
                    "expoclass = XD1",
                    "expoclass = XD2",
                    "expoclass = XD3",
                    "expoclass = XS1",
                    "expoclass = XS2",
                    "expoclass = XS3"
                ]
            ],
            "data": [
                [
                    "10",
                    "10",
                    "10",
                    "10",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "10",
                    "10",
                    "10",
                    "10",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "10",
                    "10",
                    "15",
                    "15",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "10",
                    "15",
                    "20",
                    "20",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "10",
                    "15",
                    "25",
                    "25",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "15",
                    "20",
                    "25",
                    "30",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "15",
                    "25",
                    "35",
                    "40",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "15",
                    "25",
                    "40",
                    "45",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_30",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(Table6.3)"
        ],
        "title": "Minimum concrete cover for carbonation resistance, 100-year design life",
        "description": "This parameter specifies the minimum concrete cover required for durability against carbonation in environments classified by exposure classes (XC1 to XC4) and carbonation resistance levels (XRC). It applies to structures with a 100-year design service life, ensuring long-term protection of reinforcement against corrosion.",
        "latexSymbol": "c_{min,dur,XC,100}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_26",
            "G40_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{ercxrc} = XRC0.5",
                    "\\sym{ercxrc} = XRC1",
                    "\\sym{ercxrc} = XRC2",
                    "\\sym{ercxrc} = XRC3",
                    "\\sym{ercxrc} = XRC4",
                    "\\sym{ercxrc} = XRC5",
                    "\\sym{ercxrc} = XRC6",
                    "\\sym{ercxrc} = XRC7"
                ],
                [
                    "\\sym{expoclass} = XC1",
                    "\\sym{expoclass} = XC2",
                    "\\sym{expoclass} = XC3",
                    "\\sym{expoclass} = XC4",
                    "expoclass = XD1",
                    "expoclass = XD2",
                    "expoclass = XD3",
                    "expoclass = XS1",
                    "expoclass = XS2",
                    "expoclass = XS3"
                ]
            ],
            "data": [
                [
                    "10",
                    "10",
                    "10",
                    "10",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "10",
                    "10",
                    "15",
                    "15",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "15",
                    "15",
                    "25",
                    "25",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "15",
                    "20",
                    "30",
                    "30",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "20",
                    "25",
                    "35",
                    "40",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "25",
                    "30",
                    "45",
                    "45",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "25",
                    "35",
                    "55",
                    "55",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "30",
                    "40",
                    "60",
                    "60",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_31",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(Table6.4)"
        ],
        "title": "Minimum concrete cover for chloride resistance, 50-year design life",
        "description": "This parameter specifies the minimum concrete cover required for durability against chloride ingress in environments classified by exposure classes (XS1 to XS3) and chloride resistance levels (XRDS). It applies to structures with a 50-year design service life, ensuring sufficient protection of reinforcement in chloride-rich environments such as marine conditions.",
        "latexSymbol": "c_{min,dur,XS,50}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_1",
            "G40_COMP_27"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{ercxrd} = XRDS0.5",
                    "\\sym{ercxrd} = XRDS1",
                    "\\sym{ercxrd} = XRDS1.5",
                    "\\sym{ercxrd} = XRDS2",
                    "\\sym{ercxrd} = XRDS3",
                    "\\sym{ercxrd} = XRDS4",
                    "\\sym{ercxrd} = XRDS5",
                    "\\sym{ercxrd} = XRDS6",
                    "\\sym{ercxrd} = XRDS8",
                    "\\sym{ercxrd} = XRDS10"
                ],
                [
                    "expoclass = XC1",
                    "expoclass = XC2",
                    "expoclass = XC3",
                    "expoclass = XC4",
                    "expoclass = XD1",
                    "expoclass = XD2",
                    "expoclass = XD3",
                    "\\sym{expoclass} = XS1",
                    "\\sym{expoclass} = XS2",
                    "\\sym{expoclass} = XS3"
                ]
            ],
            "data": [
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "20",
                    "20",
                    "30"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "20",
                    "25",
                    "35"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "25",
                    "30",
                    "40"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "25",
                    "35",
                    "45"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "30",
                    "40",
                    "55"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "30",
                    "50",
                    "60"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "35",
                    "60",
                    "70"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "40",
                    "65",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "45",
                    "75",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "50",
                    "80",
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_32",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(Table6.4)"
        ],
        "title": "Minimum concrete cover for chloride resistance, 100-year design life",
        "description": "This parameter specifies the minimum concrete cover required for durability against chloride ingress in environments classified by exposure classes (XS1 to XS3) and chloride resistance levels (XRDS). It applies to structures with a 100-year design service life, ensuring long-term protection of reinforcement in chloride-rich environments, such as marine conditions or areas exposed to de-icing salts.",
        "latexSymbol": "c_{min,dur,XS,100}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_1",
            "G40_COMP_27"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{ercxrd} = XRDS0.5",
                    "\\sym{ercxrd} = XRDS1",
                    "\\sym{ercxrd} = XRDS1.5",
                    "\\sym{ercxrd} = XRDS2",
                    "\\sym{ercxrd} = XRDS3",
                    "\\sym{ercxrd} = XRDS4",
                    "\\sym{ercxrd} = XRDS5",
                    "\\sym{ercxrd} = XRDS6",
                    "\\sym{ercxrd} = XRDS8",
                    "\\sym{ercxrd} = XRDS10"
                ],
                [
                    "expoclass = XC1",
                    "expoclass = XC2",
                    "expoclass = XC3",
                    "expoclass = XC4",
                    "expoclass = XD1",
                    "expoclass = XD2",
                    "expoclass = XD3",
                    "\\sym{expoclass} = XS1",
                    "\\sym{expoclass} = XS2",
                    "\\sym{expoclass} = XS3"
                ]
            ],
            "data": [
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "20",
                    "30",
                    "40"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "25",
                    "35",
                    "45"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "30",
                    "40",
                    "50"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "30",
                    "45",
                    "55"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "35",
                    "50",
                    "65"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "40",
                    "60",
                    "80"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "45",
                    "70",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "50",
                    "80",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "55",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "65",
                    "0",
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_33",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(Table6.4)"
        ],
        "title": "Minimum concrete cover for de-icing chloride resistance, 50-year design life",
        "description": "This parameter specifies the minimum concrete cover required for durability against chloride ingress in environments exposed to de-icing salts, classified by exposure classes (XD1 to XD3) and chloride resistance levels (XRDS). It applies to structures with a 50-year design service life, ensuring protection of reinforcement against corrosion caused by chlorides in roadways, bridges, or other areas where de-icing salts are used.",
        "latexSymbol": "c_{min,dur,XD,50}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_1",
            "G40_COMP_27"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{ercxrd} = XRDS0.5",
                    "\\sym{ercxrd} = XRDS1",
                    "\\sym{ercxrd} = XRDS1.5",
                    "\\sym{ercxrd} = XRDS2",
                    "\\sym{ercxrd} = XRDS3",
                    "\\sym{ercxrd} = XRDS4",
                    "\\sym{ercxrd} = XRDS5",
                    "\\sym{ercxrd} = XRDS6",
                    "\\sym{ercxrd} = XRDS8",
                    "\\sym{ercxrd} = XRDS10"
                ],
                [
                    "expoclass = XC1",
                    "expoclass = XC2",
                    "expoclass = XC3",
                    "expoclass = XC4",
                    "\\sym{expoclass} = XD1",
                    "\\sym{expoclass} = XD2",
                    "\\sym{expoclass} = XD3",
                    "expoclass = XS1",
                    "expoclass = XS2",
                    "expoclass = XS3"
                ]
            ],
            "data": [
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "20",
                    "20",
                    "30",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "20",
                    "25",
                    "35",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "25",
                    "30",
                    "40",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "25",
                    "35",
                    "45",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "30",
                    "40",
                    "55",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "30",
                    "50",
                    "60",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "35",
                    "60",
                    "70",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "40",
                    "65",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "45",
                    "75",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "50",
                    "80",
                    "0",
                    "0",
                    "0",
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G40_COMP_34",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "6.5.2.2(Table6.4)"
        ],
        "title": "Minimum concrete cover for de-icing chloride resistance, 100-year design life",
        "description": "This parameter specifies the minimum concrete cover required for durability against chloride ingress in environments exposed to de-icing salts, classified by exposure classes (XD1 to XD3) and chloride resistance levels (XRDS). It applies to structures with a 100-year design service life, ensuring long-term protection of reinforcement against corrosion in roadways, bridges, and other areas subjected to de-icing salts.",
        "latexSymbol": "c_{min,dur,XD,100}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G40_COMP_1",
            "G40_COMP_27"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{ercxrd} = XRDS0.5",
                    "\\sym{ercxrd} = XRDS1",
                    "\\sym{ercxrd} = XRDS1.5",
                    "\\sym{ercxrd} = XRDS2",
                    "\\sym{ercxrd} = XRDS3",
                    "\\sym{ercxrd} = XRDS4",
                    "\\sym{ercxrd} = XRDS5",
                    "\\sym{ercxrd} = XRDS6",
                    "\\sym{ercxrd} = XRDS8",
                    "\\sym{ercxrd} = XRDS10"
                ],
                [
                    "expoclass = XC1",
                    "expoclass = XC2",
                    "expoclass = XC3",
                    "expoclass = XC4",
                    "\\sym{expoclass} = XD1",
                    "\\sym{expoclass} = XD2",
                    "\\sym{expoclass} = XD3",
                    "expoclass = XS1",
                    "expoclass = XS2",
                    "expoclass = XS3"
                ]
            ],
            "data": [
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "20",
                    "30",
                    "40",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "25",
                    "35",
                    "45",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "30",
                    "40",
                    "50",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "30",
                    "45",
                    "55",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "35",
                    "50",
                    "65",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "40",
                    "60",
                    "80",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "45",
                    "70",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "50",
                    "80",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "55",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                [
                    "0",
                    "0",
                    "0",
                    "0",
                    "65",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ]
            ]
        }
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/133269751/2G+EN1992-1-1+Nominal+Concrete+Cover
        'id': '40',
        'standardType': '2G:EUROCODE',
        'codeName': '2G:EN1992-1-1',
        'codeTitle': 'Eurocode 2 — Design of concrete structures - Part 1-1: General rules and rules for buildings, bridges and civil engineering structures',
        'title': 'Nominal Concrete Cover Based on Exposure Resistance Classes',
        'description': r"[2G:EN1992-1-1] This guide offers a detailed approach to calculating the required concrete cover thickness for durability based on the Exposure Resistance Classes (ERC) as defined in the Eurocode 2nd Generation standards. It provides a structured process to determine the appropriate cover thickness for varying exposure conditions, ensuring effective corrosion protection and longevity of the concrete structure. The guide includes step-by-step instructions on selecting ERC values and applying them to calculate minimum cover thickness for diverse environmental scenarios. Tailored for engineers and structural designers, this guide enables users to meet Eurocode durability requirements, thereby optimizing concrete structure performance and safety across various applications.",
        'edition': '2003',
        'targetComponents': ['G40_COMP_2', 'G40_COMP_3', 'G40_COMP_5'],
        'testInput': [
            {'component': 'G40_COMP_1', 'value': 'XC1'},
            {'component': 'G40_COMP_4', 'value': 'In general: for execution in tolerance class 1 according to EN 13670'},
            {'component': 'G40_COMP_7', 'value': 'Vertical soil surface'},
            {'component': 'G40_COMP_9', 'value': '25 years'},
            {'component': 'G40_COMP_11', 'value': 'Enhanced compaction ensured'},
            {'component': 'G40_COMP_13', 'value': 'Pre-tensioned or post-tensioned tendons'},
            {'component': 'G40_COMP_15', 'value': 'Concrete with additional protection applied'},
            {'component': 'G40_COMP_17', 'value': 'XM1: Low abrasion exposure'},
            {'component': 'G40_COMP_20', 'value': 'Separated bars'},
            {'component': 'G40_COMP_22', 'value': 32},
            {'component': 'G40_COMP_25', 'value': '2'},
            {'component': 'G40_COMP_26', 'value': 'XRC0.5'},
            {'component': 'G40_COMP_27', 'value': 'XRDS0.5'},
        ],
    }
]
