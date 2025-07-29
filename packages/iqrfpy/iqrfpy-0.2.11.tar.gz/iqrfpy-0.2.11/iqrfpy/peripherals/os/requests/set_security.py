"""OS Set Security request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.objects import OsSecurityTypeParam
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = [
    'SetSecurityRequest',
    'OsSecurityTypeParam',
]


class SetSecurityRequest(IRequest):
    """OS Set Security request class."""

    __slots__ = '_security_type', '_data'

    def __init__(self, nadr: int, security_type: Union[OsSecurityTypeParam, int], data: List[int],
                 hwpid: int = dpa_constants.HWPID_MAX, dpa_rsp_time: Optional[float] = None,
                 dev_process_time: Optional[float] = None, msgid: Optional[str] = None):
        """Set Security request constructor.

        Args:
            nadr (int): Device address.
            security_type (Union[OsSecurityTypeParam, int]): Security type.
            data (List[int]): Security data.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(security_type, data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.SET_SECURITY,
            m_type=OSMessages.SET_SECURITY,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._security_type = security_type
        self._data = data

    def _validate(self, security_type: Union[OsSecurityTypeParam, int], data: List[int]):
        """Validate request parameters.

        Args:
            security_type (Union[OsSecurityTypeParam, int]): Security type.
            data (List[int]): Security data.
        """
        self._validate_security_type(security_type)
        self._validate_data(data)

    @staticmethod
    def _validate_security_type(security_type: Union[OsSecurityTypeParam, int]):
        """Validate security type parameter.

        Args:
            security_type (Union[OsSecurityTypeParam, int]): Security type.

        Raises:
            RequestParameterInvalidValueError: If security_type is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= security_type <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Security type value should be between 0 and 255.')

    @property
    def security_type(self) -> Union[OsSecurityTypeParam, int]:
        """:obj:`OsSecurityTypeParam` or :obj:`int`: Security type.

        Getter and setter.
        """
        return self._security_type

    @security_type.setter
    def security_type(self, value: Union[OsSecurityTypeParam, int]):
        self._validate_security_type(value)
        self._security_type = value

    @staticmethod
    def _validate_data(data: List[int]):
        """Validate security data parameter.

        Args:
            data (List[int]): Security data.

        Raises:
            RequestParameterInvalidValueError: If data does not contain 16 values or if values are not
                in range from 0 to 255.
        """
        if len(data) != 16:
            raise RequestParameterInvalidValueError('Data should be a list of 16 values.')
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Data values should be between 0 and 255.')

    @property
    def data(self) -> List[int]:
        """:obj:`list` of :obj:`int`: Security data.

        Getter and setter.
        """
        return self._data

    @data.setter
    def data(self, value: List[int]):
        self._validate_data(value)
        self._data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._security_type] + self._data
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'type': self._security_type, 'data': self._data}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
