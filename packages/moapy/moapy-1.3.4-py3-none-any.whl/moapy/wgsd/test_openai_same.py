import openai
import datetime

# OpenAI API 키 설정
openai.api_key = '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'

origin_text = """
#6.2.2 Members not requiring design shear reinforcement
##Section Route:
bsen1992 -> SECTION 6 ULTIMATE LIMIT STATES (ULS) -> 6.2 Shear   -> 6.2.2 Members not requiring design shear reinforcement
##Section Page Number:
89~92
##Section Content:
(1) The design value for the shear resistance \\(V_{Rd,c}\\) is given by:

\\(V_{Rd,c} = [C_{Rd,c}k(100 \\ \\rho_l f_{ck})^{1/3} + k_1 \\ \\sigma_{cp}] \\ b_wd \\) \\hspace{0.5cm} (6.2.a)

with a minimum of

\\(V_{Rd,c} = (v_{min} + k_1 \\sigma_{cp}) \\ b_wd \\) \\hspace{0.5cm} (6.2.b)

where:
\\( f_{ck} \\) is in MPa

\\( k = 1+ \\sqrt{\\frac{200}{d}} \\leq 2,0 \\) with \\( d \\) in mm

\\( \\rho_l = \\frac{A_{sl}}{b_wd} \\leq 0,02 \\)

\\( A_{sl} \\) is the area of the tensile reinforcement, which extends \\(\\geq (l_{bd} + d)\\) beyond the section considered (see Figure 6.3).

85
!#&page: 90

BS EN 1992-1-1:2004  
EN 1992-1-1:2004 (E)  

b_w is the smallest width of the cross-section in the tensile area [mm]  
\\sigma_{cp} = \\frac{N_{Ed}}{A_c} < 0.2 \\, f_{cd} \\; \\text{[MPa]}  
N_{Ed} is the axial force in the cross-section due to loading or prestressing [in N] (N_{Ed} > 0 \\text{ [AC]}
for compression). The influence of imposed deformations on N_{Ed} may be ignored. [AC]  
A_c is the area of concrete cross section [mm^2]  
V_{Rd,c} is [N]  

Note: The values of C_{Rd,c}, v_{min} and k_1 for use in a Country may be found in its National Annex. The
recommended value for C_{Rd,c} is 0.18/\\gamma_c, that for v_{min} is given by Expression (6.3N) and that for k_1 is 0.15.  

v_{min} = 0.035 \\, k^{3/2} \\cdot f_{ck}^{1/2}  

Figure 6.3: Definition of A_{sl} in Expression (6.2)  

(2) In prestressed single span members without shear reinforcement, the shear resistance of
the regions cracked in bending may be calculated using Expression (6.2a). In regions
uncracked in bending (where the flexural tensile stress is smaller than f_{ctk,0.05}/\\gamma_c) the
V_{Rd,c} = \\frac{I \\cdot b_w}{S} \\sqrt{(f_{ctd})^2 + \\alpha_l \\sigma_{cp} f_{ctd}} \\quad (6.4)

where

I \\quad\\text{is the second moment of area}

b_w \\quad\\text{is the width of the cross-section at the centroidal axis, allowing for the presence of ducts in accordance with Expressions (6.16) and (6.17)}

S \\quad\\text{is the first moment of area above and about the centroidal axis}

\\alpha_l \\quad= l_x/l_{pt2} \\leq 1.0 \\text{ for pretensioned tendons}\\
\\quad\\quad\\quad= 1.0 \\text{ for other types of prestressing}

l_x \\quad\\text{is the distance of section considered from the starting point of the transmission length}

l_{pt2} \\quad\\text{is the upper bound value of the transmission length of the prestressing element according to Expression (8.18).}

\\sigma_{cp} \\quad\\text{is the concrete compressive stress at the centroidal axis due to axial loading and/or prestressing}\\ (\\sigma_{cp} = N_{Ed}/A_c \\text{ in MPa},\\ N_{Ed} > 0 \\text{ in compression})

For cross-sections where the width varies over the height, the maximum principal stress may occur on an axis other than the centroidal axis. In such a case the minimum value of the shear resistance should be found by calculating V_{Rd,c} at various axes in the cross-section.

86
!#&page: 91

BS EN 1992-1-1:2004  
EN 1992-1-1:2004 (E)

(3) The calculation of the shear resistance according to Expression (6.4) is not required for cross-sections that are nearer to the support than the point which is the intersection of the elastic centroidal axis and a line inclined from the inner edge of the support at an angle of 45Â°.

(4) For the general case of members subjected to a bending moment and an axial force, which can be shown to be uncracked in flexure at the ULS, reference is made to 12.6.3.

(5) For the design of the longitudinal reinforcement, in the region cracked in flexure, the \\( M_{Ed} \\) line should be shifted over a distance \\( a_l = d \\) in the unfavourable direction (see 9.2.1.3 (2)).

(6) For members with loads applied on the upper side within a distance \\( 0.5d \\leq a_v \\leq 2d \\) from the edge of a support (or centre of bearing where flexible bearings are used), the contribution of this load to the shear force \\( V_{Ed} \\) may be multiplied by \\( \\beta = a_v/2d \\). This reduction may be applied for checking \\( V_{Rd,c} \\) in Expression (6.2.a). This is only valid provided that the longitudinal reinforcement is fully anchored at the support. For \\( a_v \\leq 0.5d \\) the value \\( a_v = 0.5d \\) should be used.

The shear force \\( V_{Ed} \\), calculated without reduction by \\( \\beta \\), should however always satisfy the condition

\\[ V_{Ed} \\leq 0.5 \\, b_w d \\, \\nu \\, f_{cd} \\]

(6.5)

where \\( \\nu \\) is a strength reduction factor for concrete cracked in shear

Note: The value \\( \\nu \\) for use in a Country may be found in its National Annex. The recommended value follows from:
\\nu = 0.6 \\left[ 1 - \\frac{f_{ck}}{250} \\right] \\quad (f_{ck} \\text{ in MPa}) \\quad (6.6N)

(a) Beam with direct support \\quad (b) Corbel

Figure 6.4: Loads near supports

(7) Beams with loads near to supports and corbels may alternatively be designed with strut and tie models. For this alternative, reference is made to 6.5.

87
!#&page: 92

BS EN 1992-1-1:2004  
EN 1992-1-1:2004 (E)
"""

