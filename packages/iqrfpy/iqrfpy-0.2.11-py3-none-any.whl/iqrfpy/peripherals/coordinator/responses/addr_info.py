"""Coordinator Addr Info response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import CoordinatorResponseCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['AddrInfoResponse']


class AddrInfoResponse(IResponseGetterMixin):
    """Coordinator AddrInfo response class."""

    __slots__ = '_dev_nr', '_did'

    def __init__(self, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """AddrInfo response constructor.

        Args:
            hwpid (int, optional): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            rcode (int, optional): Response code. Defaults to 128.
            dpa_value (int, optional): DPA value. Defaults to 0.
            pdata (List[int], optional): DPA response data. Defaults to None.
            msgid (str, optional): Message ID. Defaults to None.
            result (dict, optional): JSON response data. Defaults to None.
        """
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorResponseCommands.ADDR_INFO,
            m_type=CoordinatorMessages.ADDR_INFO,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._dev_nr = self._did = None
        if rcode == ResponseCodes.OK:
            self._dev_nr = result['devNr']
            self._did = result['did']

    @property
    def dev_nr(self) -> Optional[int]:
        """:obj:`int` or :obj:`None`: Number of devices in network.

        Getter only.
        """
        return self._dev_nr

    @property
    def did(self) -> Optional[int]:
        """:obj:`int` or :obj:`None`: Discovery ID.

        Getter only.
        """
        return self._did

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'AddrInfoResponse':
        """DPA response factory method.

        Parses DPA data and constructs AddrInfoResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            AddrInfoResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        _, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=10)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {'devNr': dpa[8], 'did': dpa[9]}
        return cls(hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'AddrInfoResponse':
        """JSON response factory method.

        Parses JSON API response and constructs AddrInfoResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            AddrInfoResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, _, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, pdata=pdata, result=result)
