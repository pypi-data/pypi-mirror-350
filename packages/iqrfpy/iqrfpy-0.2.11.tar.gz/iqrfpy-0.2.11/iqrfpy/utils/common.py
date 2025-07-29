"""Common utility module.

common module provides utilities and auxiliary methods for
extraction of data from DPA bytes and Daemon API JSON messages.
"""

__all__ = ['Common']

import math
from typing import List, Optional, Union
from iqrfpy.enums.commands import *
from iqrfpy.enums.message_types import *
from iqrfpy.enums.peripherals import *
from iqrfpy.exceptions import InvalidPeripheralValueError, InvalidPeripheralCommandValueError, \
    JsonMsgidMissingError, JsonMTypeMissingError, JsonNadrMissingError, JsonHwpidMissingError, JsonRCodeMissingError, \
    JsonDpaValueMissingError, JsonResultMissingError, JsonStatusMissingError, JsonGenericDataMissingError, \
    UnsupportedMessageTypeError, UnsupportedPeripheralError, UnsupportedPeripheralCommandError
import iqrfpy.utils.dpa as dpa_constants


class Common:
    """Common class provides auxiliary methods for handling DPA and Daemon API JSON messages."""

    # DPA

    @staticmethod
    def serialize_to_dpa(nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int = 0xFFFF,
                         pdata: Optional[List[int]] = None, mutable: bool = False):
        """Serialize request parameters into DPA packet.

        Args:
            nadr (int): Device address
            pnum (Union[Peripheral, int]): Peripheral.
            pcmd (Union[Command, int]): Peripheral command.
            hwpid (int): Hardware profile ID. Defaults to 65535
            pdata (List[int], optional): Request data.
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        dpa: List[int] = [nadr, 0, pnum, pcmd, hwpid & 0xFF, (hwpid >> 8) & 0xFF]
        if pdata is not None:
            dpa.extend(pdata)
        if mutable:
            return bytearray(dpa)
        return bytes(dpa)

    @staticmethod
    def hwpid_from_dpa(high: int, low: int) -> int:
        """Convert DPA HWPID bytes to a single 16bit unsigned integer.

        Args:
            high (int): HWPID high byte
            low (int): HWPID low byte
        Returns:
            :obj:`int`: 16bit unsigned integer HWPID value
        Raises:
            ValueError: Raised if input values are not between 0 and 255
        """
        if high > dpa_constants.BYTE_MAX or low > dpa_constants.BYTE_MAX:
            raise ValueError('Argument value exceeds maximum allowed value of 255.')
        if high < dpa_constants.BYTE_MIN or low < dpa_constants.BYTE_MIN:
            raise ValueError('Negative argument values are not allowed.')
        return (high << 8) + low

    @staticmethod
    def pnum_from_dpa(pnum: int) -> Union[Peripheral, int]:
        """Return peripheral enum value based on DPA peripheral data byte.

        Args:
            pnum (int): Peripheral number data byte
        Returns:
            :obj:`Peripheral` or :obj:`int`: Peripheral enum member
        Raises:
            InvalidPeripheralValueError: Raised if pnum value is not between 0 and 255
            UnsupportedPeripheralError: Raised if pnum parameter value is not recognized as a member of any
                peripheral enum
        """
        if pnum < 0 or pnum > 255:
            raise InvalidPeripheralValueError('Peripheral value out of range 0-255.')
        if pnum in EmbedPeripherals:
            return EmbedPeripherals(pnum)
        if pnum in Standards:
            return Standards(pnum)
        if dpa_constants.PNUM_USER_MIN <= pnum <= dpa_constants.PNUM_USER_MAX:
            return pnum
        raise UnsupportedPeripheralError('Unknown or unsupported peripheral.')

    @staticmethod
    def request_pcmd_from_dpa(pnum: Union[Peripheral, int], pcmd: int) -> Union[Command, int]:
        """Return request command based on DPA peripheral and command data byte.

        Args:
            pnum (Union[Peripheral, int]): Peripheral enum member
            pcmd (int): Command data byte value
        Returns:
            :obj:`Command` or :obj:`int`: Request command enum value
        Raises:
            InvalidPeripheralCommandValueError: Raised if pcmd is a negative value, or if pcmd is not a value
                between 0 and 127
            UnsupportedPeripheralError: Raised if pnum parameter value is not recognized as a member of any
                peripheral enum
            UnsupportedPeripheralCommandError: Raised if pcmd parameter value is not recognized as a member of any
                peripheral command enum
        """
        if pcmd < dpa_constants.REQUEST_PCMD_MIN:
            raise InvalidPeripheralCommandValueError('Negative peripheral command values are not allowed.')
        if pcmd > dpa_constants.REQUEST_PCMD_MAX:
            raise InvalidPeripheralCommandValueError('Peripheral command value exceeds maximum allowed value of 127.')
        if dpa_constants.PNUM_USER_MIN <= pnum <= dpa_constants.PNUM_USER_MAX:
            return pcmd
        commands = None
        match pnum:
            case EmbedPeripherals.COORDINATOR:
                commands = CoordinatorRequestCommands
            case EmbedPeripherals.NODE:
                commands = NodeRequestCommands
            case EmbedPeripherals.OS:
                commands = OSRequestCommands
            case EmbedPeripherals.EEPROM:
                commands = EEPROMRequestCommands
            case EmbedPeripherals.EEEPROM:
                commands = EEEPROMRequestCommands
            case EmbedPeripherals.RAM:
                commands = RAMRequestCommands
            case EmbedPeripherals.LEDR | EmbedPeripherals.LEDG:
                commands = LEDRequestCommands
            case EmbedPeripherals.IO:
                commands = IORequestCommands
            case EmbedPeripherals.THERMOMETER:
                commands = ThermometerRequestCommands
            case EmbedPeripherals.UART:
                commands = UartRequestCommands
            case EmbedPeripherals.FRC:
                commands = FrcRequestCommands
            case EmbedPeripherals.EXPLORATION:
                commands = ExplorationRequestCommands
            case Standards.DALI:
                commands = DALIRequestCommands
            case Standards.BINARY_OUTPUT:
                commands = BinaryOutputRequestCommands
            case Standards.SENSOR:
                commands = SensorRequestCommands
            case Standards.LIGHT:
                commands = LightRequestCommands
            case _:
                raise UnsupportedPeripheralError('Unknown or unsupported peripheral.')

        if commands is not None and pcmd in commands:
            return commands(pcmd)
        raise UnsupportedPeripheralCommandError('Unknown or unsupported peripheral command.')

    @staticmethod
    def response_pcmd_from_dpa(pnum: Union[Peripheral, int], pcmd: int) -> Union[Command, int]:
        """Return response command based on DPA peripheral and command data byte.

        Args:
            pnum (Union[Peripheral, int]): Peripheral enum member
            pcmd (int): Command data byte value
        Returns:
            :obj:`Command` or :obj:`int`: Response command enum member
        Raises:
            InvalidPeripheralCommandValueError: Raised if pcmd is a negative value, or if pcmd is not a value
                between 128 and 255
            UnsupportedPeripheralError: Raised if pnum parameter value is not recognized as a member of any
                peripheral enum
            UnsupportedPeripheralCommandError: Raised if pcmd parameter value is not recognized as a member of any
                peripheral command enum
        """
        if pcmd < dpa_constants.REQUEST_PCMD_MIN:
            raise InvalidPeripheralCommandValueError('Negative peripheral command values are not allowed.')
        if pcmd <= dpa_constants.REQUEST_PCMD_MAX or pcmd > dpa_constants.RESPONSE_PCMD_MAX:
            raise InvalidPeripheralCommandValueError('Response peripheral command should be value between 128 and 255.')
        if dpa_constants.PNUM_USER_MIN <= pnum <= dpa_constants.PNUM_USER_MAX:
            return pcmd
        commands = None
        match pnum:
            case EmbedPeripherals.COORDINATOR:
                commands = CoordinatorResponseCommands
            case EmbedPeripherals.NODE:
                commands = NodeResponseCommands
            case EmbedPeripherals.OS:
                commands = OSResponseCommands
            case EmbedPeripherals.EEPROM:
                commands = EEPROMResponseCommands
            case EmbedPeripherals.EEEPROM:
                commands = EEEPROMResponseCommands
            case EmbedPeripherals.RAM:
                commands = RAMResponseCommands
            case EmbedPeripherals.LEDR | EmbedPeripherals.LEDG:
                commands = LEDResponseCommands
            case EmbedPeripherals.IO:
                commands = IOResponseCommands
            case EmbedPeripherals.THERMOMETER:
                commands = ThermometerResponseCommands
            case EmbedPeripherals.UART:
                commands = UartResponseCommands
            case EmbedPeripherals.FRC:
                commands = FrcResponseCommands
            case EmbedPeripherals.EXPLORATION:
                commands = ExplorationResponseCommands
            case Standards.DALI:
                commands = DALIResponseCommands
            case Standards.BINARY_OUTPUT:
                commands = BinaryOutputResponseCommands
            case Standards.SENSOR:
                commands = SensorResponseCommands
            case Standards.LIGHT:
                commands = LightResponseCommands
            case _:
                raise UnsupportedPeripheralError('Unknown or unsupported peripheral.')

        if commands is not None and pcmd in commands:
            return commands(pcmd)
        raise UnsupportedPeripheralCommandError('Unknown or unsupported peripheral command.')

    @staticmethod
    def pdata_from_dpa(dpa: bytes) -> Union[List[int], None]:
        """Return PDATA from DPA response bytes.

        Args:
            dpa (bytes): DPA response message
        Returns:
            :obj:`list` of :obj:`int` or :obj:`None`: PDATA integer list or None of there are no PDATA
        """
        if len(dpa) > 8:
            return list(dpa[8:])
        return None

    @staticmethod
    def parse_dpa_into_members(dpa: bytes):
        """Parse DPA response into response members.

        Args:
            dpa (bytes): DPA response.

        Returns:
            :obj:`(int, int, int, int, int, int, Optional[List[int]])`: Response members
        """
        nadr = dpa[dpa_constants.ResponsePacketMembers.NADR]
        pnum = dpa[dpa_constants.ResponsePacketMembers.PNUM]
        pcmd = dpa[dpa_constants.ResponsePacketMembers.PCMD]
        hwpid = Common.hwpid_from_dpa(
            dpa[dpa_constants.ResponsePacketMembers.HWPID_HI],
            dpa[dpa_constants.ResponsePacketMembers.HWPID_LO]
        )
        rcode = dpa[dpa_constants.ResponsePacketMembers.RCODE]
        dpa_value = dpa[dpa_constants.ResponsePacketMembers.DPA_VALUE]
        pdata = Common.pdata_from_dpa(dpa)
        return nadr, pnum, pcmd, hwpid, rcode, dpa_value, pdata

    # json

    @staticmethod
    def serialize_to_json(mtype: MessageType, msgid: str, nadr: int, hwpid: int = 0xFFFF, params: Optional[dict] = None,
                          dpa_rsp_time: Optional[float] = None):
        """Serialize request parameters into JSON API request object.

        Args:
            mtype (MessageType): Message type.
            msgid (str): Message ID.
            nadr (int): Device address.
            hwpid (int): Hardware profile ID. Defaults to 65535.
            params (dict, optional): Request parameters.
            dpa_rsp_time (float, optional): Request timeout.

        Returns:
            :obj:`dict`: JSON-serialized request
        """
        params = params if params is not None else {}
        json: dict = {
            'mType': mtype.value,
            'data': {
                'msgId': msgid,
                'req': {
                    'nAdr': nadr,
                    'hwpId': hwpid,
                    'param': params,
                },
                'returnVerbose': True,
            },
        }
        if dpa_rsp_time is not None:
            json['data']['timeout'] = math.ceil(dpa_rsp_time * 1000)
        return json

    @staticmethod
    def msgid_from_json(json: dict) -> str:
        """Return response msgid from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`str`: JSON API response message ID
        Raises:
            JsonMsgidMissingError: Raised if Daemon API response does not contain the msgId key
        """
        try:
            return json['data']['msgId']
        except KeyError as err:
            raise JsonMsgidMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def mtype_str_from_json(json: dict) -> str:
        """Return message type from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`str`: JSON API response message type string
        Raises:
            JsonMTypeMissingError: Raised if Daemon API response does not contain the mType key
        """
        try:
            return json['mType']
        except KeyError as err:
            raise JsonMTypeMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def nadr_from_json(json: dict) -> int:
        """Return response nadr from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`int`: JSON API response device address
        Raises:
            JsonNadrMissingError: Raised if Daemon API response does not contain the nAdr key
        """
        try:
            return json['data']['rsp']['nAdr']
        except KeyError as err:
            raise JsonNadrMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def pnum_from_json(json: dict) -> int:
        """Return response pnum from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`int`: JSON API response peripheral number
        Raises:
            JsonNadrMissingError: Raised if Daemon API response does not contain the pnum key
        """
        try:
            return json['data']['rsp']['pnum']
        except KeyError as err:
            raise JsonNadrMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def pcmd_from_json(json: dict) -> int:
        """Return response pcmd from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`int`: JSON API response peripheral command
        Raises:
            JsonNadrMissingError: Raised if Daemon API response does not contain the pcmd key
        """
        try:
            return json['data']['rsp']['pcmd']
        except KeyError as err:
            raise JsonNadrMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def hwpid_from_json(json: dict) -> int:
        """Return response hwpid from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`int`: JSON API response hardware profile ID
        Raises:
            JsonHwpidMissingError: Raised if Daemon API response does not contain the hwpId key
        """
        try:
            return json['data']['rsp']['hwpId']
        except KeyError as err:
            raise JsonHwpidMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def rcode_from_json(json: dict) -> int:
        """Return response rcode from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`int`: JSON API response DPA rcode
        Raises:
            JsonRCodeMissingError: Raised if Daemon API response does not contain the rcode key
        """
        try:
            return json['data']['rsp']['rCode']
        except KeyError as err:
            raise JsonRCodeMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def dpa_value_from_json(json: dict) -> int:
        """Return response DPA value from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`int`: JSON API response dpa value
        Raises:
            JsonDpaValueMissingError: Raised if Daemon API response does not contain the dpaVal key
        """
        try:
            return json['data']['rsp']['dpaVal']
        except KeyError as err:
            raise JsonDpaValueMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def pdata_from_json(json: dict) -> Union[List[int], None]:
        """Return pdata from Daemon API JSON response if available.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`Union[List[int], None]`: JSON API response pdata or None if there are no PDATA
        """
        pdata = None
        try:
            raw = json['data']['raw']
            response = None
            if isinstance(raw, list):
                response = raw[0]['response']
            elif isinstance(raw, dict):
                response = raw['response']
            response = response.split('.')
            if len(response) > 8:
                pdata = [int(x, 16) for x in response[8:]]
        except KeyError:
            pdata = None
        finally:
            return pdata

    @staticmethod
    def result_from_json(json: dict) -> dict:
        """Return response result from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`dict`: JSON API response result object
        Raises:
            JsonResultMissingError: Raised if JSON API response does not contain the result key
        """
        try:
            return json['data']['rsp']['result']
        except KeyError as err:
            raise JsonResultMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def status_from_json(json: dict) -> int:
        """Return response status from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`int`: JSON API response status code
        Raises:
            JsonStatusMissingError: Raised if JSON API response does not contain the status key
        """
        try:
            return json['data']['status']
        except KeyError as err:
            raise JsonStatusMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def generic_rdata_from_json(json: dict) -> str:
        """Return generic response data from Daemon API JSON response.

        Args:
            json (dict): JSON API response
        Returns:
            :obj:`int`: JSON API response status code
        Raises:
            JsonStatusMissingError: Raised if JSON API response does not contain path to rData.
        """
        try:
            return json['data']['rsp']['rData']
        except KeyError as err:
            raise JsonGenericDataMissingError(f'Object does not contain property {str(err)}') from err

    @staticmethod
    def parse_json_into_members(json: dict, omit_result: bool = False):
        """Parse JSON response into response members.

        Args:
            json (dict): JSON API response
            omit_result (bool): Do not parse result
        Returns:
            :obj:`(str, int, int, int, int, List[int], dict)`: Response members
        """
        msgid = Common.msgid_from_json(json=json)
        nadr = Common.nadr_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        pdata = Common.pdata_from_json(json=json)
        if omit_result:
            result = None
        else:
            result = Common.result_from_json(json=json) if rcode == dpa_constants.ResponseCodes.OK else None
        return msgid, nadr, hwpid, rcode, dpa_value, pdata, result

    @staticmethod
    def string_to_mtype(string: str) -> MessageType:
        """Convert message type string to message type enum member value.

        Args:
            string (str): Message type string
        Returns:
            :obj:`MessageType`: Message type enum member
        Raises:
            UnsupportedMessageTypeError: Raised if message type is not recognized as a member of any message type enum
        """
        messages = [GenericMessages, ExplorationMessages, CoordinatorMessages, NodeMessages, OSMessages, EEPROMMessages,
                    EEEPROMMessages, RAMMessages, LEDRMessages, LEDGMessages, IOMessages, ThermometerMessages,
                    UartMessages, FrcMessages, DALIMessages, BinaryOutputMessages, SensorMessages, LightMessages]
        for item in messages:
            if string in item:
                return item(string)
        raise UnsupportedMessageTypeError(f'Unknown or unsupported message type: {string}.')

    # general

    @staticmethod
    def bitmap_to_nodes(bitmap: List[int], coordinator_shift: bool = False) -> List[int]:
        """Convert node bitmap to list of nodes.

        Args:
            bitmap (List[int]): Node bitmap represented by list of integers
            coordinator_shift (bool): Bitmap contains dummy coordinator value
        Returns:
            :obj:`list` of :obj:`int`: List of node addresses from bitmap
        """
        nodes = []
        start = 0 if not coordinator_shift else 1
        for i in range(start, len(bitmap * 8)):
            if bitmap[int(i / 8)] & (1 << (i % 8)):
                nodes.append(i)
        return nodes

    @staticmethod
    def nodes_to_bitmap(nodes: List[int]) -> List[int]:
        """Convert list of nodes to node bitmap.

        Args:
            nodes (List[int]): List of node addresses
        Returns:
            :obj:`list` of :obj:`int`: Nodes bitmap represented by list of 30 integers
        """
        bitmap = [0] * 30
        for node in nodes:
            bitmap[math.floor(node / 8)] |= (1 << (node % 8))
        return bitmap

    @staticmethod
    def bitmap_4byte_to_indexes(bitmap: List[int]) -> List[int]:
        """Convert 4 byte bitmap to list of indexes.

        Args:
            bitmap (List[int]): Index bitmap.

        Returns:
            :obj:`List` of :obj:`int`: List of indexes.
        """
        indexes = [0] * 32
        for i in range(0, len(bitmap * 8)):
            if bitmap[int(i / 8)] & (1 << (i % 8)):
                indexes[i] = 1
        return indexes

    @staticmethod
    def indexes_to_4byte_bitmap(values: List[int]) -> List[int]:
        """Convert list of indexes to a 4 byte bitmap.

        Args:
            values (List[int]): List of indexes
        Returns:
            :obj:`list` of :obj:`int`: Index bitmap represented by list of 4 integers
        """
        bitmap = [0] * 4
        for value in values:
            bitmap[math.floor(value / 8)] |= (1 << (value % 8))
        return bitmap

    @staticmethod
    def is_hex_string(string: str) -> bool:
        """Check if string contains only hexadecimal characters.

        Args:
            string (str): Input string
        Returns:
            :obj:`bool`: True if string contains only hexadecimal characters, False otherwise
        """
        if len(string) == 0:
            return False
        return not set(string) - set('0123456789abcdefABCDEF')

    @staticmethod
    def hex_string_to_list(string: str) -> List[int]:
        """Convert hexadecimal string to list of unsigned integers.

        Args:
            string (str): Hexadecimal string
        Returns:
            :obj:`list` of :obj:`int`: List of integers from hexadecimal string
        Raises:
            ValueError: Raised if string is of uneven length or contains non-hexadecimal characters
        """
        if not len(string) % 2 == 0:
            raise ValueError('Argument should be even length.')
        if not Common.is_hex_string(string):
            raise ValueError('Argument is not a hexadecimal string.')
        return [int(string[i:i + 2], base=16) for i in range(0, len(string), 2)]

    @staticmethod
    def list_to_hex_string(values: List[int], separator: str = ' ', uppercase: bool = True) -> str:
        """Convert list of unsigned integers to hexadecimal string.

        Args:
            values (List[int]): List of unsigned integers
            separator (str, optional): Separator for byte string. Defaults to empty string.
            uppercase (bool, optional): Output hex string uppercase. Defaults to False.

        Returns:
            :obj:`string`: Hexadecimal string representation of the list
        """
        hex_format = 'X' if uppercase else 'x'
        return separator.join(f'{value:02{hex_format}}' for value in values)

    @staticmethod
    def peripheral_list_to_bitmap(values: List[int]) -> List[int]:
        """Convert list of peripheral numbers into a bitmap of peripherals.

        For example, the coordinator peripheral would be represented by the 1st bit in bitmap.

        Args:
            values (List[int]): List of peripheral numbers
        Returns:
            :obj:`list` of :obj:`int`: Peripheral bitmap represented by list of 4 integers
        """
        bitmap = [0 for _ in range(32)]
        for value in values:
            bitmap[value] = 1
        byte_list = []
        for bits in [bitmap[i:i + 8] for i in range(0, len(bitmap), 8)]:
            bits.reverse()
            byte = 0
            for bit in bits:
                byte = (byte << 1) | bit
            byte_list.append(byte)
        return byte_list

    @staticmethod
    def values_in_byte_range(values: List[int]) -> bool:
        """Check if list elements are within unsigned integer byte range.

        Args:
            values (List[int]): Input data
        Returns:
            :obj:`bool`: True if values are in range, False otherwise
        """
        return len([value for value in values if value < 0 or value > 255]) == 0

    @staticmethod
    def byte_complement(value: int):
        """Convert unsigned 1B value into a signed 1B value.

        Args:
            value (int): Input unsigned 1B value
        Returns:
            :obj:`int`: Signed 1B value
        Raises:
            ValueError: Raised when value is not in unsigned 8bit range.
        """
        if not 0 <= value <= 0xFF:
            raise ValueError('Not an unsigned 1B value.')
        if value < 0x80:
            return value
        return value - 0x100

    @staticmethod
    def word_complement(value: int) -> int:
        """Convert unsigned 2B value into a signed 2B value.

        Args:
            value (int): Input unsigned 2B value
        Returns:
            :obj:`int`: Signed 2B value
        Raises:
            ValueError: Raised when value is not in unsigned 16bit range.
        """
        if not 0 <= value <= 0xFFFF:
            raise ValueError('Not an unsigned 2B value.')
        if value < 0x8000:
            return value
        return value - 0x10000

    @staticmethod
    def bcd_to_decimal(byte: int) -> int:
        """Convert a Binary-Coded Decimal (BCD) value to decimal integer.

        Args:
            byte (int): BCD value to convert.

        Returns:
            :obj:`int`: Decimal value encoded in BCD.

        Raises:
            ValueError: Raised when byte argument is not a valid BCD value.

        Examples:
            >>> Common.bcd_to_decimal(0x42)
            42
        """
        high = (byte >> 4) & 0x0F
        low = byte & 0x0F
        if high > 9 or low > 9:
            raise ValueError('Not a BCD value.')
        return high * 10 + low

    @staticmethod
    def dpa_build_date_to_str(par1: int, par2: int) -> str:
        """Convert DPA build date in BCD format to human-readable string.

        Outputs date string in the following format: DD.MM.YYYY.

        Args:
            par1 (int): BCD-encoded day of DPA build date.
            par2 (int): BCD-encoded month and year of DPA build date.

        Returns:
            str: Human-readable DPA build date string.
        """
        try:
            day = Common.bcd_to_decimal(par1)
            month = par2 & 0x0F
            year = 2010 + ((par2 >> 4) & 0x0F)
            return f'{day}.{month}.{year}'
        except ValueError as e:
            raise ValueError(f'Failed to convert DPA build date to string: {str(e)}') from e

    @staticmethod
    def dpa_version_to_str(dpa_version: int) -> str:
        """Convert DPA version in BCD format to human-readable version string.

        Args:
            dpa_version (int): DPA version encoded in BCD format.

        Returns:
            str: Human-readable DPA version string.

        Raises:
            ValueError: Raised when dpa_version is not a valid BCD value.
        """
        try:
            major = Common.bcd_to_decimal(int(dpa_version / 256))
            minor = dpa_version & 0x00FF
            return f'{major}.{minor:02X}'
        except ValueError as e:
            raise ValueError(f'Failed to convert version to string: {str(e)}') from e

    @staticmethod
    def fletcher_checksum(init: int, data: List[int]) -> int:
        """Calculate one's complement Fletcher checksum from list of bytes.

        See https://doc.iqrf.org/DpaTechGuide/pages/FletcherCSharp.html

        Args:
            init (int): Initial value.
            data (List[int]): List of bytes to calculate checksum from.

        Returns:
            :obj:`int`: 16bit Fletcher checksum integer value.
        """
        checksum = init
        for byte in data:
            low = checksum & 0xFF
            low += byte
            if (low & 0x100) != 0:
                low += 1
            high = checksum >> 8
            high += low & 0xFF
            if (high & 0x100) != 0:
                high += 1
            checksum = ((low & 0xFF) | (high & 0xFF) << 8)
        return checksum
