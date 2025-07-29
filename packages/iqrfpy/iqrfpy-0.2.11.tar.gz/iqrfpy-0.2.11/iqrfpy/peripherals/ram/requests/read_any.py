"""RAM Read Any request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import RAMRequestCommands
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['ReadAnyRequest']


class ReadAnyRequest(IRequest):
    """RAM Read Any request class."""

    __slots__ = '_address', '_length'

    def __init__(self, nadr: int, address: int, length: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Read Any request constructor.

        Args:
            nadr (int): Device address.
            address (int): Memory address to read from.
            length (int): Number of bytes to read from memory.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(address, length)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.RAM,
            pcmd=RAMRequestCommands.READ_ANY,
            m_type=None,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._address = address
        self._length = length

    def _validate(self, address: int, length: int) -> None:
        """Validate request parameters.

        Args:
            address (int): Memory address to read from.
            length (int): Number of bytes to read from memory.
        """
        self._validate_address(address)
        self._validate_length(length)

    @staticmethod
    def _validate_address(address: int):
        """Validates memory address parameter.

        Args:
            address (int): Memory address to read from.

        Raises:
            RequestParameterInvalidValueError: If address is less than 0 or greater than 65535.
        """
        if not dpa_constants.WORD_MIN <= address <= dpa_constants.WORD_MAX:
            raise RequestParameterInvalidValueError('Address should be between 0 and 65535.')

    @property
    def address(self) -> int:
        """:obj:`int`: Memory address to read from.

        Getter and setter.
        """
        return self._address

    @address.setter
    def address(self, value: int) -> None:
        self._validate_address(address=value)
        self._address = value

    @staticmethod
    def _validate_length(length: int):
        """Validates data length parameter.

        Args:
            length (int): Number of bytes to read from memory.

        Raises:
            RequestParameterInvalidValueError: If length is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= length <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Length should be between 0 and 255.')

    @property
    def length(self) -> int:
        """:obj:`int`: Number of bytes to read from memory.

        Getter and setter.
        """
        return self._length

    @length.setter
    def length(self, value: int) -> None:
        self._validate_length(length=value)
        self._length = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet, if mutable is True.
        """
        self._pdata = [self._address & 0xFF, (self._address >> 8) & 0xFF, self._length]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        This method is not implemented as the message type is not supported by Daemon.

        Returns:
            :obj:`dict`: JSON API request object.

        Raises:
            NotImplementedError: ReadAny message type not implemented.
        """
        raise NotImplementedError('ReadAny JSON API request not implemented.')
