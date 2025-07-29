"""Eeprom Write request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import EEPROMRequestCommands
from iqrfpy.enums.message_types import EEPROMMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['WriteRequest']


class WriteRequest(IRequest):
    """Eeprom write request class."""

    __slots__ = '_address', '_data'

    def __init__(self, nadr: int, address: int, data: List[int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Write request constructor.

        Args:
            nadr (int): Device address.
            address (int): Memory address to write to.
            data (List[int]): Data to write to memory.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(address, data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.EEPROM,
            pcmd=EEPROMRequestCommands.WRITE,
            m_type=EEPROMMessages.WRITE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._address = address
        self._data = data

    def _validate(self, address: int, data: List[int]) -> None:
        """Validate request parameters.

        Args:
            address (int): Memory address to write to.
            data (List[int]): Data to write to memory.
        """
        self._validate_address(address)
        self._validate_data(data)

    @staticmethod
    def _validate_address(address: int):
        """Validate address parameter.

        Args:
            address (int): Memory address to write to.

        Raises:
            RequestParameterInvalidValueError: If address is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= address <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Address should be between 0 and 255.')

    @property
    def address(self) -> int:
        """:obj:`int`: Memory address to write to.

        Getter and setter.
        """
        return self._address

    @address.setter
    def address(self, value: int) -> None:
        self._validate_address(address=value)
        self._address = value

    @staticmethod
    def _validate_data(data: List[int]):
        """Validate data parameter.

        Args:
            data (List[int]): Data to write to memory.

        Raises:
            RequestParameterInvalidValueError: If data contains more than 55 values or data values are not
                in range from 0 to 255.
        """
        if len(data) > dpa_constants.EEPROM_WRITE_MAX_DATA_LEN:
            raise RequestParameterInvalidValueError('Data should contain at most 55 values.')
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Data values should be between 0 and 255.')

    @property
    def data(self) -> List[int]:
        """:obj:`list` of :obj:`int`: Data to write to memory.

        Getter and setter.
        """
        return self._data

    @data.setter
    def data(self, value: List[int]) -> None:
        self._validate_data(value)
        self._data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        pdata = [self._address]
        pdata.extend(self._data)
        self._pdata = pdata
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'address': self._address, 'pData': self._data}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
