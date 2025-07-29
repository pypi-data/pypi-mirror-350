from .units import LENGTH, WEIGHT, AREA


def convert_length(value : float, from_unit : str, to_unit : str) -> float:
    """
    Converts units of length.
    Parameters:
        value (float): Numeric value for conversion
        from_unit (str): Reference unit of measure (e.g. 'mile')
        to_unit (str): Target unit of measure (e.g. 'kilometer')
    Returns:
        float: Conversion result
    Examples:
        >>> convert_length(1, "mile", "kilometer")
        1.609344
        >>> convert_length(100, "meter", "foot")
        328.084
    """
    if from_unit not in LENGTH:
        raise ValueError(f"'{from_unit}' is unknown unit. Available: {', '.join(LENGTH.keys())}")
    if to_unit not in LENGTH:
        raise ValueError(f"'{to_unit}' is unknown unit. Available: {', '.join(LENGTH.keys())}")
    return value * LENGTH[from_unit] / LENGTH[to_unit]


def convert_weight(value: float, from_unit : str, to_unit : str) -> float:
    """
    Converts units of weight.
    Parameters:
        value (float): Numeric value for conversion
        from_unit (str): Reference unit of measure (e.g. 'gram')
        to_unit (str): Target unit of measure (e.g. 'kilogram')
    Returns:
        float: Conversion result
    Examples:
        >>> convert_weight(1, "gram", "kilogram")
        0.001
        >>> convert_length(100, "kilogram", "gram")
        100000.0
    """
    if from_unit not in WEIGHT:
        raise ValueError(f"'{from_unit}' is unknown unit. Available: {', '.join(WEIGHT.keys())}")
    if to_unit not in WEIGHT:
        raise ValueError(f"'{to_unit}' is unknown unit. Available: {', '.join(WEIGHT.keys())}")
    return value * WEIGHT[from_unit] / WEIGHT[to_unit]


def convert_area(value : float, from_unit : str, to_unit : str) -> float:
    """
    Converts units of area.
    Parameters:
        value (float): Numeric value for conversion
        from_unit (str): Reference unit of measure (e.g. 'acre')
        to_unit (str): Target unit of measure (e.g. 'hectare')
    Returns:
        float: Conversion result
    Examples:
        >>> convert_area(1, "acre", "meter")
        4046.8564224
        >>> convert_area(100, "foot", "meter")
        9.290304
    """
    if from_unit not in AREA:
        raise ValueError(f"'{from_unit}' is unknown unit. Available: {', '.join(AREA.keys())}")
    if to_unit not in AREA:
        raise ValueError(f"'{to_unit}' is unknown unit. Available: {', '.join(AREA.keys())}")
    return value * AREA[from_unit] / AREA[to_unit]