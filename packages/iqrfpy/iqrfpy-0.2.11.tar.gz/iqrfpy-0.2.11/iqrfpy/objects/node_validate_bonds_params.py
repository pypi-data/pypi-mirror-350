"""Node Validate Bonds parameters."""
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants


class NodeValidateBondsParams:
    """Node Validate Bonds parameters class."""

    __slots__ = '_bond_addr', '_mid'

    def __init__(self, bond_addr: int, mid: int):
        """Validate Bonds parameters constructor.

        Args:
            bond_addr (int): Node device address.
            mid (int): Node module ID.
        """
        self._validate(bond_addr=bond_addr, mid=mid)
        self._bond_addr = bond_addr
        self._mid = mid

    def _validate(self, bond_addr: int, mid: int):
        """Validate parameters.

        Args:
            bond_addr (int): Node device address.
            mid (int): Node module ID.
        """
        self._validate_bond_addr(bond_addr)
        self._validate_mid(mid)

    @staticmethod
    def _validate_bond_addr(bond_addr: int):
        """Validate node device address parameter.

        Args:
            bond_addr (int): Node device address.

        Raises:
            RequestParameterInvalidValueError: If bond_addr is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= bond_addr <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Bond address value should be between 0 and 255.')

    @property
    def bond_addr(self) -> int:
        """:obj:`int`: Node device address.

        Getter and setter.
        """
        return self._bond_addr

    @bond_addr.setter
    def bond_addr(self, value: int):
        self._validate_bond_addr(value)
        self._bond_addr = value

    @staticmethod
    def _validate_mid(mid: int):
        """Validate module ID parameter.

        Args:
            mid (int): Node module ID.

        Raises:
            RequestParameterInvalidValueError: If mid is less than 0 or greater than 4294967295.
        """
        if not dpa_constants.MID_MIN <= mid <= dpa_constants.MID_MAX:
            raise RequestParameterInvalidValueError('MID value should be an unsigned 32bit integer.')

    @property
    def mid(self):
        """:obj:`int`: Module ID.

        Getter and setter.
        """
        return self._mid

    @mid.setter
    def mid(self, value):
        self._validate_mid(value)
        self._mid = value
