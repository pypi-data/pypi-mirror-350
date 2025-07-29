component_list = [
    {
        "id": "G24_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.3(8.3)"
        ],
        "title": "Basic required anchorage length",
        "description": "The basic required anchorage length refers to the minimum length needed to safely transfer the force from the reinforcement to the concrete, ensuring adequate bond strength. It depends on the diameter of the reinforcement bar, the design stress of the bar, and the bond stress between the reinforcement and concrete.",
        "latexSymbol": "l_{b,rqd}",
        "latexEquation": "(\\frac{\\sym{\\phi}}{4})\\times (\\frac{\\sym{\\sigma_{sd}}}{\\sym{f_{bd}}})",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_2",
            "G24_COMP_3",
            "G24_COMP_4"
        ]
    },
    {
        "id": "G24_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.1(Figure8.1)"
        ],
        "title": "Bar diameter",
        "description": "Bar diameter refers to the thickness of a reinforcement bar, usually measured in millimeters. It is a critical parameter used in calculating anchorage and lap lengths, as the size of the bar directly impacts the bond strength between the reinforcement and the surrounding concrete.",
        "latexSymbol": "\\phi",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 20.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G24_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.3(2)"
        ],
        "title": "Design stress of the reinforcement",
        "description": "The design stress of the reinforcement is the stress level in the reinforcing steel at the specific position from which the anchorage length is measured. Generally, it is desirable for anchorage lengths to be based on the design strength of the bar (i.e., when the design stress equals the yield strength), although the code allows a lower stress if the reinforcement is not intended to be fully stressed.",
        "latexSymbol": "\\sigma_{sd}",
        "latexEquation": "\\sym{f_{yd}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G18_COMP_3"
        ]
    },
    {
        "id": "G24_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.2(8.2)"
        ],
        "title": "Ultimate bond stress",
        "description": "The ultimate bond stress refers to the maximum stress that can be developed between reinforcing steel and concrete to prevent bond failure. It depends on the quality of the bond condition, the position of the reinforcement during concreting, and the bar diameter.",
        "latexSymbol": "f_{bd}",
        "latexEquation": "2.25 \\times \\sym{\\eta_{1}} \\times \\sym{\\eta_{2}} \\times \\sym{f_{ctd}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_6",
            "G24_COMP_7",
            "G14_COMP_16"
        ]
    },
    {
        "id": "G24_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.2(Figure8.2)"
        ],
        "title": "Bond condition selection",
        "description": "Bond conditions are a crucial factor in determining the anchorage length of reinforcement. The conditions vary based on the placement of the reinforcement, the thickness of the concrete element, and the direction of concrete pouring.",
        "latexSymbol": "bondcon",
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
                    "Good",
                    "Applies when the height of the concrete element is 250mm or less, or the reinforcement bar placement angle is between 45° and 90°. In this case, the bond quality between the reinforcement and concrete is optimal."
                ],
                [
                    "Poor",
                    "When the height of the concrete element exceeds 250mm, reinforcement located in the upper region, excluding the bottom 250mm, is subject to poor bond conditions. If the height exceeds 600mm, reinforcement in the top 300mm region is also considered to have poor bond conditions."
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.2(2)"
        ],
        "title": "Bond condition coefficient",
        "description": "The bond condition coefficient describes the quality of the bond between reinforcement and concrete. It indicates whether the bond conditions are optimal or reduced, affecting the overall effectiveness of the reinforcement anchorage.",
        "latexSymbol": "\\eta_{1}",
        "latexEquation": "1.0",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_5"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{bondcon} = Good",
                    "\\sym{bondcon} = Poor"
                ]
            ],
            "data": [
                [
                    "1.0"
                ],
                [
                    "0.7"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.2(2)"
        ],
        "title": "Bar diameter coefficient",
        "description": "The bar diameter coefficient reflects the influence of the reinforcement bar size on the bond stress. It adjusts the bond strength based on whether the bar diameter is greater or less than 32mm.",
        "latexSymbol": "\\eta_{2}",
        "latexEquation": "1.0",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_2"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{\\phi} <= 32",
                    "\\sym{\\phi} > 32"
                ]
            ],
            "data": [
                [
                    "1.0"
                ],
                [
                    "\\frac{(132 - \\sym{\\phi})}{100}"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(1)"
        ],
        "title": "Select anchorage condition",
        "description": "Choose the appropriate anchorage condition to determine the minimum anchorage length. This selection is crucial as the anchorage requirement differs based on whether the reinforcement is under tension or compression.",
        "latexSymbol": "anchcond",
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
                    "For anchorages in tension",
                    "Use when the reinforcement is subjected to pulling forces, such as in the bottom reinforcement of a simply supported beam, where the bar experiences tension as the beam bends downward."
                ],
                [
                    "For anchorages in compression",
                    "Use when the reinforcement is subjected to pushing forces, such as in the top reinforcement of a column, where the bar is compressed due to the weight of the structure above."
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(1)"
        ],
        "title": "Minimum anchorage length",
        "description": "The minimum anchorage length represents the shortest required length to securely anchor the reinforcement under specific conditions without imposing additional limitations. It ensures that the reinforcement can transfer forces effectively to the concrete, maintaining the integrity of the structural connection and preventing premature bond failure.",
        "latexSymbol": "l_{b,min}",
        "latexEquation": "\\max(0.3 \\times \\sym{l_{b,rqd}}, 10 \\times \\sym{\\phi}, 100)",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_1",
            "G24_COMP_2",
            "G24_COMP_8"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{anchcond} = For anchorages in tension",
                    "\\sym{anchcond} = For anchorages in compression"
                ]
            ],
            "data": [
                [
                    "\\max(0.3 \\times \\sym{l_{b,rqd}}, 10 \\times \\sym{\\phi}, 100)"
                ],
                [
                    "\\max(0.6 \\times \\sym{l_{b,rqd}}, 10 \\times \\sym{\\phi}, 100)"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(8.4)"
        ],
        "title": "Design anchorage length",
        "description": "The design anchorage length is the minimum length required to anchor the reinforcement safely, ensuring the transfer of forces from the reinforcement to the concrete. It is calculated by adjusting the basic anchorage length using various factors that account for bar shape, concrete cover, confinement, and transverse reinforcement.",
        "latexSymbol": "l_{bd}",
        "latexEquation": "\\max(\\sym{\\alpha_{1}} \\times \\sym{\\alpha_{2}} \\times \\sym{\\alpha_{3}} \\times \\sym{\\alpha_{4}} \\times \\sym{\\alpha_{5}} \\times \\sym{l_{b,rqd}}, \\sym{l_{b,min}})",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_2",
            "G24_COMP_12",
            "G24_COMP_18",
            "G24_COMP_20",
            "G24_COMP_21",
            "G24_COMP_23",
            "G24_COMP_24",
            "G24_COMP_1",
            "G24_COMP_9",
            "G24_COMP_19",
            "G24_COMP_32"
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
                    "\\max(\\sym{\\alpha_{1}} \\times \\sym{\\alpha_{2}} \\times \\sym{\\alpha_{3}} \\times \\sym{\\alpha_{4}} \\times \\sym{\\alpha_{5}} \\times \\sym{l_{b,rqd}}, \\sym{l_{b,min}})"
                ],
                [
                    "\\max(\\sym{\\alpha_{1,3\\sym{\\phi}}} \\times \\sym{\\alpha_{2}} \\times \\sym{\\alpha_{3}} \\times \\sym{\\alpha_{4}} \\times \\sym{\\alpha_{5}} \\times \\sym{l_{b,rqd}}, \\sym{l_{b,min}})"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Figure8.3)"
        ],
        "title": "Select bar configuration",
        "description": "Choose the configuration of the reinforcement bars to determine the appropriate effective concrete cover for anchorage and bond calculations. The configuration impacts how the effective cover is measured and applied.",
        "latexSymbol": "barconfig",
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
                    "Straight bars",
                    "Bars placed in a straight line, with cover determined by the smallest distance from the bar to the concrete surface."
                ],
                [
                    "Bent or hooked bars",
                    "Bars that are bent or have hooks, with cover determined based on the distance from the bar to the side of the concrete."
                ],
                [
                    "Looped bars",
                    "Bars formed into a loop, with cover measured from the bar to the concrete bottom surface."
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Figure8.3)"
        ],
        "title": "Effective concrete cover for beams and slabs",
        "description": "Effective concrete cover is the distance used to determine the bond and anchorage conditions of reinforcement bars in beams and slabs. The value of effective cover depends on the configuration of the bars (straight, bent or hooked, or looped) and is calculated differently based on the placement and cover dimensions.",
        "latexSymbol": "c_{d}",
        "latexEquation": "\\min{(\\frac{\\sym{a}}{2} , \\sym{c_{1}} , \\sym{c})}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_11",
            "G24_COMP_13",
            "G24_COMP_15",
            "G24_COMP_14"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{barconfig} = Straight bars",
                    "\\sym{barconfig} = Bent or hooked bars",
                    "\\sym{barconfig} = Looped bars"
                ]
            ],
            "data": [
                [
                    "\\min(\\frac{\\sym{a}}{2} , \\sym{c_{1}} , \\sym{c})"
                ],
                [
                    "\\min(\\frac{\\sym{a}}{2} , \\sym{c_{1}})"
                ],
                [
                    "\\sym{c}"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Figure8.3)"
        ],
        "title": "Bar spacing",
        "description": "Bar spacing distance refers to the distance between two parallel reinforcement bars. This spacing is important for ensuring proper concrete placement and adequate bond strength between the bars and the surrounding concrete.",
        "latexSymbol": "a",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 125.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G24_COMP_14",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Figure8.3)"
        ],
        "title": "Bottom concrete cover",
        "description": "Bottom concrete cover is the distance from the bottom surface of the concrete element to the surface of the nearest reinforcement bar. It is considered separately from side cover because the thickness of the cover can vary based on factors like the presence of transverse reinforcement, the specific placement of rebar, and differences in how the concrete element interacts with the ground or supports.",
        "latexSymbol": "c",
        "latexEquation": "\\sym{c_{nom}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_16"
        ]
    },
    {
        "id": "G24_COMP_15",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Figure8.3)"
        ],
        "title": "Side concrete cover",
        "description": "Side concrete cover is the distance from the side surface of the concrete element to the surface of the nearest reinforcement bar. It is treated separately from bottom cover because the cover thickness can differ due to factors such as the need for protection against lateral forces, potential exposure to different environmental conditions, and variations in reinforcement layout.",
        "latexSymbol": "c_{1}",
        "latexEquation": "\\sym{c_{nom}} + \\sym{\\phi_{t}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_16",
            "G24_COMP_17"
        ]
    },
    {
        "id": "G24_COMP_16",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Figure8.3)"
        ],
        "title": "Nominal concrete cover",
        "description": "Nominal concrete cover is the distance from the surface of the reinforcement, including links, stirrups, or surface reinforcement if applicable, to the nearest concrete surface. This cover ensures protection of the reinforcement and contributes to the overall structural integrity.",
        "latexSymbol": "c_{nom}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 55.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G24_COMP_17",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Figure8.4)"
        ],
        "title": "Diameter of transverse reinforcement",
        "description": "The diameter of transverse reinforcement refers to the thickness of the transverse reinforcement bars, such as ties or stirrups, used along the design anchorage length.",
        "latexSymbol": "\\phi_{t}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 12.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G24_COMP_18",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Standard bar shape coefficient",
        "description": "The standard bar shape coefficient is used when the effective concrete cover is less than or equal to three times the bar diameter. For straight bars in tension, this coefficient is typically 1.0, indicating that the bar shape does not affect the anchorage length.",
        "latexSymbol": "\\alpha_{1}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G24_COMP_19",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Adjusted bar shape coefficient for large cover",
        "description": "The adjusted bar shape coefficient is used when the effective concrete cover is greater than three times the bar diameter. This coefficient accounts for the additional anchorage performance provided by the larger cover, potentially reducing the required anchorage length.",
        "latexSymbol": "\\alpha_{1,3\\phi}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_11",
            "G24_COMP_8"
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
                    "1.0",
                    "1.0"
                ],
                [
                    "0.7",
                    "1.0"
                ],
                [
                    "0.7",
                    "1.0"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_20",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Concrete cover coefficient",
        "description": "The concrete cover coefficient considers the effect of the concrete cover thickness on the required anchorage length. This coefficient helps to account for how the depth of concrete surrounding the reinforcement affects bond strength. For example, a thicker concrete cover can improve bond performance and reduce the required anchorage length, while a thinner cover may require a longer anchorage length to ensure structural safety.",
        "latexSymbol": "\\alpha_{2}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_11",
            "G24_COMP_8",
            "G24_COMP_12",
            "G24_COMP_2"
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
                    "\\min(\\max(1 - 0.15\\times \\frac{(\\sym{c_{d}} - \\sym{\\phi})}{\\sym{\\phi}}, 0.7), 1.0)",
                    "1.0"
                ],
                [
                    "\\min(\\max(1 - 0.15\\times \\frac{(\\sym{c_{d}} - 3\\times \\sym{\\phi})}{\\sym{\\phi}}, 0.7), 1.0)",
                    "1.0"
                ],
                [
                    "\\min(\\max(1 - 0.15\\times \\frac{(\\sym{c_{d}} - 3\\times \\sym{\\phi})}{\\sym{\\phi}}, 0.7), 1.0)",
                    "1.0"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_21",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Coefficient of confinement by transverse reinforcement",
        "description": "The coefficient of confinement by transverse reinforcement accounts for the effect of transverse reinforcement, such as ties or stirrups, on the required anchorage length. This coefficient reflects how the presence of transverse reinforcement enhances bond strength by confining the anchored bar, which can reduce the anchorage length needed.",
        "latexSymbol": "\\alpha_{3}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_11",
            "G24_COMP_8",
            "G24_COMP_27",
            "G24_COMP_28"
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
                    "\\min(\\max(1 - \\sym{K} \\times \\sym{\\lambda}, 0.7),1.0)",
                    "1.0"
                ],
                [
                    "\\min(\\max(1 - \\sym{K} \\times \\sym{\\lambda}, 0.7),1.0)",
                    "1.0"
                ],
                [
                    "\\min(\\max(1 - \\sym{K} \\times \\sym{\\lambda}, 0.7),1.0)",
                    "1.0"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_22",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Select welded transverse reinforcement option",
        "description": "Choose whether welded transverse reinforcement is present along the design anchorage length. This selection will determine the appropriate coefficient for the level of confinement provided.",
        "latexSymbol": "weldtrans",
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
                    "Welded",
                    "Welded transverse reinforcement is present."
                ],
                [
                    "Not Welded",
                    "No welded transverse reinforcement is present."
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_23",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Coefficient for welded transverse reinforcement",
        "description": "The coefficient for welded transverse reinforcement accounts for the effect of one or more welded transverse bars along the design anchorage length. If no welded transverse reinforcement is present, the coefficient is equal to 1.0. However, if welded transverse bars are used, the coefficient is reduced to 0.7, reflecting the increased confinement provided.",
        "latexSymbol": "\\alpha_{4}",
        "latexEquation": "0.7",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_22"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{weldtrans} = Welded",
                    "\\sym{weldtrans} = Not Welded"
                ]
            ],
            "data": [
                [
                    "0.7"
                ],
                [
                    "1.0"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_24",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Coefficient for transverse pressure",
        "description": "The coefficient for transverse pressure accounts for the effect of any external pressure acting along the design anchorage length, perpendicular to the splitting plane. When no transverse pressure is present, the coefficient is equal to 1.0. If transverse pressure exists, the coefficient may be adjusted to reflect the additional confinement provided, which can influence the anchorage length requirements.",
        "latexSymbol": "\\alpha_{5}",
        "latexEquation": "\\min(\\max(1 - 0.04 \\times \\sym{p}, 0.7), 1.0)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_25",
            "G24_COMP_8"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{anchcond} = For anchorages in tension",
                    "\\sym{anchcond} = For anchorages in compression"
                ]
            ],
            "data": [
                [
                    "\\min(\\max(1 - 0.04 \\times \\sym{p}, 0.7),1.0)"
                ],
                [
                    "1.0"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_25",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Transverse pressure",
        "description": "Transverse pressure refers to the external pressure applied perpendicularly to the splitting plane along the design anchorage length at the ultimate limit state. This pressure can provide additional confinement to the reinforcement, potentially enhancing bond strength and affecting the anchorage length requirements.",
        "latexSymbol": "p",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "default": 0.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G24_COMP_26",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Figure8.4)"
        ],
        "title": "Placement option for confinement",
        "description": "Choose one of the placement options to determine the level of confinement provided by the transverse reinforcement. This selection impacts how the anchorage length is adjusted based on the position of the anchored bar.",
        "latexSymbol": "conplace",
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
                    "Bent Anchorage",
                    "When the transverse bar is positioned around a bent anchored bar for full confinement."
                ],
                [
                    "Partial Confinement",
                    "When the anchored bar is placed inside the transverse reinforcement, offering partial confinement."
                ],
                [
                    "No Confinement",
                    "When the anchored bar is placed outside the transverse reinforcement, providing no confinement."
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_27",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Figure8.4)"
        ],
        "title": "Coefficient for adjusting confinement",
        "description": "This coefficient is used to adjust the confinement effect provided by transverse reinforcement for anchorages in tension. It considers the position of the anchored bar relative to the transverse reinforcement. Whether the anchored bar is placed inside or outside the transverse reinforcement affects how the anchorage length is modified, reflecting the level of confinement and support offered by the transverse reinforcement.",
        "latexSymbol": "K",
        "latexEquation": "0.10",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G24_COMP_26"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{conplace} = Bent Anchorage",
                    "\\sym{conplace} = Partial Confinement",
                    "\\sym{conplace} = No Confinement"
                ]
            ],
            "data": [
                [
                    "0.10"
                ],
                [
                    "0.05"
                ],
                [
                    "0.00"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_28",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Transverse reinforcement ratio",
        "description": "The transverse reinforcement ratio describes the relative amount of transverse reinforcement provided along the design anchorage length. It is determined by calculating the difference between the total cross-sectional area of the transverse reinforcement and the minimum required transverse reinforcement, divided by the area of the anchored bar.",
        "latexSymbol": "\\lambda",
        "latexEquation": "\\frac{(\\sym{A_{st}} - \\sym{A_{st,min}})}{\\sym{A_{s}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_31",
            "G24_COMP_30",
            "G24_COMP_32"
        ]
    },
    {
        "id": "G24_COMP_29",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Select structure type for tension anchorage",
        "description": "For anchorages in tension, select the structure type to determine the minimum cross-sectional area of transverse reinforcement.",
        "latexSymbol": "tenstruc",
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
                    "Beam",
                    "Used for horizontal structural elements that carry loads primarily in bending."
                ],
                [
                    "Slab",
                    "Used for flat, horizontal surfaces that distribute loads over a wide area."
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_30",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Minimum cross-sectional area of transverse reinforcement",
        "description": "The minimum cross-sectional area of transverse reinforcement refers to the smallest amount of transverse reinforcement, such as ties or stirrups, required to provide adequate confinement and ensure the stability of the anchored bar.",
        "latexSymbol": "A_{st,min}",
        "latexEquation": "0.25 \\times \\sym{A_{s}}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_32",
            "G24_COMP_29"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{tenstruc} = Beam",
                    "\\sym{tenstruc} = Slab"
                ]
            ],
            "data": [
                [
                    "0.25 \\times \\sym{A_{s}}"
                ],
                [
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G24_COMP_31",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Cross-sectional area of transverse reinforcement",
        "description": "The cross-sectional area of transverse reinforcement refers to the total area of all transverse reinforcement, such as ties or stirrups, provided along the design anchorage length.",
        "latexSymbol": "A_{st}",
        "latexEquation": "\\frac{(\\pi \\times \\sym{\\phi_{t}}^{2})}{4} \\times \\sym{leg}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_17",
            "G24_COMP_33"
        ]
    },
    {
        "id": "G24_COMP_32",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.4.4(Table8.2)"
        ],
        "title": "Area of a single anchored bar",
        "description": "The area of a single anchored bar refers to the cross-sectional area of the reinforcement bar that has the maximum diameter being used in the design. This area is a critical factor in determining the required anchorage and lap lengths for the bar.",
        "latexSymbol": "A_{s}",
        "latexEquation": "\\frac{(\\pi \\times \\sym{\\phi}^{2})}{4}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G24_COMP_2"
        ]
    },
    {
        "id": "G24_COMP_33",
        "codeName": "EN1992-1-1",
        "reference": [
            "8.7.4.1(3)"
        ],
        "title": "Transverse reinforcement leg",
        "description": "In transverse reinforcement, a leg refers to the segment of a stirrup or tie that is placed parallel to the layer of reinforcement it is meant to confine. When calculating the anchorage length, these legs are considered along the design anchorage length. For lap length calculations, they are accounted for within the lap length region.",
        "latexSymbol": "leg",
        "type": "number",
        "unit": "ea",
        "notation": "standard",
        "decimal": 0,
        "default": 3.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/122881175/EN1992-1-1+Anchorage+Length
        'id': '24',
        'standardType': 'EUROCODE',
        'codeName': 'EN1992-1-1',
        'codeTitle': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Design Anchorage Length Calculation for Reinforcement Bars',
        'description': r"[EN1992-1-1] This guide provides step-by-step instructions for calculating the design anchorage length to ensure that reinforcement bars are securely anchored within concrete structures. It details how to apply various coefficients, such as those related to bar shape, concrete cover, and confinement, to determine the required length. The guide also explains how these factors influence the anchorage performance and ensure the overall safety and durability of the structure.",
        'figureFile': 'detail_content_24.png',
        'edition': '2004',
        'targetComponents': ['G24_COMP_1', 'G24_COMP_9', 'G24_COMP_10'],
        'testInput': [
            {'component': 'G14_COMP_3', 'value': 'Persistent'}, # designsitu = Persistent
            {'component': 'G14_COMP_4', 'value': 'C12/15'}, # C = C12/15
            {'component': 'G18_COMP_1', 'value': 500},
            {'component': 'G24_COMP_2', 'value': 20},
            {'component': 'G24_COMP_5', 'value': 'Good'}, # bondcon = Good
            # {'component': 'G24_COMP_5', 'value': 'Poor'}, # bondcon = Poor
            {'component': 'G24_COMP_8', 'value': 'For anchorages in tension'}, # anchcond = For anchorages in tension
            # {'component': 'G24_COMP_8', 'value': 'For anchorages in compression'}, # anchcond = For anchorages in compression
            {'component': 'G24_COMP_11', 'value': 'Straight bars'}, # barconfig = Straight bars
            # {'component': 'G24_COMP_11', 'value': 'Bent or hooked bars'}, # barconfig = Bent or hooked bars
            # {'component': 'G24_COMP_11', 'value': 'Looped bars'}, # barconfig = Looped bars
            {'component': 'G24_COMP_13', 'value': 125},
            {'component': 'G24_COMP_16', 'value': 55},
            {'component': 'G24_COMP_17', 'value': 12},
            {'component': 'G24_COMP_22', 'value': 'Welded'}, # weldtrans = Welded
            # {'component': 'G24_COMP_22', 'value': 'Not Welded'}, # weldtrans = Not Welded
            {'component': 'G24_COMP_25', 'value': 0},
            {'component': 'G24_COMP_26', 'value': 'Bent Anchorage'}, # conplace = Bent Anchorage
            # {'component': 'G24_COMP_26', 'value': 'Partial Confinement'}, # conplace = Partial Confinement
            # {'component': 'G24_COMP_26', 'value': 'No Confinement'}, # conplace = No Confinement
            {'component': 'G24_COMP_29', 'value': 'Beam'}, # tenstruc = Beam
            # {'component': 'G24_COMP_29', 'value': 'Slab'}, # tenstruc = Slab
            {'component': 'G24_COMP_33', 'value': 3},
        ],
    },
]