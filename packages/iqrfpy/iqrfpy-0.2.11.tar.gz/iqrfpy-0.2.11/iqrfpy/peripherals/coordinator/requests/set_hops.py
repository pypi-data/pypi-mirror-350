"""Coordinator Set Hops request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['SetHopsRequest']


class SetHopsRequest(IRequest):
    """Coordinator Set Hops request class."""

    __slots__ = '_request_hops', '_response_hops'

    def __init__(self, request_hops: int, response_hops: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Set Hops request constructor.

        Args:
            request_hops (int): Number of hops to send DPA request.
            response_hops (int): Number of hops to send DPA response.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(request_hops, response_hops)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SET_HOPS,
            m_type=CoordinatorMessages.SET_HOPS,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._request_hops = request_hops
        self._response_hops = response_hops

    def _validate(self, request_hops: int, response_hops: int) -> None:
        """Validates request parameters.

        Args:
            request_hops (int): Number of hops to send DPA request.
            response_hops (int): Number of hops to send DPA response.
        """
        self._validate_request_hops(request_hops)
        self._validate_response_hops(response_hops)

    @staticmethod
    def _validate_request_hops(request_hops: int):
        """Validates request hops parameter.

        Args:
            request_hops (int): Number of hops to send DPA request.

        Raises:
            RequestParameterInvalidValueError: If request_hops is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= request_hops <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Request hops value should be between 0 and 255.')

    @property
    def request_hops(self) -> int:
        """:obj:`int`: Number of hops to send DPA request.

        Getter and setter.
        """
        return self._request_hops

    @request_hops.setter
    def request_hops(self, value: int) -> None:
        self._validate_request_hops(value)
        self._request_hops = value

    @staticmethod
    def _validate_response_hops(response_hops: int):
        """Validates response hops parameter.

        Args:
            response_hops (int): Number of hops to send DPA response.

        Raises:
            RequestParameterInvalidValueError: If response_hops is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= response_hops <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Response hops value should be between 0 and 255.')

    @property
    def response_hops(self) -> int:
        """:obj:`int`: Number of hops to send DPA response.

        Getter and setter.
        """
        return self._response_hops

    @response_hops.setter
    def response_hops(self, value: int) -> None:
        self._validate_response_hops(value)
        self._response_hops = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._request_hops, self._response_hops]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'requestHops': self._request_hops, 'responseHops': self._response_hops}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
