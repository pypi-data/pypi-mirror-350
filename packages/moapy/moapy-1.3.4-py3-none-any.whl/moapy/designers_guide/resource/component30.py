component_list = [
    {
        "id": "G30_COMP_1",
        "codeName": "EN1997-1",
        "reference": [
            "2.4.7.3.4.1(1)P"
        ],
        "title": "Design approach selection",
        "description": "The appropriate design approach for geotechnical calculations is selected. Each approach applies different combinations of partial factors to actions, ground strength parameters, and resistances, affecting the verification process for ultimate limit states.",
        "latexSymbol": "deappro",
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
                    "Design Approach 1",
                    "Combination: A1+ M1 + R1"
                ],
                [
                    "Design Approach 2",
                    "Combination: A1 + M1 + R2"
                ],
                [
                    "Design Approach 3",
                    "Combination: A1 + M2 + R3"
                ]
            ]
        }
    },
    {
        "id": "G30_COMP_2",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexA(TableA.3)"
        ],
        "title": "Partial factor for unfavourable permanent actions",
        "description": "This term represents the partial factor applied specifically to unfavourable permanent actions, which increase the risk to the structure. It is used to adjust the design values of permanent loads, accounting for uncertainties by increasing the magnitude of these actions to ensure a conservative safety approach.",
        "latexSymbol": "\\gamma_{G}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "default": 1.35,
        "const": True
    },
    {
        "id": "G30_COMP_3",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexA(TableA.4)"
        ],
        "title": "Partial factor for undrained shear strength",
        "description": "This term represents the partial factor applied to the undrained shear strength of the soil. It is used in design calculations to account for uncertainties and variability in the undrained shear strength, ensuring a conservative and safe assessment of the soil's resistance under undrained conditions.",
        "latexSymbol": "\\gamma_{cu}",
        "latexEquation": "1.00",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{deappro} = Design Approach 1",
                    "\\sym{deappro} = Design Approach 2",
                    "\\sym{deappro} = Design Approach 3"
                ]
            ],
            "data": [
                [
                    "1.00"
                ],
                [
                    "1.00"
                ],
                [
                    "1.40"
                ]
            ]
        }
    },
    {
        "id": "G30_COMP_4",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexA(TableA.4)"
        ],
        "title": "Partial factor for weight density",
        "description": "This term represents the partial factor applied to the undrained shear strength of the soil. It is used in design calculations to account for uncertainties and variability in the undrained shear strength, ensuring a conservative and safe assessment of the soil's resistance under undrained conditions.",
        "latexSymbol": "\\gamma_{\\gamma}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G30_COMP_5",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexA(TableA.5)"
        ],
        "title": "Partial factor for bearing resistance",
        "description": "This term represents the partial factor applied to the bearing resistance of the foundation. It is used in design calculations to account for uncertainties in the estimated bearing capacity, ensuring a conservative approach to safety by adjusting the resistance values to reflect potential variations in soil or foundation conditions.",
        "latexSymbol": "\\gamma_{R;v}",
        "latexEquation": "1.00",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{deappro} = Design Approach 1",
                    "\\sym{deappro} = Design Approach 2",
                    "\\sym{deappro} = Design Approach 3"
                ]
            ],
            "data": [
                [
                    "1.00"
                ],
                [
                    "1.40"
                ],
                [
                    "1.00"
                ]
            ]
        }
    },
    {
        "id": "G30_COMP_6",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Foundation width",
        "description": "This term represents the actual width of the foundation, measured perpendicular to the length direction. It is used as a base dimension for calculating the effective width.",
        "latexSymbol": "B",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "default": 2.5,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G30_COMP_7",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Effective foundation width",
        "description": "This term represents the effective width of the foundation, adjusted for factors such as eccentricity and load distribution. It is used in calculating the shape factor and other parameters that influence the bearing resistance.",
        "latexSymbol": "B\\prime",
        "latexEquation": "\\sym{B} - 2 \\times \\sym{e_{B}}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_6",
            "G30_COMP_8"
        ]
    },
    {
        "id": "G30_COMP_8",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Eccentricity in width direction",
        "description": "This term represents the eccentricity of the applied load in the width direction, indicating how far the load is offset from the center of the foundation.",
        "latexSymbol": "e_{B}",
        "latexEquation": "\\frac{\\sym{M_{B}}}{\\sym{V}}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_21",
            "G30_COMP_19"
        ]
    },
    {
        "id": "G30_COMP_9",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Foundation length",
        "description": "This term represents the actual length of the foundation, measured along the longest side. It serves as the base dimension for calculating the effective length.",
        "latexSymbol": "L",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "default": 3.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G30_COMP_10",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Effective foundation length",
        "description": "This term represents the effective length of the foundation, accounting for adjustments due to factors like load distribution and eccentricity. It is a key parameter in determining the shape factor and overall bearing capacity.",
        "latexSymbol": "L\\prime",
        "latexEquation": "\\sym{L} - 2 \\times \\sym{e_{L}}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_9",
            "G30_COMP_11"
        ]
    },
    {
        "id": "G30_COMP_11",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Eccentricity in length direction",
        "description": "This term represents the eccentricity of the applied load in the length direction, showing the extent to which the load is offset from the center along the length of the foundation.",
        "latexSymbol": "e_{L}",
        "latexEquation": "\\frac{\\sym{M_{L}}}{\\sym{V}}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_22",
            "G30_COMP_19"
        ]
    },
    {
        "id": "G30_COMP_12",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(1)"
        ],
        "title": "Design effective foundation area",
        "description": "This term represents the effective foundation area, which is the adjusted area of the foundation that takes into account factors such as eccentricity and load distribution. It is used in bearing resistance calculations to reflect the portion of the foundation that effectively resists applied loads.",
        "latexSymbol": "A\\prime",
        "latexEquation": "\\sym{B\\prime} \\times \\sym{L\\prime}",
        "type": "number",
        "unit": "m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_7",
            "G30_COMP_10"
        ]
    },
    {
        "id": "G30_COMP_13",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Height of the foundation",
        "description": "This term represents the thickness of the overburden, which is the soil layer above the foundation.",
        "latexSymbol": "h_{1}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "default": 1.5,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G30_COMP_14",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Thickness of the overburden",
        "description": "This term represents the thickness of the overburden, which is the soil layer above the foundation. It is relevant when the foundation is fully embedded in the soil, indicating the depth of the material exerting pressure on the foundation.",
        "latexSymbol": "h_{2}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "default": 0.5,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G30_COMP_15",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Embedment depth of the foundation",
        "description": "This term represents the embedment depth of the foundation, calculated as the sum of the foundation height and the thickness of the overburden. It indicates the total depth from the surface to the base of the foundation, affecting the calculation of overburden pressure.",
        "latexSymbol": "D",
        "latexEquation": "\\sym{h_{1}} + \\sym{h_{2}}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_13",
            "G30_COMP_14"
        ]
    },
    {
        "id": "G30_COMP_16",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Inclination of the foundation base",
        "description": "This term represents the angle of inclination of the foundation base relative to the horizontal plane. It influences the bearing resistance calculation by accounting for how the foundation's slope affects the distribution of loads and the overall stability.",
        "latexSymbol": "\\alpha",
        "type": "number",
        "unit": "degree",
        "notation": "standard",
        "decimal": 3,
        "default": 0.0,
        "limits": {
            "inMin": 0,
            "inMax": 90
        },
        "useStd": False
    },
    {
        "id": "G30_COMP_17",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(1)"
        ],
        "title": "Weight density of overburden soil",
        "description": "This term represents the weight density of the soil, which is the weight per unit volume of the soil material. It influences the calculation of overburden pressure and is a key factor in determining the bearing capacity of the foundation. Detailed values can be found in EN1991-1-1 Annex A, Table A.6.",
        "latexSymbol": "\\gamma",
        "type": "number",
        "unit": "kN/m^3",
        "notation": "standard",
        "decimal": 3,
        "default": 15.0,
        "limits": {
            "exMin": 0
        },
        "useStd": True
    },
    {
        "id": "G30_COMP_18",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(1)"
        ],
        "title": "Weight density of concrete",
        "description": "This term represents the weight density of the concrete used in the foundation, which is the weight per unit volume of the concrete material. It is used in calculations to account for the self-weight of the foundation. Detailed values can be found in EN1991-1-1 Annex A, Table A.1.",
        "latexSymbol": "\\gamma_{c}",
        "type": "number",
        "unit": "kN/m^3",
        "notation": "standard",
        "decimal": 3,
        "default": 25.0,
        "limits": {
            "exMin": 0
        },
        "useStd": True
    },
    {
        "id": "G30_COMP_19",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(1)"
        ],
        "title": "Vertical load at center of foundation",
        "description": "This term represents the vertical load acting at the center of the foundation. It accounts for the downward force from the structure's weight and other applied loads, typically considered to act at the foundation's center.",
        "latexSymbol": "V",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "default": 500.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G30_COMP_20",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(3)"
        ],
        "title": "Horizontal load at center of foundation",
        "description": "his term represents the horizontal load acting at the center of the foundation. It reflects the forces applied laterally to the foundation, typically assumed to act at the foundation's center.",
        "latexSymbol": "H",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "default": 0.0,
        "useStd": False
    },
    {
        "id": "G30_COMP_21",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Width direction moment acting at center of foundation",
        "description": "This term represents the moment in the width direction acting at the center of the foundation. It is caused by forces that generate rotational effects around the width of the foundation.",
        "latexSymbol": "M_{B}",
        "type": "number",
        "unit": "kN.m",
        "notation": "standard",
        "decimal": 3,
        "default": 0.0,
        "useStd": False
    },
    {
        "id": "G30_COMP_22",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Length direction moment acting at center of foundation",
        "description": "This term represents the moment in the length direction acting at the center of the foundation. It results from forces that induce rotational effects along the length of the foundation.",
        "latexSymbol": "M_{L}",
        "type": "number",
        "unit": "kN.m",
        "notation": "standard",
        "decimal": 3,
        "default": 0.0,
        "useStd": False
    },
    {
        "id": "G30_COMP_23",
        "codeName": "EN1997-1",
        "reference": [
            "6.5.2.1(1)P"
        ],
        "title": "Design value of applied vertical load",
        "description": "This term represents the design value of the vertical load applied to the foundation. It includes the vertical load acting on the foundation, the self-weight of the foundation, and the weight of the soil above the foundation. The design bearing resistance should be greater than the design value of the vertical load to ensure safety.",
        "latexSymbol": "V_{d}",
        "latexEquation": "\\sym{\\gamma_{G}} \\times (V + \\sym{\\gamma_{c}} \\times \\sym{A\\prime} \\times \\sym{h_{1}} + \\sym{\\gamma} \\times \\sym{A\\prime} \\times \\sym{h_{2}})",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_2",
            "G30_COMP_19",
            "G30_COMP_18",
            "G30_COMP_12",
            "G30_COMP_13",
            "G30_COMP_17",
            "G30_COMP_14"
        ]
    },
    {
        "id": "G30_COMP_24",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(D.1)"
        ],
        "title": "Bearing resistance per unit area",
        "description": "This term represents the design bearing resistance per unit area of the foundation. It is used to assess the ability of the soil to support the applied loads, considering various factors such as soil strength, foundation shape, and loading conditions.",
        "latexSymbol": "{R/A\\prime}",
        "latexEquation": "(\\pi+2) \\times (\\frac{\\sym{c_{u}}}{\\sym{\\gamma_{cu}}}) \\times \\sym{b_{c}} \\times \\sym{s_{c}} \\times \\sym{i_{c}} + \\sym{q}",
        "type": "number",
        "unit": "kPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_28",
            "G30_COMP_3",
            "G30_COMP_26",
            "G30_COMP_29",
            "G30_COMP_30",
            "G30_COMP_27"
        ]
    },
    {
        "id": "G30_COMP_25",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(D.1)"
        ],
        "title": "Design bearing resistance",
        "description": "This term represents the design bearing resistance of a foundation, calculated to ensure the foundation can safely support the applied loads without failure. It is determined using factors such as undrained shear strength, shape factors, load inclination, and effective foundation area.",
        "latexSymbol": "R_{d}",
        "latexEquation": "\\frac{(\\sym{{R/A\\prime}} \\times \\sym{A\\prime})}{\\sym{\\gamma_{R;v}}}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_24",
            "G30_COMP_12",
            "G30_COMP_5"
        ]
    },
    {
        "id": "G30_COMP_26",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(3)"
        ],
        "title": "Base inclination factor",
        "description": "This term represents the base inclination factor, which accounts for the effect of the foundation base's inclination on the bearing resistance. It adjusts the bearing capacity calculation to reflect the influence of the angle between the foundation base and the horizontal plane.",
        "latexSymbol": "b_{c}",
        "latexEquation": "1 - \\frac{2 \\times (\\sym{\\alpha} \\times (\\frac{\\pi}{180}))}{(\\pi + 2)}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_16"
        ]
    },
    {
        "id": "G30_COMP_27",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(FigureD.1)"
        ],
        "title": "Overburden or surcharge pressure",
        "description": "This term represents the overburden or surcharge pressure at the level of the foundation base. It accounts for the weight of the soil and any additional loads above the foundation, influencing the bearing resistance and stability of the foundation.",
        "latexSymbol": "q",
        "latexEquation": "\\sym{D} \\times (\\frac{\\sym{\\gamma}}{\\sym{\\gamma_{\\gamma}}})",
        "type": "number",
        "unit": "kPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_15",
            "G30_COMP_17",
            "G30_COMP_4"
        ]
    },
    {
        "id": "G30_COMP_28",
        "codeName": "EN1997-1",
        "reference": [
            "3.3.10.3(2)"
        ],
        "title": "Undrained shear strength",
        "description": "This term represents the undrained shear strength of the soil, which measures the soil's resistance to shear deformation under conditions where pore water pressure does not dissipate. It is a key parameter in assessing the stability of soil under short-term loading conditions, particularly in saturated clay.",
        "latexSymbol": "c_{u}",
        "type": "number",
        "unit": "kPa",
        "notation": "standard",
        "decimal": 3,
        "default": 30.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G30_COMP_29",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(3)"
        ],
        "title": "Shape factor of the foundation",
        "description": "This term represents the shape factor of the foundation, which accounts for the influence of the foundation's shape on the bearing resistance. The factor varies depending on whether the foundation is rectangular or square with specific adjustments made to reflect how the shape affects load distribution.",
        "latexSymbol": "s_{c}",
        "latexEquation": "1+ 0.2 \\times (\\frac{\\sym{B\\prime}}{\\sym{L\\prime}})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_7",
            "G30_COMP_10"
        ]
    },
    {
        "id": "G30_COMP_30",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexD(3)"
        ],
        "title": "Load inclination factor",
        "description": "This term represents the load inclination factor, which accounts for the effect of a horizontal load on the bearing resistance. It adjusts the calculation to reflect how the inclination of the applied load influences the stability and performance of the foundation.",
        "latexSymbol": "i_{c}",
        "latexEquation": "\\frac{1}{2} \\times (1 + \\sqrt{(1 - \\frac{H}{\\sym{A\\prime} \\times \\sym{c_{u}}})})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G30_COMP_20",
            "G30_COMP_12",
            "G30_COMP_28"
        ]
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/117047351/EN1997-1+Bearing+Resistance
        'id': '30',
        'standardType': 'EUROCODE',
        'codeName': 'EN1997-1',
        'codeTitle': 'Eurocode 7: Geotechnical design — Part 1: General rules',
        'title': 'Bearing Resistance Calculation of Foundations under Undrained Conditions',
        'description': r"[EN1997-1] This guide provides step-by-step instructions for calculating the bearing resistance of foundation structures under undrained conditions. Bearing resistance is the ability of the soil beneath a foundation to support the applied loads without undergoing shear failure. Calculating this is essential for ensuring that the foundation can safely transfer structural loads to the ground. The guide includes calculations for Ultimate Limit States using three different design approaches, each with specific partial factors applied to structural and geotechnical limit states.",
        'edition': '2004',
        'figureFile': 'detail_content_30.png',
        'targetComponents': ['G30_COMP_23', 'G30_COMP_24', 'G30_COMP_25'],
        'testInput': [
            {'component': 'G30_COMP_1', 'value': 'Design Approach 1'},
            {'component': 'G30_COMP_6', 'value': 2.5},
            {'component': 'G30_COMP_9', 'value': 3},
            {'component': 'G30_COMP_13', 'value': 1.5},
            {'component': 'G30_COMP_14', 'value': 0.5},
            {'component': 'G30_COMP_16', 'value': 0},
            {'component': 'G30_COMP_17', 'value': 15.0},
            {'component': 'G30_COMP_18', 'value': 25.0},
            {'component': 'G30_COMP_19', 'value': 500},
            {'component': 'G30_COMP_20', 'value': 0},
            {'component': 'G30_COMP_21', 'value': 0},
            {'component': 'G30_COMP_22', 'value': 0},
            {'component': 'G30_COMP_28', 'value': 30},
        ],
    }
]
