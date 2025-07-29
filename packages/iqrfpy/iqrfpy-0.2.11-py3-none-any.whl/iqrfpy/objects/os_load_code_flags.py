"""OS Load Code flags param class."""
from iqrfpy.utils.dpa import OsLoadCodeAction, OsLoadCodeType


class OsLoadCodeFlags:
    """OS Load Code flags class."""
    __slots__ = '_action', '_code_type'

    def __init__(self, action: OsLoadCodeAction, code_type: OsLoadCodeType):
        """Load Code flags constructor.

        Args:
            action (OsLoadCodeAction): Load code action.
            code_type (OsLoadCodeType): Load code code type.
        """
        self._action = action
        self._code_type = code_type

    @property
    def action(self) -> OsLoadCodeAction:
        """:obj:`OsLoadCodeAction`: Load Code action.

        Getter and setter.
        """
        return self._action

    @action.setter
    def action(self, value: OsLoadCodeAction):
        self._action = value

    @property
    def code_type(self) -> OsLoadCodeType:
        """:obj:`OsLoadCodeType`: Load Code code type.

        Getter and setter.
        """
        return self._code_type

    @code_type.setter
    def code_type(self, value: OsLoadCodeType):
        self._code_type = value

    def serialize(self) -> int:
        """Serialize flags into an integer value.

        Returns:
            :obj:`int`: Flags value.
        """
        return self._action | (self._code_type << 1)
