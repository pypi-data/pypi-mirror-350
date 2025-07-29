"""Sensor Written Data parameters."""
from typing import List
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants


class SensorWrittenData:
    """Sensor Written Data class."""

    __slots__ = '_index', '_data'

    def __init__(self, index: int, data: List[int]):
        """Sensor Written Data constructor.

        Args:
            index (int): Sensor index.
            data (List[int]): Data to write.
        """
        self._validate(index=index, data=data)
        self._index = index
        self._data = data

    def _validate(self, index: int, data: List[int]):
        """Validate parameters.

        Args:
            index (int): Sensor index.
            data (List[int]): Data to write.
        """
        self._validate_index(index)
        self._validate_data(data)

    @staticmethod
    def _validate_index(index: int):
        """Validate sensor index parameter.

        Args:
            index (int): Sensor index.

        Raises:
            RequestParameterInvalidValueError: If index is less than 0 or greater than 31.
        """
        if not dpa_constants.SENSOR_INDEX_MIN <= index <= dpa_constants.SENSOR_INDEX_MAX:
            raise RequestParameterInvalidValueError('Index value should be between 0 and 31.')

    @property
    def index(self) -> int:
        """:obj:`int`: Sensor index.

        Getter and setter.
        """
        return self._index

    @index.setter
    def index(self, value: int):
        self._validate_index(value)
        self._index = value

    @staticmethod
    def _validate_data(data: List[int]):
        """Validate data to write.

        Args:
            data (List[int]): Data to write.

        Raises:
            RequestParameterInvalidValueError: If data contains values not in range from 0 to 255.
        """
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Data values should be between 0 and 255.')

    @property
    def data(self) -> List[int]:
        """:obj:`list` of :obj:`int`: Data to write.

        Getter and setter.
        """
        return self._data

    @data.setter
    def data(self, value: List[int]):
        self._validate_data(value)
        self._data = value

    def to_pdata(self) -> List[int]:
        """Serialize index and data to parameters.

        Returns:
            :obj:`list` of `int`: Serialized written data.
        """
        return [self.index] + self.data