origin_json_component = """
[
    {
      "metaSchemaId": "pythonFunction",
      "data": {
        "schemaId": "BSEN1992::6.2.2::CRd_c",
        "desc": "Empirical factor for shear resistance (recommended value 0.18/\\gamma_c)",
        "inputs": [
          {
            "label": "gamma_c",
            "type": "dimensionless",
            "default_unit": "factor",
            "desc": "Partial safety factor for concrete"
          }
        ],
        "outputs": [
          {
            "label": "CRd_c",
            "type": "dimensionless",
            "default_unit": "factor",
            "desc": "Empirical factor for shear resistance"
          }
        ],
        "pythonFunctionDef": {
          "name": "calculate_CRd_c",
          "args": [
            {
              "arg": "gamma_c",
              "type": "float"
            }
          ],
          "body": "return 0.18 / gamma_c",
          "returnType": "float"
        }
      }
    },
    {
      "metaSchemaId": "pythonFunction",
      "data": {
        "schemaId": "BSEN1992::6.2.2::k",
        "desc": "Size effect factor: $k = 1 + \\sqrt{\\frac{200}{d}} \\leq 2.0$ with $d$ in mm",
        "inputs": [
          {
            "label": "d",
            "type": "length",
            "default_unit": "mm",
            "desc": "Effective depth of the section in mm"
          }
        ],
        "outputs": [
          {
            "label": "k",
            "type": "dimensionless",
            "default_unit": "factor",
            "desc": "Size effect factor"
          }
        ],
        "pythonFunctionDef": {
          "name": "calculate_k",
          "args": [
            {
              "arg": "d",
              "type": "float"
            }
          ],
          "body": "import math\nk = 1 + math.sqrt(200 / d)\nreturn min(k, 2.0)",
          "returnType": "float"
        }
      }
    },
    {
      "metaSchemaId": "pythonFunction",
      "data": {
        "schemaId": "BSEN1992::6.2.2::rho_l",
        "desc": "Longitudinal reinforcement ratio: $\\rho_l = \\frac{A_{sl}}{b_w d} \\leq 0.02$",
        "inputs": [
          {
            "label": "A_sl",
            "type": "area",
            "default_unit": "mm2",
            "desc": "Total area of longitudinal reinforcement"
          },
          {
            "label": "b_w",
            "type": "length",
            "default_unit": "mm",
            "desc": "Width of the cross-section"
          },
          {
            "label": "d",
            "type": "length",
            "default_unit": "mm",
            "desc": "Effective depth of the section"
          }
        ],
        "outputs": [
          {
            "label": "rho_l",
            "type": "dimensionless",
            "default_unit": "factor",
            "desc": "Longitudinal reinforcement ratio"
          }
        ],
        "pythonFunctionDef": {
          "name": "calculate_rho_l",
          "args": [
            {
              "arg": "A_sl",
              "type": "float"
            },
            {
              "arg": "bw",
              "type": "float"
            },
            {
              "arg": "d",
              "type": "float"
            }
          ],
          "body": "rho_l = A_sl / (bw * d)\nreturn min(rho_l, 0.02)",
          "returnType": "float"
        }
      }
    },
    {
      "metaSchemaId": "pythonFunction",
      "data": {
        "schemaId": "BSEN1992::6.2.2::sigma_cp",
        "desc": "Normal stress due to axial force: $\\sigma_{cp} = \\frac{N_{Ed}}{A_c} < 0.2 f_{cd}$ in MPa",
        "inputs": [
          {
            "label": "N_Ed",
            "type": "force",
            "default_unit": "N",
            "desc": "Design value of the axial force"
          },
          {
            "label": "A_c",
            "type": "area",
            "default_unit": "mm2",
            "desc": "Area of the cross-section"
          },
          {
            "label": "f_cd",
            "type": "stress",
            "default_unit": "MPa",
            "desc": "Design compressive strength of concrete"
          }
        ],
        "outputs": [
          {
            "label": "sigma_cp",
            "type": "stress",
            "default_unit": "MPa",
            "desc": "Normal stress due to axial force"
          }
        ],
        "pythonFunctionDef": {
          "name": "calculate_sigma_cp",
          "args": [
            {
              "arg": "N_Ed",
              "type": "float"
            },
            {
              "arg": "A_c",
              "type": "float"
            },
            {
              "arg": "f_cd",
              "type": "float"
            }
          ],
          "body": "sigma_cp = N_Ed / A_c\nreturn min(sigma_cp, 0.2 * f_cd)",
          "returnType": "float"
        }
      }
    },
    {
      "metaSchemaId": "pythonFunction",
      "data": {
        "schemaId": "BSEN1992::6.2.2::v_min",
        "desc": "Minimum shear strength: $v_{min} = 0.035 k^{3/2} f_{ck}^{1/2}$ in MPa",
        "inputs": [
          {
            "label": "k",
            "type": "dimensionless",
            "default_unit": "factor",
            "desc": "Size effect factor"
          },
          {
            "label": "f_{ck}",
            "type": "stress",
            "default_unit": "MPa",
            "desc": "Characteristic compressive strength of concrete"
          }
        ],
        "outputs": [
          {
            "label": "v_min",
            "type": "stress",
            "default_unit": "MPa",
            "desc": "Minimum shear strength"
          }
        ],
        "pythonFunctionDef": {
          "name": "calculate_v_min",
          "args": [
            {
              "arg": "k",
              "type": "float"
            },
            {
              "arg": "f_ck",
              "type": "float"
            }
          ],
          "body": "v_min = 0.035 * k**(3/2) * f_ck**(1/2)\nreturn v_min",
          "returnType": "float"
        }
      }
    },
    {
      "metaSchemaId": "pythonFunction",
      "data": {
        "schemaId": "BSEN1992::6.2.2::V_Rd_c",
        "desc": "Calculate design value for the shear resistance according to Eurocode 2 (EN 1992-1-1:2004)",
        "inputs": [
          {
            "label": "C_{Rd,c}",
            "type": "dimensionless",
            "default_unit": "factor",
            "desc": "Empirical factor for shear resistance (recommended value 0.18/\\gamma_c)"
          },
          {
            "type": "dimensionless",
            "default_unit": "factor",
            "label": "k",
            "desc": "Size effect factor: $k = 1 + \\sqrt{\\frac{200}{d}} \\leq 2.0$ with $d$ in mm"
          },
          {
            "type": "dimensionless",
            "default_unit": "factor",
            "label": "\\rho_l",
            "desc": "Longitudinal reinforcement ratio $\\rho_l = \\frac{A_{sl}}{b_w d} \\leq 0.02$"
          },
          {
            "type": "stress",
            "default_unit": "MPa",
            "label": "f_{ck}",
            "desc": "Characteristic compressive strength of concrete in MPa"
          },
          {
            "type": "dimensionless",
            "default_unit": "factor",
            "label": "k_1",
            "desc": "Factor for normal stress contribution (recommended value 0.15)"
          },
          {
            "type": "stress",
            "default_unit": "MPa",
            "label": "\\sigma_{cp}",
            "desc": "Normal stress due to axial force $\\sigma_{cp} = \\frac{N_{Ed}}{A_c} < 0.2 f_{cd}$ in MPa"
          },
          {
            "type": "length",
            "default_unit": "mm",
            "label": "b_w",
            "desc": "Smallest width of cross-section in tensile area in mm"
          },
          {
            "type": "length",
            "default_unit": "mm",
            "label": "d",
            "desc": "Effective depth of cross-section in mm"
          },
          {
            "type": "stress",
            "default_unit": "MPa",
            "label": "v_{min}",
            "desc": "Minimum shear strength (default: $0.035 k^{3/2} f_{ck}^{1/2}$)"
          }
        ],
        "outputs": [
          {
            "label": "V_{Rd,c}",
            "type": "force",
            "default_unit": "N",
            "desc": "Design value of the shear resistance in N"
          }
        ],
        "pythonFunctionDef": {
          "name": "calculate_shear_resistance",
          "args": [
            {
              "arg": "CRd_c",
              "type": "float"
            },
            {
              "arg": "k",
              "type": "float"
            },
            {
              "arg": "rho_l",
              "type": "float"
            },
            {
              "arg": "fck",
              "type": "float"
            },
            {
              "arg": "k1",
              "type": "float"
            },
            {
              "arg": "sigma_cp",
              "type": "float"
            },
            {
              "arg": "bw",
              "type": "float"
            },
            {
              "arg": "d",
              "type": "float"
            },
            {
              "arg": "vmin",
              "type": "float"
            }
          ],
          "body": "VRd_c1 = (CRd_c * k * (100 * rho_l * fck)**(1/3) + k1 * sigma_cp) * bw * d\nVRd_c2 = (vmin + k1 * sigma_cp) * bw * d\nVRd_c = max(VRd_c1, VRd_c2)\nreturn VRd_c",
          "returnType": "float"
        }
      }
    }
]
"""

