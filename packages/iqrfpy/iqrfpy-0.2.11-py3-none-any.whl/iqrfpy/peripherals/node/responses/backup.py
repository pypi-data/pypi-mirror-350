"""Node Backup response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import NodeResponseCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['BackupResponse']


class BackupResponse(IResponseGetterMixin):
    """Node Backup response class."""

    __slots__ = ('_backup_data',)

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Backup response constructor.

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
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeResponseCommands.BACKUP,
            m_type=NodeMessages.BACKUP,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._backup_data = result['backupData'] if rcode == ResponseCodes.OK else None

    @property
    def backup_data(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int` or :obj:`None`: Backup data.

        Getter only.
        """
        return self._backup_data

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'BackupResponse':
        """DPA response factory method.

        Parses DPA data and constructs BackupResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            BackupResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=57)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {'backupData': list(dpa[8:])}
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'BackupResponse':
        """JSON response factory method.

        Parses JSON API response and constructs BackupResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            BackupResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(nadr=nadr, msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, pdata=pdata, result=result)
