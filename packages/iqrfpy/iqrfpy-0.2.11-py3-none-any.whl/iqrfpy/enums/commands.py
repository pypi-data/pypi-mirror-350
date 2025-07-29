"""Commands module.

This module contains embed peripherals and standards command enums.
"""

from ..utils.enums import IntEnumMember
from .peripherals import EmbedPeripherals

__all__ = [
    'Command',
    'ExplorationRequestCommands',
    'ExplorationRequestPeripheralCommand',
    'CoordinatorRequestCommands',
    'NodeRequestCommands',
    'OSRequestCommands',
    'EEPROMRequestCommands',
    'EEEPROMRequestCommands',
    'RAMRequestCommands',
    'LEDRequestCommands',
    'IORequestCommands',
    'ThermometerRequestCommands',
    'UartRequestCommands',
    'FrcRequestCommands',
    'DALIRequestCommands',
    'BinaryOutputRequestCommands',
    'SensorRequestCommands',
    'LightRequestCommands',
    'ExplorationResponseCommands',
    'ExplorationResponsePeripheralCommand',
    'CoordinatorResponseCommands',
    'NodeResponseCommands',
    'OSResponseCommands',
    'EEPROMResponseCommands',
    'EEEPROMResponseCommands',
    'RAMResponseCommands',
    'LEDResponseCommands',
    'IOResponseCommands',
    'ThermometerResponseCommands',
    'UartResponseCommands',
    'FrcResponseCommands',
    'DALIResponseCommands',
    'BinaryOutputResponseCommands',
    'SensorResponseCommands',
    'LightResponseCommands'
]


class Command(IntEnumMember):
    """DPA commands base enum."""


class ExplorationRequestCommands(Command):
    """Exploration request commands enum."""

    PERIPHERALS_ENUMERATION_INFORMATION = 63


class ExplorationRequestPeripheralCommand(Command):
    """More peripherals information peripheral commands enum."""

    PER_COORDINATOR = EmbedPeripherals.COORDINATOR
    PER_NODE = EmbedPeripherals.NODE
    PER_OS = EmbedPeripherals.OS
    PER_EEPROM = EmbedPeripherals.EEPROM
    PER_EEEPROM = EmbedPeripherals.EEEPROM
    PER_RAM = EmbedPeripherals.RAM
    PER_LEDR = EmbedPeripherals.LEDR
    PER_LEDG = EmbedPeripherals.LEDG
    PER_IO = EmbedPeripherals.IO
    PER_THERMOMETER = EmbedPeripherals.THERMOMETER
    PER_UART = EmbedPeripherals.UART
    PER_FRC = EmbedPeripherals.FRC


class CoordinatorRequestCommands(Command):
    """Coordinator request commands enum."""

    ADDR_INFO = 0
    DISCOVERED_DEVICES = 1
    BONDED_DEVICES = 2
    CLEAR_ALL_BONDS = 3
    BOND_NODE = 4
    REMOVE_BOND = 5
    DISCOVERY = 7
    SET_DPA_PARAMS = 8
    SET_HOPS = 9
    BACKUP = 11
    RESTORE = 12
    AUTHORIZE_BOND = 13
    SMART_CONNECT = 18
    SET_MID = 19


class NodeRequestCommands(Command):
    """Node request commands enum."""

    READ = 0
    REMOVE_BOND = 1
    BACKUP = 6
    RESTORE = 7
    VALIDATE_BONDS = 8


class OSRequestCommands(Command):
    """OS request commands enum."""

    READ = 0
    RESET = 1
    READ_CFG = 2
    RFPGM = 3
    SLEEP = 4
    BATCH = 5
    SET_SECURITY = 6
    INDICATE = 7
    RESTART = 8
    WRITE_CFG_BYTE = 9
    LOAD_CODE = 10
    SELECTIVE_BATCH = 11
    TEST_RF_SIGNAL = 12
    FACTORY_SETTINGS = 13
    WRITE_CFG = 15


class RAMRequestCommands(Command):
    """RAM request commands enum."""

    READ = 0
    WRITE = 1
    READ_ANY = 15


class EEPROMRequestCommands(Command):
    """EEPROM request commands enum."""

    READ = 0
    WRITE = 1


class EEEPROMRequestCommands(Command):
    """EEEPROM request commands enum."""

    READ = 2
    WRITE = 3


class LEDRequestCommands(Command):
    """LEDR/G request commands enum."""

    SET_OFF = 0
    SET_ON = 1
    PULSE = 3
    FLASHING = 4


class IORequestCommands(Command):
    """IO request commands enum."""

    DIRECTION = 0
    SET = 1
    GET = 2


class ThermometerRequestCommands(Command):
    """Thermometer request commands enum."""

    READ = 0


class UartRequestCommands(Command):
    """Uart request commands enum."""

    OPEN = 0
    CLOSE = 1
    WRITE_READ = 2
    CLEAR_WRITE_READ = 3


class FrcRequestCommands(Command):
    """FRC request commands enum."""

    SEND = 0
    EXTRA_RESULT = 1
    SEND_SELECTIVE = 2
    SET_PARAMS = 3


