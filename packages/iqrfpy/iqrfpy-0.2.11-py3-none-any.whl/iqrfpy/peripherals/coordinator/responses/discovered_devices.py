"""Coordinator Discovered Devices response message."""

from typing import List, Optional
from iqrfpy.enums.commands import CoordinatorResponseCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['DiscoveredDevicesResponse']


class DiscoveredDevicesResponse(IResponseGetterMixin):
    """Coordinator DiscoveredDevices response class."""

    __slots__ = ('_discovered',)

    def __init__(self, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """DiscoveredDevices response constructor.

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
            pcmd=CoordinatorResponseCommands.DISCOVERED_DEVICES,
            m_type=CoordinatorMessages.DISCOVERED_DEVICES,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._discovered = result['discoveredDevices'] if rcode == ResponseCodes.OK else None

    @property
    def discovered(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int` or :obj:`None`: List of discovered node devices.

        Getter only.
        """
        return self._discovered

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'DiscoveredDevicesResponse':
        """DPA response factory method.

        Parses DPA data and constructs DiscoveredDevicesResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            DiscoveredDevicesResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        _, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=40)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {'discoveredDevices': Common.bitmap_to_nodes(pdata[:30], coordinator_shift=True)}
        return cls(hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'DiscoveredDevicesResponse':
        """JSON response factory method.

        Parses JSON API response and constructs DiscoveredDevicesResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            DiscoveredDevicesResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, _, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, pdata=pdata, result=result)
