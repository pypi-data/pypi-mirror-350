[
    {
        "data": [
            {
                "id": "CRd_c",
                "schemaId": "BSEN1992:6_2_2:CRd_c",
                "inputs": [
                    {
                        "type": "dimensionless",
                        "data": {
                            "value": 0.18,
                            "unit": ""
                        }
                    }
                ]
            },
            {
                "id": "d",
                "schemaId": "BSEN1992:6_2_2:d",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 500,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "k",
                "schemaId": "BSEN1992:6_2_2:k_size_effect",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "d",
                        "index": 0
                    }
                ]
            },
            {
                "id": "Asl",
                "schemaId": "BSEN1992:6_2_2:Asl",
                "inputs": [
                    {
                        "type": "area",
                        "data": {
                            "value": 1500,
                            "unit": "mm^{2}"
                        }
                    }
                ]
            },
            {
                "id": "bw",
                "schemaId": "BSEN1992:6_2_2:bw",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 300,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "rho_l",
                "schemaId": "BSEN1992:6_2_2:rho_l",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "Asl",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "bw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "d",
                        "index": 0
                    }
                ]
            },
            {
                "id": "fck",
                "schemaId": "BSEN1992:6_2_2:fck",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 30,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "k1",
                "schemaId": "BSEN1992:6_2_2:k1",
                "inputs": [
                    {
                        "type": "dimensionless",
                        "data": {
                            "value": 0.15,
                            "unit": ""
                        }
                    }
                ]
            },
            {
                "id": "NEd",
                "schemaId": "BSEN1992:6_2_2:NEd",
                "inputs": [
                    {
                        "type": "force",
                        "data": {
                            "value": 200000,
                            "unit": "N"
                        }
                    }
                ]
            },
            {
                "id": "Ac",
                "schemaId": "BSEN1992:6_2_2:Ac",
                "inputs": [
                    {
                        "type": "area",
                        "data": {
                            "value": 300000,
                            "unit": "mm^{2}"
                        }
                    }
                ]
            },
            {
                "id": "sigma_cp",
                "schemaId": "BSEN1992:6_2_2:sigma_cp",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "NEd",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "Ac",
                        "index": 0
                    }
                ]
            },
            {
                "id": "vmin",
                "schemaId": "BSEN1992:6_2_2:vmin",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "k",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fck",
                        "index": 0
                    }
                ]
            },
            {
                "id": "VRd_c",
                "schemaId": "BSEN1992:6_2_2:VRd_c",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "CRd_c",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "k",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "rho_l",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fck",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "k1",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "sigma_cp",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "bw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "d",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "vmin",
                        "index": 0
                    }
                ],
            }
        ]
    },
    {
        "data": [
            {
                "id": "Asw",
                "schemaId": "BSEN1992:6_2_2:Asw",
                "inputs": [
                    {
                        "type": "area",
                        "data": {
                            "value": 157,
                            "unit": "mm^{2}"
                        }
                    }
                ]
            },
            {
                "id": "s",
                "schemaId": "BSEN1992:6_2_2:s",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 200,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "d",
                "schemaId": "BSEN1992:6_2_2:d",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 450,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "z",
                "schemaId": "BSEN1992:6_2_2:z",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "d",
                        "index": 0
                    }
                ]
            },
            {
                "id": "fywd",
                "schemaId": "BSEN1992:6_2_2:fywd",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 435,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "theta",
                "schemaId": "BSEN1992:6_2_2:theta",
                "inputs": [
                    {
                        "type": "angle",
                        "data": {
                            "value": 45,
                            "unit": "degree"
                        }
                    }
                ]
            },
            {
                "id": "VRd_s",
                "schemaId": "BSEN1992:6_2_2:VRd_s",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "Asw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "s",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "z",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fywd",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "theta",
                        "index": 0
                    }
                ]
            },
            {
                "id": "fck",
                "schemaId": "BSEN1992:6_2_2:fck",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 30,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "v1",
                "schemaId": "BSEN1992:6_2_2:v1",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "fck",
                        "index": 0
                    }
                ]
            },
            {
                "id": "bw",
                "schemaId": "BSEN1992:6_2_2:bw",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 300,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "fcd",
                "schemaId": "BSEN1992:6_2_2:fcd",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 20,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "sigma_cp",
                "schemaId": "BSEN1992:6_2_2:sigma_cp",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 2,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "alpha_cw",
                "schemaId": "BSEN1992:6_2_2:alpha_cw",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "sigma_cp",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fcd",
                        "index": 0
                    }
                ]
            },
            {
                "id": "VRd_max",
                "schemaId": "BSEN1992:6_2_2:VRd_max",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "alpha_cw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "bw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "z",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "v1",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fcd",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "theta",
                        "index": 0
                    }
                ]
            }
        ]
    },
    {
        "data": [
            {
                "id": "Asw",
                "schemaId": "BSEN1992:6_2_2:Asw",
                "inputs": [
                    {
                        "type": "area",
                        "data": {
                            "value": 157,
                            "unit": "mm^{2}"
                        }
                    }
                ]
            },
            {
                "id": "s",
                "schemaId": "BSEN1992:6_2_2:s",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 200,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "d",
                "schemaId": "BSEN1992:6_2_2:d",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 450,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "z",
                "schemaId": "BSEN1992:6.2.3:z_lever_arm",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "d",
                        "index": 0
                    }
                ]
            },
            {
                "id": "fywd",
                "schemaId": "BSEN1992:6_2_2:fywd",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 435,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "theta",
                "schemaId": "BSEN1992:6_2_2:theta",
                "inputs": [
                    {
                        "type": "angle",
                        "data": {
                            "value": 45,
                            "unit": "degree"
                        }
                    }
                ]
            },
            {
                "id": "alpha",
                "schemaId": "BSEN1992:6_2_2:alpha",
                "inputs": [
                    {
                        "type": "angle",
                        "data": {
                            "value": 45,
                            "unit": "degree"
                        }
                    }
                ]
            },
            {
                "id": "VRd_s",
                "schemaId": "BSEN1992:6_2_2:VRd_s",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "Asw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "s",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "z",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fywd",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "theta",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "alpha",
                        "index": 0
                    }
                ]
            },
            {
                "id": "fck",
                "schemaId": "BSEN1992:6_2_2:fck",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 30,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "v1",
                "schemaId": "BSEN1992:6_2_2:v1",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "fck",
                        "index": 0
                    }
                ]
            },
            {
                "id": "bw",
                "schemaId": "BSEN1992:6_2_2:bw",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 300,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "fcd",
                "schemaId": "BSEN1992:6_2_2:fcd",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 20,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "sigma_cp",
                "schemaId": "BSEN1992:6_2_2:sigma_cp",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 2,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "alpha_cw",
                "schemaId": "BSEN1992:6_2_2:alpha_cw",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "sigma_cp",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fcd",
                        "index": 0
                    }
                ]
            },
            {
                "id": "VRd_max",
                "schemaId": "BSEN1992:6_2_2:VRd_max",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "alpha_cw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "bw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "z",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "v1",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fcd",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "theta",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "alpha",
                        "index": 0
                    }
                ]
            }
        ]
    },
    {
        "data": [
            {
                "id": "VEd",
                "schemaId": "BSEN1992:6_2_2:VEd",
                "inputs": [
                    {
                        "type": "force",
                        "data": {
                            "value": 250000,
                            "unit": "N"
                        }
                    }
                ]
            },
            {
                "id": "bw",
                "schemaId": "BSEN1992:6_2_2:bw",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 300,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "d",
                "schemaId": "BSEN1992:6_2_2:d",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 450,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "fck",
                "schemaId": "BSEN1992:6_2_2:fck",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 30,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "v",
                "schemaId": "BSEN1992:6_2_2:v_reduction_factor",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "fck",
                        "index": 0
                    }
                ]
            },
            {
                "id": "fcd",
                "schemaId": "BSEN1992:6_2_2:fcd",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 20,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "max_shear_condition",
                "schemaId": "BSEN1992:6_2_2:max_shear_condition",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "VEd",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "bw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "d",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "v",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fcd",
                        "index": 0
                    }
                ]
            }
        ]
    },
    {
        "data": [
            {
                "id": "Asw_max",
                "schemaId": "BSEN1992:6_2_2:Asw_max",
                "inputs": [
                    {
                        "type": "area",
                        "data": {
                            "value": 200,
                            "unit": "mm^{2}"
                        }
                    }
                ]
            },
            {
                "id": "fywd",
                "schemaId": "BSEN1992:6_2_2:fywd",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 435,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "bw",
                "schemaId": "BSEN1992:6_2_2:bw",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 300,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "s",
                "schemaId": "BSEN1992:6_2_2:s",
                "inputs": [
                    {
                        "type": "length",
                        "data": {
                            "value": 200,
                            "unit": "mm"
                        }
                    }
                ]
            },
            {
                "id": "fck",
                "schemaId": "BSEN1992:6_2_2:fck",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 30,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "v1",
                "schemaId": "BSEN1992:6.2.3:v1_strength_reduction",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "fck",
                        "index": 0
                    }
                ]
            },
            {
                "id": "fcd",
                "schemaId": "BSEN1992:6_2_2:fcd",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 20,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "sigma_cp",
                "schemaId": "BSEN1992:6_2_2:sigma_cp",
                "inputs": [
                    {
                        "type": "stress",
                        "data": {
                            "value": 2,
                            "unit": "MPa"
                        }
                    }
                ]
            },
            {
                "id": "alpha_cw",
                "schemaId": "BSEN1992:6.2.3:alpha_cw",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "sigma_cp",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fcd",
                        "index": 0
                    }
                ]
            },
            {
                "id": "max_vertical_reinforcement_check",
                "schemaId": "BSEN1992:6.2.3:max_vertical_reinforcement_check",
                "inputs": [
                    {
                        "type": "edge",
                        "id": "Asw_max",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fywd",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "bw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "s",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "alpha_cw",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "v1",
                        "index": 0
                    },
                    {
                        "type": "edge",
                        "id": "fcd",
                        "index": 0
                    }
                ]
            }
        ]
    }
]
