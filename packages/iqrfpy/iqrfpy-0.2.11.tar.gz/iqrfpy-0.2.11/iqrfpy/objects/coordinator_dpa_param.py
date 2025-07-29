"""Coordinator Set DPA param param class."""
from enum import IntEnum


class CoordinatorDpaParam(IntEnum):
    """DpaParam class.

    Parameters for SetDpaParams request.
    """
    LAST_RSSI = 0
    VOLTAGE = 1
    SYSTEM = 2
    USER_SPECIFIED = 3
