from silx.utils.enum import Enum as _Enum


class Method(_Enum):
    NONE = "none"
    SUBTRACTION = "subtraction"
    DIVISION = "division"
    CHEBYSHEV = "chebyshev"
    LSQR_SPLINE = "lsqr spline"
