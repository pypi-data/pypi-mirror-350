"""Coordinator Discovery response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import CoordinatorResponseCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['DiscoveryResponse']


class DiscoveryResponse(IResponseGetterMixin):
    """Coordinator Discovery response class."""

    __slots__ = ('_disc_nr',)

    def __init__(self, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Discovery response constructor.

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
            pcmd=CoordinatorResponseCommands.DISCOVERY,
            m_type=CoordinatorMessages.DISCOVERY,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._disc_nr = result['discNr'] if rcode == ResponseCodes.OK else None

    @property
    def disc_nr(self) -> Optional[int]:
        """:obj:`int` or :obj:`None`: Number of discovered devices.

        Getter only.
        """
        return self._disc_nr

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'DiscoveryResponse':
        """DPA response factory method.

        Parses DPA data and constructs DiscoveryResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            DiscoveryResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        _, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=9)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {'discNr': dpa[8]}
        return cls(hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'DiscoveryResponse':
        """JSON response factory method.

        Parses JSON API response and constructs DiscoveryResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            DiscoveryResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, _, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, pdata=pdata, result=result)
