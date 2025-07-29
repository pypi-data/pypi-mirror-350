"""IO Triplet parameters."""
from typing import Union
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.dpa import BYTE_MIN, BYTE_MAX, IoConstants


class IoTriplet:
    """IO Triplet parameter class."""

    __slots__ = '_port', '_mask', '_value'

    def __init__(self, port: Union[IoConstants, int], mask: int, value: int):
        """IO Triplet constructor.

        Args:
            port (Union[IoConstants, int]): Port number.
            mask (int): Port pin mask.
            value (int): Value to write.
        """
        self._validate(port=port, mask=mask, value=value)
        self._port = port
        self._mask = mask
        self._value = value

    def _validate(self, port: int, mask: int, value: int):
        """Validate IO triplet parameters.

        Args:
            port (int): Port number.
            mask (int): Port pin mask.
            value (int): Value to write.
        """
        self._validate_port(port=port)
        self._validate_mask(mask=mask)
        self._validate_value(value=value)

    @staticmethod
    def _validate_port(port: Union[IoConstants, int]):
        """Validate port number.

        Args:
            port (Union[IoConstants, int]): Port number.

        Raises:
            RequestParameterInvalidValueError: If port is less than 0 or greater than 255.
        """
        if not BYTE_MIN <= port <= BYTE_MAX:
            raise RequestParameterInvalidValueError('Port should be between 0 and 255.')

    @property
    def port(self) -> Union[IoConstants, int]:
        """:obj:`int` or :obj:`IoConstants`: Port number.

        Getter and setter.
        """
        return self._port

    @port.setter
    def port(self, val: Union[IoConstants, int]):
        self._validate_port(port=val)
        self._value = val

    @staticmethod
    def _validate_mask(mask: int):
        """Validate port pin mask.

        Args:
            mask (int): Port pin mask.

        Raises:
            RequestParameterInvalidValueError: If mask is less than 0 or greater than 255.
        """
        if not BYTE_MIN <= mask <= BYTE_MAX:
            raise RequestParameterInvalidValueError('Mask should be between 0 and 255.')

    @property
    def mask(self) -> int:
        """:obj:`int`: Port pin mask.

        Getter and setter.
        """
        return self._mask

    @mask.setter
    def mask(self, val: int):
        self._validate_mask(mask=val)
        self._mask = val

    @staticmethod
    def _validate_value(value: int):
        """Validate value to write.

        Args:
            value (int): Value to write.

        Raises:
            RequestParameterInvalidValueError: If value is less than 0 or greater than 255.
        """
        if not BYTE_MIN <= value <= BYTE_MAX:
            raise RequestParameterInvalidValueError('Value should be between 0 and 255.')

    @property
    def value(self) -> int:
        """:obj:`int`: Value to write.

        Getter and setter.
        """
        return self._value

    @value.setter
    def value(self, val: int):
        self._validate_value(value=val)
        self._value = val
