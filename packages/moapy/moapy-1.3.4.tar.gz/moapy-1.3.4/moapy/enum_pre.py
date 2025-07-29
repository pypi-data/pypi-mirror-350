from enum import Enum
from generated.dbase.enum_pre import (
    en_H_EN10365,
    en_H_AISC05_US, en_T_AISC05_US, en_BOX_AISC05_US, en_PIPE_AISC05_US, en_ANGLE_AISC05_US, en_C_AISC05_US,
    en_H_AISC05_SI, en_T_AISC05_SI, en_BOX_AISC05_SI, en_PIPE_AISC05_SI, en_ANGLE_AISC05_SI, en_C_AISC05_SI,
    en_H_AISC16_US, en_T_AISC16_US, en_BOX_AISC16_US, en_PIPE_AISC16_US, en_ANGLE_AISC16_US, en_C_AISC16_US,
    en_H_AISC16_SI, en_T_AISC16_SI, en_BOX_AISC16_SI, en_PIPE_AISC16_SI, en_ANGLE_AISC16_SI, en_C_AISC16_SI,
)
from moapy.api_url import API_SECTION_DATABASE

# Enum 값을 리스트로 변환하는 함수
def enum_to_list(enum_class):
    return [member.value for member in enum_class]

class enUnitSystem(Enum):
    SI = "SI"   # Metric units (e.g., kN, kNm)
    US = "US"   # Imperial units (e.g., kip, kip-ft)

class enUnitLength(Enum):
    MM = "mm"
    CM = "cm"
    M = "m"
    IN = "in"
    FT = "ft"

class enUnitArea(Enum):
    MM2 = "mm^{2}"
    M2 = "m^{2}"
    IN2 = "in^{2}"
    FT2 = "ft^{2}"

class enUnitVolume(Enum):
    MM3 = "mm^{3}"
    M3 = "m^{3}"
    IN3 = "in^{3}"
    FT3 = "ft^{3}"

class enUnitInertia(Enum):
    MM4 = "mm^{4}"
    M4 = "m^{4}"
    IN4 = "in^{4}"
    FT4 = "ft^{4}"

class enUnitForce(Enum):
    N = "N"
    kN = "kN"
    MN = "MN"
    lbf = "lbf"
    kip = "kip"

class enUnitMoment(Enum):
    kNm = "kN.m"
    kipin = "kip.in"
    kipft = "kip.ft"
    Nmm = "N.mm"
    Nm = "N.m"

class enUnitLoad(Enum):
    kN_m2 = "kN/m^{2}"
    kip_ft2 = "kip/ft^{2}"

class enUnitStress(Enum):
    Pa = "Pa"
    KPa = "KPa"
    MPa = "MPa"
    psi = "psi"
    ksi = "ksi"

class enUnitPercentage(Enum):
    pct = "%"         # Percent symbol
    basis100 = "per 100"  # Describes as "per 100"
    parts100 = "in 100"   # Alternative notation "in 100"
    basis1 = "per 1"      # Describes as "per 1"

class enUnitThermalExpansion(Enum):
    """Thermal Expansion Coefficient units"""
    PER_CELSIUS = "1/°C"
    # PER_KELVIN = "1/K"

class enUnitAngle(Enum):
    Degree = "degree"
    Radian = "radian"

class enUnitTemperature(Enum):
    Celsius = "celsius"
    Fahrenheit = "fahrenheit"

class enDgnCode(Enum):
    """
    Enum for Design Code
    """
    ACI318M_19 = "ACI318M-19"
    Eurocode2_04 = "Eurocode2-04"

class enEccPu(Enum):
    """
    Enum for Design Code
    """
    ecc = "ecc"
    p_u = "P-U"

class enReportType(Enum):
    """
    Enum for Report Type
    """
    text = "text"
    markdown = "markdown"

class enMembType(Enum):
    """
    Enum for Member Type
    """
    Beam = "Beam"
    Column = "Column"

# ---- Steel ----
class enInteractionFactor(Enum):
    AnnexA = "kij Method 1 - Annex A"
    AnnexB = "kij Method 2 - Annex B"

class enAnchorType(Enum):
    CIP = "Cast-In-Place"
    POST = "Post-Installed"

