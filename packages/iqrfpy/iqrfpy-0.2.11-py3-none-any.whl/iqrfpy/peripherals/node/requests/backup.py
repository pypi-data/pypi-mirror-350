"""Node Backup request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import NodeRequestCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['BackupRequest']


class BackupRequest(IRequest):
    """Node Backup request class."""

    __slots__ = ('_index',)

    def __init__(self, nadr: int, index: int = 0, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Backup request constructor.

        Args:
            nadr (int): Device address.
            index (int): Data block index.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(index)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeRequestCommands.BACKUP,
            m_type=NodeMessages.BACKUP,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._index = index

    @staticmethod
    def _validate(index: int) -> None:
        """Validate data block index parameter.

        Args:
            index (int): Data block index.

        Raises:
            RequestParameterInvalidValueError: If index is less than 0 or greater than 255.
        """
        if index < dpa_constants.BYTE_MIN or index > dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Index value should be between 0 and 255.')

    @property
    def index(self) -> int:
        """:obj:`int`: Data block index.

        Getter and setter.
        """
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        self._validate(value)
        self._index = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._index]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'index': self._index}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
