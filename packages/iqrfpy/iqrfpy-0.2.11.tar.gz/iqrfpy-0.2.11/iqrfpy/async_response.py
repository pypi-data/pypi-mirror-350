"""Async response module.

This module contains Asynchronous DPA response class.
"""

from typing import List, Optional, Union
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.enums.commands import Command
from iqrfpy.enums.message_types import GenericMessages
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponsePacketMembers, ResponseCodes
from iqrfpy.utils.validators import DpaValidator

__all__ = ['AsyncResponse']


class AsyncResponse(IResponseGetterMixin):
    """Asynchronous response class.

    This class is used to capture and resolve asynchronous responses,
    as this is a generic response class, the data is only sent as string of bytes in hexadecimal
    representation separated by dots.
    """

    def __init__(self, nadr: int, pnum: Peripheral, pcmd: Command, hwpid: int = dpa_constants.HWPID_MAX,
                 rcode: int = 0x80, dpa_value: int = 0, pdata: Union[List[int], None] = None,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        """AsyncResponse constructor.

        Args:
            nadr (int): Device address.
            pnum (Peripheral): Peripheral.
            pcmd (Command): Peripheral command.
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
            pcmd=pcmd,
            m_type=GenericMessages.RAW,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            pdata=pdata,
            msgid=msgid,
            result=result
        )

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'AsyncResponse':
        """Asynchronous response DPA factory method.

        Parses DPA data and constructs :obj:`AsyncResponse` object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            :obj:`AsyncResponse`: Asynchronous response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        pnum = Common.pnum_from_dpa(dpa[ResponsePacketMembers.PNUM])
        pcmd = Common.request_pcmd_from_dpa(pnum, dpa[ResponsePacketMembers.PCMD])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        result = None
        if rcode == ResponseCodes.ASYNC_RESPONSE:
            if len(dpa) > 8:
                result = {'rData': list(dpa)}
        return cls(nadr=nadr, pnum=pnum, pcmd=pcmd, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value,
                   pdata=list(dpa), result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'AsyncResponse':
        """Asynchronous response JSON factory method.

        Parses JSON API response and constructs :obj:`AsyncResponse` object.

        Args:
            json (dict): JSON API response.

        Returns:
            :obj:`AsyncResponse`: Asynchronous response message object.
        """
        msgid = Common.msgid_from_json(json)
        result = json['data']['rsp']
        packet = result['rData'].replace('.', '')
        pdata = bytes.fromhex(packet)
        ldata = Common.hex_string_to_list(packet)
        nadr = ldata[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(ldata[ResponsePacketMembers.HWPID_HI], ldata[ResponsePacketMembers.HWPID_LO])
        pnum = Common.pnum_from_dpa(ldata[ResponsePacketMembers.PNUM])
        pcmd = Common.request_pcmd_from_dpa(pnum, ldata[ResponsePacketMembers.PCMD])
        rcode = ldata[ResponsePacketMembers.RCODE]
        dpa_value = ldata[ResponsePacketMembers.DPA_VALUE]
        return cls(nadr=nadr, pnum=pnum, pcmd=pcmd, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value,
                   pdata=list(pdata), msgid=msgid, result=result)
