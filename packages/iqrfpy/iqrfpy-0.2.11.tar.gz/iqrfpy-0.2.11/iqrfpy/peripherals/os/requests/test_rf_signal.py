"""OS Test RF Signal request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = [
    'TestRfSignalRequest'
]


class TestRfSignalRequest(IRequest):
    """OS Test RF Signal request class."""

    __slots__ = '_channel', '_rx_filter', '_time'
    __test__ = False

    def __init__(self, nadr: int, channel: int, rx_filter: int, time: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """OS Test RF Signal request constructor.

        Args:
            nadr (int): Device address.
            channel (int): Channel to test.
            rx_filter (int): RX filter.
            time (int): Signal test time (10ms unit).
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(channel=channel, rx_filter=rx_filter, time=time)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.TEST_RF_SIGNAL,
            m_type=OSMessages.TEST_RF_SIGNAL,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._channel = channel
        self._rx_filter = rx_filter
        self._time = time

    def _validate(self, channel: int, rx_filter: int, time: int):
        """Validate request parameters.

        Args:
            channel (int): Channel to test.
            rx_filter (int): RX filter.
            time (int): Signal test time (10ms unit).
        """
        self._validate_channel(channel=channel)
        self._validate_rx_filter(rx_filter=rx_filter)
        self._validate_time(time=time)

    @staticmethod
    def _validate_channel(channel: int):
        """Validate channel parameter.

        Args:
            channel (int): Channel to test.
        Raises:
            RequestParameterInvalidValueError: If channel is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= channel <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Channel value should be between 0 and 255.')

    @property
    def channel(self) -> int:
        """:obj:`int`: Channel.

        Getter and setter.
        """
        return self._channel

    @channel.setter
    def channel(self, value: int):
        self._validate_channel(channel=value)
        self._channel = value

    @staticmethod
    def _validate_rx_filter(rx_filter: int):
        """Validate RX filter parameter.

        Args:
            rx_filter (int): RX filter.
        Raises:
            RequestParameterInvalidValueError: If rx_filter is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= rx_filter <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('RX filter value should be between 0 and 255.')

    @property
    def rx_filter(self) -> int:
        """:obj:`int`: RX filter.

        Getter and setter.
        """
        return self._rx_filter

    @rx_filter.setter
    def rx_filter(self, value: int):
        self._validate_rx_filter(rx_filter=value)
        self._rx_filter = value

    @staticmethod
    def _validate_time(time: int):
        """Validate time parameter.

        Args:
            time (int): Signal test time (10ms unit).
        Raises:
            RequestParameterInvalidValueError: If time is less than 0 or greater than 65535.
        """
        if not dpa_constants.WORD_MIN <= time <= dpa_constants.WORD_MAX:
            raise RequestParameterInvalidValueError('Time value should be between 0 and 65535.')

    @property
    def time(self) -> int:
        """:obj:`int`: Time (10ms unit).

        Getter and setter.
        """
        return self._time

    @time.setter
    def time(self, value: int):
        self._validate_time(time=value)
        self._time = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._channel, self._rx_filter, self._time & 0xFF, (self._time >> 8) & 0xFF]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {
            'channel': self._channel,
            'rxFilter': self._rx_filter,
            'time': self._time,
        }
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
