"""Exploration More Peripherals Information response message."""

from typing import List, Optional, Union
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import ExplorationResponsePeripheralCommand
from iqrfpy.enums.message_types import ExplorationMessages
from iqrfpy.enums.peripherals import EmbedPeripherals, Peripheral
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.utils.common import Common
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.dpa import ResponsePacketMembers, ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator
from iqrfpy.objects import ExplorationPerInfoData

__all__ = [
    'MorePeripheralsInformationResponse',
    'ExplorationPerInfoData'
]


class MorePeripheralsInformationResponse(IResponseGetterMixin):
    """Exploration More Peripherals Information response class."""

    __slots__ = ('_peripheral_data',)

    def __init__(self, nadr: int, per: Union[Peripheral, int], hwpid: int = dpa_constants.HWPID_MAX,
                 rcode: int = 0, dpa_value: int = 0, msgid: Optional[str] = None, pdata: Optional[List[int]] = None,
                 result: Optional[dict] = None):
        """Read response constructor.

        Args:
            nadr (int): Device address.
            per (Union[Peripheral, int]): Requested peripheral.
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
            pcmd=per.value if isinstance(per, Peripheral) else per,
            m_type=ExplorationMessages.MORE_PERIPHERALS_INFORMATION,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._peripheral_data = None
        if rcode == ResponseCodes.OK:
            self._peripheral_data = [ExplorationPerInfoData(result=x) for x in result['peripherals']]

    @property
    def peripheral_data(self) -> Optional[List[ExplorationPerInfoData]]:
        """:obj:`list` of :obj:`ExplorationPerInfoData` or :obj:`None`: Peripheral information data.

        Getter only.
        """
        return self._peripheral_data

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'MorePeripheralsInformationResponse':
        """DPA response factory method.

        Parses DPA data and constructs MorePeripheralsInformationResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            MorePeripheralsInformationResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        per = ExplorationResponsePeripheralCommand(dpa[ResponsePacketMembers.PCMD])
        if rcode == ResponseCodes.OK:
            pdata = Common.pdata_from_dpa(dpa=dpa)
            if len(pdata) % 4 != 0:
                raise DpaResponsePacketLengthError('Invalid DPA response length, PDATA should be in multiples of 4B.')
            result = {'peripherals': []}
            for i in range(0, len(pdata), 4):
                result['peripherals'].append({
                    'perTe': pdata[i],
                    'perT': pdata[i + 1],
                    'par1': pdata[i + 2],
                    'par2': pdata[i + 3]
                })
        return cls(nadr=nadr, per=per, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'MorePeripheralsInformationResponse':
        """JSON response factory method.

        Parses JSON API response and constructs MorePeripheralsInformationResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            MorePeripheralsInformationResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        per = Common.pcmd_from_json(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        if rcode < 0:
            per += 0x80
        return cls(nadr=nadr, per=per, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata,
                   result=result)
