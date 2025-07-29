# NOTE: 기획 요청에 의해 component 및 content 임시 등록
component_list = [
    {
        "id": "G0_COMP_1",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Wave Height",
        "description": "The vertical distance between the wave crest and trough",
        "latexSymbol": "H",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "decimal": 3,
        "limits": {},
        "default": "15",
        "const": False,
        "unit": "m",
        "required": []
    },
    {
        "id": "G0_COMP_2",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Wave Period",
        "description": "Time taken for two successive wave crests to pass a fixed point",
        "latexSymbol": "T",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "decimal": 3,
        "limits": {},
        "default": "12.16",
        "const": False,
        "required": []
    },
    {
        "id": "G0_COMP_3",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Water Depth",
        "description": "The vertical distance from the seabed to the water surface",
        "latexSymbol": "h",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "decimal": 3,
        "limits": {},
        "default": "50",
        "const": False,
        "required": []
    },
    {
        "id": "G0_COMP_4",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Pile Diameter",
        "description": "The diameter of the pile structure interacting with the wave forces",
        "latexSymbol": "D",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "unit": "m",
        "decimal": 3,
        "limits": {},
        "default": "1",
        "const": False,
        "required": []
    },
    {
        "id": "G0_COMP_5",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Drag Coefficient",
        "description": "A dimensionless number representing the drag resistance exerted by the fluid on the structure",
        "latexSymbol": "C_d",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "decimal": 3,
        "limits": {},
        "default": "1",
        "const": False,
        "required": []
    },
    {
        "id": "G0_COMP_6",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Inertia Coefficient",
        "description": "A dimensionless number quantifying the inertia forces acting on the structure due to fluid acceleration",
        "latexSymbol": "C_m",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "decimal": 3,
        "limits": {},
        "default": "2",
        "const": False,
        "required": []
    },
    {
        "id": "G0_COMP_7",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Calculation Depth",
        "description": "The depth at which to calculate wave forces (measured from water surface, negative downward)",
        "latexSymbol": "z",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "unit": "m",
        "decimal": 3,
        "limits": {},
        "default": "7.5",
        "const": False,
        "required": []
    },
    {
        "id": "G0_COMP_8",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Time for Force Calculation",
        "description": "The time at which to calculate wave forces",
        "latexSymbol": "t",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "unit": "s",
        "decimal": 3,
        "limits": {},
        "default": "0.0",
        "const": False,
        "required": []
    },
    {
        "id": "G0_COMP_9",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Gravity Acceleration",
        "description": "Standard gravity acceleration",
        "latexSymbol": "g",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "unit": "m/s²",
        "decimal": 3,
        "limits": {},
        "default": "9.80665",
        "const": False,
        "required": []
    },
    {
        "id": "G0_COMP_10",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Deep Water Wavelength",
        "description": "Wavelength in deep water conditions",
        "latexSymbol": "L_0",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "decimal": 3,
        "limits": {},
        "default": "209.020",
        "const": False,
        "required": []
    },
    {
        "id": "G0_COMP_11",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Wavelength",
        "description": "The actual wavelength considering water depth effects",
        "latexSymbol": "L",
        "compType": "formula",
        "type": "string",
        "notation": "standard",
        "targetComponent": True,
        "decimal": 3,
        "limits": {},
        "required": [
            "G0_COMP_9",
            "G0_COMP_2",
            "G0_COMP_3",
            "G0_COMP_10"
        ],
        "latexEquation": "\\frac{\\sym{g}\\times\\sym{T}^2}{2\\times\\pi}\\times\\tanh(\\frac{2\\times\\pi\\times\\sym{h}}{\\sym{L_0}})"
    },
    {
        "id": "G0_COMP_12",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Total Wave Force",
        "description": "The total wave force on the pile using Morison equation",
        "latexSymbol": "F_{total}",
        "compType": "formula",
        "type": "string",
        "notation": "standard",
        "targetComponent": True,
        "unit": "kN/m",
        "decimal": 3,
        "limits": {},
        "required": [
            "G0_COMP_14",
            "G0_COMP_15"
        ],
        "latexEquation": "\\sym{F_i}+\\sym{F_d}"
    },
    {
        "id": "G0_COMP_13",
        "codeName": "General Engineering Formula",
        "reference": [
            "kN/m³"
        ],
        "title": "Seawater Density",
        "description": "The density of seawater",
        "latexSymbol": "\\rho_0",
        "compType": "number",
        "type": "string",
        "notation": "standard",
        "targetComponent": False,
        "decimal": 3,
        "limits": {},
        "default": "10.100",
        "const": False,
        "required": []
    },
    {
        "id": "G0_COMP_14",
        "codeName": "General Engineering Formula",
        "reference": [
            "s"
        ],
        "title": "Inertia Force",
        "description": "The inertia component of the wave force on the pile using Morison equation",
        "latexSymbol": "F_i",
        "compType": "formula",
        "type": "string",
        "notation": "standard",
        "targetComponent": True,
        "decimal": 3,
        "limits": {},
        "required": [
            "G0_COMP_6",
            "G0_COMP_13",
            "G0_COMP_4",
            "G0_COMP_1",
            "G0_COMP_11",
            "G0_COMP_7",
            "G0_COMP_3",
            "G0_COMP_8",
            "G0_COMP_2"
        ],
        "latexEquation": "\\sym{C_m}\\times\\sym{\\rho_0}\\times\\frac{\\pi\\times(\\sym{D})^2}{4}\\times\\sym{H}\\times\\frac{\\pi}{\\sym{L}}\\times\\frac{\\cosh\\left(\\frac{2\\pi\\times(\\sym{z}+\\sym{h})}{\\sym{L}}\\right)}{\\cosh\\left(\\frac{2\\pi\\times\\sym{h}}{\\sym{L}}\\right)}\\times\\sin\\left(-\\frac{2\\pi\\times\\sym{t}}{\\sym{T}}\\right)"
    },
    {
        "id": "G0_COMP_15",
        "codeName": "General Engineering Formula",
        "reference": [
            "-"
        ],
        "title": "Drag Force",
        "description": "The drag component of the wave force on the pile using Morison equation",
        "latexSymbol": "F_d",
        "compType": "formula",
        "type": "string",
        "notation": "standard",
        "targetComponent": True,
        "decimal": 3,
        "limits": {},
        "required": [
            "G0_COMP_5",
            "G0_COMP_13",
            "G0_COMP_4",
            "G0_COMP_1",
            "G0_COMP_9",
            "G0_COMP_2",
            "G0_COMP_11",
            "G0_COMP_7",
            "G0_COMP_3",
            "G0_COMP_8"
        ],
        "latexEquation": "\\frac{1}{2}\\times\\sym{C_d}\\times\\sym{\\rho_0}\\times\\sym{D}\\times(\\sym{H})^2\\times\\left[\\frac{\\sym{g}\\times(\\sym{T})^2}{4\\times(\\sym{L})^2}\\times\\left(\\frac{\\cosh\\left(\\frac{2\\pi\\times(\\sym{z}+\\sym{h})}{\\sym{L}}\\right)}{\\cosh\\left(\\frac{2\\pi\\times\\sym{h}}{\\sym{L}}\\right)}\\right)^2\\right]\\times\\cos\\left(\\frac{2\\pi\\times\\sym{t}}{\\sym{T}}\\right)\\times\\cos\\left(\\frac{2\\pi\\times\\sym{t}}{\\sym{T}}\\right)",
        "unit": "kN/m"
    }
]

# TODO : content 등록 필요 시 __init__.py 주석 해제
content_list = []