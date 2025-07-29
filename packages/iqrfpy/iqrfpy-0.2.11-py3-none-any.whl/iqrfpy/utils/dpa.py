"""DPA utility module.

This module contains DPA constants and enum classes.
"""

from .enums import IntEnumMember

__all__ = (
    'RequestPacketMembers',
    'ResponsePacketMembers',
    'COORDINATOR_NADR',
    'NADR_MIN',
    'NADR_MAX',
    'NODE_NADR_MIN',
    'NODE_NADR_MAX',
    'IQUIP_NADR',
    'PNUM_USER_MIN',
    'PNUM_USER_MAX',
    'PNUM_MAX',
    'REQUEST_PCMD_MIN',
    'REQUEST_PCMD_MAX',
    'RESPONSE_PCMD_MIN',
    'RESPONSE_PCMD_MAX',
    'HWPID_MIN',
    'HWPID_MAX',
    'CONFIRMATION_PACKET_LEN',
    'RESPONSE_GENERAL_LEN',
    'THERMOMETER_SENSOR_ERROR',
    'THERMOMETER_RESOLUTION',
    'MID_MIN',
    'MID_MAX',
    'LOCAL_DEVICE_ADDR',
    'IQMESH_TEMP_ADDR',
    'BROADCAST_ADDR',
    'BYTE_MIN',
    'BYTE_MAX',
    'WORD_MIN',
    'WORD_MAX',
    'PDATA_MAX_LEN',
    'EEEPROM_WRITE_MAX_DATA_LEN',
    'EEPROM_WRITE_MAX_DATA_LEN',
    'RAM_WRITE_MAX_DATA_LEN',
    'BACKUP_DATA_BLOCK_MAX_LEN',
    'SELECTED_NODES_LEN',
    'BINOUT_INDEX_MIN',
    'BINOUT_INDEX_MAX',
    'SENSOR_INDEX_MIN',
    'SENSOR_INDEX_MAX',
    'BaudRates',
    'ResponseCodes',
    'PeripheralTypes',
    'ExtendedPeripheralCharacteristics',
    'FrcCommands',
    'UserFrcCommands',
    'FrcResponseTimes',
    'IoConstants',
    'TrConfByteAddrs',
    'TrConfBitMasks',
    'OsLoadCodeAction',
    'OsLoadCodeType',
    'OsLoadCodeErrors',
    'OsLoadCodeResult',
    'McuTypes',
    'TrDTypes',
    'TrGTypes',
    'RfBands',
)


class RequestPacketMembers(IntEnumMember):
    """Request packet member indices."""

    NADR = 0
    PNUM = 2
    PCMD = 3
    HWPID_LO = 4
    HWPID_HI = 5


class ResponsePacketMembers(IntEnumMember):
    """Response packet member indices."""

    NADR = 0
    PNUM = 2
    PCMD = 3
    HWPID_LO = 4
    HWPID_HI = 5
    RCODE = 6
    DPA_VALUE = 7


# general constants
COORDINATOR_NADR = NADR_MIN = 0
NODE_NADR_MIN = 0x01
NADR_MAX = NODE_NADR_MAX = 0xEF
IQUIP_NADR = 0xF0
PNUM_USER_MIN = 0x20
PNUM_USER_MAX = 0x3E
PNUM_MAX = 0x7F
REQUEST_PCMD_MIN = 0
REQUEST_PCMD_MAX = 0x7F
RESPONSE_PCMD_MIN = 0x80
RESPONSE_PCMD_MAX = 0xFF
HWPID_MIN = 0
HWPID_MAX = 0xFFFF

# confirmation constants
CONFIRMATION_PACKET_LEN = 11

# response constants
RESPONSE_GENERAL_LEN = 8

# thermometer constants
THERMOMETER_SENSOR_ERROR = 0x80
THERMOMETER_RESOLUTION = 0.0625

# mid constants
MID_MIN = 0
MID_MAX = 0xFFFFFFFF

