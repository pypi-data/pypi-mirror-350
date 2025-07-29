"""Coordinator Discovery request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['DiscoveryRequest']


class DiscoveryRequest(IRequest):
    """Coordinator Discovery request class."""

    __slots__ = '_tx_power', '_max_addr'

    def __init__(self, tx_power: int, max_addr: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Discovery request constructor.

        Args:
            tx_power (int): TX power used for discovery.
            max_addr (int): Maximum node address to be included in the discovery process, 0 means all nodes.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(tx_power, max_addr)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.DISCOVERY,
            m_type=CoordinatorMessages.DISCOVERY,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._tx_power = tx_power
        self._max_addr = max_addr

    def _validate(self, tx_power: int, max_addr: int) -> None:
        """Validate request parameters.

        Addr:
            tx_power (int): TX power used for discovery.
            max_addr (int): Maximum node address to be included in the discovery process, 0 means all nodes.
        """
        self._validate_tx_power(tx_power)
        self._validate_max_addr(max_addr)

    @staticmethod
    def _validate_tx_power(tx_power: int):
        """Validate TX power parameter.

        Args:
            tx_power (int): TX power used for discovery.

        Raises:
            RequestParameterInvalidValueError: If tx_power is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= tx_power <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('TX power value should be between 0 and 255.')

    @property
    def tx_power(self) -> int:
        """:obj:`int`: TX power used for discovery.

        Getter and setter.
        """
        return self._tx_power

    @tx_power.setter
    def tx_power(self, value: int):
        self._validate_tx_power(value)
        self._tx_power = value

    @staticmethod
    def _validate_max_addr(max_addr: int):
        """Validate maximum node address parameter.

        Args:
            max_addr (int): Maximum node address to be included in the discovery process, 0 means all nodes.

        Raises:
            RequestParameterInvalidValueError: If max_addr is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= max_addr <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Max address value should be between 0 and 255.')

    @property
    def max_addr(self) -> int:
        """:obj:`int`: Maximum node address to be included in the discovery process.

        Getter and setter.
        """
        return self._max_addr

    @max_addr.setter
    def max_addr(self, value: int) -> None:
        self._validate_max_addr(value)
        self._max_addr = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._tx_power, self._max_addr]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'txPower': self._tx_power, 'maxAddr': self._max_addr}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
