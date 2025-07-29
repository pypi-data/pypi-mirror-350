"""OS Batch request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.objects.os_batch_data import OsBatchData
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = [
    'BatchRequest',
    'OsBatchData',
]


class BatchRequest(IRequest):
    """OS Batch request class."""

    __slots__ = ('_requests',)

    def __init__(self, nadr: int, requests: List[OsBatchData], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Batch request constructor.

        Args:
            nadr (int): Device address.
            requests (List[OsBatchData]): Batch request data.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(requests)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.BATCH,
            m_type=OSMessages.BATCH,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._requests = requests

    @staticmethod
    def _validate(requests: List[OsBatchData]):
        """Validate batch requests.

        Args:
            requests (List[OsBatchData]): Batch request data.
        """
        data = []
        for request in requests:
            data += request.to_pdata()
        if len(data) + 1 > dpa_constants.PDATA_MAX_LEN:
            raise RequestParameterInvalidValueError('Batch requests data should be no larger than 56B.')

    @property
    def requests(self) -> List[OsBatchData]:
        """:obj:`list` of :obj:`BatchData`: Batch request data.

        Getter and setter.
        """
        return self._requests

    @requests.setter
    def requests(self, value: List[OsBatchData]):
        self._validate(value)
        self._requests = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = []
        for request in self._requests:
            self._pdata += request.to_pdata()
        self._pdata.append(0)
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'requests': [request.to_json() for request in self._requests]}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
