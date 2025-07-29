component_list = [
    {
        "id": "G27_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(1)"
        ],
        "title": "Section type without shear reinforcement for shear resistance",
        "description": "Before calculating the shear resistance for reinforced concrete members without shear reinforcement, the type of structural element to be analyzed must be selected. This ensures that the appropriate methodology and parameters are applied for accurate and reliable design.",
        "latexSymbol": "secwobar",
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
                    "Reinforced concrete section",
                    "A reinforced concrete section without shear reinforcement; typically used for general concrete elements."
                ],
                [
                    "Cracked prestressed section",
                    "A prestressed concrete section cracked in flexure; includes bonded prestressing for shear calculations."
                ],
                [
                    "Support region",
                    "A section near supports; includes adjustments for load positions and reduced shear contributions."
                ]
            ]
        }
    },
    {
        "id": "G27_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.1(3)"
        ],
        "title": "Design shear force",
        "description": "The design shear force is the calculated value of the applied shear force acting on a concrete section due to external loading and prestressing. It is used to assess whether the section's resistance is sufficient to withstand the applied shear.",
        "latexSymbol": "V_{Ed}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "default": 350.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G27_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(1)"
        ],
        "title": "Axial force in the cross-sectio",
        "description": "Axial force in the cross-section refers to the total force acting along the axis of a concrete section due to external loading or prestressing. It is considered positive when it induces compression in the section, and the effects of imposed deformations such as shrinkage or temperature changes can be ignored in its calculation.",
        "latexSymbol": "N_{Ed}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "default": 1850.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G27_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(Figure6.3)"
        ],
        "title": "Diameter of longitudinal tensile reinforcement",
        "description": "The diameter of longitudinal tensile reinforcement refers to the thickness of individual reinforcement bars used in the tensile zone of a concrete section. This dimension directly influences the cross-sectional area of the reinforcement, affecting the structural capacity to resist tensile and shear forces.",
        "latexSymbol": "\\phi_{sl}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "default": 32.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G27_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(Figure6.3)"
        ],
        "title": "Number of longitudinal tensile reinforcement",
        "description": "The number of longitudinal tensile reinforcement bars refers to the total count of reinforcement bars placed in the tensile zone of a concrete section.",
        "latexSymbol": "n_{sl}",
        "type": "number",
        "unit": "ea",
        "notation": "standard",
        "decimal": 0,
        "default": 6.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G27_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(1)"
        ],
        "title": "Smallest cross-sectional width in tensile area",
        "description": "The smallest cross-sectional width in the tensile area refers to the narrowest part of a concrete section where tensile stresses occur. This dimension is crucial in shear resistance calculations, as it directly impacts the section's ability to handle shear forces.",
        "latexSymbol": "b_{w}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 600.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G27_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(Figure6.3)"
        ],
        "title": "Effective depth of cross section",
        "description": "The effective depth of cross section is the distance from the extreme compression fiber to the centroid of the tensile reinforcement. It is a key parameter in determining the shear and flexural resistance of a concrete section.",
        "latexSymbol": "d",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 429.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G27_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(1)"
        ],
        "title": "Area of the concrete cross-section",
        "description": "The area of the concrete cross-section refers to the total cross-sectional area of the concrete, including both the compression and tension zones. It is a fundamental parameter used in structural calculations to determine stresses, axial forces, and shear resistance.",
        "latexSymbol": "A_{C}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 3,
        "default": 300000.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G27_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(Figure6.4)"
        ],
        "title": "Distance from the load application point to the support",
        "description": "The distance from the load application point to the support is the horizontal distance measured from the centerline of the support to the point where the load is applied. This distance is critical in determining the shear force and the effective contribution of the load to the section's shear resistance.",
        "latexSymbol": "a_{v}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 200.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G27_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.1(3)"
        ],
        "title": "Shear safety ratio verification without shear reinforcement",
        "description": "The shear safety ratio is calculated by dividing the applied shear force by the design shear resistance of the section. This ratio evaluates whether the section is safe without shear reinforcement. It must be less than or equal to one; if it exceeds one, shear reinforcement must be considered to ensure safety.",
        "latexSymbol": "shearsafety",
        "latexEquation": "\\frac{\\sym{V_{Ed}}}{\\max(\\sym{V_{Rd,c}}, \\sym{V_{Rd,c,min}})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_1",
            "G27_COMP_2",
            "G27_COMP_11",
            "G27_COMP_12",
            "G27_COMP_21"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{secwobar} = Reinforced concrete section",
                    "\\sym{secwobar} = Cracked prestressed section",
                    "\\sym{secwobar} = Support region"
                ]
            ],
            "data": [
                [
                    "\\frac{\\sym{V_{Ed}}}{\\max(\\sym{V_{Rd,c}} , \\sym{V_{Rd,c,min}})}"
                ],
                [
                    "\\frac{\\sym{V_{Ed}}}{\\max(\\sym{V_{Rd,c}} , \\sym{V_{Rd,c,min}})}"
                ],
                [
                    "\\frac{\\sym{V_{Ed,\\beta}}}{\\max(V_{Rd,c} , \\sym{V_{Rd,c,min}})}"
                ]
            ]
        }
    },
    {
        "id": "G27_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(6.2.a)"
        ],
        "title": "Design shear resistance without shear reinforcement",
        "description": "This refers to the shear resistance capacity of a concrete member without shear reinforcement, considering the contributions of concrete strength, longitudinal reinforcement, and section geometry under ultimate limit state conditions.",
        "latexSymbol": "V_{Rd,c}",
        "latexEquation": "(\\sym{C_{Rd,c}} \\times \\sym{k} \\times (100 \\times \\sym{\\rho_{l}} \\times \\sym{f_{ck}})^{1/3} + \\sym{k_{1}} \\times \\sym{\\sigma_{cp}}) \\times \\sym{b_{w}} \\times \\sym{d} \\times 10^{-3}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_17",
            "G27_COMP_13",
            "G27_COMP_14",
            "G14_COMP_5",
            "G27_COMP_18",
            "G27_COMP_16",
            "G27_COMP_6",
            "G27_COMP_7"
        ]
    },
    {
        "id": "G27_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(6.2.b)"
        ],
        "title": "Minimum design shear resistance",
        "description": "Minimum design shear resistance refers to the basic shear capacity of a concrete section without shear reinforcement. It ensures structural safety by accounting for concrete strength, axial stress, and section dimensions, providing a baseline for design checks even when reinforcement is not required.",
        "latexSymbol": "V_{Rd,c,min}",
        "latexEquation": "(\\sym{v_{min}} + \\sym{k_{1}} \\times \\sym{\\sigma_{cp}}) \\times \\sym{b_{w}} \\times \\sym{d} \\times 10^{-3}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_19",
            "G27_COMP_18",
            "G27_COMP_16",
            "G27_COMP_6",
            "G27_COMP_7"
        ]
    },
    {
        "id": "G27_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(1)"
        ],
        "title": "Depth factor",
        "description": "The depth factor is a coefficient used to account for the influence of the effective depth of a concrete section on its shear resistance. It adjusts the shear strength calculation to reflect the effect of section size, with a maximum value set to ensure design safety.",
        "latexSymbol": "k",
        "latexEquation": "\\min(1+ \\sqrt{(\\frac{200}{\\sym{d}})} , 2.0)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_7"
        ]
    },
    {
        "id": "G27_COMP_14",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(1)"
        ],
        "title": "Longitudinal reinforcement ratio",
        "description": "The longitudinal reinforcement ratio represents the proportion of tensile reinforcement in a concrete section relative to the cross-sectional area. It influences the shear resistance by contributing to crack control and dowel action, enhancing the section's ability to transfer shear forces.",
        "latexSymbol": "\\rho_{l}",
        "latexEquation": "\\min(\\frac{\\sym{A_{sl}}}{\\sym{b_{w}} \\times \\sym{d}} , 0.02)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_15",
            "G27_COMP_6",
            "G27_COMP_7"
        ]
    },
    {
        "id": "G27_COMP_15",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(Figure6.3)"
        ],
        "title": "Area of longitudinal tensile reinforcement",
        "description": "The area of longitudinal tensile reinforcement refers to the total cross-sectional area of the reinforcement bars placed in the tensile zone of a concrete section. It is a key parameter in determining the structural capacity for resisting tensile forces and contributes to the overall shear resistance by enhancing crack control and dowel action.",
        "latexSymbol": "A_{sl}",
        "latexEquation": "\\frac{(\\pi \\times \\sym{\\phi_{sl}}^{2})}{4} \\times \\sym{n_{sl}}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_4",
            "G27_COMP_5"
        ]
    },
    {
        "id": "G27_COMP_16",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(1)"
        ],
        "title": "Concrete compressive stress at the centroidal axis",
        "description": "Concrete compressive stress at the centroidal axis refers to the stress induced in the concrete section by axial loading and/or prestressing. It is calculated as the ratio of the axial force to the cross-sectional area of the concrete and is positive when the force causes compression.",
        "latexSymbol": "\\sigma_{cp}",
        "latexEquation": "\\min(\\frac{\\sym{N_{Ed}} \\times 10^{3}}{\\sym{A_{C}}} , 0.2 \\times \\sym{f_{cd}})",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_3",
            "G27_COMP_8",
            "G14_COMP_15"
        ]
    },
    {
        "id": "G27_COMP_17",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(1)"
        ],
        "title": "Concrete shear resistance coefficient",
        "description": "The concrete shear resistance coefficient is a factor used in calculating the design shear resistance of a concrete section without shear reinforcement. It is determined by national standards or design codes and accounts for material properties, safety factors, and testing data.",
        "latexSymbol": "C_{Rd,c}",
        "latexEquation": "\\frac{0.18}{\\sym{\\gamma_{c}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_12"
        ]
    },
    {
        "id": "G27_COMP_18",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(1)"
        ],
        "title": "Axial stress influence coefficient",
        "description": "The axial stress influence coefficient is a factor used in calculating the contribution of axial compressive stress to the shear resistance of a concrete section. It is specified in design codes and adjusts the shear resistance based on the magnitude of axial force.",
        "latexSymbol": "k_{1}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "default": 0.15,
        "const": True
    },
    {
        "id": "G27_COMP_19",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(6.3N)"
        ],
        "title": "Minimum shear stress",
        "description": "The minimum shear stress represents the lower bound for the shear resistance of a concrete section without shear reinforcement. It is calculated based on the material properties of the concrete and is provided to ensure safety even in sections with minimal structural contributions to shear resistance.",
        "latexSymbol": "v_{min}",
        "latexEquation": "0.035 \\times \\sym{k}^{3/2} \\times \\sym{f_{ck}}^{1/2}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_13",
            "G14_COMP_5"
        ]
    },
    {
        "id": "G27_COMP_20",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(6)"
        ],
        "title": "Shear force reduction factor",
        "description": "The shear force reduction factor is applied to account for the diminished contribution of a load to the total shear force when the load is located near the support. It adjusts the effective shear force in specific conditions and is determined based on the distance from the load application point to the support.",
        "latexSymbol": "\\beta",
        "latexEquation": "\\frac{\\sym{a_{v}}}{2 \\times \\sym{d}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_9",
            "G27_COMP_7"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    " 0.5 \\times \\sym{d} <= \\sym{a_{v}} <= 2 \\times \\sym{d}",
                    " \\sym{a_{v}} < 0.5 \\times \\sym{d}"
                ]
            ],
            "data": [
                [
                    "\\frac{\\sym{a_{v}}}{2 \\times \\sym{d}}"
                ],
                [
                    "\\frac{0.5 \\times \\sym{d}}{2 \\times \\sym{d}}"
                ]
            ]
        }
    },
    {
        "id": "G27_COMP_21",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(6)"
        ],
        "title": "Reduced design shear force near supports",
        "description": "The reduced design shear force near supports is the adjusted value of the applied shear force, calculated by multiplying the design shear force by a reduction factor. This is applied in support regions where loads are located close to the support, ensuring more realistic and efficient shear force calculations.",
        "latexSymbol": "V_{Ed,\\beta}",
        "latexEquation": "\\sym{V_{Ed}} \\times \\sym{\\beta}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_2",
            "G27_COMP_20"
        ]
    },
    {
        "id": "G27_COMP_22",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(6.5)"
        ],
        "title": "Maximum design shear force",
        "description": "The maximum design shear force represents the upper limit of shear force that a concrete section can resist before failure occurs, typically due to crushing of the compression struts. It is calculated based on the section's geometry, material properties, and strength reduction factors, ensuring the structure remains within safe design limits.",
        "latexSymbol": "V_{Ed,max}",
        "latexEquation": "0.5 \\times \\sym{b_{w}} \\times \\sym{d} \\times \\sym{\\nu} \\times \\sym{f_{cd}} \\times 10^{-3}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_6",
            "G27_COMP_7",
            "G27_COMP_23",
            "G14_COMP_15"
        ]
    },
    {
        "id": "G27_COMP_23",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(6.6N)"
        ],
        "title": "Shear strength reduction factor",
        "description": "The shear strength reduction factor accounts for the decrease in concrete’s shear capacity due to cracking. It is an empirically determined coefficient that adjusts the maximum allowable shear stress in a concrete section, ensuring conservative and safe design under shear forces.",
        "latexSymbol": "\\nu",
        "latexEquation": "0.6 \\times (1 - \\frac{\\sym{f_{ck}}}{250})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_5"
        ]
    },
    {
        "id": "G27_COMP_24",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.2(6)"
        ],
        "title": "Verification of applied shear force against maximum limit",
        "description": "This verification checks whether the applied shear force is within the maximum allowable design shear force. It ensures that the section remains safe under the given loading conditions, especially in support regions.",
        "latexSymbol": "maxlimit",
        "type": "number",
        "unit": "",
        "notation": "text",
        "required": [
            "G27_COMP_1",
            "G27_COMP_2",
            "G27_COMP_22"
        ],
        "table": "text",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{secwobar} = Reinforced concrete section",
                    "\\sym{secwobar} = Cracked prestressed section",
                    "\\sym{secwobar} = Support region"
                ],
                [
                    "\\sym{V_{Ed}} <= \\sym{V_{Ed,max}}",
                    "\\sym{V_{Ed}} > \\sym{V_{Ed,max}}"
                ]
            ],
            "data": [
                [
                    "Irrelevant",
                    "Irrelevant"
                ],
                [
                    "Irrelevant",
                    "Irrelevant"
                ],
                [
                    "Shear force is within the maximum limit",
                    "Shear force exceeds the maximum limit"
                ]
            ]
        }
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/136184172/EN1992-1-1+Shear+without+reinforcement
        'id': '27',
        'standardType': 'EUROCODE',
        'codeName': 'EN1992-1-1',
        'codeTitle': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Shear Verification Without Design Shear Reinforcement',
        'description': r"[EN1992-1-1] This guide focuses on shear verification for members without design shear reinforcement, following the principles of Eurocode. It provides a comprehensive approach to evaluate shear safety for three section types: reinforced concrete sections, cracked prestressed sections, and support regions, all without shear reinforcement. The verification process considers both the calculated shear resistance and the minimum required shear resistance to ensure safety and compliance with design standards. If the calculated shear safety ratio exceeds the allowable limit, additional design checks for shear reinforcement will be required. This guide aims to help designers ensure that the structural capacity of members relying solely on the concrete section and longitudinal reinforcement is adequately verified.",
        'edition': '2004',
        'targetComponents': ['G27_COMP_10', 'G27_COMP_11', 'G27_COMP_12', 'G27_COMP_24'],
        'testInput': [
            {'component': 'G14_COMP_3', 'value': 'Persistent'}, # designsitu = Persistent
            {'component': 'G14_COMP_4', 'value': 'C12/15'}, # C = C12/15
            {'component': 'G27_COMP_1', 'value': 'Reinforced concrete section'}, # secwobar = Reinforced concrete section
            # {'component': 'G27_COMP_1', 'value': 'Cracked prestressed section'}, # secwobar = Cracked prestressed section
            # {'component': 'G27_COMP_1', 'value': 'Support region'}, # secwobar = Support region
            {'component': 'G27_COMP_2', 'value': 350},
            {'component': 'G27_COMP_3', 'value': 1850},
            {'component': 'G27_COMP_4', 'value': 32},
            {'component': 'G27_COMP_5', 'value': 6},
            {'component': 'G27_COMP_6', 'value': 600},
            {'component': 'G27_COMP_7', 'value': 429},
            {'component': 'G27_COMP_8', 'value': 300000},
            {'component': 'G27_COMP_9', 'value': 200},
        ],
    },
]