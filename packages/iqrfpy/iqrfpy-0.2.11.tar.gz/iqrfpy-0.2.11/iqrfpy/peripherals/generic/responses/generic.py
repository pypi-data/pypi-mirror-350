"""Generic response message."""

from typing import List, Optional, Union
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import Command
from iqrfpy.enums.message_types import GenericMessages
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponsePacketMembers
from iqrfpy.utils.validators import DpaValidator, JsonValidator


class GenericResponse(IResponseGetterMixin):
    """Generic response class."""

    def __init__(self, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int],
                 hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 pdata: Optional[List[int]] = None, msgid: Optional[str] = None):
        """Generic response constructor.

        Args:
            nadr (int): Device address.
            pnum (Union[Peripheral, int]): Peripheral number.
            pcmd (pcmd: Union[Command, int]): Peripheral command.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            rcode (int, optional): Response code. Defaults to 128.
            dpa_value (int, optional): DPA value. Defaults to 0.
            pdata (List[int], optional): Raw PDATA. Defaults to None.
            msgid (str, optional): Message ID. Defaults to None.
        """
        super().__init__(
            nadr=nadr,
            pnum=pnum,
            pcmd=pcmd,
            m_type=GenericMessages.RAW,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=pdata,
        )

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'GenericResponse':
        """DPA response factory method.

        Parses DPA data and constructs GenericResponse object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            GenericResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, pnum, pcmd, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        return cls(nadr=nadr, pnum=pnum, pcmd=pcmd, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata)

    @classmethod
    def from_json(cls, json: dict) -> 'GenericResponse':
        """JSON response factory method.

        Parses JSON API response and constructs GenericResponse object.

        Args:
            json (dict): JSON API response.

        Returns:
            GenericResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid = Common.msgid_from_json(json=json)
        raw = [int(x, 16) for x in Common.generic_rdata_from_json(json=json).split('.')]
        nadr = raw[ResponsePacketMembers.NADR]
        pnum = raw[ResponsePacketMembers.PNUM]
        pcmd = raw[ResponsePacketMembers.PCMD]
        hwpid = Common.hwpid_from_dpa(raw[ResponsePacketMembers.HWPID_HI], raw[ResponsePacketMembers.HWPID_LO])
        rcode = raw[ResponsePacketMembers.RCODE]
        dpa_value = raw[ResponsePacketMembers.DPA_VALUE]
        pdata = raw[8:] if len(raw) > 8 else None
        return cls(nadr=nadr, pnum=pnum, pcmd=pcmd, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata,
                   msgid=msgid)
