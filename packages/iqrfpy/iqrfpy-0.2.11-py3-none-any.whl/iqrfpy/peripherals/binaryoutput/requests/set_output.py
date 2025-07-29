"""BinaryOutput Set Output request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import BinaryOutputRequestCommands
from iqrfpy.enums.message_types import BinaryOutputMessages
from iqrfpy.enums.peripherals import Standards
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.objects.binaryoutput_state import BinaryOutputState
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = (
    'SetOutputRequest',
    'BinaryOutputState',
)


class SetOutputRequest(IRequest):
    """BinaryOutput Set Output request class."""

    __slots__ = ('_binouts',)

    def __init__(self, nadr: int, binouts: Optional[List[BinaryOutputState]] = None,
                 hwpid: int = dpa_constants.HWPID_MAX, dpa_rsp_time: Optional[float] = None,
                 dev_process_time: Optional[float] = None, msgid: Optional[str] = None):
        """Enumerate request constructor.

        Args:
            nadr (int): Network address
            binouts (List[BinaryOutputState], optional): Binary output states to set.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate_binouts(binouts=binouts)
        super().__init__(
            nadr=nadr,
            pnum=Standards.BINARY_OUTPUT,
            pcmd=BinaryOutputRequestCommands.SET_OUTPUT,
            m_type=BinaryOutputMessages.SET_OUTPUT,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._binouts: List[BinaryOutputState] = binouts if binouts is not None else []
        self._binouts.sort(key=lambda x: x.index)

    @staticmethod
    def _validate_binouts(binouts: Optional[List[BinaryOutputState]] = None):
        """Validate binary output states parameter.

        Args:
            binouts (List[BinaryOutputState], optional): Binary output states to set.

        Raises:
            RequestParameterInvalidValueError: If binouts contains more than 32 values.
        """
        if binouts is None or len(binouts) == 0:
            return
        if len(binouts) > 32:
            raise RequestParameterInvalidValueError('Binouts length should be at most 32 values.')

    @property
    def binouts(self) -> Optional[List[BinaryOutputState]]:
        """:obj:`list` of :obj:`BinaryOutputState` or :obj:`None`: Binary output states to set.

        Getter and setter.
        """
        return self._binouts

    @binouts.setter
    def binouts(self, value: Optional[List[BinaryOutputState]] = None):
        self._validate_binouts(value)
        self._binouts = value if value is not None else []
        self._binouts.sort(key=lambda x: x.index)

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        binouts = sorted(self._binouts, key=lambda x: x.index)
        indexes = [bo.index for bo in binouts]
        states = [bo.state for bo in binouts]
        self._pdata = Common.indexes_to_4byte_bitmap(indexes) + states
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {
            'binOuts': [bo.to_json() for bo in self.binouts]
        }
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
