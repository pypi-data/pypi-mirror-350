component_list = [
    {
        "id": "G23_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.2(5.33)"
        ],
        "title": "Nominal second order moment",
        "description": "The nominal second-order moment, which is calculated based on nominal curvature, is primarily suitable for isolated members with constant axial force and a defined effective length. This method accounts for additional bending moments caused by member deflection under load, making it particularly important for slender members.",
        "latexSymbol": "M_{2}",
        "latexEquation": "\\sym{N_{Ed}} \\times \\sym{e_{2}}",
        "type": "number",
        "unit": "kN.m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G21_COMP_3",
            "G23_COMP_2"
        ]
    },
    {
        "id": "G23_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.2(3)"
        ],
        "title": "Deflection due to nominal curvature",
        "description": "The deflection due to nominal curvature is calculated based on the member's curvature, effective length, and a factor that depends on the curvature distribution. This deflection accounts for the additional deformation caused by axial loads.",
        "latexSymbol": "e_{2}",
        "latexEquation": "\\sym{{1/r}} \\times \\frac{\\sym{l_{0}}^{2}}{\\sym{c_{c}}}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G23_COMP_8",
            "G6_COMP_3",
            "G23_COMP_3"
        ]
    },
    {
        "id": "G23_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.2(4)"
        ],
        "title": "Factor for curvature distribution",
        "description": "This factor accounts for the distribution of curvature in structural members. A value of 10 is used when the curvature follows a sinusoidal distribution, reflecting more severe deformations. When the first-order moment is constant, a lower value of 8 is applied. In unfavorable conditions, 8 is chosen to ensure safety by considering greater curvature effects.",
        "latexSymbol": "c_{c}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 0,
        "default": 8.0,
        "const": True
    },
    {
        "id": "G23_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.3(5.35)"
        ],
        "title": "Effective depth in sections with distributed reinforcement",
        "description": "The effective depth is the distance from the extreme compression fiber to the centroid of the tensile reinforcement. If the reinforcement is not entirely concentrated on opposite sides but is instead distributed parallel to the plane of bending, the effective depth is determined by taking half the total height of the section and adjusting for the distribution of the reinforcement.",
        "latexSymbol": "d",
        "latexEquation": "\\frac{\\sym{D}}{2} + \\sym{i_{s}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G6_COMP_9",
            "G23_COMP_5"
        ]
    },
    {
        "id": "G23_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.3(2)"
        ],
        "title": "Radius of gyration of total reinforcement area",
        "description": "The radius of gyration of the reinforcement represents how the reinforcement is distributed relative to the centroid of the section. It adjusts the calculation of the effective depth when the reinforcement is not concentrated at the extreme sides but is distributed parallel to the plane of bending. This value helps in determining the correct effective depth by accounting for the spread of the reinforcement within the section.",
        "latexSymbol": "i_{s}",
        "latexEquation": "\\sqrt{\\frac{\\sym{I_{s}}}{\\sym{A_{s}}}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G22_COMP_13",
            "G22_COMP_10"
        ]
    },
    {
        "id": "G23_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.3(4"
        ],
        "title": "Radius of gyration of concrete section",
        "description": "The radius of gyration of the concrete section reflects how the concrete mass is distributed relative to its centroid. It is used to adjust calculations related to the section’s stiffness and stability, particularly in cases where the concrete section is not uniform or symmetrically loaded.",
        "latexSymbol": "i_{c}",
        "latexEquation": "\\sqrt{\\frac{\\sym{I_{c}}}{\\sym{A_{c}}}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G22_COMP_12",
            "G22_COMP_9"
        ]
    },
    {
        "id": "G23_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.3(3)"
        ],
        "title": "Mechanical reinforcement ratio for curvature",
        "description": "The mechanical reinforcement ratio represents the contribution of reinforcement relative to the concrete's strength. For symmetrical cross sections, it affects the member's stiffness and influences the resulting curvature under loading.",
        "latexSymbol": "\\omega",
        "latexEquation": "\\frac{(\\sym{A_{s}} \\times \\sym{f_{yd}})}{(\\sym{A_{c}} \\times \\sym{f_{cd}})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G22_COMP_10",
            "G18_COMP_3",
            "G22_COMP_9",
            "G14_COMP_15"
        ]
    },
    {
        "id": "G23_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.3(5.34)"
        ],
        "title": "Curvature for symmetrical cross sections",
        "description": "Curvature refers to the degree of bending in a member under load. For symmetrical cross sections, it takes into account the effects of axial load and creep, influencing how much the member bends in response to applied forces.",
        "latexSymbol": "{1/r}",
        "latexEquation": "\\sym{K_{r}} \\times \\sym{K_{\\phi}} \\times \\sym{{1/r_{0}}}",
        "type": "number",
        "unit": "1/m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G23_COMP_10",
            "G23_COMP_13",
            "G23_COMP_9"
        ]
    },
    {
        "id": "G23_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.3(1)"
        ],
        "title": "Initial curvature based on yield strain of reinforcing steel",
        "description": "The initial curvature is determined by the yield strain of the reinforcing steel and the effective depth of the section. This curvature serves as the baseline before accounting for additional effects such as axial loads and creep.",
        "latexSymbol": "{1/r_{0}}",
        "latexEquation": "\\frac{\\frac{\\sym{\\epsilon_{yd}}}{100}}{0.45 \\times (\\frac{\\sym{d}}{1000})}",
        "type": "number",
        "unit": "1/m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G18_COMP_6",
            "G23_COMP_4"
        ]
    },
    {
        "id": "G23_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.3(5.36)"
        ],
        "title": "Correction factor depending on axial load",
        "description": "The correction factor depending on axial load adjusts the curvature based on the relative axial force in the member. It is calculated using the design axial force, the concrete cross-sectional area, and the reinforcement properties. This factor accounts for the influence of axial force on the bending capacity of the member.",
        "latexSymbol": "K_{r}",
        "latexEquation": "\\min(\\frac{\\sym{n_{u}} - \\sym{n}}{\\sym{n_{u}} - \\sym{n_{bal}}} , 1)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G23_COMP_11",
            "G22_COMP_18",
            "G23_COMP_12"
        ]
    },
    {
        "id": "G23_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.3(3)"
        ],
        "title": "Ultimate axial load capacity of reinforced concrete",
        "description": "This refers to the maximum axial load a reinforced concrete member can bear, taking into account both the load-bearing capacity of the concrete and the additional contribution from the reinforcement. It represents the combined strength of the concrete and reinforcement under axial loading conditions.",
        "latexSymbol": "n_{u}",
        "latexEquation": "1 + \\sym{\\omega}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G23_COMP_7"
        ]
    },
    {
        "id": "G23_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.3(3)"
        ],
        "title": "Balanced axial force at maximum moment resistance",
        "description": "The balanced axial force at maximum moment resistance is the point where both concrete and reinforcement are fully engaged in resisting the load. At this stage, the concrete reaches its compressive limit, and the reinforcement reaches its yield point, allowing the member to resist its maximum bending moment just before failure.",
        "latexSymbol": "n_{bal}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 0.4,
        "const": True
    },
    {
        "id": "G23_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.3(5.37)"
        ],
        "title": "Factor for taking account of creep",
        "description": "This factor adjusts for the long-term deformation, known as creep, in the member. It is calculated based on the effective creep ratio and other parameters like concrete strength and slenderness ratio.",
        "latexSymbol": "K_{\\phi}",
        "latexEquation": "\\max(1 + \\sym{\\beta} \\times \\sym{\\phi_{ef}} , 1)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G23_COMP_14",
            "G21_COMP_6"
        ]
    },
    {
        "id": "G23_COMP_14",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.8.3(4)"
        ],
        "title": "Effective creep ratio adjustment factor",
        "description": "The factor is used in the calculation of the creep adjustment factor and is multiplied by the effective creep ratio to determine the overall impact of creep on the member. This coefficient depends on the concrete strength and the slenderness ratio.",
        "latexSymbol": "\\beta",
        "latexEquation": "0.35 + \\frac{\\sym{f_{ck}}}{200} - \\frac{\\sym{\\lambda}}{150}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_5",
            "G23_COMP_15"
        ]
    },
    {
        "id": "G23_COMP_15",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(5.14)"
        ],
        "title": "Slenderness ratio for circular concrete sections",
        "description": "The slenderness ratio is a dimensionless value comparing the effective length of a circular concrete member to its radius of gyration. For circular sections, this ratio indicates the member's risk of buckling under axial loads.",
        "latexSymbol": "\\lambda",
        "latexEquation": "\\frac{\\sym{l_{0}}}{(\\frac{\\sym{i_{c}}}{1000})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G6_COMP_3",
            "G23_COMP_6"
        ]
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/107449389/EN1992-1-1+Curvature+and+Second-Order+Moment
        'id': '23',
        'standardType': 'EUROCODE',
        'codeName': 'EN1992-1-1',
        'codeTitle': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Curvature and Second-Order Moment Calculation for Circular Sections',
        'description': r"[EN1992-1-1] This guide provides a step-by-step process for calculating the curvature and using it to determine the nominal second-order moment specifically for circular sections in structural design. It explains key factors such as the radius of gyration of reinforcement, effective depth, and deflection due to nominal curvature, all of which are necessary for accurate calculations in circular sections. The guide is aimed at engineers and designers working with slender members under axial loads. Clear examples and relevant formulas are provided to ensure easy application in practice.",
        'edition': '2004',
        'targetComponents': ['G23_COMP_1', 'G23_COMP_8'],
        'testInput': [
            {'component': 'G6_COMP_2', 'value': 'Pinned Ends'}, # buckmode = Pinned Ends
            {'component': 'G6_COMP_4', 'value': 14.5},
            {'component': 'G6_COMP_9', 'value': 550},
            {'component': 'G14_COMP_3', 'value': 'Persistent'}, # designsitu = Persistent
            {'component': 'G14_COMP_4', 'value': 'C12/15'}, # C = C12/15
            {'component': 'G16_COMP_11', 'value': 534694.0},
            {'component': 'G18_COMP_1', 'value': 500},
            {'component': 'G21_COMP_3', 'value': 1500},
            {'component': 'G22_COMP_14', 'value': 16},
            {'component': 'G22_COMP_15', 'value': 32},
            {'component': 'G22_COMP_16', 'value': 80},
        ],
    },
]