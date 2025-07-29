"""Quantity data module.

This module contains Quantity dataclasses used when parsing Sensor data.
"""

from dataclasses import dataclass
from typing import Union
from iqrfpy.exceptions import UnknownSensorTypeError
from iqrfpy.utils.sensor_constants import SensorTypes, SensorFrcCommands

__all__ = [
    'Temperature',
    'CO2',
    'VOC',
    'ExtraLowVoltage',
    'EarthsMagneticField',
    'LowVoltage',
    'Current',
    'Power',
    'MainsFrequency',
    'TimeSpan',
    'Illuminance',
    'NO2',
    'SO2',
    'CO',
    'O3',
    'AtmosphericPressure',
    'ColorTemperature',
    'ParticulatesPM2_5',
    'SoundPressureLevel',
    'Altitude',
    'Acceleration',
    'NH3',
    'Methane',
    'ShortLength',
    'ParticulatesPM1',
    'ParticulatesPM4',
    'ParticulatesPM10',
    'TVOC',
    'NOX',
    'ActivityConcentration',
    'RelativeHumidity',
    'BinaryData7',
    'PowerFactor',
    'UVIndex',
    'PH',
    'RSSI',
    'Action',
    'BinaryData30',
    'Consumption',
    'Datetime',
    'TimeSpanLong',
    'Latitude',
    'Longitude',
    'TemperatureFloat',
    'Length',
    'DataBlock',
    'get_sensor_class'
]


@dataclass
class Temperature:
    """Temperature dataclass."""

    type = SensorTypes.TEMPERATURE
    name = 'Temperature'
    short_name = 'T'
    unit = '˚C'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE,
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class CO2:
    """Carbon dioxide dataclass."""

    type = SensorTypes.CO2
    name = 'Carbon dioxide'
    short_name = 'CO2'
    unit = 'ppm'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE,
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class VOC:
    """Volatile organic compound dataclass."""

    type = SensorTypes.VOC
    name = 'Volatile organic compound'
    short_name = 'VOC'
    unit = 'ppm'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE,
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class ExtraLowVoltage:
    """Extra-low voltage dataclass."""

    type = SensorTypes.EXTRA_LOW_VOLTAGE
    name = 'Extra-low voltage'
    short_name = 'U'
    unit = 'V'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class EarthsMagneticField:
    """Earth's magnetic field dataclass."""

    type = SensorTypes.EARTHS_MAGNETIC_FIELD
    name = "Earth's magnetic field"
    short_name = 'B'
    unit = 'T'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class LowVoltage:
    """Low voltage dataclass."""

    type = SensorTypes.LOW_VOLTAGE
    name = 'Low voltage'
    short_name = 'U'
    unit = 'V'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class Current:
    """Current dataclass."""

    type = SensorTypes.CURRENT
    name = 'Current'
    short_name = 'I'
    unit = 'A'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class Power:
    """Power dataclass."""

    type = SensorTypes.POWER
    name = 'Power'
    short_name = 'P'
    unit = 'W'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class MainsFrequency:
    """Mains frequency dataclass."""

    type = SensorTypes.MAINS_FREQUENCY
    name = 'Mains frequency'
    short_name = 'f'
    unit = 'Hz'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class TimeSpan:
    """Timespan dataclass."""

    type = SensorTypes.TIMESPAN
    name = 'Timespan'
    short_name = 't'
    unit = 's'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class Illuminance:
    """Illuminance dataclass."""

    type = SensorTypes.ILLUMINANCE
    name = 'Illuminance'
    short_name = 'Ev'
    unit = 'lx'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class NO2:
    """Nitrogen dioxide dataclass."""

    type = SensorTypes.NO2
    name = 'Nitrogen dioxide'
    short_name = 'NO2'
    unit = 'ppm'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class SO2:
    """Sulfur dioxide dataclass."""

    type = SensorTypes.SO2
    name = 'Sulfur dioxide'
    short_name = 'SO2'
    unit = 'ppm'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class CO:
    """Carbon monoxide dataclass."""

    type = SensorTypes.CO
    name = 'Carbon monoxide'
    short_name = 'CO'
    unit = 'ppm'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class O3:
    """Ozone dataclass."""

    type = SensorTypes.O3
    name = 'Ozone'
    short_name = 'O3'
    unit = 'ppm'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class AtmosphericPressure:
    """Atmospheric pressure dataclass."""

    type = SensorTypes.ATMOSPHERIC_PRESSURE
    name = 'Atmospheric pressure'
    short_name = 'p'
    unit = 'hPa'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class ColorTemperature:
    """Color temperature dataclass."""

    type = SensorTypes.COLOR_TEMPERATURE
    name = 'Color temperature'
    short_name = 'Tc'
    unit = 'K'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class ParticulatesPM2_5:
    """Particulates PM2.5 dataclass."""

    type = SensorTypes.PARTICULATES_PM2_5
    name = 'Particulates PM2.5'
    short_name = 'PM2.5'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class SoundPressureLevel:
    """Sound pressure level dataclass."""

    type = SensorTypes.SOUND_PRESSURE_LEVEL
    name = 'Sound pressure level'
    short_name = 'Lp'
    unit = 'dB'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class Altitude:
    """Altitude dataclass."""

    type = SensorTypes.ALTITUDE
    name = 'Altitude'
    short_name = 'h'
    unit = 'm'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class Acceleration:
    """Acceleration dataclass."""

    types = SensorTypes.ACCELERATION
    name = 'Acceleration'
    short_name = 'a'
    unit = 'm/s2'
    decimal_places = 8
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class NH3:
    """Ammonia dataclass."""

    types = SensorTypes.NH3
    name = 'Ammonia'
    short_name = 'NH3'
    unit = 'ppm'
    decimal_places = 1
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class Methane:
    """Methane dataclass."""

    type = SensorTypes.METHANE
    name = 'Methane'
    short_name = 'CH4'
    unit = '%'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class ShortLength:
    """Short length dataclass."""

    type = SensorTypes.SHORT_LENGTH
    name = 'Short length'
    short_name = 'l'
    unit = 'm'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class ParticulatesPM1:
    """Particulates PM1 dataclass."""

    type = SensorTypes.PARTICULATES_PM1
    name = 'Particulates PM1'
    short_name = 'PM1'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class ParticulatesPM4:
    """Particulates PM4 dataclass."""

    type = SensorTypes.PARTICULATES_PM4
    name = 'Particulates PM4'
    short_name = 'PM4'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class ParticulatesPM10:
    """Particulates PM10 dataclass."""

    type = SensorTypes.PARTICULATES_PM10
    name = 'Particulates PM10'
    short_name = 'PM10'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class TVOC:
    """Total volatile organic compound dataclass."""

    type = SensorTypes.TVOC
    name = 'Total volatile organic compound'
    short_name = 'TVOC'
    unit = 'µg/m3'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class NOX:
    """Nitrogen oxides dataclass."""

    type = SensorTypes.NOX
    name = 'Nitrogen oxides'
    short_name = 'NOX'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class ActivityConcentration:
    """Activity concentration dataclass."""

    type = SensorTypes.ACTIVITY_CONCENTRATION
    name = 'Activity concentration'
    short_name = 'CA'
    unit = 'Bq/m3'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class ParticulatesPM40:
    """Particulates PM40 dataclass."""

    type = SensorTypes.PARTICULATES_PM40
    name = 'Particulates PM40'
    short_name = 'PM40'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class RelativeHumidity:
    """Relative humidity dataclass."""

    type = SensorTypes.RELATIVE_HUMIDITY
    name = 'Relative humidity'
    short_name = 'RH'
    unit = '%'
    decimal_places = 1
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