# other constants
IBK_LEN = 16
LOCAL_DEVICE_ADDR = 0xFC
IQMESH_TEMP_ADDR = 0xFE
BROADCAST_ADDR = 0xFF
BYTE_MIN = 0
BYTE_MAX = 255
WORD_MIN = 0
WORD_MAX = 65535

PDATA_MAX_LEN = 56
EEPROM_WRITE_MAX_DATA_LEN = 55
EEEPROM_WRITE_MAX_DATA_LEN = 54
RAM_WRITE_MAX_DATA_LEN = 55
BACKUP_DATA_BLOCK_MAX_LEN = 49
SELECTED_NODES_LEN = 30

SENSOR_INDEX_MIN = BINOUT_INDEX_MIN = 0
SENSOR_INDEX_MAX = BINOUT_INDEX_MAX = 31


class BaudRates(IntEnumMember):
    """UART baud rate constants."""

    B1200 = 0
    B2400 = 1
    B4800 = 2
    B9600 = 3
    B19200 = 4
    B38400 = 5
    B57600 = 6
    B115200 = 7
    B230400 = 8


# rcode constants
class ResponseCodes(IntEnumMember):
    """DPA response codes."""

    OK = 0
    ERROR_FAIL = 1
    ERROR_PCMD = 2
    ERROR_PNUM = 3
    ERROR_ADDR = 4
    ERROR_DATA_LEN = 5
    ERROR_DATA = 6
    ERROR_HWPID = 7
    ERROR_NADR = 8
    ERROR_IFACE_CUSTOM_HANDLER = 9
    ERROR_MISSING_CUSTOM_DPA_HANDLER = 10
    ERROR_USER_FROM = 0x20
    ERROR_USER_TO = 0x3F
    RESERVED_FLAG = 0x40
    ASYNC_RESPONSE = 0x80
    CONFIRMATION = 0xFF

    def __str__(self):
        """Convert self to representation of error code."""
        return self.to_string(self.value)

    @classmethod
    def is_ok_response(cls, rcode: int) -> bool:
        """Check if response code indicates OK response, including flags.

        Args:
            rcode (int): Response code to check.

        Returns:
            bool: True if response code indicates OK response, False otherwise.
        """
        return (rcode & ~cls.ASYNC_RESPONSE & ~cls.RESERVED_FLAG) == ResponseCodes.OK

    @classmethod
    def to_string(cls, value: int):
        """Convert value to string representation of error code.

        Args:
            value (int): Value to convert
        Returns:
            :obj:`str`: String representation of error code
        """
        if not BYTE_MIN <= value <= BYTE_MAX:
            return 'Invalid DPA response code'
        if cls.ERROR_USER_FROM <= value <= cls.ERROR_USER_TO:
            return 'User error code'
        flags = []
        if value != cls.CONFIRMATION:
            if value & 0x40:
                flags.append('reserved')
                value -= 0x40
            if value & 0x80:
                flags.append('async')
                value -= 0x80
        if value not in cls:
            return 'Unknown DPA response code'
        val = cls(value)
        str_val = None
        match val:
            case cls.OK:
                str_val = 'No error'
            case cls.ERROR_FAIL:
                str_val = 'General fail'
            case cls.ERROR_PCMD:
                str_val = 'Incorrect PCMD'
            case cls.ERROR_PNUM:
                str_val = 'Incorrect PNUM or PCMD'
            case cls.ERROR_ADDR:
                str_val = 'Incorrect Address'
            case cls.ERROR_DATA_LEN:
                str_val = 'Incorrect Data length'
            case cls.ERROR_DATA:
                str_val = 'Incorrect Data'
            case cls.ERROR_HWPID:
                str_val = 'Incorrect HW Profile ID used'
            case cls.ERROR_NADR:
                str_val = 'Incorrect NADR'
            case cls.ERROR_IFACE_CUSTOM_HANDLER:
                str_val = 'Data from interface consumed by Custom DPA Handler'
            case cls.ERROR_MISSING_CUSTOM_DPA_HANDLER:
                str_val = 'Custom DPA Handler is missing'
            case cls.CONFIRMATION:
                str_val = 'DPA confirmation'
        flag_str = '' if len(flags) == 0 else ''.join(f' [{flag}]' for flag in flags)
        return f'{str_val}{flag_str}'


