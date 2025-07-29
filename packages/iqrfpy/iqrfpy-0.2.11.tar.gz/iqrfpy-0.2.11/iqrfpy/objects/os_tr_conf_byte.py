"""OS Batch Data parameters."""
from typing import List
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants


class OsTrConfByte:
    """TR Configuration Byte class."""

    __slots__ = '_address', '_value', '_mask'

    def __init__(self, address: int, value: int, mask: int):
        """TR Configuration Byte constructor.

        Args:
            address (int): Configuration memory block address.
            value (int): Value to set.
            mask (int): Bits of configuration byte to modify.
        """
        self._validate(address=address, value=value, mask=mask)
        self._address = address
        self._value = value
        self._mask = mask

    def __eq__(self, other: 'OsTrConfByte'):
        """Rich comparison method, comparing this and another object to determine equality based on properties.

        Args:
            other (OsTrConfByte): Object to compare with.

        Returns:
            bool: True if the objects are equivalent, False otherwise.
        """
        return self.address == other.address and \
            self.value == other.value and \
            self.mask == other.mask

    def _validate(self, address: int, value: int, mask: int):
        """Validate TR Configuration Byte parameters.

        Args:
            address (int): Configuration memory block address.
            value (int): Value to set.
            mask (int): Bits of configuration byte to modify.
        """
        self._validate_address(address=address)
        self._validate_value(value=value)
        self._validate_mask(mask=mask)

    @staticmethod
    def _validate_address(address: int):
        """Validate address parameter.

        Args:
            address (int): Configuration memory block address.

        Raises:
            RequestParameterInvalidValueError: If address is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= address <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Address value should be between 0 and 255.')

    @property
    def address(self) -> int:
        """:obj:`int`: Configuration memory block address.

        Getter and setter.
        """
        return self._address

    @address.setter
    def address(self, value: int):
        self._validate_address(address=value)
        self._address = value

    @staticmethod
    def _validate_value(value: int):
        """Validate value parameter.

        Args:
            value (int): Value to set.

        Raises:
            RequestParameterInvalidValueError: If value is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= value <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Value should be between 0 and 255.')

    @property
    def value(self) -> int:
        """:obj:`int`: Value to set.

        Getter and setter.
        """
        return self._value

    @value.setter
    def value(self, val: int):
        self._validate_value(value=val)
        self._value = val

    @staticmethod
    def _validate_mask(mask: int):
        """Validate mask parameter.

        Args:
            mask (int): Bits of configuration byte to modify.

        Raises:
            RequestParameterInvalidValueError: If mask is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= mask <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Mask value should be between 0 and 255.')

    @property
    def mask(self) -> int:
        """:obj:`int`: Bits of configuration byte to modify.

        Getter and setter.
        """
        return self._mask

    @mask.setter
    def mask(self, value: int):
        self._validate_mask(mask=value)
        self._mask = value

    def to_pdata(self) -> List[int]:
        """Serialize TR configuration byte members into pdata.

        Returns:
            :obj:`list` of :obj:`int`: Serialized TR configuration byte pdata.
        """
        return [self._address, self._value, self._mask]

    def to_json(self) -> dict:
        """Serialize TR configuration byte members into JSON.

        Returns:
            :obj:`dict`: Serialized TR configuration byte JSON request data.
        """
        return {
            'address': self._address,
            'value': self._value,
            'mask': self._mask
        }
