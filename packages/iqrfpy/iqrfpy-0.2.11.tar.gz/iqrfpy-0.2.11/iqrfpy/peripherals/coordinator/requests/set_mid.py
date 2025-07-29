"""Coordinator Set MID request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['SetMidRequest']


class SetMidRequest(IRequest):
    """Coordinator SetMID request class."""

    __slots__ = '_bond_addr', '_mid'

    def __init__(self, bond_addr: int, mid: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """SetMID request constructor.

        Args:
            bond_addr (int): Address of node device.
            mid (int): MID to assign to a node in Coordinator's DB.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(bond_addr, mid)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SET_MID,
            m_type=CoordinatorMessages.SET_MID,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._bond_addr = bond_addr
        self._mid = mid

    def _validate(self, bond_addr: int, mid: int) -> None:
        """Validates request parameters.

        Args:
            bond_addr (int): Address of node device.
            mid (int): MID to assign to a node in Coordinator's DB.
        """
        self._validate_bond_addr(bond_addr)
        self._validate_mid(mid)

    @staticmethod
    def _validate_bond_addr(bond_addr: int):
        """Validates node address parameter.

        Args:
            bond_addr (int): Address of node device.

        Raises:
            RequestParameterInvalidValueError: If bond_addr is less than 0 or greater than 255.
        """
        if bond_addr < dpa_constants.BYTE_MIN or bond_addr > dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Bond address value should be between 0 and 255.')

    @property
    def bond_addr(self) -> int:
        """:obj:`int`: Address of node device.

        Getter and setter.
        """
        return self._bond_addr

    @bond_addr.setter
    def bond_addr(self, value: int) -> None:
        self._validate_bond_addr(value)
        self._bond_addr = value

    @staticmethod
    def _validate_mid(mid: int):
        """Validates MID parameter.

        Args:
            mid (int): MID to assign to a node in Coordinator's DB.

        Raises:
            RequestParameterInvalidValueError: If MID is less than 0 or greater than 4294967295.
        """
        if mid < dpa_constants.MID_MIN or mid > dpa_constants.MID_MAX:
            raise RequestParameterInvalidValueError('MID value should be between 0 and 4294967295.')

    @property
    def mid(self) -> int:
        """:obj:`int`: MID to assign to a node in Coordinator's DB.

        Getter and setter.
        """
        return self._mid

    @mid.setter
    def mid(self, value: int) -> None:
        self._validate_mid(value)
        self._mid = value

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
            self._mid & 0xFF,
            (self._mid >> 8) & 0xFF,
            (self._mid >> 16) & 0xFF,
            (self._mid >> 24) & 0xFF,
            self._bond_addr
        ]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'bondAddr': self._bond_addr, 'mid': self._mid}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
