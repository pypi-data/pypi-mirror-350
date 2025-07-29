component_list = [
    {
        "id": "G38_COMP_1",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.5)"
        ],
        "title": "Total mean creep coefficient",
        "description": "The total mean creep coefficient represents the time-dependent deformation of concrete between two ages, based on its elastic deformation at 28 days. It combines basic and drying creep factors and accounts for influences such as concrete strength, ambient humidity, and the age at loading, providing an estimate of long-term concrete deformation under sustained loads.",
        "latexSymbol": "\\phi(t,t_{0})",
        "latexEquation": "\\sym{\\phi_{bc}(t,t_{0})} + \\sym{\\phi_{dc}(t,t_{0})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_4",
            "G38_COMP_8"
        ]
    },
    {
        "id": "G38_COMP_2",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(1)"
        ],
        "title": "Age of concrete at time of consideration",
        "description": "The age of concrete at time of consideration refers to the number of days since the concrete was cast, at which specific properties or behaviors (e.g., strength, creep) are evaluated. This value helps assess the time-dependent characteristics of concrete.",
        "latexSymbol": "t",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 0,
        "default": 36500.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G38_COMP_3",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(1)"
        ],
        "title": "Age of concrete at loading in days",
        "description": "The age of concrete at loading in days refers to the number of days since casting when a load is first applied, adjusted using specific formulae to account for factors like early strength development.",
        "latexSymbol": "t_{0}",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 0,
        "default": 7.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G38_COMP_4",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.6)"
        ],
        "title": "Basic creep coefficient",
        "description": "The basic creep coefficient indicates the intrinsic, time-dependent deformation of concrete between two ages, based on its 28-day elastic deformation, excluding drying effects. It is influenced by concrete strength and the duration since loading.",
        "latexSymbol": "\\phi_{bc}(t,t_{0})",
        "latexEquation": "\\sym{\\beta_{bc,fcm}} \\times \\sym{\\beta_{bc,t-t0}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_5",
            "G38_COMP_7"
        ]
    },
    {
        "id": "G38_COMP_5",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.7)"
        ],
        "title": "Concrete strength coefficient for basic creep",
        "description": "The concrete strength coefficient for basic creep accounts for the influence of concrete strength on its basic creep behavior. Lower concrete strength increases this coefficient, indicating a higher tendency for basic creep deformation.",
        "latexSymbol": "\\beta_{bc,fcm}",
        "latexEquation": "\\frac{1.8}{\\sym{f_{cm,28}}^{0.7}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_6"
        ]
    },
    {
        "id": "G38_COMP_6",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(2)"
        ],
        "title": "Mean compressive strength at reference age of 28 days",
        "description": "The mean compressive strength at reference age of 28 days represents the average compressive strength of concrete cured under standard conditions for 28 days, serving as a benchmark in concrete design.",
        "latexSymbol": "f_{cm,28}",
        "latexEquation": "\\sym{f_{cm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G37_COMP_6"
        ]
    },
    {
        "id": "G38_COMP_7",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.8)"
        ],
        "title": "Time evolution coefficient for basic creep",
        "description": "The time evolution coefficient for basic creep describes how basic creep progresses over time and accounts for the age of concrete at the time of loading. This coefficient reflects the gradual accumulation of basic creep deformation influenced by the time elapsed since loading.",
        "latexSymbol": "\\beta_{bc,t-t0}",
        "latexEquation": "\\ln{((\\frac{30}{\\sym{t_{0,adj}}} + 0.035)^{2} \\times (t - \\sym{t_{0}}) + 1)}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_20",
            "G38_COMP_2",
            "G38_COMP_3"
        ]
    },
    {
        "id": "G38_COMP_8",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.9)"
        ],
        "title": "Drying creep coefficient",
        "description": "The drying creep coefficient represents the component of creep deformation in concrete that results from moisture loss over time. It is influenced by factors such as concrete strength, ambient humidity, age at loading, and the notional size of the concrete element, reflecting how drying conditions contribute to overall creep behavior.",
        "latexSymbol": "\\phi_{dc}(t,t_{0})",
        "latexEquation": "\\sym{\\beta_{dc,fcm}} \\times \\sym{\\beta_{dc,RH}} \\times \\sym{\\beta_{dc,t0}} \\times \\sym{\\beta_{dc,t-t0}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_9",
            "G38_COMP_10",
            "G38_COMP_11",
            "G38_COMP_12"
        ]
    },
    {
        "id": "G38_COMP_9",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.10)"
        ],
        "title": "Concrete strength coefficient for drying creep",
        "description": "The concrete strength coefficient for drying creep accounts for the effect of concrete strength on its drying creep behavior. Lower concrete strength results in a higher value for this coefficient, indicating increased susceptibility to drying-related creep deformation.",
        "latexSymbol": "\\beta_{dc,fcm}",
        "latexEquation": "\\frac{412}{\\sym{f_{cm,28}}^{1.4}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_6"
        ]
    },
    {
        "id": "G38_COMP_10",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.11)"
        ],
        "title": "Relative humidity coefficient for drying creep",
        "description": "The relative humidity coefficient for drying creep accounts for the effect of ambient relative humidity on the drying creep behavior of concrete. Lower humidity increases this coefficient, indicating a greater potential for drying-related creep deformation.",
        "latexSymbol": "\\beta_{dc,RH}",
        "latexEquation": "\\frac{(1 - \\frac{\\sym{RH}}{100})}{\\sqrt[3]{0.1 \\times \\frac{\\sym{h_{n}}}{100}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_16",
            "G38_COMP_17"
        ]
    },
    {
        "id": "G38_COMP_11",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.12)"
        ],
        "title": "Loading age coefficient for drying creep",
        "description": "The loading age coefficient for drying creep accounts for the effect of the concrete’s age at the time of loading on its drying creep behavior. This coefficient adjusts for the reduced susceptibility to drying-related creep deformation as the concrete's age at loading increases.",
        "latexSymbol": "\\beta_{dc,t0}",
        "latexEquation": "\\frac{1}{(0.1 + \\sym{t_{0,adj}}^{0.2})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_20"
        ]
    },
    {
        "id": "G38_COMP_12",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.13)"
        ],
        "title": "Time evolution coefficient for drying creep",
        "description": "The time evolution coefficient for drying creep describes how drying creep progresses over time, taking into account the effects of the concrete’s notional size and age at loading.",
        "latexSymbol": "\\beta_{dc,t-t0}",
        "latexEquation": "(\\frac{\\sym{t} - \\sym{t_{0}}}{\\sym{\\beta_{h}} + (t - t_{0})})^{\\sym{\\gamma(t_{0,adj})}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_2",
            "G38_COMP_3",
            "G38_COMP_14",
            "G38_COMP_13"
        ]
    },
    {
        "id": "G38_COMP_13",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.14)"
        ],
        "title": "Age adjustment coefficient for drying creep",
        "description": "The age adjustment coefficient for drying creep reflects how the adjusted age at loading influences the rate of drying creep over time. This coefficient accounts for the maturity of concrete at loading, with higher maturity levels leading to a slower progression of drying-related creep.",
        "latexSymbol": "\\gamma(t_{0,adj})",
        "latexEquation": "\\frac{1}{2.3 + \\frac{3.5}{\\sqrt{\\sym{t_{0,adj}}}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_20"
        ]
    },
    {
        "id": "G38_COMP_14",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.15)"
        ],
        "title": "Size and strength coefficient for drying creep",
        "description": "The size and strength coefficient for drying creep accounts for the effects of the concrete element's notional size and concrete strength on the time development of drying creep. Larger element sizes and lower concrete strength increase this coefficient, leading to a greater impact on drying-related creep over time.",
        "latexSymbol": "\\beta_{h}",
        "latexEquation": "\\min(1.5 \\times \\sym{h_{n}} + 250 \\times \\sym{\\alpha_{fcm}} , 1500 \\times \\sym{\\alpha_{fcm}})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_17",
            "G38_COMP_15"
        ]
    },
    {
        "id": "G38_COMP_15",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(3)"
        ],
        "title": "Strength adjustment coefficient for drying creep",
        "description": "The strength adjustment coefficient for drying creep accounts for the influence of concrete strength on the progression of drying creep over time. Lower concrete strength leads to a higher value for this coefficient, indicating increased sensitivity to drying-related creep deformation as time advances.",
        "latexSymbol": "\\alpha_{fcm}",
        "latexEquation": "(\\frac{35}{\\sym{f_{cm,28}}})^{0.5}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_6"
        ]
    },
    {
        "id": "G38_COMP_16",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(3)"
        ],
        "title": "Relative humidity of the ambient environment",
        "description": "Relative humidity of the ambient environment refers to the percentage of moisture present in the surrounding air relative to the air's maximum moisture-holding capacity at a given temperature. This humidity level directly influences concrete’s drying behavior.",
        "latexSymbol": "RH",
        "type": "number",
        "unit": "%",
        "notation": "standard",
        "decimal": 0,
        "default": 80.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G38_COMP_17",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(3)"
        ],
        "title": "Notional size of concrete member",
        "description": "The notional size of a concrete member represents an effective dimension used to estimate drying and creep behavior. It is calculated based on the cross-sectional area and the perimeter exposed to the atmosphere, helping to assess the influence of member size on moisture-related deformation.",
        "latexSymbol": "h_{n}",
        "latexEquation": "\\frac{(2 \\times \\sym{A_{c}})}{\\sym{u}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_18",
            "G38_COMP_19"
        ]
    },
    {
        "id": "G38_COMP_18",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(3)"
        ],
        "title": "Cross-sectional area of concrete member",
        "description": "The cross-sectional area of a concrete member refers to the surface area of a section cut perpendicular to its length, representing the size of the concrete’s cross-section.",
        "latexSymbol": "A_{c}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 3,
        "default": 534694.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G38_COMP_19",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(3)"
        ],
        "title": "Perimeter of concrete member exposed to atmosphere",
        "description": "The perimeter of a concrete member exposed to the atmosphere represents the length around the surface area of the section that is in direct contact with the surrounding environment. This measurement is used to assess the exposure of the concrete to drying conditions.",
        "latexSymbol": "u",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 5921.89,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G38_COMP_20",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.17)"
        ],
        "title": "Adjusted concrete age at loading for strength class",
        "description": "The adjusted concrete age at loading for strength class represents the concrete’s age when load is applied, modified to reflect the specific strength class of cement.",
        "latexSymbol": "t_{0,adj}",
        "latexEquation": "\\max(\\sym{t_{0,T}} \\times [\\frac{9}{(2 + \\sym{t_{0,T}}^{1.2})} + 1]^{\\sym{\\alpha_{SC}}} , 0.5)",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_22",
            "G38_COMP_21"
        ]
    },
    {
        "id": "G38_COMP_21",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(4)"
        ],
        "title": "Exponent for strength class on adjusted loading age",
        "description": "The exponent for strength class on adjusted loading age accounts for the effect of cement strength class on the adjusted loading age, reflecting differences in early strength development due to cement type.",
        "latexSymbol": "\\alpha_{SC}",
        "latexEquation": "-1",
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
                    "-1"
                ],
                [
                    "0"
                ],
                [
                    "1"
                ]
            ]
        }
    },
    {
        "id": "G38_COMP_22",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(B.18)"
        ],
        "title": "Temperature-adjusted concrete age at loading",
        "description": "The temperature-adjusted concrete age at loading represents the concrete’s age when load is first applied, adjusted to reflect the temperature at that time. This adjusted age specifically accounts for temperature effects on concrete maturity at the point of loading.",
        "latexSymbol": "t_{0,T}",
        "latexEquation": "\\sym{\\Delta{t_{i}}} \\times \\exp(13.65 - \\frac{4000}{273 + \\sym{T(\\Delta{t_{i}})}})",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G38_COMP_23",
            "G38_COMP_24"
        ]
    },
    {
        "id": "G38_COMP_23",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(5)"
        ],
        "title": "Duration of temperature exposure",
        "description": "The duration of temperature exposure refers to the length of time a specific temperature is maintained during the curing process of concrete. This value is used to calculate the temperature-adjusted concrete age over the curing period.",
        "latexSymbol": "\\Delta{t_{i}}",
        "latexEquation": "\\sym{t_{0}}",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G38_COMP_3"
        ]
    },
    {
        "id": "G38_COMP_24",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.5(5)"
        ],
        "title": "Mean concrete temperature during exposure period",
        "description": "The mean concrete temperature during the exposure period refers to the average temperature of the concrete during a specific time period of curing. This temperature is used to adjust the concrete’s age for the effects of temperature on its maturity.",
        "latexSymbol": "T(\\Delta{t_{i}})",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 1,
        "default": 10.0,
        "useStd": False
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/131433536/2G+EN1992-1-1+Total+Mean+Creep+Coefficient
        'id': '38',
        'standardType': '2G:EUROCODE',
        'codeName': '2G:EN1992-1-1',
        'codeTitle': 'Eurocode 2 — Design of concrete structures - Part 1-1: General rules and rules for buildings, bridges and civil engineering structures',
        'title': 'Total Mean Creep Coefficient Calculation Guide',
        'description': r"[2G:EN1992-1-1] This guide provides a detailed procedure for calculating the total mean creep coefficient of concrete based on Eurocode 2nd Generation standards. It explains how to calculate the basic creep coefficient and drying creep coefficient, and then combine them to determine the total mean creep coefficient. The guide offers step-by-step instructions on how to calculate the creep coefficient, considering factors like concrete age, temperature, and humidity, using specific formulas and parameters defined by Eurocode.",
        'edition': '2023',
        'targetComponents': ['G38_COMP_1', 'G38_COMP_4', 'G38_COMP_8'],
        'testInput': [
            {'component': 'G37_COMP_4', 'value': 'C20/25'},
            {'component': 'G37_COMP_27', 'value': 'CS'},
            {'component': 'G38_COMP_2', 'value': 36500},
            {'component': 'G38_COMP_3', 'value': 7},
            {'component': 'G38_COMP_16', 'value': 80},
            {'component': 'G38_COMP_18', 'value': 534694},
            {'component': 'G38_COMP_19', 'value': 5921.89},
            {'component': 'G38_COMP_24', 'value': 10},
        ],
    }
]
