component_list = [
    {
        "id": "G21_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3(5.13N)"
        ],
        "title": "Critical slenderness limit for neglecting second-order effects",
        "description": "The critical slenderness limit is a threshold value used to determine whether second-order effects need to be considered in structural analysis. If the slenderness of a member is below this limit, second-order effects can be neglected, simplifying the design process. This limit is influenced by factors such as member shape, boundary conditions, and loading conditions.",
        "latexSymbol": "\\lambda_{lim}",
        "latexEquation": "\\frac{20 \\times \\sym{A} \\times \\sym{B} \\times \\sym{C}}{\\sqrt{\\sym{n}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G21_COMP_4",
            "G21_COMP_7",
            "G21_COMP_9",
            "G21_COMP_2"
        ]
    },
    {
        "id": "G21_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Relative normal force",
        "description": "The relative axial force is the ratio of the applied axial load to the compressive strength of the concrete section. It represents the proportion of the axial load compared to the load-bearing capacity of the concrete section. A higher value indicates a larger axial load relative to the concrete strength, while a lower value suggests a smaller axial load.",
        "latexSymbol": "n",
        "latexEquation": "\\frac{\\sym{N_{Ed}}\\times 1000}{\\sym{A_{c}} \\times \\sym{f_{cd}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G21_COMP_3",
            "G16_COMP_11",
            "G14_COMP_15"
        ]
    },
    {
        "id": "G21_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.3(1)"
        ],
        "title": "Design value of the applied axial force",
        "description": "The design axial load represents the design value of the axial force acting along the axis of a structural member. It accounts for all relevant loads, such as dead and live loads, and is used to ensure the member can safely resist compression or tension forces.",
        "latexSymbol": "N_{Ed}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "default": 1500.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G21_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Creep coefficient for second-order effects",
        "description": "The coefficient A accounts for the influence of creep on second-order effects in structural members, particularly in concrete. Creep refers to the long-term deformation of a material under sustained load, and this coefficient adjusts the calculation of second-order effects accordingly.",
        "latexSymbol": "A",
        "latexEquation": "\\frac{1}{1+0.2 \\times \\sym{\\phi_{ef}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G21_COMP_6"
        ]
    },
    {
        "id": "G21_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Input method for critical slenderness limit coefficients",
        "description": "This option allows you to choose how to input the A, B, and C coefficients needed to calculate the critical slenderness limit. You can either calculate the coefficients using formulas or use suggested values if certain required ratios are unknown.",
        "latexSymbol": "crislenmet",
        "type": "string",
        "unit": "",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label"
                ],
                [
                    "Calculate using the formula"
                ],
                [
                    "If the required ratio is unknown"
                ]
            ]
        }
    },
    {
        "id": "G21_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Effective creep ratio",
        "description": "The effective creep ratio is a simplified value that adjusts the final creep coefficient based on the ratio of the quasi-permanent to design load moments. It is used to estimate long-term creep deformation in structural members under realistic service conditions.",
        "latexSymbol": "\\phi_{ef}",
        "latexEquation": "\\frac{0.3}{0.14}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "const": True
    },
    {
        "id": "G21_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Mechanical reinforcement ratio coefficient",
        "description": "The mechanical reinforcement ratio coefficient reflects the impact of reinforcement on second-order effects in structural members. It ensures that the presence and effectiveness of reinforcement are considered when evaluating buckling and other stability-related phenomena, helping to adjust the analysis based on how reinforcement contributes to the overall stability of the member.",
        "latexSymbol": "B",
        "latexEquation": "\\sqrt{1+ 2\\times \\sym{\\omega}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G21_COMP_8"
        ]
    },
    {
        "id": "G21_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Mechanical reinforcement ratio for critical slenderness limit",
        "description": "The mechanical reinforcement ratio reflects the contribution of reinforcement to the concrete's capacity. It influences the member's stiffness and resistance to buckling. For simplified calculations, a value of 0.105 is applied.",
        "latexSymbol": "\\omega",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "default": 0.105,
        "const": True
    },
    {
        "id": "G21_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Moment distribution ratio for second-order effects",
        "description": "The moment distribution ratio reflects how the variation in first-order moments at the ends of a structural member influences second-order effects. This ratio considers the difference between the smaller and larger first-order end moments, ensuring that the moment distribution along the member’s length is properly accounted for when assessing stability and the impact of second-order effects.",
        "latexSymbol": "C",
        "latexEquation": "1.7 - \\sym{r_{m}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G21_COMP_10"
        ]
    },
    {
        "id": "G21_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "First-order moment ratio between member ends",
        "description": "The moment ratio represents the relationship between the first-order moments at the two ends of a structural member. It is calculated by dividing the smaller moment by the larger one. If both moments act in the same direction (i.e., have the same sign), the moment ratio is considered positive. Conversely, if the moments act in opposite directions (i.e., have opposite signs), the moment ratio is considered negative.",
        "latexSymbol": "r_{m}",
        "latexEquation": "\\frac{\\sym{M_{01}}}{\\sym{M_{02}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G21_COMP_5",
            "G21_COMP_13",
            "G21_COMP_14"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{crislenmet} = Calculate using the formula",
                    "\\sym{crislenmet} = If the required ratio is unknown"
                ]
            ],
            "data": [
                [
                    "\\frac{\\sym{M_{01}}}{\\sym{M_{02}}}"
                ],
                [
                    "1"
                ]
            ]
        }
    },
    {
        "id": "G21_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Moment acting at bottom",
        "description": "This represents the first-order moment acting at the bottom end of the structural member. The user is expected to input the value of the moment applied to the bottom of the member, which will be used to determine the smaller and larger moments in subsequent calculations.",
        "latexSymbol": "M_{bo}",
        "type": "number",
        "unit": "kN.m",
        "notation": "standard",
        "decimal": 3,
        "default": 100.0,
        "useStd": False
    },
    {
        "id": "G21_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Moment acting at top",
        "description": "This represents the first-order moment acting at the top end of the structural member. The user is expected to input the value of the moment applied to the top of the member, which will be used to determine the smaller and larger moments in subsequent calculations.",
        "latexSymbol": "M_{to}",
        "type": "number",
        "unit": "kN.m",
        "notation": "standard",
        "decimal": 3,
        "default": -100.0,
        "useStd": False
    },
    {
        "id": "G21_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Smaller first-order end moment",
        "description": "The smaller first-order end moment refers to the lesser of the two moments acting at the ends of a structural member, based purely on magnitude. The position where the moments act does not matter, only their size.",
        "latexSymbol": "M_{01}",
        "latexEquation": "\\sym{M_{bo}}",
        "type": "number",
        "unit": "kN.m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G21_COMP_11",
            "G21_COMP_12"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\Abs{\\sym{M_{bo}}} < \\Abs{\\sym{M_{to}}}",
                    "\\Abs{\\sym{M_{bo}}} >= \\Abs{\\sym{M_{to}}}"
                ]
            ],
            "data": [
                [
                    "\\sym{M_{bo}}"
                ],
                [
                    "\\sym{M_{to}}"
                ]
            ]
        }
    },
    {
        "id": "G21_COMP_14",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(1)"
        ],
        "title": "Larger first-order end moment",
        "description": "The larger first-order end moment refers to the greater of the two moments acting at the ends of a structural member, determined solely by magnitude. The location where the moments act is irrelevant, and only their size is considered.",
        "latexSymbol": "M_{02}",
        "latexEquation": "\\sym{M_{to}}",
        "type": "number",
        "unit": "kN.m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G21_COMP_11",
            "G21_COMP_12"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\Abs{\\sym{M_{to}}} > \\Abs{\\sym{M_{bo}}}",
                    "\\Abs{\\sym{M_{to}}} <= \\Abs{\\sym{M_{bo}}}"
                ]
            ],
            "data": [
                [
                    "\\sym{M_{to}}"
                ],
                [
                    "\\sym{M_{bo}}"
                ]
            ]
        }
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/107119119/EN1992-1-1+Critical+Slenderness+Limit
        'id': '21',
        'standardType': 'EUROCODE',
        'codeName': 'EN1992-1-1',
        'codeTitle': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Critical Slenderness Limit Calculation for Neglecting Second-Order Effects',
        'description': r"[EN1992-1-1] This guide explains how to calculate the critical slenderness limit, which determines whether second-order effects can be neglected in the structural analysis of a member. If the slenderness of a member is below this critical limit, second-order effects, such as buckling and geometric non-linearity, can be ignored, simplifying the design process. The calculation is based on an empirical formula provided in Eurocode, which accounts for factors like member shape, boundary conditions, and axial force. In this guide, default values are used for the mechanical reinforcement ratio or the effective creep ratio when these ratios are unknown, simplifying the calculation process.",
        'edition': '2004',
        'targetComponents': ['G21_COMP_1'],
        'testInput': [
            {'component': 'G14_COMP_3', 'value': 'Persistent'}, # designsitu = Persistent
            {'component': 'G14_COMP_4', 'value': 'C12/15'}, # C = C12/15
            # {'component': 'G14_COMP_4', 'value': 'C40/50'}, # C = C40/50
            {'component': 'G16_COMP_11', 'value': 534694.0}, # A_{c} = 534694.0
            {'component': 'G21_COMP_3', 'value': 1500},
            {'component': 'G21_COMP_5', 'value': 'Calculate using the formula'}, # crislenmet = Calculate using the formula
            # {'component': 'G21_COMP_5', 'value': 'If the required ratio is unknown'}, # crislenmet = If the required ratio is unknown
            {'component': 'G21_COMP_11', 'value': '100'},
            {'component': 'G21_COMP_12', 'value': '-98'},
        ],
    },
]