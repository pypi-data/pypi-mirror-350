"""Exploration Peripheral Information response message."""

from typing import List, Optional, Union
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import ExplorationResponseCommands
from iqrfpy.enums.message_types import ExplorationMessages
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.utils.common import Common
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator
from iqrfpy.objects import ExplorationPerInfoData

__all__ = [
    'PeripheralInformationResponse',
    'ExplorationPerInfoData',
]


class PeripheralInformationResponse(IResponseGetterMixin):
    """Exploration Peripheral Information response class."""

    __slots__ = ('_peripheral_data',)

    def __init__(self, nadr: int, pnum: Union[Peripheral, int], hwpid: int = dpa_constants.HWPID_MAX,
                 rcode: int = 0, dpa_value: int = 0, msgid: Optional[str] = None, pdata: Optional[List[int]] = None,
                 result: Optional[dict] = None):
        """Read response constructor.

        Args:
            nadr (int): Device address.
            pnum (pnum: Union[Peripheral, int]): Requested peripheral.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            rcode (int, optional): Response code. Defaults to 128.
            dpa_value (int, optional): DPA value. Defaults to 0.
            pdata (List[int], optional): DPA response data. Defaults to None.
            msgid (str, optional): Message ID. Defaults to None.
            result (dict, optional): JSON response data. Defaults to None.
        """
        super().__init__(
            nadr=nadr,
            pnum=pnum,
            pcmd=ExplorationResponseCommands.PERIPHERALS_ENUMERATION_INFORMATION,
            m_type=ExplorationMessages.PERIPHERAL_INFORMATION,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._peripheral_data = ExplorationPerInfoData(result=result) if rcode == ResponseCodes.OK else None

    @property
    def peripheral_data(self) -> Optional[ExplorationPerInfoData]:
        """:obj:`ExplorationPerInfoData` or :obj:`None`: Peripheral information data.

        Getter only.
        """
        return self._peripheral_data

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'PeripheralInformationResponse':
        """DPA response factory method.

        Parses DPA data and constructs PeripheralInformationResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            PeripheralInformationResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, pnum, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=12)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {
                'perTe': dpa[8],
                'perT': dpa[9],
                'par1': dpa[10],
                'par2': dpa[11],
            }
        return cls(nadr=nadr, pnum=pnum, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'PeripheralInformationResponse':
        """JSON response factory method.

        Parses JSON API response and constructs PeripheralInformationResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            PeripheralInformationResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        pnum = Common.pnum_from_json(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        if rcode < 0:
            pnum += 0x80
        return cls(nadr=nadr, pnum=pnum, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata,
                   result=result)
