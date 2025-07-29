component_list = [
    {
        "id": "G33_COMP_1",
        "codeName": "EN1998-2",
        "reference": [
            "4.1.6(Table4.1)"
        ],
        "title": "Ductility behavior selection",
        "description": "This selection allows the user to choose between ductile structures, which dissipate significant seismic energy through plastic deformations, and limited ductile structures, which have reduced energy dissipation capabilities during seismic events.",
        "latexSymbol": "ducbehav",
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
                    "Limited Ductile",
                    "The seismic behavior of bridges with limited energy dissipation, where plastic hinges do not form significantly under design seismic action."
                ],
                [
                    "Ductile",
                    "structure designed to dissipate significant amounts of seismic energy through plastic hinges or other mechanisms during strong seismic motions."
                ]
            ]
        }
    },
    {
        "id": "G33_COMP_2",
        "codeName": "EN1998-2",
        "reference": [
            "4.1.6(Table4.1)"
        ],
        "title": "Ductile member types for seismic design",
        "description": "This menu allows the user to select the type of ductile members involved in seismic design. Options include different structural elements such as reinforced concrete piers, steel piers, abutments, and bridges, categorized by their ductility behavior. Each option reflects specific structural characteristics, like higher mode effects, plastic hinge reliability, and bracing types. The menu also includes options for seismic analysis in the vertical direction.",
        "latexSymbol": "ductmemb",
        "type": "string",
        "unit": "",
        "notation": "text",
        "default": "Reinforced concrete piers with inclined struts in bending",
        "table": "dropdown",
        "tableDetail": {
            "data": [
                [
                    "label"
                ],
                [
                    "Bridges dominated by higher mode effects (e.g. cable-stayed bridges)"
                ],
                [
                    "Bridges with unreliable plastic hinge detailing (e.g. due to high axial force or low shear-span ratio)"
                ],
                [
                    "Reinforced concrete vertical piers in bending"
                ],
                [
                    "Reinforced concrete piers with inclined struts in bending"
                ],
                [
                    "Steel vertical piers in bending"
                ],
                [
                    "Steel piers with inclined struts in bending"
                ],
                [
                    "Steel piers with normal bracing"
                ],
                [
                    "Steel piers with eccentric bracing"
                ],
                [
                    "Abutments rigidly connected to the deck in general"
                ],
                [
                    "Abutments rigidly connected to the deck in cases of locked-in structures"
                ],
                [
                    "Arches"
                ],
                [
                    "Seismic analysis in the vertical direction"
                ]
            ]
        }
    },
    {
        "id": "G33_COMP_3",
        "codeName": "EN1998-2",
        "reference": [
            "4.1.6(Table4.1)"
        ],
        "title": "Behaviour factor for linear analysis",
        "description": "The behaviour factor is a coefficient used in seismic design to reduce the elastic response spectrum. It reflects the capacity of a structure to dissipate energy through inelastic deformations during seismic events. The value of this factor depends on the ductility and design characteristics of the structure.",
        "latexSymbol": "q",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G33_COMP_2",
            "G33_COMP_1",
            "G33_COMP_4"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{ductmemb} = Bridges dominated by higher mode effects (e.g. cable-stayed bridges)",
                    "\\sym{ductmemb} = Bridges with unreliable plastic hinge detailing (e.g. due to high axial force or low shear-span ratio)",
                    "\\sym{ductmemb} = Reinforced concrete vertical piers in bending",
                    "\\sym{ductmemb} = Reinforced concrete piers with inclined struts in bending",
                    "\\sym{ductmemb} = Steel vertical piers in bending",
                    "\\sym{ductmemb} = Steel piers with inclined struts in bending",
                    "\\sym{ductmemb} = Steel piers with normal bracing",
                    "\\sym{ductmemb} = Steel piers with eccentric bracing",
                    "\\sym{ductmemb} = Abutments rigidly connected to the deck in general",
                    "\\sym{ductmemb} = Abutments rigidly connected to the deck in cases of locked-in structures",
                    "\\sym{ductmemb} = Arches",
                    "\\sym{ductmemb} = Seismic analysis in the vertical direction"
                ],
                [
                    "\\sym{ducbehav} = Limited Ductile",
                    "\\sym{ducbehav} = Ductile"
                ]
            ],
            "data": [
                [
                    "\\mathit{NA}",
                    "1.0"
                ],
                [
                    "\\mathit{NA}",
                    "1.0"
                ],
                [
                    "1.5",
                    "3.5 \\times \\sym{\\lambda(\\alpha_{s})}"
                ],
                [
                    "1.2",
                    "2.1 \\times \\sym{\\lambda(\\alpha_{s})}"
                ],
                [
                    "1.5",
                    "3.5"
                ],
                [
                    "1.2",
                    "2.0"
                ],
                [
                    "1.5",
                    "2.5"
                ],
                [
                    "\\mathit{NA}",
                    "3.5"
                ],
                [
                    "1.5",
                    "1.5"
                ],
                [
                    "1.0",
                    "1.0"
                ],
                [
                    "1.2",
                    "2.0"
                ],
                [
                    "1.0",
                    "1.0"
                ]
            ]
        }
    },
    {
        "id": "G33_COMP_4",
        "codeName": "EN1998-2",
        "reference": [
            "4.1.6(Table4.1)"
        ],
        "title": "Shear span ratio adjustment factor",
        "description": "This factor adjusts the behavior of a reinforced concrete pier based on its shear span ratio. It reflects how the ratio between the distance from the plastic hinge to the point of zero moment and the cross-section's depth in the direction of flexure influences the pier's ductility and bending resistance.",
        "latexSymbol": "\\lambda(\\alpha_{s})",
        "latexEquation": "1",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G33_COMP_5"
        ],
        "table": "formula",
        "tableDetail": {
            "criteria": [
                [
                    "\\sym{\\alpha_{s}} >= 3",
                    "1.0 <= \\sym{\\alpha_{s}} < 3"
                ]
            ],
            "data": [
                [
                    "1"
                ],
                [
                    "\\sqrt{\\frac{\\sym{\\alpha_{s}}}{3}}"
                ]
            ]
        }
    },
    {
        "id": "G33_COMP_5",
        "codeName": "EN1998-2",
        "reference": [
            "4.1.6(Table4.1)"
        ],
        "title": "Shear span ratio of the pier",
        "description": "The shear span ratio is the relationship between the distance from the plastic hinge to the point of zero moment and the depth of the cross-section in the direction of bending. It indicates how a pier's geometry affects its shear and bending performance, influencing the ductility and strength characteristics.",
        "latexSymbol": "\\alpha_{s}",
        "latexEquation": "\\frac{\\sym{L_{s}}}{\\sym{h}}",
        "type": "number",
        "unit": "",
        "notation": "standard",
        "decimal": 3,
        "required": [
            "G33_COMP_6",
            "G33_COMP_7"
        ]
    },
    {
        "id": "G33_COMP_6",
        "codeName": "EN1998-2",
        "reference": [
            "4.1.6(Table4.1)"
        ],
        "title": "Distance from the plastic hinge to the point of zero moment",
        "description": "The distance from the plastic hinge to the point where the bending moment becomes zero in a structural member is used in the calculation of the shear span ratio. It helps assess the member’s bending and shear behavior under load. This measurement is crucial for evaluating how bending and shear forces interact in the structural element.",
        "latexSymbol": "L_{s}",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "default": 3.0,
        "limits": {
            "inMin": 0
        }
    },
    {
        "id": "G33_COMP_7",
        "codeName": "EN1998-2",
        "reference": [
            "4.1.6(Table4.1)"
        ],
        "title": "Depth of the cross-section in the direction of flexure of the plastic hinge",
        "description": "The depth of the cross-section in the direction of flexure of the plastic hinge refers to the vertical distance measured within the structural member's cross-section along the axis where bending occurs. This measurement is crucial in determining how the member behaves under bending forces and is a key parameter when calculating the shear span ratio, influencing both the strength and ductility of the member.",
        "latexSymbol": "h",
        "type": "number",
        "unit": "m",
        "notation": "standard",
        "decimal": 3,
        "default": 1.5,
        "limits": {
            "exMin": 0
        }
    }
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/110594007/EN1998-2+Behaviour+Factor+for+Bridges
        'id': '33',
        'standardType': 'EUROCODE',
        'codeName': 'EN1998-2',
        'codeTitle': 'Eurocode 8 — Design of structures for earthquake resistance — Part 2: Bridges',
        'title': 'Behaviour Factor Calculation for Bridges',
        'description': r"[EN1998-2] This guide outlines the process of calculating the seismic behaviour factor (q) for bridges, categorized by the type of ductile members in the structure. It focuses on how different bridge components, such as reinforced concrete and steel piers, and struts, influence the behaviour factor through their ability to dissipate energy during seismic events. Important variables, such as shear span ratio, plastic hinge behaviour, and the depth of cross-sections, are explained to help ensure that the correct q values are applied for accurate and safe seismic bridge design.",
        'edition': '2005+A2:2011 Incorporating corrigenda February 2010 and February 2012',
        'figureFile': 'detail_content_33.png',
        'targetComponents': ['G33_COMP_3'],
        'testInput': [
            {'component': 'G33_COMP_1', 'value': 'Limited Ductile'},
            # {'component': 'G33_COMP_1', 'value': 'Ductile'},
            {'component': 'G33_COMP_2', 'value': 'Bridges dominated by higher mode effects (e.g. cable-stayed bridges)'},
            # {'component': 'G33_COMP_2', 'value': 'Reinforced concrete piers with inclined struts in bending'},
            {'component': 'G33_COMP_6', 'value': 3.0},
            {'component': 'G33_COMP_7', 'value': 1.5},
        ],
    }
]