@dataclass
class BinaryData7:
    """Binary data 7 dataclass."""

    type = SensorTypes.BINARYDATA7
    name = 'Binary data7'
    short_name = 'bin7'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BITS,
        SensorFrcCommands.FRC_1BYTE
    ]


@dataclass
class PowerFactor:
    """Power factor dataclass."""

    type = SensorTypes.POWER_FACTOR
    name = 'Power factor'
    short_name = 'cos θ'
    unit = ''
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


@dataclass
class UVIndex:
    """UV index dataclass."""

    type = SensorTypes.UV_INDEX
    name = 'UV index'
    short_name = 'UV'
    unit = ''
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


@dataclass
class PH:
    """PH dataclass."""

    type = SensorTypes.PH
    name = 'pH'
    short_name = 'pH'
    unit = ''
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


@dataclass
class RSSI:
    """RSSI dataclass."""

    type = SensorTypes.RSSI
    name = 'RSSI'
    short_name = 'RSSI'
    unit = 'dBm'
    decimal_places = 1
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


@dataclass
class Action:
    """Action dataclass."""

    type = SensorTypes.ACTION
    name = 'Action'
    short_name = 'Action'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


@dataclass
class BinaryData30:
    """Binary data 30 dataclass."""

    type = SensorTypes.BINARYDATA30
    name = 'Binary data30'
    short_name = 'bin30'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES,
        SensorFrcCommands.FRC_4BYTES
    ]


@dataclass
class Consumption:
    """Consumption dataclass."""

    type = SensorTypes.CONSUMPTION
    name = 'Consumption'
    short_name = 'E'
    unit = 'Wh'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


@dataclass
class Datetime:
    """Datetime dataclass."""

    type = SensorTypes.DATETIME
    name = 'DateTime'
    short_name = 'DateTime'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