class PeripheralTypes(IntEnumMember):
    """Peripheral type constants."""

    PERIPHERAL_TYPE_DUMMY = 0
    PERIPHERAL_TYPE_COORDINATOR = 1
    PERIPHERAL_TYPE_NODE = 2
    PERIPHERAL_TYPE_OS = 3
    PERIPHERAL_TYPE_EEPROM = 4
    PERIPHERAL_TYPE_BLOCK_EEPROM = 5
    PERIPHERAL_TYPE_RAM = 6
    PERIPHERAL_TYPE_LED = 7
    PERIPHERAL_TYPE_SPI = 8
    PERIPHERAL_TYPE_IO = 9
    PERIPHERAL_TYPE_UART = 10
    PERIPHERAL_TYPE_THERMOMETER = 11
    PERIPHERAL_TYPE_FRC = 14


class ExtendedPeripheralCharacteristics(IntEnumMember):
    """Extended peripheral characteristics constants."""

    PERIPHERAL_TYPE_EXTENDED_DEFAULT = 0
    PERIPHERAL_TYPE_EXTENDED_READ = 1
    PERIPHERAL_TYPE_EXTENDED_WRITE = 2
    PERIPHERAL_TYPE_EXTENDED_READ_WRITE = 3


class FrcCommands(IntEnumMember):
    """FRC command intervals."""

    FRC_2BIT_FROM = 0
    FRC_2BIT_TO = 0x7F
    FRC_1BYTE_FROM = 0x80
    FRC_1BYTE_TO = 0xDF
    FRC_2BYTE_FROM = 0xE0
    FRC_2BYTE_TO = 0xF7
    FRC_4BYTE_FROM = 0xF8
    FRC_4BYTE_TO = 0xFF


class UserFrcCommands(IntEnumMember):
    """User FRC command intervals."""

    USER_BIT_FROM = 0x40
    USER_BIT_TO = 0x7F
    USER_BYTE_FROM = 0xC0
    USER_BYTE_TO = 0xDF
    USER_2BYTE_FROM = 0xF0
    USER_2BYTE_TO = 0xFF
    USER_4BYTE_FROM = 0xFC
    USER_4BYTE_TO = 0xFF


class FrcResponseTimes(IntEnumMember):
    """FRC response time constants."""

    MS40 = 0
    MS360 = 16
    MS680 = 32
    MS1320 = 48
    MS2600 = 64
    MS5160 = 80
    MS10280 = 96
    MS20520 = 112


class IoConstants(IntEnumMember):
    """IO peripheral constants enum."""

    TRIS_A = PORT_A = 0x00
    TRIS_B = PORT_B = 0x01
    TRIS_C = PORT_C = 0x02
    TRIS_E = PORT_E = 0x04
    PULL_UP_A = 0x10
    PULL_UP_B = 0x11
    PULL_UP_C = 0x12
    PULL_UP_E = 0x14
    DELAY = 0xFF


class TrConfByteAddrs(IntEnumMember):
    """TR configuration memory block address enum."""

    DPA_CONFIG_BITS_0 = 0x05
    RF_OUTPUT_POWER = 0x08
    RF_SIGNAL_FILTER = 0x09
    LP_RF_TIMEOUT = 0x0A
    UART_BAUD_RATE = 0x0B
    ALTERNATIVE_DSM_CHANNEL = 0x0C
    DPA_CONFIG_BITS_1 = 0x0D
    RF_CHANNEL_A = 0x11
    RF_CHANNEL_B = 0x12


