from __future__ import annotations

import re
from pint import UnitRegistry

# ------------------------------------------------------------------------------
# Unit Conversion wrapper
# ------------------------------------------------------------------------------

ureg = UnitRegistry()
ureg.define("psia = psi")
ureg.define("psid = psi")
ureg.define("gpm = gal/min")
ureg.define("lbm = lb")


def convert(value: float, in_units: str, out_units: str):
    """
    Converts a unit from in_units to out_units
    Compatible Strings: https://github.com/hgrecco/pint/blob/master/pint/default_en.txt
    """
    if in_units == out_units:
        return value

    _u = ureg.Quantity(value, in_units)

    return _u.to(out_units).magnitude


def get_brack_units(string: str):
    """
    Returns the units inside the first []
    """
    return re.findall(r"\[(.*?)\]", string)[0]


def string_to_imperial(string: str):

    def replace(match):

        string = match.group(0)
        if string == "[watt/(m*degK)]":
            return string.replace("watt/(m*degK)", "Btu/(hr*ft*degF)")

        if "m" in string:
            string = re.sub(r"\bm\b", "in", string)

        if "kg" in string:
            string = string.replace("kg", "lbm")

        if "N" in string:
            string = string.replace("N", "lbf")

        if "J" in string:
            string = string.replace("J", "ft*lbf")

        if "degK" in string:
            string = string.replace("degK", "degF")

        if "Pa" in string:
            string = string.replace("Pa", "psia")

        if "watt" in string:
            string = string.replace("watt", "ft*lbf/s")

        return string

    # Replace the text within brackets based on different conditions
    return re.sub(r"\[.*?\]", replace, string)

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# Standard Constants
# Source:https://en.wikipedia.org/wiki/Standard_temperature_and_pressure
STD_G_MPS2 = 9.80665
STD_ATM_PA = 101_325
STD_ATM_K = 288.15
R_JPDEGK_MOL = 8.31446261815324