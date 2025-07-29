component_list = [
    {
        "id": "G22_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(5.17)"
        ],
        "title": "Buckling load",
        "description": "The buckling load represents the critical load at which a structural member becomes unstable and buckles. It is used to determine the effective length of members where normal force and/or cross-sectional properties vary. This load is calculated in terms of the member’s bending stiffness, and it is crucial for evaluating a member’s capacity to resist buckling.",
        "latexSymbol": "N_{B}",
        "latexEquation": "\\frac{(\\pi^{2} \\times (\\frac{\\sym{EI}}{10^{9}}))}{\\sym{l_{0}}^{2}}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G22_COMP_2",
            "G6_COMP_3"
        ]
    },
    {
        "id": "G22_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(5.21)"
        ],
        "title": "Nominal stiffness of slender compression members",
        "description": "The nominal stiffness represents the overall stiffness of slender compression members with arbitrary cross sections, considering the contributions of both concrete and steel reinforcements. It accounts for the effects of cracking, material non-linearity, and creep. This stiffness is particularly useful for evaluating the stability, buckling behavior, and deformations of slender compression members or entire structures under axial loads.",
        "latexSymbol": "EI",
        "latexEquation": "\\sym{K_{c}} \\times \\sym{E_{cd}} \\times \\sym{I_{c}} + \\sym{K_{s}} \\times \\sym{E_{s}} \\times \\sym{I_{s}}",
        "type": "number",
        "unit": "N·mm²",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G22_COMP_4",
            "G22_COMP_7",
            "G22_COMP_12",
            "G22_COMP_3",
            "G18_COMP_5",
            "G22_COMP_13"
        ]
    },
    {
        "id": "G22_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(2)",
            "(3)"
        ],
        "title": "Factor for contribution of reinforcement",
        "description": "The factor for the contribution of reinforcement adjusts the stiffness contribution from the steel reinforcement in structural members. In simplified calculations, if the geometric reinforcement ratio is at least 0.002, this factor is typically set to 1, indicating a significant contribution from the reinforcement. However, when the reinforcement ratio is 0.01 or higher, the contribution of reinforcement can be neglected, and the factor is set to 0.",
        "latexSymbol": "K_{s}",
        "latexEquation": "1",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G22_COMP_11"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "0.002 <= \\sym{\\rho} < 0.01",
                    "0.01 <= \\sym{\\rho}"
                ]
            ],
            "data": [
                [
                    "1"
                ],
                [
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G22_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(2)",
            "(3)"
        ],
        "title": "Factor for effects of cracking and creep",
        "description": "The factor for the contribution of reinforcement adjusts the stiffness contribution from the steel reinforcement in structural members. In simplified calculations, if the geometric reinforcement ratio is at least 0.002, this factor is typically set to 1, indicating a significant contribution from the reinforcement. However, when the reinforcement ratio is 0.01 or higher, the contribution of reinforcement can be neglected, and the factor is set to 0.",
        "latexSymbol": "K_{c}",
        "latexEquation": "\\frac{\\sym{k_{1}} \\times k_{2}}{(1 + \\sym{\\phi_{ef}})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G22_COMP_11",
            "G22_COMP_5",
            "G22_COMP_6",
            "G21_COMP_6"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "0.002 <= \\sym{\\rho} < 0.01",
                    "0.01 <= \\sym{\\rho}"
                ]
            ],
            "data": [
                [
                    "\\frac{\\sym{k_{1}} \\times k_{2}}{(1 + \\sym{\\phi_{ef}})}"
                ],
                [
                    "\\frac{0.3}{(1 + 0.5 \\times \\sym{\\phi_{ef}})}"
                ]
            ]
        }
    },
    {
        "id": "G22_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(5.23)"
        ],
        "title": "Factor depending on concrete strength class",
        "description": "This factor depends on the compressive strength class of the concrete. It adjusts the stiffness calculation based on the strength of the concrete, accounting for the effects of cracking and other non-linear behaviors.",
        "latexSymbol": "k_{1}",
        "latexEquation": "\\sqrt{\\frac{\\sym{f_{ck}}}{20}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_5"
        ]
    },
    {
        "id": "G22_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(5.25)"
        ],
        "title": "Factor depending on axial force and slenderness",
        "description": "This factor is influenced by the relative axial force and the slenderness ratio of a structural member. It provides different formulas depending on whether the slenderness ratio is defined or not. In this guide, to simplify the calculation, the formula for cases where the slenderness ratio is not defined will be used.",
        "latexSymbol": "k_{2}",
        "latexEquation": "\\min(\\sym{n} \\times 0.30 , 0.20)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G22_COMP_18"
        ]
    },
    {
        "id": "G22_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.6(5.20)"
        ],
        "title": "Design elasticity modulus for concrete",
        "description": "The design elasticity modulus for concrete is the adjusted value used in structural calculations. It is derived by applying a safety factor to the mean modulus of elasticity, ensuring that the design reflects a more conservative estimate of the material’s stiffness for safety in structural applications.",
        "latexSymbol": "E_{cd}",
        "latexEquation": "\\frac{\\sym{E_{cm}}}{\\sym{\\gamma_{cE}}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G14_COMP_11",
            "G22_COMP_8"
        ]
    },
    {
        "id": "G22_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.6(3)"
        ],
        "title": "Safety factor for elasticity modulus",
        "description": "The safety factor for the elasticity modulus is applied to adjust the mean modulus of elasticity in structural design calculations. The value of this factor can vary depending on national standards, with a typical recommended value of 1.2.",
        "latexSymbol": "\\gamma_{cE}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.2,
        "const": True
    },
    {
        "id": "G22_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(2)"
        ],
        "title": "Concrete area for circular cross-section",
        "description": "The concrete area refers to the total cross-sectional area of concrete in a structural member with a circular cross-section. It is used to calculate stiffness and other structural properties, such as the reinforcement ratio, and is crucial for assessing load-bearing capacity.",
        "latexSymbol": "A_{c}",
        "latexEquation": "\\frac{(\\pi \\times \\sym{D}^{2})}{4}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G6_COMP_9"
        ]
    },
    {
        "id": "G22_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(2)"
        ],
        "title": "Total area of reinforcement",
        "description": "The area of reinforcement refers to the total cross-sectional area of the steel reinforcement in a structural member. This value is used to calculate the geometric reinforcement ratio and directly affects the contribution of the reinforcement to the member's stiffness.",
        "latexSymbol": "A_{s}",
        "latexEquation": "(\\frac{(\\pi \\times \\sym{\\phi}^{2})}{4})\\times \\sym{n_{\\phi}}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G22_COMP_14",
            "G22_COMP_15"
        ]
    },
    {
        "id": "G22_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(2)"
        ],
        "title": "Geometric reinforcement ratio",
        "description": "The geometric reinforcement ratio represents the ratio of the total area of reinforcement to the area of the concrete section. This ratio is a key factor in determining the contribution of reinforcement to the stiffness of structural members. A minimum value of 0.002 is typically required for the reinforcement to have a meaningful effect on the member’s stiffness.",
        "latexSymbol": "\\rho",
        "latexEquation": "\\frac{\\sym{A_{s}}}{\\sym{A_{c}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G22_COMP_10",
            "G22_COMP_9"
        ]
    },
    {
        "id": "G22_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(1)"
        ],
        "title": "Moment of inertia of circular concrete cross section",
        "description": "The moment of inertia of a circular concrete cross section refers to the geometrical property of the section that reflects its ability to resist bending. It is calculated based on the radius of the circular section and is critical in determining the stiffness and bending performance of the structural member.",
        "latexSymbol": "I_{c}",
        "latexEquation": "\\frac{(\\pi \\times \\sym{D}^{4})}{64}",
        "type": "number",
        "unit": "mm^4",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G6_COMP_9"
        ]
    },
    {
        "id": "G22_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(1)"
        ],
        "title": "Second moment of area of reinforcement",
        "description": "The second moment of area of the reinforcement reflects the contribution of the steel reinforcement to the overall stiffness of the structural member. It is calculated by considering the placement of the steel bars in relation to the center of the concrete section and their geometric properties.",
        "latexSymbol": "I_{s}",
        "latexEquation": "(\\frac{(\\pi \\times \\sym{\\phi}^{4})}{64} \\times \\sym{n_{\\phi}}) + \\frac{(\\pi \\times \\phi^{2})}{4} \\times \\sym{y_{i}^{2}}",
        "type": "number",
        "unit": "mm^4",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G6_COMP_9",
            "G22_COMP_16",
            "G22_COMP_14",
            "G22_COMP_15",
            "G22_COMP_17"
        ]
    },
    {
        "id": "G22_COMP_14",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(2)"
        ],
        "title": "Diameter of reinforcement",
        "description": "The diameter of reinforcement refers to the thickness of the steel bars used in reinforced concrete structures.",
        "latexSymbol": "\\phi",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 16,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G22_COMP_15",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(2)"
        ],
        "title": "Number of bars in a circular cross section",
        "description": "The number of reinforcements in a circular cross section refers to the total count of steel bars arranged within a circular concrete section.",
        "latexSymbol": "n_{\\phi}",
        "type": "number",
        "unit": "ea",
        "notation": "standard",
        "decimal": 0,
        "default": 32,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G22_COMP_16",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(2)"
        ],
        "title": "Cover to longitudinal reinforcement in circular cross section",
        "description": "The cover to longitudinal reinforcement in a circular cross section refers to the distance between the outer surface of the concrete and the nearest surface of the steel reinforcement.",
        "latexSymbol": "c",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 80,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G22_COMP_17",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.7.2(1)"
        ],
        "title": "Sum of squared distances to reinforcement",
        "description": "This value represents the total of the squared distances from the center of the concrete area to each reinforcement bar in a circular cross-section.",
        "latexSymbol": "y_{i}^{2}",
        "latexEquation": "\\sum_{n=1}^{\\sym{n_{\\phi}}}(\\cos((\\frac{2 \\times \\pi}{\\sym{n_{\\phi}}}) \\times (n-1)) \\times (\\frac{\\sym{D}}{2}-\\sym{c}-\\frac{\\sym{\\phi}}{2}))^{2}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G22_COMP_15",
            "G6_COMP_9",
            "G22_COMP_16",
            "G22_COMP_14"
        ]
    },
    {
        "id": "G22_COMP_18",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.1(5.13N)"
        ],
        "title": "Relative normal force affecting the critical slenderness limit",
        "description": "The relative axial force is the ratio of the applied axial load to the compressive strength of the concrete section. It represents the proportion of the axial load compared to the load-bearing capacity of the concrete section. A higher value indicates a larger axial load relative to the concrete strength, while a lower value suggests a smaller axial load.",
        "latexSymbol": "n",
        "latexEquation": "\\frac{\\sym{N_{Ed}}\\times 1000}{\\sym{A_{c}} \\times \\sym{f_{cd}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G21_COMP_3",
            "G22_COMP_9",
            "G14_COMP_15"
        ]
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/107448295/EN1992-1-1+Nominal+Stiffness+and+Buckling+Load
        'id': '22',
        'standardType': 'EUROCODE',
        'codeName': 'EN1992-1-1',
        'codeTitle': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Nominal Stiffness and Buckling Load Calculation for Statically Determinate Structures',
        'description': r"[EN1992-1-1] This guide provides a step-by-step process for calculating the nominal stiffness of slender compression members in statically determinate structures, specifically focusing on members with circular cross sections, and using this information to compute the buckling load. The nominal stiffness represents the overall stiffness of members with arbitrary cross sections, considering the contributions of both concrete and steel reinforcements. Once the nominal stiffness is calculated, it is used to determine the critical buckling load, which is the point at which a structural member becomes unstable and buckles. This guide is specifically tailored for statically determinate structures where these methods are applicable, with a particular emphasis on circular cross sections.",
        'edition': '2004',
        'targetComponents': ['G22_COMP_1', 'G22_COMP_2'],
        'testInput': [
            {'component': 'G6_COMP_2', 'value': 'Pinned Ends'}, # buckmode = Pinned Ends
            {'component': 'G6_COMP_4', 'value': 14.5},
            {'component': 'G6_COMP_9', 'value': 550},
            {'component': 'G14_COMP_3', 'value': 'Persistent'}, # designsitu = Persistent
            {'component': 'G14_COMP_4', 'value': 'C12/15'}, # C = C12/15
            {'component': 'G21_COMP_3', 'value': 1500},
            {'component': 'G22_COMP_14', 'value': 16},
            {'component': 'G22_COMP_15', 'value': 32},
            {'component': 'G22_COMP_16', 'value': 80},
        ],
    },
]