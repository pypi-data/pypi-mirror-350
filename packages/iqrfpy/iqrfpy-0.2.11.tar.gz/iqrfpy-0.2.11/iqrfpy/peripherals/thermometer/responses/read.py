"""Thermometer Read response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import ThermometerResponseCommands
from iqrfpy.enums.message_types import ThermometerMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['ReadResponse']


class ReadResponse(IResponseGetterMixin):
    """Thermometer Read response class."""

    __slots__ = ('_temperature',)

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Read response constructor.

        Args:
            nadr (int): Device address.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            rcode (int, optional): Response code. Defaults to 128.
            dpa_value (int, optional): DPA value. Defaults to 0.
            pdata (List[int], optional): DPA response data. Defaults to None.
            msgid (str, optional): Message ID. Defaults to None.
            result (dict, optional): JSON response data. Defaults to None.
        """
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.THERMOMETER,
            pcmd=ThermometerResponseCommands.READ,
            m_type=ThermometerMessages.READ,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._temperature = result['temperature'] if rcode == ResponseCodes.OK else None

    @property
    def temperature(self) -> Optional[float]:
        """:obj:`float` or :obj:`None`: Measured temperature.

        Getter only.
        """
        return self._temperature

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'ReadResponse':
        """DPA response factory method.

        Parses DPA data and constructs :obj:`ReadResponse` object.

        Args:
            dpa (bytes): DPA response bytes.

        Returns:
            :obj:`ReadResponse`: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr, _, _, hwpid, rcode, dpa_value, pdata = Common.parse_dpa_into_members(dpa=dpa)
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=11)
            val = dpa[9] + (dpa[10] << 8)
            if dpa[8] > dpa_constants.THERMOMETER_SENSOR_ERROR:
                val = (val ^ 0xFFF) + 1
                val *= -1
            val *= dpa_constants.THERMOMETER_RESOLUTION
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {'temperature': val}
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'ReadResponse':
        """JSON response factory method.

        Parses JSON API response and constructs :obj:`ReadResponse` object.

        Args:
            json (dict): JSON API response.

        Returns:
            :obj:`ReadResponse`: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid, nadr, hwpid, rcode, dpa_value, pdata, result = Common.parse_json_into_members(json=json)
        return cls(nadr=nadr, msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, pdata=pdata, result=result)
