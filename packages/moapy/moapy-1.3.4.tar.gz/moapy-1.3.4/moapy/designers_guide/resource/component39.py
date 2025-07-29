component_list = [
    {
        "id": "G39_COMP_1",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(B.23)"
        ],
        "title": "Total mean shrinkage or swelling strain",
        "description": "The total mean shrinkage or swelling strain represents the overall deformation due to shrinkage or swelling in concrete, combining both basic shrinkage and drying shrinkage components. It is calculated by adding the basic shrinkage strain, which occurs even without moisture loss, and the drying shrinkage strain, which occurs when moisture loss happens.",
        "latexSymbol": "\\epsilon_{cs}(t,t_{s})",
        "latexEquation": "\\sym{\\epsilon_{cbs}(t)} + \\sym{\\epsilon_{cds}(t-t_{0})}",
        "type": "number",
        "unit": "mm/mm",
        "notation": "scientific",
        "decimal": 3,
        "required": [
            "G39_COMP_2",
            "G39_COMP_3"
        ]
    },
    {
        "id": "G39_COMP_2",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(B.24)"
        ],
        "title": "Basic shrinkage strain",
        "description": "The basic shrinkage strain represents the intrinsic shrinkage that occurs in concrete even when no moisture loss is possible. It is the initial deformation due to hydration and curing processes, independent of drying conditions.",
        "latexSymbol": "\\epsilon_{cbs}(t)",
        "latexEquation": "\\sym{\\epsilon_{cbs,fcm}} \\times \\sym{\\beta_{bs,t}} \\times \\sym{\\alpha_{NDP,b}}",
        "type": "number",
        "unit": "mm/mm",
        "notation": "scientific",
        "decimal": 3,
        "required": [
            "G39_COMP_6",
            "G39_COMP_7",
            "G39_COMP_4"
        ]
    },
    {
        "id": "G39_COMP_3",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(B.25)"
        ],
        "title": "Drying shrinkage strain",
        "description": "The drying shrinkage strain represents the additional shrinkage in concrete due to moisture loss after the concrete has been cast. It occurs after the initial setting and hydration phases, and it is influenced by factors like the relative humidity and the duration of drying.",
        "latexSymbol": "\\epsilon_{cds}(t-t_{0})",
        "latexEquation": "\\sym{\\epsilon_{cds,fcm}} \\times \\sym{\\beta_{RH}} \\times \\sym{\\beta_{ds,t-ts}} \\times \\sym{\\alpha_{NDP,d}}",
        "type": "number",
        "unit": "mm/mm",
        "notation": "scientific",
        "decimal": 3,
        "required": [
            "G39_COMP_10",
            "G39_COMP_11",
            "G39_COMP_13",
            "G39_COMP_8"
        ]
    },
    {
        "id": "G39_COMP_4",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(1)"
        ],
        "title": "Nationally Determined Parameter for basic shrinkage",
        "description": "The nationally determined parameter for basic shrinkage is a coefficient set by national standards to adjust the basic shrinkage value based on local conditions, practices, or specific material properties. Unless specified otherwise by a National Annex, this coefficient is typically set to 1.0.",
        "latexSymbol": "\\alpha_{NDP,b}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "limits": {
            "inMin": 0
        }
    },
    {
        "id": "G39_COMP_5",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(TableB.3)"
        ],
        "title": "Strength class coefficient for basic shrinkage",
        "description": "The strength class coefficient for basic shrinkage reflects the influence of the cement’s strength class on basic shrinkage behavior. This coefficient adjusts the basic shrinkage strain to account for variations in shrinkage that result from differences in the early strength development of cement.",
        "latexSymbol": "\\alpha_{bs}",
        "latexEquation": "800",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G37_COMP_27"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{concclass} = CS",
                    "\\sym{concclass} = CN",
                    "\\sym{concclass} = CR"
                ]
            ],
            "data": [
                [
                    "800"
                ],
                [
                    "700"
                ],
                [
                    "600"
                ]
            ]
        }
    },
    {
        "id": "G39_COMP_6",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(B.26)"
        ],
        "title": "Notional basic shrinkage coefficient",
        "description": "The notional basic shrinkage coefficient accounts for the effect of concrete strength and the strength class of cement on basic shrinkage. It quantifies the intrinsic shrinkage that occurs during the hydration and curing process, even without moisture loss, influenced by the strength properties of the concrete and cement.",
        "latexSymbol": "\\epsilon_{cbs,fcm}",
        "latexEquation": "\\sym{\\alpha_{bs}} \\times (\\frac{\\sym{f_{cm,28}}}{60 + \\sym{f_{cm,28}}})^{2.5} \\times 10^{-6}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 3,
        "required": [
            "G39_COMP_5",
            "G38_COMP_6"
        ]
    },
    {
        "id": "G39_COMP_7",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(B.27)"
        ],
        "title": "Time evolution coefficient for basic shrinkage",
        "description": "The coefficient for basic shrinkage evolution with time describes how basic shrinkage strain develops over time. It reflects the gradual increase in shrinkage as time progresses, influenced by the curing and hydration process.",
        "latexSymbol": "\\beta_{bs,t}",
        "latexEquation": "1 - \\exp(-0.2 \\times \\sqrt{(\\sym{t})})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_2"
        ]
    },
    {
        "id": "G39_COMP_8",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(1)"
        ],
        "title": "Nationally determined parameter for drying shrinkage",
        "description": "The nationally determined parameter for drying shrinkage is a coefficient set by national standards to adjust the drying shrinkage value based on local conditions, practices, or specific material properties. Unless specified otherwise by a National Annex, this coefficient is typically set to 1.0.",
        "latexSymbol": "\\alpha_{NDP,d}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "limits": {
            "inMin": 0
        }
    },
    {
        "id": "G39_COMP_9",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(TableB.3)"
        ],
        "title": "Strength class coefficient for drying shrinkage",
        "description": "The strength class coefficient for drying shrinkage reflects the effect of the cement’s strength class on drying shrinkage behavior. This coefficient adjusts the drying shrinkage to account for variations in shrinkage that arise due to differences in the early strength development of cement.",
        "latexSymbol": "\\alpha_{ds}",
        "latexEquation": "3",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G37_COMP_27"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{concclass} = CS",
                    "\\sym{concclass} = CN",
                    "\\sym{concclass} = CR"
                ]
            ],
            "data": [
                [
                    "3"
                ],
                [
                    "4"
                ],
                [
                    "6"
                ]
            ]
        }
    },
    {
        "id": "G39_COMP_10",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(B.28)"
        ],
        "title": "Notional drying shrinkage coefficient",
        "description": "The notional drying shrinkage coefficient represents a reference value for drying shrinkage in concrete, accounting for the effects of concrete strength and the strength class of cement. This coefficient quantifies the additional shrinkage due to moisture loss after the initial curing phase.",
        "latexSymbol": "\\epsilon_{cds,fcm}",
        "latexEquation": "(220 + 110 \\times \\sym{\\alpha_{ds}}) \\times \\exp(-0.012 \\times \\sym{f_{cm,28}}) \\times 10^{-6}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 3,
        "required": [
            "G39_COMP_9",
            "G38_COMP_6"
        ]
    },
    {
        "id": "G39_COMP_11",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(3)"
        ],
        "title": "Relative humidity coefficient for drying shrinkage",
        "description": "The relative humidity coefficient for drying shrinkage reflects the influence of ambient relative humidity on the drying shrinkage of concrete. Lower humidity levels increase this coefficient, indicating a higher potential for shrinkage due to increased moisture loss.",
        "latexSymbol": "\\beta_{RH}",
        "latexEquation": "1.55 \\times (1 - (\\frac{\\sym{RH}}{\\sym{RH_{eq}}})^{3})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_16",
            "G39_COMP_12"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "20 <= \\sym{RH} <= \\sym{RH_{eq}}",
                    "\\sym{RH_{eq}} < \\sym{RH} < 100",
                    "\\sym{RH} = 100"
                ]
            ],
            "data": [
                [
                    "1.55 \\times (1 - (\\frac{\\sym{RH}}{\\sym{RH_{eq}}})^{3})"
                ],
                [
                    "1.55 \\times (1 - (\\frac{\\sym{RH}}{\\sym{RH_{eq}}})^{2})"
                ],
                [
                    "1.55 \\times (1 - (\\frac{\\sym{RH}}{\\sym{RH_{eq}}}) - 0.25"
                ]
            ]
        }
    },
    {
        "id": "G39_COMP_12",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(B.32)"
        ],
        "title": "Internal relative humidity of concrete at equilibrium",
        "description": "The internal relative humidity of concrete at equilibrium represents the humidity level within concrete at which moisture movement ceases. This value accounts for self-desiccation effects, particularly relevant in high-performance concrete.",
        "latexSymbol": "RH_{eq}",
        "latexEquation": "\\min(99 \\times (\\frac{35}{\\sym{f_{cm,28}}})^{0.1} , 99)",
        "type": "number",
        "unit": "%",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_6"
        ]
    },
    {
        "id": "G39_COMP_13",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(B.33)"
        ],
        "title": "Time evolution coefficient for drying shrinkage",
        "description": "The time evolution coefficient for drying shrinkage describes how drying shrinkage develops over time, taking into account the notional size of the concrete element. This coefficient reflects the gradual progression of shrinkage as moisture loss continues, influenced by the size of the concrete member.",
        "latexSymbol": "\\beta_{ds,t-ts}",
        "latexEquation": "(\\frac{(\\sym{t} - \\sym{t_{s}})}{0.035 \\times \\sym{h_{n}}^{2} + (\\sym{t} - \\sym{t_{s}})})^{0.5}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_2",
            "G39_COMP_14",
            "G38_COMP_17"
        ]
    },
    {
        "id": "G39_COMP_14",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.6(1)"
        ],
        "title": "Age of concrete at the beginning of drying",
        "description": "The age of concrete at the beginning of drying represents the time, in days, from when the concrete was cast until the drying process begins. This value marks the start of moisture loss in the concrete and is used to calculate drying-related strains such as drying shrinkage.",
        "latexSymbol": "t_{s}",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 0,
        "default": 7.0,
        "limits": {
            "exMin": 0
        }
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/131368407/2G+EN1992-1-1+Total+Mean+Shrinkage+Strain
        'id': '39',
        'standardType': '2G:EUROCODE',
        'codeName': '2G:EN1992-1-1',
        'codeTitle': 'Eurocode 2 — Design of concrete structures - Part 1-1: General rules and rules for buildings, bridges and civil engineering structures',
        'title': 'Total Mean Shrinkage or Swelling Strain Calculation Guide',
        'description': r"[2G:EN1992-1-1] This guide details the process of calculating the total mean shrinkage or swelling strain in concrete by combining both basic and drying shrinkage strains. Following the Eurocode 2nd Generation, it explains how to use formulas that account for concrete properties, including concrete strength, the age of concrete at the start of drying, relative humidity, and the notional size of the concrete member. By following this guide, users can accurately calculate time-dependent shrinkage or swelling strains that affect concrete performance in structures over time.",
        'edition': '2023',
        'targetComponents': ['G39_COMP_1', 'G39_COMP_2', 'G39_COMP_3'],
        'testInput': [
            {'component': 'G37_COMP_4', 'value': 'C20/25'},
            {'component': 'G37_COMP_27', 'value': 'CS'},
            {'component': 'G38_COMP_2', 'value': 36500},
            {'component': 'G38_COMP_16', 'value': 80},
            {'component': 'G38_COMP_18', 'value': 534694},
            {'component': 'G38_COMP_19', 'value': 5921.89},
            {'component': 'G39_COMP_4', 'value': 1.0},
            {'component': 'G39_COMP_8', 'value': 1.0},
            {'component': 'G39_COMP_14', 'value': 7.0},
        ]
    }
]