[
{
    "metaSchemaId": "pythonFunction",
    "schemaId": "BSEN1992:6_2_2:VRd_c",
    "data": {
        "desc": "Calculate design value for the shear resistance according to Eurocode 2 (EN 1992-1-1:2004)",
        "inputs": [
            {
                "arg": "CRd_c",
                "type": "dimensionless",
                "label": "C_{Rd,c}",
                "desc": "Empirical factor for shear resistance (recommended value 0.18/\\gamma_c)"
            },
            {
                "arg": "k",
                "type": "dimensionless",
                "label": "k",
                "desc": "Size effect factor: $k = 1 + \\sqrt{\\frac{200}{d}} \\leq 2.0$ with $d$ in mm"
            },
            {
                "arg": "rho_l",
                "type": "dimensionless",
                "label": "\\rho_l",
                "desc": "Longitudinal reinforcement ratio $\\rho_l = \\frac{A_{sl}}{b_w d} \\leq 0.02$"
            },
            {
                "arg": "fck",
                "type": "stress",
                "label": "f_{ck}",
                "desc": "Characteristic compressive strength of concrete in MPa"
            },
            {
                "arg": "k1",
                "type": "dimensionless",
                "label": "k_1",
                "desc": "Factor for normal stress contribution (recommended value 0.15)"
            },
            {
                "arg": "sigma_cp",
                "type": "stress",
                "label": "\\sigma_{cp}",
                "desc": "Normal stress due to axial force $\\sigma_{cp} = \\frac{N_{Ed}}{A_c} < 0.2 f_{cd}$ in MPa"
            },
            {
                "arg": "bw",
                "type": "length",
                "label": "b_w",
                "desc": "Smallest width of cross-section in tensile area in mm"
            },
            {
                "arg": "d",
                "type": "length",
                "label": "d",
                "desc": "Effective depth of cross-section in mm"
            },
            {
                "arg": "vmin",
                "type": "stress",
                "label": "v_{min}",
                "desc": "Minimum shear strength (default: $0.035 k^{3/2} f_{ck}^{1/2}$)"
            }
        ],
        "outputs": [
            {
                "label": "V_{Rd,c}",
                "type": "force",
                "desc": "Design value of the shear resistance in N"
            }
        ],
        "pythonFunctionDef": {
            "name": "calculate_shear_resistance",
            "args": [
                {
                    "arg": "CRd_c",
                    "type": "dimensionless"
                },
                {
                    "arg": "k",
                    "type": "dimensionless"
                },
                {
                    "arg": "rho_l",
                    "type": "dimensionless"
                },
                {
                    "arg": "fck",
                    "type": "stress"
                },
                {
                    "arg": "k1",
                    "type": "dimensionless"
                },
                {
                    "arg": "sigma_cp",
                    "type": "stress"
                },
                {
                    "arg": "bw",
                    "type": "length"
                },
                {
                    "arg": "d",
                    "type": "length"
                },
                {
                    "arg": "vmin",
                    "type": "stress"
                }
            ],
            "body": "VRd_c1 = (CRd_c * k * (100 * rho_l * fck)**(1/3) + k1 * sigma_cp) * bw * d\nVRd_c2 = (vmin + k1 * sigma_cp) * bw * d\nVRd_c = max(VRd_c1, VRd_c2)\nreturn VRd_c",
            "returnType": "force"
        }
    }
},
    {
        "metaSchemaId": "pythonFunction",
        "schemaId": "BSEN1992:6.2.4:VRd_c_uncracked",
        "data": {
            "desc": "Calculate shear resistance for uncracked regions in prestressed members according to Eurocode 2 (EN 1992-1-1:2004) Expression (6.4)",
            "inputs": [
                {
                    "arg": "I",
                    "type": "inertia",
                    "label": "I",
                    "desc": "Second moment of area of the cross-section"
                },
                {
                    "arg": "bw",
                    "type": "length",
                    "label": "b_w",
                    "desc": "Width of the cross-section at the centroidal axis"
                },
                {
                    "arg": "S",
                    "type": "volume",
                    "label": "S",
                    "desc": "First moment of area above and about the centroidal axis"
                },
                {
                    "arg": "fctd",
                    "type": "stress",
                    "label": "f_{ctd}",
                    "desc": "Design tensile strength of concrete"
                },
                {
                    "arg": "alpha_l",
                    "type": "dimensionless",
                    "label": "\\alpha_l",
                    "desc": "Coefficient for pretensioned tendons (≤ 1.0) or other prestressing (= 1.0)"
                },
                {
                    "arg": "sigma_cp",
                    "type": "stress",
                    "label": "\\sigma_{cp}",
                    "desc": "Concrete compressive stress at centroidal axis due to axial loading/prestressing (MPa)"
                }
            ],
            "outputs": [
                {
                    "label": "V_{Rd,c}",
                    "type": "force",
                    "desc": "Design shear resistance in uncracked regions (N)"
                }
            ],
            "pythonFunctionDef": {
                "name": "calculate_shear_resistance_uncracked",
                "args": [
                    {
                        "arg": "I",
                        "type": "inertia"
                    },
                    {
                        "arg": "bw",
                        "type": "length"
                    },
                    {
                        "arg": "S",
                        "type": "volume"
                    },
                    {
                        "arg": "fctd",
                        "type": "stress"
                    },
                    {
                        "arg": "alpha_l",
                        "type": "dimensionless"
                    },
                    {
                        "arg": "sigma_cp",
                        "type": "stress"
                    }
                ],
                "body": "import math\nVRd_c = (I * bw / S) * math.sqrt(fctd**2 + alpha_l * sigma_cp * fctd)\nreturn VRd_c",
                "returnType": "force"
            }
        }
    },
    {
        "metaSchemaId": "pythonFunction",
        "schemaId": "BSEN1992:6_2_2:max_shear_condition",
        "data": {
            "desc": "Check if design shear force satisfies maximum condition according to Eurocode 2 (6.5)",
            "inputs": [
                {
                    "arg": "VEd",
                    "type": "force",
                    "label": "V_{Ed}",
                    "desc": "Design shear force without reduction by β"
                },
                {
                    "arg": "bw",
                    "type": "length",
                    "label": "b_w",
                    "desc": "Width of the section"
                },
                {
                    "arg": "d",
                    "type": "length",
                    "label": "d",
                    "desc": "Effective depth of the section"
                },
                {
                    "arg": "v",
                    "type": "dimensionless",
                    "label": "\\nu",
                    "desc": "Strength reduction factor for concrete cracked in shear"
                },
                {
                    "arg": "fcd",
                    "type": "stress",
                    "label": "f_{cd}",
                    "desc": "Design compressive strength of concrete"
                }
            ],
            "outputs": [
                {
                    "label": "\\text{Condition satisfied}",
                    "type": "bool",
                    "desc": "True if VEd ≤ 0.5 bw·d·v·fcd"
                }
            ],
            "pythonFunctionDef": {
                "name": "check_max_shear_force_condition",
                "args": [
                    {
                        "arg": "VEd",
                        "type": "force"
                    },
                    {
                        "arg": "bw",
                        "type": "length"
                    },
                    {
                        "arg": "d",
                        "type": "length"
                    },
                    {
                        "arg": "v",
                        "type": "dimensionless"
                    },
                    {
                        "arg": "fcd",
                        "type": "stress"
                    }
                ],
                "body": "max_allowed = 0.5 * bw * d * v * fcd\nreturn VEd <= max_allowed",
                "returnType": "bool"
            }
        }
    },
    {
        "metaSchemaId": "pythonFunction",
        "schemaId": "BSEN1992:6_2_2:v_reduction_factor",
        "data": {
            "desc": "Calculate strength reduction factor v for concrete cracked in shear according to Eurocode 2 (6.6N)",
            "inputs": [
                {
                    "arg": "fck",
                    "type": "stress",
                    "label": "f_{ck}",
                    "desc": "Characteristic compressive strength of concrete in MPa"
                }
            ],
            "outputs": [
                {
                    "label": "\\nu",
                    "type": "dimensionless",
                    "desc": "Strength reduction factor"
                }
            ],
            "pythonFunctionDef": {
                "name": "calculate_strength_reduction_factor",
                "args": [
                    {
                        "arg": "fck",
                        "type": "stress"
                    }
                ],
                "body": "v = 0.6 * (1 - fck/250)\nreturn v",
                "returnType": "dimensionless"
            }
        }
    },
    {
        "metaSchemaId": "pythonFunction",
        "schemaId": "BSEN1992:6.2.3:VRd_s_vertical",
        "data": {
            "desc": "Calculate shear resistance for members with vertical shear reinforcement according to Eurocode 2 (6.8)",
            "inputs": [
                {
                    "arg": "Asw",
                    "type": "area",
                    "label": "A_{sw}",
                    "desc": "Cross-sectional area of shear reinforcement"
                },
                {
                    "arg": "s",
                    "type": "length",
                    "label": "s",
                    "desc": "Spacing of stirrups"
                },
                {
                    "arg": "z",
                    "type": "length",
                    "label": "z",
                    "desc": "Inner lever arm"
                },
                {
                    "arg": "fywd",
                    "type": "stress",
                    "label": "f_{ywd}",
                    "desc": "Design yield strength of shear reinforcement"
                },
                {
                    "arg": "theta",
                    "type": "angle",
                    "label": "\\theta",
                    "desc": "Angle between concrete compression strut and beam axis"
                }
            ],
            "outputs": [
                {
                    "label": "V_{Rd,s}",
                    "type": "force",
                    "desc": "Shear resistance provided by shear reinforcement"
                }
            ],
            "pythonFunctionDef": {
                "name": "calculate_vertical_shear_resistance",
                "args": [
                    {
                        "arg": "Asw",
                        "type": "area"
                    },
                    {
                        "arg": "s",
                        "type": "length"
                    },
                    {
                        "arg": "z",
                        "type": "length"
                    },
                    {
                        "arg": "fywd",
                        "type": "stress"
                    },
                    {
                        "arg": "theta",
                        "type": "angle"
                    }
                ],
                "body": "import math\nVRd_s = (Asw / s) * z * fywd * math.cos(math.radians(theta))\nreturn VRd_s",
                "returnType": "force"
            }
        }
    },
    {
        "metaSchemaId": "pythonFunction",
        "schemaId": "BSEN1992:6.2.3:VRd_max_vertical",
        "data": {
            "desc": "Calculate maximum shear resistance for members with vertical shear reinforcement according to Eurocode 2 (6.9)",
            "inputs": [
                {
                    "arg": "alpha_cw",
                    "type": "dimensionless",
                    "label": "\\alpha_{cw}",
                    "desc": "Coefficient for compression chord stress state"
                },
                {
                    "arg": "bw",
                    "type": "length",
                    "label": "b_w",
                    "desc": "Minimum width between tension and compression chords"
                },
                {
                    "arg": "z",
                    "type": "length",
                    "label": "z",
                    "desc": "Inner lever arm"
                },
                {
                    "arg": "v1",
                    "type": "dimensionless",
                    "label": "\\nu_1",
                    "desc": "Strength reduction factor for concrete cracked in shear"
                },
                {
                    "arg": "fcd",
                    "type": "stress",
                    "label": "f_{cd}",
                    "desc": "Design compressive strength of concrete"
                },
                {
                    "arg": "theta",
                    "type": "angle",
                    "label": "\\theta",
                    "desc": "Angle between concrete compression strut and beam axis"
                }
            ],
            "outputs": [
                {
                    "label": "V_{Rd,max}",
                    "type": "force",
                    "desc": "Maximum shear resistance limited by concrete crushing"
                }
            ],
            "pythonFunctionDef": {
                "name": "calculate_max_shear_resistance_vertical",
                "args": [
                    {
                        "arg": "alpha_cw",
                        "type": "dimensionless"
                    },
                    {
                        "arg": "bw",
                        "type": "length"
                    },
                    {
                        "arg": "z",
                        "type": "length"
                    },
                    {
                        "arg": "v1",
                        "type": "dimensionless"
                    },
                    {
                        "arg": "fcd",
                        "type": "stress"
                    },
                    {
                        "arg": "theta",
                        "type": "angle"
                    }
                ],
                "body": "import math\ntheta_rad = math.radians(theta)\nVRd_max = alpha_cw * bw * z * v1 * fcd / (math.cos(theta_rad) + math.sin(theta_rad))\nreturn VRd_max",
                "returnType": "force"
            }
        }
    },
    {
        "metaSchemaId": "pythonFunction",
        "schemaId": "BSEN1992:6.2.3:VRd_s_inclined",
        "data": {
            "desc": "Calculate shear resistance for members with inclined shear reinforcement according to Eurocode 2 (6.13)",
            "inputs": [
                {
                    "arg": "Asw",
                    "type": "area",
                    "label": "A_{sw}",
                    "desc": "Cross-sectional area of shear reinforcement"
                },
                {
                    "arg": "s",
                    "type": "length",
                    "label": "s",
                    "desc": "Spacing of stirrups"
                },
                {
                    "arg": "z",
                    "type": "length",
                    "label": "z",
                    "desc": "Inner lever arm"
                },
                {
                    "arg": "fywd",
                    "type": "stress",
                    "label": "f_{ywd}",
                    "desc": "Design yield strength of shear reinforcement"
                },
                {
                    "arg": "theta",
                    "type": "angle",
                    "label": "\\theta",
                    "desc": "Angle between concrete compression strut and beam axis"
                },
                {
                    "arg": "alpha",
                    "type": "angle",
                    "label": "\\alpha",
                    "desc": "Angle between shear reinforcement and beam axis"
                }
            ],
            "outputs": [
                {
                    "label": "V_{Rd,s}",
                    "type": "force",
                    "desc": "Shear resistance provided by inclined shear reinforcement"
                }
            ],
            "pythonFunctionDef": {
                "name": "calculate_inclined_shear_resistance",
                "args": [
                    {
                        "arg": "Asw",
                        "type": "area"
                    },
                    {
                        "arg": "s",
                        "type": "length"
                    },
                    {
                        "arg": "z",
                        "type": "length"
                    },
                    {
                        "arg": "fywd",
                        "type": "stress"
                    },
                    {
                        "arg": "theta",
                        "type": "angle"
                    },
                    {
                        "arg": "alpha",
                        "type": "angle"
                    }
                ],
                "body": "import math\ntheta_rad = math.radians(theta)\nalpha_rad = math.radians(alpha)\nVRd_s = (Asw / s) * z * fywd * (math.cos(theta_rad) + math.cos(alpha_rad)) * math.sin(alpha_rad)\nreturn VRd_s",
                "returnType": "force"
            }
        }
    },
    {
        "metaSchemaId": "pythonFunction",
        "schemaId": "BSEN1992:6.2.3:VRd_max_inclined",
        "data": {
            "desc": "Calculate maximum shear resistance for members with inclined shear reinforcement according to Eurocode 2 (6.14)",
            "inputs": [
                {
                    "arg": "alpha_cw",
                    "type": "dimensionless",
                    "label": "\\alpha_{cw}",
                    "desc": "Coefficient for compression chord stress state"
                },
                {
                    "arg": "bw",
                    "type": "length",
                    "label": "b_w",
                    "desc": "Minimum width between tension and compression chords"
                },
                {
                    "arg": "z",
                    "type": "length",
                    "label": "z",
                    "desc": "Inner lever arm"
                },
                {
                    "arg": "v1",
                    "type": "dimensionless",
                    "label": "\\nu_1",
                    "desc": "Strength reduction factor for concrete cracked in shear"
                },
                {
                    "arg": "fcd",
                    "type": "stress",
                    "label": "f_{cd}",
                    "desc": "Design compressive strength of concrete"
                },
                {
                    "arg": "theta",
                    "type": "angle",
                    "label": "\\theta",
                    "desc": "Angle between concrete compression strut and beam axis"
                },
                {
                    "arg": "alpha",
                    "type": "angle",
                    "label": "\\alpha",
                    "desc": "Angle between shear reinforcement and beam axis"
                }
            ],
            "outputs": [
                {
                    "label": "V_{Rd,max}",
                    "type": "force",
                    "desc": "Maximum shear resistance limited by concrete crushing"
                }
            ],
            "pythonFunctionDef": {
                "name": "calculate_max_shear_resistance_inclined",
                "args": [
                    {
                        "arg": "alpha_cw",
                        "type": "dimensionless"
                    },
                    {
                        "arg": "bw",
                        "type": "length"
                    },
                    {
                        "arg": "z",
                        "type": "length"
                    },
                    {
                        "arg": "v1",
                        "type": "dimensionless"
                    },
                    {
                        "arg": "fcd",
                        "type": "stress"
                    },
                    {
                        "arg": "theta",
                        "type": "angle"
                    },
                    {
                        "arg": "alpha",
                        "type": "angle"
                    }
                ],
                "body": "import math\ntheta_rad = math.radians(theta)\nalpha_rad = math.radians(alpha)\nVRd_max = alpha_cw * bw * z * v1 * fcd * (math.cos(theta_rad) + math.cos(alpha_rad)) / (1 + math.cos(theta_rad)**2)\nreturn VRd_max",
                "returnType": "force"
            }
        }
    },
    {
        "metaSchemaId": "pythonFunction",
        "schemaId": "BSEN1992:6.2.3:alpha_cw",
        "data": {
            "desc": "Calculate coefficient alpha_cw taking into account the state of stress in compression chord according to Eurocode 2 (6.11)",
            "inputs": [
                {
                    "arg": "sigma_cp",
                    "type": "stress",
                    "label": "\\sigma_{cp}",
                    "desc": "Mean compressive stress in concrete due to design axial force"
                },
                {
                    "arg": "fcd",
                    "type": "stress",
                    "label": "f_{cd}",
                    "desc": "Design compressive strength of concrete"
                }
            ],
            "outputs": [
                {
                    "label": "\\alpha_{cw}",
                    "type": "dimensionless",
                    "desc": "Coefficient for stress state in compression chord"
                }
            ],
            "pythonFunctionDef": {
                "name": "calculate_alpha_cw",
                "args": [
                    {
                        "arg": "sigma_cp",
                        "type": "stress"
                    },
                    {
                        "arg": "fcd",
                        "type": "stress"
                    }
                ],
                "body": "if sigma_cp == 0:\n    return 1.0  # For non-prestressed structures\nelif 0 < sigma_cp <= 0.25 * fcd:\n    return 1 + sigma_cp / fcd\nelif 0.25 * fcd < sigma_cp <= 0.5 * fcd:\n    return 1.25\nelif 0.5 * fcd < sigma_cp < 1.0 * fcd:\n    return 2.5 * (1 - sigma_cp / fcd)\nelse:\n    return 0  # Outside valid range",
                "returnType": "dimensionless"
            }
        }
    },
    {
        "metaSchemaId": "pythonFunction",
        "schemaId": "BSEN1992:6.2.3:max_vertical_reinforcement_check",
        "data": {
            "desc": "Check if the amount of vertical shear reinforcement satisfies the maximum limit according to Eurocode 2 (6.12)",
            "inputs": [
                {
                    "arg": "Asw_max",
                    "type": "area",
                    "label": "A_{sw,max}",
                    "desc": "Maximum cross-sectional area of shear reinforcement"
                },
                {
                    "arg": "fywd",
                    "type": "stress",
                    "label": "f_{ywd}",
                    "desc": "Design yield strength of shear reinforcement"
                },
                {
                    "arg": "bw",
                    "type": "length",
                    "label": "b_w",
                    "desc": "Minimum width of section"
                },
                {
                    "arg": "s",
                    "type": "length",
                    "label": "s",
                    "desc": "Spacing of stirrups"
                },
                {
                    "arg": "alpha_cw",
                    "type": "dimensionless",
                    "label": "\\alpha_{cw}",
                    "desc": "Coefficient for stress state in compression chord"
                },
                {
                    "arg": "v1",
                    "type": "dimensionless",
                    "label": "\\nu_1",
                    "desc": "Strength reduction factor for concrete"
                },
                {
                    "arg": "fcd",
                    "type": "stress",
                    "label": "f_{cd}",
                    "desc": "Design compressive strength of concrete"
                }
            ],
            "outputs": [
                {
                    "label": "\\text{Condition satisfied}",
                    "type": "bool",
                    "desc": "True if maximum effective shear reinforcement limit is satisfied"
                }
            ],
            "pythonFunctionDef": {
                "name": "check_max_vertical_shear_reinforcement",
                "args": [
                    {
                        "arg": "Asw_max",
                        "type": "area"
                    },
                    {
                        "arg": "fywd",
                        "type": "stress"
                    },
                    {
                        "arg": "bw",
                        "type": "length"
                    },
                    {
                        "arg": "s",
                        "type": "length"
                    },
                    {
                        "arg": "alpha_cw",
                        "type": "dimensionless"
                    },
                    {
                        "arg": "v1",
                        "type": "dimensionless"
                    },
                    {
                        "arg": "fcd",
                        "type": "stress"
                    }
                ],
                "body": "max_limit = 0.5 * alpha_cw * v1 * fcd\nactual = (Asw_max * fywd) / (bw * s)\nreturn actual <= max_limit",
                "returnType": "bool"
            }
        }
    },
    {
        "metaSchemaId": "pythonFunction",
        "schemaId": "BSEN1992:6.2.3:max_inclined_reinforcement_check",
        "data": {
            "desc": "Check if the amount of inclined shear reinforcement satisfies the maximum limit according to Eurocode 2 (6.15)",
            "inputs": [
                {
                    "arg": "Asw_max",
                    "type": "area",
                    "label": "A_{sw,max}",
                    "desc": "Maximum cross-sectional area of shear reinforcement"
                },
                {
                    "arg": "fywd",
                    "type": "stress",
                    "label": "f_{ywd}",
                    "desc": "Design yield strength of shear reinforcement"
                },
                {
                    "arg": "bw",
                    "type": "length",
                    "label": "b_w",
                    "desc": "Minimum width of section"
                },
                {
                    "arg": "s",
                    "type": "length",
                    "label": "s",
                    "desc": "Spacing of stirrups"
                },
                {
                    "arg": "alpha_cw",
                    "type": "dimensionless",
                    "label": "\\alpha_{cw}",
                    "desc": "Coefficient for stress state in compression chord"
                },
                {
                    "arg": "v1",
                    "type": "dimensionless",
                    "label": "\\nu_1",
                    "desc": "Strength reduction factor for concrete"
                },
                {
                    "arg": "fcd",
                    "type": "stress",
                    "label": "f_{cd}",
                    "desc": "Design compressive strength of concrete"
                },
                {
                    "arg": "alpha",
                    "type": "angle",
                    "label": "\\alpha",
                    "desc": "Angle between shear reinforcement and beam axis"
                }
            ],
            "outputs": [
                {
                    "label": "\\text{Condition satisfied}",
                    "type": "bool",
                    "desc": "True if maximum effective shear reinforcement limit is satisfied"
                }
            ],
            "pythonFunctionDef": {
                "name": "check_max_inclined_shear_reinforcement",
                "args": [
                    {
                        "arg": "Asw_max",
                        "type": "area"
                    },
                    {
                        "arg": "fywd",
                        "type": "stress"
                    },
                    {
                        "arg": "bw",
                        "type": "length"
                    },
                    {
                        "arg": "s",
                        "type": "length"
                    },
                    {
                        "arg": "alpha_cw",
                        "type": "dimensionless"
                    },
                    {
                        "arg": "v1",
                        "type": "dimensionless"
                    },
                    {
                        "arg": "fcd",
                        "type": "stress"
                    },
                    {
                        "arg": "alpha",
                        "type": "angle"
                    }
                ],
                "body": "import math\nalpha_rad = math.radians(alpha)\nmax_limit = 0.5 * alpha_cw * v1 * fcd / math.sin(alpha_rad)\nactual = (Asw_max * fywd) / (bw * s)\nreturn actual <= max_limit",
                "returnType": "bool"
            }
        }
    }
]