component_list = [
    {
        "id": "G35_COMP_1",
        "codeName": "EN1998-2",
        "reference": [
            "6.6.4(3)"
        ],
        "title": "Seismic condition based on proximity to active fault",
        "description": "This option allows the user to select the seismic condition based on the distance of the bridge site from an active fault. It determines how the effective displacement due to seismic ground movement is calculated for seismic design.",
        "latexSymbol": "seiscond",
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
                    "Condition A",
                    "5 km or more from an active fault"
                ],
                [
                    "Condition B",
                    "Less than 5 km from an active fault capable of producing a magnitude 6.5 or greater earthquake"
                ]
            ]
        }
    },
    {
        "id": "G35_COMP_2",
        "codeName": "EN1998-2",
        "reference": [
            "6.6.4(6.12)"
        ],
        "title": "Minimum overlap length under seismic conditions",
        "description": "The minimum overlap length under seismic conditions refers to the required length at a support to ensure stability and functionality during seismic events. It accounts for the relative displacement between supported and supporting members due to seismic ground movement and structural deformation.",
        "latexSymbol": "l_{ov}",
        "latexEquation": "\\sym{l_{m}} + \\sym{d_{eg}} + \\sym{d_{es}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G35_COMP_3",
            "G35_COMP_4",
            "G35_COMP_9"
        ]
    },
    {
        "id": "G35_COMP_3",
        "codeName": "EN1998-2",
        "reference": [
            "6.6.4(3)"
        ],
        "title": "Minimum support length under seismic conditions",
        "description": "The minimum support length under seismic conditions refers to the shortest length required at a support to safely transmit the vertical reaction force during an earthquake. It ensures the structure's stability and must be at least 400 mm.",
        "latexSymbol": "l_{m}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 400,
        "const": True
    },
    {
        "id": "G35_COMP_4",
        "codeName": "EN1998-2",
        "reference": [
            "6.6.4(6.13)"
        ],
        "title": "Effective displacement due to seismic ground displacement",
        "description": "The effective displacement due to seismic ground displacement refers to the relative displacement between supported and supporting members caused by spatial variations in ground movement during an earthquake. The calculation depends on the proximity of the bridge site to an active fault, with adjustments made if the site is less than 5 km from a fault capable of producing a magnitude 6.5 or greater earthquake.",
        "latexSymbol": "d_{eg}",
        "latexEquation": "\\min(\\sym{\\epsilon_{e}} \\times \\sym{L_{eff}}\\times 1000, 2\\times \\sym{d_{g}} \\times 1000)",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G35_COMP_1",
            "G35_COMP_6",
            "G35_COMP_5",
            "G31_COMP_13"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{seiscond} = Condition A",
                    "\\sym{seiscond} = Condition B"
                ]
            ],
            "data": [
                [
                    "\\min(\\sym{\\epsilon_{e}} \\times \\sym{L_{eff}}\\times 1000 , 2\\times \\sym{d_{g}} \\times 1000)"
                ],
                [
                    "2 \\times \\min(\\sym{\\epsilon_{e}} \\times \\sym{L_{eff}} \\times 1000 , 2 \\times \\sym{d_{g}} \\times 1000)"
                ]
            ]
        }
    },
    {
        "id": "G35_COMP_5",
        "codeName": "EN1998-2",
        "reference": [
            "6.6.4(3)"
        ],
        "title": "Effective length of the deck",
        "description": "The effective length of the deck refers to the distance from a specific deck joint to the nearest point where the deck is fully connected to the substructure. If the deck is fully connected to a group of piers, it is taken as the distance between the support and the center of the pier group. A 'full connection' means a solid connection to the substructure, either monolithically or through fixed bearings, seismic links, or shock transmission units, without any force-limiting function.",
        "latexSymbol": "L_{eff}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "default": 50.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G35_COMP_6",
        "codeName": "EN1998-2",
        "reference": [
            "6.6.4(6.14)"
        ],
        "title": "Strain due to seismic ground displacement",
        "description": "The strain due to seismic ground displacement refers to the ratio of the design ground displacement to the specified distance parameter. It represents the deformation experienced by the structure as a result of seismic ground movement and is used in calculating effective displacement.",
        "latexSymbol": "\\epsilon_{e}",
        "latexEquation": "\\frac{2 \\times \\sym{d_{g}}}{\\sym{L_{g}}}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 3,
        "required": [
            "G31_COMP_13",
            "G35_COMP_7"
        ]
    },
    {
        "id": "G35_COMP_7",
        "codeName": "EN1998-2",
        "reference": [
            "3.3(Table3.1N)"
        ],
        "title": "Distance parameter for seismic design",
        "description": "The distance parameter for seismic design refers to the distance beyond which ground motions are considered to be completely uncorrelated. It is used to account for the loss of correlation in ground movements when calculating seismic effects on structures.",
        "latexSymbol": "L_{g}",
        "latexEquation": "600",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G31_COMP_1"
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
                ]
            ],
            "data": [
                [
                    "600"
                ],
                [
                    "500"
                ],
                [
                    "400"
                ],
                [
                    "300"
                ],
                [
                    "500"
                ]
            ]
        }
    },
    {
        "id": "G35_COMP_8",
        "codeName": "EN1998-2",
        "reference": [
            "6.6.4(3)"
        ],
        "title": "Selecting deck connection option",
        "description": "This option allows the user to choose the appropriate method for calculating the effective seismic displacement based on how the deck is connected to the piers or abutments. Selecting the correct connection type ensures accurate calculation of displacement during seismic events.",
        "latexSymbol": "deckconn",
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
                    "Monolithic or fixed bearing connection",
                    "Deck connected monolithically or through fixed bearings acting as full seismic links"
                ],
                [
                    "Seismic link with slack connection",
                    "Deck connected to piers or abutments through seismic links with slack"
                ]
            ]
        }
    },
    {
        "id": "G35_COMP_9",
        "codeName": "EN1998-2",
        "reference": [
            "6.6.4(3)"
        ],
        "title": "Effective seismic displacement of the support",
        "description": "The effective seismic displacement of the support refers to the displacement experienced by the support structure due to seismic forces. It is calculated based on the total design displacement and any additional slack in the seismic links, accounting for structural deformation during an earthquake.",
        "latexSymbol": "d_{es}",
        "latexEquation": "\\sym{d_{Ed}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G35_COMP_8",
            "G35_COMP_11",
            "G35_COMP_10"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{deckconn} = Monolithic or fixed bearing connection",
                    "\\sym{deckconn} = Seismic link with slack connection"
                ]
            ],
            "data": [
                [
                    "\\sym{d_{Ed}}"
                ],
                [
                    "\\sym{d_{Ed}} + \\sym{s}"
                ]
            ]
        }
    },
    {
        "id": "G35_COMP_10",
        "codeName": "EN1998-2",
        "reference": [
            "6.6.1(Figure6.2)"
        ],
        "title": "Slack of the seismic link",
        "description": "The slack of the seismic link refers to the additional movement allowed in the connection between the deck and the piers or abutment. It represents the extra displacement capacity due to looseness or flexibility in the seismic link, which must be considered when calculating the effective seismic displacement.",
        "latexSymbol": "s",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 25.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G35_COMP_11",
        "codeName": "EN1998-2",
        "reference": [
            "2.3.6.3(2.7)"
        ],
        "title": "Total design displacement in the seismic design situation",
        "description": "The total design displacement accounts for the combined effects of seismic displacement, long-term deformations from permanent actions, and thermal movements. It includes a combination factor for thermal action to assess the maximum displacement the structure must accommodate under seismic conditions.",
        "latexSymbol": "d_{Ed}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 100.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/112034826/EN1998-2+Overlap+Length+under+Seismic+Conditions
        'id': '35',
        'standardType': 'EUROCODE',
        'codeName': 'EN1998-2',
        'codeTitle': 'Eurocode 8 — Design of structures for earthquake resistance — Part 2: Bridges',
        'title': 'Minimum Overlap Length Calculation under Seismic Conditions',
        'description': r"[EN1998-2] This guide provides a step-by-step approach to calculating the minimum overlap length required at supports during seismic events. It covers essential factors, including the minimum support length, effective ground displacement, and structural deformation, to ensure structural stability and safety. By following this guide, users can accurately determine the necessary overlap to accommodate seismic movement.",
        'edition': '2005+A2:2011 Incorporating corrigenda February 2010 and February 2012',
        'figureFile': 'detail_content_35.png',
        'targetComponents': ['G35_COMP_2'],
        'testInput': [
            {'component': 'G31_COMP_1', 'value': 'A'},
            {'component': 'G31_COMP_2', 'value': 2.35},
            {'component': 'G31_COMP_3', 'value': 'Class I'},
            {'component': 'G31_COMP_6', 'value': 'Type 1 (For large earthquakes)'},
            {'component': 'G35_COMP_1', 'value': 'Condition A'},
            {'component': 'G35_COMP_5', 'value': 50.0},
            {'component': 'G35_COMP_8', 'value': 'Monolithic or fixed bearing connection'},
            {'component': 'G35_COMP_10', 'value': 25},
            {'component': 'G35_COMP_11', 'value': 100.0},
        ],
    },
]
