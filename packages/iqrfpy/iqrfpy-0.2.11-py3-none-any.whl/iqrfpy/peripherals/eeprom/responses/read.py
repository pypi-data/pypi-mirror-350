"""Eeprom Read response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import EEPROMResponseCommands
from iqrfpy.enums.message_types import EEPROMMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['ReadResponse']


class ReadResponse(IResponseGetterMixin):
    """Eeprom Read response class."""

    __slots__ = ('_data',)

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Read response constructor.

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
            pnum=EmbedPeripherals.EEPROM,
            pcmd=EEPROMResponseCommands.READ,
            m_type=EEPROMMessages.READ,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._data = result['pData'] if rcode == ResponseCodes.OK else None

    @property
    def data(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int` or :obj:`None`: Data read from memory.

        Getter only.
        """
        return self._data

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'ReadResponse':
        """DPA response factory method.

        Parses DPA data and constructs :obj:`ReadResponse` object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            :obj:`ReadResponse`: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {'pData': list(dpa[8:])}
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'ReadResponse':
        """JSON response factory method.

        Parses JSON API response and constructs :obj:`ReadResponse` object.

        Args:
            json (dict): JSON API response.

        Returns:
            :obj:`ReadResponse`: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)
