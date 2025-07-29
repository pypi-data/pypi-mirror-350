component_list = [
    {
        "id": "G32_COMP_1",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.3(Table3.4)"
        ],
        "title": "Design ground acceleration for vertical response spectrum",
        "description": "The vertical design ground acceleration is used to calculate the seismic forces acting in the vertical direction on structures during an earthquake. For Type 1 spectra, the vertical design ground acceleration is typically 90% of the horizontal design ground acceleration. For Type 2 spectra, it is calculated as 45% of the horizontal design ground acceleration.",
        "latexSymbol": "a_{vg}",
        "latexEquation": "0.9 \\times \\sym{a_{g}}",
        "type": "number",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_5",
            "G31_COMP_6"
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
                    "0.9 \\times \\sym{a_{g}}"
                ],
                [
                    "0.45 \\times \\sym{a_{g}}"
                ]
            ]
        }
    },
    {
        "id": "G32_COMP_2",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.3(Table3.4)"
        ],
        "title": "Lower bound of constant spectral acceleration period",
        "description": "This represents the lower limit of the period in the vertical elastic response spectrum. It defines the point at which the spectral acceleration starts to stabilize in the initial phase of the response spectrum.",
        "latexSymbol": "T_{B,V}",
        "latexEquation": "0.05",
        "type": "number",
        "unit": "s",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G31_COMP_6"
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
                    "0.05"
                ],
                [
                    "0.05"
                ]
            ]
        }
    },
    {
        "id": "G32_COMP_3",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.3(Table3.4)"
        ],
        "title": "Upper bound of constant spectral acceleration period",
        "description": "This represents the upper limit of the constant spectral acceleration period in the vertical elastic response spectrum. It marks the point where the spectral acceleration starts to decrease after remaining constant.",
        "latexSymbol": "T_{C,V}",
        "latexEquation": "0.15",
        "type": "number",
        "unit": "s",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G31_COMP_6"
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
                    "0.15"
                ],
                [
                    "0.15"
                ]
            ]
        }
    },
    {
        "id": "G32_COMP_4",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.3(Table3.4)"
        ],
        "title": "Period defining the start of the constant displacement response",
        "description": "This defines the beginning of the constant displacement response period in the vertical elastic response spectrum, where the spectral acceleration decreases as the displacement becomes constant.",
        "latexSymbol": "T_{D,V}",
        "latexEquation": "1.00",
        "type": "number",
        "unit": "s",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G31_COMP_6"
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
                    "1.00"
                ],
                [
                    "1.00"
                ]
            ]
        }
    },
    {
        "id": "G32_COMP_5",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.3(1)P"
        ],
        "title": "Vertical elastic response spectrum",
        "description": "The vertical elastic response spectrum represents the seismic response of a structure in the vertical direction as a function of its natural vibration period. This spectrum is used to calculate the vertical forces that act on a structure during an earthquake. It accounts for the vertical component of the seismic action and is typically smaller than the horizontal response spectrum.",
        "latexSymbol": "S_{ve}(T)",
        "latexEquation": "\\sym{a_{vg}} \\times (1 + \\frac{\\sym{T_{V}}}{\\sym{T_{B,V}}} \\times ( \\sym{\\eta} \\times 3 - 1))",
        "type": "number",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G32_COMP_8",
            "G32_COMP_9",
            "G32_COMP_2",
            "G32_COMP_3",
            "G32_COMP_4",
            "G32_COMP_1",
            "G31_COMP_12"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{T_{V,type}} = Start point(0.0s)",
                    "\\sym{T_{V,type}} = Lower limit",
                    "\\sym{T_{V,type}} = Upper limit",
                    "\\sym{T_{V,type}} = Constant range",
                    "\\sym{T_{V,type}} = End point(4.0s)"
                ]
            ],
            "data": [
                [
                    "\\sym{a_{vg}} \\times (1 + \\frac{\\sym{T_{V}}}{\\sym{T_{B,V}}} \\times ( \\sym{\\eta} \\times 3 - 1))"
                ],
                [
                    "\\sym{a_{vg}} \\times (1 + \\frac{\\sym{T_{V}}}{\\sym{T_{B,V}}} \\times ( \\sym{\\eta} \\times 3 - 1))"
                ],
                [
                    "\\sym{a_{vg}} \\times \\sym{\\eta} \\times 3"
                ],
                [
                    "\\sym{a_{vg}} \\times \\sym{\\eta} \\times 3 \\times (\\frac{\\sym{T_{C,V}}}{\\sym{T_{V}}})"
                ],
                [
                    "\\sym{a_{vg}} \\times \\sym{\\eta} \\times 3 \\times (\\frac{\\sym{T_{C,V}}\\times \\sym{T_{D,V}}}{\\sym{T_{V}}^{2}})"
                ]
            ]
        }
    },
    {
        "id": "G32_COMP_6",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.5(5)"
        ],
        "title": "Vertical design spectrum for elastic analysis",
        "description": "The design spectrum represents the horizontal seismic response of a structure that accounts for inelastic behavior by reducing the elastic response spectrum using the behavior factor. This spectrum ensures that the structure can dissipate energy through ductile mechanisms, allowing for a more efficient design by considering reduced seismic forces in the horizontal direction.",
        "latexSymbol": "S_{vd}(T)",
        "latexEquation": "\\sym{a_{vg}} \\times (\\frac{2}{3} + \\frac{\\sym{T_{V}}}{\\sym{T_{B,V}}} \\times (\\frac{2.5}{\\sym{q}} - \\frac{2}{3}))",
        "type": "number",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G32_COMP_8",
            "G32_COMP_9",
            "G32_COMP_2",
            "G32_COMP_3",
            "G32_COMP_4",
            "G32_COMP_1",
            "G32_COMP_7"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{T_{V,type}} = Start point(0.0s)",
                    "\\sym{T_{V,type}} = Lower limit",
                    "\\sym{T_{V,type}} = Upper limit",
                    "\\sym{T_{V,type}} = Constant range",
                    "\\sym{T_{V,type}} = End point(4.0s)"
                ]
            ],
            "data": [
                [
                    "\\sym{a_{vg}} \\times (\\frac{2}{3} + \\frac{\\sym{T_{V}}}{\\sym{T_{B,V}}} \\times (\\frac{2.5}{\\sym{q}} - \\frac{2}{3}))"
                ],
                [
                    "\\sym{a_{vg}} \\times (\\frac{2}{3} + \\frac{\\sym{T_{V}}}{\\sym{T_{B,V}}} \\times (\\frac{2.5}{\\sym{q}} - \\frac{2}{3}))"
                ],
                [
                    "\\sym{a_{vg}} \\times \\frac{2.5}{\\sym{q}}"
                ],
                [
                    "\\sym{a_{vg}} \\times \\frac{2.5}{\\sym{q}}\\times \\frac{\\sym{T_{C,V}}}{\\sym{T_{V}}}"
                ],
                [
                    "\\sym{a_{vg}} \\times \\frac{2.5}{\\sym{q}}\\times \\frac{\\sym{T_{C,V}} \\times \\sym{T_{D,V}}}{\\sym{T_{V}}^{2}}"
                ]
            ]
        }
    },
    {
        "id": "G32_COMP_7",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.5(6)"
        ],
        "title": "Behavior factor for energy dissipation in vertical elastic design",
        "description": "For the vertical component of seismic action, a behavior factor up to 1.5 should generally be adopted for all materials and structural systems. This means that for most vertical seismic load designs, values of 1.5 or less are appropriate to reflect the inelastic behavior of structures under seismic forces.",
        "latexSymbol": "q",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "default": 1,
        "const": True
    },
    {
        "id": "G32_COMP_8",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.3(1)P"
        ],
        "title": "Vibration period type for vertical response",
        "description": "This parameter allows users to select the type of vertical vibration period from predefined options, including the starting point, the limits of the constant spectral acceleration branch, and the beginning of the constant displacement response range for vertical seismic actions.",
        "latexSymbol": "T_{V,type}",
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
                    "Start point(0.0s)",
                    "Represents the initial state with no vertical vibration period, used as a reference point."
                ],
                [
                    "Lower limit",
                    "($$T_{B,V}$$) The lower limit of the period where the constant spectral acceleration branch for vertical response begins."
                ],
                [
                    "Upper limit",
                    "($$T_{C,V}$$) The upper limit of the period where the constant spectral acceleration branch for vertical response ends."
                ],
                [
                    "Constant range",
                    "($$T_{D,V}$$) The point where the constant displacement response range for vertical response starts."
                ],
                [
                    "End point(4.0s)",
                    "Represents the maximum vertical vibration period considered in this spectrum."
                ]
            ]
        }
    },
    {
        "id": "G32_COMP_9",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.3(1)P"
        ],
        "title": "Vibration period for vertical response",
        "description": "The vibration period for vertical response refers to the time it takes for one complete cycle of vertical vibration in a single-degree-of-freedom system. It is used to evaluate the dynamic behavior of structures under the vertical component of seismic actions.",
        "latexSymbol": "T_{V}",
        "latexEquation": "0",
        "type": "number",
        "unit": "s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G32_COMP_8",
            "G32_COMP_2",
            "G32_COMP_3",
            "G32_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{T_{V,type}} = Start point(0.0s)",
                    "\\sym{T_{V,type}} = Lower limit",
                    "\\sym{T_{V,type}} = Upper limit",
                    "\\sym{T_{V,type}} = Constant range",
                    "\\sym{T_{V,type}} = End point(4.0s)"
                ]
            ],
            "data": [
                [
                    "0"
                ],
                [
                    "\\sym{T_{B,V}}"
                ],
                [
                    "\\sym{T_{C,V}}"
                ],
                [
                    "\\sym{T_{D,V}}"
                ],
                [
                    "4"
                ]
            ]
        }
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/110560817/EN1998-1+Vertical+Response+Spectrum
        'id': '32',
        'standardType': 'EUROCODE',
        'codeName': 'EN1998-1',
        'codeTitle': 'Eurocode 8 — Design of structures for earthquake resistance — Part 1: General rules, seismic actions and rules for buildings',
        'title': 'Vertical Elastic Response and Design Spectrum Calculation',
        'description': r"[EN1998-1] This guide provides detailed instructions for calculating both the vertical elastic response spectrum and the design spectrum for elastic analysis. The elastic response spectrum represents the maximum elastic response of a structure under vertical seismic forces, while the design spectrum incorporates the behavior factor to account for inelastic deformation. The guide explains how to use vertical ground acceleration, soil factors, and vibration periods to determine the structure’s vertical response under both elastic and inelastic conditions. This guide is primarily used in the initial analysis phase to assess the vertical performance of a structure during an earthquake.",
        'edition': '2004',
        'targetComponents': ['G32_COMP_5', 'G32_COMP_6'],
        'testInput': [
            {'component': 'G31_COMP_2', 'value': 2.35},
            {'component': 'G31_COMP_3', 'value': 'Class I'},
            {'component': 'G31_COMP_6', 'value': 'Type 1 (For large earthquakes)'},
            {'component': 'G31_COMP_11', 'value': 5},
            {'component': 'G32_COMP_8', 'value': 'Start point(0.0s)'},
            # {'component': 'G32_COMP_8', 'value': 'Lower limit'},
        ]
    }
]