origin_json_flow = """
{
  "data": [
    {
      "id": "CRd_c",
      "schemaId": "BSEN1992::6.2.2::CRd_c",
      "inputs": [
        {
          "type": "value",
          "value": {
            "name": "gamma_c",
            "unit": "factor",
            "value": 1.2
          }
        }
      ]
    },
    {
      "id": "k",
      "schemaId": "BSEN1992::6.2.2::k",
      "inputs": [
        {
          "type": "value",
          "value": {
            "name": "d",
            "unit": "mm",
            "value": 450
          }
        }
      ]
    },
    {
      "id": "v_min",
      "schemaId": "BSEN1992::6.2.2::v_min",
      "inputs": [
        {
          "type": "value",
          "value": {
            "name": "k",
            "unit": "dimensionless",
            "value": 1.667
          }
        },
        {
          "type": "value",
          "value": {
            "name": "f_ck",
            "unit": "MPa",
            "value": 40
          }
        }
      ]
    },
    {
      "id": "rho_l",
      "schemaId": "BSEN1992::6.2.2::rho_l",
      "inputs": [
        {
          "type": "value",
          "value": {
            "name": "A_sl",
            "unit": "mm2",
            "value": 1000
          }
        },
        {
          "type": "value",
          "value": {
            "name": "b_w",
            "unit": "mm",
            "value": 300
          }
        },
        {
          "type": "value",
          "value": {
            "name": "d",
            "unit": "mm",
            "value": 450
          }
        }
      ]
    },
    {
      "id": "sigma_cp",
      "schemaId": "BSEN1992::6.2.2::sigma_cp",
      "inputs": [
        {
          "type": "value",
          "value": {
            "name": "N_Ed",
            "unit": "N",
            "value": 100000
          }
        },
        {
          "type": "value",
          "value": {
            "name": "A_c",
            "unit": "mm2",
            "value": 100000
          }
        },
        {
          "type": "value",
          "value": {
            "name": "f_cd",
            "unit": "MPa",
            "value": 100
          }
        }
      ]
    },
    {
      "id": "V_Rd_c",
      "schemaId": "BSEN1992::6.2.2::V_Rd_c",
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
          "type": "value",
          "value": {
            "name": "f_ck",
            "unit": "MPa",
            "value": 40
          }
        },
        {
          "type": "value",
          "value": {
            "name": "k_1",
            "unit": "dimensionless",
            "value": 0.15
          }
        },
        {
          "type": "edge",
          "id": "sigma_cp",
          "index": 0
        },
        {
          "type": "value",
          "value": {
            "name": "b_w",
            "unit": "mm",
            "value": 300
          }
        },
        {
          "type": "value",
          "value": {
            "name": "d",
            "unit": "mm",
            "value": 450
          }
        },
        {
          "type": "edge",
          "id": "v_min",
          "index": 0
        }
      ]
    }
  ],
  "sendBroadcastData": false,
  "options": {}
}
"""

