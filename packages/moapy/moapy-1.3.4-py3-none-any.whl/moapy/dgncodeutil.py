from enum import Enum

class enDgnCode(Enum):
    EN1992_1_1_2004_REC = "EN1992"
    ACI318_19 = "ACI318-19"
    ACI318M_19 = "ACI318M-19"

class enDgnUnit(Enum):
    US = "US"  # kip, inch
    SI = "SI"  # N, mm


code_to_unit = {
    enDgnCode.EN1992_1_1_2004_REC: enDgnUnit.SI,
    enDgnCode.ACI318_19: enDgnUnit.US,
    enDgnCode.ACI318M_19: enDgnUnit.US,
    # Add more mappings as needed
}

def get_dgnunit_type(dgn_code: str) -> str:
    try:
        # Convert the string dgn_code to the corresponding enDgnCode enum
        code_enum = enDgnCode(dgn_code)
        # Get the corresponding unit from the code_to_unit dictionary
        unit_enum = code_to_unit[code_enum]
        # Return the value of the unit enum ("US" or "SI")
        return unit_enum.value
    except KeyError:
        # Handle the case where the dgn_code is not in the code_to_unit dictionary
        raise ValueError(f"Invalid design code: {dgn_code}")
    except ValueError:
        # Handle the case where the dgn_code is not a valid enDgnCode
        raise ValueError(f"Invalid design code: {dgn_code}")

def get_dgn_unit_by_code(dgn_code: enDgnCode) -> enDgnUnit:
    """
    Returns the design unit (US or SI) based on the given design code.

    Args:
        dgn_code (enDgnCode): The design code (e.g., EN1992_1_1_2004_REC, ACI318_19, etc.).

    Returns:
        enDgnUnit: The corresponding design unit (US or SI).
    """
    return code_to_unit.get(dgn_code, enDgnUnit.SI)
