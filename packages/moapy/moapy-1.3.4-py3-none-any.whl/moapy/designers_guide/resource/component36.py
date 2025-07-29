component_list = [
    {
        "id": "G36_COMP_1",
        "codeName": "EN1998-5",
        "reference": [
            "7.3.2.2(7.1)"
        ],
        "title": "Horizontal seismic coefficient",
        "description": "The horizontal seismic coefficient represents the ratio of horizontal seismic acceleration to gravity, used in seismic design for pseudo-static analysis. It reflects the intensity of horizontal seismic forces acting on a structure and is a key parameter in calculating the forces exerted on retaining walls during an earthquake.",
        "latexSymbol": "k_{h}",
        "latexEquation": "\\sym{\\alpha} \\times (\\frac{\\sym{S}}{\\sym{r}})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G36_COMP_3",
            "G31_COMP_10",
            "G36_COMP_2"
        ]
    },
    {
        "id": "G36_COMP_2",
        "codeName": "EN1998-5",
        "reference": [
            "7.3.2.2(Table7.1)"
        ],
        "title": "Factor for horizontal seismic coefficient",
        "description": "The factor for the horizontal seismic coefficient is used to adjust seismic force calculations for retaining structures. When the retaining structure is a flexural reinforced concrete wall, anchored or braced wall, reinforced concrete wall on vertical piles, restrained basement wall, or bridge abutment, the factor is set to one, indicating no reduction in seismic forces.",
        "latexSymbol": "r",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G36_COMP_3",
        "codeName": "EN1998-5",
        "reference": [
            "4.1.3.3(5)P)"
        ],
        "title": "Ratio of design ground acceleration",
        "description": "The ratio of design ground acceleration represents the relationship between the design ground acceleration on type A ground and the acceleration due to gravity. It is used in seismic design to quantify the intensity of ground shaking relative to gravity.",
        "latexSymbol": "\\alpha",
        "latexEquation": "\\frac{\\sym{a_{g}}}{\\sym{g}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_5",
            "G4_COMP_2"
        ]
    },
    {
        "id": "G36_COMP_4",
        "codeName": "EN1998-5",
        "reference": [
            "7.3.2.2(4)P"
        ],
        "title": "Vertical seismic coefficient",
        "description": "The vertical seismic coefficient represents the ratio of vertical seismic acceleration to gravity, used in pseudo-static analysis for seismic design. It accounts for the vertical component of seismic forces that can act in both upward and downward directions, influencing the forces on the retaining structure.",
        "latexSymbol": "k_{v}",
        "latexEquation": "0.5 \\times \\sym{k_{h}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_6",
            "G36_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{spectype} = Type 1 (For large earthquakes)",
                    "\\sym{spectype} = Type 2 (For smaller earthquakes)"
                ]
            ],
            "data": [
                [
                    "0.5 \\times \\sym{k_{h}}"
                ],
                [
                    "0.33 \\times \\sym{k_{h}}"
                ]
            ]
        }
    },
    {
        "id": "G36_COMP_5",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(5)"
        ],
        "title": "Selection for vertical seismic force direction",
        "description": "This selection distinguishes whether the vertical seismic force acts in the same direction as gravity (upward) or in the opposite direction (downward). The differentiation between upward and downward forces affects the response of the soil-wall system during seismic events, requiring different calculations.",
        "latexSymbol": "seisdirect",
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
                    "Upward vertical force",
                    "Vertical seismic force acts in the same direction as gravity."
                ],
                [
                    "Downward vertical force",
                    "Vertical seismic force acts in the opposite direction to gravity."
                ]
            ]
        }
    },
    {
        "id": "G36_COMP_6",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(5)"
        ],
        "title": "Seismic adjustment angle for downward vertical force",
        "description": "The seismic adjustment angle modifies the soil-wall system's response based on the direction of the vertical seismic force, using different calculations for upward and downward forces depending on whether they act with or against gravity.",
        "latexSymbol": "\\theta",
        "latexEquation": "\\arctan{(\\frac{\\sym{k_{h}}}{1 + \\sym{k_{v}}})}",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G36_COMP_5",
            "G36_COMP_1",
            "G36_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{seisdirect} = Upward vertical force",
                    "\\sym{seisdirect} = Downward vertical force"
                ]
            ],
            "data": [
                [
                    "\\arctan{(\\frac{\\sym{k_{h}}}{1 + \\sym{k_{v}}})}"
                ],
                [
                    "\\arctan{(\\frac{\\sym{k_{h}}}{1 - \\sym{k_{v}}})}"
                ]
            ]
        }
    },
    {
        "id": "G36_COMP_7",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(4)"
        ],
        "title": "Seismic earth pressure coefficient in active state",
        "description": "The seismic earth pressure coefficient in the active state represents the ratio of horizontal to vertical stress in the soil when the retaining wall is moving away from the backfill, resulting in a decrease in seismic earth pressure.",
        "latexSymbol": "K_{a}",
        "latexEquation": "\\frac{\\sin^{2}(\\sym{\\psi_{d}} + \\sym{\\phi\\prime_{d}} - \\sym{\\theta})}{\\cos(\\sym{\\theta}) \\sin^{2}(\\sym{\\psi_{d}}) \\sin(\\sym{\\psi_{d}} - \\sym{\\theta} - \\sym{\\delta_{d}}) (1+\\sqrt{\\frac{\\sin(\\sym{\\phi\\prime_{d}} + \\sym{\\delta_{d}}) \\sin(\\sym{\\phi\\prime_{d}} - \\sym{\\beta_{d}} - \\theta)}{\\sin(\\psi_{d} - \\sym{\\theta} - \\sym{\\delta_{d}}) \\sin(\\psi_{d} + \\sym{\\beta_{d}})} })^{2}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G36_COMP_9",
            "G36_COMP_13",
            "G36_COMP_6",
            "G36_COMP_17",
            "G36_COMP_15"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{\\beta_{d}} <= \\sym{\\phi\\prime_{d}} - \\sym{\\theta}",
                    "\\sym{\\beta_{d}} > \\sym{\\phi\\prime_{d}} - \\sym{\\theta}"
                ]
            ],
            "data": [
                [
                    "\\frac{\\sin^{2}(\\sym{\\psi_{d}} + \\sym{\\phi\\prime_{d}} - \\sym{\\theta})}{\\cos(\\sym{\\theta}) \\sin^{2}(\\sym{\\psi_{d}}) \\sin(\\sym{\\psi_{d}} - \\sym{\\theta} - \\sym{\\delta_{d}}) (1+\\sqrt{\\frac{\\sin(\\sym{\\phi\\prime_{d}} + \\sym{\\delta_{d}}) \\sin(\\sym{\\phi\\prime_{d}} - \\sym{\\beta_{d}} - \\theta)}{\\sin(\\psi_{d} - \\sym{\\theta} - \\sym{\\delta_{d}}) \\sin(\\psi_{d} + \\sym{\\beta_{d}})} })^{2}}"
                ],
                [
                    "\\frac{\\sin^{2}(\\sym{\\psi_{d}} + \\sym{\\phi\\prime_{d}} - \\sym{\\theta})}{\\cos(\\sym{\\theta}) \\sin^{2}(\\sym{\\psi_{d}}) \\sin(\\sym{\\psi_{d}} - \\sym{\\theta} - \\sym{\\delta_{d}})}"
                ]
            ]
        }
    },
    {
        "id": "G36_COMP_8",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(E.4)"
        ],
        "title": "Seismic earth pressure coefficient in passive state",
        "description": "The seismic earth pressure coefficient in the passive state represents the ratio of horizontal to vertical stress in the soil when the retaining wall is moving toward the backfill, causing an increase in seismic earth pressure.",
        "latexSymbol": "K_{p}",
        "latexEquation": "\\frac{\\sin^{2}(\\sym{\\psi_{d}} + \\sym{\\phi\\prime_{d}} - \\sym{\\theta})}{\\cos(\\sym{\\theta}) \\sin^{2}(\\sym{\\psi_{d}}) \\sin(\\sym{\\psi_{d}} + \\sym{\\theta}) (1 - \\sqrt{ \\frac{ \\sin(\\sym{\\phi\\prime_{d}}) \\sin(\\sym{\\phi\\prime_{d}} + \\sym{\\beta_{d}} - \\theta)}{\\sin(\\psi_{d} + \\sym{\\beta_{d}}) \\sin(\\sym{\\psi_{d}} + \\sym{\\theta})}})^{2}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G36_COMP_9",
            "G36_COMP_13",
            "G36_COMP_6",
            "G36_COMP_15"
        ]
    },
    {
        "id": "G36_COMP_9",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(4)"
        ],
        "title": "Design angle of shearing resistance of soil",
        "description": "The design angle of shearing resistance of soil is a parameter representing the soil's resistance to shearing forces. It is calculated considering the soil's internal friction and is used to assess the stability and earth pressure on retaining structures.",
        "latexSymbol": "\\phi\\prime_{d}",
        "latexEquation": "\\arctan(\\frac{\\tan(\\sym{\\phi\\prime} \\times \\frac{\\pi}{180})}{ \\sym{\\gamma\\prime_{\\phi}}})",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G36_COMP_10",
            "G36_COMP_11"
        ]
    },
    {
        "id": "G36_COMP_10",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(4)"
        ],
        "title": "Angle of shearing resistance in terms of effective stress",
        "description": "The angle of shearing resistance in terms of effective stress represents the soil's resistance to shear under effective stress conditions. It reflects the frictional strength of the soil when considering the stress carried by the soil particles, excluding pore water pressure.",
        "latexSymbol": "\\phi\\prime",
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
        "id": "G36_COMP_11",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(4)"
        ],
        "title": "Partial factor for shearing resistance angle",
        "description": "The partial factor for the shearing resistance angle is used to account for uncertainties in the soil's shear strength parameters during design. It ensures a safety margin by adjusting the calculated values of the shearing resistance angle. More details can be found in EN 1997-1 Annex A.",
        "latexSymbol": "\\gamma\\prime_{\\phi}",
        "type": "string",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "default": "1.00",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "1.00",
                    "Applied for structural (STR) and geotechnical (GEO) limit state M1 verifications, reflecting a lower safety margin for cases where conditions are better understood or less critical."
                ],
                [
                    "1.25",
                    "Used for verifications of equilibrium limit state (EQU), structural (STR) and geotechnical (GEO) limit state M2, and uplift limit state (UPL), providing a higher safety margin to account for uncertainties in these critical conditions."
                ]
            ]
        }
    },
    {
        "id": "G36_COMP_12",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(FigureE.1)"
        ],
        "title": "Inclination angle of the back face of the wall",
        "description": "The inclination angle of the back face of the wall refers to the angle between the back face of the wall and the horizontal line. This angle influences how earth pressure is distributed on the retaining structure.",
        "latexSymbol": "\\psi",
        "type": "number",
        "unit": "degree",
        "notation": "standard",
        "decimal": 3,
        "default": 90.0,
        "limits": {
            "exMin": 0,
            "exMax": 180
        },
        "useStd": True
    },
    {
        "id": "G36_COMP_13",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(FigureE.1)"
        ],
        "title": "Design inclination angle of the back face of the wall",
        "description": "The design inclination angle of the back face of the wall is the converted value of the inclination angle from degrees to radians for calculation purposes. The converted value is used in calculating the seismic earth pressure coefficient.",
        "latexSymbol": "\\psi_{d}",
        "latexEquation": "\\sym{\\psi} \\times (\\frac{\\pi}{180})",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G36_COMP_12"
        ]
    },
    {
        "id": "G36_COMP_14",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(FigureE.1)"
        ],
        "title": "Inclination angle of the backfill surface",
        "description": "The backfill slope angle refers to the angle between the horizontal ground and the slope of the backfill material behind the retaining wall. It influences the earth pressure acting on the wall, depending on how steep the backfill is.",
        "latexSymbol": "\\beta",
        "type": "number",
        "unit": "degree",
        "notation": "standard",
        "decimal": 3,
        "default": 0.0,
        "limits": {
            "inMin": -180,
            "inMax": 180
        },
        "useStd": True
    },
    {
        "id": "G36_COMP_15",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(FigureE.1)"
        ],
        "title": "Design inclination angle of the backfill surface",
        "description": "The design inclination angle of the backfill surface is the converted value of the backfill slope angle from degrees to radians for calculation purposes. The converted value is used in determining the earth pressure acting on the retaining wall.",
        "latexSymbol": "\\beta_{d}",
        "latexEquation": "\\sym{\\beta} \\times (\\frac{\\pi}{180})",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G36_COMP_14"
        ]
    },
    {
        "id": "G36_COMP_16",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(FigureE.1)"
        ],
        "title": "Friction angle between soil and wall",
        "description": "The friction angle between the soil and the wall represents the angle of shearing resistance along the interface between the backfill soil and the retaining wall. It reflects the degree of frictional interaction, influencing the magnitude of earth pressure exerted on the wall.",
        "latexSymbol": "\\delta",
        "type": "number",
        "unit": "degree",
        "notation": "standard",
        "decimal": 3,
        "default": 0.0,
        "limits": {
            "inMin": 0,
            "exMax": 90
        },
        "useStd": True
    },
    {
        "id": "G36_COMP_17",
        "codeName": "EN1998-5",
        "reference": [
            "AnnexE(4)"
        ],
        "title": "Design friction angle between soil and wall",
        "description": "The design friction angle between the soil and the wall is an adjusted value used for safety in engineering calculations. It accounts for uncertainties in the frictional properties between the backfill soil and the retaining structure, helping ensure a more conservative design.",
        "latexSymbol": "\\delta_{d}",
        "latexEquation": "\\arctan(\\frac{\\tan(\\sym{\\delta} \\times \\frac{\\pi}{180})}{ \\sym{\\gamma\\prime_{\\phi}}})",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G36_COMP_16",
            "G36_COMP_11"
        ]
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/113541829/EN1998-5+Mononobe-Okabe+Formula
        'id': '36',
        'standardType': 'EUROCODE',
        'codeName': 'EN1998-5',
        'codeTitle': 'Eurocode 8 — Design of structures for earthquake resistance — Part 5: Foundations, retaining structures and geotechnical aspects',
        'title': 'Seismic Earth Pressure Coefficient Using Mononobe-Okabe Formula',
        'description': r"[EN1998-5] This guide provides detailed steps for calculating the earth pressure coefficient for retaining structures using the Mononobe-Okabe formula, excluding water table effects. It includes methods for both active and passive earth pressure states, explaining how to incorporate factors such as soil friction angle, wall and backfill inclination, and seismic coefficients. By following this guide, users can accurately assess earth pressures under seismic conditions, ensuring the stability and safety of retaining structures.",
        'edition': '2004',
        'figureFile': 'detail_content_36.png',
        'targetComponents': ['G36_COMP_7', 'G36_COMP_8'],
        'testInput': [
            {'component': 'G31_COMP_1', 'value': 'A'},
            {'component': 'G31_COMP_2', 'value': 2.35},
            {'component': 'G31_COMP_3', 'value': 'Class I'},
            {'component': 'G31_COMP_6', 'value': 'Type 1 (For large earthquakes)'},
            {'component': 'G36_COMP_5', 'value': 'Upward vertical force'},
            {'component': 'G36_COMP_10', 'value': 35},
            {'component': 'G36_COMP_11', 'value': '1.00'},
            {'component': 'G36_COMP_12', 'value': 90},
            {'component': 'G36_COMP_14', 'value': 0},
            {'component': 'G36_COMP_16', 'value': 0},
        ],
    }
]