class TrConfBitMasks(IntEnumMember):
    """TR configuration bits enum."""

    CUSTOM_DPA_HANDLER = LOCAL_FRC = 1
    DPA_PEER_TO_PEER = 2
    ROUTING_OFF = 8
    IO_SETUP = 16
    USER_PEER_TO_PEER = 32
    STAY_AWAKE_WHEN_NOT_BONDED = 64
    STD_AND_LP_NETWORK = 128


class OsLoadCodeAction(IntEnumMember):
    """OS Load Code flags action enum."""

    VERIFY = 0
    VERIFY_AND_LOAD = 1


class OsLoadCodeType(IntEnumMember):
    """OS Load Code flags code type enum."""

    CUSTOM_DPA_HANDLER = 0
    IQRF_PLUGIN = 1
    IQRF_OS_CHANGE_FILE = 2


class OsLoadCodeResult(IntEnumMember):
    """OS Load Code result enum."""

    ERROR = 0
    NO_ERROR = 1


class OsLoadCodeErrors(IntEnumMember):
    """OS Load Code error enum."""

    RESERVED = -1
    HEX_IQRF_CHECKSUM_MISMATCH = 0
    OLD_OS_MISSING = 3
    IQRF_OS_CHANGE_CHECKSUM_MISMATCH = 4
    UNSUPPORTED_IQRF_OS_VERSION = 7


class McuTypes(IntEnumMember):
    """TR module MCU types enum."""

    PIC16LF1938 = 4
    PIC16LF18877 = 5

    def __str__(self):
        """String representation of MCU type as module code.

        PIC16LF1938 => D
        PIC16LF18877 => G

        Returns:
            str: MCU type code.
        """
        match self.value:
            case self.PIC16LF1938:
                return 'D'
            case self.PIC16LF18877:
                return 'G'

    @classmethod
    def get_mcu_code_str(cls, value: int) -> str:
        """Return MCU code associated with its type.

        Args:
            value (int): Value to get MCU code from.

        Returns:
            str: MCU code associated with its type ('D' for PIC16LF1938, 'G' for PIC16LF18877, or '?' for unknown).
        """
        if value in cls:
            return str(cls(value))
        else:
            return '?'


class TrDTypes(IntEnumMember):
    """TR module D types enum."""

    TR_52D = 0
    TR_58D_RJ = 1
    TR_72D = 2
    TR_53D = 3
    TR_78D = 4
    TR_54D = 8
    TR_55D = 9
    TR_56D = 10
    TR_76D = 11
    TR_77D = 12
    TR_75D = 13

    def __str__(self):
        """String representation of TR D type.

        TR_72D => TR-72D

        Returns:
           str: TR D type string.
        """
        return self.name.replace('_', '-')

    @classmethod
    def get_tr_series_str(cls, value: int) -> str:
        """Return TR D series string from integer value.

        Args:
            value (int): Value to get TR D series from.

        Returns:
            str: TR D series string.
        """
        if value in cls:
            return str(cls(value))
        else:
            return 'Unknown'


class TrGTypes(IntEnumMember):
    """TR module G types enum."""

    TR_82G = 0
    TR_72G = 2
    TR_85G = 9
    TR_86G = 10
    TR_76G = 11
    TR_75G = 13

    def __str__(self):
        """String representation of TR G type.

        TR_82G => TR-82G

        Returns:
            str: TR G type string.
        """
        return self.name.replace('_', '-')

    @classmethod
    def get_tr_series_str(cls, value: int) -> str:
        """Return TR G series string from integer value.

        Args:
            value (int): Value to get TR G series from.

        Returns:
            str: TR G series string.
        """
        if value in cls:
            return str(cls(value))
        else:
            return 'Unknown'


class RfBands(IntEnumMember):
    """RF bands enum."""

    RF_BAND_868 = 0
    RF_BAND_916 = 1
    RF_BAND_433 = 2
    RF_BAND_RESERVED = 3

    def __str__(self):
        """Convert to human-readable string representation.

        Example format 868 MHz.

        Returns:
            str: Human-readable RF Band string
        """
        if self.name == self.RF_BAND_RESERVED.name:
            return 'Reserved'
        return f'{self.name[8:]} MHz'
