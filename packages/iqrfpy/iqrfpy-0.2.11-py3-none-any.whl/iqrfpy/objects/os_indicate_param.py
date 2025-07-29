"""OS Indicate param class."""
from iqrfpy.utils.enums import IntEnumMember


class OsIndicateParam(IntEnumMember):
    """OS Indicate control params enum."""

    OFF = 0
    ON = 1
    INDICATE_1S = 2
    INDICATE_10S = 3
