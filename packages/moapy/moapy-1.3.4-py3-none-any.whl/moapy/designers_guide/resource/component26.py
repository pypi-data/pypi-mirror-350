component_list = [
    {
        "id": "G26_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(4)"
        ],
        "title": "Maximum design compressive stress for nodes",
        "description": "The minimum transverse reinforcement area for lap length, Ast,min,lap, is the smallest amount of transverse reinforcement, such as ties or stirrups, required to provide adequate confinement and ensure proper force transfer in the lapped area. This value helps to maintain the structural integrity of the lap splice by enhancing bond strength.",
        "latexSymbol": "\\sigma_{Rd,max}",
        "latexEquation": "\\sym{k_{2}} \\times \\sym{\\nu\\prime} \\times \\sym{f_{cd}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_3",
            "G26_COMP_2",
            "G14_COMP_15"
        ]
    },
    {
        "id": "G26_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.2(6.57N)"
        ],
        "title": "Reduction factor for concrete strength",
        "description": "The reduction factor is used to adjust the design compressive strength of concrete in struts, considering factors that may affect material strength. This value is specified in the National Annex or can be calculated based on concrete compressive strength.",
        "latexSymbol": "\\nu\\prime",
        "latexEquation": "1 - \\sym{f_{ck}} /250",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_5"
        ]
    },
    {
        "id": "G26_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(4)"
        ],
        "title": "Coefficient for compression node with ties in one direction",
        "description": "This coefficient is applied to compression-tension nodes where ties are anchored in one direction, allowing calculation of the maximum design compressive stress based on reinforcement along a single axis.",
        "latexSymbol": "k_{2}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "default": 0.85,
        "const": True
    },
    {
        "id": "G26_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Width of the structure",
        "description": "The width of the structure refers to the horizontal dimension of the cross-section. It plays a critical role in determining the load transfer area at the support and the effective width of nodes during the design process using the strut-and-tie model.",
        "latexSymbol": "B",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 3200.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G26_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Height of the structure",
        "description": "The height of the structure refers to the vertical dimension of the cross-section. It determines the spatial constraints of the node and influences the stress distribution within the node and the arrangement of reinforcement.",
        "latexSymbol": "H",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 1200.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G26_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Length of the structure",
        "description": "The length of the structure refers to the horizontal distance in the direction perpendicular to its width. It defines the overall span or reach of the structure and impacts the distribution of loads, support reactions, and the geometry of struts and ties in the design process.",
        "latexSymbol": "L",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 1000.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G26_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Width of tie or height of nodal zone",
        "description": "The width of the tie or the height of the nodal zone is a crucial dimension that affects compressive stress distribution within the node. Adjusting this width can increase the node size, allowing for more effective stress distribution and enhanced capacity of incoming struts. This dimension is influenced by the spacing between tie centers and the concrete cover thickness.",
        "latexSymbol": "u",
        "latexEquation": "2 \\times \\sym{s_{o}} + (\\sym{n} - 1) \\times \\sym{s}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_14",
            "G26_COMP_13",
            "G26_COMP_12"
        ]
    },
    {
        "id": "G26_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Angle between tie and strut in CCT node",
        "description": "The angle between the tie and strut in a CCT node represents the orientation at which the strut intersects with the tie within the node. This angle is influenced by factors such as the width of the tie (u) and the bearing width, which impact the overall geometry and load transfer characteristics of the strut-and-tie model (STM).",
        "latexSymbol": "\\theta",
        "latexEquation": "\\arctan{(\\frac{(\\sym{H} - \\sym{u})}{(\\frac{\\sym{B}}{2} - \\sym{l_{b}} + \\frac{\\sym{a_{1}}}{2})})}",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_5",
            "G26_COMP_7",
            "G26_COMP_4",
            "G26_COMP_10",
            "G26_COMP_9"
        ]
    },
    {
        "id": "G26_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Effective width at support interface",
        "description": "The effective width at the support interface represents the portion of the support width where loads are primarily concentrated and transferred. This focused width reflects the zone where load distribution is most intense, allowing for a more accurate and efficient assessment of bearing stresses.",
        "latexSymbol": "a_{1}",
        "latexEquation": "\\sym{l_{b}} - 2 \\times s_{o} - \\sym{c_{nom}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_10",
            "G26_COMP_14",
            "G26_COMP_15"
        ]
    },
    {
        "id": "G26_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Width of support structure",
        "description": "The width of the support structure refers to the total width of the structural element that provides bearing support. The effective width of the bearing face is determined within this overall width, serving as the area where loads are directly transferred to the node.",
        "latexSymbol": "l_{b}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 1000.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G26_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Width of strut",
        "description": "The width of the strut refers to the effective width of the strut where it connects to the node. This dimension is calculated based on the effective width of the bearing face, the angle of the strut, and the width of the tie.",
        "latexSymbol": "a_{2}",
        "latexEquation": "\\sym{a_{1}} \\times \\sin{(\\sym{\\theta})} + \\sym{u} \\times \\cos{(\\sym{\\theta})}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_9",
            "G26_COMP_8",
            "G26_COMP_7"
        ]
    },
    {
        "id": "G26_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Spacing between tie bars",
        "description": "The spacing between tie bars is the distance between the centers of adjacent tie reinforcements. This spacing directly influences the overall width of the tie or the height of the nodal zone, playing a critical role in managing stress distribution within the node and ensuring optimal reinforcement placement.",
        "latexSymbol": "s",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 150.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G26_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Number of tie bars",
        "description": "The number of tie bars refers to the total count of reinforcement bars within a node. While having more tie bars can increase the width of the tie or the height of the nodal zone, enhancing the node’s capacity to distribute stress effectively, it can also reduce the angle of connected struts, which may negatively impact the efficiency of the strut-and-tie model.",
        "latexSymbol": "n",
        "type": "number",
        "unit": "ea",
        "notation": "standard",
        "decimal": 0,
        "default": 2.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G26_COMP_14",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Distance from concrete surface to outermost tie center",
        "description": "The distance from the concrete surface to the center of the outermost tie reinforcement is essential for determining node and strut dimensions. This distance, along with factors such as bearing length, tie width, and strut angle, influences the width of struts at CCT nodes, ensuring effective stress distribution and sufficient cover for reinforcement.",
        "latexSymbol": "s_{o}",
        "latexEquation": "\\sym{c_{nom}} + \\sym{\\phi_{t}} + \\frac{\\sym{\\phi}}{2}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_15",
            "G26_COMP_16",
            "G26_COMP_17"
        ]
    },
    {
        "id": "G26_COMP_15",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Nominal concrete cover",
        "description": "The nominal concrete cover is the specified distance from the nearest concrete surface to the outermost reinforcement surface, ensuring protection and durability. It is calculated as the minimum cover, which provides necessary protection, plus an additional allowance to account for construction deviations.",
        "latexSymbol": "c_{nom}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 50.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G26_COMP_16",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Diameter of transverse reinforcement",
        "description": "The diameter of the transverse reinforcement refers to the thickness of the reinforcing bar placed perpendicular to the main reinforcement. This dimension is part of the calculation for the distance from the concrete surface to the center of the outermost tie.",
        "latexSymbol": "\\phi_{t}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "default": 16.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G26_COMP_17",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Diameter of tie reinforcement",
        "description": "The diameter of the tie reinforcement refers to the thickness of the primary reinforcing bar within a node, determined based on the requirements of the strut-and-tie model (STM) analysis. This value is crucial for calculating the distance from the concrete surface to the outermost tie center.",
        "latexSymbol": "\\phi",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 0,
        "default": 32.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G26_COMP_18",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.26)"
        ],
        "title": "Vertical load acting on structure",
        "description": "The vertical load acting on the structure, often represented as the force due to gravity, is the downward force applied perpendicular to the structural element.",
        "latexSymbol": "F_{cd}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "default": 5000.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G26_COMP_19",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Support reaction due to vertical load",
        "description": "The support reaction is the force generated at the support position due to the vertical load acting on the structure. This reaction force acts at the center of the effective width of the bearing face.",
        "latexSymbol": "F_{cd1}",
        "latexEquation": "\\frac{\\sym{F_{cd}}}{2}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_18"
        ]
    },
    {
        "id": "G26_COMP_20",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Design compressive stress at the node",
        "description": "The design compressive stress at the node is calculated using the support reaction force. It is determined by dividing the support reaction by the product of the effective width at the support and the length of the structure. This value represents the compressive stress within the node.",
        "latexSymbol": "\\sigma_{Rd1}",
        "latexEquation": "\\frac{(\\sym{F_{cd1}} \\times 10^{3})}{(\\sym{a_{1}} \\times \\sym{L})}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_19",
            "G26_COMP_9",
            "G26_COMP_6"
        ]
    },
    {
        "id": "G26_COMP_21",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Force Acting on the Strut",
        "description": "This represents the force acting along the strut at the node. It is calculated as the horizontal component of the vertical support reaction, considering the angle between the strut and the tie. This force indicates the magnitude of load transferred through the strut within the strut-and-tie model.",
        "latexSymbol": "F_{cd2}",
        "latexEquation": "\\frac{\\sym{F_{cd1}}}{\\sin{(\\sym{\\theta})}}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_19",
            "G26_COMP_8"
        ]
    },
    {
        "id": "G26_COMP_22",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Design compressive stress along the strut",
        "description": "This is the design compressive stress along the strut at the node, determined by dividing the force acting on the strut by the product of the effective width of the strut and the length of the structure. It provides the stress value transmitted through the strut to ensure the node's stability.",
        "latexSymbol": "\\sigma_{Rd2}",
        "latexEquation": "\\frac{\\sym{F_{cd2}} \\times 10^{3}}{(\\sym{a_{2}} \\times \\sym{L})}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_21",
            "G26_COMP_11",
            "G26_COMP_6"
        ]
    },
    {
        "id": "G26_COMP_23",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Design compressive stress in the CCT node",
        "description": "This represents the highest compressive stress at the node, determined by comparing the compressive stresses along the vertical and horizontal components and selecting the larger value. It ensures the design accounts for the most critical stress scenario within the node.",
        "latexSymbol": "\\sigma_{Rd}",
        "latexEquation": "\\max(\\sym{\\sigma_{Rd1}}, \\sym{\\sigma_{Rd2}})",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G26_COMP_20",
            "G26_COMP_22"
        ]
    },
    {
        "id": "G26_COMP_24",
        "codeName": "EN1992-1-1",
        "reference": [
            "6.5.4(Figure6.27)"
        ],
        "title": "Compressive stress verification for CCT nodes",
        "description": "This section verifies whether the compressive stress in CCT nodes meets the design requirements by comparing the design compressive stress, calculated as the larger value between stresses along vertical and horizontal directions, with the maximum allowable compressive stress. The maximum allowable stress is determined based on material properties and the configuration of the node.",
        "latexSymbol": "cctverif",
        "type": "number",
        "unit": "",
        "notation": "text",
        "required": [
            "G26_COMP_1",
            "G26_COMP_23"
        ],
        "table": "text",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{\\sigma_{Rd,max}} > \\sym{\\sigma_{Rd}}",
                    "\\sym{\\sigma_{Rd,max}} <= \\sym{\\sigma_{Rd}}"
                ]
            ],
            "data": [
                [
                    "OK"
                ],
                [
                    "NG"
                ]
            ]
        }
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/134709621/EN1992-1-1+CCT+Nodes+Compressive+Stress
        'id': '26',
        'standardType': 'EUROCODE',
        'codeName': 'EN1992-1-1',
        'codeTitle': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Maximum and Design Compressive Stress in CCT Nodes',
        'description': r"[EN1992-1-1] This guide provides a comprehensive method for calculating the maximum design compressive stress and the design compressive stress at CCT nodes. It explains the relationship between forces acting on the strut and tie, the geometry of the node, and material properties. To illustrate the calculation process, a simple deep beam example is used, offering clear step-by-step instructions. The guide includes key equations, parameter definitions, and practical examples to help users better understand the process of calculating CCT nodes in the strut-and-tie model.",
        'figureFile': 'detail_content_26.png',
        'edition': '2004',
        'targetComponents': ['G26_COMP_1', 'G26_COMP_23', 'G26_COMP_24'],
        'testInput': [
            {'component': 'G14_COMP_3', 'value': 'Persistent'}, # designsitu = Persistent
            {'component': 'G14_COMP_4', 'value': 'C12/15'}, # C = C12/15
            {'component': 'G26_COMP_4', 'value': 3200},
            {'component': 'G26_COMP_5', 'value': 1200},
            {'component': 'G26_COMP_6', 'value': 1000},
            {'component': 'G26_COMP_10', 'value': 1000},
            {'component': 'G26_COMP_12', 'value': 150},
            {'component': 'G26_COMP_13', 'value': 2},
            {'component': 'G26_COMP_15', 'value': 50},
            {'component': 'G26_COMP_16', 'value': 16},
            {'component': 'G26_COMP_17', 'value': 32},
            {'component': 'G26_COMP_18', 'value': 5000},
        ],
    },
]