"""Node Read response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import NodeResponseCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.objects.node_read_data import NodeReadData
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = [
    'ReadResponse',
    'NodeReadData'
]


class ReadResponse(IResponseGetterMixin):
    """Node Read response class."""

    __slots__ = ('_node_data',)

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
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeResponseCommands.READ,
            m_type=NodeMessages.READ,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._node_data = NodeReadData(result) if rcode == ResponseCodes.OK else None

    @property
    def node_data(self) -> Optional[NodeReadData]:
        """:obj:`NodeReadData` :obj:`None`: Node read data.

        Getter only.
        """
        return self._node_data

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'ReadResponse':
        """DPA response factory method.

        Parses DPA data and constructs ReadResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            ReadResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == 0:
            DpaValidator.response_length(dpa=dpa, expected_len=20)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {
                'ntwADDR': pdata[0],
                'ntwVRN': pdata[1],
                'ntwZIN': pdata[2],
                'ntwDID': pdata[3],
                'ntwPVRN': pdata[4],
                'ntwUSERADDRESS': (pdata[6] << 8) + pdata[5],
                'ntwID': (pdata[8] << 8) + pdata[7],
                'ntwVRNFNZ': pdata[9],
                'ntwCFG': pdata[10],
                'flags': pdata[11]
            }
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'ReadResponse':
        """JSON response factory method.

        Parses JSON API response and constructs ReadResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            ReadResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)
