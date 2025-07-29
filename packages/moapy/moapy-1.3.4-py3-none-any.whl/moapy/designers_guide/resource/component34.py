component_list = [
    {
        "id": "G34_COMP_1",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(5)P"
        ],
        "title": "Section type selection for confining reinforcement",
        "description": "In rectangular sections, the transverse reinforcement ratio is defined based on the area of hoops or ties. In circular sections, the volumetric ratio of the spiral reinforcement relative to the concrete core is used. Users must select the section type to apply the appropriate formula for calculating the reinforcement ratio.",
        "latexSymbol": "sectype",
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
                    "In rectangular sections"
                ],
                [
                    "In circular sections"
                ]
            ]
        }
    },
    {
        "id": "G34_COMP_2",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(5)P"
        ],
        "title": "Diameter of spiral or hoop bar",
        "description": "The diameter of the spiral or hoop reinforcement used in circular sections is an important parameter in determining the volumetric reinforcement ratio and the confinement effectiveness in the structural element.",
        "latexSymbol": "d_{bT}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 16.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G34_COMP_3",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(5)P"
        ],
        "title": "Longitudinal spacing of hoops or ties",
        "description": "The longitudinal spacing refers to the center-to-center distance between hoops or ties in the longitudinal direction of the structure. In rectangular sections, it must not exceed 6 times the diameter of the longitudinal bar or 1/5 of the smallest dimension of the confined concrete core to the hoop center line. In circular sections, it must not exceed 6 times the diameter of the longitudinal bar or 1/5 of the diameter of the confined concrete core to the hoop center line.",
        "latexSymbol": "s_{L}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "default": 100.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G34_COMP_4",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(5)P"
        ],
        "title": "Leg of spiral or ties in the one direction",
        "description": "A leg refers to the number of hoops or ties arranged in one direction within a rectangular section, representing how many are present to provide reinforcement in that specific direction.",
        "latexSymbol": "leg",
        "type": "number",
        "unit": "ea",
        "notation": "standard",
        "decimal": 0,
        "default": 4.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G34_COMP_5",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(5)P"
        ],
        "title": "Total area of transverse reinforcement",
        "description": "The total area of transverse reinforcement is calculated based on the section type. In rectangular sections, it includes the area of hoops or ties and the number of legs contributing to confinement. In circular sections, it refers to the cross-sectional area of a single spiral or hoop bar, with each calculation specific to the respective section type.",
        "latexSymbol": "A_{sw,p}",
        "latexEquation": "\\frac{(\\pi \\times \\sym{d_{bT}}^{2})}{4} \\times \\sym{leg}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G34_COMP_1",
            "G34_COMP_2",
            "G34_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{sectype} = In rectangular sections",
                    "\\sym{sectype} = In circular sections"
                ]
            ],
            "data": [
                [
                    "\\frac{(\\pi \\times \\sym{d_{bT}}^{2})}{4} \\times \\sym{leg}"
                ],
                [
                    "\\frac{(\\pi \\times \\sym{d_{bT}}^{2})}{4}"
                ]
            ]
        }
    },
    {
        "id": "G34_COMP_6",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(Figure6.1b)"
        ],
        "title": "Diameter of Spiral or Hoop in Circular Piers",
        "description": "The diameter of the spiral or hoop refers to the overall diameter of the reinforcement placed in circular piers. This parameter is essential for calculating the volumetric reinforcement ratio and ensuring effective confinement within the pier.",
        "latexSymbol": "D_{sp}",
        "latexEquation": "\\sym{D} - 2 \\times (\\sym{c} + \\frac{\\sym{d_{bT}}}{2})",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_9",
            "G34_COMP_12",
            "G34_COMP_2"
        ]
    },
    {
        "id": "G34_COMP_7",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.2(3)P"
        ],
        "title": "Diameter of longitudinal bar",
        "description": "The diameter of the longitudinal bar refers to the thickness of the reinforcement bars placed along the length of the structural element, which plays a key role in determining the spacing and amount of reinforcement needed.",
        "latexSymbol": "d_{bL}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 32.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G34_COMP_8",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(2)P"
        ],
        "title": "Number of longitudinal bars",
        "description": "The number of longitudinal bars refers to how many reinforcement bars are placed along the length of the structural element, which, along with the bar diameter, is necessary for calculating the longitudinal reinforcement ratio.",
        "latexSymbol": "n_{d,bL}",
        "type": "number",
        "unit": "ea",
        "notation": "standard",
        "decimal": 0,
        "default": 24.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G34_COMP_9",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(2)P"
        ],
        "title": "Diameter for circular sections",
        "description": "The diameter for circular sections refers to the total width across the circular section, measured from one edge to the opposite edge, passing through the center.",
        "latexSymbol": "D",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 1200.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G34_COMP_10",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(2)P"
        ],
        "title": "Width for rectangular sections",
        "description": "The width for rectangular sections is the horizontal distance across the rectangular cross-section, measured perpendicular to the height.",
        "latexSymbol": "b",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 800.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G34_COMP_11",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(2)P"
        ],
        "title": "Height for rectangular sections",
        "description": "The height for rectangular sections refers to the vertical distance of the rectangular cross-section, measured perpendicular to the width.",
        "latexSymbol": "h",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 1000.0,
        "limits": {
            "exMin": 0
        },
        "useStd": False
    },
    {
        "id": "G34_COMP_12",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(2)P"
        ],
        "title": "Concrete cover(distance to outermost reinforcement surface)",
        "description": "Concrete cover is the distance between the surface of the reinforcement closest to the nearest concrete surface, including links, stirrups, and surface reinforcement where applicable.",
        "latexSymbol": "c",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 1,
        "default": 50.0,
        "limits": {
            "inMin": 0
        },
        "useStd": False
    },
    {
        "id": "G34_COMP_13",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(5)P"
        ],
        "title": "Dimension of concrete core in rectangular sections",
        "description": "In rectangular sections, the dimension of the concrete core refers to the distance perpendicular to the direction of confinement, measured from the inside of the section to the outer edge of the perimeter hoop.",
        "latexSymbol": "b_{c}",
        "latexEquation": "\\sym{b} - 2 \\times \\sym{c}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_10",
            "G34_COMP_12"
        ]
    },
    {
        "id": "G34_COMP_14",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(2)P"
        ],
        "title": "Area of the gross concrete section",
        "description": "The area of the gross concrete section refers to the total cross-sectional area of the concrete, including both the core and the surrounding unconfined concrete.",
        "latexSymbol": "A_{c}",
        "latexEquation": "\\sym{b} \\times \\sym{h}",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G34_COMP_1",
            "G34_COMP_10",
            "G34_COMP_11",
            "G34_COMP_9"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{sectype} = In rectangular sections",
                    "\\sym{sectype} = In circular sections"
                ]
            ],
            "data": [
                [
                    "\\sym{b} \\times \\sym{h}"
                ],
                [
                    "\\frac{(\\pi \\times \\sym{D}^{2})}{4}"
                ]
            ]
        }
    },
    {
        "id": "G34_COMP_15",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(2)P"
        ],
        "title": "Confined concrete area of the section",
        "description": "The confined concrete core area refers to the area of the concrete core within a structural section, measured up to the centerline of the hoop reinforcement. This area represents the confined portion of the concrete that is effectively enclosed by the hoop reinforcement.",
        "latexSymbol": "A_{cc}",
        "latexEquation": "(\\sym{b} - 2 \\times (\\sym{c} + \\frac{\\sym{d_{bT}}}{2})) \\times (\\sym{h} - 2 \\times (\\sym{c} + \\frac{\\sym{d_{bT}}}{2}))",
        "type": "number",
        "unit": "mm^2",
        "notation": "standard",
        "decimal": 1,
        "required": [
            "G34_COMP_1",
            "G34_COMP_10",
            "G34_COMP_11",
            "G34_COMP_9",
            "G34_COMP_12",
            "G34_COMP_2"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{sectype} = In rectangular sections",
                    "\\sym{sectype} = In circular sections"
                ]
            ],
            "data": [
                [
                    "(\\sym{b} - 2 \\times (\\sym{c} + \\frac{\\sym{d_{bT}}}{2})) \\times (\\sym{h} - 2 \\times (\\sym{c} + \\frac{\\sym{d_{bT}}}{2}))"
                ],
                [
                    "\\frac{(\\pi * (\\sym{D} - 2 * (c + \\frac{\\sym{d_{bT}}}{2}))^{2})}{4}"
                ]
            ]
        }
    },
    {
        "id": "G34_COMP_16",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(6.3)"
        ],
        "title": "Mechanical reinforcement ratio for confining reinforcement",
        "description": "The mechanical reinforcement ratio defines the required amount of confining reinforcement relative to the strength of the concrete, ensuring adequate confinement and ductility in critical structural areas.",
        "latexSymbol": "\\omega_{wd}",
        "latexEquation": "\\sym{\\rho_{w}} \\times \\frac{\\sym{f_{yd}}}{\\sym{f_{cd}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_17",
            "G18_COMP_3",
            "G14_COMP_15"
        ]
    },
    {
        "id": "G34_COMP_17",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(5)P"
        ],
        "title": "Confining reinforcement ratio for different section types",
        "description": "In rectangular sections, the reinforcement ratio for confinement is the transverse reinforcement ratio, which is based on the area of hoops or ties. In circular sections, the reinforcement ratio for confinement is the volumetric ratio of the spiral reinforcement relative to the concrete core. This distinction ensures the correct application of confinement reinforcement for different structural types.",
        "latexSymbol": "\\rho_{w}",
        "latexEquation": "\\frac{\\sym{A_{sw,p}}}{(\\sym{s_{L}} \\times \\sym{b_{c}})}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_1",
            "G34_COMP_5",
            "G34_COMP_3",
            "G34_COMP_13",
            "G34_COMP_6"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{sectype} = In rectangular sections",
                    "\\sym{sectype} = In circular sections"
                ]
            ],
            "data": [
                [
                    "\\frac{\\sym{A_{sw,p}}}{(\\sym{s_{L}} \\times \\sym{b_{c}})}"
                ],
                [
                    "\\frac{(4 \\times \\sym{A_{sw,p}})}{(\\sym{D_{sp}} \\times \\sym{s_{L}})}"
                ]
            ]
        }
    },
    {
        "id": "G34_COMP_18",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(2)P"
        ],
        "title": "Maximum confining reinforcement requirement",
        "description": "The maximum confining reinforcement requirement is determined by comparing the required confining reinforcement and two-thirds of the minimum reinforcement, and applying the greater value to ensure sufficient confinement in critical structural areas.",
        "latexSymbol": "\\omega_{wd,r,c}",
        "latexEquation": "\\max(\\sym{\\omega_{w,req}}, \\frac{2}{3} \\times \\sym{\\omega_{w,min}})",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_1",
            "G34_COMP_19",
            "G34_COMP_22"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{sectype} = In rectangular sections",
                    "\\sym{sectype} = In circular sections"
                ]
            ],
            "data": [
                [
                    "\\max(\\sym{\\omega_{w,req}} , \\frac{2}{3} \\times \\sym{\\omega_{w,min}})"
                ],
                [
                    "\\max(1.4 \\times \\sym{\\omega_{w,req}} , \\sym{\\omega_{w,min}})"
                ]
            ]
        }
    },
    {
        "id": "G34_COMP_19",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(6.7)"
        ],
        "title": "Required confining reinforcement",
        "description": "The required reinforcement ratio represents the minimum amount of confining reinforcement needed for structural sections, calculated based on the area of the gross concrete section, the confined core area, and other factors to ensure adequate confinement.",
        "latexSymbol": "\\omega_{w,req}",
        "latexEquation": "\\frac{\\sym{A_{c}}}{\\sym{A_{cc}}} \\times \\sym{\\lambda} \\times \\sym{\\eta_{k}} + 0.13 \\times \\frac{\\sym{f_{yd}}}{f_{cd}} \\times (\\sym{\\rho_{L}} - 0.01)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_14",
            "G34_COMP_15",
            "G34_COMP_21",
            "G34_COMP_23",
            "G18_COMP_3",
            "G14_COMP_15",
            "G34_COMP_20"
        ]
    },
    {
        "id": "G34_COMP_20",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(2)P"
        ],
        "title": "Longitudinal reinforcement ratio",
        "description": "The longitudinal reinforcement ratio refers to the ratio of the total area of the longitudinal reinforcement to the gross area of the concrete section, indicating how much reinforcement is provided along the length of the structural element.",
        "latexSymbol": "\\rho_{L}",
        "latexEquation": "\\frac{\\frac{(\\pi \\times \\sym{d_{bL}}^{2})}{4} \\times \\sym{n_{d,bL}}}{\\sym{A_{c}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_7",
            "G34_COMP_8",
            "G34_COMP_14"
        ]
    },
    {
        "id": "G34_COMP_21",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(Table6.1)"
        ],
        "title": "Confinement effectiveness factor for seismic behaviour",
        "description": "The confinement effectiveness factor varies based on the seismic behaviour of the structure. For ductile structures, the factor is set at 0.37, and for limited ductile structures, it is 0.28. This factor accounts for how effectively the transverse reinforcement confines the concrete core.",
        "latexSymbol": "\\lambda",
        "latexEquation": "0.37",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G33_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{ducbehav} = Ductile",
                    "\\sym{ducbehav} = Limited Ductile"
                ]
            ],
            "data": [
                [
                    "0.37"
                ],
                [
                    "0.28"
                ]
            ]
        }
    },
    {
        "id": "G34_COMP_22",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.4(Table6.1)"
        ],
        "title": "Minimum confining reinforcement ratio for seismic behaviour",
        "description": "The minimum confining reinforcement ratio varies based on the seismic behaviour of the structure. For ductile structures, the ratio is 0.18, and for limited ductile structures, it is 0.12. This ratio ensures that the structure has at least the minimum required reinforcement for confinement.",
        "latexSymbol": "\\omega_{w,min}",
        "latexEquation": "0.18",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G33_COMP_1"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{ducbehav} = Ductile",
                    "\\sym{ducbehav} = Limited Ductile"
                ]
            ],
            "data": [
                [
                    "0.18"
                ],
                [
                    "0.12"
                ]
            ]
        }
    },
    {
        "id": "G34_COMP_23",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(6.1)"
        ],
        "title": "Normalised axial force limit in potential plastic hinge regions",
        "description": "The normalised axial force limit represents the threshold beyond which additional confinement is required in the potential plastic hinge regions of piers. It is a measure used to ensure that the pier behaves ductilely when the normalised axial force exceeds a specified limit.",
        "latexSymbol": "\\eta_{k}",
        "latexEquation": "\\max(\\frac{(\\sym{N_{Ed}} \\times 1000)}{(\\sym{A_{c}} \\times \\sym{f_{ck}})} , 0.08)",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_24",
            "G34_COMP_14",
            "G14_COMP_5"
        ]
    },
    {
        "id": "G34_COMP_24",
        "codeName": "EN1998-2",
        "reference": [
            "5.3(4)"
        ],
        "title": "Axial force in seismic design situation",
        "description": "The axial force in the seismic design situation refers to the force acting on a pier during a seismic event at the plastic hinge. It is considered positive when the force is compressive.",
        "latexSymbol": "N_{Ed}",
        "type": "number",
        "unit": "kN",
        "notation": "standard",
        "decimal": 3,
        "default": 7600.0,
        "useStd": False
    },
    {
        "id": "G34_COMP_25",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(6.3)"
        ],
        "title": "Required confining reinforcement ratio",
        "description": "The required confining reinforcement ratio refers to the amount of transverse reinforcement, such as spirals, hoops, or ties, needed to provide adequate confinement in both rectangular and circular sections. This ratio is determined based on the maximum confining reinforcement requirement.",
        "latexSymbol": "\\rho_{w,r}",
        "latexEquation": "\\sym{\\omega_{wd,r,c}} \\times \\frac{\\sym{f_{cd}}}{\\sym{f_{yd}}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_18",
            "G14_COMP_15",
            "G18_COMP_3"
        ]
    },
    {
        "id": "G34_COMP_26",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(5)P"
        ],
        "title": "Required confining reinforcement area per spcaing",
        "description": "The required confining reinforcement area per spacing refers to the amount of transverse reinforcement, such as spiral or hoop bars, provided for each spacing between reinforcement elements. This ensures adequate confinement by calculating the reinforcement based on the spacing between the bars.",
        "latexSymbol": "A_{sw,p,r}",
        "latexEquation": "\\sym{\\rho_{w,r}} \\times \\sym{b_{c}}",
        "type": "number",
        "unit": "mm^2/mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_1",
            "G34_COMP_25",
            "G34_COMP_13",
            "G34_COMP_6"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{sectype} = In rectangular sections",
                    "\\sym{sectype} = In circular sections"
                ]
            ],
            "data": [
                [
                    "\\sym{\\rho_{w,r}} \\times \\sym{b_{c}}"
                ],
                [
                    "\\sym{\\rho_{w,r}} \\times \\frac{\\sym{D_{sp}}}{4}"
                ]
            ]
        }
    },
    {
        "id": "G34_COMP_27",
        "codeName": "EN1998-2",
        "reference": [
            "6.2.1.1(5)P"
        ],
        "title": "Required longitudinal spacing of hoops or ties",
        "description": "The required longitudinal spacing of hoops or ties refers to the center-to-center distance between these reinforcements along the length of the structure. It is determined based on the required confining reinforcement area per spacing and the diameter of the confinement reinforcement.",
        "latexSymbol": "s_{L,r}",
        "latexEquation": "\\frac{\\frac{\\pi \\times \\sym{d_{bT}}^{2}}{4}}{\\sym{A_{sw,p,r}}}",
        "type": "number",
        "unit": "mm",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G34_COMP_26",
            "G34_COMP_2"
        ]
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/111707237/EN1998-2+Confinement+Reinforcement
        'id': '34',
        'standardType': 'EUROCODE',
        'codeName': 'EN1998-2',
        'codeTitle': 'Eurocode 8 — Design of structures for earthquake resistance — Part 2: Bridges',
        'title': 'Confinement Design for Concrete Piers and Pile Foundations',
        'description': r"[EN1998-2] This guide provides step-by-step instructions for accurately designing confinement in concrete piers and pile foundations. It covers essential calculations for determining the reinforcement ratio for different section types, such as rectangular and circular sections, and helps you calculate the confining reinforcement requirement to ensure structural integrity under seismic conditions. Whether you're working on piers, columns, or any critical structural element, this guide will help you achieve the right balance of strength and ductility.",
        'edition': '2005+A2:2011 Incorporating corrigenda February 2010 and February 2012',
        'figureFile': 'detail_content_34.png',
        'targetComponents': ['G34_COMP_16', 'G34_COMP_18', 'G34_COMP_25', 'G34_COMP_26'],
        # 'targetComponents': ['G34_COMP_16', 'G34_COMP_18', 'G34_COMP_25', 'G34_COMP_26', 'G34_COMP_27'], # NOTE : G34_COMP_27 수식 오류로 인해 제외
        'testInput': [
            {'component': 'G14_COMP_3', 'value': 'Persistent'},
            {'component': 'G14_COMP_4', 'value': 'C12/15'},
            {'component': 'G18_COMP_1', 'value': 500},
            {'component': 'G33_COMP_1', 'value': 'Limited Ductile'},
            {'component': 'G34_COMP_1', 'value': 'In rectangular sections'},
            {'component': 'G34_COMP_2', 'value': 16},
            {'component': 'G34_COMP_3', 'value': 100},
            {'component': 'G34_COMP_4', 'value': 4},
            {'component': 'G34_COMP_7', 'value': 32},
            {'component': 'G34_COMP_8', 'value': 24},
            {'component': 'G34_COMP_9', 'value': 1200},
            {'component': 'G34_COMP_10', 'value': 800},
            {'component': 'G34_COMP_11', 'value': 1000},
            {'component': 'G34_COMP_12', 'value': 50},
            {'component': 'G34_COMP_24', 'value': 7600},
        ],
    }
]
