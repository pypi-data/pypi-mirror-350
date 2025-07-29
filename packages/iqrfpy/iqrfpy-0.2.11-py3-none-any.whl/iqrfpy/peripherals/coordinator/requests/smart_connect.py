"""Coordinator Smart Connect request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['SmartConnectRequest']


class SmartConnectRequest(IRequest):
    """Coordinator SmartConnect request class."""

    __slots__ = '_req_addr', '_bonding_test_retries', '_ibk', '_mid', '_virtual_device_address'

    def __init__(self, req_addr: int, bonding_test_retries: int, ibk: List[int], mid: int,
                 virtual_device_address: int = 0xFF, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """SmartConnect request constructor.

        Args:
            req_addr (int): Requested node address.
            bonding_test_retries (int): Maximum number of FRCs used to test whether node was bonded.
            ibk (List[int]): Individual bonding key of node devices.
            mid (int): MID of node device.
            virtual_device_address (int): Virtual device address.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(req_addr, bonding_test_retries, ibk, mid, virtual_device_address)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SMART_CONNECT,
            m_type=CoordinatorMessages.SMART_CONNECT,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._req_addr = req_addr
        self._bonding_test_retries = bonding_test_retries
        self._ibk = ibk
        self._mid = mid
        self._virtual_device_address = virtual_device_address

    def _validate(self, req_addr: int, bonding_test_retries: int, ibk: List[int], mid: int,
                  virtual_device_address: int) -> None:
        """Validates request parameters.

        Args:
            req_addr (int): Requested node address.
            bonding_test_retries (int): Maximum number of FRCs used to test whether node was bonded.
            ibk (List[int]): Individual bonding key of node devices.
            mid (int): MID of node device.
            virtual_device_address (int): Virtual device address.
        """
        self._validate_req_addr(req_addr)
        self._validate_bonding_test_retries(bonding_test_retries)
        self._validate_ibk(ibk)
        self._validate_mid(mid)
        self._validate_virtual_device_address(virtual_device_address)

    @staticmethod
    def _validate_req_addr(req_addr: int):
        """Validates requested address parameter.

        Args:
            req_addr (int): Requested node address.

        Raises:
            RequestParameterInvalidValueError: If req_addr is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= req_addr <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Requested address should be between 0 and 255.')

    @property
    def req_addr(self) -> int:
        """:obj:`int`: Requested node address.

        Getter and setter.
        """
        return self._req_addr

    @req_addr.setter
    def req_addr(self, value: int) -> None:
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
        if not dpa_constants.BYTE_MIN <= bonding_test_retries <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Bonding test retries should be between 0 and 255.')

    @property
    def bonding_test_retries(self) -> int:
        """:obj:`int`: Maximum number of FRCs used to test whether node was bonded.

        Getter and setter.
        """
        return self._bonding_test_retries

    @bonding_test_retries.setter
    def bonding_test_retries(self, value: int) -> None:
        self._validate_bonding_test_retries(value)
        self._bonding_test_retries = value

    @staticmethod
    def _validate_ibk(ibk: List[int]):
        """Validates individual bonding key parameter.

        Args:
            ibk (List[int]): Individual bonding key of node devices.

        Raises:
            RequestParameterInvalidValueError: If ibk is not 16 values long or if ibk values are not between 0 and 255.
        """
        if len(ibk) != dpa_constants.IBK_LEN:
            raise RequestParameterInvalidValueError('IBK should be list of 16 8bit unsigned integers.')
        if not Common.values_in_byte_range(ibk):
            raise RequestParameterInvalidValueError('IBK list should only contain values between 0 and 255.')

    @property
    def ibk(self) -> List[int]:
        """:obj:`list` of :obj:`int`: Individual bonding key of node devices.

        Getter and setter.
        """
        return self._ibk

    @ibk.setter
    def ibk(self, value: List[int]) -> None:
        self._validate_ibk(value)
        self._ibk = value

    @staticmethod
    def _validate_mid(mid: int):
        """Validates MID parameter.

        Args:
            mid (int): MID of node device.

        Raises:
            RequestParameterInvalidValueError: If MID is less than 0 or greater than 4294967295.
        """
        if not dpa_constants.MID_MIN <= mid <= dpa_constants.MID_MAX:
            raise RequestParameterInvalidValueError('MID value should be between 0 and 4294967295.')

    @property
    def mid(self) -> int:
        """:obj:`int`: MID of node device.

        Getter and setter.
        """
        return self._mid

    @mid.setter
    def mid(self, value: int) -> None:
        self._validate_mid(value)
        self._mid = value

    @staticmethod
    def _validate_virtual_device_address(virtual_device_address: int):
        """Validates virtual device address parameter.

        Args:
            virtual_device_address (int): Virtual device address.

        Raises:
            RequestParameterInvalidValueError: If virtual_device_address is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= virtual_device_address <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Virtual device address should be between 0 and 255.')

    @property
    def virtual_device_address(self) -> int:
        """:obj:`int`: Virtual device address.

        Getter and setter.
        """
        return self._virtual_device_address

    @virtual_device_address.setter
    def virtual_device_address(self, value: int):
        self._validate_virtual_device_address(value)
        self._virtual_device_address = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        params = [self._req_addr, self._bonding_test_retries]
        params.extend(self._ibk)
        params.extend([
            self._mid & 0xFF,
            (self._mid >> 8) & 0xFF,
            (self._mid >> 16) & 0xFF,
            (self._mid >> 24) & 0xFF,
            0,
            self._virtual_device_address,
        ])
        params.extend([0] * 14)
        self._pdata = params
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {
            'reqAddr': self._req_addr,
            'bondingTestRetries': self._bonding_test_retries,
            'ibk': self._ibk,
            'mid': self._mid,
            'virtualDeviceAddress': self._virtual_device_address,
            'userData': [0, 0, 0, 0]
        }
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
