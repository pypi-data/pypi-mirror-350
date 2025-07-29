"""FRC Send Selective request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import FrcRequestCommands
from iqrfpy.enums.message_types import FrcMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['SendSelectiveRequest']


class SendSelectiveRequest(IRequest):
    """FRC Send Selective request class."""

    __slots__ = '_frc_command', '_selected_nodes', '_user_data'

    def __init__(self, nadr: int, frc_command: int, selected_nodes: List[int], user_data: List[int],
                 hwpid: int = dpa_constants.HWPID_MAX, dpa_rsp_time: Optional[float] = None,
                 dev_process_time: Optional[float] = None, msgid: Optional[str] = None):
        """Send Selective request constructor.

        Args:
            nadr (int): Device address.
            frc_command (int): FRC command (data to collect).
            selected_nodes (List[int]): Selected nodes.
            user_data (List[int]): User data (see FRC commands for details).
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(frc_command, selected_nodes, user_data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.FRC,
            pcmd=FrcRequestCommands.SEND_SELECTIVE,
            m_type=FrcMessages.SEND_SELECTIVE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._frc_command = frc_command
        self._selected_nodes = selected_nodes
        self._user_data = user_data

    def _validate(self, frc_command: int, selected_nodes: List[int], user_data: List[int]):
        """Validate request parameters.

        Args:
            frc_command (int): FRC command (data to collect).
            selected_nodes (List[int]): Selected nodes.
            user_data (List[int]): User data (see FRC commands for details).
        """
        self._validate_frc_command(frc_command)
        self._validate_selected_nodes(selected_nodes)
        self._validate_user_data(user_data)

    @staticmethod
    def _validate_frc_command(frc_command: int):
        """Validate FRC command parameter.

        Args:
            frc_command (int): FRC command (data to collect).

        Raises:
            RequestParameterInvalidValueError: If frc_command is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= frc_command <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('FRC command value should be between 0 and 255.')

    @property
    def frc_command(self) -> int:
        """:obj:`int`: FRC command.

        Getter and setter.
        """
        return self._frc_command

    @frc_command.setter
    def frc_command(self, value: int):
        self._validate_frc_command(value)
        self._frc_command = value

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
    def _validate_user_data(user_data: List[int]):
        """Validate user data.

        Args:
            user_data (List[int]): User data (see FRC commands for details).

        Raises:
            RequestParameterInvalidValueError: If user_data contains more than 27 values or values are not
            in range from 0 to 255.
        """
        if len(user_data) > 27:
            raise RequestParameterInvalidValueError('User data should contain at most 27 values.')
        if not Common.values_in_byte_range(user_data):
            raise RequestParameterInvalidValueError('User data values should be between 0 and 255.')

    @property
    def user_data(self) -> List[int]:
        """:obj:`list` of :obj:`int`: User data.

        Getter and setter.
        """
        return self._user_data

    @user_data.setter
    def user_data(self, value: List[int]):
        self._validate_user_data(value)
        self._user_data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._frc_command] + Common.nodes_to_bitmap(self._selected_nodes) + self._user_data
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {
            'frcCommand': self._frc_command,
            'selectedNodes': self._selected_nodes,
            'userData': self._user_data
        }
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
