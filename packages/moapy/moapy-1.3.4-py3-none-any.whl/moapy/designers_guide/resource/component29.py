component_list = [
    {
        "id": "G29_COMP_1",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(2)"
        ],
        "title": "Selection of earth pressure state",
        "description": "Choose the earth pressure state to determine the appropriate calculations for the retaining wall. Selecting \"Active\" will calculate pressures when the wall moves away from the soil, while \"Passive\" will calculate pressures when the wall moves towards the soil.",
        "latexSymbol": "earthpress",
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
                    "Active",
                    "Calculates earth pressure when the retaining wall moves away from the soil, reducing pressure."
                ],
                [
                    "Passive",
                    "Calculates earth pressure when the retaining wall moves towards the soil, increasing pressure."
                ]
            ]
        }
    },
    {
        "id": "G29_COMP_2",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(C.6)"
        ],
        "title": "Coefficient of horizontal earth pressure",
        "description": "The coefficient of horizontal earth pressure calculates the lateral pressure exerted by soil on a retaining wall for both active and passive conditions. It depends on factors such as soil properties, wall inclination, and the slope of the retained surface, with different formulas used for active and passive states.",
        "latexSymbol": "K_{n}",
        "latexEquation": "\\frac{1 - \\sin(\\sym{\\phi\\prime}) \\times \\sin(2 \\times \\sym{m_{w}} - \\sym{\\phi\\prime})}{1 + \\sin(\\sym{\\phi\\prime}) \\times \\sin(2 \\times m_{t} - \\sym{\\phi\\prime})} \\times \\exp{(-2\\times \\sym{\\nu} \\times \\tan{\\sym{\\phi\\prime}})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_1",
            "G29_COMP_4",
            "G29_COMP_12",
            "G29_COMP_11",
            "G29_COMP_13"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{earthpress} = Active",
                    "\\sym{earthpress} = Passive"
                ]
            ],
            "data": [
                [
                    "\\frac{1 - \\sin(\\sym{\\phi\\prime}) \\times \\sin(2 \\times \\sym{m_{w}} - \\sym{\\phi\\prime})}{1 + \\sin(\\sym{\\phi\\prime}) \\times \\sin(2 \\times m_{t} - \\sym{\\phi\\prime})} \\times \\exp{(-2\\times \\sym{\\nu} \\times \\tan{\\sym{\\phi\\prime}})}"
                ],
                [
                    "\\frac{1 + \\sin(\\sym{\\phi\\prime}) \\times \\sin(2 \\times \\sym{m_{w}} + \\sym{\\phi\\prime})}{1 - \\sin(\\sym{\\phi\\prime}) \\times \\sin(2 \\times m_{t} + \\sym{\\phi\\prime})} \\times \\exp{(2\\times \\sym{\\nu} \\times \\tan{\\sym{\\phi\\prime}})}"
                ]
            ]
        }
    },
    {
        "id": "G29_COMP_3",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(2)"
        ],
        "title": "Angle of shearing resistance in terms of effective stress",
        "description": "The angle of shearing resistance in terms of effective stress represents the shear strength of soil calculated based on the effective stress, which is the total stress minus pore water pressure. It is a crucial parameter in geotechnical engineering used to assess soil stability and design retaining structures.",
        "latexSymbol": "\\phi",
        "type": "number",
        "unit": "degree",
        "notation": "standard",
        "decimal": 3,
        "default": 35.0,
        "limits": {
            "exMin": 0,
            "exMax": 90
        },
        "useStd": False
    },
    {
        "id": "G29_COMP_4",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(2)"
        ],
        "title": "Angle of shearing resistance in radians",
        "description": "The angle of shearing resistance in radians is used to represent the shear strength of soil in radian measure, based on effective stress. It is obtained by converting the angle from degrees to radians to facilitate calculations in certain geotechnical engineering applications.",
        "latexSymbol": "\\phi\\prime",
        "latexEquation": "\\sym{\\phi} \\times (\\frac{\\pi}{180})",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_3"
        ]
    },
    {
        "id": "G29_COMP_5",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(2)"
        ],
        "title": "Angle of shearing resistance between soil and wall",
        "description": "The angle of shearing resistance between soil and wall represents the frictional interaction angle at the interface where the soil contacts the retaining wall. It affects the amount of lateral earth pressure exerted on the wall and is a key factor in calculating earth pressure coefficients.",
        "latexSymbol": "\\delta",
        "type": "number",
        "unit": "degree",
        "notation": "standard",
        "decimal": 3,
        "default": 20.0,
        "useStd": False
    },
    {
        "id": "G29_COMP_6",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(2)"
        ],
        "title": "Angle of shearing resistance between soil and wall in radians",
        "description": "The angle of shearing resistance between soil and wall represents the frictional interaction angle at the interface where the soil contacts the retaining wall. It affects the amount of lateral earth pressure exerted on the wall and is a key factor in calculating earth pressure coefficients.",
        "latexSymbol": "\\delta\\prime",
        "latexEquation": "\\sym{\\delta} \\times (\\frac{\\pi}{180})",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_5"
        ]
    },
    {
        "id": "G29_COMP_7",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(1)"
        ],
        "title": "Slope angle of the ground behind the wall",
        "description": "The slope angle of the ground behind the wall is the angle of inclination of the soil surface located behind the retaining wall. It measures the steepness of the ground and is positive when the slope rises upward away from the wall.",
        "latexSymbol": "\\beta",
        "type": "number",
        "unit": "degree",
        "notation": "standard",
        "decimal": 3,
        "default": 15.0,
        "useStd": False
    },
    {
        "id": "G29_COMP_8",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(1)"
        ],
        "title": "Slope angle of the ground behind the wall in radians",
        "description": "The slope angle of the ground behind the wall in radians represents the inclination of the soil surface, expressed in radian measure. Converting this angle to radians is necessary for precise geotechnical calculations, especially when analyzing earth pressure.",
        "latexSymbol": "\\beta\\prime",
        "latexEquation": "\\sym{\\beta} \\times (\\frac{\\pi}{180})",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_7"
        ]
    },
    {
        "id": "G29_COMP_9",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(FigureC.4)"
        ],
        "title": "Wall inclination angle",
        "description": "The wall inclination angle is the angle between the vertical line and the direction of the wall. It is considered positive when the wall overhangs, leaning away from the soil.",
        "latexSymbol": "\\theta",
        "type": "number",
        "unit": "degree",
        "notation": "standard",
        "decimal": 3,
        "default": 10.0,
        "limits": {
            "inMin": 0,
            "exMax": 90
        },
        "useStd": False
    },
    {
        "id": "G29_COMP_10",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(FigureC.4)"
        ],
        "title": "Wall inclination angle in radians",
        "description": "The wall inclination angle in radians represents the angle between the vertical line and the wall, expressed in radian measure.",
        "latexSymbol": "\\theta\\prime",
        "latexEquation": "\\sym{\\theta} \\times (\\frac{\\pi}{180})",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_9"
        ]
    },
    {
        "id": "G29_COMP_11",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(C.3)"
        ],
        "title": "Angle from soil surface to slip line",
        "description": "The angle from the soil surface to the slip line is measured from the direction of the soil surface, pointing away from the wall, to the tangent direction of the intersecting slip line that bounds the moving soil mass. It indicates the orientation of the slip line relative to the soil surface.",
        "latexSymbol": "m_{t}",
        "latexEquation": "0.5(\\arccos(\\frac{-\\sin(\\sym{\\beta\\prime})}{-\\sin(\\sym{\\phi\\prime})}) + \\sym{\\phi\\prime} - \\sym{\\beta\\prime})",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_1",
            "G29_COMP_8",
            "G29_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{earthpress} = Active",
                    "\\sym{earthpress} = Passive"
                ]
            ],
            "data": [
                [
                    "0.5(\\arccos(\\frac{-\\sin(\\sym{\\beta\\prime})}{-\\sin(\\sym{\\phi\\prime})}) + \\sym{\\phi\\prime} - \\sym{\\beta\\prime})"
                ],
                [
                    "0.5(\\arccos(\\frac{-\\sin(\\sym{\\beta\\prime})}{\\sin(\\sym{\\phi\\prime})}) - \\sym{\\phi\\prime} - \\sym{\\beta\\prime})"
                ]
            ]
        }
    },
    {
        "id": "G29_COMP_12",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(C.4)"
        ],
        "title": "Angle from wall normal to slip line",
        "description": "The angle from the wall normal to the slip line is measured from the normal direction of the wall to the tangent direction at the wall of the exterior slip line. It is considered positive when the tangent points upwards behind the wall.",
        "latexSymbol": "m_{w}",
        "latexEquation": "0.5(\\arccos(\\frac{\\sin(\\sym{\\delta\\prime})}{\\sin(\\sym{\\phi\\prime})}) + \\sym{\\phi\\prime} + \\sym{\\delta\\prime})",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_1",
            "G29_COMP_4",
            "G29_COMP_6"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{earthpress} = Active",
                    "\\sym{earthpress} = Passive"
                ]
            ],
            "data": [
                [
                    "0.5(\\arccos(\\frac{\\sin(\\sym{\\delta\\prime})}{\\sin(\\sym{\\phi\\prime})}) + \\sym{\\phi\\prime} + \\sym{\\delta\\prime})"
                ],
                [
                    "0.5(\\arccos(\\frac{\\sin(\\sym{\\delta\\prime})}{\\sin(\\sym{\\phi\\prime})}) - \\sym{\\phi\\prime} - \\sym{\\delta\\prime})"
                ]
            ]
        }
    },
    {
        "id": "G29_COMP_13",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(C.5)"
        ],
        "title": "Total tangent rotation angle",
        "description": "The total tangent rotation angle represents the rotation along the slip line of the moving soil mass. It is calculated using the angles related to the soil surface, wall inclination, and slip line characteristics, indicating how the soil mass deforms.",
        "latexSymbol": "\\nu",
        "latexEquation": "\\sym{m_{t}} + \\sym{\\beta\\prime} - m_{w} - \\sym{\\theta\\prime}",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_11",
            "G29_COMP_8",
            "G29_COMP_12",
            "G29_COMP_10"
        ]
    },
    {
        "id": "G29_COMP_14",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(C.7)"
        ],
        "title": "Coefficient for vertical loading",
        "description": "The coefficient for vertical loading represents the influence of vertical surcharge pressure on the lateral earth pressure exerted on a retaining wall. It accounts for the effect of vertical loads on the stability and pressure distribution of the soil, and is used in geotechnical calculations to assess the impact of surface loads.",
        "latexSymbol": "K_{q}",
        "latexEquation": "\\sym{K_{n}} \\times (\\cos{\\sym{\\beta\\prime}})^{2}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_2",
            "G29_COMP_8"
        ]
    },
    {
        "id": "G29_COMP_15",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(C.8)"
        ],
        "title": "Coefficient for cohesion",
        "description": "The coefficient for cohesion represents the contribution of soil cohesion to the lateral earth pressure acting on a retaining wall. It is used in geotechnical calculations to assess the effect of cohesive forces in the soil, which can influence the stability and pressure distribution on the wall.",
        "latexSymbol": "K_{c}",
        "latexEquation": "(\\sym{K_{n}} -1) \\times \\cot{\\sym{\\phi\\prime}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_2",
            "G29_COMP_4"
        ]
    },
    {
        "id": "G29_COMP_16",
        "codeName": "EN1997-1",
        "reference": [
            "AnnexC(C.9)"
        ],
        "title": "Coefficient for soil weight",
        "description": "The coefficient for soil weight represents the effect of the soil's own weight on the lateral earth pressure exerted on a retaining wall. It is used in geotechnical calculations to account for the influence of the soil's weight on the pressure distribution and stability of the retaining structure.",
        "latexSymbol": "K_{\\gamma}",
        "latexEquation": "\\sym{K_{n}} \\times \\cos{\\sym{\\beta\\prime}} \\times \\cos{(\\sym{\\beta\\prime} - \\sym{\\theta\\prime})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G29_COMP_2",
            "G29_COMP_8",
            "G29_COMP_10"
        ]
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/116097391/EN1997-1+Earth+Pressure
        'id': '29',
        'standardType': 'EUROCODE',
        'codeName': 'EN1997-1',
        'codeTitle': 'Eurocode 7: Geotechnical design — Part 1: General rules',
        'title': 'Passive and Active Earth Pressure Calculation Using Annex C',
        'description': r"[EN1997-1] This guide provides a step-by-step procedure for calculating passive and active earth pressures based on the numerical method described in Annex C of Eurocode 1997-1. It includes instructions on applying the formulas for different conditions, such as varying soil properties, wall inclinations, and slope angles, to determine earth pressure coefficients accurately. Although the design standards provide formulas and graphs for calculating these values, discrepancies can occur between the values calculated using the formulas and those obtained from the graphs. For instance, while the results are similar for the condition where β = 0, they do not exactly match. Under other conditions, the calculated values may further diverge from the graph values, making it necessary for engineers to use their judgment in selecting the appropriate values for design purposes.",
        'edition': '2004',
        'figureFile': 'detail_content_29.png',
        'targetComponents': ['G29_COMP_2', 'G29_COMP_14', 'G29_COMP_15', 'G29_COMP_16'],
        'testInput': [
            {'component': 'G29_COMP_1', 'value': 'Active'},
            {'component': 'G29_COMP_3', 'value': 35},
            {'component': 'G29_COMP_5', 'value': 20},
            {'component': 'G29_COMP_7', 'value': 15},
            {'component': 'G29_COMP_9', 'value': 10},
        ],
    }
]
