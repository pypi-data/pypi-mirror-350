"""UART Clear Write Read request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import UartRequestCommands
from iqrfpy.enums.message_types import UartMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['ClearWriteReadRequest']


class ClearWriteReadRequest(IRequest):
    """UART Clear Write Read request class."""

    __slots__ = '_read_timeout', '_data'

    def __init__(self, nadr: int, read_timeout: int, data: Optional[List[int]] = None,
                 hwpid: int = dpa_constants.HWPID_MAX, dpa_rsp_time: Optional[float] = None,
                 dev_process_time: Optional[float] = None, msgid: Optional[str] = None):
        """Clear Write Read request constructor.

        Args:
            nadr (int): Device address.
            read_timeout (int): Timeout in 10ms unit to wait for data to be read. To read no data, use value 255.
            data (List[int], optional): Data to write to TX buffer.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(read_timeout=read_timeout, data=data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.UART,
            pcmd=UartRequestCommands.CLEAR_WRITE_READ,
            m_type=UartMessages.CLEAR_WRITE_READ,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._read_timeout = read_timeout
        self._data = data if data is not None else []

    def _validate(self, read_timeout: int, data: Optional[List[int]] = None):
        """Validate request parameters.

        Args:
            read_timeout (int): Timeout in 10ms unit to wait for data to be read. To read no data, use value 255.
            data (List[int], optional): Data to write to TX buffer.
        """
        self._validate_read_timeout(read_timeout=read_timeout)
        self._validate_data(data=data)

    @staticmethod
    def _validate_read_timeout(read_timeout: int):
        """Validate read timeout parameter.

        Args:
            read_timeout (int): Timeout in 10ms unit to wait for data to be read. To read no data, use value 255.

        Raises:
            RequestParameterInvalidValueError: If read_timeout is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= read_timeout <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Read timeout value should be between 0 and 255.')

    @property
    def read_timeout(self) -> int:
        """:obj:`int`: Timeout in 10ms unit to wait for data to be read. To read no data, use value 255.

        Getter and setter.
        """
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, value: int):
        self._validate_read_timeout(value)
        self._read_timeout = value

    @staticmethod
    def _validate_data(data: Optional[List[int]] = None):
        """Validate data parameter.

        Args:
            data (List[int], optional): Data to write to TX buffer.

        Raises:
            RequestParameterInvalidValueError: If data contains more than 57 values or if values are not
                in range from 0 to 255.
        """
        if data is None:
            return
        if len(data) > 57:
            raise RequestParameterInvalidValueError('Maximum data length is 57 bytes.')
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Write data values should be between 0 and 255.')

    @property
    def data(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int` or :obj:`None`: Data to write to TX buffer.

        Getter and setter.
        """
        return self._data

    @data.setter
    def data(self, value: Optional[List[int]]):
        self._validate_data(value)
        self._data = value if value is not None else []

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._read_timeout] + self._data
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {
            'readTimeout': self._read_timeout,
            'writtenData': self._data,
        }
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
