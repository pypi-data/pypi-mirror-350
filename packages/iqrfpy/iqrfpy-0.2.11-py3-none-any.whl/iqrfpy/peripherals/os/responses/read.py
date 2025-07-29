"""OS Read response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.objects.os_read_data import OsReadData
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.common import Common
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = [
    'ReadResponse',
    'OsReadData',
]


class ReadResponse(IResponseGetterMixin):
    """OS Read response class."""

    __slots__ = ('_os_read_data',)

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
            pnum=EmbedPeripherals.OS,
            pcmd=OSResponseCommands.READ,
            m_type=OSMessages.READ,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._os_read_data = OsReadData(data=result) if rcode == ResponseCodes.OK else None

    @property
    def os_read_data(self) -> Optional[OsReadData]:
        """:obj:`OsReadData` or :obj:`None`: OS Read data.

        Getter only.
        """
        return self._os_read_data

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
            if len(dpa) < 48:
                raise DpaResponsePacketLengthError('DPA response packet length invalid, expected at least 48B of data.')
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {
                'mid': (dpa[11] << 24) + (dpa[10] << 16) + (dpa[9] << 8) + dpa[8],
                'osVersion': dpa[12],
                'trMcuType': dpa[13],
                'osBuild': (dpa[15] << 8) + dpa[14],
                'rssi': dpa[16],
                'supplyVoltage': 261.12 / (127 - dpa[17]),
                'flags': dpa[18],
                'slotLimits': dpa[19],
                'ibk': list(dpa[20:36]),
                'dpaVer': (dpa[37] << 8) + dpa[36],
                'perNr': dpa[38],
                'hwpid': (dpa[44] << 8) + dpa[43],
                'hwpidVer': (dpa[46] << 8) + dpa[45],
                'flagsEnum': dpa[47],
                'userPer': [],
            }
            embed_pers_data = list(dpa[39:43])
            embedded_pers = []
            for i in range(0, len(embed_pers_data * 8)):
                if embed_pers_data[int(i / 8)] & (1 << (i % 8)) and i in EmbedPeripherals:
                    embedded_pers.append(i)
            result['embeddedPers'] = embedded_pers
            if result['perNr'] > 0:
                user_per_data = list(dpa[48:])
                user_pers = []
                for i in range(0, len(user_per_data * 8)):
                    if user_per_data[int(i / 8)] & (1 << (i % 8)):
                        user_pers.append(i + 0x20)
                result['userPer'] = user_pers
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
