"""Confirmation module.

This module contains DPA Confirmation message class.
"""

from typing import List, Optional, Union
from iqrfpy.enums.commands import Command
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.utils.common import Common
from iqrfpy.utils.dpa import ResponsePacketMembers
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.utils.validators import DpaValidator

__all__ = ['Confirmation']


class Confirmation(IResponseGetterMixin):
    """Confirmation message class.

    DPA confirmation is used to confirm reception of DPA request by node device at coordinator.
    The message carries DPA value, request hops (number of hops used to deliver DPA request to node device),
    response hops (number of hops used to deliver DPA response from node device to coordinator),
    and timeslot (see DPA documentation for timeslot length calculation).
    """

    __slots__ = '_request_hops', '_response_hops', '_timeslot'

    def __init__(self, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int, dpa_value: int,
                 rcode: int, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Confirmation constructor.

        Args:
            nadr (int): Device address.
            pnum (Union[Peripheral, int]): Peripheral.
            pcmd (Union[Command, int]): Peripheral command.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            rcode (int, optional): Response code. Defaults to 128.
            dpa_value (int, optional): DPA value. Defaults to 0.
            pdata (List[int], optional): DPA response data. Defaults to None.
            result (dict, optional): JSON response data. Defaults to None.
        """
        super().__init__(
            nadr=nadr,
            pcmd=pcmd,
            pnum=pnum,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            pdata=pdata,
            result=result
        )
        self._request_hops: int = result['requestHops']
        self._response_hops: int = result['responseHops']
        self._timeslot: int = result['timeslot']

    @property
    def request_hops(self) -> int:
        """:obj:`int`: Request hops.

        Getter only.
        """
        return self._request_hops

    @property
    def response_hops(self) -> int:
        """:obj:`int`: Response hops.

        Getter only.
        """
        return self._response_hops

    @property
    def timeslot(self) -> int:
        """:obj:`int`: Timeslot.

        Getter only.
        """
        return self._timeslot

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'Confirmation':
        """Confirmation DPA factory method.

        Parses DPA confirmation message and constructs :obj:`Confirmation` object.

        Args:
            dpa (bytes): DPA confirmation bytes.

        Returns:
            :obj:`Confirmation`: Confirmation message object.
        """
        DpaValidator.confirmation_length(dpa=dpa)
        DpaValidator.confirmation_code(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        pnum = Common.pnum_from_dpa(dpa[ResponsePacketMembers.PNUM])
        pcmd = Common.request_pcmd_from_dpa(pnum, dpa[ResponsePacketMembers.PCMD])
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        pdata = list(dpa[8:])
        result = {'requestHops': dpa[8], 'responseHops': dpa[10], 'timeslot': dpa[9]}
        return cls(nadr=nadr, pnum=pnum, pcmd=pcmd, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value,
                   pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'Confirmation':
        """Confirmation JSON factory method.

        This method is not implemented as JSON API does not support standalone Confirmation messages.

        Raises:
            NotImplementedError: This method is not implemented.
        """
        raise NotImplementedError('from_json() method not implemented.')
