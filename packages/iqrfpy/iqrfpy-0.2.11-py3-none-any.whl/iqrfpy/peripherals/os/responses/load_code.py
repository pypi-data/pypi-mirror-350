"""OS Load Code response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes, OsLoadCodeErrors, OsLoadCodeResult
from iqrfpy.utils.common import Common
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = [
    'LoadCodeResponse'
]


class LoadCodeResponse(IResponseGetterMixin):
    """OS Load Code response class."""

    __slots__ = ('_load_result',)

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Load Code response constructor.

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
            pnum=EmbedPeripherals.OS,
            pcmd=OSResponseCommands.LOAD_CODE,
            m_type=OSMessages.LOAD_CODE,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._load_result = None
        if rcode == ResponseCodes.OK:
            self._load_result = result['loadingCode']

    @property
    def load_result(self) -> Optional[int]:
        """:obj:`int` or :obj:`None`: Load code raw result value.

        Getter only.
        """
        return self._load_result

    def get_load_result(self) -> Optional[OsLoadCodeResult]:
        """Get load result as enum member.

        Returns:
            :obj:`OsLoadCodeResult` or :obj:`None`: Load code result.
        """
        if self._load_result is None:
            return None
        return OsLoadCodeResult(self._load_result & 1)

    def get_load_error(self) -> Optional[OsLoadCodeErrors]:
        """Get load result error as enum member.

        Returns:
            :obj:`OsLoadCodeErrors` or :obj:`None`: Load code error.
        """
        if self.get_load_result() is None:
            return None
        val = (self._load_result >> 1)
        if val in OsLoadCodeErrors:
            return OsLoadCodeErrors(val)
        return OsLoadCodeErrors.RESERVED

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'LoadCodeResponse':
        """DPA response factory method.

        Parses DPA data and constructs :obj:`LoadCodeResponse` object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            :obj:`LoadCodeResponse`: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=9)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {
                'loadingCode': pdata[0],
            }
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'LoadCodeResponse':
        """JSON response factory method.

        Parses JSON API response and constructs :obj:`LoadCodeResponse` object.

        Args:
            json (dict): JSON API response.

        Returns:
            :obj:`LoadCodeResponse`: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)
