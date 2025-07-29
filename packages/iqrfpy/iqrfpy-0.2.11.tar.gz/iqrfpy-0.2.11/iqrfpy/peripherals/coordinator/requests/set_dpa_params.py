"""Coordinator Set Dpa Params request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.objects import CoordinatorDpaParam
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = [
    'SetDpaParamsRequest',
    'CoordinatorDpaParam',
]


class SetDpaParamsRequest(IRequest):
    """Coordinator Set Dpa Params request class."""

    __slots__ = ('_dpa_param',)

    def __init__(self, dpa_param: Union[CoordinatorDpaParam, int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """SetDpaParams request constructor.

        Args:
            dpa_param (Union[CoordinatorDpaParam, int]): DPA param to set.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate_dpa_param(dpa_param)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SET_DPA_PARAMS,
            m_type=CoordinatorMessages.SET_DPA_PARAMS,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._dpa_param = dpa_param

    @staticmethod
    def _validate_dpa_param(dpa_param: Union[CoordinatorDpaParam, int]):
        """Validates DPA param parameter.

        Args:
            dpa_param (Union[CoordinatorDpaParam, int]): DPA param to set.

        Raises:
            RequestParameterInvalidValueError: If dpa_param is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= dpa_param <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('DPA param value should be between 0 and 255.')

    @property
    def dpa_param(self) -> Union[CoordinatorDpaParam, int]:
        """:obj:`CoordinatorDpaParam` or :obj:`int`: DPA param.

        Getter and setter.
        """
        return self._dpa_param

    @dpa_param.setter
    def dpa_param(self, value: Union[CoordinatorDpaParam, int]) -> None:
        self._validate_dpa_param(value)
        self._dpa_param = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._dpa_param]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'dpaParam': self._dpa_param}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
