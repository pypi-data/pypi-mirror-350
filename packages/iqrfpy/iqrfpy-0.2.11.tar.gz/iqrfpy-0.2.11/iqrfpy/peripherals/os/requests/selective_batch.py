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
    'SelectiveBatchRequest',
    'OsBatchData',
]


class SelectiveBatchRequest(IRequest):
    """OS Selective Batch request class."""

    __slots__ = '_selected_nodes', '_requests'

    def __init__(self, nadr: int, selected_nodes: List[int], requests: List[OsBatchData],
                 hwpid: int = dpa_constants.HWPID_MAX, dpa_rsp_time: Optional[float] = None,
                 dev_process_time: Optional[float] = None, msgid: Optional[str] = None):
        """Selective Batch request constructor.

        Args:
            nadr (int): Device address.
            selected_nodes (List[int]): Selected nodes.
            requests (List[OsBatchData]): Batch request data.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(selected_nodes, requests)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.SELECTIVE_BATCH,
            m_type=OSMessages.SELECTIVE_BATCH,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._selected_nodes = selected_nodes
        self._requests = requests

    def _validate(self, selected_nodes: List[int], requests: List[OsBatchData]):
        """Validate request parameters.

        Args:
            selected_nodes (List[int]): Selected nodes.
            requests (List[OsBatchData]): Batch request data.
        """
        self._validate_selected_nodes(selected_nodes)
        self._validate_requests(requests)

    @staticmethod
    def _validate_selected_nodes(selected_nodes: List[int]):
        """Validate selected nodes parameter.

        Args:
            selected_nodes (List[int]): Selected nodes.

        Raises:
            RequestParameterInvalidValueError: If selected_nodes contains more than 240 values or values are not
            in range from 0 to 255.
        """
        if len(selected_nodes) > 240:
            raise RequestParameterInvalidValueError('Selected nodes should contain at most 240 values.')
        if min(selected_nodes) < 0 or max(selected_nodes) > 239:
            raise RequestParameterInvalidValueError('Selected nodes values should be between 1 and 239.')

    @property
    def selected_nodes(self) -> List[int]:
        """:obj:`list` of :obj:`int`: Selected nodes.

        Getter and setter.
        """
        return self._selected_nodes

    @selected_nodes.setter
    def selected_nodes(self, value: List[int]):
        self._validate_selected_nodes(value)
        self._selected_nodes = value

    @staticmethod
    def _validate_requests(requests: List[OsBatchData]):
        """Validate batch requests.

        Args:
            requests (List[OsBatchData]): Batch request data.
        """
        data = []
        for request in requests:
            data += request.to_pdata()
        if len(data) + 1 > dpa_constants.PDATA_MAX_LEN - dpa_constants.SELECTED_NODES_LEN:
            raise RequestParameterInvalidValueError('Batch requests data should be no larger than 26B.')

    @property
    def requests(self) -> List[OsBatchData]:
        """:obj:`list` of :obj:`OsBatchData`: Batch request data.

        Getter and setter.
        """
        return self._requests

    @requests.setter
    def requests(self, value: List[OsBatchData]):
        self._validate_requests(value)
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
        self._pdata = Common.nodes_to_bitmap(self._selected_nodes)
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
        self._params = {
            'selectedNodes': self._selected_nodes,
            'requests': [request.to_json() for request in self._requests]
        }
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
