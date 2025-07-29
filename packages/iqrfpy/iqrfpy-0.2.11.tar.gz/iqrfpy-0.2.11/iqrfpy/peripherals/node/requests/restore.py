"""Node Restore request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import NodeRequestCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['RestoreRequest']


class RestoreRequest(IRequest):
    """Node Restore request class."""

    __slots__ = ('_backup_data',)

    def __init__(self, nadr: int, backup_data: List[int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Restore request constructor.

        Args:
            nadr (int): Device address.
            backup_data (List[int]): Backup data.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(backup_data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeRequestCommands.RESTORE,
            m_type=NodeMessages.RESTORE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._backup_data = backup_data

    @staticmethod
    def _validate(backup_data: List[int]):
        """Validate backup data.

        Args:
            backup_data (List[int]): Backup data.

        Raises:
            RequestParameterInvalidValueError: If backup_data is longer than 49 values or values are not
                in range from 0 to 255.
        """
        if len(backup_data) > dpa_constants.BACKUP_DATA_BLOCK_MAX_LEN:
            raise RequestParameterInvalidValueError('Backup data should be at most 49 bytes long.')
        if not Common.values_in_byte_range(backup_data):
            raise RequestParameterInvalidValueError('Backup data block values should be between 0 and 255.')

    @property
    def backup_data(self) -> List[int]:
        """:obj:`list` of :obj:`int`: Backup data.

        Getter and setter.
        """
        return self._backup_data

    @backup_data.setter
    def backup_data(self, value: List[int]) -> None:
        self._validate(value)
        self._backup_data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = self._backup_data
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'backupData': self._backup_data}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
