"""OS Test RF Signal response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.common import Common
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = [
    'TestRfSignalResponse'
]


class TestRfSignalResponse(IResponseGetterMixin):
    """OS Test RF Signal response class."""

    __slots__ = ('_counter',)
    __test__ = False

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Test RF Signal response constructor.

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
            pcmd=OSResponseCommands.TEST_RF_SIGNAL,
            m_type=OSMessages.TEST_RF_SIGNAL,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._counter = None
        if rcode == ResponseCodes.OK:
            self._counter = result['counter']

    @property
    def counter(self) -> Optional[int]:
        """:obj:`int` or :obj:`None`: Counter value.

        Getter only.
        """
        return self._counter

    def get_count(self) -> str:
        """String representation of counter value.

        Returns:
            :obj:`str`: String representation of counter value.
        """
        if self._counter is None:
            return 'None'
        if self._counter == 0:
            val = 0
        elif 1 <= self._counter <= 0x7f:
            val = self._counter - 1
        else:
            val = f'{((self._counter & 0x7f) * 0x80) - 1}-{((self._counter & 0x7f) * 0x80) + 0x7e}'
        return f'{val}'

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'TestRfSignalResponse':
        """DPA response factory method.

        Parses DPA data and constructs :obj:`TestRfSignalResponse` object.

        Args:
            dpa (bytes): DPA response bytes.
        Returns:
            :obj:`TestRfSignalResponse`: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=9)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {
                'counter': pdata[0],
            }
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'TestRfSignalResponse':
        """JSON response factory method.

        Parses JSON API response and constructs :obj:`TestRfSignalResponse` object.

        Args:
            json (dict): JSON API response.
        Returns:
            :obj:`TestRfSignalResponse`: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)
