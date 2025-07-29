"""OS Load Code request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest
from iqrfpy.objects.os_load_code_flags import OsLoadCodeFlags

__all__ = [
    'LoadCodeRequest',
    'OsLoadCodeFlags',
]


class LoadCodeRequest(IRequest):
    """OS Load Code request class."""

    __slots__ = '_flags', '_address', '_length', '_checksum'

    def __init__(self, nadr: int, flags: Union[OsLoadCodeFlags, int], address: int, length: int, checksum: int,
                 hwpid: int = dpa_constants.HWPID_MAX, dpa_rsp_time: Optional[float] = None,
                 dev_process_time: Optional[float] = None, msgid: Optional[str] = None):
        """Load Code request constructor.

        Args:
            nadr (int): Device address.
            flags (Union[OsLoadCodeFlags, int]): Load code flags.
            address (int): EEEPROM address to load code from.
            length (int): Length of code in bytes to load.
            checksum (int): Fletcher-16 checksum of the code to load.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(flags=flags, address=address, length=length, checksum=checksum)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.LOAD_CODE,
            m_type=OSMessages.LOAD_CODE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._flags = flags
        self._address = address
        self._length = length
        self._checksum = checksum

    def _validate(self, flags: Union[OsLoadCodeFlags, int], address: int, length: int, checksum: int):
        """Validate request parameters.

        Args:
            flags (Union[OsLoadCodeFlags, int]): Load code flags.
            address (int): EEEPROM address to load code from.
            length (int): Length of code in bytes to load.
            checksum (int): Fletcher-16 checksum of the code to load.
        """
        self._validate_flags(flags=flags)
        self._validate_address(address=address)
        self._validate_length(length=length)
        self._validate_checksum(checksum=checksum)

    @staticmethod
    def _validate_flags(flags: Union[OsLoadCodeFlags, int]):
        """Validate flags parameter.

        Args:
            flags (Union[LoadCodeFlags, int]): Load code flags.

        Raises:
            RequestParameterInvalidValueError: If flags is less than 0 or greater than 255.
        """
        if isinstance(flags, OsLoadCodeFlags):
            return
        if not dpa_constants.BYTE_MIN <= flags <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Flags value should be between 0 and 255.')

    @property
    def flags(self) -> Union[OsLoadCodeFlags, int]:
        """:obj:`LoadCodeFlags` or :obj:`int`: Load code flags.

        Getter and setter.
        """
        return self._flags

    @flags.setter
    def flags(self, value: Union[OsLoadCodeFlags, int]):
        self._validate_flags(flags=value)
        self._flags = value

    @staticmethod
    def _validate_address(address: int):
        """Validate address parameter.

        Args:
            address (int): EEEPROM address to load code from.

        Raises:
            RequestParameterInvalidValueError: If address is less than 0 or greater than 65535.
        """
        if not dpa_constants.WORD_MIN <= address <= dpa_constants.WORD_MAX:
            raise RequestParameterInvalidValueError('Address value should be between 0 and 65535.')

    @property
    def address(self) -> int:
        """:obj:`int`: EEEPROM address to load code from.

        Getter and setter.
        """
        return self._address

    @address.setter
    def address(self, value: int):
        self._validate_address(address=value)
        self._address = value

    @staticmethod
    def _validate_length(length: int):
        """Validate length parameter.

        Args:
            length (int): EEEPROM address to load code from.

        Raises:
            RequestParameterInvalidValueError: If length is less than 0 or greater than 65535.
        """
        if not dpa_constants.WORD_MIN <= length <= dpa_constants.WORD_MAX:
            raise RequestParameterInvalidValueError('Length value should be between 0 and 65535.')

    @property
    def length(self) -> int:
        """:obj:`int`: Length of code in bytes to load.

        Getter and setter.
        """
        return self._length

    @length.setter
    def length(self, value: int):
        self._validate_length(length=value)
        self._length = value

    @staticmethod
    def _validate_checksum(checksum: int):
        """Validate address parameter.

        Args:
            checksum (int): Fletcher-16 checksum of the code to load.

        Raises:
            RequestParameterInvalidValueError: If checksum is less than 0 or greater than 65535.
        """
        if not dpa_constants.WORD_MIN <= checksum <= dpa_constants.WORD_MAX:
            raise RequestParameterInvalidValueError('Checksum value should be between 0 and 65535.')

    @property
    def checksum(self) -> int:
        """:obj:`int`: Fletcher-16 checksum of the code to load.

        Getter and setter.
        """
        return self._checksum

    @checksum.setter
    def checksum(self, value: int):
        self._validate_checksum(checksum=value)
        self._checksum = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [
            self._flags.serialize() if isinstance(self._flags, OsLoadCodeFlags) else self._flags,
            self._address & 0xFF,
            (self._address >> 8) & 0xFF,
            self._length & 0xFF,
            (self._length >> 8) & 0xFF,
            self._checksum & 0xFF,
            (self._checksum >> 8) & 0xFF,
        ]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {
            'flags': self._flags.serialize() if isinstance(self._flags, OsLoadCodeFlags) else self._flags,
            'address': self._address,
            'length': self._length,
            'checkSum': self._checksum,
        }
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
