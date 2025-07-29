"""Generic request message."""

import math
from typing import List, Optional, Union
from iqrfpy.enums.commands import Command
from iqrfpy.enums.message_types import GenericMessages
from iqrfpy.enums.peripherals import Peripheral
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['GenericRequest']


class GenericRequest(IRequest):
    """Generic request class."""

    def __init__(self, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int],
                 hwpid: int = dpa_constants.HWPID_MAX, pdata: Optional[List[int]] = None,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Generic request constructor.

        Args:
            nadr (int): Device address.
            pnum (Union[Peripheral, int]): Peripheral number.
            pcmd (Union[Command, int]): Peripheral command.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            pdata (List[int], optional): Request data.
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        super().__init__(
            nadr=nadr,
            pnum=pnum,
            pcmd=pcmd,
            m_type=GenericMessages.RAW,
            hwpid=hwpid,
            pdata=pdata,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        dpa: List[int] = [self._nadr, 0, self._pnum, self._pcmd, self._hwpid & 0xFF, (self._hwpid >> 8) & 0xFF]
        if self._pdata is not None:
            dpa.extend(self._pdata)
        json: dict = {
            'mType': self._mtype.value,
            'data': {
                'msgId': self._msgid,
                'req': {
                    'rData': '.'.join([f'{x:02x}' for x in dpa])
                },
                'returnVerbose': True,
            },
        }
        if self._dpa_rsp_time is not None:
            json['data']['timeout'] = math.ceil(self._dpa_rsp_time * 1000)
        return json
