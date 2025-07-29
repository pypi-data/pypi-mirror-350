"""Coordinator Restore request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['RestoreRequest']


class RestoreRequest(IRequest):
    """Coordinator Restore request class."""

    __slots__ = ('_network_data',)

    def __init__(self, network_data: List[int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Restore request constructor.

        Args:
            network_data (List[int]): Block of Coordinator network info data obtained by Backup request.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate_network_data(network_data)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.RESTORE,
            m_type=CoordinatorMessages.RESTORE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._network_data = network_data

    @staticmethod
    def _validate_network_data(network_data: List[int]):
        """Validates network data parameter.

        Args:
            network_data (List[int]): Block of Coordinator network info data obtained by Backup request.

        Raises:
            RequestParameterInvalidValueError: If network_data is longer than 49 bytes (values)
                or the values are not between 0 and 255.
        """
        if len(network_data) > dpa_constants.BACKUP_DATA_BLOCK_MAX_LEN:
            raise RequestParameterInvalidValueError('Network data should be at most 49 bytes long.')
        if not Common.values_in_byte_range(network_data):
            raise RequestParameterInvalidValueError('Network data block values should be between 0 and 255.')

    @property
    def network_data(self) -> List[int]:
        """:obj:`list` of :obj:`int`: Block of Coordinator network info data obtained by Backup request.

        Getter and setter.
        """
        return self._network_data

    @network_data.setter
    def network_data(self, value: List[int]) -> None:
        self._validate_network_data(value)
        self._network_data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = self._network_data
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'networkData': self._network_data}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
