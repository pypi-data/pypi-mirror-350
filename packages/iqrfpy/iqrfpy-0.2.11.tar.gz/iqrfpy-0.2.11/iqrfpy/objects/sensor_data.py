"""Sensor data class."""
from dataclasses import dataclass
from typing import List, Union

from iqrfpy.utils.sensor_constants import SensorTypes, SensorFrcErrors


@dataclass
class SensorData:
    """Class representing Sensor (quantity) information and value."""

    __slots__ = 'sensor_type', 'index', 'name', 'short_name', 'unit', 'decimal_places', 'frc_commands', 'value'

    sensor_type: SensorTypes
    index: int
    name: str
    short_name: str
    unit: str
    decimal_places: int
    frc_commands: List[int]
    value: Union[int, float, List[int], SensorFrcErrors, None]

    def __init__(self, sensor_type: SensorTypes, index: int, name: str,
                 short_name: str, unit: str, decimal_places: int, frc_commands: List[int],
                 value: Union[int, float, List[int], SensorFrcErrors, None] = None):
        """Class representing Sensor (quantity) information and value.

        Args:
            sensor_type (SensorTypes): Sensor type (represents a quantity).
            index (int): Index of sensor.
            name (str): Quantity name.
            short_name (str): Short quantity name.
            unit (str): Quantity unit.
            decimal_places (int): Precision.
            frc_commands (List[int]): Implemented FRC commands.
            value (Union[int, float, List[int], SensorFrcErrors, None]): Measured value.
        """
        self.sensor_type = sensor_type
        """Sensor type (represents a quantity)."""
        self.index = index
        """Index of sensor."""
        self.name = name
        """Quantity name"""
        self.short_name = short_name
        """Short quantity name."""
        self.unit = unit
        """Quantity unit."""
        self.decimal_places = decimal_places
        """Precision."""
        self.frc_commands = frc_commands
        """Implemented FRC commands."""
        self.value = value
        """Measured value."""
