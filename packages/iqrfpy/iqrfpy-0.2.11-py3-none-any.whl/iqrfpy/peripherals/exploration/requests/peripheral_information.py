"""Exploration Peripheral Information request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import ExplorationRequestCommands
from iqrfpy.enums.message_types import ExplorationMessages
from iqrfpy.enums.peripherals import Peripheral
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['PeripheralInformationRequest']


class PeripheralInformationRequest(IRequest):
    """Exploration Peripheral Information request class."""

    def __init__(self, nadr: int, per: Union[Peripheral, int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Read request constructor.

        Args:
            nadr (int): Device address.
            per (Union[Peripheral, int]): Requested peripheral.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        super().__init__(
            nadr=nadr,
            pnum=per,
            pcmd=ExplorationRequestCommands.PERIPHERALS_ENUMERATION_INFORMATION,
            m_type=ExplorationMessages.PERIPHERAL_INFORMATION,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )

    @property
    def per(self) -> Union[Peripheral, int]:
        """:obj:`iqrfpy.enums.peripherals.Peripheral` or :obj:`int`: Requested periphera;.

        Getter and setter.
        """
        return self._pnum

    @per.setter
    def per(self, value: Union[Peripheral, int]):
        self._pnum = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'per': self._pnum.value if isinstance(self._pnum, Peripheral) else self._pnum}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
