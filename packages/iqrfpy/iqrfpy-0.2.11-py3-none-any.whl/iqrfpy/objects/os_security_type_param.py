"""OS Security type param class."""
from iqrfpy.utils.enums import IntEnumMember


class OsSecurityTypeParam(IntEnumMember):
    """OS Security type enum."""

    ACCESS_PASSWORD = 0
    USER_KEY = 1
