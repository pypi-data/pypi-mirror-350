"""FRC Set FRC Params request message."""

from typing import Optional, Union
from iqrfpy.enums.commands import FrcRequestCommands
from iqrfpy.enums.message_types import FrcMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.irequest import IRequest
from iqrfpy.objects.frc_params import FrcParams
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common

__all__ = [
    'SetFrcParamsRequest',
    'FrcParams',
]


class SetFrcParamsRequest(IRequest):
    """FRC Set Frc Params request class."""

    __slots__ = ('_frc_params',)

    def __init__(self, nadr: int, frc_params: Union[FrcParams, int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Send request constructor.

        Args:
            nadr (int): Device address.
            frc_params (Union[FrcParams, int]): FRC parameters.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate(frc_params)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.FRC,
            pcmd=FrcRequestCommands.SET_PARAMS,
            m_type=FrcMessages.SET_PARAMS,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._frc_params = frc_params

    @staticmethod
    def _validate(frc_params: Union[FrcParams, int]):
        """Validate FRC params parameter.

        Args:
            frc_params (Union[FrcParams, int]): FRC parameters.

        Raises:
            RequestParameterInvalidValueError: If frc_params is less than 0 or greater than 255.
        """
        if isinstance(frc_params, int) and not dpa_constants.BYTE_MIN <= frc_params <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('FRC params value should be between 0 and 255.')

    @property
    def frc_params(self) -> FrcParams:
        """:obj:`FrcParams`: FRC parameters.

        Getter and setter.
        """
        return self._frc_params

    @frc_params.setter
    def frc_params(self, value: Union[FrcParams, int]):
        self._validate(value)
        self._frc_params = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        self._pdata = [self._frc_params if isinstance(self._frc_params, int) else self._frc_params.to_data()]
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {
            'frcResponseTime': self._frc_params if isinstance(self._frc_params, int) else self._frc_params.to_data()
        }
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
