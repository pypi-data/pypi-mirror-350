component_list = [
    {
        "id": "G37_COMP_1",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "4.3.3(Table4.3)"
        ],
        "title": "Design situation selection",
        "description": "Select the applicable design situation for the concrete structure. Each situation corresponds to different load conditions and factors that impact structural requirements and safety considerations.",
        "latexSymbol": "designsitu",
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
                    "Persistent and transient design situation",
                    "Standard load conditions expected over the structure's lifespan, including both short- and long-term loads."
                ],
                [
                    "Fatigue design situation",
                    "Load conditions that consider repetitive or cyclic loading, such as from machinery or traffic."
                ],
                [
                    "Accidental design situation",
                    "Unusual or extreme load conditions due to accidents or unforeseen events, impacting structural resilience."
                ],
                [
                    "Serviceability limit state",
                    "Conditions that ensure the structure’s functionality, durability, and comfort under regular use."
                ]
            ]
        }
    },
    {
        "id": "G37_COMP_2",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "4.3.3(Table4.3)"
        ],
        "title": "Partial factor for concrete",
        "description": "This factor accounts for the variability and uncertainties in concrete strength, providing a safety margin in design calculations. It is applied to ensure the concrete can reliably withstand applied loads under different conditions.",
        "latexSymbol": "\\gamma_{c}",
        "latexEquation": "1.50",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G37_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{designsitu} = Persistent and transient design situation",
                    "\\sym{designsitu} = Fatigue design situation",
                    "\\sym{designsitu} = Accidental design situation",
                    "\\sym{designsitu} = Serviceability limit state"
                ]
            ],
            "data": [
                [
                    "1.50"
                ],
                [
                    "1.50"
                ],
                [
                    "1.15"
                ],
                [
                    "1.00"
                ]
            ]
        }
    },
    {
        "id": "G37_COMP_3",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "4.3.3(Table4.3)"
        ],
        "title": "Partial factor for reinforcing or prestressing steel",
        "description": "This factor addresses the variability and uncertainties in reinforcing or prestressing steel strength, ensuring reliable performance across different design situations. It adjusts for differences in risk levels, with higher factors often used in standard conditions and lower factors in accidental or serviceability situations.",
        "latexSymbol": "\\gamma_{s}",
        "latexEquation": "1.15",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G37_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{designsitu} = Persistent and transient design situation",
                    "\\sym{designsitu} = Fatigue design situation",
                    "\\sym{designsitu} = Accidental design situation",
                    "\\sym{designsitu} = Serviceability limit state"
                ]
            ],
            "data": [
                [
                    "1.15"
                ],
                [
                    "1.15"
                ],
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
        "id": "G37_COMP_4",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.3(Table5.1)"
        ],
        "title": "Strength classes for concrete",
        "description": "This term refers to the classification of concrete based on its compressive strength, allowing for standardized strength categories used in design. These classes help engineers select appropriate concrete strength levels for various structural applications.",
        "latexSymbol": "f",
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
                ],
                [
                    "C100/115"
                ]
            ]
        }
    },
    {
        "id": "G37_COMP_5",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.3(Table5.1)"
        ],
        "title": "Characteristic concrete cylinder compressive strength",
        "description": "This term represents the characteristic compressive strength of concrete measured using a standard cylinder, typically defined at the 5th percentile. It serves as a lower-bound value in design to ensure concrete meets minimum compressive strength requirements under typical conditions.",
        "latexSymbol": "f_{ck}",
        "latexEquation": "12",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G37_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{f} = C12/15",
                    "\\sym{f} = C16/20",
                    "\\sym{f} = C20/25",
                    "\\sym{f} = C25/30",
                    "\\sym{f} = C30/37",
                    "\\sym{f} = C35/45",
                    "\\sym{f} = C40/50",
                    "\\sym{f} = C45/55",
                    "\\sym{f} = C50/60",
                    "\\sym{f} = C55/67",
                    "\\sym{f} = C60/75",
                    "\\sym{f} = C70/85",
                    "\\sym{f} = C80/95",
                    "\\sym{f} = C90/105",
                    "\\sym{f} = C100/115"
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
                ],
                [
                    "100"
                ]
            ]
        }
    },
    {
        "id": "G37_COMP_6",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.3(Table5.1)"
        ],
        "title": "Mean concrete cylinder compressive strength",
        "description": "This term represents the average compressive strength of concrete measured using a standard cylinder, providing a central value for expected compressive strength. It is used in design to assess the typical compressive capacity of concrete under standard conditions.",
        "latexSymbol": "f_{cm}",
        "latexEquation": "\\sym{f_{ck}} + 8",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G37_COMP_5"
        ]
    },
    {
        "id": "G37_COMP_7",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.3(Table5.1)"
        ],
        "title": "Mean axial tensile strength of concrete",
        "description": "This term represents the average axial tensile strength of concrete, providing a central value for expected tensile strength. It is used in design calculations to model the typical tensile behavior of concrete under normal conditions.",
        "latexSymbol": "f_{ctm}",
        "latexEquation": "0.3 \\times \\sym{f_{ck}}^{2/3}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_5"
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
                    "0.3 \\times \\sym{f_{ck}}^{2/3}"
                ],
                [
                    "1.1 \\times \\sym{f_{ck}}^{1/3}"
                ]
            ]
        }
    },
    {
        "id": "G37_COMP_8",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.3(Table5.1)"
        ],
        "title": "Characteristic axial tensile strength of concrete at 5% fractile",
        "description": "This term represents the axial tensile strength of concrete at the 5th percentile, indicating a conservative or lower-bound strength level. It is used in design to ensure safety by accounting for the minimum expected tensile strength of concrete under typical conditions.",
        "latexSymbol": "f_{ctk,0.05}",
        "latexEquation": "0.7 \\times \\sym{f_{ctm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_7"
        ]
    },
    {
        "id": "G37_COMP_9",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.3(Table5.1)"
        ],
        "title": "Characteristic axial tensile strength of concrete at 95% fractile",
        "description": "This term represents the axial tensile strength of concrete at the 95th percentile, indicating a higher-than-average strength level. It is used in design to account for the concrete’s tensile strength in conditions where higher strength is expected.",
        "latexSymbol": "f_{ctk,0.95}",
        "latexEquation": "1.3 \\times \\sym{f_{ctm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_7"
        ]
    },
    {
        "id": "G37_COMP_10",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.4(5.1)"
        ],
        "title": "Secant modulus of elasticity of concrete",
        "description": "This term represents the secant modulus of elasticity for concrete, which is calculated between zero stress and a specific stress level. It provides a measure of concrete's stiffness and is used in design to assess how concrete deforms under load.",
        "latexSymbol": "E_{cm}",
        "latexEquation": "\\sym{k_{E}} \\times \\sym{f_{cm}}^{1/3}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G37_COMP_11",
            "G37_COMP_6"
        ]
    },
    {
        "id": "G37_COMP_11",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.4(2)"
        ],
        "title": "Adjusting factor for the modulus of elasticity of concrete based on aggregate type",
        "description": "For concrete with quartzite aggregates, the factor is typically set at 9500. For other aggregate types, the factor can range from 5000 to 13000, depending on the specific characteristics of the aggregates used. This adjustment ensures that the modulus of elasticity reflects the material properties of different aggregate compositions.",
        "latexSymbol": "k_{E}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 0,
        "default": 9500.0,
        "limits": {
            "inMin": 5000,
            "inMax": 13000
        },
        "useStd": True
    },
    {
        "id": "G37_COMP_12",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(5.3)"
        ],
        "title": "Design value of concrete compressive strength",
        "description": "This term represents the adjusted compressive strength of concrete used in design calculations, taking into account safety factors and material variability. It is essential for assessing the concrete’s ability to resist compressive forces in structural applications.",
        "latexSymbol": "f_{cd}",
        "latexEquation": "\\sym{\\eta_{cc}} \\times \\sym{k_{tc}} \\times (\\frac{f_{ck}}{ \\sym{\\gamma_{c}}})",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_13",
            "G37_COMP_15",
            "G37_COMP_5",
            "G37_COMP_2"
        ]
    },
    {
        "id": "G37_COMP_13",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(5.4)"
        ],
        "title": "Adjustment factor for effective compressive strength",
        "description": "This factor accounts for the difference between the undisturbed compressive strength of a cylinder and the compressive strength that can actually be achieved in a structural component.",
        "latexSymbol": "\\eta_{cc}",
        "latexEquation": "\\min((\\frac{\\sym{f_{ck,ref}}}{\\sym{f_{ck}}})^{1/3} , 1.0)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_14",
            "G37_COMP_5"
        ]
    },
    {
        "id": "G37_COMP_14",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(1)"
        ],
        "title": "Reference compressive strength for design",
        "description": "This value represents the standard reference compressive strength, typically set at 40 MPa, used to calibrate design factors such as the factor accounting for effective strength differences. It provides a baseline for adjusting strength values based on varying concrete compositions or conditions.",
        "latexSymbol": "f_{ck,ref}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 0,
        "default": 40.0,
        "const": True
    },
    {
        "id": "G37_COMP_15",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(1)"
        ],
        "title": "Coefficient for sustained load impact on compressive strength",
        "description": "This coefficient accounts for the reduction in concrete's compressive strength due to prolonged exposure to high loads over time. For characteristic compressive strength at the reference age, the coefficient is taken as 1.0, while for time-dependent compressive strength, it is reduced to 0.85.",
        "latexSymbol": "k_{tc}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 1.0,
        "const": True
    },
    {
        "id": "G37_COMP_16",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(5.5)"
        ],
        "title": "Design value of the tensile strength of concrete",
        "description": "This term represents the tensile strength of concrete used in design calculations, adjusted for safety and material variability factors. It is a critical parameter in determining the concrete’s capacity to withstand tensile forces without cracking or failure.",
        "latexSymbol": "f_{ctd}",
        "latexEquation": "\\sym{k_{tt}} \\times (\\frac{\\sym{f_{ctk,0.05}}}{\\sym{\\gamma_{c}}})",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_17",
            "G37_COMP_8",
            "G37_COMP_2"
        ]
    },
    {
        "id": "G37_COMP_17",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(2)"
        ],
        "title": "Coefficient for sustained load impact on tensile strength",
        "description": "This coefficient accounts for the reduction in concrete's tensile strength due to prolonged exposure to high loads over time. For characteristic tensile strength at the reference age, the coefficient is taken as 0.8, while for time-dependent tensile strength, it is reduced to 0.7.",
        "latexSymbol": "k_{tt}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "default": 0.8,
        "const": True
    },
    {
        "id": "G37_COMP_18",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(5.6)"
        ],
        "title": "Compressive stress in the concrete",
        "description": "This term represents the stress exerted on concrete when it is subjected to compressive forces. It is a key factor in design calculations, used to assess the concrete’s ability to withstand loads without failing in compression.",
        "latexSymbol": "\\sigma_{c}",
        "latexEquation": "(\\frac{(\\sym{k} \\times \\sym{\\eta} - \\sym{\\eta}^{2})}{(1 + (\\sym{k} -2) \\times \\sym{\\eta})}) \\times \\sym{f_{cm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_19",
            "G37_COMP_20",
            "G37_COMP_6"
        ]
    },
    {
        "id": "G37_COMP_19",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(3)"
        ],
        "title": "Factor for stress-strain relationship in concrete under compression",
        "description": "This factor adjusts the stress-strain relationship in concrete, accounting for the modulus of elasticity and specific strain conditions. It is used in design formulas to accurately model the behavior of concrete under uniaxial compressive loads over a short term.",
        "latexSymbol": "k",
        "latexEquation": "1.05 \\times \\sym{E_{cm}} \\times (\\frac{\\sym{\\epsilon_{c1}}}{\\sym{f_{cm}}})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_10",
            "G37_COMP_21",
            "G37_COMP_6"
        ]
    },
    {
        "id": "G37_COMP_20",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(3)"
        ],
        "title": "Ratio of strains used to define stress-strain model",
        "description": "This term represents the ratio of actual strain in the concrete to a reference strain value. It normalizes strain values, allowing for a more standardized assessment of the concrete’s behavior under compressive loads.",
        "latexSymbol": "\\eta",
        "latexEquation": "\\frac{\\sym{\\epsilon_{c}}}{\\sym{\\epsilon_{c1}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_22",
            "G37_COMP_21"
        ]
    },
    {
        "id": "G37_COMP_21",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(3)"
        ],
        "title": "Strain at maximum compressive stress",
        "description": "This term represents the strain value in concrete at the point of maximum compressive stress. It serves as a reference in defining the stress-strain relationship for concrete under compression and is essential for calculating normalized strain ratios in design models.",
        "latexSymbol": "\\epsilon_{c1}",
        "latexEquation": "\\min(0.7 \\times \\sym{f_{cm}}^{1/3} , 2.8)",
        "type": "number",
        "unit": "‰",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_6"
        ]
    },
    {
        "id": "G37_COMP_22",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.6(3)"
        ],
        "title": "Compressive strain in the concrete",
        "description": "This term represents the amount of strain in concrete when subjected to compressive stress. It is a key parameter in defining the concrete's behavior under load and is often compared to the reference strain εc1 to assess the normalized strain ratio in stress-strain models.",
        "latexSymbol": "\\epsilon_{c}",
        "latexEquation": "\\min(2.8 + 14 \\times (1 - \\frac{\\sym{f_{cm}}}{108})^{4} , 3.5)",
        "type": "number",
        "unit": "‰",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_6"
        ]
    },
    {
        "id": "G37_COMP_23",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.2.2(Table5.4)"
        ],
        "title": "Strength classes of reinforcing steel",
        "description": "This classification denotes the minimum yield strength of reinforcing steel, with each class (e.g., B400, B500) indicating strength in megapascals (MPa). Higher classes are selected for structures requiring greater load capacity.",
        "latexSymbol": "rebarclass",
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
                    "B400"
                ],
                [
                    "B450"
                ],
                [
                    "B500"
                ],
                [
                    "B550"
                ],
                [
                    "B600"
                ],
                [
                    "B700"
                ]
            ]
        }
    },
    {
        "id": "G37_COMP_24",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.2.2(Table5.4)"
        ],
        "title": "Characteristic value of yield strength of reinforcement",
        "description": "This term represents the characteristic yield strength of reinforcing steel, or if the yield phenomenon is not present, the 0.2% proof strength. It is a key parameter in design, defining the stress level at which the steel begins to deform permanently.",
        "latexSymbol": "f_{yk}",
        "latexEquation": "400",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G37_COMP_23"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{rebarclass} = B400",
                    "\\sym{rebarclass} = B450",
                    "\\sym{rebarclass} = B500",
                    "\\sym{rebarclass} = B550",
                    "\\sym{rebarclass} = B600",
                    "\\sym{rebarclass} = B700"
                ]
            ],
            "data": [
                [
                    "400"
                ],
                [
                    "450"
                ],
                [
                    "500"
                ],
                [
                    "550"
                ],
                [
                    "600"
                ],
                [
                    "700"
                ]
            ]
        }
    },
    {
        "id": "G37_COMP_25",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.2.4(5.11)"
        ],
        "title": "Design yield strength of reinforcement",
        "description": "This term represents the design yield strength of reinforcing steel, calculated by applying a partial safety factor to the characteristic yield strength. It is used in structural design to ensure that the reinforcement can safely withstand loads within specified limits.",
        "latexSymbol": "f_{yd}",
        "latexEquation": "\\frac{\\sym{f_{yk}}}{\\sym{\\gamma_{s}}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_24",
            "G37_COMP_3"
        ]
    },
    {
        "id": "G37_COMP_26",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "5.1.3(2)"
        ],
        "title": "Reference age of concrete for strength determination",
        "description": "This term refers to the specific reference age, in days, at which the concrete strength is measured. It is commonly set at 28 days as a standard for assessing the compressive strength of concrete.",
        "latexSymbol": "t_{ref}",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 0,
        "default": 28.0,
        "const": True
    },
    {
        "id": "G37_COMP_27",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.3(TableB.1)"
        ],
        "title": "Concrete strength class selection",
        "description": "Select the appropriate concrete strength class based on the type of cement, cement strength, and binder composition. Each class defines specific material properties used in design calculations for time-dependent behavior and durability.",
        "latexSymbol": "concclass",
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
                    "CS",
                    "Type: CEM III, CEM II/B; Cement Strength Class: 32,5 N; 42,5 N; Binder Composition: Portland cement clinker with more than 65% ggbs or more than 35% fly ash (fa)"
                ],
                [
                    "CN",
                    "Type: CEM II, CEM I; Cement Strength Class: 42,5 N; 32,5 R; Binder Composition: Portland cement clinker with 35-65% ggbs or 20-35% fly ash (fa)"
                ],
                [
                    "CR",
                    "Type: CEM I; Cement Strength Class: 42,5 R; 52,5 N; 52,5 R; Binder Composition: -"
                ]
            ]
        }
    },
    {
        "id": "G37_COMP_28",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.4(B.2)"
        ],
        "title": "Age of the concrete being considered",
        "description": "This term represents the specific age of the concrete at which its properties are evaluated, where t is less than or equal to the reference age. It is used to assess how concrete characteristics develop over time.",
        "latexSymbol": "t",
        "type": "number",
        "unit": "days",
        "notation": "standard",
        "decimal": 0,
        "default": 3.0,
        "limits": {
            "exMin": 0,
            "inMax": 28
        }
    },
    {
        "id": "G37_COMP_29",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.4(B.1)"
        ],
        "title": "Mean concrete cylinder compressive strength at age t",
        "description": "This term represents the average compressive strength of a concrete cylinder at an age t, up to the reference age (typically 28 days). It is used to evaluate the early-age strength development of concrete in design calculations.",
        "latexSymbol": "f_{cm}(t)",
        "latexEquation": "\\sym{\\beta_{cc}(t)} \\times \\sym{f_{cm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_30",
            "G37_COMP_6"
        ]
    },
    {
        "id": "G37_COMP_30",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.4(B.2)"
        ],
        "title": "Age-dependent coefficient for compressive strength of concrete",
        "description": "This coefficient is used to determine the compressive strength of concrete based on its age, t. It accounts for the increase in strength as the concrete matures over time, allowing for accurate strength predictions in design calculations.",
        "latexSymbol": "\\beta_{cc}(t)",
        "latexEquation": "\\exp(\\sym{s_{c}} \\times (1 - \\sqrt{\\frac{\\sym{t_{ref}}}{\\sym{t}}}) \\times \\sqrt{\\frac{28}{\\sym{t_{ref}}}})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_31",
            "G37_COMP_26",
            "G37_COMP_28"
        ]
    },
    {
        "id": "G37_COMP_31",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.4(TableB.2)"
        ],
        "title": "Coefficient based on concrete strength class",
        "description": "This coefficient varies depending on the strength class of the concrete. It is used in design calculations to adjust for creep and long-term deformation, ensuring that the concrete's behavior over time is accurately represented according to its specified class.",
        "latexSymbol": "s_{c}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G37_COMP_27",
            "G37_COMP_5"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{f_{ck}} <= 35",
                    "35 < \\sym{f_{ck}} < 60",
                    "\\sym{f_{ck}} >= 60"
                ],
                [
                    "\\sym{concclass} = CS",
                    "\\sym{concclass} = CN",
                    "\\sym{concclass} = CR"
                ]
            ],
            "data": [
                [
                    "0.6",
                    "0.5",
                    "0.3"
                ],
                [
                    "0.5",
                    "0.4",
                    "0.2"
                ],
                [
                    "0.4",
                    "0.3",
                    "0.1"
                ]
            ]
        }
    },
    {
        "id": "G37_COMP_32",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.4(B.3)"
        ],
        "title": "Mean concrete axial tensile strength at age t",
        "description": "This term represents the average axial tensile strength of concrete at a specific age t. It is used in design calculations to determine how the tensile strength of concrete develops over time.",
        "latexSymbol": "f_{ctm}(t)",
        "latexEquation": "\\sym{\\beta_{cc}(t)}^{0.6} \\times \\sym{f_{ctm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_30",
            "G37_COMP_7"
        ]
    },
    {
        "id": "G37_COMP_33",
        "codeName": "2G:EN1992-1-1",
        "reference": [
            "B.4(B.4)"
        ],
        "title": "Secant modulus of elasticity of concrete at age t",
        "description": "This term represents the secant modulus of elasticity of concrete at a specific age t, indicating its stiffness at that stage. It is used in design calculations to evaluate the development of concrete's elasticity over time, which is important for understanding its deformation response under load.",
        "latexSymbol": "E_{cm}(t)",
        "latexEquation": "\\sym{\\beta_{cc}(t)}^{1/3} \\times \\sym{E_{cm}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G37_COMP_30",
            "G37_COMP_10"
        ]
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/130287306/2G+EN1992-1-1+Material+Properties+and+Parameters
        'id': '37',
        'standardType': '2G:EUROCODE',
        'codeName': '2G:EN1992-1-1',
        'codeTitle': 'Eurocode 2 — Design of concrete structures - Part 1-1: General rules and rules for buildings, bridges and civil engineering structures',
        'title': 'Concrete and Reinforcement Properties and Design Parameter Calculation',
        'description': r"[2G:EN1992-1-1] This guide provides a comprehensive overview of the essential parameters for concrete and reinforcement bar design based on the Eurocode 2nd Generation standards. It includes step-by-step instructions on calculating key values such as compressive and tensile strengths, and modulus of elasticity, using the specific factors and reference values defined by Eurocode. Designed for engineers and designers, this guide ensures that all concrete and reinforcement bar parameters are calculated to meet the required safety and performance standards in structural applications.",
        'edition': '2023',
        'targetComponents': ['G37_COMP_9', 'G37_COMP_12', 'G37_COMP_16', 'G37_COMP_18', 'G37_COMP_25', 'G37_COMP_29', 'G37_COMP_32', 'G37_COMP_33'],
        'testInput': [
            {'component': 'G37_COMP_1', 'value': 'Persistent and transient design situation'},
            {'component': 'G37_COMP_4', 'value': 'C20/25'},
            {'component': 'G37_COMP_11', 'value': 9500},
            {'component': 'G37_COMP_23', 'value': 'B400'},
            {'component': 'G37_COMP_27', 'value': 'CS'},
            {'component': 'G37_COMP_28', 'value': 20},
        ],
    }
]