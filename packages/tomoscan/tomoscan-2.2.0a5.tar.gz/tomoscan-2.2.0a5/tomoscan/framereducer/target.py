from silx.utils.enum import Enum as _Enum


class REDUCER_TARGET(_Enum):
    """
    type of frame to reduce
    """

    DARKS = "darks"
    FLATS = "flats"
