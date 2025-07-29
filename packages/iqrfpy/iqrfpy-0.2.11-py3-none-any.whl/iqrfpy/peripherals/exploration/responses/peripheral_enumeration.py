"""Exploration Peripheral Enumeration response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import ExplorationResponseCommands
from iqrfpy.enums.message_types import ExplorationMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.objects import ExplorationPerEnumData
from iqrfpy.utils.common import Common
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = (
    'PeripheralEnumerationResponse',
    'ExplorationPerEnumData',
)


class PeripheralEnumerationResponse(IResponseGetterMixin):
    """Exploration Peripheral Enumeration response class."""

    __slots__ = ('_per_enum_response',)

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Peripheral Enumeration response constructor.

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
            pnum=EmbedPeripherals.EXPLORATION,
            pcmd=ExplorationResponseCommands.PERIPHERALS_ENUMERATION_INFORMATION,
            m_type=ExplorationMessages.ENUMERATE,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._per_enum_response = ExplorationPerEnumData(result=result) if rcode == ResponseCodes.OK else None

    @property
    def per_enum_data(self) -> Optional[ExplorationPerEnumData]:
        """:obj:`ExplorationPerEnumData` or :obj:`None`: Peripheral enumeration data.

        Getter only.
        """
        return self._per_enum_response

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'PeripheralEnumerationResponse':
        """DPA response factory method.

        Parses DPA data and constructs PeripheralEnumerationResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            PeripheralEnumerationResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            if len(dpa) < 20:
                raise DpaResponsePacketLengthError('DPA response packet too short, expected payload of at least 20B.')
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {
                'dpaVer': (dpa[9] << 8) + dpa[8],
                'perNr': dpa[10],
                'hwpid': (dpa[16] << 8) + dpa[15],
                'hwpidVer': (dpa[18] << 8) + dpa[17],
                'flags': dpa[19],
                'userPer': [],
            }
            embed_pers_data = list(dpa[11:14])
            embedded_pers = []
            for i in range(0, len(embed_pers_data * 8)):
                if embed_pers_data[int(i / 8)] & (1 << (i % 8)) and i in EmbedPeripherals:
                    embedded_pers.append(i)
            result['embeddedPers'] = embedded_pers
            if result['perNr'] > 0:
                user_per_data = list(dpa[20:])
                user_pers = []
                for i in range(0, len(user_per_data * 8)):
                    if user_per_data[int(i / 8)] & (1 << (i % 8)):
                        user_pers.append(i + 0x20)
                result['userPer'] = user_pers
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'PeripheralEnumerationResponse':
        """JSON response factory method.

        Parses JSON API response and constructs PeripheralEnumerationResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            PeripheralEnumerationResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)
