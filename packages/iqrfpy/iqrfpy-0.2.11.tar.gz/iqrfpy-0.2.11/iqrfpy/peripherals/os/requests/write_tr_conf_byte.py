"""OS Write TR Configuration Byte request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.objects.os_tr_conf_byte import OsTrConfByte
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = [
    'WriteTrConfByteRequest',
    'OsTrConfByte'
]


class WriteTrConfByteRequest(IRequest):
    """OS Write TR Configuration Byte request class."""

    __slots__ = ('_configuration_bytes',)

    def __init__(self, nadr: int, configuration_bytes: List[OsTrConfByte], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Write TR Configuration Byte request constructor.

        Args:
            nadr (int): Device address.
            configuration_bytes (List[OsTrConfByte]): TR Configuration bytes.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(configuration_bytes=configuration_bytes)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.WRITE_CFG_BYTE,
            m_type=OSMessages.WRITE_CFG_BYTE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._configuration_bytes = configuration_bytes

    @staticmethod
    def _validate(configuration_bytes: List[OsTrConfByte]) -> None:
        """Validate configuration bytes.

        Args:
            configuration_bytes (List[OsTrConfByte]): TR configuration bytes.
        """
        if len(configuration_bytes) > 18:
            raise RequestParameterInvalidValueError('Request can carry at most 18 configuration bytes.')

    @property
    def configuration_bytes(self) -> List[OsTrConfByte]:
        """:obj:`OsTrConfByte`: TR Configuration bytes.

        Getter and setter.
        """
        return self._configuration_bytes

    @configuration_bytes.setter
    def configuration_bytes(self, value: List[OsTrConfByte]) -> None:
        self._validate(configuration_bytes=value)
        self._configuration_bytes = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        data = []
        for byte in self._configuration_bytes:
            data += byte.to_pdata()
        self._pdata = data
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {
            'bytes': [byte.to_json() for byte in self._configuration_bytes]
        }
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
