# Code > Ref > Symbol 계층 구조는 어디서나 공통
# description 과 같은 파라미터에 필요한 추가 정보는 openapi schema의 규칙을 따라야 함
# 참조 https://swagger.io/docs/specification/data-models/keywords/
# https://www.learnjsonschema.com/2020-12/

SERVER_URL = 'https://moa.rpm.kr-dv-midasit.com/design-guide/figures'

def get_figure_server_url():
    return SERVER_URL


# List of operators
binary_operators = [r'\\pm', r'\\cdot', r'\\times', r'\\div', r'\\mod', r'\\land', r'\\lor', r'\\cup', r'\\cap', r'\\oplus']
relation_operators = [r'=', r'\\neq', r'\\leq', r'\\geq', r'<', r'>', r'\\approx', r'\\sim', r'\\equiv', r'\\subset', r'\\supset']
function_operators = [r'\\sin', r'\\cos', r'\\log', r'\\ln' r'\\lim', r'\\int', r'\\sum', r'\\left', r'\\right']

component_list = [
    {
        "id": "G1_COMP_1",
        "codeName": "EN1991-1-5",
        "reference": [
            "6.1.1(1)"
        ],
        "title": "Deck type selection",
        "description": "This section categorizes bridge decks into different types based on their material and structural design. The classification includes steel decks, composite decks, and concrete decks, each with distinct subtypes like steel box girders, concrete slabs, and concrete box girders.",
        "figureFile": "detail_g1_comp_11.png",
        "latexSymbol": "seldeck",
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
                    "steel box girder"
                ],
                [
                    "steel truss or plate girder"
                ],
                [
                    "composite deck"
                ],
                [
                    "concrete slab"
                ],
                [
                    "concrete beam"
                ],
                [
                    "concrete box girder"
                ]
            ]
        }
    },
    {
        "id": "G1_COMP_2",
        "codeName": "EN1991-1-5",
        "reference": [
            "6.1.1(1)"
        ],
        "title": "Bridge deck types",
        "description": "This section categorizes bridge decks into different types based on their material and structural design. The classification includes steel decks, composite decks, and concrete decks, each with distinct subtypes like steel box girders, concrete slabs, and concrete box girders.",
        "latexSymbol": "decktype",
        "type": "string",
        "unit": "",
        "notation": "text",
        "required": [
            "G1_COMP_1"
        ],
        "default": "Type1",
        "table": "text",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{seldeck} = steel box girder",
                    "\\sym{seldeck} = steel truss or plate girder",
                    "\\sym{seldeck} = composite deck",
                    "\\sym{seldeck} = concrete slab",
                    "\\sym{seldeck} = concrete beam",
                    "\\sym{seldeck} = concrete box girder"
                ]
            ],
            "data": [
                [
                    "Type1"
                ],
                [
                    "Type1"
                ],
                [
                    "Type2"
                ],
                [
                    "Type3"
                ],
                [
                    "Type3"
                ],
                [
                    "Type3"
                ]
            ]
        }
    },
    {
        "id": "G1_COMP_3",
        "codeName": "EN1991-1-5",
        "reference": [
            "AnnexA.1"
        ],
        "title": "The initial bridge temperature",
        "description": "The initial bridge temperature should be taken as the temperature of the structure at the time of restraint or completion. If unpredictable, the average temperature during construction should be used. The initial temperature may also be specified in the National Annex.",
        "latexSymbol": "T_{0}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 1,
        "limits": {
            "inMin": 0
        },
        "default": 10.0,
        "useStd": True
    },
    {
        "id": "G1_COMP_4",
        "codeName": "EN1991-1-5",
        "reference": [
            "1.5.3",
            "1.5.4"
        ],
        "title": "Return period",
        "description": "The return period refers to the number of years after which a specific event, like extreme temperatures, is statistically expected to occur. In Eurocode, the default return period is set to 50 years, but this can be adjusted depending on project requirements or specified in the Annex A.",
        "latexSymbol": "p_{years}",
        "type": "number",
        "unit": "years",
        "notation": "standard",
        "decimal": 0,
        "limits": {
            "exMin": 0
        },
        "default": 50.0,
        "useStd": True
    },
    {
        "id": "G1_COMP_5",
        "codeName": "EN1991-1-5",
        "reference": [
            "1.6"
        ],
        "title": "Annual exceedance probability",
        "description": "The Annual Exceedance Probability is the probability that a specific event, such as an extreme temperature, will be exceeded in a given year. It is calculated as the inverse of the return period. For example, if the return period is 50 years, the annual exceedance probability is 1/50, or 0.02 (2%). This value helps assess the likelihood of rare events occurring within any given year and is crucial for determining the appropriate safety measures in structural design.",
        "latexSymbol": "p",
        "latexEquation": "\\frac{1}{\\sym{p_{years}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G1_COMP_4"
        ]
    },
    {
        "id": "G1_COMP_6",
        "codeName": "EN1991-1-5",
        "reference": [
            "6.1.3.2(1)P"
        ],
        "title": "Minimum shade air temperature (exceedance probability 0.02)",
        "description": "The minimum shade air temperatures with an annual probability of being exceeded of 0.02 represents the lowest expected air temperature that has a 2% chance of being exceeded in any given year. This corresponds to a return period of 50 years. These values are typically derived from national maps of isotherms and are often specified in the National Annex for structural design.",
        "latexSymbol": "T_{min}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "default": -17,
        "useStd": False
    },
    {
        "id": "G1_COMP_7",
        "codeName": "EN1991-1-5",
        "reference": [
            "6.1.3.2(1)P"
        ],
        "title": "Maximum shade air temperature (exceedance probability 0.02)",
        "description": "The maximum shade air temperatures with an annual probability of being exceeded of 0.02 refers to the highest expected air temperature that has a 2% chance of being exceeded in any given year, equivalent to a 50-year return period. These values are derived from national maps of isotherms and are often specified in the National Annex for use in structural design.",
        "latexSymbol": "T_{max}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "default": 34,
        "useStd": False
    },
    {
        "id": "G1_COMP_8",
        "codeName": "EN1991-1-5",
        "reference": [
            "AnnexA.2(2)"
        ],
        "title": "Minimum shade air temperature with exceedance probability p",
        "description": "The minimum shade air temperature represents the temperature with an annual probability of being exceeded by p, which is different from the standard 0.02 exceedance probability. This value corresponds to a return period of 1/p years, meaning it reflects the minimum air temperature expected to be exceeded once every 1/p years on average, depending on the chosen probability. These values are critical for projects that require specific safety measures based on local climate conditions.",
        "latexSymbol": "T_{min,p}",
        "latexEquation": "\\sym{T_{min}} \\times \\left( \\sym{k_{3}} + \\sym{k_{4}} \\times \\ln \\left[ - \\ln \\left( 1 - \\sym{p} \\right) \\right] \\right)",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G1_COMP_6",
            "G1_COMP_12",
            "G1_COMP_13",
            "G1_COMP_5"
        ]
    },
    {
        "id": "G1_COMP_9",
        "codeName": "EN1991-1-5",
        "reference": [
            "AnnexA.2(2)"
        ],
        "title": "Maximum shade air temperature with exceedance probability p",
        "description": "The maximum shade air temperature represents the temperature with an annual probability of being exceeded by p, which differs from the standard exceedance probability of 0.02. This value is associated with a return period of 1/p years, meaning it reflects the highest air temperature expected to be exceeded once every 1/p years on average. These values are crucial for projects requiring adjustments based on local climate conditions to ensure the structural safety of the design.",
        "latexSymbol": "T_{max,p}",
        "latexEquation": "\\sym{T_{max}} \\times \\left( \\sym{k_{1}} - \\sym{k_{2}} \\times \\ln \\left[ - \\ln \\left( 1 - \\sym{p} \\right) \\right] \\right)",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G1_COMP_7",
            "G1_COMP_10",
            "G1_COMP_11",
            "G1_COMP_5"
        ]
    },
    {
        "id": "G1_COMP_10",
        "codeName": "EN1991-1-5",
        "reference": [
            "AnnexA.2(2)"
        ],
        "title": "Coefficient for maximum shade air temperature",
        "description": "This coefficient is used for calculating the maximum air temperature with a specified probability (p). It depends on the variation coefficient and can be modified using meteorological data for the mean value and standard deviation.",
        "latexSymbol": "k_{1}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 0.781,
        "const": True
    },
    {
        "id": "G1_COMP_11",
        "codeName": "EN1991-1-5",
        "reference": [
            "AnnexA.2(2)"
        ],
        "title": "Scaling factor for maximum shade air temperature",
        "description": "This coefficient serves as a scaling factor for the maximum air temperature calculation. It is influenced by the variation coefficient and can be adjusted by meteorological data.",
        "latexSymbol": "k_{2}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 0.056,
        "const": True
    },
    {
        "id": "G1_COMP_12",
        "codeName": "EN1991-1-5",
        "reference": [
            "AnnexA.2(2)"
        ],
        "title": "Coefficient for minimum shade air temperature",
        "description": "This coefficient is used to calculate the minimum (negative) air temperature with a specified probability (p). It relates to the variation coefficient for negative temperatures and can be modified using meteorological data.",
        "latexSymbol": "k_{3}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 0.393,
        "const": True
    },
    {
        "id": "G1_COMP_13",
        "codeName": "EN1991-1-5",
        "reference": [
            "AnnexA.2(2)"
        ],
        "title": "Scaling factor for minimum shade air temperature",
        "description": "Similar to k2, this coefficient scales the calculation for minimum (negative) air temperatures. It is based on the variation coefficient for negative temperatures and can be adjusted using meteorological data.",
        "latexSymbol": "k_{4}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": -0.156,
        "const": True
    },
    {
        "id": "G1_COMP_14",
        "codeName": "EN1991-1-5",
        "reference": [
            "6.1.3.1(Figure6.1)"
        ],
        "title": "Minimum uniform bridge temperature component",
        "description": "The minimum uniform bridge temperature component represents the lowest temperature that a bridge structure can uniformly experience. It should be determined based on local climatic conditions and national guidelines. The values are typically derived from a correlation with the minimum shade air temperature. National Annexes may specify exact values, and recommended ranges are provided.",
        "latexSymbol": "T_{e,min}",
        "latexEquation": "\\sym{T_{min,p}} - 3",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G1_COMP_2",
            "G1_COMP_8"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{decktype} = Type1",
                    "\\sym{decktype} = Type2",
                    "\\sym{decktype} = Type3"
                ]
            ],
            "data": [
                [
                    "\\sym{T_{min,p}} - 3"
                ],
                [
                    "\\sym{T_{min,p}} + 4"
                ],
                [
                    "\\sym{T_{min,p}} + 8"
                ]
            ]
        }
    },
    {
        "id": "G1_COMP_15",
        "codeName": "EN1991-1-5",
        "reference": [
            "6.1.3.1(Figure6.1)"
        ],
        "title": "Maximum uniform bridge temperature component",
        "description": "The maximum uniform bridge temperature component represents the highest temperature that a bridge structure can uniformly experience. Like the minimum uniform temperature, it is determined based on local climate and national guidelines. This component is correlated with the maximum shade air temperature. The National Annex may provide specific values, and appropriate ranges are suggested.",
        "latexSymbol": "T_{e,max}",
        "latexEquation": "\\sym{T_{max,p}} + 16",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G1_COMP_2",
            "G1_COMP_9"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{decktype} = Type1",
                    "\\sym{decktype} = Type2",
                    "\\sym{decktype} = Type3"
                ]
            ],
            "data": [
                [
                    "\\sym{T_{max,p}} - 16"
                ],
                [
                    "\\sym{T_{max,p}} + 4"
                ],
                [
                    "\\sym{T_{max,p}} + 2"
                ]
            ]
        }
    },
    {
        "id": "G1_COMP_16",
        "codeName": "EN1991-1-5",
        "reference": [
            "6.1.3.3(3)"
        ],
        "title": "Maximum contraction range of a uniform bridge temperature",
        "description": "The maximum contraction range of a uniform bridge temperature component represents the temperature difference between the initial bridge temperature and the minimum uniform bridge temperature. This value reflects how much the bridge may contract as its temperature drops from the initial temperature to the minimum operational temperature.",
        "latexSymbol": "\\Delta{T_{N,con}}",
        "latexEquation": "\\sym{T_{0}} - \\sym{T_{e,min}}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G1_COMP_3",
            "G1_COMP_14"
        ]
    },
    {
        "id": "G1_COMP_17",
        "codeName": "EN1991-1-5",
        "reference": [
            "6.1.3.3(3)"
        ],
        "title": "Maximum expansion range of a uniform bridge temperature",
        "description": "The maximum expansion range of a uniform bridge temperature represents the temperature difference between the maximum uniform bridge temperature and the initial bridge temperature. This value indicates how much the bridge may expand as its temperature increases from the initial temperature to the maximum operational temperature.",
        "latexSymbol": "\\Delta{T_{N,exp}}",
        "latexEquation": "\\sym{T_{e,max}} - \\sym{T_{0}}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G1_COMP_15",
            "G1_COMP_3"
        ]
    },
    {
        "id": "G2_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.2(5.1)"
        ],
        "title": "Geometrical imperfections in bridge",
        "description": "Inclination caused by geometrical imperfections refers to the initial deviation in the structure's alignment due to fabrication or construction errors. It affects the stability of structural members like girders, piers, and arches, and must be accounted for in design to ensure the bridge's overall stability under load. For bridge-specific details, refer to EN1992-2(5.101).",
        "latexSymbol": "\\theta_{i}",
        "latexEquation": "\\sym{\\theta_{0}} \\times \\sym{\\alpha_{h}}",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G2_COMP_2",
            "G2_COMP_3"
        ]
    },
    {
        "id": "G2_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.2(5)"
        ],
        "title": "Basic value of initial imperfections in bridge",
        "description": "The basic value of initial imperfections in bridge structures represents the initial deviation or inclination due to construction or fabrication inaccuracies. This value, often specified in national standards, is typically set as 1/200 and serves as the foundation for calculating the overall imperfections in structural members such as girders, piers, and arches.",
        "latexSymbol": "\\theta_{0}",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "default": 0.005,
        "const": True
    },
    {
        "id": "G2_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.2(5)"
        ],
        "title": "Reduction factor for height or length in bridge",
        "description": "The reduction factor for height or length in bridge structures is used to adjust the basic value of initial imperfections. This factor accounts for the length or height of structural elements like girders, piers, or arches, ensuring that imperfections are scaled appropriately based on the size of the structure. For more detailed information, refer to EN1992-2(5.2).",
        "latexSymbol": "\\alpha_{h}",
        "latexEquation": "\\min \\left( \\frac{2}{\\sqrt{\\sym{l}}}, 1 \\right)",
        "type": "number",
        "unit": "rad",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G2_COMP_4"
        ]
    },
    {
        "id": "G2_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.2(5)"
        ],
        "title": "Length or height of structural members in bridge design",
        "description": "The length or height of structural members is used to calculate the reduction factor for geometrical imperfections, reflecting the actual size of elements like girders, piers, and arches in bridge design.",
        "latexSymbol": "l",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 30,
        "useStd": False
    },
    {
        "id": "G2_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.2(5.2)"
        ],
        "title": "Eccentricity due to geometrical imperfections in isolated members",
        "description": "In bridge design, eccentricity due to geometrical imperfections in isolated members refers to the deviation of the structural axis, which results in additional bending moments. This provides a simplified way to account for imperfections in structural analysis, particularly in compression elements like columns and girders.",
        "latexSymbol": "e_{i}",
        "latexEquation": "\\sym{\\theta_{i}} \\times \\left( \\frac{\\sym{l_{0}}}{2} \\right)",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G2_COMP_1",
            "G2_COMP_8"
        ]
    },
    {
        "id": "G2_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.2(7)"
        ],
        "title": "Transverse force due to imperfections in isolated members",
        "description": "The transverse force due to imperfections in isolated members refers to the lateral force applied at the position that creates the maximum moment. This force accounts for geometrical imperfections such as initial deflections and is used to ensure accurate buckling analysis in structural design.",
        "latexSymbol": "H_{i}",
        "latexEquation": "\\sym{N} \\times \\sym{e_{i}} \\times \\left( \\frac{4}{\\sym{l}} \\right)",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G6_COMP_2",
            "G2_COMP_4",
            "G2_COMP_5",
            "G2_COMP_7"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{buckmode} = Pinned Ends",
                    "\\sym{buckmode} = Free - Fixed Ends",
                    "\\sym{buckmode} = Pinned - Fixed Ends",
                    "\\sym{buckmode} = Fixed Ends",
                    "\\sym{buckmode} = Guided - Fixed Ends"
                ]
            ],
            "data": [
                [
                    "\\sym{N} \\times \\sym{e_{i}} \\times \\left( \\frac{4}{\\sym{l}} \\right)"
                ],
                [
                    "\\sym{N} \\times \\sym{e_{i}} \\times \\left( \\frac{1}{\\sym{l}} \\right)"
                ],
                [
                    "\\sym{N} \\times \\sym{e_{i}} \\times \\left( \\frac{16}{3 \\times \\sym{l}} \\right)"
                ],
                [
                    "\\sym{N} \\times \\sym{e_{i}} \\times \\left( \\frac{8}{\\sym{l}} \\right)"
                ],
                [
                    "\\sym{N} \\times \\sym{e_{i}} \\times \\left( \\frac{2}{\\sym{l}} \\right)"
                ]
            ]
        }
    },
    {
        "id": "G2_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.2(7)"
        ],
        "title": "Axial load in isolated members",
        "description": "Axial load in isolated members refers to the vertical or compressive force applied along the axis of a structural element. This load is crucial in analyzing buckling behavior, as it interacts with imperfections such as initial deflection or inclination, affecting the stability of the member.",
        "latexSymbol": "N",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 0
        },
        "default": 650,
        "useStd": False
    },
    {
        "id": "G2_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.2(7)"
        ],
        "title": "Effective length",
        "description": "The effective length of isolated members refers to the length used in buckling analysis to represent the portion of a structural member that is free to buckle under load. This length depends on the boundary conditions, such as pinned, fixed, or free ends. It is essential for predicting when and how isolated members, like girders or columns, will buckle. For more detailed information, please refer to Section 5.8.3.2 (Figure 5.7).",
        "latexSymbol": "l_{0}",
        "latexEquation": "\\sym{l}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G6_COMP_2",
            "G2_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{buckmode} = Pinned Ends",
                    "\\sym{buckmode} = Free - Fixed Ends",
                    "\\sym{buckmode} = Pinned - Fixed Ends",
                    "\\sym{buckmode} = Fixed Ends",
                    "\\sym{buckmode} = Guided - Fixed Ends"
                ]
            ],
            "data": [
                [
                    "\\sym{l}"
                ],
                [
                    "2 \\times \\sym{l}"
                ],
                [
                    "0.7 \\times \\sym{l}"
                ],
                [
                    "0.5 \\times \\sym{l}"
                ],
                [
                    "\\sym{l}"
                ]
            ]
        }
    },
    {
        "id": "G3_COMP_1",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.2(4.1)"
        ],
        "title": "Basic wind velocity",
        "description": "The basic wind velocity refers to the mean wind speed calculated over a 10-minute period at a height of 10 meters above the ground in terrain with minimal vegetation and few obstacles. It takes into account factors like wind direction and the time of year and is adjusted using directional and seasonal factors.",
        "latexSymbol": "v_{b}",
        "latexEquation": "\\sym{c_{dir}} \\times \\sym{c_{season}} \\times \\sym{v_{b,0}} \\times \\sym{c_{prob}}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_3",
            "G3_COMP_4",
            "G3_COMP_2",
            "G3_COMP_5"
        ]
    },
    {
        "id": "G3_COMP_2",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.2(1)P"
        ],
        "title": "Fundamental wind velocity",
        "description": "The fundamental wind velocity is the baseline 10-minute mean wind speed measured at a height of 10 meters above open terrain with minimal vegetation and few obstacles. It is the starting point for calculating the basic wind velocity, before applying any adjustments for wind direction or season. The value is typically provided in national standards.",
        "latexSymbol": "v_{b,0}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 27,
        "useStd": False
    },
    {
        "id": "G3_COMP_3",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.2(2)P"
        ],
        "title": "Wind directional adjustment factor",
        "description": "The directional factor is a coefficient that adjusts the basic wind velocity based on the wind direction. It accounts for the variability in wind speeds depending on which direction the wind is coming from. The value of this factor may vary depending on national standards, but a common recommended value is 1.0.",
        "latexSymbol": "c_{dir}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G3_COMP_4",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.2(2)P"
        ],
        "title": "Seasonal adjustment factor",
        "description": "The seasonal adjustment factor accounts for changes in wind speed due to seasonal variations. It modifies the basic wind velocity to reflect different wind conditions throughout the year. The recommended value is often 1.0, indicating no adjustment for seasons.",
        "latexSymbol": "c_{season}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G3_COMP_5",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.2(4.2)"
        ],
        "title": "Wind probability adjustment factor",
        "description": "The wind probability adjustment factor modifies the basic wind velocity based on the likelihood of extreme wind speeds occurring within a given year. It adjusts the wind speed to account for the probability of these events, using specific statistical parameters related to the distribution of extreme values. These parameters are typically provided in national standards.",
        "latexSymbol": "c_{prob}",
        "latexEquation": "\\left( \\frac{ \\left(1 - \\sym{K} \\times \\ln \\left( -\\ln \\left(1 - \\sym{p} \\right) \\right) \\right) }{ 1 - \\sym{K} \\times \\ln \\left(-\\ln \\left( 0.98 \\right) \\right) } \\right)^{\\sym{n}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_8",
            "G3_COMP_9",
            "G3_COMP_7"
        ]
    },
    {
        "id": "G3_COMP_6",
        "codeName": "EN1991-1-4",
        "reference": [
            "3.4(1)"
        ],
        "title": "Mean return period",
        "description": "The mean return period is the average time interval over which a specific wind event (like a wind speed) is expected to be exceeded once. A mean return period of 50 years indicates that the wind speed is likely to be exceeded once every 50 years on average.",
        "latexSymbol": "p_{years}",
        "type": "number",
        "unit": "years",
        "notation": "standard",
        "decimal": 0,
        "limits": {
            "exMin": 0
        },
        "default": 50,
        "useStd": True
    },
    {
        "id": "G3_COMP_7",
        "codeName": "EN1991-1-4",
        "reference": [
            "3.4(1)"
        ],
        "title": "Annual exceedance probability",
        "description": "This refers to the likelihood that a specific wind speed will be exceeded in any given year. An annual probability of exceedence of 0.02 means there is a 2% chance that the wind speed will exceed this value in one year.",
        "latexSymbol": "p",
        "latexEquation": "\\frac{1}{(\\sym{p_{years}})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_6"
        ]
    },
    {
        "id": "G3_COMP_8",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.2(2)P"
        ],
        "title": "Wind speed shape parameter for extreme events",
        "description": "The wind speed shape parameter for extreme events is a statistical coefficient that characterizes the distribution of extreme wind speeds. It influences the adjustment of the probability factor, reflecting the variability and likelihood of extreme wind conditions. This parameter is typically determined based on the variation in wind speed data and is provided in national standards.",
        "latexSymbol": "K",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 0.2,
        "const": True
    },
    {
        "id": "G3_COMP_9",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.2(2)P"
        ],
        "title": "Exponent for wind probability adjustment",
        "description": "The exponent for wind probability adjustment is a factor used to modify the probability factor in wind speed calculations. It determines the degree of influence that the probability of extreme wind events has on the adjusted wind velocity.",
        "latexSymbol": "n",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 0.5,
        "const": True
    },
    {
        "id": "G3_COMP_10",
        "codeName": "EN1991-1-4",
        "reference": [
            "5.1(Table5.1)"
        ],
        "title": "Reference height above ground",
        "description": "The reference height is the maximum height above ground for the section being considered. This height is used in wind load calculations to determine the peak wind velocity and other wind-related forces acting on the structure.",
        "latexSymbol": "z_{e}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 0
        },
        "default": 6,
        "useStd": False
    },
    {
        "id": "G3_COMP_11",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.3.1(1)"
        ],
        "title": "Height above ground level",
        "description": "The height above ground level refers to the vertical distance from the ground where wind speed measurements or calculations are taken. It is a key parameter in determining wind velocity, as wind speed varies with height due to changes in terrain roughness and other factors.",
        "latexSymbol": "z",
        "latexEquation": "\\min \\left(\\sym{z_{e}}, \\sym{z_{max}} \\right)",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_10",
            "G3_COMP_20"
        ]
    },
    {
        "id": "G3_COMP_12",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.3.1(4.3)"
        ],
        "title": "Mean wind velocity at height",
        "description": "The mean wind velocity at height refers to the average wind speed at a specific height above the ground. This value is influenced by factors such as the roughness of the terrain, the topography (orography), and the basic wind velocity. It is calculated using the roughness and orography adjustment factors, which modify the wind speed to reflect the effects of the surrounding environment at different heights.",
        "latexSymbol": "v_{m}(z)",
        "latexEquation": "\\sym{c_{r}(z)} \\times \\sym{c_{o}(z)} \\times \\sym{v_{b}}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_14",
            "G3_COMP_13",
            "G3_COMP_1"
        ]
    },
    {
        "id": "G3_COMP_13",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.3.1(1)"
        ],
        "title": "Orography adjustment factor for mean wind speed",
        "description": "The orography adjustment factor for mean wind speed takes into account the effects of terrain features such as hills or valleys on wind speed at various heights. It adjusts the mean wind speed based on these topographical variations. Typically, the value is set to 1.0 unless specified otherwise in national standards, indicating no adjustment for orography.",
        "latexSymbol": "c_{o}(z)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G3_COMP_14",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.3.2(4.4)"
        ],
        "title": "Terrain roughness factor for mean wind velocity",
        "description": "The terrain roughness factor adjusts the mean wind velocity to account for changes in wind speed caused by the roughness of the terrain and the height above the ground. It is determined using a logarithmic formula and varies based on the roughness of the terrain and specific height.",
        "latexSymbol": "c_{r}(z)",
        "latexEquation": "\\sym{k_{r}} \\times \\ln \\left(\\frac{\\sym{z_{min}}}{\\sym{z_{0}}} \\right)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_11",
            "G3_COMP_17",
            "G3_COMP_16",
            "G3_COMP_18"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{z} <= \\sym{z_{min}}",
                    "\\sym{z} > \\sym{z_{min}}"
                ]
            ],
            "data": [
                [
                    "\\sym{k_{r}} \\times \\ln \\left(\\frac{\\sym{z_{min}}}{\\sym{z_{0}}} \\right)"
                ],
                [
                    "\\sym{k_{r}} \\times \\ln \\left(\\frac{z}{\\sym{z_{0}}} \\right)"
                ]
            ]
        }
    },
    {
        "id": "G3_COMP_15",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.3.2(Table4.1)"
        ],
        "title": "Terrain category selection",
        "description": "This section allows the user to choose the appropriate terrain category based on the characteristics of the surrounding area. Terrain categories are used to define the roughness of the ground, which affects wind speed calculations. Options typically range from open terrain with low vegetation to urban environments with numerous obstacles.",
        "figureFile": "detail_g3_comp_15.png",
        "latexSymbol": "terrain",
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
                    "[0] Sea or coastal area exposed to the open sea",
                    "Areas directly exposed to the open sea, such as coastal regions with no protection from land (e.g., oceanfront cliffs or beaches)."
                ],
                [
                    "[I] Lakes or flat and horizontal area with negligible vegetation and without obstacles",
                    "Flat, open areas like large lakes or plains with minimal vegetation and no significant obstacles (e.g., flat open fields or dried-up lakebeds)."
                ],
                [
                    "[II] Area with low vegetation such as grass and isolated obstacles (trees, buildings) with separations of at least 20 obstacle heights",
                    "Areas with low vegetation like grasslands or farmland, with occasional obstacles such as trees or buildings, separated by at least 20 times their height (e.g., rural fields with scattered farmhouses)."
                ],
                [
                    "[III] Area with regular cover of vegetation or buildings or with isolated obstacles with separations of maximum 20 obstacle heights (such as villages, suburban \\sym{terrain}, permanent forest)",
                    "Areas with a regular cover of vegetation or buildings, such as suburban areas or forests, with obstacles like trees or houses spaced up to 20 times their height (e.g., villages or small towns surrounded by forests)."
                ],
                [
                    "[IV] Area in which at least 15 % of the surface is covered with buildings and their average height exceeds 15 m",
                    "Urbanized areas where at least 15% of the ground surface is covered by tall buildings, typically over 15 meters in height (e.g., city centers with skyscrapers or densely built industrial zones)."
                ]
            ]
        }
    },
    {
        "id": "G3_COMP_16",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.3.2(Table4.1)"
        ],
        "title": "Roughness length for terrain",
        "description": "The roughness length is a parameter that represents the height above ground level where the wind speed theoretically becomes zero due to surface roughness. It is used in the calculation of the terrain roughness factor and depends on the type of terrain. The value of the roughness length varies according to different terrain categories.",
        "latexSymbol": "z_{0}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_15"
        ],
        "default": 0.003,
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{terrain} = [0] Sea or coastal area exposed to the open sea",
                    "\\sym{terrain} = [I] Lakes or flat and horizontal area with negligible vegetation and without obstacles",
                    "\\sym{terrain} = [II] Area with low vegetation such as grass and isolated obstacles (trees, buildings) with separations of at least 20 obstacle heights",
                    "\\sym{terrain} = [III] Area with regular cover of vegetation or buildings or with isolated obstacles with separations of maximum 20 obstacle heights (such as villages, suburban \\sym{terrain}, permanent forest)",
                    "\\sym{terrain} = [IV] Area in which at least 15 % of the surface is covered with buildings and their average height exceeds 15 m"
                ]
            ],
            "data": [
                [
                    "0.003"
                ],
                [
                    "0.010"
                ],
                [
                    "0.050"
                ],
                [
                    "0.300"
                ],
                [
                    "1.000"
                ]
            ]
        }
    },
    {
        "id": "G3_COMP_17",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.3.2(Table4.1)"
        ],
        "title": "Minimum height for roughness factor calculation",
        "description": "The minimum height is the lowest height above the ground at which the roughness factor is applicable. Below this height, the roughness factor remains constant. The value of the minimum height is determined by the terrain category and is used in the calculation of wind speed adjustments.",
        "latexSymbol": "z_{min}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G3_COMP_15"
        ],
        "default": 1,
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{terrain} = [0] Sea or coastal area exposed to the open sea",
                    "\\sym{terrain} = [I] Lakes or flat and horizontal area with negligible vegetation and without obstacles",
                    "\\sym{terrain} = [II] Area with low vegetation such as grass and isolated obstacles (trees, buildings) with separations of at least 20 obstacle heights",
                    "\\sym{terrain} = [III] Area with regular cover of vegetation or buildings or with isolated obstacles with separations of maximum 20 obstacle heights (such as villages, suburban \\sym{terrain}, permanent forest)",
                    "\\sym{terrain} = [IV] Area in which at least 15 % of the surface is covered with buildings and their average height exceeds 15 m"
                ]
            ],
            "data": [
                [
                    "1"
                ],
                [
                    "1"
                ],
                [
                    "2"
                ],
                [
                    "5"
                ],
                [
                    "10"
                ]
            ]
        }
    },
    {
        "id": "G3_COMP_18",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.3.2(4.5)"
        ],
        "title": "Terrain factor for roughness calculation",
        "description": "The terrain factor is a coefficient used in the calculation of the roughness factor, reflecting the influence of the terrain's roughness length. It depends on the ratio between the roughness length of the terrain and the standard roughness length for a reference terrain (terrain category II). This factor helps adjust wind speed based on different terrain conditions.",
        "latexSymbol": "k_{r}",
        "latexEquation": "0.19 \\times \\left( \\frac{\\sym{z_{0}}}{\\sym{z_{0,II}}} \\right) ^ {0.07}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_16",
            "G3_COMP_19"
        ]
    },
    {
        "id": "G3_COMP_19",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.3.2(Table4.1)"
        ],
        "title": "Reference roughness length for terrain category II",
        "description": "The reference roughness length for terrain category II is a standard value used as a baseline for calculating the terrain factor in wind speed assessments. It represents the roughness length for open terrain with low vegetation, typically set at 0.05 meters. This value is used to compare other terrain roughness lengths and adjust the wind speed accordingly.",
        "latexSymbol": "z_{0,II}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 2,
        "default": 0.05,
        "const": True
    },
    {
        "id": "G3_COMP_20",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.3.2(1)"
        ],
        "title": "Maximum height for roughness factor calculation",
        "description": "The maximum height is the highest altitude above ground where the roughness factor is considered in wind speed calculations. Above this height, the roughness factor does not apply. For most cases, the maximum height is set at 200 meters, unless otherwise specified.",
        "latexSymbol": "z_{max}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 1,
        "default": 200,
        "const": True
    },
    {
        "id": "G3_COMP_21",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.5(4.8)"
        ],
        "title": "Standard deviation of wind turbulence",
        "description": "The peak velocity pressure at height accounts for both the mean wind velocity and short-term wind fluctuations at a specific height above the ground. It is calculated using the air density, mean wind velocity, and an exposure factor, which reflects the terrain and other local conditions. The peak velocity pressure helps in determining the wind loads on structures.",
        "latexSymbol": "\\sigma_{v}",
        "latexEquation": "\\sym{k_{r}} \\times \\sym{v_{b}} \\times \\sym{k_{l}}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_18",
            "G3_COMP_1",
            "G3_COMP_22"
        ]
    },
    {
        "id": "G3_COMP_22",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.4(1)"
        ],
        "title": "Turbulence factor",
        "description": "The turbulence factor is a coefficient used in the calculation of wind turbulence intensity. It accounts for the variability of turbulence in different wind conditions and terrains. The value of the turbulence factor may be specified in national standards, with a commonly recommended value being 1.0. This factor adjusts the standard deviation of wind turbulence in relation to the basic wind velocity.",
        "latexSymbol": "k_{l}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G3_COMP_23",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.4(4.7)"
        ],
        "title": "Turbulence intensity at height",
        "description": "Turbulence intensity at height is the ratio of the standard deviation of wind turbulence to the mean wind velocity at a specific height. It measures the level of wind speed fluctuations due to turbulence. The value of turbulence intensity depends on the terrain roughness and height above ground. It is calculated using a formula that incorporates factors such as the roughness length and orography.",
        "latexSymbol": "I_{v}(z)",
        "latexEquation": "\\frac{\\sym{k_{l}}}{\\sym{c_{o}(z)} \\times \\ln \\left( \\frac{\\sym{z_{min}}}{\\sym{z_{0}}} \\right)}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_22",
            "G3_COMP_13",
            "G3_COMP_11",
            "G3_COMP_17",
            "G3_COMP_16"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{z} < \\sym{z_{min}}",
                    "\\sym{z} >= \\sym{z_{min}}"
                ]
            ],
            "data": [
                [
                    "\\frac{\\sym{k_{l}}}{\\sym{c_{o}(z)} \\times \\ln \\left( \\frac{\\sym{z_{min}}}}{\\sym{z_{0}}} \\right)}"
                ],
                [
                    "\\frac{\\sym{k_{l}}}{\\sym{c_{o}(z)} \\times \\ln \\left( \\frac{z}{\\sym{z_{0}}} \\right)}"
                ]
            ]
        }
    },
    {
        "id": "G3_COMP_24",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.5(4.8)"
        ],
        "title": "Peak velocity pressure at height",
        "description": "The peak velocity pressure at height accounts for both the mean wind velocity and short-term wind fluctuations at a specific height above the ground. It is calculated using the air density, mean wind velocity, and an exposure factor, which reflects the terrain and other local conditions. The peak velocity pressure helps in determining the wind loads on structures.",
        "latexSymbol": "q_{p}(z)",
        "latexEquation": "\\left[ 1 + 7 \\times \\sym{I_{v}(z)}  \\right] \\cdot \\frac{1}{2} \\times \\sym{\\rho} \\times \\sym{v_{m}(z)}^{2} \\times 10^{-3}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_23",
            "G3_COMP_25",
            "G3_COMP_12"
        ]
    },
    {
        "id": "G3_COMP_25",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.5(1)"
        ],
        "title": "Air density during wind storms",
        "description": "Air density during wind storms is a crucial factor in wind load calculations, as it depends on altitude, temperature, and barometric pressure expected in the region during extreme wind events. This parameter affects the calculation of peak velocity pressure and can vary with changing atmospheric conditions.",
        "latexSymbol": "\\rho",
        "type": "number",
        "unit": "kg/m^3",
        "notation": "standard",
        "decimal": 3,
        "default": 1.25,
        "const": True
    },
    {
        "id": "G3_COMP_26",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.5(4.9)"
        ],
        "title": "Exposure factor at heigh",
        "description": "The exposure factor at height adjusts the peak velocity pressure based on the height above ground and the surrounding terrain conditions. It reflects the influence of terrain roughness and exposure to wind, varying with the type of terrain and height. This factor helps modify the peak wind pressure to better represent real-world conditions at different elevations.",
        "latexSymbol": "c_{e}(z)",
        "latexEquation": "\\frac{\\sym{q_{p}(z)}}{\\sym{q_{b}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_24",
            "G3_COMP_27"
        ]
    },
    {
        "id": "G3_COMP_27",
        "codeName": "EN1991-1-4",
        "reference": [
            "4.5(4.10)"
        ],
        "title": "Basic velocity pressure",
        "description": "The basic velocity pressure represents the wind pressure at a given location based on the basic wind velocity. It is calculated using air density and the square of the basic wind velocity. This value serves as a reference for further adjustments when calculating the peak velocity pressure at different heights or under different terrain conditions.",
        "latexSymbol": "q_{b}",
        "latexEquation": "\\left( \\frac{1}{2} \\times \\sym{\\rho} \\times \\sym{v_{b}}^{2} \\right) \\times 10^{-3}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_25",
            "G3_COMP_1"
        ]
    },
    {
        "id": "G4_COMP_1",
        "codeName": "EN1991-1-1",
        "reference": [
            "AnnexA"
        ],
        "title": "Density Type",
        "description": "'Density Type' clearly categorizes the different forms of density, such as 'Mass Density' and 'Weight Density.' This title helps distinguish between how density is expressed, whether as mass per unit volume (kg/m³) or weight per unit volume (kN/m³), ensuring clarity in the table.",
        "latexSymbol": "densitytype",
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
                    "Weight density (kN/m^{3})"
                ],
                [
                    "Mass density (kg/m^{3})"
                ]
            ]
        }
    },
    {
        "id": "G4_COMP_2",
        "codeName": "EN1991-1-1",
        "reference": [
            "AnnexA"
        ],
        "title": "Gravity acceleration",
        "description": "Gravity acceleration is applied to convert weight density to mass density. The value of gravity acceleration follows Eurocode standards. Detailed information can be found in EN 1998-1 Section 1.7.",
        "latexSymbol": "g",
        "type": "number",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 3,
        "default": "9.81",
        "const": True
    },
    {
        "id": "G4_COMP_3",
        "codeName": "EN1991-1-1",
        "reference": [
            "AnnexA"
        ],
        "title": "kN to kg unit converter",
        "description": "This logic converts between kilonewtons (kN) and kilograms (kg) by applying gravitational acceleration, offering an efficient way to handle force and mass conversions.",
        "latexSymbol": "kntokg",
        "latexEquation": "1",
        "type": "number",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G4_COMP_1",
            "G4_COMP_2"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{densitytype} = Weight density (kN/m^{3})",
                    "\\sym{densitytype} = Mass density (kg/m^{3})"
                ]
            ],
            "data": [
                [
                    "1"
                ],
                [
                    "1000/\\sym{g}"
                ]
            ]
        }
    },
    {
        "id": "G4_COMP_4",
        "codeName": "EN1991-1-1",
        "reference": [
            "AnnexA(Table A.1)"
        ],
        "title": "Density of concrete material",
        "description": "This menu provides the density corresponding to the selected type of concrete, allowing users to easily find the appropriate density for normal weight, reinforced, or pre-stressed concrete.",
        "latexSymbol": "conmater",
        "type": "object",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G4_COMP_3"
        ],
        "table": "result",
        "tableDetail": {
            "data": [
                [
                    "Concrete Type",
                    "Density"
                ],
                [
                    "Normal weight concrete",
                    "24 \\times \\sym{kntokg}"
                ],
                [
                    "Normal weight reinforced concrete",
                    "25 \\times \\sym{kntokg}"
                ],
                [
                    "Normal weight pre-stressed concrete",
                    "25 \\times \\sym{kntokg}"
                ],
                [
                    "(unhardened)Normal weight concrete",
                    "25 \\times \\sym{kntokg}"
                ],
                [
                    "(unhardened)Normal weight reinforced concrete",
                    "26 \\times \\sym{kntokg}"
                ],
                [
                    "(unhardened)Normal weight pre-stressed concrete",
                    "26 \\times \\sym{kntokg}"
                ]
            ]
        }
    },
    {
        "id": "G4_COMP_5",
        "codeName": "EN1991-1-1",
        "reference": [
            "AnnexA(Table A.6)"
        ],
        "title": "Pavement of road bridges",
        "description": "This section provides the density values for different types of asphalt used in road bridge pavements, including Guss Asphalt for waterproofing and bridge decks, Mastic Asphalt for dense and smooth surfaces, and Hot Rolled Asphalt (HRA) for durable, wear-resistant applications.",
        "latexSymbol": "paveroad",
        "type": "object",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G4_COMP_3"
        ],
        "table": "result",
        "tableDetail": {
            "data": [
                [
                    "Pavement Type",
                    "Density"
                ],
                [
                    "Gussasphalt and asphaltic concrete",
                    "24 \\times \\sym{kntokg} \\text{~} 25 \\times \\sym{kntokg}"
                ],
                [
                    "Mastic asphalt",
                    "18 \\times \\sym{kntokg} \\text{~} 22 \\times \\sym{kntokg}"
                ],
                [
                    "Hot rolled asphalt",
                    "23 \\times \\sym{kntokg}"
                ]
            ]
        }
    },
    {
        "id": "G4_COMP_6",
        "codeName": "EN1991-1-1",
        "reference": [
            "AnnexA(Table A.6)"
        ],
        "title": "Pavement of rail bridges",
        "description": "This section provides the density values for materials used in rail bridge pavements, including the concrete protective layer, normal ballast (e.g., granite, gneiss), and basaltic ballast. These materials are essential for ensuring the durability and stability of the bridge surface.",
        "latexSymbol": "paverail",
        "type": "object",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G4_COMP_3"
        ],
        "table": "result",
        "tableDetail": {
            "data": [
                [
                    "Pavement Type",
                    "Density"
                ],
                [
                    "concrete protective layer",
                    "25 \\times \\sym{kntokg}"
                ],
                [
                    "normal ballast (e.g. granite, gneiss, etc.)",
                    "20 \\times \\sym{kntokg}"
                ],
                [
                    "basaltic ballast",
                    "26 \\times \\sym{kntokg}"
                ]
            ]
        }
    },
    {
        "id": "G4_COMP_7",
        "codeName": "EN1991-1-1",
        "reference": [
            "AnnexA(Table A.6)"
        ],
        "title": "Infill for bridges",
        "description": "This section lists the density values for various infill materials used in bridge construction, including ballast, gravel (loose), hardcore, crushed slag, packed stone rubble, and puddle clay. These materials are essential for providing stability, drainage, and support in bridge structures.",
        "latexSymbol": "infillbridge",
        "type": "object",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G4_COMP_3"
        ],
        "table": "result",
        "tableDetail": {
            "data": [
                [
                    "Infill Material Type",
                    "Density"
                ],
                [
                    "sand (dry)",
                    "15 \\times \\sym{kntokg} \\text{~} 16 \\times \\sym{kntokg}"
                ],
                [
                    "ballast, gravel (loose)",
                    "15 \\times \\sym{kntokg} \\text{~} 16 \\times \\sym{kntokg}"
                ],
                [
                    "hardcore",
                    "18.5 \\times \\sym{kntokg} \\text{~} 19.5 \\times \\sym{kntokg}"
                ],
                [
                    "crushed slag",
                    "13.5 \\times \\sym{kntokg} \\text{~} 14.5 \\times \\sym{kntokg}"
                ],
                [
                    "packed stone rubble",
                    "20.5 \\times \\sym{kntokg} \\text{~} 21.5 \\times \\sym{kntokg}"
                ],
                [
                    "puddle clay",
                    "18.5 \\times \\sym{kntokg} \\text{~} 19.5 \\times \\sym{kntokg}"
                ]
            ]
        }
    },
    {
        "id": "G4_COMP_8",
        "codeName": "EN1991-1-1",
        "reference": [
            "AnnexA(Table A.6)"
        ],
        "title": "Structures with ballasted bed",
        "description": "This section provides the density values for various track components used in structures with ballasted beds, including 2 rails UIC 60, prestressed concrete sleepers with track fastenings, concrete sleepers with metal angle braces, and timber sleepers with track fastenings.",
        "latexSymbol": "wballa",
        "type": "object",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G4_COMP_3"
        ],
        "table": "result",
        "tableDetail": {
            "data": [
                [
                    "Track Components",
                    "Density"
                ],
                [
                    "2 rails UIC 60",
                    "1.2 \\times \\sym{kntokg}"
                ],
                [
                    "prestressed concrete sleeper with track fastenings",
                    "4.8 \\times \\sym{kntokg}"
                ],
                [
                    "timber sleepers with track fastenings",
                    "1.9 \\times \\sym{kntokg}"
                ]
            ]
        }
    },
    {
        "id": "G4_COMP_9",
        "codeName": "EN1991-1-1",
        "reference": [
            "AnnexA(Table A.6)"
        ],
        "title": "Structures without ballasted bed",
        "description": "This section provides the density values for components used in structures without a ballasted bed, including 2 rails UIC 60 with track fastenings, bridge beams, and guard rails.",
        "latexSymbol": "woballa",
        "type": "object",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G4_COMP_3"
        ],
        "table": "result",
        "tableDetail": {
            "data": [
                [
                    "Track Components",
                    "Density"
                ],
                [
                    "2 rails UIC 60 with track fastenings",
                    "1.7 \\times \\sym{kntokg}"
                ],
                [
                    "bridge beam and guard rails",
                    "4.9 \\times \\sym{kntokg}"
                ]
            ]
        }
    },
    {
        "id": "G5_COMP_1",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.2(8.2)"
        ],
        "title": "Wind force acting in the x-direction on bridges",
        "description": "The wind force acting in the x-direction on bridges refers to the horizontal wind load exerted perpendicular to the bridge span. This force impacts the width of the deck and is influenced by factors such as basic wind speed, air density, and the shape of the bridges. It is calculated to ensure the structural integrity of the bridges under wind pressure. When wind forces and traffic loads occur simultaneously, adjustments are made to account for both effects to maintain safety.",
        "latexSymbol": "F_{w}",
        "latexEquation": "\\frac{1}{2} \\times \\sym{\\rho} \\times \\sym{v_{b}}^{2} \\times C \\times \\sym{A_{ref,x}} \\times 10^{-3}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_25",
            "G3_COMP_1",
            "G5_COMP_2",
            "G5_COMP_5"
        ]
    },
    {
        "id": "G5_COMP_2",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.2(1)"
        ],
        "title": "Wind load factor acting on bridges",
        "description": "The wind load factor adjusts the wind pressure on a bridge based on its exposure to wind and aerodynamic shape. It combines the effects of the exposure and shape factors to ensure accurate calculation of wind forces.",
        "latexSymbol": "C",
        "latexEquation": "\\sym{c_{e}(z)} \\times \\sym{c_{f,x}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_26",
            "G5_COMP_3"
        ]
    },
    {
        "id": "G5_COMP_3",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.1(8.1)"
        ],
        "title": "Force coefficient in the x-direction",
        "description": "The force coefficient in the x-direction represents the wind resistance on a bridge deck from wind acting perpendicular to the span. For standard bridges, it is usually taken as 1.3, or determined from charts. Special cases may apply for steep wind angles or multiple bridge decks.",
        "latexSymbol": "c_{f,x}",
        "latexEquation": "\\sym{c_{fx,0}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G5_COMP_4"
        ]
    },
    {
        "id": "G5_COMP_4",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.1(1)"
        ],
        "title": "Base force coefficient in the x-direction",
        "description": "The base force coefficient in the x-direction represents the wind resistance of a bridge deck without considering free-end flow. It can either be taken as 1.3 for standard bridges, or calculated based on the b/d_{tot} ratio.",
        "latexSymbol": "c_{fx,0}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.3,
        "const": True
    },
    {
        "id": "G5_COMP_5",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.1(Figure8.3)"
        ],
        "title": "Reference area in the x-direction",
        "description": "The reference area in the x-direction is calculated by multiplying the total depth of the bridge deck by the length of the bridge. This area represents the surface exposed to wind forces acting perpendicular to the span and is used in wind load calculations.",
        "latexSymbol": "A_{ref,x}",
        "latexEquation": "\\sym{d_{tot}} \\times \\sym{L}",
        "type": "number",
        "unit": "m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G5_COMP_10",
            "G5_COMP_6"
        ]
    },
    {
        "id": "G5_COMP_6",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.1(Figure8.3)"
        ],
        "title": "Length of the bridge",
        "description": "The length of the bridge, denoted as L, refers to the horizontal distance measured along the span of the bridge from one end to the other. This dimension is important in wind load calculations, as it helps determine the surface area of the bridge exposed to wind forces, particularly in the x and z directions. The length L is used to calculate the reference areas for wind loads acting on the bridge deck.",
        "latexSymbol": "L",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 10,
        "useStd": False
    },
    {
        "id": "G5_COMP_7",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.1(Table8.1)"
        ],
        "title": "Depth of the bridge deck",
        "description": "The depth of the bridge deck refers to the vertical distance from the top surface of the deck to the bottom of the main supporting structure. It is essential for calculating the total depth of the bridge deck, considering additional components and traffic. This depth helps determine wind loads acting on the structure.",
        "latexSymbol": "d",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 1.9,
        "useStd": False
    },
    {
        "id": "G5_COMP_8",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.1(Table8.1)"
        ],
        "title": "Road restraint system options",
        "description": "This section lists different types of road restraint systems used on bridges, which include open parapets, solid parapets, and safety barriers. ",
        "latexSymbol": "restop",
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
                    "Open parapet or safety barrier"
                ],
                [
                    "Solid parapet or safety barrier"
                ],
                [
                    "Open parapet and safety barrier"
                ]
            ]
        }
    },
    {
        "id": "G5_COMP_9",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.1(Table8.1)"
        ],
        "title": "Parapet or barrier placement options",
        "description": "This section allows the user to select whether the parapet or safety barrier is placed on one side or both sides of the bridge. The placement affects the structural load distribution and wind load calculations.",
        "latexSymbol": "restpla",
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
                    "on one side"
                ],
                [
                    "on both sides"
                ]
            ]
        }
    },
    {
        "id": "G5_COMP_10",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.1(Table8.1)"
        ],
        "title": "Total depth for without traffic",
        "description": "This field allows users to input the total depth of the bridge deck when there is no traffic and safety restraints (such as parapets or barriers) are installed on one side and on both side of the bridge.",
        "latexSymbol": "d_{tot}",
        "latexEquation": "\\sym{d} + 0.3",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G5_COMP_8",
            "G5_COMP_9",
            "G5_COMP_7",
            "G5_COMP_11"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{restop} = Open parapet or safety barrier",
                    "\\sym{restop} = Solid parapet or safety barrier",
                    "\\sym{restop} = Open parapet and safety barrier"
                ],
                [
                    "\\sym{restpla} = on one side",
                    "\\sym{restpla} = on both sides"
                ]
            ],
            "data": [
                [
                    "\\sym{d} + 0.3",
                    "\\sym{d} + 0.6"
                ],
                [
                    "\\sym{d} + \\sym{d_{1}}",
                    "\\sym{d} + 2 \\times \\sym{d_{1}}"
                ],
                [
                    "\\sym{d} + 0.6",
                    "\\sym{d} + 1.2"
                ]
            ]
        }
    },
    {
        "id": "G5_COMP_11",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.1(Figure8.5)"
        ],
        "title": "Height for safety barriers or restraints",
        "description": "This refers to the height added to the total depth of the bridge deck to account for the presence of safety barriers, parapets, or other restraints. This value is used in wind load calculations when the structure includes such elements, increasing the overall height of the section exposed to wind forces.",
        "latexSymbol": "d_{1}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 0
        },
        "default": 4.24,
        "useStd": False
    },
    {
        "id": "G5_COMP_12",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.4(1)"
        ],
        "title": "Select bridge type",
        "description": "Users can select the type of bridge for wind load calculations. The two options available are Plated bridges, which refer to bridges with solid beams or girders, and Truss bridges, which are composed of connected elements forming triangular units. Each bridge type requires different wind load considerations due to its structure.",
        "latexSymbol": "bridgetype",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label"
                ],
                [
                    "Plated bridges"
                ],
                [
                    "Truss bridges"
                ]
            ]
        }
    },
    {
        "id": "G5_COMP_13",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.4(1)"
        ],
        "title": "Wind force acting in the y-direction on bridges",
        "description": "The wind force in the y-direction is the longitudinal wind load along the span of the bridge, calculated as 25% of the x-direction wind force for plated bridges and 50% for truss bridges.",
        "latexSymbol": "F_{w,y}",
        "latexEquation": "0.25 \\times \\sym{F_{w}}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G5_COMP_12",
            "G5_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{bridgetype} = Plated bridges",
                    "\\sym{bridgetype} = Truss bridges"
                ]
            ],
            "data": [
                [
                    "0.25 \\times \\sym{F_{w}}"
                ],
                [
                    "0.5 \\times \\sym{F_{w}}"
                ]
            ]
        }
    },
    {
        "id": "G5_COMP_14",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.3(1)"
        ],
        "title": "Force coefficient in the z-direction",
        "description": "The force coefficient in the z-direction represents the wind forces acting vertically on a bridge deck, both upwards (lift) and downwards. It accounts for factors like deck slope, terrain slope, and wind direction fluctuations. The typical value is ±0.9, depending on whether the wind applies an upward or downward force.",
        "latexSymbol": "c_{f,z}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 0.9,
        "const": True
    },
    {
        "id": "G5_COMP_15",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.3(8.3)"
        ],
        "title": "Reference area in the z-direction",
        "description": "The reference area in the z-direction refers to the plan area of the bridge deck exposed to vertical wind forces. It is calculated by multiplying the width of the bridge deck by its length. This area is used to determine the wind load acting vertically (upward or downward) on the deck.",
        "latexSymbol": "A_{ref,z}",
        "latexEquation": "\\sym{b} \\times \\sym{L}",
        "type": "number",
        "unit": "m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G5_COMP_17",
            "G5_COMP_6"
        ]
    },
    {
        "id": "G5_COMP_16",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.3"
        ],
        "title": "Wind force acting in the z-direction on bridges",
        "description": "The wind force in the z-direction represents the vertical force exerted by wind on a bridge deck, either upward (lift) or downward. It is calculated using the air density, basic wind speed, force coefficient in the z-direction, and the reference area in the z-direction.",
        "latexSymbol": "F_{w,z}",
        "latexEquation": "\\frac{1}{2} \\times \\sym{\\rho} \\times \\sym{v_{b}}^{2} \\times \\sym{c_{f,z}} \\times \\sym{A_{ref,z}} \\times 10^{-3}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G3_COMP_25",
            "G3_COMP_1",
            "G5_COMP_14",
            "G5_COMP_15"
        ]
    },
    {
        "id": "G5_COMP_17",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.3.1(1)"
        ],
        "title": "Width of the bridge deck",
        "description": "The width of the bridge deck refers to the horizontal distance across the deck of the bridge, measured perpendicular to the direction of the span. It is an important dimension used in wind load calculations, as it determines the area exposed to wind forces acting in the x-direction.",
        "latexSymbol": "b",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 12.95,
        "useStd": False
    },
    {
        "id": "G6_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(5.14)"
        ],
        "title": "Slenderness ratio",
        "description": "The slenderness ratio is a dimensionless value that compares the effective length of a structural member to its radius of gyration. It indicates the likelihood of buckling in compression members, with higher values showing greater susceptibility to buckling.",
        "latexSymbol": "\\lambda",
        "latexEquation": "\\frac{\\sym{l_{0}}}{\\sym{i}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G6_COMP_3",
            "G6_COMP_5"
        ]
    },
    {
        "id": "G6_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(Figure5.7)"
        ],
        "title": "Buckling modes and boundary conditions",
        "description": "Buckling modes and boundary conditions describe how structural members behave under load based on their end restraints. Different conditions, such as pinned, fixed, or guided ends, affect the way a member experiences buckling.",
        "figureFile": "detail_g6_comp_2.png",
        "latexSymbol": "buckmode",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label"
                ],
                [
                    "Pinned Ends"
                ],
                [
                    "Free - Fixed Ends"
                ],
                [
                    "Pinned - Fixed Ends"
                ],
                [
                    "Fixed Ends"
                ],
                [
                    "Guided - Fixed Ends"
                ]
            ]
        }
    },
    {
        "id": "G6_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(Figure5.7)"
        ],
        "title": "Effective length of isolated members",
        "description": "The effective length of isolated members refers to the length used in buckling analysis to represent the portion of a structural member that is free to buckle under load. This length depends on the boundary conditions, such as pinned, fixed, or free ends. It is essential for predicting when and how isolated members, like girders or columns, will buckle.",
        "latexSymbol": "l_{0}",
        "latexEquation": "\\sym{l}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G6_COMP_2",
            "G6_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{buckmode} = Pinned Ends",
                    "\\sym{buckmode} = Free - Fixed Ends",
                    "\\sym{buckmode} = Pinned - Fixed Ends",
                    "\\sym{buckmode} = Fixed Ends",
                    "\\sym{buckmode} = Guided - Fixed Ends"
                ]
            ],
            "data": [
                [
                    "\\sym{l}"
                ],
                [
                    "2 \\times \\sym{l}"
                ],
                [
                    "0.7 \\times \\sym{l}"
                ],
                [
                    "0.5 \\times \\sym{l}"
                ],
                [
                    "\\sym{l}"
                ]
            ]
        }
    },
    {
        "id": "G6_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(3)"
        ],
        "title": "Clear height of compression member",
        "description": "The clear height refers to the vertical distance between the end restraints of a compression member. It represents the unsupported length of the member, which is critical in determining its slenderness and buckling behavior.",
        "latexSymbol": "l",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 14.5,
        "useStd": False
    },
    {
        "id": "G6_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(1)"
        ],
        "title": "Radius of gyration",
        "description": "The radius of gyration represents how a cross-sectional area is distributed around its centroid and is used to calculate a member's slenderness. It is calculated by dividing the second moment of area by the cross-sectional area and then taking the square root. A larger radius of gyration means the member is more resistant to buckling.",
        "latexSymbol": "i",
        "latexEquation": "\\sqrt{\\frac{\\sym{I}}{\\sym{A}}}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G6_COMP_8",
            "G6_COMP_7"
        ]
    },
    {
        "id": "G6_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(1)"
        ],
        "title": "Cross section type selection",
        "description": "This option allows the user to choose the type of cross section for which the slenderness ratio will be calculated. You can select either a circular section or a rectangular section, and the appropriate radius of gyration will be calculated accordingly.",
        "latexSymbol": "cosssect",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label"
                ],
                [
                    "circular"
                ],
                [
                    "rectangular"
                ]
            ]
        }
    },
    {
        "id": "G6_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(1)"
        ],
        "title": "Second moment of area of section",
        "description": "The second moment of area measures the distribution of a concrete section's area about a reference axis, representing its resistance to bending. A larger value means greater resistance to bending.",
        "latexSymbol": "I",
        "latexEquation": "\\frac{(\\pi \\times (\\frac{\\sym{D}}{1000})^{4})}{64}",
        "type": "number",
        "unit": "m^4",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G6_COMP_6",
            "G6_COMP_9",
            "G6_COMP_10",
            "G6_COMP_11"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{cosssect} = circular",
                    "\\sym{cosssect} = rectangular"
                ]
            ],
            "data": [
                [
                    "\\frac{(\\pi \\times (\\frac{\\sym{D}}{1000})^{4})}{64}"
                ],
                [
                    "\\frac{\\frac{\\sym{b}}{1000} \\times (\\frac{\\sym{h}}{1000})^{3}}{12}"
                ]
            ]
        }
    },
    {
        "id": "G6_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(1)"
        ],
        "title": "Cross-sectional area",
        "description": "The cross-sectional area represents the total area of a member's section that resists applied loads. For circular sections, it depends on the diameter, and for rectangular sections, it depends on the width and height.",
        "latexSymbol": "A",
        "latexEquation": "\\frac{\\pi \\times (\\frac{\\sym{D}}{1000})^{2}}{4}",
        "type": "number",
        "unit": "m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G6_COMP_6",
            "G6_COMP_9",
            "G6_COMP_10",
            "G6_COMP_11"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{cosssect} = circular",
                    "\\sym{cosssect} = rectangular"
                ]
            ],
            "data": [
                [
                    "\\frac{\\pi \\times (\\frac{\\sym{D}}{1000})^{2}}{4}"
                ],
                [
                    "\\frac{\\sym{b}}{1000} \\times \\frac{\\sym{h}}{1000}"
                ]
            ]
        }
    },
    {
        "id": "G6_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(1)"
        ],
        "title": "Diameter for circular sections",
        "description": "For circular sections, the diameter refers to the distance across the cross section, passing through its center. It is used to calculate the area of circular sections.",
        "latexSymbol": "D",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 550,
        "useStd": False
    },
    {
        "id": "G6_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(1)"
        ],
        "title": "Width for rectangular sections",
        "description": "For rectangular sections, the width refers to the horizontal dimension of the cross section. It is used along with the height to calculate the area of rectangular sections.",
        "latexSymbol": "b",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 250,
        "useStd": False
    },
    {
        "id": "G6_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.8.3.2(1)"
        ],
        "title": "Height for rectangular sections",
        "description": "For rectangular sections, the height refers to the vertical dimension of the cross section. It is used in combination with the width to calculate the area of rectangular sections.",
        "latexSymbol": "h",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 300,
        "useStd": False
    },
    {
        "id": "G7_COMP_1",
        "codeName": "EN1991-2",
        "reference": [
            "4.4.1(4.6)"
        ],
        "title": "Braking forces on road bridges",
        "description": "Braking forces on road bridges are longitudinal forces acting at the road surface level, caused by vehicles decelerating. These forces are calculated as a fraction of the maximum vertical loads from Load Model 1 applied to Lane 1. The braking force can be uniformly distributed along the axis of the lane, considering the length of the loaded deck.",
        "latexSymbol": "Q_{lk}",
        "latexEquation": "\\min(\\max(0.6 \\times \\sym{\\alpha_{Q1}} \\times (2 \\times \\sym{Q_{1k}}) + 0.10 \\times \\sym{\\alpha_{q1}} \\times \\sym{q_{1k}} \\times \\sym{w_{1}} \\times \\sym{L}, 180), 900)",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G7_COMP_10",
            "G7_COMP_16",
            "G7_COMP_13",
            "G7_COMP_11",
            "G7_COMP_5",
            "G7_COMP_3"
        ]
    },
    {
        "id": "G7_COMP_2",
        "codeName": "EN1991-2",
        "reference": [
            "4.4.1(5)"
        ],
        "title": "Acceleration forces on road bridges",
        "description": "Acceleration forces on road bridges are longitudinal forces acting at the road surface level, caused by vehicles accelerating. These forces act in the opposite direction to braking forces and are calculated in the same manner, based on the maximum vertical loads from Load Model 1 on Lane 1. The acceleration force may be distributed along the lane axis.",
        "latexSymbol": "Q_{ck}",
        "latexEquation": "-\\sym{Q_{lk}}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G7_COMP_1"
        ]
    },
    {
        "id": "G7_COMP_3",
        "codeName": "EN1991-2",
        "reference": [
            "4.4.1(2)"
        ],
        "title": "Length of the loaded deck",
        "description": "The length of the loaded deck refers to the portion of the bridge deck being considered for load application. It is a key factor in determining how forces, such as braking and acceleration, are distributed along the bridge. This length is used in load calculations to ensure the bridge can handle the forces generated by moving vehicles.",
        "latexSymbol": "L",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 35,
        "useStd": False
    },
    {
        "id": "G7_COMP_4",
        "codeName": "EN1991-2",
        "reference": [
            "4.2.3(1)"
        ],
        "title": "Carriageway width for road bridge",
        "description": "The carriageway width refers to the total width of the road surface between the kerbs or vehicle restraint systems on a road bridge. It excludes the width of any central reservations or the vehicle restraint systems themselves. This measurement is crucial for determining the number of notional lanes on the bridge and is a key factor in road bridge load calculations.",
        "latexSymbol": "w",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 11,
        "useStd": False
    },
    {
        "id": "G7_COMP_5",
        "codeName": "EN1991-2",
        "reference": [
            "4.2.3(Table4.1)"
        ],
        "title": "Width of notional lanes on a carriageway",
        "description": "The notional lane width is the assigned width for each lane on a road used for load distribution calculations in bridge design. It helps ensure even distribution of loads across lanes and is determined by the total width of the carriageway.",
        "latexSymbol": "w_{1}",
        "latexEquation": "3",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G7_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{w} < 5.4",
                    "5.4 <= \\sym{w} < 6",
                    "6 < \\sym{w}"
                ]
            ],
            "data": [
                [
                    "3"
                ],
                [
                    "\\frac{\\sym{w}}{2}"
                ],
                [
                    "3"
                ]
            ]
        }
    },
    {
        "id": "G7_COMP_6",
        "codeName": "EN1991-2",
        "reference": [
            "4.2.3(Table4.1)"
        ],
        "title": "Number of notional lanes on road bridges",
        "description": "The number of notional lanes on a road bridge represents the maximum number of lanes that can be assigned to the carriageway width. It is determined by dividing the total width of the carriageway by the standard width of a notional lane. This value is essential for calculating load distribution across the bridge.",
        "latexSymbol": "n_{1}",
        "latexEquation": "1",
        "type": "number",
        "unit": "ea",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G7_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{w} < 5.4",
                    "5.4 <= \\sym{w} < 6",
                    "6 < \\sym{w}"
                ]
            ],
            "data": [
                [
                    "1"
                ],
                [
                    "2"
                ],
                [
                    "\\lfloor \\frac{\\sym{w}}{3} \\rfloor"
                ]
            ]
        }
    },
    {
        "id": "G7_COMP_7",
        "codeName": "EN1991-2",
        "reference": [
            "4.4.2(Table4.3)"
        ],
        "title": "Centrifugal force on road bridges",
        "description": "Centrifugal force is a transverse force acting radially to the axis of the carriageway at the road surface level. It depends on the horizontal radius of the bridge and the total vertical load from vehicles.",
        "latexSymbol": "Q_{tk}",
        "type": "object",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G7_COMP_12",
            "G7_COMP_8"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{r} = 0",
                    "\\sym{r} < 200",
                    "200 <= \\sym{r} <= 1500",
                    "\\sym{r} > 1500"
                ]
            ],
            "data": [
                [
                    "0"
                ],
                [
                    "0.2 \\times \\sym{Q_{v}}"
                ],
                [
                    "\\frac{40 \\times \\sym{Q_{v}}}{\\sym{r}}"
                ],
                [
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G7_COMP_8",
        "codeName": "EN1991-2",
        "reference": [
            "4.4.2(2)"
        ],
        "title": "Horizontal radius of the carriageway",
        "description": "The horizontal radius of the carriageway refers to the radius of the curve along the bridge's centerline. It determines the magnitude of centrifugal forces, with smaller radii resulting in higher forces. When the radius exceeds 1500 meters, the centrifugal force becomes negligible due to the gentle curve.",
        "latexSymbol": "r",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 0
        },
        "default": 1500,
        "useStd": False
    },
    {
        "id": "G7_COMP_9",
        "codeName": "EN1991-2",
        "reference": [
            "4.4.2(4)"
        ],
        "title": "Transverse braking force on road bridges with radius",
        "description": "The transverse braking force is a lateral force that occurs due to skew braking or skidding, particularly on road bridges with a horizontal radius. It is calculated as 25% of the longitudinal braking or acceleration force and acts simultaneously with the longitudinal force, ensuring lateral stability on curved sections of the bridge.",
        "latexSymbol": "Q_{trk}",
        "latexEquation": "1",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G7_COMP_8",
            "G7_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{r} = 0",
                    "0 < \\sym{r} <= 1500",
                    "\\sym{r} > 1500"
                ]
            ],
            "data": [
                [
                    "0"
                ],
                [
                    "0.25 \\times \\sym{Q_{lk}}"
                ],
                [
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G7_COMP_10",
        "codeName": "EN1991-2",
        "reference": [
            "4.3.2(3)"
        ],
        "title": "Adjustment factor for uniformly distributed load  on lane 1",
        "description": "The adjustment factor for the uniformly distributed load on lane 1 is applied to modify the distributed load values in Load Model 1. This factor ensures that the distributed load on lane 1 reflects actual traffic conditions or specific design requirements, adjusting the load to better represent the traffic's effect on the bridge.",
        "latexSymbol": "\\alpha_{q1}",
        "type": "number",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G7_COMP_11",
        "codeName": "EN1991-2",
        "reference": [
            "4.3.2(Table4.2)"
        ],
        "title": "Uniformly distributed load for notional lane 1",
        "description": "The uniformly distributed load for notional lane 1 refers to the load per square meter applied across the lane in Load Model 1. This load represents the spread of traffic weight, such as that from congested or slow-moving vehicles, over the lane's surface. The load is distributed only over the areas where it creates unfavorable effects on the bridge.",
        "latexSymbol": "q_{1k}",
        "type": "number",
        "nuit": "kN/m^2",
        "notation": "standard",
        "decimal": 1,
        "default": 9.0,
        "const": True
    },
    {
        "id": "G7_COMP_12",
        "codeName": "EN1991-2",
        "reference": [
            "4.4.2(2)"
        ],
        "title": "Total vertical load from tandem systems",
        "description": "The total vertical load refers to the combined load from all tandem systems in Load Model 1, representing the sum of vertical concentrated loads applied to the bridge. This value indicates the maximum weight of vehicles distributed across notional lanes.",
        "latexSymbol": "Q_{v}",
        "latexEquation": "\\sym{\\alpha_{Q1}} \\times \\sym{Q_{1k}}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G7_COMP_6",
            "G7_COMP_13",
            "G7_COMP_16",
            "G7_COMP_14",
            "G7_COMP_17",
            "G7_COMP_15",
            "G7_COMP_18"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{n_{1}} = 1",
                    "\\sym{n_{1}} = 2",
                    "2 < \\sym{n_{1}}"
                ]
            ],
            "data": [
                [
                    "\\sym{\\alpha_{Q1}} \\times \\sym{Q_{1k}}"
                ],
                [
                    "\\sym{\\alpha_{Q1}} \\times \\sym{Q_{1k}} + \\sym{\\alpha_{Q2}} \\times \\sym{Q_{2k}}"
                ],
                [
                    "\\sym{\\alpha_{Q1}} \\times \\sym{Q_{1k}} + \\sym{\\alpha_{Q2}} \\times \\sym{Q_{2k}} + \\sym{\\alpha_{Q3}} \\times (\\sym{n_{1}} - 2)  \\times \\sym{Q_{3k}} \\times (\\sym{n_{1}} - 2)"
                ]
            ]
        }
    },
    {
        "id": "G7_COMP_13",
        "codeName": "EN1991-2",
        "reference": [
            "4.3.2(3)"
        ],
        "title": "Adjustment factor for tandem system on lane 1",
        "description": "The adjustment factor for the tandem load is applied to modify the concentrated load on notional lane 1 in Load Model 1. This factor adjusts the standard load values to account for variations in traffic conditions or design requirements, ensuring the loads reflect the actual traffic composition and bridge usage.",
        "latexSymbol": "\\alpha_{Q1}",
        "type": "number",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G7_COMP_14",
        "codeName": "EN1991-2",
        "reference": [
            "4.3.2(3)"
        ],
        "title": "Adjustment factor for tandem system on lane 2",
        "description": "The adjustment factor for the tandem load is applied to modify the concentrated load on notional lane 2 in Load Model 1.",
        "latexSymbol": "\\alpha_{Q2}",
        "type": "number",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G7_COMP_15",
        "codeName": "EN1991-2",
        "reference": [
            "4.3.2(3)"
        ],
        "title": "Adjustment factor for tandem system on lane 3 and beyond",
        "description": "The adjustment factor for the tandem load is applied to modify the concentrated load on notional lane 3 and beyond in Load Model 1. This factor adjusts the standard load values to account for variations in traffic conditions or design requirements, ensuring that the loads on the third lane and subsequent lanes accurately reflect the traffic composition and bridge usage.",
        "latexSymbol": "\\alpha_{Q3}",
        "type": "number",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G7_COMP_16",
        "codeName": "EN1991-2",
        "reference": [
            "4.3.2(Table4.2)"
        ],
        "title": "Tandem system load for notional lane 1",
        "description": "The load for notional lane 1 refers to the concentrated load from a tandem axle system applied to the first lane in Load Model 1. This load simulates the vertical forces from heavy vehicles. Each axle has two identical wheels, and the load is distributed equally across them, with a square contact surface for each wheel.",
        "latexSymbol": "Q_{1k}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 1,
        "default": 300.0,
        "const": True
    },
    {
        "id": "G7_COMP_17",
        "codeName": "EN1991-2",
        "reference": [
            "4.3.2(Table4.2)"
        ],
        "title": "Tandem system load for notional lane 2",
        "description": "The load for notional lane 2 refers to the concentrated load from a tandem axle system applied to the first lane in Load Model 1.",
        "latexSymbol": "Q_{2k}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 1,
        "default": 200.0,
        "const": True
    },
    {
        "id": "G7_COMP_18",
        "codeName": "EN1991-2",
        "reference": [
            "4.3.2(Table4.2)"
        ],
        "title": "Tandem system load for notional lane 3 and beyond",
        "description": "The load for notional lane 3 and beyond refers to the concentrated load from a tandem axle system applied to the third and subsequent lanes in Load Model 1. This load simulates the vertical forces from heavy vehicles. Each axle has two identical wheels, and the load is distributed equally across them, with a square contact surface for each wheel.",
        "latexSymbol": "Q_{3k}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 1,
        "default": 100.0,
        "const": True
    },
    {
        "id": "G8_COMP_1",
        "codeName": "EN1991-2",
        "reference": [
            "6.4.5.2(6.4)"
        ],
        "title": "Dynamic factor for carefully maintained tracks",
        "description": "The dynamic factor is used to account for the dynamic amplification effects caused by the speed and load of trains passing over a railway bridge. Specifically, this factor applies to well-maintained tracks and calculates the dynamic amplification based on the span length of the bridge.",
        "latexSymbol": "\\Phi_{2}",
        "latexEquation": "\\min(\\max(\\frac{1.44}{\\sqrt{\\sym{L_{\\Phi}}} - 0.2} + 0.82, 1.0), 1.67)",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_7"
        ]
    },
    {
        "id": "G8_COMP_2",
        "codeName": "EN1991-2",
        "reference": [
            "6.4.5.2(6.5)"
        ],
        "title": "Dynamic factor for standard maintained tracks",
        "description": "The dynamic factor is used to account for the dynamic amplification effects caused by the speed and load of trains passing over a railway bridge. This factor applies to tracks maintained at a standard level and calculates the dynamic amplification based on the span length of the bridge.",
        "latexSymbol": "\\Phi_{3}",
        "latexEquation": "\\min(\\max(\\frac{2.16}{\\sqrt{\\sym{L_{\\Phi}}} - 0.2} + 0.73, 1.0), 2.0)",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_7"
        ]
    },
    {
        "id": "G8_COMP_3",
        "codeName": "EN1991-2",
        "reference": [
            "6.4.5.3(Table6.2)"
        ],
        "title": "Total span length for multi-span main girder",
        "description": "The total span length for a multi-span main girder, denoted as Li, is the sum of all individual span lengths in a continuous main girder system. This combined length, from L1 to Ln, is crucial for calculating the mean span length, which is used in dynamic analysis and load distribution for multi-span main girders.",
        "latexSymbol": "L_{i}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 115,
        "useStd": False
    },
    {
        "id": "G8_COMP_4",
        "codeName": "EN1991-2",
        "reference": [
            "6.4.5.3(Table6.2)"
        ],
        "title": "Number of spans for continuous girders",
        "description": "The number of spans refers to how many spans are present in a continuous girder or slab system. It is used to calculate the mean span length, and this value helps determine the determinant length, which must not be less than the longest span.",
        "latexSymbol": "n",
        "type": "number",
        "unit": "ea",
        "notation": "standard",
        "decimal": 0,
        "limits": {
            "exMin": 1
        },
        "default": 5,
        "useStd": False
    },
    {
        "id": "G8_COMP_5",
        "codeName": "EN1991-2",
        "reference": [
            "6.4.5.3(Table6.2)"
        ],
        "title": "Multiplication factor for determinant length",
        "description": "The multiplication factor is used to adjust the mean span length to calculate the determinant length in continuous girder systems. This factor depends on the number of spans, increasing as the number of spans increases.",
        "latexSymbol": "k",
        "latexEquation": "1.2",
        "type": "number",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G8_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{n} = 2",
                    "\\sym{n} = 3",
                    "\\sym{n} = 4",
                    "\\sym{n} >= 5"
                ]
            ],
            "data": [
                [
                    "1.2"
                ],
                [
                    "1.3"
                ],
                [
                    "1.4"
                ],
                [
                    "1.5"
                ]
            ]
        }
    },
    {
        "id": "G8_COMP_6",
        "codeName": "EN1991-2",
        "reference": [
            "6.4.5.3(6.6)"
        ],
        "title": "Mean span length for continuous girders",
        "description": "The mean span length is the average length of continuous girders or slabs, calculated by summing all span lengths and dividing by the number of spans, and is used to determine the determinant length.",
        "latexSymbol": "L_{m}",
        "latexEquation": "\\frac{1}{\\sym{n}} \\times \\sym{L_{i}}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_4",
            "G8_COMP_3"
        ]
    },
    {
        "id": "G8_COMP_7",
        "codeName": "EN1991-2",
        "reference": [
            "6.4.5.3(6.7)"
        ],
        "title": "Determinant length for dynamic factors",
        "description": "The mean span length is the average length of continuous girders or slabs, calculated by summing all span lengths and dividing by the number of spans, and is used to determine the determinant length.",
        "latexSymbol": "L_{\\Phi}",
        "latexEquation": "\\min(\\max(\\sym{k} \\times \\sym{L_{m}}, 4), 100)",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_5",
            "G8_COMP_6"
        ]
    },
    {
        "id": "G8_COMP_8",
        "codeName": "EN1991-2",
        "reference": [
            "6.4.4(1)"
        ],
        "title": "Maximum line speed at the site",
        "description": "The maximum line speed at the site refers to the highest speed allowed for trains on a specific section of the railway track. It is crucial for evaluating dynamic effects on structures like bridges, ensuring they are designed to handle the expected train speeds safely.",
        "latexSymbol": "V",
        "type": "number",
        "unit": "km/h",
        "notation": "standard",
        "decimal": 1,
        "limits": {
            "exMin": 0
        },
        "default": 350,
        "useStd": False
    },
    {
        "id": "G8_COMP_9",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(3)P"
        ],
        "title": "Maximum permitted vehicle speed",
        "description": "The maximum permitted vehicle speed refers to the highest speed at which a train is allowed to travel over a specific section of track or a bridge. It plays a critical role in dynamic calculations, as higher speeds can lead to greater dynamic impacts on the structure, affecting both the design and safety assessments of the bridge.",
        "latexSymbol": "\\nu",
        "latexEquation": "\\frac{\\sym{V}}{\\frac{3600}{1000}}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_8"
        ]
    },
    {
        "id": "G8_COMP_10",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.2)"
        ],
        "title": "Dynamic factor for real trains on carefully maintained track (Upper Limit)",
        "description": "The dynamic factor for real trains on carefully maintained tracks (upper limit) accounts for reduced dynamic impacts in bridges with higher natural frequencies. It ensures accurate load evaluation by considering lower amplification effects due to better track conditions and faster train speeds on stiffer or shorter span bridges.",
        "latexSymbol": "(1+\\phi)_{2,U}",
        "latexEquation": "1 + \\sym{\\phi\\prime_{U}} + 0.5 \\times \\sym{\\phi\\prime\\prime_{U}}",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_14",
            "G8_COMP_16"
        ]
    },
    {
        "id": "G8_COMP_11",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.2)"
        ],
        "title": "Dynamic factor for real trains on carefully maintained track (Lower Limit)",
        "description": "The dynamic factor for real trains on carefully maintained tracks (lower limit) evaluates the reduced dynamic impacts in bridges with lower natural frequencies. It considers slower train speeds and the improved track conditions to ensure accurate load assessment in longer span or more flexible bridges.",
        "latexSymbol": "(1+\\phi)_{2,L}",
        "latexEquation": "1 + \\sym{\\phi\\prime_{L}} + 0.5 \\times \\sym{\\phi\\prime\\prime_{L}}",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_15",
            "G8_COMP_17"
        ]
    },
    {
        "id": "G8_COMP_12",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.1)"
        ],
        "title": "Dynamic factor for real trains on standard maintenance track (Upper Limit)",
        "description": "The dynamic factor for real trains on standard maintenance tracks (upper limit) reflects the increased dynamic impacts in bridges with higher natural frequencies. It ensures that the structure can manage the amplified stresses and vibrations caused by faster train speeds on tracks with standard maintenance, particularly in stiffer or shorter span bridges.",
        "latexSymbol": "(1+\\phi)_{3,U}",
        "latexEquation": "1 + \\sym{\\phi\\prime_{U}} + \\sym{\\phi\\prime\\prime_{U}}",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_14",
            "G8_COMP_16"
        ]
    },
    {
        "id": "G8_COMP_13",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.1)"
        ],
        "title": "Dynamic factor for real trains on standard maintenance track (Lower Limit)",
        "description": "The dynamic factor for real trains on standard maintenance tracks (upper limit) reflects the increased dynamic impacts in bridges with higher natural frequencies. It ensures that the structure can manage the amplified stresses and vibrations caused by faster train speeds on tracks with standard maintenance, particularly in stiffer or shorter span bridges.",
        "latexSymbol": "(1+\\phi)_{3,L}",
        "latexEquation": "1 + \\sym{\\phi\\prime_{L}} + \\sym{\\phi\\prime\\prime_{L}}",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_15",
            "G8_COMP_17"
        ]
    },
    {
        "id": "G8_COMP_14",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.3)",
            "AnnexC(C.4)"
        ],
        "title": "Speed-related dynamic component for upper limit",
        "description": "The speed-related dynamic component for the upper limit accounts for increased dynamic effects on bridges with higher natural frequencies, typically caused by faster trains. It ensures that the amplified impact of speed on these stiffer or shorter span bridges is accurately evaluated.",
        "latexSymbol": "\\phi\\prime_{U}",
        "latexEquation": "\\frac{\\sym{K_{U}}}{(1 - \\sym{K_{U}} + \\sym{K_{U}}^{4})}",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_18"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{K_{U}} < 0.76",
                    "\\sym{K_{U}} >= 0.76"
                ]
            ],
            "data": [
                [
                    "\\frac{\\sym{K_{U}}}{(1 - \\sym{K_{U}} + \\sym{K_{U}}^{4})}"
                ],
                [
                    "1.325"
                ]
            ]
        }
    },
    {
        "id": "G8_COMP_15",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.3)",
            "AnnexC(C.4)"
        ],
        "title": "Speed-related dynamic component for lower limit",
        "description": "The speed-related dynamic component for the lower limit evaluates the dynamic effects on bridges with lower natural frequencies, typically caused by slower trains. This ensures that the structure's response to lower speeds is accurately assessed, especially in longer span or more flexible bridges.",
        "latexSymbol": "\\phi\\prime_{L}",
        "latexEquation": "\\frac{\\sym{K_{L}}}{(1 - \\sym{K_{L}} + \\sym{K_{L}}^{4})}",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_19"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{K_{L}} < 0.76",
                    "\\sym{K_{L}} >= 0.76"
                ]
            ],
            "data": [
                [
                    "\\frac{\\sym{K_{L}}}{(1 - \\sym{K_{L}} + \\sym{K_{L}}^{4})}"
                ],
                [
                    "1.325"
                ]
            ]
        }
    },
    {
        "id": "G8_COMP_16",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.6)"
        ],
        "title": "Amplification-related dynamic component for upper limit",
        "description": "The amplification-related dynamic component for the upper limit accounts for additional dynamic effects in bridges with higher natural frequencies. It reflects the amplified dynamic impacts caused by the interaction between the train and the bridge, particularly in shorter span or stiffer bridges.",
        "latexSymbol": "\\phi\\prime\\prime_{U}",
        "latexEquation": "\\max(\\frac{\\sym{\\alpha_{v}}}{100} \\times (56 \\times \\exp(-(\\frac{\\sym{L_{\\Phi}}}{10})^{2}) + 50 \\times (\\frac{\\sym{L_{\\Phi}} \\times \\sym{n_{0,U}}}{80} - 1) \\times \\exp(-(\\frac{\\sym{L_{\\Phi}}}{20})^{2})),0)",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_20",
            "G8_COMP_7",
            "G8_COMP_21"
        ]
    },
    {
        "id": "G8_COMP_17",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.6)"
        ],
        "title": "Amplification-related dynamic component for lower limit",
        "description": "The amplification-related dynamic component for the lower limit evaluates the dynamic effects on bridges with lower natural frequencies. It assesses the additional impacts caused by train-bridge interaction, particularly in longer span or more flexible bridges.",
        "latexSymbol": "\\phi\\prime\\prime_{L}",
        "latexEquation": "\\max(\\frac{\\sym{\\alpha_{v}}}{100} \\times (56 \\times \\exp(-(\\frac{\\sym{L_{\\Phi}}}{10})^{2}) + 50 \\times (\\frac{\\sym{L_{\\Phi}} \\times \\sym{n_{0,L}}}{80} - 1) \\times \\exp(-(\\frac{\\sym{L_{\\Phi}}}{20})^{2})),0)",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_20",
            "G8_COMP_7",
            "G8_COMP_22"
        ]
    },
    {
        "id": "G8_COMP_18",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.5)"
        ],
        "title": "Speed-frequency ratio for upper limit condition",
        "description": "The speed-frequency ratio for the upper limit condition assesses potential dynamic amplification in bridges with higher natural frequencies, ensuring the structure can manage amplified dynamic loads caused by faster train speeds.",
        "latexSymbol": "K_{U}",
        "latexEquation": "\\frac{\\sym{\\nu}}{2\\times \\sym{L_{\\Phi}} \\times \\sym{n_{0,U}}}",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_9",
            "G8_COMP_7",
            "G8_COMP_21"
        ]
    },
    {
        "id": "G8_COMP_19",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.5)"
        ],
        "title": "Speed-frequency ratio for lower limit condition",
        "description": "The speed-frequency ratio for the lower limit condition evaluates dynamic amplification in bridges with lower natural frequencies, ensuring the structure can withstand dynamic effects at slower train speeds.",
        "latexSymbol": "K_{L}",
        "latexEquation": "\\frac{\\sym{\\nu}}{2\\times \\sym{L_{\\Phi}} \\times \\sym{n_{0,L}}}",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_9",
            "G8_COMP_7",
            "G8_COMP_22"
        ]
    },
    {
        "id": "G8_COMP_20",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.7)"
        ],
        "title": "Speed-related coefficient for dynamic effects",
        "description": "The speed-related coefficient is used to adjust the dynamic response of a structure based on the train's speed. Its role is to account for the increased dynamic impact that higher speeds can have on bridges, ensuring that the structure is properly assessed for the effects of moving loads at different speeds.",
        "latexSymbol": "\\alpha_{v}",
        "latexEquation": "1",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_9"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{\\nu} > 22",
                    "\\sym{\\nu} <= 22"
                ]
            ],
            "data": [
                [
                    "1"
                ],
                [
                    "\\frac{\\sym{\\nu}}{22}"
                ]
            ]
        }
    },
    {
        "id": "G8_COMP_21",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.8)"
        ],
        "title": "Upper limit of the first natural bending frequency",
        "description": "The upper limit of the first natural bending frequency represents the maximum frequency at which the bridge vibrates under permanent loads. It is used to evaluate the dynamic response of the bridge to train movements, ensuring that the structure is assessed for higher frequency vibrations that may occur in shorter span bridges or stiffer structures.",
        "latexSymbol": "n_{0,U}",
        "latexEquation": "94.76 \\times \\sym{L_{\\Phi}}^{-0.748}",
        "type": "number",
        "unit": "Hz",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_7"
        ]
    },
    {
        "id": "G8_COMP_22",
        "codeName": "EN1991-2",
        "reference": [
            "AnnexC(C.9)",
            "AnnexC(C.10)"
        ],
        "title": "Lower limit of the first natural bending frequency",
        "description": "The lower limit of the first natural bending frequency represents the minimum frequency at which the bridge vibrates under permanent loads. It is essential for evaluating the bridge's dynamic response to slower vibrations, which typically occur in longer span bridges or more flexible structures.",
        "latexSymbol": "n_{0,L}",
        "latexEquation": "23.58 \\times \\sym{L_{\\Phi}}^{-0.592}",
        "type": "number",
        "unit": "Hz",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_7"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "20 < \\sym{L_{\\Phi}}",
                    "20 >= \\sym{L_{\\Phi}}"
                ]
            ],
            "data": [
                [
                    "23.58 \\times \\sym{L_{\\Phi}}^{-0.592}"
                ],
                [
                    "\\frac{80}{\\sym{L_{\\Phi}}}"
                ]
            ]
        }
    },
    {
        "id": "G9_COMP_1",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.1(6.17)"
        ],
        "title": "Characteristic value of centrifugal force as concentrated load",
        "description": "The characteristic value of centrifugal force as a concentrated load represents the horizontal force acting at specific points on a bridge when a train moves along a curved track. This concentrated load is applied in the case of Load Model 71.",
        "latexSymbol": "Q_{tk}",
        "latexEquation": "\\frac{(\\frac{\\sym{V}}{3.6})^{2}}{(\\sym{g} \\times \\sym{r})}\\times (\\sym{f} \\times \\sym{Q_{vk}})",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_8",
            "G9_COMP_3",
            "G9_COMP_4",
            "G9_COMP_9",
            "G9_COMP_6"
        ]
    },
    {
        "id": "G9_COMP_2",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.1(6.18)"
        ],
        "title": "Characteristic value of centrifugal force as uniformly distributed load",
        "description": "The characteristic value of centrifugal force as a uniformly distributed load represents the horizontal force distributed along the length of a bridge when a train moves along a curved track. This uniformly distributed load is applied in the case of Load Model 71, SW/0, SW/2, and the unloaded train model.",
        "latexSymbol": "q_{tk}",
        "latexEquation": "\\frac{(\\frac{\\sym{V}}{3.6})^{2}}{(\\sym{g} \\times \\sym{r})}\\times (\\sym{f} \\times \\sym{q_{vk}})",
        "type": "number",
        "unit": "kN/m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_8",
            "G9_COMP_3",
            "G9_COMP_4",
            "G9_COMP_9",
            "G9_COMP_7"
        ]
    },
    {
        "id": "G9_COMP_3",
        "codeName": "EN1991-1-5",
        "reference": [
            "6.5.1(4)"
        ],
        "title": "Acceleration due to gravity",
        "description": "The acceleration due to gravity refers to the constant force that pulls objects towards the Earth. This value is used in engineering calculations, including those for railway bridges, to account for the influence of gravity on forces such as centrifugal forces.",
        "latexSymbol": "g",
        "type": "number",
        "unit": "m/s^2",
        "notation": "standard",
        "decimal": 2,
        "default": 9.81,
        "const": True
    },
    {
        "id": "G9_COMP_4",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.1(4)"
        ],
        "title": "Radius of curvature for railway bridges",
        "description": "The radius of curvature for railway bridges refers to the radius of the curve along which a railway track is laid on a bridge. It is a key factor in calculating centrifugal forces, as tighter curves (smaller radii) result in higher centrifugal forces on the bridge.",
        "latexSymbol": "r",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 0
        },
        "default": 1500,
        "useStd": False
    },
    {
        "id": "G9_COMP_5",
        "codeName": "EN1991-2",
        "reference": [
            "6.3.1(1)"
        ],
        "title": "Selection of railway traffic load models",
        "description": "This section outlines the selection criteria for railway traffic load models used in bridge analysis. Load Model LM71 (and SW/0 for continuous bridges) is used to represent normal rail traffic, while Load Model SW/2 is for heavy loads. The 'unloaded train' model represents the effects of an unloaded train.",
        "latexSymbol": "rtmodel",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label"
                ],
                [
                    "Load Model 71"
                ],
                [
                    "Load Model SW/0"
                ],
                [
                    "Load Model SW/2"
                ],
                [
                    "Unloaded Train"
                ]
            ]
        }
    },
    {
        "id": "G9_COMP_6",
        "codeName": "EN1991-2",
        "reference": [
            "6.3"
        ],
        "title": "Characteristic values of concentrated loads for railway traffic",
        "description": "The characteristic values of concentrated loads for railway traffic represent the concentrated vertical loads specific to Load Model 71. These loads are crucial for evaluating the impact of concentrated railway traffic loads on bridge structures and ensuring the bridge design accounts for the intense forces exerted by passing trains.",
        "latexSymbol": "Q_{vk}",
        "latexEquation": "1000",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G9_COMP_5"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{rtmodel} = Load Model 71",
                    "\\sym{rtmodel} = Load Model SW/0",
                    "\\sym{rtmodel} = Load Model SW/2",
                    "\\sym{rtmodel} = Unloaded Train"
                ]
            ],
            "data": [
                [
                    "1000"
                ],
                [
                    "0"
                ],
                [
                    "0"
                ],
                [
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G9_COMP_7",
        "codeName": "EN1991-2",
        "reference": [
            "6.3"
        ],
        "title": "Characteristic values of distributed loads for railway traffic",
        "description": "The characteristic values of distributed loads for railway traffic represent the uniformly distributed vertical loads in train loads and apply to all load models, including Load Model 71, SW/0, SW/2, and the Unloaded Train. For high-speed load models (HSLM), centrifugal forces are determined using the values from Load Model 71.",
        "latexSymbol": "q_{vk}",
        "latexEquation": "80",
        "type": "number",
        "unit": "kN/m",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G9_COMP_5"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{rtmodel} = Load Model 71",
                    "\\sym{rtmodel} = Load Model SW/0",
                    "\\sym{rtmodel} = Load Model SW/2",
                    "\\sym{rtmodel} = Unloaded Train"
                ]
            ],
            "data": [
                [
                    "80"
                ],
                [
                    "133"
                ],
                [
                    "150"
                ],
                [
                    "10"
                ]
            ]
        }
    },
    {
        "id": "G9_COMP_8",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.1(8)"
        ],
        "title": "Influence length of the loaded part of curved track",
        "description": "The influence length refers to the length of the curved track on a railway bridge that is directly affected by the train load. It plays a crucial role in determining the horizontal forces, such as centrifugal forces, acting on the structure. A shorter influence length generally leads to higher localized forces, making it essential for accurately calculating load effects on the bridge.",
        "latexSymbol": "L_{f}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 0
        },
        "default": 115,
        "useStd": False
    },
    {
        "id": "G9_COMP_9",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.1(6.19)"
        ],
        "title": "Reduction factor for centrifugal forces",
        "description": "The reduction factor for centrifugal forces adjusts the vertical train loads based on train speed and the influence length of the curved track on the bridge, ultimately modifying the centrifugal force acting on the structure.",
        "latexSymbol": "f",
        "latexEquation": "\\sym{f_{1}}",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G9_COMP_5",
            "G9_COMP_10"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{rtmodel} = Load Model 71",
                    "\\sym{rtmodel} = Load Model SW/0",
                    "\\sym{rtmodel} = Load Model SW/2",
                    "\\sym{rtmodel} = Unloaded Train"
                ]
            ],
            "data": [
                [
                    "\\sym{f_{1}}"
                ],
                [
                    "\\sym{f_{1}}"
                ],
                [
                    "1"
                ],
                [
                    "1"
                ]
            ]
        }
    },
    {
        "id": "G9_COMP_10",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.1(6.19)"
        ],
        "title": "Initial reduction factor for centrifugal force",
        "description": "The initial reduction factor for centrifugal force is calculated when the train speed exceeds 120km/h and the influence length is greater than 2.88m. This factor is applied to Load Model 71 and SW/0.",
        "latexSymbol": "f_{1}",
        "latexEquation": "[1 - \\frac{(\\sym{V}-120)}{1000} \\times (\\frac{814}{\\sym{V}} + 1.75)\\times(1 - \\sqrt{\\frac{2.88}{\\sym{L_{f}}}})]",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G8_COMP_8",
            "G9_COMP_8"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{V}>120 \\land \\sym{L_{f}} > 2.88",
                    "\\sym{V}>=120 \\lor \\sym{L_{f}} >= 2.88"
                ]
            ],
            "data": [
                [
                    "[1 - \\frac{(\\sym{V}-120)}{1000} \\times (\\frac{814}{\\sym{V}} + 1.75)\\times(1 - \\sqrt{\\frac{2.88}{\\sym{L_{f}}}})]"
                ],
                [
                    "1"
                ]
            ]
        }
    },
    {
        "id": "G9_COMP_11",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.2(2)P"
        ],
        "title": "Characteristic value of nosing force",
        "description": "The characteristic value of the nosing force represents a concentrated horizontal force of 100 kN acting at the top of the rails, perpendicular to the track's centerline. This force is applied on both straight and curved tracks. While it is not multiplied by the dynamic or reduction factors used for centrifugal forces, it must be multiplied by a factor for classified vertical loads if that factor is 1.0 or greater. It is always combined with vertical traffic loads.",
        "latexSymbol": "Q_{sk}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 1,
        "default": 100,
        "const": True
    },
    {
        "id": "G9_COMP_12",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.3(1)P"
        ],
        "title": "Influence length for traction and braking forces",
        "description": "The influence length for traction and braking forces refers to the portion of the structure over which traction and braking forces are applied as a uniformly distributed load. This length is typically determined based on the geometry of the bridge and the portion of the track that is directly affected by the train's braking and traction efforts.",
        "latexSymbol": "L_{a,b}",
        "latexEquation": "\\sym{L_{LM71}}",
        "type": "number",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G9_COMP_5",
            "G9_COMP_17"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{rtmodel} = Load Model 71",
                    "\\sym{rtmodel} = Load Model SW/0",
                    "\\sym{rtmodel} = Load Model SW/2",
                    "\\sym{rtmodel} = Unloaded Train"
                ]
            ],
            "data": [
                [
                    "\\sym{L_{LM71}}"
                ],
                [
                    "35.3"
                ],
                [
                    "57.0"
                ],
                [
                    "0.0"
                ]
            ]
        }
    },
    {
        "id": "G9_COMP_13",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.3(6.20)"
        ],
        "title": "Characteristic value of traction force",
        "description": "The characteristic value of the traction force represents the uniformly distributed longitudinal force acting along the rails due to traction. This force is distributed over the influence length of the structural element and applies to Load Models 71, SW/0, SW/2, and HSLM. The traction force is calculated as 33 kN per meter of the influence length, with a maximum value of 1000 kN.",
        "latexSymbol": "Q_{lak}",
        "latexEquation": "\\min(33 \\times \\sym{L_{a,b}}, 1000)",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G9_COMP_5",
            "G9_COMP_12"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{rtmodel} = Load Model 71",
                    "\\sym{rtmodel} = Load Model SW/0",
                    "\\sym{rtmodel} = Load Model SW/2",
                    "\\sym{rtmodel} = Unloaded Train"
                ]
            ],
            "data": [
                [
                    "\\min(33 \\times \\sym{L_{a,b}} , 1000)"
                ],
                [
                    "\\min(33 \\times \\sym{L_{a,b}} , 1000)"
                ],
                [
                    "\\min(33 \\times \\sym{L_{a,b}} , 1000)"
                ],
                [
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G9_COMP_14",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.3(6.21)",
            "6.5.3(6.22)"
        ],
        "title": "Characteristic value of braking force",
        "description": "The characteristic value of the braking force, denoted as the uniformly distributed longitudinal force acting along the rails due to braking. This force is distributed over the influence length of the structural element and applies to Load Models 71, SW/0, SW/2, and HSLM.",
        "latexSymbol": "Q_{lbk}",
        "latexEquation": "\\min(22 \\times \\sym{L_{a,b}}, 6000)",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G9_COMP_5",
            "G9_COMP_12",
            "G9_COMP_15",
            "G9_COMP_16"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{rtmodel} = Load Model 71",
                    "\\sym{rtmodel} = Load Model SW/0",
                    "\\sym{rtmodel} = Load Model SW/2",
                    "\\sym{rtmodel} = Unloaded Train"
                ]
            ],
            "data": [
                [
                    "\\min(22 \\times \\sym{L_{a,b}}, 6000)"
                ],
                [
                    "\\min(22 \\times \\sym{a_{SW/0}}, 6000)"
                ],
                [
                    "35 \\times \\sym{a_{SW/2}}"
                ],
                [
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G9_COMP_15",
        "codeName": "EN1991-2",
        "reference": [
            "6.3.2(Table6.1)"
        ],
        "title": "Load application length for Load Model SW/0",
        "description": "The value of 15 meters represents the load application length of the vehicle model acting as a uniformly distributed load in Load Model SW/0. This parameter defines the length over which the load is applied across the span of a continuous bridge. ",
        "latexSymbol": "a_{SW/0}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 1,
        "default": 15.0,
        "const": True
    },
    {
        "id": "G9_COMP_16",
        "codeName": "EN1991-2",
        "reference": [
            "6.3.2(Table6.1)"
        ],
        "title": "Load application length for Load Model SW/2",
        "description": "The value represents the load application length of the vehicle model acting as a uniformly distributed load in Load Model SW/2. This load model is used to represent heavy rail traffic, and the length is crucial for determining how the load is applied across the span of a bridge.",
        "latexSymbol": "a_{SW/2}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 1,
        "default": 25.0,
        "const": True
    },
    {
        "id": "G9_COMP_17",
        "codeName": "EN1991-2",
        "reference": [
            "6.5.3(1)P"
        ],
        "title": "Influence length of the loaded part of curved track",
        "description": "For Load Model 71, the influence length for traction and braking forces refers specifically to the part of the structure subjected to these forces, applied as a uniformly distributed load. This length is typically defined based on the bridge's geometry and the portion of the track directly affected by the braking and traction efforts of the train under Load Model 71 conditions.",
        "latexSymbol": "L_{LM71}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 0
        },
        "default": 25.4,
        "useStd": False
    },
    {
        "id": "G10_COMP_1",
        "codeName": "EN1991-1-4",
        "reference": [
            "5.3(5.3)"
        ],
        "title": "Wind force acting on a structure",
        "description": "The wind force acting on a structure or structural component is calculated using the force coefficient, structural factor, peak velocity pressure at the reference height, and the reference area exposed to the wind. This formula helps determine the total wind load on a structure for safety and design purposes.",
        "latexSymbol": "F_{w}",
        "latexEquation": "\\sym{c_{s}c_{d}} \\times \\sym{c_{f}} \\times \\sym{q_{p}(z)} \\times \\sym{A_{ref}}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_2",
            "G10_COMP_10",
            "G3_COMP_24",
            "G10_COMP_7"
        ]
    },
    {
        "id": "G10_COMP_2",
        "codeName": "EN1991-1-4",
        "reference": [
            "8.2(1)"
        ],
        "title": "Structural factor",
        "description": "The structural factor accounts for the combined effects of non-simultaneous peak wind pressures on a structure and the vibrations caused by wind turbulence. This factor may be divided into a size factor and a dynamic factor, depending on the structure's characteristics, such as height, frequency, and shape.",
        "latexSymbol": "c_{s}c_{d}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G10_COMP_3",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.6(2)"
        ],
        "title": "Length of the rectangular pier being considered",
        "description": "The length of the rectangular pier refers to the total vertical height of the pier being analyzed. This measurement is crucial for determining the reference area exposed to wind loads and is used in wind force calculations.",
        "latexSymbol": "l",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 6.5,
        "useStd": False
    },
    {
        "id": "G10_COMP_4",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.6(Figure7.23)"
        ],
        "title": "Breadth of rectangular sections",
        "description": "In rectangular sections, the breadth refers to the shorter dimension of the cross-section that is perpendicular to the wind direction. This dimension is critical in determining the reference area and the wind loads acting on the structure.",
        "latexSymbol": "b",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 2.5,
        "useStd": False
    },
    {
        "id": "G10_COMP_5",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.6(Figure7.23)"
        ],
        "title": "Depth of rectangular section",
        "description": "The depth, denoted as d, refers to the longer dimension of the rectangular section perpendicular to the wind direction. It represents the distance between the front and back faces of the section, playing a crucial role in determining the wind forces acting on the structure. The depth is used to calculate the reference area and influences the pressure distribution on the rectangular section.",
        "latexSymbol": "d",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 3,
        "useStd": False
    },
    {
        "id": "G10_COMP_6",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.6(Figure7.24)"
        ],
        "title": "Radius of rounded corners",
        "description": "The radius of rounded corners refers to the curvature of the edges where two surfaces meet, typically on rectangular or square structural sections. This radius is important in wind load calculations, as rounded corners reduce wind resistance and turbulence compared to sharp edges, leading to a more streamlined flow of wind around the structure.",
        "latexSymbol": "r",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 0
        },
        "default": 0,
        "useStd": False
    },
    {
        "id": "G10_COMP_7",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.6(7.10)"
        ],
        "title": "Reference area for rectangular bridge piers",
        "description": "For rectangular sections, the reference area is calculated by multiplying the length and the breadth of the structural element. This area represents the surface exposed to wind forces and is essential for calculating wind loads on rectangular bridge piers.",
        "latexSymbol": "A_{ref}",
        "latexEquation": "\\sym{l} \\times \\sym{b}",
        "type": "number",
        "unit": "m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_3",
            "G10_COMP_4"
        ]
    },
    {
        "id": "G10_COMP_8",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.6(Figure7.23)"
        ],
        "title": "Ratio of depth to breadth",
        "description": "The ratio of depth to breadth is a key parameter in determining the base force coefficient for rectangular sections. This ratio represents the proportion of the longer side (depth) to the shorter side (breadth) of the section. It influences the aerodynamic behavior and wind load distribution on the structure, and is essential for calculating the base force coefficient accurately.",
        "latexSymbol": "{d/b}",
        "latexEquation": "\\frac{\\sym{d}}{\\sym{b}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_5",
            "G10_COMP_4"
        ]
    },
    {
        "id": "G10_COMP_9",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.6(Figure7.24)"
        ],
        "title": "Ratio of corner radius to breadth",
        "description": "The ratio of the corner radius to breadth is used to account for the effect of rounded corners on the aerodynamic performance of rectangular sections. This ratio influences the reduction factor applied to wind load calculations, as larger corner radii reduce turbulence and drag, leading to a more streamlined flow around the section.",
        "latexSymbol": "{r/b}",
        "latexEquation": "\\frac{\\sym{r}}{\\sym{b}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_6",
            "G10_COMP_4"
        ]
    },
    {
        "id": "G10_COMP_10",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.6(7.9)"
        ],
        "title": "Force coefficient for rectangular sections",
        "description": "The force coefficient represents the wind load acting on structural elements with rectangular sections. It is calculated by multiplying the base force coefficient by two factors: the reduction factor for rounded corners and the end-effect factor for elements with free-end flow.",
        "latexSymbol": "c_{f}",
        "latexEquation": "\\sym{c_{f,0}} \\times \\sym{\\psi_{r}} \\times \\sym{\\psi_{\\lambda,R}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_11",
            "G10_COMP_12",
            "G10_COMP_13"
        ]
    },
    {
        "id": "G10_COMP_11",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.6(Figure7.23)"
        ],
        "title": "Base force coefficient for rectangular sections",
        "description": "The base force coefficient represents the wind load on rectangular sections with sharp corners and no free-end flow. It serves as the foundation for calculating the total wind force, and adjustments are made with additional factors like the reduction for rounded corners or end effects.",
        "latexSymbol": "c_{f,0}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_8"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "{d/b}",
                    "value": [
                        0.1,
                        0.2,
                        0.7,
                        5.0,
                        10.0,
                        50.0
                    ]
                }
            ],
            "data": [
                2.0,
                2.0,
                2.4,
                1.0,
                0.9,
                0.9
            ]
        }
    },
    {
        "id": "G10_COMP_12",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.6(Figure7.24)"
        ],
        "title": "Reduction factor for rounded corners",
        "description": "The reduction factor is applied to square sections with rounded corners to account for aerodynamic effects that reduce wind forces. This factor depends on the Reynolds number, which influences the flow characteristics around the section.",
        "latexSymbol": "\\psi_{r}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_9"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "{r/b}",
                    "value": [
                        0.0,
                        0.2,
                        0.4
                    ]
                }
            ],
            "data": [
                1.0,
                0.5,
                0.5
            ]
        }
    },
    {
        "id": "G10_COMP_13",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.13(Figure7.36)"
        ],
        "title": "End-effect factor for elements with free-end flow",
        "description": "The end-effect factor is applied to structural elements with free-end flow to account for the additional wind effects near the free ends of the element. This factor adjusts the wind force calculations for elements where the wind can flow around the ends, influencing the overall aerodynamic behavior.",
        "latexSymbol": "\\psi_{\\lambda,R}",
        "latexEquation": "0.1 \\times \\log_{10}{\\sym{\\lambda_{R}}} + 0.6",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_14"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "1 <= \\sym{\\lambda_{R}} <= 10",
                    "10 < \\sym{\\lambda_{R}} <= 100",
                    "100 < \\sym{\\lambda_{R}} <= 200"
                ]
            ],
            "data": [
                [
                    "0.1 \\times \\log_{10}{\\sym{\\lambda_{R}}} + 0.6"
                ],
                [
                    "0.25 \\times \\log_{10}{\\sym{\\lambda_{R}}} + 0.45"
                ],
                [
                    "0.166 \\times \\log_{10}{\\sym{\\lambda_{R}}} + 0.618"
                ]
            ]
        }
    },
    {
        "id": "G10_COMP_14",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.13(Table7.16)"
        ],
        "title": "Effective slenderness ratio for rectangular sections",
        "description": "The effective slenderness ratio for rectangular sections is key to determining the end-effect factor, which accounts for wind flow around the free ends. A higher slenderness ratio means the structure is more slender and more affected by wind forces, especially at the ends.",
        "latexSymbol": "\\lambda_{R}",
        "latexEquation": "\\min(2 \\times \\frac{\\sym{l}}{\\sym{b}}, 70)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_3",
            "G10_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{l} < 15",
                    "15 <= \\sym{l} < 50",
                    "\\sym{l} >= 50"
                ]
            ],
            "data": [
                [
                    "\\min(2 \\times \\frac{\\sym{l}}{\\sym{b}}, 70)"
                ],
                [
                    "\\min(\\frac{\\sym{l}}{\\sym{b}} \\times (\\frac{79}{35} - (0.6 \\times \\frac{\\sym{l}}{35})), 70)"
                ],
                [
                    "\\min(1.4 \\times \\frac{\\sym{l}}{\\sym{b}}, 70)"
                ]
            ]
        }
    },
    {
        "id": "G10_COMP_15",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.13(7.28)"
        ],
        "title": "Solidity ratio",
        "description": "The solidity ratio is the ratio of the projected area of the structural members to the overall envelope area. It indicates how solid or open a structure is, affecting its aerodynamic behavior and wind resistance. A higher ratio means the structure is more solid, leading to greater wind forces. This ratio is important for calculating wind loads on various structural sections.",
        "latexSymbol": "\\phi",
        "latexEquation": "\\min(2 \\times \\frac{l}{b}, 70)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_7",
            "G10_COMP_16"
        ]
    },
    {
        "id": "G10_COMP_16",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.13(3)"
        ],
        "title": "Overall envelope area",
        "description": "The overall envelope area refers to the projected area of a structure when viewed perpendicular to the wind direction. It represents the total surface area that is exposed to wind forces. This area is critical in wind load calculations as it determines the amount of force exerted by the wind on the structure. It is typically calculated based on the dimensions of the structure's length and breadth.",
        "latexSymbol": "A_{c}",
        "latexEquation": "\\sym{l} \\times \\sym{b}",
        "type": "number",
        "unit": "m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_3",
            "G10_COMP_4"
        ]
    },
    {
        "id": "G11_COMP_1",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(5)"
        ],
        "title": "Selection of wind action calculation procedure",
        "description": "The choice of wind action calculation procedure can be categorized into General, Simplified Procedure, or Full Procedure. The General approach is applied broadly, the Simplified Procedure is used for most highway and railway bridges for straightforward calculations, while the Full Procedure is for structures requiring higher structural reliability against wind loading, applied to bridges that meet specific safety criteria.",
        "latexSymbol": "windproce",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "General",
                    "A general procedure for calculating wind actions, involving a measured location selection and calculations based on the return period."
                ],
                [
                    "Simplified",
                    "Suitable for most highway and railway bridges, following Clause 3.4.2 for simpler requirements for wind action calculations."
                ],
                [
                    "Full",
                    "Required for structures needing enhanced structural reliability against wind loading, following Clause 3.4.3 and applied to bridges meeting specific safety criteria."
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_2",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4"
        ],
        "title": "Peak velocity pressure for wind leading combinations",
        "description": "The peak velocity pressure for wind leading combinations is calculated according to three different procedures: General, Simplified, and Full. Each procedure has its own criteria and methods to determine the wind pressure on structures, ensuring proper application for varying levels of structural reliability and exposure.",
        "latexSymbol": "q_{p,w}",
        "latexEquation": "\\sym{q_{p}}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_1",
            "G11_COMP_6",
            "G11_COMP_12",
            "G11_COMP_15"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{windproce} = General",
                    "\\sym{windproce} = Simplified",
                    "\\sym{windproce} = Full"
                ]
            ],
            "data": [
                [
                    "\\sym{q_{p}}"
                ],
                [
                    "\\sym{q_{p,s,w}}"
                ],
                [
                    "\\sym{q_{p}(z)}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_3",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4"
        ],
        "title": "Peak velocity pressure for traffic leading combinations",
        "description": "The peak velocity pressure for traffic leading combinations is calculated using different procedures, including General, Simplified, and Full. Each procedure ensures that the wind pressure calculations are appropriate for the design requirements of road and railway bridges, considering traffic conditions and structural reliability.",
        "latexSymbol": "q_{p,t}",
        "latexEquation": "\\sym{q\\prime}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_1",
            "G11_COMP_7",
            "G11_COMP_13",
            "G11_COMP_16"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{windproce} = General",
                    "\\sym{windproce} = Simplified",
                    "\\sym{windproce} = Full"
                ]
            ],
            "data": [
                [
                    "\\sym{q\\prime}"
                ],
                [
                    "\\sym{q_{p,s,t}}"
                ],
                [
                    "\\sym{q\\prime(z)}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_4",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(Table3.6)"
        ],
        "title": "Selection of primary wind measurement location",
        "description": "Waglan Island provides wind data that reflects extreme, open-sea wind conditions ideal for conservative design. In contrast, the Hong Kong Observatory offers urban wind data typical of pre-development conditions, suitable for urban-focused structural considerations.",
        "latexSymbol": "windloca",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Waglan Island",
                    "Exposed site providing data based on long-fetch southeasterly winds over open sea, suitable for conservative design considerations."
                ],
                [
                    "Hong Kong Observatory",
                    "Urban location data representative of typical conditions before urban development, offering insights into an exposed urban area."
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_5",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(Table3.6)"
        ],
        "title": "Return period in years",
        "description": "The return period is the estimated interval of time between occurrences of a specific event, such as extreme weather or natural phenomena, at a given location. It represents the average frequency with which a particular intensity or magnitude of an event is expected to be equaled or exceeded, aiding in risk assessment and planning.",
        "latexSymbol": "T",
        "type": "number",
        "unit": "years",
        "notation": "standard",
        "decimal": 0,
        "limits": {
            "inMin": 50,
            "inMax": 200
        },
        "default": 120,
        "useStd": True
    },
    {
        "id": "G11_COMP_6",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(3)"
        ],
        "title": "Peak velocity pressure in general procedure",
        "description": "Peak velocity pressure calculated by the general procedure represents the pressure exerted by the maximum peak wind velocity on a structure. This measure is vital for designing safe and resilient buildings and bridges, ensuring that structures can withstand wind forces effectively.",
        "latexSymbol": "q_{p}",
        "latexEquation": "(\\frac{1}{2}) \\times \\sym{\\rho} \\times 10^{-3} \\times \\sym{v_{d}}^{2}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_8",
            "G11_COMP_9"
        ]
    },
    {
        "id": "G11_COMP_7",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(3)"
        ],
        "title": "Hourly mean velocity pressure in general procedure",
        "description": "Hourly mean velocity pressure in the general procedure refers to the average pressure exerted by the wind on a structure over an hour. It is used to evaluate wind loads and ensure that structures are designed to withstand consistent wind forces.",
        "latexSymbol": "q\\prime",
        "latexEquation": "(\\frac{1}{2}) \\times \\sym{\\rho} \\times 10^{-3} \\times \\sym{v\\prime}^{2}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_8",
            "G11_COMP_10"
        ]
    },
    {
        "id": "G11_COMP_8",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(3)"
        ],
        "title": "Air density",
        "description": "Air density refers to the mass per unit volume of air and is an essential factor in calculating wind pressure on structures.",
        "latexSymbol": "\\rho",
        "type": "number",
        "unit": "kg/m^3",
        "notation": "standard",
        "decimal": 3,
        "default": 1.226,
        "const": True
    },
    {
        "id": "G11_COMP_9",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(Table3.6)"
        ],
        "title": "Maximum peak wind velocity",
        "description": "Maximum peak wind velocity refers to the highest wind speed experienced at a given location and is used to assess the wind loads on structures. This parameter is critical for determining the design wind pressure and ensuring that structures can withstand extreme wind conditions.",
        "latexSymbol": "v_{d}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_4",
            "G11_COMP_48",
            "G11_COMP_49"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{windloca} = Waglan Island",
                    "\\sym{windloca} = Hong Kong Observatory"
                ]
            ],
            "data": [
                [
                    "\\sym{v_{d,wa}}"
                ],
                [
                    "\\sym{v_{d,ob}}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_10",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(Table3.6)"
        ],
        "title": "Maximum hourly mean wind velocity",
        "description": "The maximum hourly mean wind velocity represents the highest average wind speed measured over one hour at a specific location. It is used to assess wind loads and their potential impact on structural stability.",
        "latexSymbol": "v\\prime",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_4",
            "G11_COMP_50",
            "G11_COMP_51"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{windloca} = Waglan Island",
                    "\\sym{windloca} = Hong Kong Observatory"
                ]
            ],
            "data": [
                [
                    "\\sym{v\\prime_{wa}}"
                ],
                [
                    "\\sym{v\\prime_{ob}}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_11",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.2.1(Table3.8)"
        ],
        "title": "Selection of degree of exposure",
        "description": "The degree of exposure refers to the extent to which a structure is affected by surrounding conditions such as buildings, topography, or open areas. Selecting the appropriate exposure level is crucial for accurately calculating wind pressures on structures.",
        "figureFile": "detail_g11_comp_11.png",
        "latexSymbol": "degexpo",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "1",
                    "[Sheltered Location] Sheltered by surrounding buildings and/or topography (e.g., Kowloon Park Drive Flyover)"
                ],
                [
                    "2",
                    "Normal exposure (e.g., Castle Road Flyover)"
                ],
                [
                    "3",
                    "Elevated situation; not sheltered by buildings or topography (e.g., Tai Po Road Interchange)"
                ],
                [
                    "4",
                    "[Exposed Location] Exposed to north-easterly or south-easterly winds across open sea (e.g., Ap Lei Chau Bridge)"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_12",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.2.1(Table3.8)"
        ],
        "title": "Peak velocity pressure for wind leading in simplified procedure",
        "description": "The peak velocity pressure derived from this table is used in the simplified procedure to estimate wind loads for wind leading combinations in structural design. For locations with intermediate exposure, engineers should interpolate values using their judgment between those for sheltered and exposed locations, aided by typical examples and descriptions.",
        "latexSymbol": "q_{p,s,w}",
        "latexEquation": "2.5",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_11"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{degexpo} = 1",
                    "\\sym{degexpo} = 2",
                    "\\sym{degexpo} = 3",
                    "\\sym{degexpo} = 4"
                ]
            ],
            "data": [
                [
                    "2.5"
                ],
                [
                    "2.8"
                ],
                [
                    "3.3"
                ],
                [
                    "3.8"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_13",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.2.2(1)"
        ],
        "title": "Peak velocity pressure for traffic leading in simplified procedure",
        "description": "For road bridges, due to the low probability of significant traffic presence at peak wind velocities over 44 m/s, a peak velocity pressure of 1.2 is applied in traffic leading combinations. This ensures the wind action combination value on the bridge and vehicles does not exceed the set limit.",
        "latexSymbol": "q_{p,s,t}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "default": 1.2,
        "const": True
    },
    {
        "id": "G11_COMP_14",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Selection of orography significance for site",
        "description": "Orography significance for a site refers to whether the location has terrain features, such as hills or cliffs, that increase wind velocities by more than 5%, necessitating the use of an orography factor in wind calculations. If the average slope of the upwind terrain is less than 3°, orographic effects can be disregarded.",
        "figureFile": "detail_g11_comp_14.png",
        "latexSymbol": "orosigsite",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Non-Significant Orography Site",
                    "The site does not have significant terrain features, so the topographical factor is not applied."
                ],
                [
                    "Significant Orography Site",
                    "The site has notable terrain features that require applying the topographical factor to wind pressure calculations."
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_15",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3.1"
        ],
        "title": "Peak velocity pressure for wind leading in full procedure",
        "description": "The peak velocity pressure for wind leading in the full procedure is calculated using the basic peak velocity pressure and a climate change multiplying factor. The basic peak velocity pressure is determined based on the height of the bridge and the loaded length under consideration.",
        "latexSymbol": "q_{p}(z)",
        "latexEquation": "\\sym{c_{e}(z)} \\times \\sym{q_{pb}(z)} \\times \\sym{K_{pc}}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_14",
            "G11_COMP_23",
            "G11_COMP_22",
            "G11_COMP_20",
            "G11_COMP_17"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{orosigsite} = Non-Significant Orography Site",
                    "\\sym{orosigsite} = Significant Orography Site"
                ]
            ],
            "data": [
                [
                    "\\sym{c_{e}(z)} \\times \\sym{q_{pb}(z)} \\times \\sym{K_{pc}}"
                ],
                [
                    "\\sym{c_{o}(z)}^{2} \\times \\sym{c_{e}(z)} \\times \\sym{q_{pb}(z)} \\times \\sym{K_{pc}}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_16",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3.1"
        ],
        "title": "Hourly mean velocity pressure",
        "description": "The hourly mean velocity pressure represents the average wind pressure exerted on a structure over an hour. It is calculated using the basic hourly mean velocity pressure and a climate change multiplying factor, considering the structure's height and loaded length to accurately assess wind effects.",
        "latexSymbol": "q\\prime(z)",
        "latexEquation": "\\sym{c_{e}(z)} \\times \\sym{q_{b}\\prime(z)} \\times \\sym{K_{pc}}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_14",
            "G11_COMP_23",
            "G11_COMP_22",
            "G11_COMP_21",
            "G11_COMP_17"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{orosigsite} = Non-Significant Orography Site",
                    "\\sym{orosigsite} = Significant Orography Site"
                ]
            ],
            "data": [
                [
                    "\\sym{c_{e}(z)} \\times \\sym{q_{b}\\prime(z)} \\times \\sym{K_{pc}}"
                ],
                [
                    "\\sym{c_{o}(z)}^{2} \\times \\sym{c_{e}(z)} \\times \\sym{q_{b}\\prime(z)} \\times \\sym{K_{pc}}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_17",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3.6"
        ],
        "title": "Climate change velocity pressure multiplying factor",
        "description": "The climate change velocity pressure multiplying factor is used in the full procedure to adjust wind pressure calculations for the expected future increase in wind speed due to climate change.",
        "latexSymbol": "K_{pc}",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 2,
        "default": 1.22,
        "const": True
    },
    {
        "id": "G11_COMP_18",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Height above ground level",
        "description": "The height above ground level refers to the vertical distance from the ground surface to the topmost part of the bridge structure, such as the deck or any point exposed to wind.",
        "latexSymbol": "z",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 10,
            "inMax": 100
        },
        "default": 40,
        "useStd": False
    },
    {
        "id": "G11_COMP_19",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Horizontal wind loaded lengths",
        "description": "The horizontal wind loaded length is the section of the bridge exposed to wind, producing the most severe effect. It can refer to the base length of a single adverse area or a combined length of multiple adverse areas in continuous structures.",
        "latexSymbol": "L",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 20,
            "inMax": 2000
        },
        "default": 100,
        "useStd": False
    },
    {
        "id": "G11_COMP_20",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Basic peak velocity pressure",
        "description": "Basic peak velocity pressure represents the peak wind pressure acting on a structure at a given height above ground level. It varies depending on the height and loaded length of the structure and reflects the potential wind force that can impact the structure.",
        "latexSymbol": "q_{pb}(z)",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_19"
        ],
        "table": "bi-interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "z",
                    "value": [
                        10,
                        15,
                        20,
                        30,
                        40,
                        50,
                        60,
                        80,
                        100,
                        150,
                        200
                    ]
                },
                {
                    "symbol": "L",
                    "value": [
                        20,
                        100,
                        200,
                        400,
                        600,
                        1000,
                        2000
                    ]
                }
            ],
            "data": [
                [
                    4.2,
                    2.8,
                    2.4,
                    2.1,
                    2.0,
                    1.8,
                    1.6
                ],
                [
                    4.2,
                    2.8,
                    2.5,
                    2.2,
                    2.0,
                    1.9,
                    1.7
                ],
                [
                    4.2,
                    2.8,
                    2.5,
                    2.2,
                    2.1,
                    2.0,
                    1.8
                ],
                [
                    4.2,
                    2.9,
                    2.6,
                    2.3,
                    2.3,
                    2.1,
                    1.9
                ],
                [
                    4.2,
                    3.0,
                    2.7,
                    2.5,
                    2.3,
                    2.2,
                    2.0
                ],
                [
                    4.2,
                    3.1,
                    2.8,
                    2.5,
                    2.4,
                    2.3,
                    2.1
                ],
                [
                    4.3,
                    3.1,
                    2.9,
                    2.6,
                    2.5,
                    2.4,
                    2.2
                ],
                [
                    4.3,
                    3.3,
                    3.0,
                    2.8,
                    2.7,
                    2.5,
                    2.4
                ],
                [
                    4.4,
                    3.4,
                    3.1,
                    2.9,
                    2.8,
                    2.7,
                    2.5
                ],
                [
                    4.6,
                    3.6,
                    3.4,
                    3.2,
                    3.1,
                    3.0,
                    2.8
                ],
                [
                    4.8,
                    3.8,
                    3.6,
                    3.4,
                    3.3,
                    3.2,
                    3.0
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_21",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Basic hourly mean velocity pressure",
        "description": "Basic hourly mean velocity pressure represents the average wind pressure exerted on a structure over an hour at a specific height above ground level. It varies based on the height and loaded length of the structure, providing an assessment of consistent wind force on the structure.",
        "latexSymbol": "q_{b}\\prime(z)",
        "type": "number",
        "unit": "kN/m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "z",
                    "value": [
                        10,
                        15,
                        20,
                        30,
                        40,
                        50,
                        60,
                        80,
                        100,
                        150,
                        200
                    ]
                }
            ],
            "data": [
                0.8,
                0.9,
                1.0,
                1.1,
                1.3,
                1.4,
                1.5,
                1.7,
                1.8,
                2.1,
                2.3
            ]
        }
    },
    {
        "id": "G11_COMP_22",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Exposure-based velocity pressure adjustment factor",
        "description": "These adjustment factors modify the basic peak velocity pressure and basic hourly mean velocity pressure based on the exposure level of a location. They ensure that wind pressure calculations accurately reflect the influence of different exposure conditions.",
        "latexSymbol": "c_{e}(z)",
        "latexEquation": "0.7",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G11_COMP_11"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{degexpo} = 1",
                    "\\sym{degexpo} = 2",
                    "\\sym{degexpo} = 3",
                    "\\sym{degexpo} = 4"
                ]
            ],
            "data": [
                [
                    "0.7"
                ],
                [
                    "0.8"
                ],
                [
                    "0.9"
                ],
                [
                    "1.0"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_23",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Topographical factor for significant orography",
        "description": "The topographical factor for significant orography, denoted as co(z), accounts for the influence of terrain features, such as hills and slopes, on wind pressure. This factor adjusts wind pressure calculations to reflect the amplification or reduction of wind forces due to the shape and elevation of the landscape.",
        "latexSymbol": "c_{o}(z)",
        "latexEquation": "1",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_35",
            "G11_COMP_24",
            "G11_COMP_28",
            "G11_COMP_27"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{\\Phi} < 0.05",
                    "0.05 <= \\sym{\\Phi} < 0.3",
                    "\\sym{\\Phi} >= 0.3"
                ]
            ],
            "data": [
                [
                    "1"
                ],
                [
                    "1 + 2 \\times \\sym{s} \\times \\sym{\\Phi} \\times \\frac{\\sym{s_{c}(z)}}{\\sym{s_{b}(z)}}"
                ],
                [
                    "1 + 0.6 \\times \\sym{s} \\times Φ \\times \\sym{s_{c}(z)} / \\sym{s_{b}(z)}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_24",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "name_Details",
        "description": "The upwind slope is a measure representing the ratio of the height to the length of a hill, ridge, cliff, or escarpment in the direction of the wind. It affects wind velocity as it approaches these topographical features and is defined in Annex A.3 of BS EN 1991-1-4.",
        "latexSymbol": "\\Phi",
        "latexEquation": "\\frac{H}{\\sym{L_{u}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_25",
            "G11_COMP_26"
        ]
    },
    {
        "id": "G11_COMP_25",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Height of orographic features",
        "description": "Height refers to the vertical distance from the base level of flat terrain to the top of an orographic feature, such as a hill, ridge, or cliff. This measurement is essential for calculating the upwind slope and determining its effect on wind velocity as illustrated in Figure A.1 of EN 1991-1-4.",
        "latexSymbol": "H",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 80,
        "useStd": False
    },
    {
        "id": "G11_COMP_26",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Actual length of the upwind slope in the wind direction",
        "description": "Length refers to the horizontal distance from the start of an incline to the point where it reaches the maximum height of an orographic feature. This distance helps in defining the upwind slope, which influences how wind velocity changes as it passes over the terrain, as shown in Figure A.1 of EN 1991-1-4.",
        "latexSymbol": "L_{u}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 650,
        "useStd": False
    },
    {
        "id": "G11_COMP_27",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.10)"
        ],
        "title": "Terrain and bridge factor",
        "description": "The terrain and bridge factor is used in wind pressure calculations to account for the impact of the surrounding terrain and bridge structure at a certain height. For short loaded lengths (less than 50 m) and heights less than 25 m, the height above ground level, z, should be taken as 25 m to ensure consistent and accurate interpolation in calculations.",
        "latexSymbol": "s_{b}(z)",
        "latexEquation": "(1 + (\\frac{\\max(\\sym{z}, 25)}{10})^{-0.4} \\times [1.48 - 0.704 \\times \\ln(\\ln{(\\sym{t})})]) \\times (\\frac{\\max{(\\sym{z}, 25)}}{10})^{0.19}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_19",
            "G11_COMP_29"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{L} < 50",
                    "\\sym{L} >= 50"
                ]
            ],
            "data": [
                [
                    "(1 + (\\frac{\\max{(\\sym{z}, 25)}}{10})^{-0.4} \\times [1.48 - 0.704 \\times \\ln(\\ln{(\\sym{t})})]) \\times (\\frac{\\max{(\\sym{z}, 25)}}{10})^{0.19}"
                ],
                [
                    "(1 + (\\frac{\\sym{z}}{10})^{-0.4} \\times [1.48 - 0.704\\times \\ln(\\ln{(\\sym{t})})]) \\times (\\frac{\\sym{z}}{10})^{0.19}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_28",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.10)"
        ],
        "title": "Hourly velocity factor",
        "description": "The hourly velocity factor is used to represent the variation in wind speed over an hour at a given height. This factor helps in adjusting the wind pressure calculations to reflect the actual wind conditions experienced by the structure, accounting for time-dependent changes in wind velocity.",
        "latexSymbol": "s_{c}(z)",
        "latexEquation": "(\\frac{\\sym{z}}{10})^{0.19}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18"
        ]
    },
    {
        "id": "G11_COMP_29",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.10)"
        ],
        "title": "Gust duration",
        "description": "Gust duration refers to the time interval over which a gust of wind acts on a structure. It is an important parameter in wind load analysis as it helps in understanding the impact of short-term wind speed fluctuations on the structural response.",
        "latexSymbol": "t",
        "latexEquation": "3",
        "type": "number",
        "unit": "sec",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_19"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{L} <= 20",
                    "\\sym{L} > 20"
                ]
            ],
            "data": [
                [
                    "3"
                ],
                [
                    "0.375 \\times \\sym{L}^{0.69}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_30",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Selection of terrain type for s factor",
        "description": "The calculation for the s factor differs based on whether the terrain type is classified as cliffs and escarpments or hills and ridges. Selecting the appropriate terrain type is essential for applying the correct method in wind pressure assessments. Refer to Figure A.2 and Figure A.3 of BS EN 1991-1-4 for detailed guidance.",
        "figureFile": "detail_g11_comp_30.png",
        "latexSymbol": "terrtype",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Cliffs and Escarpments",
                    "Evaluates the impact of wind over steep and abrupt slopes where wind decreases sharply beyond the crest."
                ],
                [
                    "Hills and Ridges",
                    "Represents terrain with gradual or rolling slopes, where wind gradually decreases after crossing the crest."
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_31",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Effective length of upwind slope",
        "description": "The effective length of the upwind slope is a measure used to represent the length of the slope that impacts wind behavior, as defined in Table A.2 of BS EN 1991-1-4. It varies based on whether the slope is shallow or steep and affects wind load calculations on structures.",
        "latexSymbol": "L_{e}",
        "latexEquation": "\\sym{L_{u}} \\times \\sym{u}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_26",
            "G11_COMP_32"
        ]
    },
    {
        "id": "G11_COMP_32",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Adjustment factor for effective length",
        "description": "The adjustment factor for effective length is used to modify the calculation of the effective length of the upwind slope based on the steepness of the slope. According to Table A.2 of BS EN 1991-1-4, when the slope is shallow (between 0.05 and 0.3), the factor is set to 1. For steeper slopes (greater than 0.3), the factor is calculated as the ratio of the slope's steepness to 0.3.",
        "latexSymbol": "u",
        "latexEquation": "1",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_24"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "0.05 < \\sym{\\Phi} < 0.3",
                    "\\sym{\\Phi} >= 0.3"
                ]
            ],
            "data": [
                [
                    "1"
                ],
                [
                    "\\frac{\\sym{\\Phi}}{0.3}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_33",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Length of downwind slope for hills and ridges",
        "description": "The length of the downwind slope is the horizontal distance from the crest of a hill or ridge to the end of the slope in the wind direction. This measurement is crucial for assessing how wind velocity and pressure change as the wind moves beyond the crest and is specifically applied in Figure A.3 of BS EN 1991-1-4 for calculating the s factor for hills and ridges.",
        "latexSymbol": "L_{d}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "exMin": 0
        },
        "default": 400,
        "useStd": False
    },
    {
        "id": "G11_COMP_34",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Horizontal distance from the top of the crest",
        "description": "The horizontal distance from the top of the crest refers to the measurement from the highest point of a hill or ridge to the structure's location on the ground. This distance is important for assessing how wind behaves as it travels over and beyond the crest. The distance is considered negative (-) to the left of the crest and positive (+) to the right of the crest.",
        "latexSymbol": "x",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {},
        "default": -150,
        "useStd": False
    },
    {
        "id": "G11_COMP_35",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Orographic location factor",
        "description": "The orographic location factor, denoted as s, is used to account for the impact of terrain features on wind velocity. It is determined from diagrams such as Figure A.2 or Figure A.3, scaled according to the length of the effective upwind slope, and is specified in Annex A.3 of BS EN 1991-1-4.",
        "latexSymbol": "s",
        "latexEquation": "\\sym{s_{ce}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_30",
            "G11_COMP_36",
            "G11_COMP_37"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{terrtype} = Cliffs and Escarpments",
                    "\\sym{terrtype} = Hills and Ridges"
                ]
            ],
            "data": [
                [
                    "\\sym{s_{ce}}"
                ],
                [
                    "\\sym{s_{hr}}"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_36",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Orographic location factor for cliffs and escarpments",
        "description": "The orographic location factor for cliffs and escarpments, denoted as s_ce, is used to evaluate wind behavior over steep terrain features. This factor is derived from Figure A.2 of BS EN 1991-1-4 and is essential for accurate wind load calculations for structures in such terrains.",
        "latexSymbol": "s_{ce}",
        "latexEquation": "\\sym{A} \\times \\exp(\\sym{B} \\times \\frac{x}{\\sym{L_{u}}})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_34",
            "G11_COMP_18",
            "G11_COMP_31",
            "G11_COMP_32",
            "G11_COMP_38",
            "G11_COMP_39",
            "G11_COMP_26",
            "G11_COMP_40",
            "G11_COMP_41",
            "G11_COMP_42",
            "G11_COMP_43",
            "G11_COMP_44",
            "G11_COMP_45"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "-1.5 <= \\frac{\\sym{x}}{(\\frac{\\sym{L_{e}}}{\\sym{u}})} <= 0 \\land 0 <= \\frac{z}{\\sym{L_{e}}} <= 2.0",
                    "\\frac{\\sym{x}}{\\sym{L_{e}}} = 0",
                    "0 < \\frac{\\sym{x}}{\\sym{L_{e}}} < 0.1",
                    "0.1 <= \\frac{\\sym{x}}{\\sym{L_{e}}} <= 3.5 \\land 0.1 <= \\frac{z}{\\sym{L_{e}}} <=2.0",
                    "\\frac{\\sym{x}}{(\\frac{\\sym{L_{e}}}{\\sym{u}})} < -1.5 \\lor \\frac{x}{\\sym{L_{e}}} > 3.5 \\lor \\frac{z}{\\sym{L_{e}}} > 2"
                ]
            ],
            "data": [
                [
                    "\\sym{A} \\times \\exp(\\sym{B} \\times \\frac{x}{\\sym{L_{u}}})"
                ],
                [
                    "\\sym{A}"
                ],
                [
                    "\\sym{A} + (\\frac{(\\sym{A2} - \\sym{B2} + \\sym{C2} - \\sym{A})}{0.1}) \\times (\\frac{\\sym{x}}{\\sym{L_{e}}})\\sym{A}"
                ],
                [
                    "\\sym{A1} \\times (\\log{(\\frac{x}{\\sym{L_{e}}})})^{2} + \\sym{B1} \\times (\\log{(\\frac{x}{\\sym{L_{e}}})}) + \\sym{C1}"
                ],
                [
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_37",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Orographic location factor for hills and ridges",
        "description": "The orographic location factor for hills and ridges, denoted as s_hr, is used to assess wind behavior over more gradual terrain features. This factor is derived from Figure A.3 of BS EN 1991-1-4 and plays a crucial role in determining wind loads on structures in such areas.",
        "latexSymbol": "s_{hr}",
        "latexEquation": "\\sym{A} \\times \\exp(\\sym{B} \\times \\frac{x}{\\sym{L_{u}}})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_34",
            "G11_COMP_31",
            "G11_COMP_32",
            "G11_COMP_18",
            "G11_COMP_26",
            "G11_COMP_33",
            "G11_COMP_38",
            "G11_COMP_39",
            "G11_COMP_46",
            "G11_COMP_47"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "-1.5 <= \\frac{\\sym{x}}{(\\frac{\\sym{L_{e}}}{\\sym{u}})} <= 0 \\land 0 <= \\frac{z}{\\sym{L_{e}}} <= 2.0",
                    "0 <= \\frac{\\sym{x}}{\\sym{L_{d}}} <2.0 \\land 0 <= \\frac{z}{\\sym{L_{e}}} <= 2.0",
                    "\\frac{\\sym{x}}{(\\frac{\\sym{L_{e}}}{\\sym{u}})} < -1.5 \\lor \\frac{x}{\\sym{L_{d}}} > 2.0 \\lor \\frac{\\sym{z}}{\\sym{L_{e}}} > 2"
                ]
            ],
            "data": [
                [
                    "\\sym{A} \\times \\exp(\\sym{B} \\times \\frac{x}{\\sym{L_{u}}})"
                ],
                [
                    "\\sym{A3} \\times \\exp(\\sym{B}3} \\times \\frac{\\sym{x}}{\\sym{L_{d}}})"
                ],
                [
                    "0"
                ]
            ]
        }
    },
    {
        "id": "G11_COMP_38",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Coefficient A for upwind section calculation",
        "description": "Coefficient A is used in the calculation of the s factor for the upwind section of all types of orography.",
        "latexSymbol": "A",
        "latexEquation": "0.1552 \\times (\\frac{z}{\\sym{L_{e}}})^{4} - 0.8575 \\times (\\frac{z}{\\sym{L_{e}}})^{3} + 1.8133 \\times (\\frac{z}{\\sym{L_{e}}})^{2} - 1.9115 \\times (\\frac{z}{\\sym{L_{e}}}) + 0.10124",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_31"
        ]
    },
    {
        "id": "G11_COMP_39",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Coefficient B for upwind section calculation",
        "description": "Coefficient B is used alongside Coefficient A for the s factor calculation in the upwind section of all orography.",
        "latexSymbol": "B",
        "latexEquation": "0.3542 \\times (\\frac{z}{\\sym{L_{e}}})^{2} - 1.0577 \\times (\\frac{z}{\\sym{L_{e}}}) + 2.6456",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_31"
        ]
    },
    {
        "id": "G11_COMP_40",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Coefficient A1 for downwind section calculation",
        "description": "Coefficient A1 is used for calculating the s factor in the downwind section for cliffs and escarpments. (Cliffs and Escarpments)",
        "latexSymbol": "A1",
        "latexEquation": "-1.3420 * (\\log{(\\frac{z}{\\sym{L_{e}}})})^{3} - 0.8222 * (\\log{(\\frac{z}{\\sym{L_{e}}})})^{2} + 0.4609 * (\\log{(\\frac{z}{\\sym{L_{e}}})}) - 0.0791",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_31"
        ]
    },
    {
        "id": "G11_COMP_41",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Coefficient B1 for downwind section calculation",
        "description": "Coefficient B1 is used in the calculation of the s factor for the downwind section for cliffs and escarpments. (Cliffs and Escarpments)",
        "latexSymbol": "B1",
        "latexEquation": "-1.0196 \\times (\\log{(\\frac{z}{\\sym{L_{e}}})})^{3} - 0.8910 \\times (\\log{(\\frac{z}{\\sym{L_{e}}})})^{2} + 0.5343 \\times (\\log{(\\frac{z}{\\sym{L_{e}}})}) - 0.1156",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_31"
        ]
    },
    {
        "id": "G11_COMP_42",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Coefficient C1 for downwind section calculation",
        "description": "Coefficient C1 is applied in calculating the s factor for the downwind section of cliffs and escarpments.(Cliffs and Escarpments)",
        "latexSymbol": "C1",
        "latexEquation": "0.8030 \\times (\\log{(\\frac{z}{\\sym{L_{e}}})})^{3} + 0.4236 \\times (\\log{(\\frac{z}{\\sym{L_{e}}})})^{2} - 0.5738 \\times (\\log{(\\frac{z}{\\sym{L_{e}}})}) + 0.1606",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_31"
        ]
    },
    {
        "id": "G11_COMP_43",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Coefficient A2 for downwind section calculation",
        "description": "Coefficient A2 is specifically used for calculating the s factor in the downwind section for cliffs and escarpments when the vertical position is less than 0.1 relative to the effective length.",
        "latexSymbol": "A2",
        "latexEquation": "-1.3420 \\times (\\log{(\\max{(\\frac{z}{\\sym{L_{e}}}, 0.1)})})^{3} - 0.8222 \\times (\\log{(\\max{(\\frac{z}{\\sym{L_{e}}}, 0.1)})})^{2} + 0.4609 \\times (\\log{(\\max{(\\frac{z}{\\sym{L_{e}}}, 0.1)})}) - 0.0791",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_31"
        ]
    },
    {
        "id": "G11_COMP_44",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Coefficient B2 for downwind section calculation",
        "description": "Coefficient B2 is used for calculating the s factor in the downwind section for cliffs and escarpments when the vertical position is less than 0.1 relative to the effective length.",
        "latexSymbol": "B2",
        "latexEquation": "-1.0196 \\times (\\log{(\\max{(\\frac{z}{\\sym{L_{e}}}, 0.1)})})^{3} - 0.8910 \\times (\\log{(\\max{(\\frac{z}{\\sym{L_{e}}}, 0.1)})})^{2} + 0.5343 \\times (\\log{(\\max{(\\frac{z}{\\sym{L_{e}}}, 0.1)})}) - 0.1156",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_31"
        ]
    },
    {
        "id": "G11_COMP_45",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Coefficient C2 for downwind section calculation",
        "description": "Coefficient C2 is applied to the calculation of the s factor for the downwind section of cliffs and escarpments when the vertical position is less than 0.1 relative to the effective length.",
        "latexSymbol": "C2",
        "latexEquation": "0.8030 \\times (\\log{(\\max{(\\frac{z}{\\sym{L_{e}}}, 0.1)})})^{3} + 0.4236 \\times (\\log{(\\max{(\\frac{z}{\\sym{L_{e}}}, 0.1)})})^{2} - 0.5738 \\times (\\log{(\\max{(\\frac{z}{\\sym{L_{e}}}, 0.1)})}) + 0.1606",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_31"
        ]
    },
    {
        "id": "G11_COMP_46",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Coefficient A3 for downwind section calculation",
        "description": "Coefficient A3 is used in the calculation of the s factor for the downwind section of hills and ridges, accounting for the terrain's influence on wind behavior.",
        "latexSymbol": "A3",
        "latexEquation": "0.1552 \\times (\\frac{z}{\\sym{L_{e}}})^{4} - 0.8575 \\times (\\frac{z}{\\sym{L_{e}}})^{3} + 1.8133 \\times (\\frac{z}{\\sym{L_{e}}})^{2} - 1.9115 \\times (\\frac{z}{\\sym{L_{e}}}) + 1.0124",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_31"
        ]
    },
    {
        "id": "G11_COMP_47",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.3(Table3.9)"
        ],
        "title": "Coefficient B3 for downwind section calculation",
        "description": "Coefficient B3 is applied in the s factor calculation for the downwind section of hills and ridges to refine the evaluation of wind pressure effects on structures.",
        "latexSymbol": "B3",
        "latexEquation": "-0.3056 \\times (\\frac{z}{\\sym{L_{e}}})^{2} + 1.0212 \\times (\\frac{z}{\\sym{L_{e}}}) - 1.7637",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_18",
            "G11_COMP_31"
        ]
    },
    {
        "id": "G11_COMP_48",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(Table3.6)"
        ],
        "title": "Maximum Peak Wind Velocity for Waglan Island by Return Period",
        "description": "This section defines the maximum peak wind velocity specific to Waglan Island, determined based on return periods. It represents the expected wind speeds associated with events occurring within 50 to 200 years.",
        "latexSymbol": "v_{d,wa}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_5"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "T",
                    "value": [
                        50,
                        100,
                        200
                    ]
                }
            ],
            "data": [
                71,
                78,
                85
            ]
        }
    },
    {
        "id": "G11_COMP_49",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(Table3.6)"
        ],
        "title": "Maximum Peak Wind Velocity for Hong Kong Observatory by Return Period",
        "description": "This section specifies the maximum peak wind velocity recorded at the Hong Kong Observatory, categorized by return periods. It provides wind speed values for events expected within return periods of 50 to 200 years.",
        "latexSymbol": "v_{d,ob}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_5"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "T",
                    "value": [
                        50,
                        100,
                        200
                    ]
                }
            ],
            "data": [
                68,
                75,
                81
            ]
        }
    },
    {
        "id": "G11_COMP_50",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(Table3.6)"
        ],
        "title": "Maximum Hourly Mean Wind Velocity for Waglan Island by Return Period",
        "description": "This section outlines the maximum hourly mean wind velocity at Waglan Island, calculated based on specific return periods. It presents the expected wind speeds for return periods ranging from 50 to 200 years.",
        "latexSymbol": "v\\prime_{wa}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_5"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "T",
                    "value": [
                        50,
                        100,
                        200
                    ]
                }
            ],
            "data": [
                44,
                48,
                53
            ]
        }
    },
    {
        "id": "G11_COMP_51",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.4.1(Table3.6)"
        ],
        "title": "Maximum Hourly Mean Wind Velocity for Hong Kong Observatory by Return Period",
        "description": "This section defines the maximum hourly mean wind velocity observed at the Hong Kong Observatory, categorized by return periods. It indicates the expected wind speeds for events with return periods ranging from 50 to 200 years.",
        "latexSymbol": "v\\prime_{ob}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G11_COMP_5"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "T",
                    "value": [
                        50,
                        100,
                        200
                    ]
                }
            ],
            "data": [
                41,
                45,
                50
            ]
        }
    },
    {
        "id": "G12_COMP_1",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.17)"
        ],
        "title": "Structure type selection for uniform bridge temperature",
        "description": "Selecting the structure type as either normal or minor determines which uniform bridge temperature values apply. Normal structures require standard temperatures adjusted for climate change, while minor structures allow simplified temperature values suited to specific structural elements.",
        "latexSymbol": "tempstruct",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Normal",
                    "Uses standard uniform temperatures, adjusted for climate change effects."
                ],
                [
                    "Minor",
                    "Uses simplified temperatures for foot/cycle track bridges, carriageway joints, and temporary erection loading."
                ]
            ]
        }
    },
    {
        "id": "G12_COMP_2",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.3(Figure3.2)"
        ],
        "title": "Type of superstructure",
        "description": "Select the type of superstructure for the bridge. The superstructure type affects various design parameters, including load distribution and temperature adjustments.",
        "figureFile": "detail_g12_comp_2.png",
        "latexSymbol": "supertype",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Steel deck on steel girders",
                    "A steel deck supported by steel girders, commonly used for high load capacity and flexibility in design."
                ],
                [
                    "Steel deck on steel truss or plate girders",
                    "A steel deck supported by steel truss or plate girders, offering enhanced structural integrity and load distribution."
                ],
                [
                    "Concrete deck on steel box",
                    "A concrete deck supported by a steel box girder, providing high torsional rigidity and strength, ideal for longer spans or curved bridges."
                ],
                [
                    "Concrete deck on truss or plate girders",
                    "A concrete deck supported by truss or plate girders, offering enhanced load distribution and stability, suitable for medium to long spans."
                ],
                [
                    "Concrete slab",
                    "A solid concrete slab superstructure, typically for smaller spans and simpler load distribution."
                ],
                [
                    "Concrete beams",
                    "Concrete beams as the primary supporting structure, suitable for moderate to long spans."
                ],
                [
                    "Concrete box girder",
                    "A concrete box girder structure, known for its strength, torsional resistance, and suitability for curved spans."
                ]
            ]
        }
    },
    {
        "id": "G12_COMP_3",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.3(Figure3.2)"
        ],
        "title": "Superstructure group",
        "description": "The superstructure group is automatically assigned as Type 1, Type 2, or Type 3 based on the selected superstructure. Each group type corresponds to specific design parameters and adjustments.",
        "latexSymbol": "supergroup",
        "type": "number",
        "notation": "text",
        "required": [
            "G12_COMP_2"
        ],
        "default": "Type1",
        "table": "text",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{supertype} = Steel deck on steel girders",
                    "\\sym{supertype} = Steel deck on steel truss or plate girders",
                    "\\sym{supertype} = Concrete deck on steel box",
                    "\\sym{supertype} = Concrete deck on truss or plate girders",
                    "\\sym{supertype} = Concrete slab",
                    "\\sym{supertype} = Concrete beams",
                    "\\sym{supertype} = Concrete box girder"
                ]
            ],
            "data": [
                [
                    "Type1"
                ],
                [
                    "Type1"
                ],
                [
                    "Type2"
                ],
                [
                    "Type2"
                ],
                [
                    "Type3"
                ],
                [
                    "Type3"
                ],
                [
                    "Type3"
                ]
            ]
        }
    },
    {
        "id": "G12_COMP_4",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Deck surfacing type for uniform bridge temperature adjustment",
        "description": "Select the deck surfacing type for the bridge. This choice affects the uniform bridge temperature adjustments, as different surfacing types and depths impact the thermal properties of the structure. Refer to Table 3.18 for specific adjustment values.",
        "latexSymbol": "dsurftype",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label",
                    "description"
                ],
                [
                    "Unsurfaced Plain",
                    "Deck with no surfacing, typically exposed concrete."
                ],
                [
                    "Unsurfaced Trafficked or Waterproofed",
                    "Deck with no surfacing but designed for traffic or waterproofed for additional protection."
                ],
                [
                    "Surfacing Depths",
                    "Deck with a specific surfacing depth (e.g., 40 mm, 100 mm, etc.), including waterproofing layers."
                ]
            ]
        }
    },
    {
        "id": "G12_COMP_5",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Deck surfacing depth",
        "description": "Enter the surfacing depth for the bridge deck, including any waterproofing layers. This value is used to adjust the uniform bridge temperature based on the thickness of the surfacing.",
        "latexSymbol": "t_{s}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 40,
            "inMax": 200
        },
        "default": 120,
        "useStd": False
    },
    {
        "id": "G12_COMP_6",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(5)"
        ],
        "title": "Height above mean sea level ",
        "description": "Enter the height above mean sea level for the structure. This value is used to adjust the uniform bridge temperature values based on elevation, as specified in Table 3.17.",
        "latexSymbol": "amsl",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "limits": {
            "inMin": 0
        },
        "default": 95.5,
        "useStd": False
    },
    {
        "id": "G12_COMP_7",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.17)"
        ],
        "title": "Minimum uniform bridge temperature",
        "description": "The minimum uniform bridge temperature is the lowest average temperature that a structure might experience across its entirety. This temperature is used as a reference point for calculating potential contraction effects within the structure due to temperature decreases.",
        "latexSymbol": "T_{e,min}",
        "latexEquation": "-0.5 \\times (\\frac{\\sym{amsl}}{100}) + \\sym{T_{a,min}}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_6",
            "G12_COMP_9"
        ]
    },
    {
        "id": "G12_COMP_8",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.17)"
        ],
        "title": "Maximum uniform bridge temperature",
        "description": "The maximum uniform bridge temperature is the highest average temperature that a structure might experience across its entirety. This temperature serves as a reference for calculating potential expansion effects within the structure due to temperature increases.",
        "latexSymbol": "T_{e,max}",
        "latexEquation": "55 - (\\sym{amsl}/100) + \\sym{T_{a,max}}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_1",
            "G12_COMP_3",
            "G12_COMP_6",
            "G12_COMP_10"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{supergroup} = Type1",
                    "\\sym{supergroup} = Type2",
                    "\\sym{supergroup} = Type3"
                ],
                [
                    "\\sym{tempstruct} = Normal",
                    "\\sym{tempstruct} = Minor"
                ]
            ],
            "data": [
                [
                    "55 - (\\sym{amsl}/100) + \\sym{T_{a,max}}",
                    "53 - (\\sym{amsl}/100) + \\sym{T_{a,max}}"
                ],
                [
                    "48 - (\\sym{amsl}/100) + \\sym{T_{a,max}}",
                    "46 - (\\sym{amsl}/100) + \\sym{T_{a,max}}"
                ],
                [
                    "45 - (\\sym{amsl}/100) + \\sym{T_{a,max}}",
                    "43 - (\\sym{amsl}/100) + \\sym{T_{a,max}}"
                ]
            ]
        }
    },
    {
        "id": "G12_COMP_9",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Adjustment to minimum uniform bridge temperature",
        "description": "This value represents the adjustment to the minimum uniform bridge temperature in degrees Celsius based on the deck surfacing depth provided by the user. Refer to Table 3.18 to calculate the adjustment specific to the entered depth.",
        "latexSymbol": "T_{a,min}",
        "latexEquation": "0",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_4",
            "G12_COMP_3",
            "G12_COMP_11"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{dsurftype} = Unsurfaced Plain",
                    "\\sym{dsurftype} = Unsurfaced Trafficked or Waterproofed",
                    "\\sym{dsurftype} = Surfacing Depths"
                ],
                [
                    "\\sym{supergroup} = Type1",
                    "\\sym{supergroup} = Type2",
                    "\\sym{supergroup} = Type3"
                ]
            ],
            "data": [
                [
                    "0",
                    "-3",
                    "-1"
                ],
                [
                    "0",
                    "-3",
                    "-1"
                ],
                [
                    "\\sym{T_{s,min}}",
                    "\\sym{T_{s,min}}",
                    "\\sym{T_{s,min}}"
                ]
            ]
        }
    },
    {
        "id": "G12_COMP_10",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Adjustment to maximum uniform bridge temperature",
        "description": "This value represents the adjustment to the maximum uniform bridge temperature in degrees Celsius based on the deck surfacing depth provided by the user. Refer to Table 3.18 to calculate the adjustment specific to the entered depth.",
        "latexSymbol": "T_{a,max}",
        "latexEquation": "4",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_4",
            "G12_COMP_3",
            "G12_COMP_12"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{dsurftype} = Unsurfaced Plain",
                    "\\sym{dsurftype} = Unsurfaced Trafficked or Waterproofed",
                    "\\sym{dsurftype} = Surfacing Depths"
                ],
                [
                    "\\sym{supergroup} = Type1",
                    "\\sym{supergroup} = Type2",
                    "\\sym{supergroup} = Type3"
                ]
            ],
            "data": [
                [
                    "4",
                    "0",
                    "0"
                ],
                [
                    "2",
                    "4",
                    "2"
                ],
                [
                    "\\sym{T_{s,max}}",
                    "\\sym{T_{s,max}}",
                    "\\sym{T_{s,max}}"
                ]
            ]
        }
    },
    {
        "id": "G12_COMP_11",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Additional minimum temperature due to deck surfacing depth",
        "description": "This value represents the additional temperature applied to the minimum uniform bridge temperature based on the user-entered deck surfacing depth. The adjustment is determined by linear interpolation between the standard depths listed in Table 3.18.",
        "latexSymbol": "T_{s,min}",
        "latexEquation": "\\sym{T_{s,min,t1}}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_3",
            "G12_COMP_18",
            "G12_COMP_19",
            "G12_COMP_20"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{supergroup} = Type1",
                    "\\sym{supergroup} = Type2",
                    "\\sym{supergroup} = Type3"
                ]
            ],
            "data": [
                [
                    "\\sym{T_{s,min,t1}}"
                ],
                [
                    "\\sym{T_{s,min,t2}}"
                ],
                [
                    "\\sym{T_{s,min,t3}}"
                ]
            ]
        }
    },
    {
        "id": "G12_COMP_12",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Additional maximum temperature due to deck surfacing depth",
        "description": "This value represents the additional temperature applied to the minimum uniform bridge temperature based on the user-entered deck surfacing depth. The adjustment is determined by linear interpolation between the standard depths listed in Table 3.18.",
        "latexSymbol": "T_{s,max}",
        "latexEquation": "\\sym{T_{s,max,t1}}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_3",
            "G12_COMP_21",
            "G12_COMP_22",
            "G12_COMP_23"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{supergroup} = Type1",
                    "\\sym{supergroup} = Type2",
                    "\\sym{supergroup} = Type3"
                ]
            ],
            "data": [
                [
                    "\\sym{T_{s,max,t1}}"
                ],
                [
                    "\\sym{T_{s,max,t2}}"
                ],
                [
                    "\\sym{T_{s,max,t3}}"
                ]
            ]
        }
    },
    {
        "id": "G12_COMP_13",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(6)"
        ],
        "title": "Initial bridge temperature for contraction",
        "description": "The initial bridge temperature for contraction is the reference temperature at the time the structure is restrained upon completion of construction. It serves as a baseline for calculating how much the structure contracts as temperatures decrease toward the minimum uniform bridge temperature component.",
        "latexSymbol": "T_{0,con}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 0,
        "default": 30,
        "const": True
    },
    {
        "id": "G12_COMP_14",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(6)"
        ],
        "title": "Initial bridge temperature for expansion",
        "description": "The initial bridge temperature for expansion is the reference temperature at the time the structure is restrained upon completion of construction. It provides a baseline for calculating the expansion of the structure as temperatures increase toward the maximum uniform bridge temperature component.",
        "latexSymbol": "T_{0,exp}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 0,
        "default": 10,
        "const": True
    },
    {
        "id": "G12_COMP_15",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.4"
        ],
        "title": "Range of the uniform bridge temperature component for contraction",
        "description": "This is the calculated contraction range for the uniform bridge temperature component, determined from the initial bridge temperature at the time of restraint and the minimum uniform bridge temperature, as specified in EN 1991-1-5 Section 6.1.3.3.",
        "latexSymbol": "\\Delta{T_{N,con}}",
        "latexEquation": "\\sym{T_{0,con}} - \\sym{T_{e,min}}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_13",
            "G12_COMP_7"
        ]
    },
    {
        "id": "G12_COMP_16",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.4"
        ],
        "title": "Range of the uniform bridge temperature component for expansion",
        "description": "This is the calculated expansion range for the uniform bridge temperature component, based on the initial bridge temperature at the time of restraint and the maximum uniform bridge temperature, as specified in EN 1991-1-5 Section 6.1.3.3.",
        "latexSymbol": "\\Delta{T_{N,exp}}",
        "latexEquation": "\\sym{T_{e,max}} - \\sym{T_{0,exp}}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_8",
            "G12_COMP_14"
        ]
    },
    {
        "id": "G12_COMP_17",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.4"
        ],
        "title": "Overall range of the uniform bridge temperature component",
        "description": "This is the overall temperature range for the uniform bridge temperature component, calculated as the difference between the maximum and minimum uniform bridge temperatures, as specified in EN 1991-1-5 Section 6.1.3.3.",
        "latexSymbol": "\\Delta{T_{N}}",
        "latexEquation": "\\sym{T_{e,max}} - \\sym{T_{e,min}}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_8",
            "G12_COMP_7"
        ]
    },
    {
        "id": "G12_COMP_18",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Additional minimum temperature due to deck surfacing depth for Type 1",
        "description": "This section specifies that no additional temperature adjustment is applied to Type 1 structures, as the adjustment value is always zero regardless of the surfacing depth.",
        "latexSymbol": "T_{s,min,t1}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "default": 0,
        "const": True
    },
    {
        "id": "G12_COMP_19",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Additional minimum temperature due to deck surfacing depth for Type 2",
        "description": "This section defines temperature adjustments for Type 2 structures based on surfacing depth: -2 at 40, 0 at 100, and 3 at 200. Values for other depths are calculated using linear interpolation.",
        "latexSymbol": "T_{s,min,t2}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_5"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "t_{s}",
                    "value": [
                        40,
                        100,
                        200
                    ]
                }
            ],
            "data": [
                -2,
                0,
                3
            ]
        }
    },
    {
        "id": "G12_COMP_20",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Additional minimum temperature due to deck surfacing depth for Type 3",
        "description": "This section defines temperature adjustments for Type 3 structures based on surfacing depth: -1 at 40, 0 at 100, and 1 at 200. Values for other depths are calculated using linear interpolation.",
        "latexSymbol": "T_{s,min,t3}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_5"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "t_{s}",
                    "value": [
                        40,
                        100,
                        200
                    ]
                }
            ],
            "data": [
                -1,
                0,
                1
            ]
        }
    },
    {
        "id": "G12_COMP_21",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Additional maximum temperature due to deck surfacing depth for Type 1",
        "description": "This section specifies that no additional maximum temperature adjustment is applied to Type 1 structures, as the adjustment value is always zero regardless of the surfacing depth.",
        "latexSymbol": "T_{s,max,t1}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "default": 0,
        "const": True
    },
    {
        "id": "G12_COMP_22",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Additional maximum temperature due to deck surfacing depth for Type 2",
        "description": "This section defines the additional maximum temperature adjustments for Type 2 structures based on surfacing depth: 2 at 40, 0 at 100, and -4 at 200. Values for other depths are calculated using linear interpolation.",
        "latexSymbol": "T_{s,max,t2}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_5"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "t_{s}",
                    "value": [
                        40,
                        100,
                        200
                    ]
                }
            ],
            "data": [
                2,
                0,
                -4
            ]
        }
    },
    {
        "id": "G12_COMP_23",
        "codeName": "HK.SDM2013",
        "reference": [
            "3.5.2(Table3.18)"
        ],
        "title": "Additional maximum temperature due to deck surfacing depth for Type 3",
        "description": "This section defines the additional maximum temperature adjustments for Type 3 structures based on surfacing depth: 1 at 40, 0 at 100, and -2 at 200. Values for other depths are calculated using linear interpolation.",
        "latexSymbol": "T_{s,max,t3}",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G12_COMP_5"
        ],
        "table": "interpolation",
        "tableDetail": {
            "point": [
                {
                    "symbol": "t_{s}",
                    "value": [
                        40,
                        100,
                        200
                    ]
                }
            ],
            "data": [
                1,
                0,
                -2
            ]
        }
    },
    {
        "id": "G13_COMP_1",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.2(7.20)"
        ],
        "title": "Reference area for circular bridge piers",
        "description": "The reference area for circular bridge piers is calculated using the pier's diameter and height. It represents the surface area exposed to wind loads. For a circular pier, the reference area is determined by multiplying the pier's diameter by its height.",
        "latexSymbol": "A_{ref}",
        "latexEquation": "\\sym{l} \\times \\sym{b}",
        "type": "number",
        "unit": "m^2",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G13_COMP_2",
            "G13_COMP_3"
        ]
    },
    {
        "id": "G13_COMP_2",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.2(4)"
        ],
        "title": "Length of the circular pier being considered",
        "description": "The length refers to the total vertical height of the structural element being analyzed, such as a circular pier. This measurement is crucial for determining the reference area exposed to wind loads.",
        "latexSymbol": "l",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "default": 11.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G13_COMP_3",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.1(1)"
        ],
        "title": "Diameter of circular pier",
        "description": "The diameter represents the width of the circular bridge pier. It is the horizontal measurement across the pier's cross-section and is used to calculate the reference area for wind load analysis.",
        "latexSymbol": "b",
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
        "id": "G13_COMP_4",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.2(7.19)"
        ],
        "title": "Force coefficient for finite circular cylinders",
        "description": "The force coefficient for finite circular cylinders is used to calculate the aerodynamic forces acting on a cylinder subjected to wind. It is determined by considering the base force coefficient and the end-effect factor, which accounts for the influence of wind flowing around the ends of the cylinder.",
        "latexSymbol": "c_{f}",
        "latexEquation": "\\sym{c_{f,0}} \\times \\sym{\\psi_{\\lambda,C}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G13_COMP_5",
            "G13_COMP_14"
        ]
    },
    {
        "id": "G13_COMP_5",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.2(Figure7.28)"
        ],
        "title": "Force coefficient of cylinders without free-end flow",
        "description": "The base force coefficient for circular cylinders without free-end flow accounts for aerodynamic drag due to wind. It depends on the surface roughness and Reynolds number, with a maximum value capped at 1.2.",
        "latexSymbol": "c_{f,0}",
        "latexEquation": "\\min(\\max(\\sym{c_{f,0,1}}, \\sym{c_{f,0,2}}), 1.2)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G13_COMP_6",
            "G13_COMP_7"
        ]
    },
    {
        "id": "G13_COMP_6",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.2(Figure7.28)"
        ],
        "title": "Force coefficient for lower reynolds number range",
        "description": "The force coefficient in this lower Reynolds number range applies to cases where the airflow around a circular cylinder is more likely to be laminar or in transition. It is calculated based on the Reynolds number alone and is used to estimate the aerodynamic drag in flow regimes where surface roughness has less impact.",
        "latexSymbol": "c_{f,0,1}",
        "latexEquation": "\\frac{0.11}{(\\frac{\\sym{R_{e}}}{10^{6}})^{1.4}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G13_COMP_11"
        ]
    },
    {
        "id": "G13_COMP_7",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.2(Figure7.28)"
        ],
        "title": "Force coefficient for higher reynolds number range",
        "description": "The force coefficient in this higher Reynolds number range is applied when the wind flow around a circular cylinder becomes fully turbulent. It takes both surface roughness and the Reynolds number into account, allowing for a more accurate estimation of drag forces, especially for rough surfaces.",
        "latexSymbol": "c_{f,0,2}",
        "latexEquation": "1.2 + \\frac{0.18\\times\\log(10\\times \\sym{{k/b}} )}{1+ 0.4 \\times \\log( \\frac{\\sym{R_{e}}}{10^{6}})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G13_COMP_10",
            "G13_COMP_11"
        ]
    },
    {
        "id": "G13_COMP_8",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.2(Table7.13)"
        ],
        "title": "Surface type selection",
        "description": "This menu allows users to select the type of surface material for the structure. Different surface types, such as smooth concrete, rough concrete, and various metals, affect wind resistance and load calculations.",
        "latexSymbol": "surftype",
        "type": "string",
        "notation": "text",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label"
                ],
                [
                    "Smooth Concrete"
                ],
                [
                    "Rough Concrete"
                ],
                [
                    "Bright Steel"
                ],
                [
                    "Cast Iron"
                ],
                [
                    "Galvanised Steel"
                ]
            ]
        }
    },
    {
        "id": "G13_COMP_9",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.2(Table7.13)"
        ],
        "title": "Equivalent surface roughness",
        "description": "The equivalent surface roughness (k) refers to the roughness of a structure's surface, which affects how wind flows around it. This factor is important in determining the wind resistance and the drag forces acting on the structure. The roughness height is used in wind load calculations to adjust force coefficients based on the surface texture of the structure.",
        "latexSymbol": "k",
        "latexEquation": "0.20",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G13_COMP_8"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{surftype} = Smooth Concrete",
                    "\\sym{surftype} = Rough Concrete",
                    "\\sym{surftype} = Bright Steel",
                    "\\sym{surftype} = Cast Iron",
                    "\\sym{surftype} = Galvanised Steel"
                ]
            ],
            "data": [
                [
                    "0.20"
                ],
                [
                    "1.00"
                ],
                [
                    "0.05"
                ],
                [
                    "0.20"
                ],
                [
                    "0.20"
                ]
            ]
        }
    },
    {
        "id": "G13_COMP_10",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.2(Figure7.28)"
        ],
        "title": "Surface roughness to diameter ratio",
        "description": "The surface roughness to diameter ratio indicates how rough a structure's surface is relative to its diameter. This ratio affects wind resistance, with higher values representing rougher surfaces and greater aerodynamic drag.",
        "latexSymbol": "{k/b}",
        "latexEquation": "\\frac{\\sym{k}}{(\\sym{b}\\times10^{3})}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G13_COMP_9",
            "G13_COMP_3"
        ]
    },
    {
        "id": "G13_COMP_11",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.1(7.15)"
        ],
        "title": "Reynolds number",
        "description": "Reynolds number  is a dimensionless quantity used to predict the flow patterns of wind around a structure, particularly circular cylinders. It is calculated using the diameter of the structure, wind velocity, and the kinematic viscosity of the air.",
        "latexSymbol": "R_{e}",
        "latexEquation": "\\frac{\\sym{b} \\times \\sym{v(z_{e})}}{\\sym{\\nu}}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G13_COMP_3",
            "G13_COMP_13",
            "G13_COMP_12"
        ]
    },
    {
        "id": "G13_COMP_12",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.1(1)"
        ],
        "title": "Kinematic viscosity",
        "description": "Kinematic viscosity is a property of air that describes its resistance to flow and shear. It is defined as the ratio of dynamic viscosity to density. In wind load calculations, kinematic viscosity is used to determine the Reynolds number, which helps predict the flow behavior around structures.",
        "latexSymbol": "\\nu",
        "type": "number",
        "unit": "m^2/s",
        "notation": "scientific",
        "decimal": 2,
        "default": 1.5e-05,
        "const": True
    },
    {
        "id": "G13_COMP_13",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.9.1(Figure7.27)"
        ],
        "title": "Peak wind velocity at height",
        "description": "The peak wind velocity at height refers to the highest wind speed at a specific reference height above ground. This value is critical for calculating wind pressures and forces acting on structures.",
        "latexSymbol": "v(z_{e})",
        "latexEquation": "\\sqrt{\\frac{2 \\times (\\sym{q_{p}(z)} \\times 10^{3})}{\\sym{\\rho}}}",
        "type": "number",
        "unit": "m/s",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G3_COMP_24",
            "G3_COMP_25"
        ]
    },
    {
        "id": "G13_COMP_14",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.13(Figure7.36)"
        ],
        "title": "End-effect factor for elements with free-end flow",
        "description": "The end-effect factor is applied to structural elements with free-end flow to account for the additional wind effects near the free ends of the element. This factor adjusts the wind force calculations for elements where the wind can flow around the ends, influencing the overall aerodynamic behavior.",
        "latexSymbol": "\\psi_{\\lambda,C}",
        "latexEquation": "0.1 \\times \\log_{10}{\\sym{\\lambda_{C}}} + 0.6",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G13_COMP_15"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "1 <= \\sym{\\lambda_{C}} <= 10",
                    "10< \\sym{\\lambda_{C}} <= 100",
                    "100< \\sym{\\lambda_{C}} <= 200"
                ]
            ],
            "data": [
                [
                    "0.1 \\times \\log_{10}{\\sym{\\lambda_{C}}} + 0.6"
                ],
                [
                    "0.25 \\times \\log_{10}{\\sym{\\lambda_{C}}} + 0.45"
                ],
                [
                    "0.166 \\times \\log_{10}{\\sym{\\lambda_{C}}} + 0.618"
                ]
            ]
        }
    },
    {
        "id": "G13_COMP_15",
        "codeName": "EN1991-1-4",
        "reference": [
            "7.13(Table7.16)"
        ],
        "title": "Effective slenderness ratio for circular sections",
        "description": "The effective slenderness ratio for circular sections is crucial in determining the end-effect factor, which accounts for wind flow around the free ends. A higher slenderness ratio indicates that the structure is more slender and more susceptible to wind forces, particularly at the ends of the structure.",
        "latexSymbol": "\\lambda_{C}",
        "latexEquation": "\\min(\\frac{\\sym{l}}{\\sym{b}}, 70)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G13_COMP_2",
            "G13_COMP_3"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{l} < 15",
                    "15 <= \\sym{l} < 50",
                    "\\sym{l} >= 50"
                ]
            ],
            "data": [
                [
                    "\\min(\\frac{\\sym{l}}{\\sym{b}}, 70)"
                ],
                [
                    "\\min(\\frac{\\sym{l}}{\\sym{b}} \\times (1 - (\\frac{0.3}{35}) \\times (\\sym{l}-15)), 70)"
                ],
                [
                    "\\min(0.7 \\times \\frac{\\sym{l}}{\\sym{b}}, 70)"
                ]
            ]
        }
    },
    {
        "id": "G13_COMP_16",
        "codeName": "EN1991-1-4",
        "reference": [
            "5.3(5.3)"
        ],
        "title": "Wind force acting on a circular pier",
        "description": "The wind force acting on a circular pier is determined using the force coefficient, structural factor, peak velocity pressure at the reference height, and the projected area of the pier exposed to the wind.",
        "latexSymbol": "F_{w,c}",
        "latexEquation": "\\sym{c_{s}c_{d}} \\times \\sym{c_{f}} \\times \\sym{q_{p}(z)} \\times \\sym{A_{ref}}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G10_COMP_2",
            "G13_COMP_4",
            "G3_COMP_24",
            "G13_COMP_1"
        ]
    },
    {
        "id": "G14_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.8(1)"
        ],
        "title": "Total member depth",
        "description": "The total member depth (h) refers to the overall vertical thickness of the concrete member from the top surface to the bottom, used in calculations to determine the mean flexural tensile strength of reinforced concrete.",
        "latexSymbol": "h",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 1500.0,
        "limits": {
            "inMin": 0
        }
    },
    {
        "id": "G14_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3 (5)"
        ],
        "title": "Scale of temperature",
        "description": "This table allows users to select a temperature scale, offering options such as Kelvin (K), Celsius (°C), and Fahrenheit (°F) for various temperature measurements.",
        "latexSymbol": "tempscale",
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
                    "K^{-1} (Kelvin)"
                ],
                [
                    "°C^{-1} (Celsius)"
                ],
                [
                    "°F^{-1} (Fahrenheit)"
                ]
            ]
        }
    },
    {
        "id": "G14_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "2.4.2.4(Table2.1N)"
        ],
        "title": "Design situations",
        "description": "This table outlines different design situations, categorized into persistent, transient, and accidental conditions. Each category represents a specific scenario that may affect the design and safety considerations of a structure.",
        "latexSymbol": "designsitu",
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
                    "Persistent"
                ],
                [
                    "Transient"
                ],
                [
                    "Accidental"
                ]
            ]
        }
    },
    {
        "id": "G14_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(Table 3.1)"
        ],
        "title": "Compressive strength classes",
        "description": "Compressive strength classes categorize concrete based on its compressive strength, typically indicated by a standard notation such as C30/37, where the first number represents the cylinder strength and the second the cube strength. For more detailed information, refer toEN 206-1 (Table 7).",
        "latexSymbol": "C",
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
                    "C12/15"
                ],
                [
                    "C16/20"
                ],
                [
                    "C20/25"
                ],
                [
                    "C25/30"
                ],
                [
                    "C30/37"
                ],
                [
                    "C35/45"
                ],
                [
                    "C40/50"
                ],
                [
                    "C45/55"
                ],
                [
                    "C50/60"
                ],
                [
                    "C55/67"
                ],
                [
                    "C60/75"
                ],
                [
                    "C70/85"
                ],
                [
                    "C80/95"
                ],
                [
                    "C90/105"
                ]
            ]
        }
    },
    {
        "id": "G14_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(Table 3.1)"
        ],
        "title": "Characteristic compressive cylinder strength of concrete",
        "description": "The characteristic compressive cylinder strength of concrete measured at 28 days, representing the strength that 95% of the concrete samples are expected to exceed. For more detailed information, refer toEN 206-1 (Table 7).",
        "latexSymbol": "f_{ck}",
        "latexEquation": "12",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G14_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{C} = C12/15",
                    "\\sym{C} = C16/20",
                    "\\sym{C} = C20/25",
                    "\\sym{C} = C25/30",
                    "\\sym{C} = C30/37",
                    "\\sym{C} = C35/45",
                    "\\sym{C} = C40/50",
                    "\\sym{C} = C45/55",
                    "\\sym{C} = C50/60",
                    "\\sym{C} = C55/67",
                    "\\sym{C} = C60/75",
                    "\\sym{C} = C70/85",
                    "\\sym{C} = C80/95",
                    "\\sym{C} = C90/105"
                ]
            ],
            "data": [
                [
                    "12"
                ],
                [
                    "16"
                ],
                [
                    "20"
                ],
                [
                    "25"
                ],
                [
                    "30"
                ],
                [
                    "35"
                ],
                [
                    "40"
                ],
                [
                    "45"
                ],
                [
                    "50"
                ],
                [
                    "55"
                ],
                [
                    "60"
                ],
                [
                    "70"
                ],
                [
                    "80"
                ],
                [
                    "90"
                ]
            ]
        }
    },
    {
        "id": "G14_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(Table 3.1)"
        ],
        "title": "Characteristic compressive cube strength",
        "description": "The characteristic compressive cylinder strength of concrete measured at 28 days, representing the strength that 95% of the concrete samples are expected to exceed. For more detailed information, refer toEN 206-1 (Table 7).",
        "latexSymbol": "f_{ck,cube}",
        "latexEquation": "15",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G14_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{C} = C12/15",
                    "\\sym{C} = C16/20",
                    "\\sym{C} = C20/25",
                    "\\sym{C} = C25/30",
                    "\\sym{C} = C30/37",
                    "\\sym{C} = C35/45",
                    "\\sym{C} = C40/50",
                    "\\sym{C} = C45/55",
                    "\\sym{C} = C50/60",
                    "\\sym{C} = C55/67",
                    "\\sym{C} = C60/75",
                    "\\sym{C} = C70/85",
                    "\\sym{C} = C80/95",
                    "\\sym{C} = C90/105"
                ]
            ],
            "data": [
                [
                    "15"
                ],
                [
                    "20"
                ],
                [
                    "25"
                ],
                [
                    "30"
                ],
                [
                    "37"
                ],
                [
                    "45"
                ],
                [
                    "50"
                ],
                [
                    "55"
                ],
                [
                    "60"
                ],
                [
                    "67"
                ],
                [
                    "75"
                ],
                [
                    "85"
                ],
                [
                    "95"
                ],
                [
                    "105"
                ]
            ]
        }
    },
    {
        "id": "G14_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(Table 3.1)"
        ],
        "title": "Mean value of concrete cylinder compressive strength",
        "description": "The mean value of concrete cylinder compressive strength is the average compressive strength obtained from multiple concrete cylinder tests, typically measured at 28 days, representing the expected average strength of the concrete.",
        "latexSymbol": "f_{cm}",
        "latexEquation": "\\sym{f_{ck}} + 8",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G14_COMP_5"
        ]
    },
    {
        "id": "G14_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(Table 3.1)"
        ],
        "title": "Mean value of axial tensile strength of concrete",
        "description": "The mean value of axial tensile strength of concrete is the average tensile strength measured along the axis of concrete specimens, typically representing the concrete's resistance to tension forces.",
        "latexSymbol": "f_{ctm}",
        "latexEquation": "0.3\\times \\sym{f_{ck}}^{(\\frac{2}{3})}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_5",
            "G14_COMP_7"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{f_{ck}} <= 50",
                    "\\sym{f_{ck}} > 50"
                ]
            ],
            "data": [
                [
                    "0.3\\times \\sym{f_{ck}}^{(\\frac{2}{3})}"
                ],
                [
                    "2.12\\times \\ln(1+\\frac{\\sym{f_{cm}}}{10})"
                ]
            ]
        }
    },
    {
        "id": "G14_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(Table 3.1)"
        ],
        "title": "5% fractile value of axial tensile strength of concrete",
        "description": "The 5% fractile value of concrete's axial tensile strength, meaning 95% of samples have a higher tensile strength than this value.",
        "latexSymbol": "f_{ctk,0.05}",
        "latexEquation": "0.7\\times \\sym{f_{ctm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_8"
        ]
    },
    {
        "id": "G14_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(Table 3.1)"
        ],
        "title": "95% fractile value of axial tensile strength of concrete",
        "description": "The 95% fractile value of concrete's axial tensile strength, meaning only 5% of samples have a higher tensile strength than this value.",
        "latexSymbol": "f_{ctk,0.95}",
        "latexEquation": "1.3\\times \\sym{f_{ctm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_8"
        ]
    },
    {
        "id": "G14_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(Table 3.1)"
        ],
        "title": "Secant modulus of elasticity of concrete",
        "description": "The secant modulus of elasticity of concrete is the slope of the secant drawn from the origin to a specific point on the stress-strain curve of concrete, representing the average stiffness of the material under loading.",
        "latexSymbol": "E_{cm}",
        "latexEquation": "22[\\frac{\\sym{f_{cm}}}{10}]^{0.3} \\times 1000",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G14_COMP_7"
        ]
    },
    {
        "id": "G14_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "2.4.2.4(Table2.1N)"
        ],
        "title": "The partial safety factor for concrete",
        "description": "The partial safety factor for concrete is a coefficient applied to reduce the characteristic strength of concrete in design calculations, accounting for uncertainties in material properties, construction methods, and loading conditions to ensure structural safety.",
        "latexSymbol": "\\gamma_{c}",
        "latexEquation": "1.5",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G14_COMP_3"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{designsitu} = Persistent",
                    "\\sym{designsitu} = Transient",
                    "\\sym{designsitu} = Accidental"
                ]
            ],
            "data": [
                [
                    "1.5"
                ],
                [
                    "1.5"
                ],
                [
                    "1.2"
                ]
            ]
        }
    },
    {
        "id": "G14_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.6(1)P"
        ],
        "title": "Coefficient for long-term and load application effects on compressive strength",
        "description": "This coefficient accounts for the long-term effects on compressive strength and the unfavorable effects resulting from how the load is applied, ensuring that these factors are considered in the design process.",
        "latexSymbol": "\\alpha_{cc}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G14_COMP_14",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.6(2)P"
        ],
        "title": "Coefficient for long-term and load application effects on tensile strength",
        "description": "This coefficient accounts for the long-term effects on tensile strength and the unfavorable effects resulting from how the load is applied, ensuring that these factors are considered in the design process.",
        "latexSymbol": "\\alpha_{ct}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G14_COMP_15",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.6(3.15)"
        ],
        "title": "Design compressive strength",
        "description": "Design compressive strength is the reduced value of the characteristic compressive strength of concrete, used in structural design calculations to ensure safety by accounting for material variability and uncertainties in load conditions.",
        "latexSymbol": "f_{cd}",
        "latexEquation": "\\sym{\\alpha_{cc}}\\times \\frac{\\sym{f_{ck}}}{\\sym{\\gamma_{c}}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_5",
            "G14_COMP_12",
            "G14_COMP_13"
        ]
    },
    {
        "id": "G14_COMP_16",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.6(3.16)"
        ],
        "title": "Design tensile strength",
        "description": "Design tensile strength is the reduced value of the characteristic tensile strength of concrete, used in structural design calculations to ensure safety by accounting for material variability and uncertainties in load conditions.",
        "latexSymbol": "f_{ctd}",
        "latexEquation": "\\sym{\\alpha_{ct}}\\times \\frac{\\sym{f_{ctk,0.05}}}{\\sym{\\gamma_{c}}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_14",
            "G14_COMP_9",
            "G14_COMP_12"
        ]
    },
    {
        "id": "G14_COMP_17",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.8(3.23)"
        ],
        "title": "Mean flexural tensile strength of reinforced concrete",
        "description": "Mean flexural tensile strength of reinforced concrete is the average strength of reinforced concrete in bending, representing its ability to resist tensile forces across its cross-section.",
        "latexSymbol": "f_{ctm,fl}",
        "latexEquation": "\\max((1.6 - \\frac{\\sym{h}}{1000})\\sym{f_{ctm}}, \\sym{f_{ctm}})",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_1",
            "G14_COMP_8"
        ]
    },
    {
        "id": "G14_COMP_18",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(4)"
        ],
        "title": "Poisson's ratio",
        "description": "Poisson's ratio is a measure of the deformation of a material in the directions perpendicular to the direction of applied force. For uncracked concrete, it is typically 0.2, while for cracked concrete, it is considered 0.",
        "latexSymbol": "\\nu",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 0.2,
        "const": True
    },
    {
        "id": "G14_COMP_19",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(5)"
        ],
        "title": "The linear coefficient of thermal expansion",
        "description": "The linear coefficient of thermal expansion measures how much a material expands or contracts with changes in temperature. It is expressed as a fractional change in length per degree of temperature change, typically in units of 1/K or 1/°C.",
        "latexSymbol": "\\alpha_{c}",
        "latexEquation": "10 \\times 10^{-6}",
        "type": "number",
        "unit": "",
        "notation": "scientific",
        "decimal": 2,
        "required": [
            "G14_COMP_2"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{tempscale} = K^{-1} (Kelvin)",
                    "\\sym{tempscale} = °C^{-1} (Celsius)",
                    "\\sym{tempscale} = °F^{-1} (Fahrenheit)"
                ]
            ],
            "data": [
                [
                    "10 \\times 10^{-6}"
                ],
                [
                    "10 \\times 10^{-6}"
                ],
                [
                    "5.5556 \\times 10^{-6}"
                ]
            ]
        }
    },
    {
        "id": "G15_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.2(5)"
        ],
        "title": "Age of concrete being considered",
        "description": "t represents the age of the concrete in days, which is critical for determining its compressive strength. For concrete aged 3 days or less, more precise values should be based on specific tests to ensure accuracy.",
        "latexSymbol": "t",
        "type": "number",
        "unit": "day",
        "notation": "standard",
        "decimal": 0,
        "default": 3.0,
        "limits": {
            "inMin": 3,
            "inMax": 28
        },
        "useStd": False
    },
    {
        "id": "G15_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.2 (6)"
        ],
        "title": "Cement type selection",
        "description": "This menu allows users to select the type of cement, including Class S, Class N, and Class R, each of which represents different strength and curing properties tailored for specific construction needs.",
        "latexSymbol": "cementype",
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
                    "Class S"
                ],
                [
                    "Class N"
                ],
                [
                    "Class R"
                ]
            ]
        }
    },
    {
        "id": "G15_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.2(6)"
        ],
        "title": "Cement type coefficient",
        "description": "This coefficient varies depending on the type of cement used, reflecting the different strength development characteristics of each cement class. Stronger cements or those designed for rapid strength gain have lower coefficients, while slower-setting cements have higher coefficients to account for their extended curing times and slower strength development.",
        "latexSymbol": "s",
        "latexEquation": "0.20",
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
                    "\\sym{cementype} = Class R",
                    "\\sym{cementype} = Class N",
                    "\\sym{cementype} = Class S"
                ]
            ],
            "data": [
                [
                    "0.20"
                ],
                [
                    "0.25"
                ],
                [
                    "0.38"
                ]
            ]
        }
    },
    {
        "id": "G15_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.2(3.2)"
        ],
        "title": "Coefficient for time-dependent compressive strength development",
        "description": "This coefficient represents the time-dependent development of compressive strength, accounting for how the material's strength increases over time and ensuring this progression is factored into the design process.",
        "latexSymbol": "\\beta_{cc}(t)",
        "latexEquation": "\\exp(\\sym{s} \\times[1-(\\frac{28}{\\sym{t}})^{0.5}])",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G15_COMP_3",
            "G15_COMP_1"
        ]
    },
    {
        "id": "G15_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.2(3.1)"
        ],
        "title": "The mean concrete compressive strength at an age of t days",
        "description": "This refers to the mean compressive strength of concrete at a specific age t, which serves as a reference value for determining the characteristic strength at early ages.",
        "latexSymbol": "f_{cm}(t)",
        "latexEquation": "\\sym{\\beta_{cc}(t)}\\times \\sym{f_{cm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G15_COMP_4",
            "G14_COMP_7"
        ]
    },
    {
        "id": "G15_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.2(5)"
        ],
        "title": "Concrete compressive strength at time t",
        "description": "Concrete compressive strength at time t refers to the strength of the concrete at a specific time during its curing process, reflecting its development over time.",
        "latexSymbol": "f_{ck}(t)",
        "latexEquation": "\\sym{f_{ck}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_5",
            "G15_COMP_5"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{f_{ck}} >= 28",
                    "\\sym{f_{ck}} < 28"
                ]
            ],
            "data": [
                [
                    "\\sym{f_{ck}}"
                ],
                [
                    "\\sym{f_{cm}(t)} - 8"
                ]
            ]
        }
    },
    {
        "id": "G15_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.2(9)"
        ],
        "title": "Exponent for time-dependent strength adjustment",
        "description": "This exponent is used to adjust the rate of strength development in concrete over time. It ensures that the early linear strength gain is accurately reflected and accounts for the slower strength increase after 28 days.",
        "latexSymbol": "\\alpha",
        "latexEquation": "1",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3
    },
    {
        "id": "G15_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.2(3.4)"
        ],
        "title": "Time-dependent tensile strength of concrete",
        "description": "This refers to the tensile strength of concrete at a specific time, influenced by factors such as curing conditions, drying conditions, and the dimensions of the structural members. The strength can vary over time as the concrete continues to harden and develop its properties.",
        "latexSymbol": "f_{ctm}(t)",
        "latexEquation": "\\sym{\\beta_{cc}(t)}^{\\sym{\\alpha}} \\times \\sym{f_{ctm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G15_COMP_4",
            "G15_COMP_7",
            "G14_COMP_8"
        ]
    },
    {
        "id": "G15_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.3(3.5)"
        ],
        "title": "Time-dependent modulus of elasticity",
        "description": "This represents the modulus of elasticity of concrete at a specific age, showing how the stiffness of the concrete changes over time. It is compared to the modulus of elasticity determined at 28 days, with its variation estimated based on the corresponding compressive strength at that age.",
        "latexSymbol": "E_{cm}(t)",
        "latexEquation": "(\\frac{\\sym{f_{cm}(t)}}{\\sym{f_{cm}}})^{0.3}\\times \\sym{E_{cm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G15_COMP_5",
            "G14_COMP_7",
            "G14_COMP_11"
        ]
    },
    {
        "id": "G16_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.8c)"
        ],
        "title": "Concrete strength influence coefficient for relative humidity effect",
        "description": "This factor adjusts the effect of ambient humidity and the notional size of the concrete member on the notional creep coefficient for concretes with compressive strengths greater than 35 MPa. As the concrete's strength increases, this factor reduces the impact of relative humidity and notional size in the creep calculations, reflecting how stronger concretes exhibit less creep under the same environmental conditions.",
        "latexSymbol": "\\alpha_{1}",
        "latexEquation": "[\\frac{35}{\\sym{f_{cm}}}]^{0.7}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_7"
        ]
    },
    {
        "id": "G16_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.8c)"
        ],
        "title": "Concrete strength influence coefficient for ϕRH",
        "description": "This factor fine-tunes the effect of relative humidity on the notional creep coefficient for concretes with compressive strengths greater than 35 MPa. It makes slight adjustments to reflect how stronger concretes experience less creep, ensuring that the creep behavior is accurately represented in varying humidity conditions.",
        "latexSymbol": "\\alpha_{2}",
        "latexEquation": "[\\frac{35}{\\sym{f_{cm}}}]^{0.2}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_7"
        ]
    },
    {
        "id": "G16_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.8c)"
        ],
        "title": "Concrete strength influence coefficient for βH",
        "description": "This factor adjusts the relative humidity and notional size coefficient for concretes with compressive strengths greater than 35 MPa. While it does not directly affect the relative humidity or notional size, it reduces the constants and limits in the calculation, refining the impact of these parameters on the creep behavior of stronger concretes.",
        "latexSymbol": "\\alpha_{3}",
        "latexEquation": "[\\frac{35}{\\sym{f_{cm}}}]^{0.5}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_7"
        ]
    },
    {
        "id": "G16_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.4)"
        ],
        "title": "Concrete strength adjustment factor",
        "description": "The concrete strength factor adjusts the notional creep coefficient to reflect the impact of the concrete's compressive strength. Stronger concrete typically exhibits less creep, and this factor helps quantify that relationship.",
        "latexSymbol": "\\beta(f_{cm})",
        "latexEquation": "\\frac{16.8}{\\sqrt{\\sym{f_{cm}}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_7"
        ]
    },
    {
        "id": "G16_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(3)"
        ],
        "title": "Temperature during time period",
        "description": "This term refers to the temperature, measured in degrees Celsius, during a specific time period. It is used to calculate the effect of temperature on the maturity and aging process of concrete over that period.",
        "latexSymbol": "T(\\Delta{t_{i}})",
        "type": "number",
        "unit": "°C",
        "notation": "standard",
        "decimal": 1,
        "default": 10,
        "limits": {
            "exMin": 0
        },
        "useStd": True
    },
    {
        "id": "G16_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(1)"
        ],
        "title": "Duration of temperature exposure",
        "description": "This represents the number of days during which a specific temperature is maintained. It accounts for the influence of consistent temperature conditions on material properties over time.",
        "latexSymbol": "\\Delta{t_{i}}",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 0,
        "default": 3,
        "limits": {
            "exMin": 0
        },
        "useStd": True
    },
    {
        "id": "G16_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.9)"
        ],
        "title": "Modified concrete age of loading for cement type effect",
        "description": "The age of loading is modified to account for the effect of the type of cement on the creep coefficient of concrete. This adjustment ensures that the influence of cement type is considered in the concrete's behavior over time.",
        "latexSymbol": "t_{0}",
        "latexEquation": "\\max(\\sym{t_{0,T}} \\times (\\frac{9}{(2 + \\sym{t_{0,T}}^{1.2})}+1)^{\\sym{\\alpha}}, 0.5)",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_9",
            "G16_COMP_8"
        ]
    },
    {
        "id": "G16_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(2)"
        ],
        "title": "Cement type power exponent",
        "description": "This exponent varies depending on the type of cement used. It adjusts the calculation to reflect the specific characteristics of the cement class: it is -1 for Class S cement, 0 for Class N cement, and 1 for Class R cement. This adjustment helps in accurately predicting the concrete's behavior based on the cement type.",
        "latexSymbol": "\\alpha",
        "latexEquation": "-1",
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
        "id": "G16_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.10)"
        ],
        "title": "Temperature-adjusted age of concrete at loading",
        "description": "This term represents the age of concrete adjusted for the effects of temperature within the range of 0 to 80°C. It replaces the standard concrete age in calculations to account for how temperature variations accelerate or slow down the curing process, thereby affecting the concrete's maturity.",
        "latexSymbol": "t_{0,T}",
        "latexEquation": "\\exp(-(\\frac{4000}{273 + \\sym{T(\\Delta{t_{i}})}} - 13.65))\\times \\sym{\\Delta{t_{i}}}",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_5",
            "G16_COMP_6"
        ]
    },
    {
        "id": "G16_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.5)"
        ],
        "title": "Concrete strength adjustment factor",
        "description": "This factor adjusts the notional creep coefficient to account for the effect of the concrete's age at the time the load is applied. It reflects how older concrete, when loaded, generally exhibits less creep, thereby modifying the creep calculation based on the age of the concrete in days at the time of loading.",
        "latexSymbol": "\\beta(t_{0})",
        "latexEquation": "\\frac{1}{(0.1 + \\sym{t_{0}}^{0.2})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_7"
        ]
    },
    {
        "id": "G16_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(1)"
        ],
        "title": "Concrete cross-sectional area",
        "description": "The concrete cross-sectional area represents the total area of the concrete member's cross-section, typically measured in square millimeters. It is used in various structural calculations, including determining the notional size of the member for creep and shrinkage analysis.",
        "latexSymbol": "A_{c}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 1,
        "default": 534694.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G16_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(1)"
        ],
        "title": "Perimeter in contact with the atmosphere",
        "description": "The perimeter in contact with the atmosphere is the length of the boundary of the concrete member that is exposed to the surrounding air. This perimeter is crucial for calculating the notional size of the member, which influences how environmental factors like humidity affect the concrete.",
        "latexSymbol": "u",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 5921.8,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G16_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.6)"
        ],
        "title": "Notional size of the member",
        "description": "The notional size of the member is a calculated value that represents the effective size of the concrete element for creep and shrinkage calculations. It is determined by the ratio of the cross-sectional area of the member to the perimeter that is exposed to the atmosphere. This value is crucial for accurately assessing the influence of the relative humidity on the concrete's behavior.",
        "latexSymbol": "h_{0}",
        "latexEquation": "\\frac{2 \\times \\sym{A_{c}}}{\\sym{u}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_11",
            "G16_COMP_12"
        ]
    },
    {
        "id": "G16_COMP_14",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(Figure 3.1)"
        ],
        "title": "Selecting relative humidity type",
        "description": "This option allows you to choose the appropriate relative humidity condition based on the environment. Available options include user input, inside conditions, or outside conditions.",
        "latexSymbol": "rhtype",
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
                    "User Input"
                ],
                [
                    "inside conditions"
                ],
                [
                    "outside conditions"
                ]
            ]
        }
    },
    {
        "id": "G16_COMP_15",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(Figure 3.1)"
        ],
        "title": "Relative humidity of the environment",
        "description": "This table presents options for relative humidity settings, allowing the user to input custom values or select predefined conditions for inside or outside environments.",
        "latexSymbol": "RH",
        "latexEquation": "\\sym{RH_{user}}",
        "type": "number",
        "unit": "%",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_14",
            "G16_COMP_23"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{rhtype} = User Input",
                    "\\sym{rhtype} = inside conditions",
                    "\\sym{rhtype} = outside conditions"
                ]
            ],
            "data": [
                [
                    "\\sym{RH_{user}}"
                ],
                [
                    "50"
                ],
                [
                    "80"
                ]
            ]
        }
    },
    {
        "id": "G16_COMP_16",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.3a)",
            "(B.3b)"
        ],
        "title": "Relative humidity adjustment factor",
        "description": "This factor adjusts the notional creep coefficient to account for the effect of ambient relative humidity. It modifies the creep behavior based on the moisture level in the environment, the size of the concrete member, and the concrete's compressive strength. This adjustment ensures that the creep calculation accurately reflects how humidity influences concrete performance over time.",
        "latexSymbol": "\\phi_{RH}",
        "latexEquation": "[1 + \\frac{(1 - \\frac{\\sym{RH}}{100})}{(0.1\\times \\sqrt[3]{\\sym{h_{0}}})}\\times \\sym{\\alpha_{1}}]\\times \\sym{\\alpha_{2}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_7",
            "G16_COMP_15",
            "G16_COMP_13",
            "G16_COMP_1",
            "G16_COMP_2"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{f_{cm}} > 35",
                    "\\sym{f_{cm}} <= 35"
                ]
            ],
            "data": [
                [
                    "[1 + \\frac{(1 - \\frac{\\sym{RH}}{100})}{(0.1\\times \\sqrt[3]{\\sym{h_{0}}})}\\times \\sym{\\alpha_{1}}]\\times \\sym{\\alpha_{2}}"
                ],
                [
                    "1 + \\frac{(1 - \\frac{\\sym{RH}}{100})}{(0.1\\times \\sqrt[3]{\\sym{h_{0}}})}"
                ]
            ]
        }
    },
    {
        "id": "G16_COMP_17",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.2)"
        ],
        "title": "Notional creep coefficient",
        "description": "The notional creep coefficient is a baseline value used to calculate the overall creep deformation of concrete. It is estimated by considering factors such as the relative humidity, the mean compressive strength of the concrete, and the age of the concrete at the time of loading.",
        "latexSymbol": "\\phi_{0}",
        "latexEquation": "\\sym{\\phi_{RH}} \\times \\sym{\\beta(f_{cm})} \\times \\sym{\\beta(t_{0})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_16",
            "G16_COMP_4",
            "G16_COMP_10"
        ]
    },
    {
        "id": "G16_COMP_19",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.1)"
        ],
        "title": "Time-dependent creep coefficient",
        "description": "The creep coefficient quantifies the time-dependent deformation of concrete under sustained load from the time of loading t0 to a later time t. It is calculated using the basic creep coefficient and the creep development factor.",
        "latexSymbol": "\\phi(t,t_{0})",
        "latexEquation": "\\sym{\\phi_{0}} \\times \\sym{\\beta_c(t,t_{0})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_17",
            "G16_COMP_20"
        ]
    },
    {
        "id": "G16_COMP_20",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.7)"
        ],
        "title": "Time-dependent creep development coefficient",
        "description": "The time-dependent creep development coefficient describes how the creep deformation of concrete evolves over time after the load is applied. It is calculated using factors that account for the time elapsed since loading and the specific characteristics of the concrete.",
        "latexSymbol": "\\beta_c(t,t_{0})",
        "latexEquation": "[\\frac{(\\sym{t} - \\sym{t_{0}})}{(\\sym{\\beta_{H}} + t - \\sym{t_{0}})}]^{0.3}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G16_COMP_22",
            "G16_COMP_7",
            "G16_COMP_21"
        ]
    },
    {
        "id": "G16_COMP_21",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(B.8a)",
            "(B.8b)"
        ],
        "title": "Relative humidity and member size coefficient",
        "description": "This coefficient depends on the relative humidity of the environment and the notional size of the concrete member. It adjusts the creep calculations based on how these two factors influence the concrete's behavior, particularly in terms of how moisture interacts with the concrete over time.",
        "latexSymbol": "\\beta_{H}",
        "latexEquation": "\\min(1.5 [1 + (0.012\\times \\sym{RH})^{18}] \\times \\sym{h_{0}} + 250 \\sym{\\alpha_{3}}, 1500 \\times \\sym{\\alpha_{3}})",
        "type": "#CHECK_NOT_IMPLEMENTED",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G14_COMP_7",
            "G16_COMP_15",
            "G16_COMP_13",
            "G16_COMP_3"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{f_{cm}} > 35",
                    "\\sym{f_{cm}} <= 35"
                ]
            ],
            "data": [
                [
                    "\\min(1.5 [1 + (0.012\\times \\sym{RH})^{18}] \\times \\sym{h_{0}} + 250 \\sym{\\alpha_{3}} , 1500 \\times \\sym{\\alpha_{3}})"
                ],
                [
                    "\\min(1.5 [1 + (0.012\\times \\sym{RH})^{18}] \\times \\sym{h_{0}} + 250 , 1500)"
                ]
            ]
        }
    },
    {
        "id": "G16_COMP_22",
        "codeName": "EN1992-1-1",
        "reference": [
            "AnnexB.1(1)"
        ],
        "title": "Age of concrete at the moment considered",
        "description": "The age of concrete at the moment considered represents the total number of days since the concrete was poured or placed. It is used to determine how much the concrete has matured, which affects its creep behavior over time.",
        "latexSymbol": "t",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 0,
        "default": 36500,
        "const": True
    },
    {
        "id": "G16_COMP_23",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.1.4(Figure 3.1)"
        ],
        "title": "User-defined relative humidity of the environment",
        "description": "This parameter allows users to manually define and input relative humidity values based on specific project requirements or environmental conditions, aside from the inside or outside conditions suggested by Eurocode.",
        "latexSymbol": "RH_{user}",
        "type": "number",
        "unit": "%",
        "notation": "standard",
        "decimal": 0,
        "default": 70,
        "limits": {
            "inMin": 40,
            "inMax": 100
        },
        "useStd": False
    }
]