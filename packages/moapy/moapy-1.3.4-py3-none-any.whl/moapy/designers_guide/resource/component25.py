component_list = [
    {
        "id": "G25_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.7.3(8.10)"
        ],
        "title": "Design lap length",
        "description": "Design lap length is the minimum length required to ensure that the force can be safely transferred between overlapping reinforcement bars. This length is determined by adjusting the basic lap length using various coefficients that account for factors like bar shape, concrete cover, confinement, and the distribution of lapped reinforcement.",
        "latexSymbol": "l_{0}",
        "latexEquation": "\\max(\\sym{\\alpha_{1}} \\times \\sym{\\alpha_{2}} \\times \\sym{\\alpha_{3,lap}} \\times \\sym{\\alpha_{5}} \\times \\sym{\\alpha_{6}} \\times \\sym{l_{b,rqd}} ,\\sym{l_{0,min}})",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_2",
            "G24_COMP_12",
            "G24_COMP_18",
            "G24_COMP_20",
            "G25_COMP_3",
            "G24_COMP_24",
            "G25_COMP_6",
            "G24_COMP_1",
            "G25_COMP_2",
            "G24_COMP_19"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{c_{d}} <= 3 \\times \\sym{\\phi}",
                    "\\sym{c_{d}} > 3 \\times \\sym{\\phi}"
                ]
            ],
            "data": [
                [
                    "\\max(\\sym{\\alpha_{1}} \\times \\sym{\\alpha_{2}} \\times \\sym{\\alpha_{3,lap}} \\times \\sym{\\alpha_{5}} \\times \\sym{\\alpha_{6}} \\times \\sym{l_{b,rqd}},\\sym{l_{0,min}})"
                ],
                [
                    "\\max(\\sym{\\alpha_{1,3\\sym{\\phi}}} \\times \\sym{\\alpha_{2}} \\times \\sym{\\alpha_{3,lap}} \\times \\sym{\\alpha_{5}} \\times \\sym{\\alpha_{6}} \\times \\sym{l_{b,rqd}},\\sym{l_{0,min}})"
                ]
            ]
        }
    },
    {
        "id": "G25_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.7.3(8.11)"
        ],
        "title": "Minimum lap length",
        "description": "The minimum lap length is the smallest allowable length for overlapping reinforcement bars to ensure proper force transfer and structural integrity. It serves as a lower bound and is determined based on specific criteria, including bar diameter and concrete properties, to prevent premature failure or inadequate bonding.",
        "latexSymbol": "l_{0,min}",
        "latexEquation": "\\max(0.3 \\times \\sym{\\alpha_{6}} \\times \\sym{l_{b,rqd}}, 15 \\times \\sym{\\phi}, 200)",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G25_COMP_6",
            "G24_COMP_1",
            "G24_COMP_2"
        ]
    },
    {
        "id": "G25_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Lap length confinement coefficient",
        "description": "The lap length confinement coefficient represents the effect of transverse reinforcement, such as ties or stirrups, on the required lap length. It reflects how the confinement provided by transverse reinforcement enhances bond strength in the lapped area, which can lead to a reduction in the required lap length",
        "latexSymbol": "\\alpha_{3,lap}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_27",
            "G24_COMP_11",
            "G24_COMP_8",
            "G25_COMP_7"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{barconfig} = Straight bars",
                    "\\sym{barconfig} = Bent or hooked bars",
                    "\\sym{barconfig} = Looped bars"
                ],
                [
                    "\\sym{anchcond} = For anchorages in tension",
                    "\\sym{anchcond} = For anchorages in compression"
                ]
            ],
            "data": [
                [
                    "\\min(\\max(1 - \\sym{K} \\times \\sym{\\lambda_{lap}}, 0.7),1.0)",
                    "1.0"
                ],
                [
                    "\\min(\\max(1 - \\sym{K} \\times \\sym{\\lambda_{lap}}, 0.7),1.0)",
                    "1.0"
                ],
                [
                    "\\min(\\max(1 - \\sym{K} \\times \\sym{\\lambda_{lap}}, 0.7),1.0)",
                    "1.0"
                ]
            ]
        }
    },
    {
        "id": "G25_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.7.3(1)"
        ],
        "title": "Minimum transverse reinforcement area for lap length",
        "description": "The minimum transverse reinforcement area for lap length, Ast,min,lap, is the smallest amount of transverse reinforcement, such as ties or stirrups, required to provide adequate confinement and ensure proper force transfer in the lapped area. This value helps to maintain the structural integrity of the lap splice by enhancing bond strength.",
        "latexSymbol": "A_{st,min}",
        "latexEquation": "1.0 \\times \\sym{A_{s}} \\times (\\frac{\\sym{\\sigma_{sd}}}{\\sym{f_{yd}}})",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_32",
            "G24_COMP_3",
            "G18_COMP_3"
        ]
    },
    {
        "id": "G25_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.7.3(Figure8.8)"
        ],
        "title": "Reinforcement lap ratio",
        "description": "The reinforcement lap ratio is the percentage of reinforcement bars that are lapped within 65% of the lap length, measured from the center of the lap length. This ratio helps determine how the distribution of overlapping bars influences the necessary lap length.",
        "figureFile": "detail_g25_comp_6.png",
        "latexSymbol": "\\rho_{1}",
        "type": "number",
        "unit": "%",
        "notation": "standard",
        "decimal": 1,
        "default": 50.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G25_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.7.3(Table8.3)"
        ],
        "title": "Reinforcement lap percentage coefficient",
        "description": "The reinforcement lap percentage coefficient considers the proportion of reinforcement bars that are overlapped within a specific distance from the center of the lap length. This coefficient adjusts the lap length to ensure that the design properly accounts for the distribution and density of the lapped reinforcement.",
        "latexSymbol": "\\alpha_{6}",
        "latexEquation": "\\min(\\max((\\frac{\\sym{\\rho_{1}}}{25})^{0.5}, 1.0), 1.5)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G25_COMP_5"
        ]
    },
    {
        "id": "G25_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Transverse reinforcement ratio",
        "description": "The transverse reinforcement ratio describes the relative amount of transverse reinforcement provided along the design anchorage length. It is determined by calculating the difference between the total cross-sectional area of the transverse reinforcement and the minimum required transverse reinforcement, divided by the area of the anchored bar.",
        "latexSymbol": "\\lambda_{lap}",
        "latexEquation": "\\frac{(\\sym{A_{st}} - \\sym{A_{st,min}})}{\\sym{A_{s}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_31",
            "G25_COMP_4",
            "G24_COMP_32"
        ]
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/123633976/EN1992-1-1+Lap+length
        'id': '25',
        'standardType': 'EUROCODE',
        'codeName': 'EN1992-1-1',
        'codeTitle': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Design Lap Length Calculation for Reinforcement Bars',
        'description': r"[EN1992-1-1] This guide provides detailed instructions for calculating the design lap length to ensure that the force is properly transferred between overlapping reinforcement bars. It covers the use of adjustment coefficients for factors such as bar shape, concrete cover, confinement, and the distribution of lapped bars. By following this guide, users will be able to determine the appropriate lap length to maintain structural safety and integrity.",
        'edition': '2004',
        'targetComponents': ['G25_COMP_1', 'G25_COMP_2'],
        'testInput': [
            {'component': 'G14_COMP_3', 'value': 'Persistent'}, # designsitu = Persistent
            {'component': 'G14_COMP_4', 'value': 'C12/15'}, # C = C12/15
            {'component': 'G18_COMP_1', 'value': 500},
            {'component': 'G24_COMP_2', 'value': 20},
            {'component': 'G24_COMP_5', 'value': 'Good'}, # bondcon = Good
            {'component': 'G24_COMP_8', 'value': 'For anchorages in tension'}, # anchcond = For anchorages in tension
            {'component': 'G24_COMP_11', 'value': 'Straight bars'}, # barconfig = Straight bars
            {'component': 'G24_COMP_13', 'value': 125},
            {'component': 'G24_COMP_16', 'value': 55},
            {'component': 'G24_COMP_17', 'value': 12},
            {'component': 'G24_COMP_25', 'value': 0},
            {'component': 'G24_COMP_26', 'value': 'Bent Anchorage'}, # conplace = Bent Anchorage
            {'component': 'G24_COMP_33', 'value': 3},
            {'component': 'G25_COMP_5', 'value': 50},
        ],
    },
]