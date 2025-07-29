import moapy.unit_converter
import moapy.dgncodeutil

# about design code
def get_dgnunit_type(dgn_code : str):
    """get the unit type of the design code (US or SI)

    Args:
        dgn_code (str): the design code

    Returns:
        str : "US" or "SI"
    """
    return moapy.dgncodeutil.get_dgnunit_type(dgn_code)

# about unit converter
def convert_length(length : float, from_unit : str, to_unit : str) -> float:
    """get the unit converted length

    Args:
        length (float): _description_
        from_unit (str): _description_
        to_unit (str): _description_

    Returns:
        float: converted length
    """
    uc = moapy.unit_converter.UnitConverter()
    return uc.length(length, from_unit, to_unit)

def convert_area(area : float, from_unit : str, to_unit : str) -> float:
    """get the unit converted area

    Args:
        area (float): _description_
        from_unit (str): _description_
        to_unit (str): _description_

    Returns:
        float: _description_
    """
    uc = moapy.unit_converter.UnitConverter()
    return uc.area(area, from_unit, to_unit)

def convert_force(force : float, from_unit : str, to_unit : str) -> float:
    """get the unit converted force

    Args:
        force (float): _description_
        from_unit (str): _description_
        to_unit (str): _description_

    Returns:
        float: _description_
    """
    uc = moapy.unit_converter.UnitConverter()
    return uc.force(force, from_unit, to_unit)

def convert_stress(stress : float, from_unit : str, to_unit : str) -> float:
    """get the unit converted stress

    Args:
        stress (float): _description_
        from_unit (str): _description_
        to_unit (str): _description_

    Returns:
        float: _description_
    """
    uc = moapy.unit_converter.UnitConverter()
    return uc.stress(stress, from_unit, to_unit)

def convert_moment(moment : float, from_unit : str, to_unit : str) -> float:
    """get the unit converted moment

    Args:
        moment (float): _description_
        from_unit (str): _description_
        to_unit (str): _description_

    Returns:
        float: _description_
    """
    uc = moapy.unit_converter.UnitConverter()
    return uc.moment(moment, from_unit, to_unit)