"""FRC Send Selective response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import FrcResponseCommands
from iqrfpy.enums.message_types import FrcMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['SendSelectiveResponse']


class SendSelectiveResponse(IResponseGetterMixin):
    """FRC Send Selective response class."""

    __slots__ = '_status', '_frc_data'

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Send Selective response constructor.

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
            pnum=EmbedPeripherals.FRC,
            pcmd=FrcResponseCommands.SEND_SELECTIVE,
            m_type=FrcMessages.SEND_SELECTIVE,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._status = self._frc_data = None
        if rcode == ResponseCodes.OK:
            self._status = result['status']
            self._frc_data = result['frcData']

    @property
    def status(self) -> Optional[int]:
        """:obj:`int` or :obj:`None`: FRC return code (number of responded nodes or error code).

        Getter only.
        """
        return self._status

    @property
    def frc_data(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int` or :obj:`None`: FRC data.

        Getter only.
        """
        return self._frc_data

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'SendSelectiveResponse':
        """DPA response factory method.

        Parses DPA data and constructs SendSelectiveResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            SendSelectiveResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=64)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {'status': pdata[0], 'frcData': list(pdata[1:])}
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'SendSelectiveResponse':
        """JSON response factory method.

        Parses JSON API response and constructs SendSelectiveResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            SendSelectiveResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(msgid=msgid, nadr=nadr, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, pdata=pdata, result=result)
