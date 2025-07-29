"""IO Direction request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import IORequestCommands
from iqrfpy.enums.message_types import IOMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest
from iqrfpy.objects.io_triplet import IoTriplet

__all__ = [
    'DirectionRequest',
    'IoTriplet',
]


class DirectionRequest(IRequest):
    """IO direction request class."""

    __slots__ = ('_triplets',)

    def __init__(self, nadr: int, triplets: List[IoTriplet], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Direction request constructor.

        Args:
            nadr (int): Device address.
            triplets (List[IoTriplet]): List of port, mask and value subcommands triplets.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate_triplets(triplets=triplets)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.IO,
            pcmd=IORequestCommands.DIRECTION,
            m_type=IOMessages.DIRECTION,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._triplets = triplets

    @staticmethod
    def _validate_triplets(triplets: List[IoTriplet]):
        """Validate IO subcommands triplets parameter.

        Args:
            triplets (List[IoTriplet]): List of port, mask and value subcommands triplets.

        Raises:
            RequestParameterInvalidValueError: If list contains more than 18 triplets.
        """
        if len(triplets) > 18:
            raise RequestParameterInvalidValueError('Request can carry at most 18 triplets.')

    @property
    def triplets(self) -> List[IoTriplet]:
        """:obj:`list` of :obj:`IoTriplet`: List of port, mask and value subcommands triplets.

        Getter and setter.
        """
        return self._triplets

    @triplets.setter
    def triplets(self, val: List[IoTriplet]):
        self._validate_triplets(triplets=val)
        self._triplets = val

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
        for triplet in self._triplets:
            pdata.extend([triplet.port, triplet.mask, triplet.value])
        self._pdata = pdata
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        ports = [{'port': triplet.port, 'mask': triplet.mask, 'value': triplet.value} for triplet in self._triplets]
        self._params = {'ports': ports}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
