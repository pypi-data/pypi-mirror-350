component_list = [
    {
        "id": "G28_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(1)"
        ],
        "title": "Inclination angle of shear reinforcement",
        "description": "The angle of shear reinforcement refers to the inclination of the shear reinforcement relative to the beam axis perpendicular to the shear force. It is used in the design of shear resistance, with vertical reinforcement having an angle of 90 degrees, while inclined reinforcement may have a smaller angle to enhance shear resistance efficiency.",
        "latexSymbol": "\\alpha_{D}",
        "type": "number",
        "unit": "degree",
        "notation": "standard",
        "decimal": 3,
        "default": 90.0,
        "limits": {
            "inMin": 45,
            "inMax": 90
        },
        "useStd": False
    },
    {
        "id": "G28_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(1)"
        ],
        "title": "Inclination angle of shear reinforcement in radians",
        "description": "The inclination angle of shear reinforcement in radians is the angle converted from the user's input in degrees.",
        "latexSymbol": "\\alpha",
        "latexEquation": "\\sym{\\alpha_{D}} \\times \\frac{\\pi}{180}",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G28_COMP_1"
        ]
    },
    {
        "id": "G28_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(6.7N)"
        ],
        "title": "Angle of the concrete compression strut",
        "description": "The angle of the concrete compression strut represents the inclination of the internal compressive forces in the concrete relative to the beam axis perpendicular to the shear force. It is a critical parameter in the truss model for shear design and typically ranges between 21.8degrees (cot theta equals two point five) and 45degrees (cot theta equals one) as specified in design codes.",
        "latexSymbol": "\\theta_{D}",
        "type": "number",
        "unit": "degree",
        "notation": "standard",
        "decimal": 3,
        "default": 45.0,
        "limits": {
            "inMin": 21.8,
            "inMax": 45
        },
        "useStd": False
    },
    {
        "id": "G28_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(6.7N)"
        ],
        "title": "Angle of concrete compression strut in radians",
        "description": "The angle of the concrete compression strut in radians is the angle converted from the user's input in degrees.",
        "latexSymbol": "\\theta",
        "latexEquation": "\\sym{\\theta_{D}} \\times \\frac{\\pi}{180}",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G28_COMP_3"
        ]
    },
    {
        "id": "G28_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(1)"
        ],
        "title": "Lever arm for internal forces",
        "description": "The lever arm for internal forces refers to the effective distance between the lines of action of the tensile and compressive forces within a structural member. It is used in design calculations to determine the moment capacity and shear resistance of a section. For members of constant depth, it is typically approximated as 90% of the effective depth.",
        "latexSymbol": "z",
        "latexEquation": "0.9 \\times \\sym{d}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_7"
        ]
    },
    {
        "id": "G28_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(6.8)(6.13)"
        ],
        "title": "Required shear reinforcement area divided by spacing",
        "description": "The required shear reinforcement area divided by spacing represents the cross-sectional area of shear reinforcement needed per unit spacing of stirrups. For vertical reinforcement, it is calculated using a formula that includes the cotangent of the strut angle. For inclined reinforcement, the calculation incorporates the sine and cotangent of the inclination angle to account for the additional efficiency of inclined reinforcement.",
        "latexSymbol": "A_{sw}/s",
        "latexEquation": "\\frac{(\\sym{V_{Ed}} \\times 10^{3})}{(\\sym{z} \\times \\sym{f_{ywd}} \\times \\cot{\\sym{\\theta}})}",
        "type": "number",
        "unit": "mm^2/mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_2",
            "G28_COMP_1",
            "G28_COMP_5",
            "G28_COMP_10",
            "G28_COMP_4",
            "G28_COMP_2"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{\\alpha_{D}} = 90",
                    "\\sym{\\alpha_{D}} < 90"
                ]
            ],
            "data": [
                [
                    "\\frac{(\\sym{V_{Ed}} \\times 10^{3})}{(\\sym{z} \\times \\sym{f_{ywd}} \\times \\cot{\\sym{\\theta}})}"
                ],
                [
                    "\\frac{(\\sym{V_{Ed}} \\times 10^{3})}{(\\sym{z} \\times \\sym{f_{ywd}} \\times (\\cot{\\sym{\\theta}} + \\cot{\\sym{\\alpha}}) \\times \\sin{\\sym{\\alpha}})}"
                ]
            ]
        }
    },
    {
        "id": "G28_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(3)"
        ],
        "title": "Required area of shear reinforcement",
        "description": "The required area of shear reinforcement refers to the calculated cross-sectional area of shear reinforcement necessary to resist the design shear force in a structural member. It is determined using the shear resistance formula for vertical or inclined shear reinforcement and ensures that the provided reinforcement meets the structural safety requirements.",
        "latexSymbol": "A_{sw,req}",
        "latexEquation": "\\sym{A_{sw}/s} \\times \\sym{s}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G28_COMP_6",
            "G28_COMP_8"
        ]
    },
    {
        "id": "G28_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(3)"
        ],
        "title": "Spacing of shear reinforcement",
        "description": "The spacing of shear reinforcement refers to the distance between consecutive stirrups or shear reinforcement elements along the length of a structural member. It is a critical parameter in ensuring uniform distribution of reinforcement to resist shear forces effectively.",
        "latexSymbol": "s",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 200.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G28_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(6.9)(6.14)"
        ],
        "title": "Shear resistance limited by concrete crushing",
        "description": "Shear resistance limited by concrete crushing refers to the maximum shear force a structural member can resist before failure due to crushing of the concrete struts. This limit depends on factors such as the concrete compressive strength, effective width, lever arm, and the angle of the compression strut.",
        "latexSymbol": "V_{Rd,max}",
        "latexEquation": "\\frac{\\sym{\\alpha_{cw}} \\times \\sym{b_{w}} \\times \\sym{z} \\times \\sym{\\nu_{1}} \\times \\sym{f_{cd}}}{(\\cot{\\sym{\\theta}} + \\tan{\\sym{\\theta}})} \\times 10^{-3}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G28_COMP_1",
            "G28_COMP_13",
            "G27_COMP_6",
            "G28_COMP_5",
            "G28_COMP_12",
            "G14_COMP_15",
            "G28_COMP_4",
            "G28_COMP_2"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{\\alpha_{D}} = 90",
                    "\\sym{\\alpha_{D}} < 90"
                ]
            ],
            "data": [
                [
                    "\\frac{\\sym{\\alpha_{cw}} \\times \\sym{b_{w}} \\times \\sym{z} \\times \\sym{\\nu_{1}} \\times \\sym{f_{cd}}}{(\\cot{\\sym{\\theta}} + \\tan{\\sym{\\theta}})} \\times 10^{-3}"
                ],
                [
                    "\\frac{\\sym{\\alpha_{cw}} \\times \\sym{b_{w}} \\times \\sym{z} \\times \\sym{\\nu_{1}} \\times \\sym{f_{cd}} \\times (\\cot{\\sym{\\theta}} + \\cot{\\sym{\\alpha}})}{(1 + (\\cot{\\sym{\\theta}})^2)} \\times 10^{-3}"
                ]
            ]
        }
    },
    {
        "id": "G28_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(3)"
        ],
        "title": "Design yield strength of shear reinforcement",
        "description": "The design yield strength of shear reinforcement refers to the maximum stress that the shear reinforcement can withstand without yielding, adjusted for safety factors. It is calculated based on the characteristic yield strength of the material and partial safety factors specified in the design code.",
        "latexSymbol": "f_{ywd}",
        "latexEquation": "\\frac{\\sym{f_{ywk}}}{\\sym{\\gamma_{s}}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G28_COMP_11",
            "G18_COMP_2"
        ]
    },
    {
        "id": "G28_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(3)"
        ],
        "title": "Characteristic yield strength of shear reinforcement",
        "description": "The characteristic yield strength of shear reinforcement refers to the specified yield strength of the reinforcement material, representing the stress level at which the material begins to deform plastically. It is used as a baseline value in structural design calculations.",
        "latexSymbol": "f_{ywk}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 0,
        "default": 400.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G28_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(3)"
        ],
        "title": "Strength reduction factor for concrete cracked in shear",
        "description": "The strength reduction factor for concrete cracked in shear represents the reduction in shear strength due to the presence of cracks in the concrete. It is determined based on the compressive strength of the concrete and the stress conditions in the compression chord.",
        "latexSymbol": "\\nu_{1}",
        "latexEquation": "\\sym{\\nu}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G27_COMP_23"
        ]
    },
    {
        "id": "G28_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.2.3(3)"
        ],
        "title": "Coefficient accounting for stress in the compression chord",
        "description": "The coefficient accounting for stress in the compression chord represents the influence of axial compressive stress on the shear capacity of a structural member. For non-prestressed structures, this coefficient is equal to 1.",
        "latexSymbol": "\\alpha_{cw}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/137068741/EN1992-1-1+Shear+with+reinforcement
        'id': '28',
        'standardType': 'EUROCODE',
        'codeName': 'EN1992-1-1',
        'codeTitle': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Required Shear Reinforcement Area Calculation',
        'description': r"[EN1992-1-1] This guide explains how to calculate the required shear reinforcement area using the design shear force, lever arm, and yield strength of the reinforcement. It includes the process to calculate the required shear reinforcement area divided by spacing and, based on the user-provided spacing, determine the final required shear reinforcement area. The guide also explains how to apply the appropriate formulas for vertical or inclined shear reinforcement, depending on the inclination angle, ensuring accurate determination of the reinforcement needed for structural design.",
        'edition': '2004',
        'targetComponents': ['G28_COMP_6', 'G28_COMP_7', 'G28_COMP_9'],
        'testInput': [
            {'component': 'G14_COMP_3', 'value': 'Persistent'}, # designsitu = Persistent
            {'component': 'G14_COMP_4', 'value': 'C12/15'}, # C = C12/15
            {'component': 'G27_COMP_2', 'value': 350},
            {'component': 'G27_COMP_6', 'value': 600},
            {'component': 'G27_COMP_7', 'value': 429},
            {'component': 'G28_COMP_1', 'value': 90},
            {'component': 'G28_COMP_3', 'value': 45},
            {'component': 'G28_COMP_8', 'value': 200},
            {'component': 'G28_COMP_11', 'value': 400},
        ],
    },
]