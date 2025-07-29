"""BinaryOutput Set Output response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import BinaryOutputResponseCommands
from iqrfpy.enums.message_types import BinaryOutputMessages
from iqrfpy.enums.peripherals import Standards
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['SetOutputResponse']


class SetOutputResponse(IResponseGetterMixin):
    """BinaryOutput Set Output response class."""

    __slots__ = ('_states',)

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Set Output response constructor.

        Args:
            nadr (int): Device address.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            rcode (int, optional): Response code. Defaults to 128.
            dpa_value (int, optional): DPA value. Defaults to 0.
            pdata (List[int], optional): DPA response data. Defaults to None.
            msgid (str, optional): Message ID. Defaults to None.
            result (dict, optional): JSON response data. Defaults to None.
        """
        super().__init__(
            nadr=nadr,
            pnum=Standards.BINARY_OUTPUT,
            pcmd=BinaryOutputResponseCommands.SET_OUTPUT,
            m_type=BinaryOutputMessages.SET_OUTPUT,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._states = result['prevVals'] if rcode == ResponseCodes.OK else None

    @property
    def states(self) -> Optional[List[bool]]:
        """:obj:`list` of :obj:`bool` or :obj:`None`: Previous binary output states.

        Getter only.
        """
        return self._states

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'SetOutputResponse':
        """DPA response factory method.

        Parses DPA data and constructs :obj:`SetOutputResponse` object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            :obj:`SetOutputResponse`: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=12)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            binouts = [bool(x) for x in Common.bitmap_4byte_to_indexes(pdata)]
            result = {'prevVals': binouts}
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'SetOutputResponse':
        """JSON response factory method.

        Parses JSON API response and constructs :obj:`SetOutputResponse` object.

        Args:
            json (dict): JSON API response.

        Returns:
            :obj:`SetOutputResponse`: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(nadr=nadr, msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, pdata=pdata, result=result)
