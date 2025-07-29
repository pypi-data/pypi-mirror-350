component_list = [
    {
        "id": "G17_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.2(1)"
        ],
        "title": "Reference concrete strength for shrinkage calculations",
        "description": "The reference concrete strength is used in shrinkage calculations. It serves as a baseline value to determine the extent of shrinkage based on the material's properties and environmental conditions.",
        "latexSymbol": "f_{cmo}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 0,
        "default": 10,
        "const": True
    },
    {
        "id": "G17_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.2(1)"
        ],
        "title": "Reference relative humidity",
        "description": "This term represents the standard reference value for relative humidity, set at 100%. It is used as a baseline in calculations to compare the actual ambient relative humidity and to adjust factors related to concrete shrinkage.",
        "latexSymbol": "RH_{0}",
        "type": "number",
        "unit": "%",
        "notation": "standard",
        "decimal": 0,
        "default": 100.0,
        "const": True
    },
    {
        "id": "G17_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.2(1)"
        ],
        "title": "Initial drying shrinkage coefficient based on cement type",
        "description": "This coefficient adjusts the base value of the drying shrinkage strain according to the type of cement used. It directly influences the initial potential for drying shrinkage, with different values assigned depending on the cement class. This adjustment is crucial in setting the baseline for how much shrinkage the concrete might experience initially.",
        "latexSymbol": "\\alpha_{ds1}",
        "latexEquation": "3",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G15_COMP_2"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{cementype} = Class S",
                    "\\sym{cementype} = Class N",
                    "\\sym{cementype} = Class R"
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
        "id": "G17_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.2(1)"
        ],
        "title": "Exponential adjustment for concrete strength based on cement type",
        "description": "This coefficient is used to adjust the drying shrinkage calculation based on the concrete's compressive strength and the type of cement used. It applies an exponential correction that accounts for how different cement types influence the concrete's strength and, consequently, its drying shrinkage behavior. This adjustment ensures that the effects of cement type on concrete strength are accurately reflected in the shrinkage predictions.",
        "latexSymbol": "\\alpha_{ds2}",
        "latexEquation": "0.13",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G15_COMP_2"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{cementype} = Class S",
                    "\\sym{cementype} = Class N",
                    "\\sym{cementype} = Class R"
                ]
            ],
            "data": [
                [
                    "0.13"
                ],
                [
                    "0.12"
                ],
                [
                    "0.11"
                ]
            ]
        }
    },
    {
        "id": "G17_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.2(B.12)"
        ],
        "title": "Relative humidity ratio adjustment factor",
        "description": "This factor modifies the basic drying shrinkage strain of concrete based on the ambient relative humidity. The adjustment is made by considering the ratio of the ambient relative humidity to a reference value of 100%. This helps predict how much the concrete will shrink depending on the moisture levels in the surrounding environment.",
        "latexSymbol": "\\beta_{RH}",
        "latexEquation": "1.55 \\times [1 - (\\frac{\\sym{RH}}{\\sym{RH_{0}}})^{3}]",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_15",
            "G17_COMP_2"
        ]
    },
    {
        "id": "G17_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.2(B.11)"
        ],
        "title": "Basic drying shrinkage strain",
        "description": "This term represents the initial or basic drying shrinkage strain of concrete. It is a starting point for calculating the total drying shrinkage strain and is determined based on the concrete's properties and environmental conditions. The basic drying shrinkage strain is used to predict the long-term shrinkage behavior of the concrete.",
        "latexSymbol": "\\epsilon_{cd,0}",
        "latexEquation": "0.85 \\times [(220+110\\times \\sym{\\alpha_{ds1}})\\times\\exp(-\\sym{\\alpha_{ds2}}\\times \\frac{\\sym{f_{cm}}}{\\sym{f_{cmo}}})]\\times 10^{-6}\\times \\sym{\\beta_{RH}}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G17_COMP_3",
            "G17_COMP_4",
            "G14_COMP_7",
            "G17_COMP_1",
            "G17_COMP_5"
        ]
    },
    {
        "id": "G17_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(3.12)"
        ],
        "title": "Autogenous shrinkage strain",
        "description": "This term represents the overall autogenous shrinkage strain in concrete without considering the time-dependent development. It reflects the shrinkage that occurs as a result of the internal chemical processes during the hardening of the concrete, primarily occurring in the early stages after casting.",
        "latexSymbol": "\\epsilon_{ca}(\\infty)",
        "latexEquation": "2.5\\times (\\sym{f_{ck}} - 10)\\times 10^{-6}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G14_COMP_5"
        ]
    },
    {
        "id": "G17_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(Table3.3)"
        ],
        "title": "Coefficient depending on the notional size",
        "description": "The value of the coefficient depends on the notional size of the concrete member. A smaller notional size means that the exposed surface area is large relative to the cross-sectional area of the concrete. This results in greater and faster drying shrinkage because there is more surface area available for moisture loss. As the notional size increases, the ratio of the exposed surface area to the cross-sectional area decreases, which slows down moisture loss and reduces drying shrinkage. Therefore, the coefficient decreases as the notional size increases, reflecting the reduced shrinkage potential in larger cross-sections.",
        "latexSymbol": "k_{h}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_13"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "h_{0}",
                    "value": [
                        100,
                        200,
                        300,
                        500
                    ]
                }
            ],
            "data": [
                1.0,
                0.85,
                0.75,
                0.7
            ]
        }
    },
    {
        "id": "G17_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(6)"
        ],
        "title": "Final value of the drying shrinkage strain",
        "description": "This term represents the final or ultimate value of the drying shrinkage strain that the concrete will experience over time. It is calculated by multiplying the initial drying shrinkage strain by a coefficient that depends on the notional size of the concrete member. This value provides an estimate of the long-term shrinkage that the concrete will undergo.",
        "latexSymbol": "\\epsilon_{cd}(\\infty)",
        "latexEquation": "\\sym{k_{h}} \\times \\sym{\\epsilon_{cd,0}}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G17_COMP_8",
            "G17_COMP_6"
        ]
    },
    {
        "id": "G17_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4 (3.8)"
        ],
        "title": "Total shrinkage strain due to drying and autogenous shrinkage",
        "description": "This term represents the total shrinkage strain in concrete, which is the sum of drying shrinkage and autogenous shrinkage. Drying shrinkage occurs as moisture slowly migrates through the hardened concrete, while autogenous shrinkage primarily develops during the early stages of concrete hardening.",
        "latexSymbol": "\\epsilon_{cs}(\\infty)",
        "latexEquation": "\\sym{\\epsilon_{cd}(\\infty)} + \\sym{\\epsilon_{ca}(\\infty)}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G17_COMP_9",
            "G17_COMP_7"
        ]
    },
    {
        "id": "G17_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(6)"
        ],
        "title": "Age at the start of drying shrinkage",
        "description": "This term represents the age of the concrete in days when drying shrinkage (or swelling) begins, typically at the end of the curing period. The age at which drying shrinkage starts is generally considered to be around 7 to 14 days, depending on the curing method and environmental conditions. For standard curing, this age is often set at 7 days, but it may vary if longer curing periods are required, such as in special conditions or projects.",
        "latexSymbol": "t_{s}",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 0,
        "default": 3.0,
        "limits": {
            "exMin": 0
        }
    },
    {
        "id": "G17_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(3.9)"
        ],
        "title": "Time-dependent drying shrinkage strain",
        "description": "This term represents the drying shrinkage strain of concrete as it develops over time. It accounts for how the strain increases as moisture gradually leaves the concrete. The time-dependent drying shrinkage strain helps in understanding and predicting how the concrete will continue to shrink as it ages.",
        "latexSymbol": "\\epsilon_{cd}(t)",
        "latexEquation": "\\sym{\\beta_{ds}(t,t_{s})} \\times \\sym{k_{h}} \\times \\sym{\\epsilon_{cd,0}}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G17_COMP_13",
            "G17_COMP_8",
            "G17_COMP_6"
        ]
    },
    {
        "id": "G17_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(3.10)"
        ],
        "title": "Drying shrinkage development factor",
        "description": "This factor represents the time-dependent development of drying shrinkage in concrete. It describes how the drying shrinkage strain progresses over time, starting from the initial time of drying. The factor accounts for the ongoing moisture loss and helps in predicting the long-term shrinkage behavior of the concrete.",
        "latexSymbol": "\\beta_{ds}(t,t_{s})",
        "latexEquation": "\\frac{(\\sym{t} - \\sym{t_{s}})}{(t - \\sym{t_{s}}) + 0.04 \\sqrt{\\sym{h_{0}}^{3}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_22",
            "G17_COMP_11",
            "G16_COMP_13"
        ]
    },
    {
        "id": "G17_COMP_14",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(3.11)"
        ],
        "title": "Time-dependent autogenous shrinkage strain",
        "description": "This term represents the autogenous shrinkage strain in concrete as it develops over time. Autogenous shrinkage occurs during the hardening process of the concrete, particularly in the early stages after casting, and it is influenced by the concrete's strength. The time-dependent nature of this strain helps in understanding how the shrinkage evolves as the concrete matures.",
        "latexSymbol": "\\epsilon_{ca}(t)",
        "latexEquation": "\\sym{\\beta_{as}(t)} \\times \\sym{\\epsilon_{ca}(\\infty)}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G17_COMP_15",
            "G17_COMP_7"
        ]
    },
    {
        "id": "G17_COMP_15",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(3.13)"
        ],
        "title": "Time-dependent autogenous shrinkage development factor",
        "description": "This factor describes how autogenous shrinkage in concrete develops over time. It is used to calculate the progression of autogenous shrinkage from the initial stages of concrete hardening up to its final value. The factor is particularly important for predicting how much shrinkage will occur as the concrete ages.",
        "latexSymbol": "\\beta_{as}(t)",
        "latexEquation": "1 - \\exp(-0.2 \\times \\sym{t}^{0.5})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_22"
        ]
    },
    {
        "id": "G17_COMP_16",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(3.8)"
        ],
        "title": "Time-dependent total shrinkage strain",
        "description": "This term represents the total shrinkage strain in concrete as it develops over time, including both drying shrinkage and autogenous shrinkage. It accounts for how these strains evolve as the concrete ages, helping to predict the overall deformation of the concrete structure throughout its lifespan.",
        "latexSymbol": "\\epsilon_{cs}(t)",
        "latexEquation": "\\sym{\\epsilon_{cd}(t)} + \\sym{\\epsilon_{ca}(t)}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G17_COMP_12",
            "G17_COMP_14"
        ]
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/88278896/EN1992-1-1+Shrinkage+Strain
        'id': '17',
        'standardType': 'EUROCODE',
        'codeName': 'EN1992-1-1',
        'codeTitle': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Shrinkage Strain Calculation According to Eurocode',
        'description': "[EN1992-1-1] This guide provides a comprehensive overview of the methods and formulas used to calculate shrinkage strain in concrete as outlined in the Eurocode. It covers the components of shrinkage, including drying shrinkage and autogenous shrinkage, and explains how to apply relevant coefficients and factors. This guide is essential for engineers seeking to accurately predict and account for shrinkage in concrete structures during the design process.",
        'edition': '2004',
        'targetComponents': ['G17_COMP_10', 'G17_COMP_16'],
        'testInput': [
            {'component': "G14_COMP_4", 'value': 'C12/15'}, # C = C12/15
            {'component': "G15_COMP_2", 'value': 'Class S'}, # cementtype = Class S
            {'component': "G16_COMP_11", 'value': 534694.0},
            {'component': "G16_COMP_12", 'value': 5921.8},
            {'component': "G16_COMP_14", 'value': 'User Input'}, # rhtype = User Input
            {'component': "G16_COMP_23", 'value': 70},
            {'component': "G17_COMP_11", 'value': 3.0},
        ],
    },
]
