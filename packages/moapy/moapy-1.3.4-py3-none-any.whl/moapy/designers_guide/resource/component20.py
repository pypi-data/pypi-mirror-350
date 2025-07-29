component_list = [
    {
        "id": "G20_COMP_1",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.10.2.1(5.41)"
        ],
        "title": "Maximum prestressing force during tensioning",
        "description": "The maximum prestressing force during tensioning, denoted as Pmax, is the highest permissible force that can be applied to a prestressing tendon during the tensioning process. It is calculated based on the tendon’s cross-sectional area and the maximum stress limits, which are determined by the material properties and national standards.",
        "latexSymbol": "P_{max}",
        "latexEquation": "\\sym{A_{p}} \\times \\sym{\\sigma_{p,max}}\\times 10^{-3}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G20_COMP_2",
            "G20_COMP_3"
        ]
    },
    {
        "id": "G20_COMP_2",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.10.2.1(1)"
        ],
        "title": "Cross-sectional area of the tendon",
        "description": "The cross-sectional area of the tendon represents the total area of the tendon’s cross-section. This value is crucial for calculating the stress applied to the tendon during the prestressing process, as it directly affects the maximum allowable force that can be safely applied to the tendon.",
        "latexSymbol": "A_{p}",
        "latexEquation": "\\sym{S_{n}}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G20_COMP_16"
        ]
    },
    {
        "id": "G20_COMP_3",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.10.2.1(1)"
        ],
        "title": "Maximum stress applied to the tendon",
        "description": "The maximum stress applied to the tendon refers to the highest level of stress that can be safely exerted on the tendon during the prestressing process. This value is determined by the material properties and is used to calculate the maximum permissible force to avoid overstressing the tendon.",
        "latexSymbol": "\\sigma_{p,max}",
        "latexEquation": "\\min(\\sym{k_{1}} \\times \\sym{f_{pk}}, \\sym{k_{2}} \\times \\sym{f_{p0,1k}})",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G20_COMP_4",
            "G20_COMP_6",
            "G20_COMP_5",
            "G20_COMP_7"
        ]
    },
    {
        "id": "G20_COMP_4",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.10.2.1(1)"
        ],
        "title": "Coefficient for ultimate tensile strength",
        "description": "This coefficient is applied to the characteristic tensile strength of the prestressing steel, determining the maximum allowable stress that can be applied to the tendon based on its ultimate tensile strength. It is used to ensure that the stress in the tendon does not exceed a safe limit relative to the steel's maximum capacity.",
        "latexSymbol": "k_{1}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "default": 0.8,
        "const": True
    },
    {
        "id": "G20_COMP_5",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.10.2.1(1)"
        ],
        "title": "Coefficient for 0.1% proof strength",
        "description": "This coefficient is applied to the 0.1% proof strength of the prestressing steel, setting an additional limit on the maximum allowable stress that can be applied to the tendon. It ensures that the stress in the tendon remains within a safe range based on the steel's proof strength, which is a measure of its ability to resist permanent deformation.",
        "latexSymbol": "k_{2}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "default": 0.9,
        "const": True
    },
    {
        "id": "G20_COMP_6",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.3.1(5)"
        ],
        "title": "Characteristic tensile strength of prestressing steel",
        "description": "This represents the characteristic tensile strength of the prestressing steel, which is the stress level at which the steel is expected to break or fail under tension. It is a key parameter in designing prestressed concrete structures, ensuring that the material can withstand the required loads without failure.",
        "latexSymbol": "f_{pk}",
        "latexEquation": "\\sym{R_{m}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G20_COMP_17"
        ]
    },
    {
        "id": "G20_COMP_7",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.3.1(5)"
        ],
        "title": "Characteristic 0.1% proof stress of prestressing steel",
        "description": "This is the characteristic 0.1% proof strength, indicating the stress level at which the prestressing steel undergoes 0.1% permanent deformation. It is used to ensure that the steel remains within its elastic limit under operational loads, preventing permanent deformation in the structure.",
        "latexSymbol": "f_{p0,1k}",
        "latexEquation": "\\frac{\\sym{F_{p0,1}}\\times1000}{\\sym{S_{n}}}",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G20_COMP_19",
            "G20_COMP_16"
        ]
    },
    {
        "id": "G20_COMP_8",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.10.2.1(5.43)"
        ],
        "title": "Initial prestress force at distance x",
        "description": "The initial prestress force at distance x is calculated by subtracting immediate losses from the maximum tensioning force. This force is applied to the concrete right after tensioning or transfer and must not exceed the maximum value determined by the tendon’s cross-sectional area and allowable stress.",
        "latexSymbol": "P_{m0}(x)",
        "latexEquation": "\\sym{A_{p}} \\times \\sym{\\sigma_{pm0}(x)} \\times 10^{-3}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G20_COMP_2",
            "G20_COMP_9"
        ]
    },
    {
        "id": "G20_COMP_9",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.10.3(2)"
        ],
        "title": "Allowable stress at initial prestress",
        "description": "The allowable stress at initial prestress is the maximum stress that can be applied to the tendon at a specific distance x during the initial prestressing phase. This stress value ensures the safety and integrity of the tendon and the surrounding concrete, preventing overstressing during the early stages of prestressing.",
        "latexSymbol": "\\sigma_{pm0}(x)",
        "latexEquation": "\\min(\\sym{k_{7}} \\times \\sym{f_{pk}}, \\sym{k_{8}} \\times \\sym{f_{p0,1k}})",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G20_COMP_10",
            "G20_COMP_6",
            "G20_COMP_11",
            "G20_COMP_7"
        ]
    },
    {
        "id": "G20_COMP_10",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.10.3(2)"
        ],
        "title": "Coefficient for ultimate tensile strength in initial prestress",
        "description": "The coefficient for ultimate tensile strength in initial prestress is applied to the ultimate tensile strength of the prestressing steel to determine the maximum allowable stress during the initial prestressing phase. This coefficient ensures that the stress remains within safe limits based on the steel's ultimate capacity.",
        "latexSymbol": "k_{7}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "default": 0.75,
        "const": True
    },
    {
        "id": "G20_COMP_11",
        "codeName": "EN1992-1-1",
        "reference": [
            "5.10.3(2)"
        ],
        "title": "Coefficient for 0.1% proof strength in initial prestress",
        "description": "The coefficient for 0.1% proof strength in initial prestress is applied to the 0.1% proof strength of the prestressing steel to set the maximum allowable stress during the initial prestressing phase. This coefficient ensures that the stress does not exceed the elastic limit of the steel.",
        "latexSymbol": "k_{8}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 2,
        "default": 0.85,
        "const": True
    },
    {
        "id": "G20_COMP_12",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.3.6(4)"
        ],
        "title": "Select design standard for mass calculation",
        "description": "Choose the design standard to calculate the mass of the selected strand. You can apply either EN 10138-3, which uses a density of 7.81 kg/dm³ for prestressing steel strands, or EN 1992-1-1, which uses a density of 7850 kg/m³ for steel reinforcement in concrete structures. Select the appropriate standard to calculate the mass based on the specific material characteristics.",
        "latexSymbol": "standmass",
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
                    "Based on EN 10138-3 (7.81kg/dm^{3})"
                ],
                [
                    "Based on EN 1992-1-1 3.3.6 (7,850kg/m^{3})"
                ]
            ]
        }
    },
    {
        "id": "G20_COMP_13",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.3.6(4)"
        ],
        "title": "Mass per Metre of Selected Strand",
        "description": "This table provides options for calculating the mass per meter of the selected strand based on different standards. Users can choose to calculate the mass using either EN 10138-3 (Tables 3 & 4) or EN 1992-1-1 (3.3.6 (4)) to comply with specific design requirements.",
        "latexSymbol": "M",
        "latexEquation": "\\sym{S_{n}} \\times 7.81",
        "type": "number",
        "unit": "g/m",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G20_COMP_12",
            "G20_COMP_16"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{standmass} = Based on EN 10138-3 (7.81kg/dm^{3})",
                    "\\sym{standmass} = Based on EN 1992-1-1 3.3.6 (7,850kg/m^{3})"
                ]
            ],
            "data": [
                [
                    "\\sym{S_{n}} \\times 7.81"
                ],
                [
                    "\\sym{S_{n}} \\times (\\frac{7850}{1000})"
                ]
            ]
        }
    },
    {
        "id": "G20_COMP_14",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.3.1(5)"
        ],
        "title": "Select strand type for high tensile steel wire",
        "description": "This table allows users to select strand grades, listing a variety of strand options based on the number of wires and their respective tensile strengths. The grades are categorized by wire count (2-wire, 3-wire, 7-wire, and 7G-wire) and tensile strength values, making it easy to choose the appropriate strand for specific construction needs. For more detailed information, refer to EN 10138-3 (Table 3).",
        "latexSymbol": "strandgrade",
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
                    "(2-Wire)Y1770S2-5.6"
                ],
                [
                    "(2-Wire)Y1770S2-6.0"
                ],
                [
                    "(2-Wire)Y1860S2-4.5"
                ],
                [
                    "(3-Wire)Y1770S3-7.5"
                ],
                [
                    "(3-Wire)Y1860S3-4.85"
                ],
                [
                    "(3-Wire)Y1860S3-6.5"
                ],
                [
                    "(3-Wire)Y1860S3-6.9"
                ],
                [
                    "(3-Wire)Y1860S3-7.5"
                ],
                [
                    "(3-Wire)Y1860S3-8.6"
                ],
                [
                    "(3-Wire)Y1920S3-6.3"
                ],
                [
                    "(3-Wire)Y1920S3-6.5"
                ],
                [
                    "(3-Wire)Y1960S3-6.8"
                ],
                [
                    "(3-Wire)Y1960S3-5.2"
                ],
                [
                    "(3-Wire)Y1960S3-6.5"
                ],
                [
                    "(3-Wire)Y1960S3-6.85"
                ],
                [
                    "(3-Wire)Y2060S3-5.2"
                ],
                [
                    "(3-Wire)Y2160S3-5.2"
                ],
                [
                    "(7-Wire)Y1670S7-15.2"
                ],
                [
                    "(7-Wire)Y1770S7-6.9"
                ],
                [
                    "(7-Wire)Y1770S7-9.0"
                ],
                [
                    "(7-Wire)Y1770S7-9.3"
                ],
                [
                    "(7-Wire)Y1770S7-9.6"
                ],
                [
                    "(7-Wire)Y1770S7-11.0"
                ],
                [
                    "(7-Wire)Y1770S7-12.5"
                ],
                [
                    "(7-Wire)Y1770S7-12.9"
                ],
                [
                    "(7-Wire)Y1770S7-15.2"
                ],
                [
                    "(7-Wire)Y1770S7-15.3"
                ],
                [
                    "(7-Wire)Y1770S7-15.7"
                ],
                [
                    "(7-Wire)Y1770S7-18.0"
                ],
                [
                    "(7-Wire)Y1860S7-6.9"
                ],
                [
                    "(7-Wire)Y1860S7-7.0"
                ],
                [
                    "(7-Wire)Y1860S7-8.0"
                ],
                [
                    "(7-Wire)Y1860S7-9.0"
                ],
                [
                    "(7-Wire)Y1860S7-9.3"
                ],
                [
                    "(7-Wire)Y1860S7-9.6"
                ],
                [
                    "(7-Wire)Y1860S7-11.0"
                ],
                [
                    "(7-Wire)Y1860S7-11.3"
                ],
                [
                    "(7-Wire)Y1860S7-12.5"
                ],
                [
                    "(7-Wire)Y1860S7-12.9"
                ],
                [
                    "(7-Wire)Y1860S7-13.0"
                ],
                [
                    "(7-Wire)Y1860S7-15.2"
                ],
                [
                    "(7-Wire)Y1860S7-15.3"
                ],
                [
                    "(7-Wire)Y1860S7-15.7"
                ],
                [
                    "(7-Wire)Y1960S7-9.0"
                ],
                [
                    "(7-Wire)Y1960S7-9.3"
                ],
                [
                    "(7-Wire)Y2060S7-6.4"
                ],
                [
                    "(7-Wire)Y2060S7-6.85"
                ],
                [
                    "(7-Wire)Y2060S7-7.0"
                ],
                [
                    "(7-Wire)Y2060S7-8.6"
                ],
                [
                    "(7-Wire)Y2060S7-11.3"
                ],
                [
                    "(7-Wire)Y2160S7-6.85"
                ],
                [
                    "(7G-Wire)Y1700S7G-18.0"
                ],
                [
                    "(7G-Wire)Y1820S7G-15.2"
                ],
                [
                    "(7G-Wire)Y1860S7G-12.7"
                ],
                [
                    "(7G-Wire)Y1860S7G-15.2"
                ]
            ]
        }
    },
    {
        "id": "G20_COMP_15",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.3.1(5)"
        ],
        "title": "Nominal strand diameter",
        "description": "This column specifies the diameter of the strand or individual wires within the strand. The diameter is a critical factor that influences the strand's strength and suitability for various applications. For more detailed information, refer to EN 10138-3 (Table 3).",
        "latexSymbol": "d",
        "latexEquation": "5.60",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G20_COMP_14"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{strandgrade} = (2-Wire)Y1770S2-5.6",
                    "\\sym{strandgrade} = (2-Wire)Y1770S2-6.0",
                    "\\sym{strandgrade} = (2-Wire)Y1860S2-4.5",
                    "\\sym{strandgrade} = (3-Wire)Y1770S3-7.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-4.85",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-6.9",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-7.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-8.6",
                    "\\sym{strandgrade} = (3-Wire)Y1920S3-6.3",
                    "\\sym{strandgrade} = (3-Wire)Y1920S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.8",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-5.2",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.85",
                    "\\sym{strandgrade} = (3-Wire)Y2060S3-5.2",
                    "\\sym{strandgrade} = (3-Wire)Y2160S3-5.2",
                    "\\sym{strandgrade} = (7-Wire)Y1670S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-6.9",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.6",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-11.0",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-12.5",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-12.9",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.3",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.7",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-18.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-6.9",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-7.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-8.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.6",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-11.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-11.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-12.5",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-12.9",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-13.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.7",
                    "\\sym{strandgrade} = (7-Wire)Y1960S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1960S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-6.4",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-6.85",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-7.0",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-8.6",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-11.3",
                    "\\sym{strandgrade} = (7-Wire)Y2160S7-6.85",
                    "\\sym{strandgrade} = (7G-Wire)Y1700S7G-18.0",
                    "\\sym{strandgrade} = (7G-Wire)Y1820S7G-15.2",
                    "\\sym{strandgrade} = (7G-Wire)Y1860S7G-12.7",
                    "\\sym{strandgrade} = (7G-Wire)Y1860S7G-15.2"
                ]
            ],
            "data": [
                [
                    "5.60"
                ],
                [
                    "6.00"
                ],
                [
                    "4.50"
                ],
                [
                    "7.50"
                ],
                [
                    "4.85"
                ],
                [
                    "6.50"
                ],
                [
                    "6.90"
                ],
                [
                    "7.50"
                ],
                [
                    "8.60"
                ],
                [
                    "6.30"
                ],
                [
                    "6.50"
                ],
                [
                    "4.80"
                ],
                [
                    "5.20"
                ],
                [
                    "6.50"
                ],
                [
                    "6.85"
                ],
                [
                    "5.20"
                ],
                [
                    "5.20"
                ],
                [
                    "15.20"
                ],
                [
                    "6.90"
                ],
                [
                    "9.00"
                ],
                [
                    "9.30"
                ],
                [
                    "9.60"
                ],
                [
                    "11.00"
                ],
                [
                    "12.50"
                ],
                [
                    "12.90"
                ],
                [
                    "15.20"
                ],
                [
                    "15.30"
                ],
                [
                    "15.70"
                ],
                [
                    "18.00"
                ],
                [
                    "6.90"
                ],
                [
                    "7.00"
                ],
                [
                    "8.00"
                ],
                [
                    "9.00"
                ],
                [
                    "9.30"
                ],
                [
                    "9.60"
                ],
                [
                    "11.00"
                ],
                [
                    "11.30"
                ],
                [
                    "12.50"
                ],
                [
                    "12.90"
                ],
                [
                    "13.00"
                ],
                [
                    "15.20"
                ],
                [
                    "15.30"
                ],
                [
                    "15.70"
                ],
                [
                    "9.00"
                ],
                [
                    "9.30"
                ],
                [
                    "6.40"
                ],
                [
                    "6.85"
                ],
                [
                    "7.00"
                ],
                [
                    "8.60"
                ],
                [
                    "11.30"
                ],
                [
                    "6.85"
                ],
                [
                    "18.00"
                ],
                [
                    "15.20"
                ],
                [
                    "12.70"
                ],
                [
                    "15.20"
                ]
            ]
        }
    },
    {
        "id": "G20_COMP_16",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.3.1(5)"
        ],
        "title": "Cross-sectional area of strand",
        "description": "This column provides the cross-sectional area of the strand, which is essential for calculating the strand's load-bearing capacity. It reflects the total area of the strand's wire section. For more detailed information, refer to EN 10138-3 (Table 3).",
        "latexSymbol": "S_{n}",
        "latexEquation": "9.70",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 2,
        "required": [
            "G20_COMP_14"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{strandgrade} = (2-Wire)Y1770S2-5.6",
                    "\\sym{strandgrade} = (2-Wire)Y1770S2-6.0",
                    "\\sym{strandgrade} = (2-Wire)Y1860S2-4.5",
                    "\\sym{strandgrade} = (3-Wire)Y1770S3-7.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-4.85",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-6.9",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-7.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-8.6",
                    "\\sym{strandgrade} = (3-Wire)Y1920S3-6.3",
                    "\\sym{strandgrade} = (3-Wire)Y1920S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.8",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-5.2",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.85",
                    "\\sym{strandgrade} = (3-Wire)Y2060S3-5.2",
                    "\\sym{strandgrade} = (3-Wire)Y2160S3-5.2",
                    "\\sym{strandgrade} = (7-Wire)Y1670S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-6.9",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.6",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-11.0",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-12.5",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-12.9",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.3",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.7",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-18.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-6.9",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-7.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-8.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.6",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-11.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-11.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-12.5",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-12.9",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-13.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.7",
                    "\\sym{strandgrade} = (7-Wire)Y1960S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1960S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-6.4",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-6.85",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-7.0",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-8.6",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-11.3",
                    "\\sym{strandgrade} = (7-Wire)Y2160S7-6.85",
                    "\\sym{strandgrade} = (7G-Wire)Y1700S7G-18.0",
                    "\\sym{strandgrade} = (7G-Wire)Y1820S7G-15.2",
                    "\\sym{strandgrade} = (7G-Wire)Y1860S7G-12.7",
                    "\\sym{strandgrade} = (7G-Wire)Y1860S7G-15.2"
                ]
            ],
            "data": [
                [
                    "9.70"
                ],
                [
                    "15.10"
                ],
                [
                    "7.98"
                ],
                [
                    "29.00"
                ],
                [
                    "11.90"
                ],
                [
                    "21.20"
                ],
                [
                    "23.40"
                ],
                [
                    "29.00"
                ],
                [
                    "37.40"
                ],
                [
                    "19.80"
                ],
                [
                    "21.20"
                ],
                [
                    "12.00"
                ],
                [
                    "13.60"
                ],
                [
                    "21.20"
                ],
                [
                    "23.60"
                ],
                [
                    "13.60"
                ],
                [
                    "13.60"
                ],
                [
                    "139.00"
                ],
                [
                    "29.00"
                ],
                [
                    "50.00"
                ],
                [
                    "52.00"
                ],
                [
                    "55.00"
                ],
                [
                    "70.00"
                ],
                [
                    "93.00"
                ],
                [
                    "100.00"
                ],
                [
                    "139.00"
                ],
                [
                    "140.00"
                ],
                [
                    "150.00"
                ],
                [
                    "200.00"
                ],
                [
                    "29.00"
                ],
                [
                    "30.00"
                ],
                [
                    "38.00"
                ],
                [
                    "50.00"
                ],
                [
                    "52.00"
                ],
                [
                    "55.00"
                ],
                [
                    "70.00"
                ],
                [
                    "75.00"
                ],
                [
                    "93.00"
                ],
                [
                    "100.00"
                ],
                [
                    "102.00"
                ],
                [
                    "139.00"
                ],
                [
                    "140.00"
                ],
                [
                    "150.00"
                ],
                [
                    "50.00"
                ],
                [
                    "52.00"
                ],
                [
                    "25.00"
                ],
                [
                    "28.20"
                ],
                [
                    "30.00"
                ],
                [
                    "45.00"
                ],
                [
                    "75.00"
                ],
                [
                    "28.20"
                ],
                [
                    "223.00"
                ],
                [
                    "165.00"
                ],
                [
                    "112.00"
                ],
                [
                    "165.00"
                ]
            ]
        }
    },
    {
        "id": "G20_COMP_17",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.3.1(5)"
        ],
        "title": "Tensile strength of strand",
        "description": "This column shows the tensile strength of the strand, representing the maximum stress that the strand can withstand before breaking. It is a key indicator of the strand's performance under tension. For more detailed information, refer to EN 10138-3 (Table 3).",
        "latexSymbol": "R_{m}",
        "latexEquation": "1770",
        "type": "number",
        "unit": "MPa",
        "notation": "standard",
        "decimal": 0,
        "required": [
            "G20_COMP_14"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{strandgrade} = (2-Wire)Y1770S2-5.6",
                    "\\sym{strandgrade} = (2-Wire)Y1770S2-6.0",
                    "\\sym{strandgrade} = (2-Wire)Y1860S2-4.5",
                    "\\sym{strandgrade} = (3-Wire)Y1770S3-7.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-4.85",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-6.9",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-7.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-8.6",
                    "\\sym{strandgrade} = (3-Wire)Y1920S3-6.3",
                    "\\sym{strandgrade} = (3-Wire)Y1920S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.8",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-5.2",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.85",
                    "\\sym{strandgrade} = (3-Wire)Y2060S3-5.2",
                    "\\sym{strandgrade} = (3-Wire)Y2160S3-5.2",
                    "\\sym{strandgrade} = (7-Wire)Y1670S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-6.9",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.6",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-11.0",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-12.5",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-12.9",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.3",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.7",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-18.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-6.9",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-7.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-8.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.6",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-11.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-11.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-12.5",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-12.9",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-13.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.7",
                    "\\sym{strandgrade} = (7-Wire)Y1960S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1960S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-6.4",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-6.85",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-7.0",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-8.6",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-11.3",
                    "\\sym{strandgrade} = (7-Wire)Y2160S7-6.85",
                    "\\sym{strandgrade} = (7G-Wire)Y1700S7G-18.0",
                    "\\sym{strandgrade} = (7G-Wire)Y1820S7G-15.2",
                    "\\sym{strandgrade} = (7G-Wire)Y1860S7G-12.7",
                    "\\sym{strandgrade} = (7G-Wire)Y1860S7G-15.2"
                ]
            ],
            "data": [
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1860"
                ],
                [
                    "1770"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1920"
                ],
                [
                    "1920"
                ],
                [
                    "1960"
                ],
                [
                    "1960"
                ],
                [
                    "1960"
                ],
                [
                    "1960"
                ],
                [
                    "2060"
                ],
                [
                    "2160"
                ],
                [
                    "1670"
                ],
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1770"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ],
                [
                    "1960"
                ],
                [
                    "1960"
                ],
                [
                    "2060"
                ],
                [
                    "2060"
                ],
                [
                    "2060"
                ],
                [
                    "2060"
                ],
                [
                    "2060"
                ],
                [
                    "2160"
                ],
                [
                    "1700"
                ],
                [
                    "1820"
                ],
                [
                    "1860"
                ],
                [
                    "1860"
                ]
            ]
        }
    },
    {
        "id": "G20_COMP_18",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.3.1(5)"
        ],
        "title": "Characteristic value of maximum force",
        "description": "The characteristic maximum force represents the calculated value of the highest force that the strand can withstand based on its tensile strength and cross-sectional area. For more detailed information, refer to EN 10138-3 (Table 3 and Table4)",
        "latexSymbol": "F_{m}",
        "latexEquation": "17.17",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G20_COMP_14"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{strandgrade} = (2-Wire)Y1770S2-5.6",
                    "\\sym{strandgrade} = (2-Wire)Y1770S2-6.0",
                    "\\sym{strandgrade} = (2-Wire)Y1860S2-4.5",
                    "\\sym{strandgrade} = (3-Wire)Y1770S3-7.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-4.85",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-6.9",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-7.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-8.6",
                    "\\sym{strandgrade} = (3-Wire)Y1920S3-6.3",
                    "\\sym{strandgrade} = (3-Wire)Y1920S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.8",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-5.2",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.85",
                    "\\sym{strandgrade} = (3-Wire)Y2060S3-5.2",
                    "\\sym{strandgrade} = (3-Wire)Y2160S3-5.2",
                    "\\sym{strandgrade} = (7-Wire)Y1670S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-6.9",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.6",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-11.0",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-12.5",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-12.9",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.3",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.7",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-18.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-6.9",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-7.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-8.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.6",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-11.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-11.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-12.5",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-12.9",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-13.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.7",
                    "\\sym{strandgrade} = (7-Wire)Y1960S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1960S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-6.4",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-6.85",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-7.0",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-8.6",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-11.3",
                    "\\sym{strandgrade} = (7-Wire)Y2160S7-6.85",
                    "\\sym{strandgrade} = (7G-Wire)Y1700S7G-18.0",
                    "\\sym{strandgrade} = (7G-Wire)Y1820S7G-15.2",
                    "\\sym{strandgrade} = (7G-Wire)Y1860S7G-12.7",
                    "\\sym{strandgrade} = (7G-Wire)Y1860S7G-15.2"
                ]
            ],
            "data": [
                [
                    "17.17"
                ],
                [
                    "26.73"
                ],
                [
                    "14.84"
                ],
                [
                    "51.33"
                ],
                [
                    "22.13"
                ],
                [
                    "39.43"
                ],
                [
                    "43.52"
                ],
                [
                    "53.94"
                ],
                [
                    "69.56"
                ],
                [
                    "38.02"
                ],
                [
                    "40.70"
                ],
                [
                    "23.52"
                ],
                [
                    "26.66"
                ],
                [
                    "41.55"
                ],
                [
                    "46.26"
                ],
                [
                    "28.02"
                ],
                [
                    "29.38"
                ],
                [
                    "232.13"
                ],
                [
                    "51.33"
                ],
                [
                    "88.50"
                ],
                [
                    "92.04"
                ],
                [
                    "97.35"
                ],
                [
                    "123.90"
                ],
                [
                    "164.61"
                ],
                [
                    "177.00"
                ],
                [
                    "246.03"
                ],
                [
                    "247.80"
                ],
                [
                    "265.50"
                ],
                [
                    "354.00"
                ],
                [
                    "53.94"
                ],
                [
                    "55.80"
                ],
                [
                    "70.68"
                ],
                [
                    "93.00"
                ],
                [
                    "96.72"
                ],
                [
                    "102.30"
                ],
                [
                    "130.20"
                ],
                [
                    "139.50"
                ],
                [
                    "172.98"
                ],
                [
                    "186.00"
                ],
                [
                    "189.72"
                ],
                [
                    "258.54"
                ],
                [
                    "260.40"
                ],
                [
                    "279.00"
                ],
                [
                    "98.00"
                ],
                [
                    "101.92"
                ],
                [
                    "51.50"
                ],
                [
                    "58.09"
                ],
                [
                    "61.80"
                ],
                [
                    "92.70"
                ],
                [
                    "154.50"
                ],
                [
                    "60.91"
                ],
                [
                    "379.10"
                ],
                [
                    "300.30"
                ],
                [
                    "208.32"
                ],
                [
                    "306.90"
                ]
            ]
        }
    },
    {
        "id": "G20_COMP_19",
        "codeName": "EN1992-1-1",
        "reference": [
            "3.3.1(5)"
        ],
        "title": "Characteristic value of 0.1% proof force",
        "description": "The characteristic 0.1% proof force is a calculated value that represents the force at which the strand undergoes 0.1% permanent deformation. For more detailed information, refer to EN 10138-3 (Table 3 and Table4).",
        "latexSymbol": "F_{p0,1}",
        "latexEquation": "14.77",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G20_COMP_14"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{strandgrade} = (2-Wire)Y1770S2-5.6",
                    "\\sym{strandgrade} = (2-Wire)Y1770S2-6.0",
                    "\\sym{strandgrade} = (2-Wire)Y1860S2-4.5",
                    "\\sym{strandgrade} = (3-Wire)Y1770S3-7.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-4.85",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-6.9",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-7.5",
                    "\\sym{strandgrade} = (3-Wire)Y1860S3-8.6",
                    "\\sym{strandgrade} = (3-Wire)Y1920S3-6.3",
                    "\\sym{strandgrade} = (3-Wire)Y1920S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.8",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-5.2",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.5",
                    "\\sym{strandgrade} = (3-Wire)Y1960S3-6.85",
                    "\\sym{strandgrade} = (3-Wire)Y2060S3-5.2",
                    "\\sym{strandgrade} = (3-Wire)Y2160S3-5.2",
                    "\\sym{strandgrade} = (7-Wire)Y1670S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-6.9",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-9.6",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-11.0",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-12.5",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-12.9",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.3",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-15.7",
                    "\\sym{strandgrade} = (7-Wire)Y1770S7-18.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-6.9",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-7.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-8.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-9.6",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-11.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-11.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-12.5",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-12.9",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-13.0",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.2",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.3",
                    "\\sym{strandgrade} = (7-Wire)Y1860S7-15.7",
                    "\\sym{strandgrade} = (7-Wire)Y1960S7-9.0",
                    "\\sym{strandgrade} = (7-Wire)Y1960S7-9.3",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-6.4",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-6.85",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-7.0",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-8.6",
                    "\\sym{strandgrade} = (7-Wire)Y2060S7-11.3",
                    "\\sym{strandgrade} = (7-Wire)Y2160S7-6.85",
                    "\\sym{strandgrade} = (7G-Wire)Y1700S7G-18.0",
                    "\\sym{strandgrade} = (7G-Wire)Y1820S7G-15.2",
                    "\\sym{strandgrade} = (7G-Wire)Y1860S7G-12.7",
                    "\\sym{strandgrade} = (7G-Wire)Y1860S7G-15.2"
                ]
            ],
            "data": [
                [
                    "14.77"
                ],
                [
                    "22.99"
                ],
                [
                    "12.76"
                ],
                [
                    "44.14"
                ],
                [
                    "19.04"
                ],
                [
                    "33.91"
                ],
                [
                    "37.43"
                ],
                [
                    "46.39"
                ],
                [
                    "59.83"
                ],
                [
                    "32.69"
                ],
                [
                    "35.01"
                ],
                [
                    "20.93"
                ],
                [
                    "23.72"
                ],
                [
                    "36.98"
                ],
                [
                    "41.17"
                ],
                [
                    "24.93"
                ],
                [
                    "26.14"
                ],
                [
                    "199.63"
                ],
                [
                    "44.14"
                ],
                [
                    "76.11"
                ],
                [
                    "79.15"
                ],
                [
                    "83.72"
                ],
                [
                    "106.55"
                ],
                [
                    "141.56"
                ],
                [
                    "152.22"
                ],
                [
                    "211.59"
                ],
                [
                    "213.11"
                ],
                [
                    "228.33"
                ],
                [
                    "304.44"
                ],
                [
                    "46.39"
                ],
                [
                    "47.99"
                ],
                [
                    "60.78"
                ],
                [
                    "79.98"
                ],
                [
                    "83.18"
                ],
                [
                    "87.98"
                ],
                [
                    "111.97"
                ],
                [
                    "119.97"
                ],
                [
                    "148.76"
                ],
                [
                    "159.96"
                ],
                [
                    "163.16"
                ],
                [
                    "222.34"
                ],
                [
                    "223.94"
                ],
                [
                    "239.94"
                ],
                [
                    "86.24"
                ],
                [
                    "89.69"
                ],
                [
                    "45.32"
                ],
                [
                    "51.12"
                ],
                [
                    "54.38"
                ],
                [
                    "81.58"
                ],
                [
                    "135.96"
                ],
                [
                    "53.60"
                ],
                [
                    "326.03"
                ],
                [
                    "258.26"
                ],
                [
                    "179.16"
                ],
                [
                    "263.93"
                ]
            ]
        }
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/88180775/EN1992-1-1+Maximum+and+Initial+Prestressing+Force
        'id': '20',
        'standardType': 'EUROCODE',
        'codeName': 'EN1992-1-1',
        'codeTitle': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Maximum Prestressing Force and Initial Prestress Force',
        'description': r"[EN1992-1-1] This guide provides a step-by-step approach to calculating the maximum prestressing force and the initial prestress force in prestressed concrete structures. The maximum prestressing force is determined by considering the allowable stress limits based on the ultimate tensile strength and the 0.1% proof strength of the prestressing steel, applying the appropriate coefficients. The initial prestress force is then calculated by subtracting the immediate losses from the maximum prestressing force, ensuring that the force applied to the concrete does not exceed the specified limits at the initial stage of prestressing.",
        'edition': '2004',
        "figureFile": "detail_content_20.png",
        'targetComponents': ['G20_COMP_1', 'G20_COMP_8', 'G20_COMP_13', 'G20_COMP_15', 'G20_COMP_18'],
        'testInput': [
            {'component': 'G20_COMP_12', 'value': 'Based on EN 10138-3 (7.81kg/dm^{3})'}, # standmass = Based on EN 10138-3 (7.81kg/dm^{3})
            # {'component': 'G20_COMP_12', 'value': 'Based on EN 1992-1-1 3.3.6 (7,850kg/m^{3})'}, # standmass = Based on EN 1992-1-1 3.3.6 (7,850kg/m^{3})
            {'component': 'G20_COMP_14', 'value': '(2-Wire)Y1770S2-5.6'}, # strandgrade = (2-Wire)Y1770S2-5.6
            # {'component': 'G20_COMP_14', 'value': '(7-Wire)Y1860S7-12.5'}, # strandgrade = (7-Wire)Y1860S7-12.5
        ],
    },]