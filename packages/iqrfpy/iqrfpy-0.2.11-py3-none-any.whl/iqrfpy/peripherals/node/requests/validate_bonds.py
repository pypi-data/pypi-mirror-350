"""Node Validate Bonds request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import NodeRequestCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.objects import NodeValidateBondsParams
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = [
    'ValidateBondsRequest',
    'NodeValidateBondsParams',
]


class ValidateBondsRequest(IRequest):
    """Node Validate Bonds request class."""

    __slots__ = ('_nodes',)

    def __init__(self, nadr: int, nodes: List[NodeValidateBondsParams], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Validate Bonds request constructor.

        Args:
            nadr (int): Device address.
            nodes (List[NodeValidateBondsParams]): List of node and mid pairs.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(nodes)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeRequestCommands.VALIDATE_BONDS,
            m_type=NodeMessages.VALIDATE_BONDS,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._nodes: List[NodeValidateBondsParams] = nodes

    @staticmethod
    def _validate(nodes: List[NodeValidateBondsParams]) -> None:
        """Validate nodes parameter.

        Args:
            nodes (List[NodeValidateBondsParams]): List of node and mid pairs.

        Raises:
            RequestParameterInvalidValueError: If length of nodes is 0 or greater than 11.
        """
        if len(nodes) == 0:
            raise RequestParameterInvalidValueError('At least one pair of address and MID is required.')
        if len(nodes) > 11:
            raise RequestParameterInvalidValueError('Request can carry at most 11 pairs of address and MID.')

    @property
    def nodes(self) -> list[NodeValidateBondsParams]:
        """:obj:`list` of :obj:`NodeValidateBondsParams`: List of node and mid pairs.

        Getter and setter.
        """
        return self._nodes

    @nodes.setter
    def nodes(self, value: List[NodeValidateBondsParams]) -> None:
        self._validate(value)
        self._nodes = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        pdata = []
        for node in self._nodes:
            pdata.append(node.bond_addr)
            pdata.append(node.mid & 0xFF)
            pdata.append((node.mid >> 8) & 0xFF)
            pdata.append((node.mid >> 16) & 0xFF)
            pdata.append((node.mid >> 24) & 0xFF)
        self._pdata = pdata
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'nodes': [{'bondAddr': node.bond_addr, 'mid': node.mid} for node in self._nodes]}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
