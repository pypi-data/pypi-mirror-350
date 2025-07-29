"""Coordinator Authorize Bond parameters."""
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants


class CoordinatorAuthorizeBondParams:
    """AuthorizeBondParams class.

    Parameters for AuthorizeBond request. Each object represents a single
    pair of device address and MID.
    """

    __slots__ = '_req_addr', '_mid'

    def __init__(self, req_addr: int, mid: int):
        """AuthorizeBondParams constructor.

        Args:
            req_addr (int): Device address
            mid (int): Module ID
        """
        self._validate(req_addr=req_addr, mid=mid)
        self._req_addr = req_addr
        self._mid = mid

    def _validate(self, req_addr: int, mid: int):
        """Validates pair parameters.

        Args:
            req_addr (int): Requested node address.
            mid (int): Module ID.
        """
        self._validate_req_addr(req_addr=req_addr)
        self._validate_mid(mid=mid)

    @staticmethod
    def _validate_req_addr(req_addr: int):
        """Validates requested node address.

        Args:
            req_addr (int): Requested node address.

        Raises:
            RequestParameterInvalidValueError: If req_addr is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= req_addr <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Requested address value should be between 1 and 239.')

    @property
    def req_addr(self) -> int:
        """:obj:`int`: Requested node address.

        Getter and setter.
        """
        return self._req_addr

    @req_addr.setter
    def req_addr(self, value: int):
        self._validate_req_addr(req_addr=value)
        self._req_addr = value

    @staticmethod
    def _validate_mid(mid: int):
        """Validates module ID.

        Args:
            mid (int): Module ID.

        Raises:
            RequestParameterInvalidValueError: If mid is less than 0 or greater than 4294967295.
        """
        if not dpa_constants.MID_MIN <= mid <= dpa_constants.MID_MAX:
            raise RequestParameterInvalidValueError('MID value should be an unsigned 32bit integer.')

    @property
    def mid(self) -> int:
        """:obj:`int`: Module ID.

        Getter and setter.
        """
        return self._mid

    @mid.setter
    def mid(self, value: int):
        self._validate_mid(mid=value)
        self._mid = value