class enBoltMaterialEC(Enum):
    Class46 = "4.6"
    Class48 = "4.8"
    Class56 = "5.6"
    Class58 = "5.8"
    Class68 = "6.8"
    Class88 = "8.8"
    Class109 = "10.9"

class enBoltMaterialASTM(Enum):
    A36 = "A36"
    A307 = "A307"
    A325 = "A325"
    A354 = "A354"
    A354_BD = "A354-BD"
    A449 = "A449"
    A490 = "A490"
    A572_42 = "A572-42"
    A572_50 = "A572-50"
    F1554_36 = "F1554-36"
    F1554_55 = "F1554-55"
    F1554_105 = "F1554-105"
    F1852 = "F1852"
    F2280 = "F2280"
    A588 = "A588"
    A36M = "A36M"
    A325M = "A325M"
    A572M_42 = "A572M-42"
    A572M_50 = "A572M-50"
    A588M = "A588M"
    A193_B7 = "A193-B7"
    A193M_B7 = "A193M-B7"

class enAnchorBoltName(Enum):
    _3_8 = "3/8"
    _1_2 = "1/2"
    _5_8 = "5/8"
    _3_4 = "3/4"
    _7_8 = "7/8"
    _1 = "1"
    _1_1_8 = "1-1/8"
    _1_1_4 = "1-1/4"
    _1_3_8 = "1-3/8"
    _1_1_2 = "1-1/2"
    _1_3_4 = "1-3/4"
    _2 = "2"
    _2_1_4 = "2-1/4"
    _2_1_2 = "2-1/2"
    _2_3_4 = "2-3/4"
    _3 = "3"

class enStudBoltName(Enum):
    M6 = "M6"
    M8 = "M8"
    M9 = "M9"
    M13 = "M13"
    M16 = "M16"
    M19 = "M19"
    M22 = "M22"
    M25 = "M25"

class enBoltName(Enum):
    M12 = "M12"
    M16 = "M16"
    M20 = "M20"
    M22 = "M22"
    M24 = "M24"
    M27 = "M27"
    M30 = "M30"
    M36 = "M36"

class enConnectionType(Enum):
    """
    Enum for Connection Type
    """
    Fin_B_B = "Fin Plate - Beam to Beam"
    Fin_B_C = "Fin Plate - Beam to Column"
    End_B_B = "End Plate - Beam to Beam"
    End_B_C = "End Plate - Beam to Column"

class enSteelMaterial_ASTM(Enum):
    A36 = "A36"
    A53 = "A53"
    A242_40 = "A242-40"
    A242_42 = "A242-42"
    A242_46 = "A242-46"
    A242_50 = "A242-50"
    A283_24 = "A283-24"
    A283_27 = "A283-27"
    A283_30 = "A283-30"
    A283_33 = "A283-33"
    A283_36 = "A283-36"
    A500_39 = "A500-39"
    A500_42 = "A500-42"
    A500_46 = "A500-46"
    A500_50 = "A500-50"
    A501 = "A501"
    A514_90 = "A514-90"
    A514_100 = "A514-100"
    A529_42 = "A529-42"
    A529_50 = "A529-50"
    A572_42 = "A572-42"
    A572_50 = "A572-50"
    A572_60 = "A572-60"
    A572_65 = "A572-65"
    A588_40 = "A588-40"
    A588_42 = "A588-42"
    A588_46 = "A588-46"
    A588_50 = "A588-50"
    A606_45 = "A606-45"
    A606_50 = "A606-50"
    A618_50 = "A618-50"
    A709_36 = "A709-36"
    A709_50 = "A709-50"
    A709_50S = "A709-50S"
    A709_50W = "A709-50W"
    A709_HPS50W = "A709-HPS50W"
    A709_HPS70W = "A709-HPS70W"
    A709_100_Thin = "A709-100(Thin)"
    A709_100_Thick = "A709-100(Thick)"
    A709_100W_Thin = "A709-100W(Thin)"
    A709_100W_Thick = "A709-100W(Thick)"
    A847 = "A847"
    A852 = "A852"
    A913_50 = "A913-50"
    A913_60 = "A913-60"
    A913_65 = "A913-65"
    A913_70 = "A913-70"
    A992 = "A992"
    A1011_30 = "A1011-30"
    A1011_33 = "A1011-33"
    A1011_36 = "A1011-36"
    A1011_40 = "A1011-40"
    A1011_45 = "A1011-45"
    A1011_50 = "A1011-50"
    A1011_55 = "A1011-55"
    A1011_60 = "A1011-60"
    A1011_70 = "A1011-70"
    A1011_80 = "A1011-80"