ntc_2018_text = """
#4.1.2.3.5 Resistance to Shear Stresses
##Section Route:
ntc2018 -> CHAPTER 4. -> 4.1. CONCRETE STRUCTURES -> 4.1.2. LIMIT STATE VERIFICATIONS -> 4.1.2.3 ULTIMATE LIMIT STATES -> 4.1.2.3.5 Resistance to Shear Stresses
##Section Page Number:
83~85
##Section Content:
Without excluding the possibility of specific studies, for the evaluation of the ultimate resistances of one-dimensional elements against shear stresses and the ultimate resistances for punching, the following must be considered.

4.1.2.3.5.1 Elements without shear-resistant transverse reinforcements
If, based on calculations, shear reinforcement is not required, a minimum reinforcement must still be provided as specified in point 4.1.6.1.1.1. It is permissible to omit such minimum reinforcement in elements such as slabs, plates, and members with similar behavior, provided that a transverse distribution of loads is ensured.

The resistance verification (ULS) is expressed as
\\(V_{Rd} \\geq V_{Ed}\\) \\hspace{4em} [4.1.22]
where \\(V_{Ed}\\) is the design value of the acting shear force.
\\(v_{Rd}= \\max \\left\\lbrace \\left\\lbrace 0.18 \\cdot k \\cdot (100 \\cdot \\rho_l \\cdot f_{ck})^{1/3}/\\gamma_c + 0.15 \\cdot \\sigma_{cp} \\right\\rbrace \\cdot b_w \\cdot d ; \\left\\lbrace v_{min} + 0.15 \\cdot \\sigma_{cp} \\right\\rbrace \\cdot b_w d \\right\\rbrace \\quad [4.1.23]\\)

with

\\(f_{ck}\\) expressed in MPa
\\(k = 1 + (200/d)^{1/2} \\leq 2\\)
\\(v_{min} = 0.035k^{3/2} f_{ck}^{1/2}\\)
and where

\\(d\\) is the effective depth of the section (in mm);
\\(\\rho_l = A_{sl} / (b_w \\cdot d)\\) is the geometric ratio of tensile longitudinal reinforcement (\\(\\leq 0.02\\)) extending for no less than \\((l_{bd} + d)\\) beyond the considered section, where \\(l_{bd}\\) is the anchorage length;
\\(\\sigma_{cp} = N_{Ed}/A_c\\) [MPa] is the average compressive stress in the section (\\(\\leq 0.2 \\ f_{cd}\\));
\\(b_w\\) is the minimum width of the section (in mm).

In the case of simply supported prestressed reinforced concrete elements, in uncracked zones due to bending moment (with tensile stresses not exceeding \\(f_{ctd}\\)), the design resistance can be simplistically evaluated with the formula:

\\(V_{Rd} = 0.7 \\cdot b_w \\cdot d \\cdot (f_{ctd} \\ + \\sigma_{cp} \\ + \\ f_{ctd})^{1/3} \\quad [4.1.24]\\)

In the presence of significant tensile stresses, the shear resistance of the concrete is considered null, and in such cases, elements without transverse reinforcement cannot be used.

Longitudinal reinforcements, in addition to absorbing stresses resulting from bending, must absorb those caused by shear due to the inclination of cracks with respect to the beam axis, assumed to be 45°. In particular, at supports, longitudinal reinforcements must absorb a force equal to the shear at the support.

4.1.2.3.5.2 Elements with shear-resistant transverse reinforcements
The design shear resistance \\(V_{Rd}\\) of structural elements equipped with specific shear reinforcement must be evaluated based on an appropriate truss model. The resisting elements of the ideal truss are: the transverse reinforcements, the longitudinal reinforcements, the compressed concrete chord, and the inclined web struts. The inclination \\(\\theta\\) of the concrete struts with respect to the beam axis must respect the following limits:
\\(1 \\le ctg \\ \\theta \\le 2.5 \\hspace{50mm} [4.1.25]\\)
The resistance verification (ULS) is expressed as
\\(V_{Rd} \\ge V_{Ed} \\hspace{50mm} [4.1.26]\\)
where \\(V_{Ed}\\) is the design value of the acting shear force.
With reference to the transverse reinforcement, the design resistance to \"shear tension\" is calculated with:
\\(V_{Rsd} = 0.9 \\cdot d \\cdot \\frac{A_{sw}}{s} \\cdot f_{yd} \\cdot (ctg \\ \\alpha + ctg \\ \\theta) \\cdot sin \\ \\alpha \\hspace{50mm} [4.1.27]\\)
With reference to the web concrete, the design resistance to \"shear compression\" is calculated with
\\(V_{Rcd} = 0.9 \\cdot d \\cdot b_w \\cdot \\alpha_c \\cdot v \\cdot f_{cd} (ctg \\ \\alpha + ctg \\ \\theta) / (1 + ctg^2 \\ \\theta) \\hspace{50mm} [4.1.28]\\)
The design shear resistance of the beam is the lesser of the two defined above:
\\(V_{Rd} = min (V_{Rsd}, \\ V_{Rcd}) \\hspace{50mm} [4.1.29]\\)
where \\(d\\), \\(b_w\\), and \\(\\sigma_{cp}\\) have the meanings indicated in \\S 4.1.2.3.5.1. Additionally, it is assumed:
\\(A_{sw}\\) area of the transverse reinforcement;
\\(s\\) spacing between two consecutive transverse reinforcements;
\\(\\alpha\\) angle of inclination of the transverse reinforcement with respect to the beam axis;
\\(v f_{cd}\\) reduced design compressive resistance of the web concrete (v = 0.5);
\\(\\alpha_c\\) enhancement coefficient equal to 1 \\hspace{10mm} for non-compressed members
\\(1 + \\frac{\\sigma_{cp}}{f_{cd}}\\) for \\(0 \\le \\sigma_{cp} < 0.25 \\ f_{cd}\\)
\\(1.25\\) for \\(0.25 \\ f_{cd} \\le \\sigma_{cp} \\le 0.5 \\ f_{cd}\\)
\\(2.5 (1 - \\frac{\\sigma_{cp}}{f_{cd}})\\) for \\(0.5 \\ f_{cd} < \\sigma_{cp} \\le f_{cd}\\)

Longitudinal reinforcements must be sized based on the flexural stresses obtained by shifting the bending moment diagram by

\\(a_{1} = \\left( 0.9 \\cdot d \\cdot \\cot{\\theta} \\right) / 2 \\hspace{1cm} \\left[4.1.30\\right]\\)

along the beam axis, in the least favorable direction.

4.1.2.3.5.3 Special Cases

Transverse Components
In the case of elements with variable height or with inclined prestressing cables, the design shear is assumed to be:
\\hspace{8cm} \\(V_{Ed} = V_{d} + V_{md} + V_{pd} \\hspace{0.75cm} \\left[4.1.31\\right]\\)

where:
\\(V_{d}\\) = design value of the shear due to external loads;
\\(V_{md}\\) = design value of the shear component due to the inclination of the member edges;
\\(V_{pd}\\) = design value of the shear component due to prestressing.

Loads Near Supports
The shear at the support determined by loads applied at a distance \\(a_{v} \\leq 2d\\) from the support itself can be reduced by the ratio \\(a_{v}/2d\\), with the following prescriptions:

in the case of an end support, the tensile reinforcement required in the section where the load closest to the support is applied must be extended and anchored beyond the theoretical support axis;

in the case of an intermediate support, the tensile reinforcement at the support must be extended as necessary and in any case up to the section where the farthest load within the zone with \\(a_{v} \\leq 2d\\) is applied.

In the case of elements with shear-resistant transverse reinforcements, it must be verified that the shear force \\(V_{Ed}\\) calculated in this way satisfies the condition
\\hspace{4cm} \\(V_{Ed} \\leq A_{s} \\cdot f_{yd} \\cdot \\sin{\\alpha} \\hspace{0.75cm} \\left[4.1.32\\right]\\)

where \\(A_{s} f_{yd}\\) is the resistance of the transverse reinforcement contained in the length zone \\(0.75 a_{v}\\) centered between the load and the support and crossing the inclined shear crack included therein.

The shear force \\(V_{Ed}\\) calculated without the reduction \\(a_v/2d\\) must always satisfy the condition: \\(V_{Ed} \\leq 0.5\\, b_w \\, d \\, \\sqrt{f_{cd}} \\quad \\quad [4.1.33]\\) with \\(v = 0.5\\) being a reduction coefficient of the cracked concrete shear resistance.

Hanging or Indirect Loads
If due to particular load application methods the stresses of the tensile elements of the truss are increased, the reinforcements must be appropriately adjusted.

4.1.2.3.5.4 Punching Verification
Solid slabs, ribbed slabs with a solid section above columns, and foundations must be verified for punching at the ultimate limit state, at the columns and concentrated loads.

In the absence of specifically designed transverse reinforcement, the punching resistance must be evaluated using formulas of proven reliability, based on the tensile strength of the concrete, considering the stress distributed over an effective perimeter located 2d from the loaded footprint, with d being the effective (average) depth of the slab.

If, based on calculations, the tensile strength of the concrete on the effective perimeter is insufficient to provide the required punching resistance, specific shear reinforcements must be inserted. These reinforcements must extend to the outermost perimeter where the tensile strength of the concrete is sufficient. For the evaluation of punching resistance, reference can be made to § 6.4.4 of the UNI EN1992-1-1 standard in the absence of shear reinforcements, and to § 6.4.5 of the UNI EN1992-1-1 standard in the presence of shear reinforcements.

In the case of foundations, appropriate adaptations of the above model will be adopted.
"""

