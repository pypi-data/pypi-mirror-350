"""OS Write TR Configuration request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest
from iqrfpy.objects.os_tr_conf_data import OsTrConfData

__all__ = [
    'WriteTrConfRequest',
    'OsTrConfData',
]


class WriteTrConfRequest(IRequest):
    """OS Write TR Configuration request class."""

    __slots__ = '_configuration', '_rfpgm'

    def __init__(self, nadr: int, configuration: OsTrConfData, rfpgm: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Write TR Configuration request constructor.

        Args:
            nadr (int): Device address.
            configuration (OsTrConfData): TR Configuration.
            rfpgm (int): RFPGM parameters.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate_rfpgm(rfpgm=rfpgm)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.WRITE_CFG,
            m_type=OSMessages.WRITE_CFG,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._configuration = configuration
        self._rfpgm = rfpgm

    @staticmethod
    def _validate_rfpgm(rfpgm: int) -> None:
        """Validate RFPGM parameter.

        Args:
            rfpgm (int): RFPGM parameters.
        """
        if not dpa_constants.BYTE_MIN <= rfpgm <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('RFPGM should be a value between 0 and 255.')

    @property
    def configuration(self) -> OsTrConfData:
        """:obj:`OsTrConfData`: TR Configuration.

        Getter and setter.
        """
        return self._configuration

    @configuration.setter
    def configuration(self, value: OsTrConfData) -> None:
        self._configuration = value

    @property
    def rfpgm(self) -> int:
        """:obj:`int`: RFPGM parameters.

        Getter and setter.
        """
        return self._rfpgm

    @rfpgm.setter
    def rfpgm(self, value: int) -> None:
        self._validate_rfpgm(value)
        self._rfpgm = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [0] + self._configuration.to_pdata() + [self._rfpgm]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {
            'checksum': 0,
            'configuration': self._configuration.to_pdata(),
            'rfpgm': self._rfpgm,
        }
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
