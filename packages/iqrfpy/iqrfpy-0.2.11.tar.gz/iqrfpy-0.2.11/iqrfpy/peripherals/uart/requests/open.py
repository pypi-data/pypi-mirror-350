"""UART Open request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import UartRequestCommands
from iqrfpy.enums.message_types import UartMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
from iqrfpy.utils.dpa import BaudRates, BYTE_MIN, BYTE_MAX, HWPID_MAX
from iqrfpy.irequest import IRequest

__all__ = [
    'OpenRequest',
]


class OpenRequest(IRequest):
    """UART Open request class."""

    __slots__ = ('_baud_rate',)

    def __init__(self, nadr: int, baud_rate: Union[BaudRates, int], hwpid: int = HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Read request constructor.

        Args:
            nadr (int): Device address.
            baud_rate (Union[BaudRates, int]): Baud rate.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate_baud_rate(baud_rate=baud_rate)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.UART,
            pcmd=UartRequestCommands.OPEN,
            m_type=UartMessages.OPEN,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._baud_rate = baud_rate

    @staticmethod
    def _validate_baud_rate(baud_rate: Union[BaudRates, int]):
        """Validate baud rate parameter.

        Args:
            baud_rate (Union[BaudRates, int]): Baud rate.

        Raises:
            RequestParameterInvalidValueError: If baud_rate is less than 0 or greater than 255.
        """
        if not BYTE_MIN <= baud_rate <= BYTE_MAX:
            raise RequestParameterInvalidValueError('Baud rate value should be between 0 and 255.')

    @property
    def baud_rate(self) -> Union[BaudRates, int]:
        """:obj:`BaudRates` or :obj:`int`: Baud rate.

        Getter and setter.
        """
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, value: Union[BaudRates, int]):
        self._validate_baud_rate(value)
        self._baud_rate = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._baud_rate]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'baudRate': self._baud_rate}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