class enSteelMaterial_EN10025(Enum):
    S235 = "S235"
    S275 = "S275"
    S355 = "S355"
    S450 = "S450"
    S275NL = "S275N/NL"
    S355NL = "S355N/NL"
    S420NL = "S420N/NL"
    S460NL = "S460N/NL"
    S275ML = "S275M/ML"
    S355ML = "S355M/ML"
    S420ML = "S420M/ML"
    S460ML = "S460M/ML"
    S235W = "S235W"
    S355W = "S355W"
    S460QL1 = "S460Q/QL/QL1"

class enAluminumMaterial_AA(Enum):
    EN_2014_T6 = "2014-T6"
    EN_2014_T6510 = "2014-T6510"
    EN_2014_T6511 = "2014-T6511"
    EN_5083_H111 = "5083-H111"
    EN_5086_H111 = "5086-H111"
    EN_5454_H111 = "5454-H111"
    EN_5454_H112 = "5454-H112"
    EN_5456_H111 = "5456-H111"
    EN_5456_H112 = "5456-H112"
    EN_6061_T6 = "6061-T6"
    EN_6061_T6511 = "6061-T6511"
    EN_6061_T651O = "6061-T651O"
    EN_6063_T5 = "6063-T5"
    EN_6063_T6 = "6063-T6"

class enRebar_ASTM(Enum):
    D3 = "#3"
    D4 = "#4"
    D5 = "#5"
    D6 = "#6"
    D7 = "#7"
    D8 = "#8"
    D9 = "#9"
    D10 = "#10"
    D11 = "#11"
    D14 = "#14"
    D18 = "#18"

class enRebar_UNI(Enum):
    P4 = "P4"
    P5 = "P5"
    P6 = "P6"
    P8 = "P8"
    P10 = "P10"
    P12 = "P12"
    P14 = "P14"
    P16 = "P16"
    P18 = "P18"
    P20 = "P20"
    P22 = "P22"
    P24 = "P24"
    P26 = "P26"
    P30 = "P30"
    P32 = "P32"
    P36 = "P36"
    P40 = "P40"

class enAnchorBoltType(Enum):
    STUD = "Headed Stud"
    BOLT = "Headed Bolt"
    BOLT_L = "Hooked Bolt-L"
    BOLT_J = "Hooked Bolt-J"

# API에서 SectionNameList 데이터를 받아오는 함수
# def get_section_names_from_api(codes, types):
#     return do_section_names_from_api(API_SECTION_DATABASE, codes, types)

# def do_section_names_from_api(base_url, codes, types):
#     api_url = base_url + f"codes/{codes}/types/{types}/names"
#     response = requests.get(api_url)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("sectionNameList", [])
#     else:
#         raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

# # 동적으로 Enum 클래스를 생성하는 함수
# def create_enum_class(class_name, enum_data):
#     # Enum 이름에 적합한 형식으로 변환 (공백과 특수문자 등을 처리)
#     enum_dict = {name.replace(' ', '_').replace('.', '_'): name for name in enum_data}
#     return Enum(class_name, enum_dict)


# 동적으로 생성된 enum 클래스
# en_H_EN10365 = create_enum_class('en_H_EN10365', get_section_names_from_api("EN 10365:2017", "H_Section"))
# en_H_AISC05_US = create_enum_class('en_H_AISC05_US', get_section_names_from_api("AISC05(US)", "H_Section"))
# en_H_AISC05_SI = create_enum_class('en_H_AISC05_SI', get_section_names_from_api("AISC05(SI)", "H_Section"))
# en_H_AISC10_US = create_enum_class('en_H_AISC10_US', get_section_names_from_api("AISC10(US)", "H_Section"))
# en_H_AISC10_SI = create_enum_class('en_H_AISC10_SI', get_section_names_from_api("AISC10(SI)", "H_Section"))
