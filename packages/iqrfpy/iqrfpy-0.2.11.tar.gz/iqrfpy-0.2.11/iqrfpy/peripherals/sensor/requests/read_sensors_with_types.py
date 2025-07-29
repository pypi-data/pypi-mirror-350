"""Sensor Read Sensors With Types request message."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import SensorRequestCommands
from iqrfpy.enums.message_types import SensorMessages
from iqrfpy.enums.peripherals import Standards
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest
from iqrfpy.objects.sensor_written_data import SensorWrittenData

__all__ = [
    'ReadSensorsWithTypesRequest',
    'SensorWrittenData',
]


class ReadSensorsWithTypesRequest(IRequest):
    """Sensor Read Sensors With Types request class."""

    __slots__ = '_sensors', '_written_data'

    def __init__(self, nadr: int, sensors: Optional[List[int]] = None,
                 written_data: Optional[List[SensorWrittenData]] = None, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """Read Sensors With Types request constructor.

        Args:
            nadr (int): Device address.
            sensors (List[int], optional): List of sensor indexes to read. If left empty, only the first sensor is read.
            written_data (List[SensorWrittenData], optional): Data to write to sensors.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate_sensors(sensors)
        super().__init__(
            nadr=nadr,
            pnum=Standards.SENSOR,
            pcmd=SensorRequestCommands.READ_SENSORS_WITH_TYPES,
            m_type=SensorMessages.READ_SENSORS_WITH_TYPES,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._sensors = sensors
        self._written_data = written_data

    @staticmethod
    def _validate_sensors(sensors: Optional[List[int]] = None):
        """Validate sensors parameter.

        Args:
            sensors (List[int], optional): List of sensor indexes to read. If left empty, only the first sensor is read.

        Raises:
            RequestParameterInvalidValueError: If sensors contains more than 32 values or if values are not
                in range from 0 to 31.
        """
        if sensors is not None:
            if len(sensors) == 0:
                return
            if len(sensors) > 32:
                raise RequestParameterInvalidValueError('Sensors length should be at most 32 bytes.')
            if min(sensors) < 0 or max(sensors) > 31:
                raise RequestParameterInvalidValueError('Sensors values should be between 0 and 31.')

    @property
    def sensors(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int` or :obj:`None`: List of sensor indexes to read.

        If left empty, only the first sensor is read.

        Getter and setter.
        """
        return self._sensors

    @sensors.setter
    def sensors(self, value: Optional[List[int]] = None):
        self._validate_sensors(value)
        self._sensors = value

    @property
    def written_data(self) -> Optional[List[SensorWrittenData]]:
        """:obj:`list` of :obj:`SensorWrittenData` or :obj:`None`: Data to write to sensors.

        Getter and setter.
        """
        return self._written_data

    @written_data.setter
    def written_data(self, value: List[SensorWrittenData]):
        self._written_data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        if self._sensors is not None:
            written_data = []
            if self._written_data is not None:
                for data in self._written_data:
                    written_data += data.to_pdata()
            self._pdata = Common.indexes_to_4byte_bitmap(self._sensors) + written_data
        else:
            self._pdata = None
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        if self._sensors is not None:
            params = {
                'sensorIndexes': self._sensors
            }
            if self._written_data is not None:
                params['writtenData'] = [data.to_pdata() for data in self._written_data]
            self._params = params
        else:
            self._params = {}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
