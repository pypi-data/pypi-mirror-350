component_list = [
    {
        "id": "G31_COMP_1",
        "codeName": "EN1998-1",
        "reference": [
            "3.1.2(Table3.1)"
        ],
        "title": "Selection of ground type",
        "description": "Choose the appropriate ground type based on the geotechnical properties of the site. The available types range from rock-like formations (Type A) to soft soils (Type D and E), each influencing the seismic response of the structure.",
        "latexSymbol": "groundtype",
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
                    "A",
                    "Rock or rock-like geological formations with a maximum of 5 meters of weaker material at the surface. The shear wave velocity $$v_{s,30}$$ exceeds 800 m/s."
                ],
                [
                    "B",
                    "Deposits of very dense sand, gravel, or very stiff clay, extending at least several tens of meters in thickness, characterized by a gradual increase in mechanical properties with depth. The shear wave velocity $$v_{s,30}$$ ranges between 360 and 800 m/s."
                ],
                [
                    "C",
                    "Deep deposits of dense or medium-dense sand, gravel, or stiff clay, with a thickness ranging from several tens to many hundreds of meters. The shear wave velocity $$v_{s,30}$$ ranges between 180 and 360 m/s."
                ],
                [
                    "D",
                    "Deposits of loose-to-medium cohesionless soil (with or without soft cohesive layers) or predominantly soft-to-firm cohesive soil. The shear wave velocity $$v_{s,30}$$ is less than 180 m/s."
                ],
                [
                    "E",
                    "A soil profile consisting of a surface alluvium layer, with shear wave velocities typical of Type C or D (between 5 m and 20 m thick), underlain by stiffer material with a shear wave velocity greater than 800 m/s."
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_2",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.1(2)"
        ],
        "title": "Reference peak ground acceleration",
        "description": "The reference peak ground acceleration represents the maximum expected ground acceleration for a specific location during an earthquake, assuming it occurs on Type A ground (rock or very stiff soil). It is typically based on a 475-year return period, corresponding to an approximately 10% probability of exceedance over 50 years.",
        "latexSymbol": "a_{gR}",
        "type": "number",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 3,
        "default": 2.35,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G31_COMP_3",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.1(3)"
        ],
        "title": "Selection of importance class",
        "description": "Select the importance class for the bridge based on its criticality. Class I applies to less critical bridges, Class II to standard bridges, and Class III to essential bridges that require higher safety standards. Detailed information can be found in Eurocode 1998-2, section 2.1.",
        "latexSymbol": "impoclass",
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
                    "Class I"
                ],
                [
                    "Class II"
                ],
                [
                    "Class III"
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_4",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.1(3)"
        ],
        "title": "Importance factor for seismic design",
        "description": "The importance factor adjusts the design seismic load based on the structure’s significance. It is applied to account for the potential impact on human life, economic, and social consequences in case of failure. For most structures, the importance factor is 1.0. For critical infrastructure, a higher value like 1.3 may be used, while less critical structures may have a lower value, such as 0.85. Detailed classifications can be found in Eurocode 1998-2, section 2.1.",
        "latexSymbol": "\\gamma_{I}",
        "latexEquation": "0.85",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G31_COMP_3"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{impoclass} = Class I",
                    "\\sym{impoclass} = Class II",
                    "\\sym{impoclass} = Class III"
                ]
            ],
            "data": [
                [
                    "0.85"
                ],
                [
                    "1.00"
                ],
                [
                    "1.30"
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_5",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(1)P"
        ],
        "title": "Design ground acceleration on Type A ground",
        "description": "The design ground acceleration refers to the peak ground acceleration for structures built on Type A ground (rock or very stiff soil). It serves as the baseline acceleration used in seismic design and is modified for other ground types using the soil factor to account for local ground conditions. In seismic calculations, it represents the reference value before adjustments for different soil types.",
        "latexSymbol": "a_{g}",
        "latexEquation": "\\sym{\\gamma_{I}} \\times \\sym{a_{gR}}",
        "type": "number",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_4",
            "G31_COMP_2"
        ]
    },
    {
        "id": "G31_COMP_6",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(2)P"
        ],
        "title": "Selection of response spectrum type",
        "description": "The values for the periods and soil factor that define the shape of the elastic response spectrum depend on the ground type. Generally, Type 1 is recommended for areas where large earthquakes occur, with surface-wave magnitudes exceeding 5.5, while Type 2 is suitable for regions with smaller earthquakes, where the surface-wave magnitude is 5.5 or less.",
        "latexSymbol": "spectype",
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
                    "Type 1 (For large earthquakes)"
                ],
                [
                    "Type 2 (For smaller earthquakes)"
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_7",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(2)P"
        ],
        "title": "Lower limit of the constant spectral acceleration period",
        "description": "The lower limit of the period in the constant spectral acceleration range represents the period at which the acceleration response starts to stabilize and remains constant until it reaches the upper limit. This value depends on the ground type and is used to define the shape of the response spectrum.",
        "latexSymbol": "T_{B}",
        "type": "number",
        "unit": "s",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G31_COMP_1",
            "G31_COMP_6"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{groundtype} = A",
                    "\\sym{groundtype} = B",
                    "\\sym{groundtype} = C",
                    "\\sym{groundtype} = D",
                    "\\sym{groundtype} = E"
                ],
                [
                    "\\sym{spectype} = Type 1 (For large earthquakes)",
                    "\\sym{spectype} = Type 2 (For smaller earthquakes)"
                ]
            ],
            "data": [
                [
                    "0.15",
                    "0.05"
                ],
                [
                    "0.15",
                    "0.05"
                ],
                [
                    "0.20",
                    "0.10"
                ],
                [
                    "0.20",
                    "0.10"
                ],
                [
                    "0.15",
                    "0.05"
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_8",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(2)P"
        ],
        "title": "Upper limit of the constant spectral acceleration period",
        "description": "The upper limit of the period in the constant spectral acceleration range marks the point where the acceleration response begins to decrease. This value is used to define the transition from the constant acceleration phase to the phase where acceleration decreases with increasing period.",
        "latexSymbol": "T_{C}",
        "type": "number",
        "unit": "s",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G31_COMP_1",
            "G31_COMP_6"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{groundtype} = A",
                    "\\sym{groundtype} = B",
                    "\\sym{groundtype} = C",
                    "\\sym{groundtype} = D",
                    "\\sym{groundtype} = E"
                ],
                [
                    "\\sym{spectype} = Type 1 (For large earthquakes)",
                    "\\sym{spectype} = Type 2 (For smaller earthquakes)"
                ]
            ],
            "data": [
                [
                    "0.40",
                    "0.25"
                ],
                [
                    "0.50",
                    "0.25"
                ],
                [
                    "0.60",
                    "0.25"
                ],
                [
                    "0.80",
                    "0.30"
                ],
                [
                    "0.50",
                    "0.25"
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_9",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(2)P"
        ],
        "title": "Period defining the start of the constant displacement response",
        "description": "The period that defines the start of the constant displacement response marks the point in the response spectrum where the displacement response becomes constant, while the acceleration continues to decrease with increasing period. This value is significant in the long-period range of the spectrum and depends on the ground type.",
        "latexSymbol": "T_{D}",
        "type": "number",
        "unit": "s",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G31_COMP_1",
            "G31_COMP_6"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{groundtype} = A",
                    "\\sym{groundtype} = B",
                    "\\sym{groundtype} = C",
                    "\\sym{groundtype} = D",
                    "\\sym{groundtype} = E"
                ],
                [
                    "\\sym{spectype} = Type 1 (For large earthquakes)",
                    "\\sym{spectype} = Type 2 (For smaller earthquakes)"
                ]
            ],
            "data": [
                [
                    "2.00",
                    "1.20"
                ],
                [
                    "2.00",
                    "1.20"
                ],
                [
                    "2.00",
                    "1.20"
                ],
                [
                    "2.00",
                    "1.20"
                ],
                [
                    "2.00",
                    "1.20"
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_10",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(2)P"
        ],
        "title": "Soil factor in seismic response",
        "description": "The soil factor represents the influence of local ground conditions on the seismic response of a structure. It adjusts the design ground acceleration to account for how different soil types either amplify or reduce the seismic forces that affect the structure. The value of the soil factor varies depending on the type of ground, with softer soils typically having higher values due to their potential to amplify seismic waves, while harder soils or rock have lower values due to less amplification.",
        "latexSymbol": "S",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G31_COMP_1",
            "G31_COMP_6"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{groundtype} = A",
                    "\\sym{groundtype} = B",
                    "\\sym{groundtype} = C",
                    "\\sym{groundtype} = D",
                    "\\sym{groundtype} = E"
                ],
                [
                    "\\sym{spectype} = Type 1 (For large earthquakes)",
                    "\\sym{spectype} = Type 2 (For smaller earthquakes)"
                ]
            ],
            "data": [
                [
                    "1.00",
                    "1.00"
                ],
                [
                    "1.20",
                    "1.35"
                ],
                [
                    "1.15",
                    "1.50"
                ],
                [
                    "1.35",
                    "1.80"
                ],
                [
                    "1.40",
                    "1.60"
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_11",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(3)"
        ],
        "title": "Viscous damping ratio of the structure",
        "description": "The viscous damping ratio represents the amount of energy dissipated by a structure during dynamic motion, such as during an earthquake. It is expressed as a percentage of critical damping, where 100% would mean no oscillations after the initial displacement. In most structural applications, the viscous damping ratio is typically around 5%, meaning the structure dissipates 5% of the critical damping energy.",
        "latexSymbol": "\\xi",
        "type": "number",
        "unit": "%",
        "notation": "standard",
        "decimal": 1,
        "default": 5.0,
        "limits": {
            "inMin": 0
        },
        "useStd": True
    },
    {
        "id": "G31_COMP_12",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(3.6)"
        ],
        "title": "Damping correction factor",
        "description": "The damping correction factor η adjusts the seismic response to account for the level of damping in the structure. For the standard case of 5% viscous damping, η is set to 1.0. If the damping differs from 5%, the value of η will be adjusted accordingly to reflect the impact of higher or lower damping on the seismic response of the structure.",
        "latexSymbol": "\\eta",
        "latexEquation": "\\max(\\sqrt{\\frac{10}{(5 + \\sym{\\xi})}} , 0.55)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_11"
        ]
    },
    {
        "id": "G31_COMP_13",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.4(3.12)"
        ],
        "title": "Design ground displacement",
        "description": "The design ground displacement represents the estimated maximum displacement of the ground during an earthquake, based on the design ground acceleration. It is calculated using factors such as the design ground acceleration, the soil factor, and the periods defining the limits of the spectral acceleration range.",
        "latexSymbol": "d_{g}",
        "latexEquation": "0.025 \\times \\sym{a_{g}} \\times \\sym{S} \\times \\sym{T_{C}} \\times \\sym{T_{D}}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_5",
            "G31_COMP_10",
            "G31_COMP_8",
            "G31_COMP_9"
        ]
    },
    {
        "id": "G31_COMP_14",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(1)P"
        ],
        "title": "Horizontal elastic response spectrum",
        "description": "The horizontal elastic response spectrum represents the maximum expected response of a structure to seismic forces, assuming elastic behavior in the horizontal direction. It is based on the vibration period and is used to predict the structure’s acceleration, velocity, or displacement during an earthquake.",
        "latexSymbol": "S_{e}(T)",
        "latexEquation": "\\sym{a_{g}} \\times \\sym{S} \\times [1 + (\\frac{T}{\\sym{t_{B}}}) \\times (\\sym{\\eta} \\times 2.5 - 1)]",
        "type": "number",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_5",
            "G31_COMP_10",
            "G31_COMP_19",
            "G31_COMP_20",
            "G31_COMP_7",
            "G31_COMP_8",
            "G31_COMP_9",
            "G31_COMP_12"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{T_{type}} = \\sym{S}tart point(0.0s)",
                    "\\sym{T_{type}} = Lower limit",
                    "\\sym{T_{type}} = Upper limit",
                    "\\sym{T_{type}} = Constant range",
                    "\\sym{T_{type}} = End point(4.0s)"
                ]
            ],
            "data": [
                [
                    "\\sym{a_{g}} \\times \\sym{S} \\times [1 + (\\frac{T}{\\sym{t_{B}}}) \\times (\\sym{\\eta} \\times 2.5 - 1)]"
                ],
                [
                    "\\sym{a_{g}} \\times \\sym{S} \\times [1 + (\\frac{T}{\\sym{t_{B}}}) \\times (\\sym{\\eta} \\times 2.5 - 1)]"
                ],
                [
                    "\\sym{a_{g}} \\times \\sym{S} \\times \\sym{\\eta} \\times 2.5"
                ],
                [
                    "\\sym{a_{g}} \\times \\sym{S} \\times \\sym{\\eta} \\times 2.5 \\times (\\frac{\\sym{t_{C}}}{\\sym{T}})"
                ],
                [
                    "\\sym{a_{g}} \\times \\sym{S} \\times \\sym{\\eta} \\times 2.5\\times (\\frac{\\sym{t_{C}} \\times \\sym{t_{D}}}{\\sym{T}^{2}})"
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_15",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(3.7)"
        ],
        "title": "Elastic displacement response spectrum",
        "description": "The elastic displacement response spectrum represents the maximum expected displacement of a structure during an earthquake, assuming the structure behaves elastically. It is derived from the elastic acceleration response spectrum and is used to assess how much a structure may displace under seismic loads.",
        "latexSymbol": "S_{De}(T)",
        "latexEquation": "\\sym{S_{e}(T)} \\times (\\frac{\\sym{T}}{2\\times\\pi})^{2}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_14",
            "G31_COMP_20"
        ]
    },
    {
        "id": "G31_COMP_16",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.5(4)P"
        ],
        "title": "Horizontal design spectrum for elastic analysis",
        "description": "The design spectrum represents the horizontal seismic response of a structure that accounts for inelastic behavior by reducing the elastic response spectrum using the behavior factor. This spectrum ensures that the structure can dissipate energy through ductile mechanisms, allowing for a more efficient design by considering reduced seismic forces in the horizontal direction.",
        "latexSymbol": "S_{d}(T)",
        "type": "number",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_5",
            "G31_COMP_10",
            "G31_COMP_19",
            "G31_COMP_20",
            "G31_COMP_7",
            "G31_COMP_8",
            "G31_COMP_9",
            "G31_COMP_17",
            "G31_COMP_18"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{T_{type}} = \\sym{S}tart point(0.0s)",
                    "\\sym{T_{type}} = Lower limit",
                    "\\sym{T_{type}} = Upper limit",
                    "\\sym{T_{type}} = Constant range",
                    "\\sym{T_{type}} = End point(4.0s)"
                ]
            ],
            "data": [
                [
                    "\\sym{a_{g}} \\times \\sym{S} \\times [\\frac{2}{3} + \\frac{T}{\\sym{t_{B}}} \\times (\\frac{2.5}{\\sym{q}} - \\frac{2}{3})]"
                ],
                [
                    "\\sym{a_{g}} \\times \\sym{S} \\times [\\frac{2}{3} + \\frac{T}{\\sym{t_{B}}} \\times (\\frac{2.5}{\\sym{q}} - \\frac{2}{3})]"
                ],
                [
                    "\\sym{a_{g}} \\times \\sym{S} \\times \\frac{2.5}{\\sym{q}}"
                ],
                [
                    "\\max(\\sym{a_{g}} \\times \\sym{S} \\times \\frac{2.5}{\\sym{q}} \\times \\frac{\\sym{t_{C}}}{T}, \\sym{\\beta} \\times \\sym{a_{g}})"
                ],
                [
                    "\\max(\\sym{a_{g}} \\times \\sym{S} \\times \\frac{2.5}{\\sym{q}} \\times \\frac{(\\sym{t_{C}} \\times \\sym{t_{D}})}{T^{2}}, \\sym{\\beta} \\times \\sym{a_{g}})"
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_17",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.5(3)P"
        ],
        "title": "Behavior factor for energy dissipation in elastic design",
        "description": "The seismic behavior factor is a coefficient that reduces the elastic response spectrum to account for the inelastic energy dissipation capacity of a structure during seismic events. It reflects the structure's ability to undergo ductile deformations without collapsing, allowing for more efficient designs by lowering the seismic forces used in calculations.",
        "latexSymbol": "q",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "default": 1.5,
        "const": True
    },
    {
        "id": "G31_COMP_18",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.5(4)P"
        ],
        "title": "Lower bound factor for horizontal design spectrum",
        "description": "The lower bound factor represents the minimum limit for the horizontal design spectrum in seismic design. It ensures that the design spectrum does not drop below a certain threshold, even for longer vibration periods. The value of this factor can vary depending on national regulations, but the recommended value in many standards is typically set at 0.2.",
        "latexSymbol": "\\beta",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "default": 0.2,
        "const": True
    },
    {
        "id": "G31_COMP_19",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(1)P"
        ],
        "title": "Vibration period type for spectral response",
        "description": "This parameter allows users to select the appropriate vibration period type from predefined options, including the starting point, limits of the constant spectral acceleration branch, and the beginning of the constant displacement response range within the response spectrum.",
        "latexSymbol": "T_{type}",
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
                    "Represents the initial state with no vibration period, typically used as a baseline or reference."
                ],
                [
                    "Lower limit",
                    "($$T_{B}$$) The lower limit of the period where the constant spectral acceleration branch begins."
                ],
                [
                    "Upper limit",
                    "($$T_{C}$$) The upper limit of the period where the constant spectral acceleration branch ends."
                ],
                [
                    "Constant range",
                    "($$T_{D}$$) The starting point of the constant displacement response range in the response spectrum."
                ],
                [
                    "End point(4.0s)",
                    "Represents the maximum considered vibration period in this context."
                ]
            ]
        }
    },
    {
        "id": "G31_COMP_20",
        "codeName": "EN1998-1",
        "reference": [
            "3.2.2.2(1)P"
        ],
        "title": "Vibration period of a linear single-degree-of-freedom system",
        "description": "The vibration period refers to the time required for a single cycle of vibration in a linear single-degree-of-freedom system. It is an important parameter used to assess the dynamic behavior of structures under seismic loads.",
        "latexSymbol": "T",
        "latexEquation": "0",
        "type": "number",
        "unit": "s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_19",
            "G31_COMP_7",
            "G31_COMP_8",
            "G31_COMP_9"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{T_{type}} = Start point(0.0s)",
                    "\\sym{T_{type}} = Lower limit",
                    "\\sym{T_{type}} = Upper limit",
                    "\\sym{T_{type}} = Constant range",
                    "\\sym{T_{type}} = End point(4.0s)"
                ]
            ],
            "data": [
                [
                    "0"
                ],
                [
                    "\\sym{t_{B}}"
                ],
                [
                    "\\sym{t_{C}}"
                ],
                [
                    "\\sym{t_{D}}"
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
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/110560693/EN1998-1+Horizontal+Response+Spectrum
        'id': '31',
        'standardType': 'EUROCODE',
        'codeName': 'EN1988-1',
        'codeTitle': 'Eurocode 8 — Design of structures for earthquake resistance — Part 1: General rules, seismic actions and rules for buildings',
        'title': 'Horizontal Elastic Response and Design Spectrum Calculation',
        'description': r"[EN1998-1] This guide provides detailed instructions for calculating both the horizontal elastic response spectrum and the design spectrum for elastic analysis. The elastic response spectrum represents the maximum elastic response of a structure under horizontal seismic forces, while the design spectrum accounts for inelastic behavior using the behavior factor. It explains how to use ground acceleration, soil factors, and vibration periods to determine the structure’s horizontal response under both elastic and inelastic conditions. This guide is primarily used in the initial analysis phase to assess the structure’s performance during an earthquake.",
        'edition': '2004',
        'targetComponents': ['G31_COMP_13', 'G31_COMP_14', 'G31_COMP_15', 'G31_COMP_16'],
        'testInput': [
            {'component': 'G31_COMP_1', 'value': 'A'},
            {'component': 'G31_COMP_2', 'value': 2.35},
            {'component': 'G31_COMP_3', 'value': 'Class I'},
            {'component': 'G31_COMP_6', 'value': 'Type 1 (For large earthquakes)'},
            {'component': 'G31_COMP_11', 'value': 5},
            {'component': 'G31_COMP_19', 'value': 'Start point(0.0s)'},
            # {'component': 'G31_COMP_19', 'value': 'Lower limit'},
        ],
    }
]