@dataclass
class TimeSpanLong:
    """Timespan long dataclass."""

    type = SensorTypes.TIMESPAN_LONG
    name = 'Timespan long'
    short_name = 't'
    unit = 's'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


@dataclass
class Latitude:
    """Latitude dataclass."""

    type = SensorTypes.LATITUDE
    name = 'Latitude'
    short_name = 'LAT'
    unit = '°'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


@dataclass
class Longitude:
    """Longitude dataclass."""

    type = SensorTypes.LONGITUDE
    name = 'Longitude'
    short_name = 'LONG'
    unit = '°'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


@dataclass
class TemperatureFloat:
    """Temperature float dataclass."""

    type = SensorTypes.TEMPERATURE_FLOAT
    name = 'Temperature'
    short_name = 'T'
    unit = '˚C'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


@dataclass
class Length:
    """Length dataclass."""

    type = SensorTypes.LENGTH
    name = 'Length'
    short_name = 'l'
    unit = 'm'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


@dataclass
class DataBlock:
    """Data block dataclass."""

    type = SensorTypes.DATA_BLOCK
    name = 'Data block'
    short_name = 'datablock'
    unit = ''
    decimal_places = 0
    frc_commands = []


_type_classes = {
    SensorTypes.TEMPERATURE: Temperature,
    SensorTypes.CO2: CO2,
    SensorTypes.VOC: VOC,
    SensorTypes.EXTRA_LOW_VOLTAGE: ExtraLowVoltage,
    SensorTypes.EARTHS_MAGNETIC_FIELD: EarthsMagneticField,
    SensorTypes.LOW_VOLTAGE: LowVoltage,
    SensorTypes.CURRENT: Current,
    SensorTypes.POWER: Power,
    SensorTypes.MAINS_FREQUENCY: MainsFrequency,
    SensorTypes.TIMESPAN: TimeSpan,
    SensorTypes.ILLUMINANCE: Illuminance,
    SensorTypes.NO2: NO2,
    SensorTypes.SO2: SO2,
    SensorTypes.CO: CO,
    SensorTypes.O3: O3,
    SensorTypes.ATMOSPHERIC_PRESSURE: AtmosphericPressure,
    SensorTypes.COLOR_TEMPERATURE: ColorTemperature,
    SensorTypes.PARTICULATES_PM2_5: ParticulatesPM2_5,
    SensorTypes.SOUND_PRESSURE_LEVEL: SoundPressureLevel,
    SensorTypes.ALTITUDE: Altitude,
    SensorTypes.ACCELERATION: Acceleration,
    SensorTypes.NH3: NH3,
    SensorTypes.METHANE: Methane,
    SensorTypes.SHORT_LENGTH: ShortLength,
    SensorTypes.PARTICULATES_PM1: ParticulatesPM1,
    SensorTypes.PARTICULATES_PM4: ParticulatesPM4,
    SensorTypes.PARTICULATES_PM10: ParticulatesPM10,
    SensorTypes.TVOC: TVOC,
    SensorTypes.NOX: NOX,
    SensorTypes.ACTIVITY_CONCENTRATION: ActivityConcentration,
    SensorTypes.PARTICULATES_PM40: ParticulatesPM40,
    SensorTypes.RELATIVE_HUMIDITY: RelativeHumidity,
    SensorTypes.BINARYDATA7: BinaryData7,
    SensorTypes.POWER_FACTOR: PowerFactor,
    SensorTypes.UV_INDEX: UVIndex,
    SensorTypes.PH: PH,
    SensorTypes.RSSI: RSSI,
    SensorTypes.ACTION: Action,
    SensorTypes.BINARYDATA30: BinaryData30,
    SensorTypes.CONSUMPTION: Consumption,
    SensorTypes.DATETIME: Datetime,
    SensorTypes.TIMESPAN_LONG: TimeSpanLong,
    SensorTypes.LATITUDE: Latitude,
    SensorTypes.LONGITUDE: Longitude,
    SensorTypes.TEMPERATURE_FLOAT: TemperatureFloat,
    SensorTypes.LENGTH: Length,
    SensorTypes.DATA_BLOCK: DataBlock,
}


def get_sensor_class(sensor_type: Union[SensorTypes, int]):
    """Return quantity class corresponding to sensor type.

    Args:
        sensor_type (Union[SensorTypes, int]): Sensor type (represents a quantity)

    Returns:
        Quantity dataclass
    Raises:
        UnknownSensorTypeError: Raised if sensor type is passed as integer and the value is not recognized
        ValueError: Raised if sensor type is recognized, but corresponding quantity data is missing
    """
    if sensor_type not in SensorTypes:
        raise UnknownSensorTypeError(f'Unknown or unsupported sensor type: {sensor_type}')
    if sensor_type not in _type_classes:
        raise ValueError(f'Quantity data not available for sensor type: {sensor_type}')
    return _type_classes[sensor_type]
