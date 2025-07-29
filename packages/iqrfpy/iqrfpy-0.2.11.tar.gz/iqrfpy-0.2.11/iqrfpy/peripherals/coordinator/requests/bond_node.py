"""Coordinator Bond Node request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['BondNodeRequest']


class BondNodeRequest(IRequest):
    """Coordinator BondNode request class."""

    __slots__ = '_req_addr', '_bonding_test_retries'

    def __init__(self, req_addr: int, bonding_test_retries: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """BondNode request constructor.

        Args:
            req_addr (int): Requested node address.
            bonding_test_retries (int): Maximum number of FRCs used to test whether node was bonded.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(req_addr, bonding_test_retries)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.BOND_NODE,
            m_type=CoordinatorMessages.BOND_NODE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._req_addr = req_addr
        self._bonding_test_retries = bonding_test_retries

    def _validate(self, req_addr: int, bonding_test_retries: int) -> None:
        """Validate request parameters.

        Addr:
            req_addr (int): Requested node address.
            bonding_test_retries (int): Maximum number of FRCs used to test whether node was bonded.
        """
        self._validate_req_addr(req_addr)
        self._validate_bonding_test_retries(bonding_test_retries)

    @staticmethod
    def _validate_req_addr(req_addr: int):
        """Validates requested address parameter.

        Args:
            req_addr (int): Requested node address.

        Raises:
            RequestParameterInvalidValueError: If req_addr is less than 0 or greater than 255.
        """
        if req_addr < dpa_constants.BYTE_MIN or req_addr > dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Address value should be between 0 and 255.')

    @property
    def req_addr(self) -> int:
        """:obj:`int`: Requested node address.

        Getter and setter.
        """
        return self._req_addr

    @req_addr.setter
    def req_addr(self, value: int):
        self._validate_req_addr(value)
        self._req_addr = value

    @staticmethod
    def _validate_bonding_test_retries(bonding_test_retries: int):
        """Validates bonding test retries parameter.

        Args:
            bonding_test_retries (int): Maximum number of FRCs used to test whether node was bonded.

        Raises:
            RequestParameterInvalidValueError: If bonding_test_retries is less than 0 or greater than 255.
        """
        if bonding_test_retries < dpa_constants.BYTE_MIN or bonding_test_retries > dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Bonding test retries value should be between 0 and 255.')

    @property
    def bonding_test_retries(self) -> int:
        """:obj:`int`: Maximum number of FRCs used to test whether node was bonded.

        Getter and setter.
        """
        return self._bonding_test_retries

    @bonding_test_retries.setter
    def bonding_test_retries(self, value: int):
        self._validate_bonding_test_retries(value)
        self._bonding_test_retries = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._req_addr, self._bonding_test_retries]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'reqAddr': self._req_addr, 'bondingMask': self._bonding_test_retries}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
