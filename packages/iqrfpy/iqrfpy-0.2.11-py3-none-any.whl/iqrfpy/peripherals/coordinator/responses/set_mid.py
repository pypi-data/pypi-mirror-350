"""Coordinator Set MID response message."""

from typing import Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import CoordinatorResponseCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['SetMidResponse']


class SetMidResponse(IResponseGetterMixin):
    """Coordinator Set MID response class."""

    def __init__(self, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        """SetMID response constructor.

        Args:
            hwpid (int, optional): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            rcode (int, optional): Response code. Defaults to 128.
            dpa_value (int, optional): DPA value. Defaults to 0.
            msgid (str, optional): Message ID. Defaults to None.
            result (dict, optional): JSON response data. Defaults to None.
        """
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorResponseCommands.SET_MID,
            m_type=CoordinatorMessages.SET_MID,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'SetMidResponse':
        """DPA response factory method.

        Parses DPA data and constructs SetMidResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            SetMidResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        DpaValidator.response_length(dpa=dpa, expected_len=8)
        _, _, _, hwpid, rcode, dpa_value, _ = Common.parse_dpa_into_members(dpa=dpa)
        return cls(hwpid=hwpid, rcode=rcode, dpa_value=dpa_value)

    @classmethod
    def from_json(cls, json: dict) -> 'SetMidResponse':
        """JSON response factory method.

        Parses JSON API response and constructs SetMidResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            SetMidResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, _, hwpid, rcode, dpa_value, _, _ = Common.parse_json_into_members(json=json, omit_result=True)
        return cls(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode)