#tgt_text = origin_text
tgt_text = ntc_2018_text

if __name__ == "__main__":
    for i in range(2):
        if i == 0:
            origin_json = origin_json_component
        else:
            origin_json = origin_json_flow
        # 사용자 질문 정의
        user_input = f"""
        A라는 설계기준 본문을 제공하겠습니다. 또한 B라는 JSON 형태를 제공할 텐데, B는 A를 기반으로 생성된 것입니다. A와 B의 내용과 규칙을 이해하고, C를 제공할 예정입니다. C를 바탕으로 D라는 JSON을 만들어 주세요.
        1. A는 설계기준 문서이므로, 문서에 포함된 각 항목을 분석하여 이를 JSON 형식으로 변환하는 규칙을 이해해야 합니다.
        2. B는 A의 내용에서 추출된 JSON 형식이며, A에서 B로 변환된 방식과 규칙을 반영합니다.
        3. C는 A의 기준을 따르되, B의 구조에 맞게 변환해야 할 새로운 데이터를 포함하고 있습니다.
        4. D는 C의 데이터를 바탕으로 JSON 형식으로 작성되어야 하며, B에서 사용된 규칙을 그대로 적용해야 합니다.
        이 과정에서 중요한 점은, B의 JSON 구조와 그 안의 데이터가 A의 설계기준을 정확히 반영하는 방식으로 변환되었음을 이해하는 것입니다. C를 제공하면, 이를 D라는 JSON 형식으로 정확히 변환해 주세요.

        A 설계기준 본문:
        {origin_text}


        B JSON 형식:
        {origin_json}


        C 설계기준 본문:
        {tgt_text}

        #참고사항
        결과는 json 형식으로만 반환해 주세요.
        틀린경우 패널티를 부과 합니다.
        응답하기전에 맞는지 한번 더 확인해 주세요.
        """

        # GPT-4 모델로 요청 보내기
        temperature = 0.1  # 원하는 온도 설정

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                    "content": "당신은 설계기준으로 부터 json 형식으로 변환하는 프로그램을 만들어주는 전문가입니다. 아래 질문에 대한 답변을 만들어주세요."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.1
        )
        res = response.choices[0].message.content

        # 현재 시간을 파일명에 포함하여 저장
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if i == 0:
            filename = f"response_component_{current_time}.json"
        else:
            filename = f"response_flow_{current_time}.json"

        # 응답을 JSON 파일로 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(res)

        print(f"응답이 {filename}에 저장되었습니다.")