class DALIRequestCommands(Command):
    """DALI request commands enum."""

    SEND_REQUEST_COMMANDS = 0
    SEND_REQUEST_COMMANDS_ASYNC = 1
    FRC = -1


class BinaryOutputRequestCommands(Command):
    """BinaryOutput request commands enum."""

    SET_OUTPUT = 0
    ENUMERATE_OUTPUTS = 62


class SensorRequestCommands(Command):
    """Sensor request commands enum."""

    READ_SENSORS = 0
    READ_SENSORS_WITH_TYPES = 1
    ENUMERATE = 62
    FRC = -1


class LightRequestCommands(Command):
    """Light request commands enum."""

    SET_POWER = 0
    INCREMENT_POWER = 1
    DECREMENT_POWER = 2
    ENUMERATE = 62


class ExplorationResponseCommands(Command):
    """Exploration response commands enum."""

    PERIPHERALS_ENUMERATION_INFORMATION = 191
    MORE_PERIPHERALS_INFORMATION = 255


class ExplorationResponsePeripheralCommand(Command):
    """More peripherals information peripheral commands enum."""

    PER_COORDINATOR = EmbedPeripherals.COORDINATOR + 0x80
    PER_NODE = EmbedPeripherals.NODE + 0x80
    PER_OS = EmbedPeripherals.OS + 0x80
    PER_EEPROM = EmbedPeripherals.EEPROM + 0x80
    PER_EEEPROM = EmbedPeripherals.EEEPROM + 0x80
    PER_RAM = EmbedPeripherals.RAM + 0x80
    PER_LEDR = EmbedPeripherals.LEDR + 0x80
    PER_LEDG = EmbedPeripherals.LEDG + 0x80
    PER_IO = EmbedPeripherals.IO + 0x80
    PER_THERMOMETER = EmbedPeripherals.THERMOMETER + 0x80
    PER_UART = EmbedPeripherals.UART + 0x80
    PER_FRC = EmbedPeripherals.FRC + 0x80


class CoordinatorResponseCommands(Command):
    """Coordinator response commands enum."""

    ADDR_INFO = 128
    DISCOVERED_DEVICES = 129
    BONDED_DEVICES = 130
    CLEAR_ALL_BONDS = 131
    BOND_NODE = 132
    REMOVE_BOND = 133
    DISCOVERY = 135
    SET_DPA_PARAMS = 136
    SET_HOPS = 137
    BACKUP = 139
    RESTORE = 140
    AUTHORIZE_BOND = 141
    SMART_CONNECT = 146
    SET_MID = 147


class NodeResponseCommands(Command):
    """Node response commands enum."""

    READ = 128
    REMOVE_BOND = 129
    BACKUP = 134
    RESTORE = 135
    VALIDATE_BONDS = 136


class OSResponseCommands(Command):
    """OS response commands enum."""

    READ = 128
    RESET = 129
    READ_CFG = 130
    RFPGM = 131
    SLEEP = 132
    BATCH = 133
    SET_SECURITY = 134
    INDICATE = 135
    RESTART = 136
    WRITE_CFG_BYTE = 137
    LOAD_CODE = 138
    SELECTIVE_BATCH = 139
    TEST_RF_SIGNAL = 140
    FACTORY_SETTINGS = 141
    WRITE_CFG = 143


class RAMResponseCommands(Command):
    """RAM response commands enum."""

    READ = 128
    WRITE = 129
    READ_ANY = 143


class EEPROMResponseCommands(Command):
    """EEPROM response commands enum."""

    READ = 128
    WRITE = 129


class EEEPROMResponseCommands(Command):
    """EEEPROM response commands enum."""

    READ = 130
    WRITE = 131


class LEDResponseCommands(Command):
    """LEDR/G response commands enum."""

    SET_OFF = 128
    SET_ON = 129
    PULSE = 131
    FLASHING = 132


class IOResponseCommands(Command):
    """IO response commands enum."""

    DIRECTION = 128
    SET = 129
    GET = 130


class ThermometerResponseCommands(Command):
    """Thermometer response commands enum."""

    READ = 128


class UartResponseCommands(Command):
    """Uart response commands enum."""

    OPEN = 128
    CLOSE = 129
    WRITE_READ = 130
    CLEAR_WRITE_READ = 131


class FrcResponseCommands(Command):
    """FRC response commands enum."""

    SEND = 128
    EXTRA_RESULT = 129
    SEND_SELECTIVE = 130
    SET_PARAMS = 131


class DALIResponseCommands(Command):
    """DALI response commands enum."""

    SEND_REQUEST_COMMANDS = 128
    SEND_REQUEST_COMMANDS_ASYNC = 129
    FRC = -1


class BinaryOutputResponseCommands(Command):
    """BinaryOutput response commands enum."""

    SET_OUTPUT = 128
    ENUMERATE_OUTPUTS = 190


class SensorResponseCommands(Command):
    """Sensor response commands enum."""

    READ_SENSORS = 128
    READ_SENSORS_WITH_TYPES = 129
    ENUMERATE = 190
    FRC = -1


class LightResponseCommands(Command):
    """Light response commands enum."""

    SET_POWER = 128
    INCREMENT_POWER = 129
    DECREMENT_POWER = 130
    ENUMERATE = 190
