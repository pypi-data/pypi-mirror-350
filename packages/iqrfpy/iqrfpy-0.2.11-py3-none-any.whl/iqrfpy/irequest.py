"""Request message class abstraction."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union
from uuid import uuid4
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.enums.commands import Command
from iqrfpy.enums.message_types import MessageType
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.exceptions import RequestNadrInvalidError, RequestPnumInvalidError, RequestPcmdInvalidError, \
    RequestHwpidInvalidError, RequestParameterInvalidValueError

__all__ = ['IRequest']


class IRequest(ABC):
    """This abstract class serves as an interface for embedded peripherals and standards request messages.

    The class provides getters and setters for shared request properties in the form of the @property decorator.
    Shared properties such as device address, peripheral, peripheral command and hwpid are validated here.
    The class also provides generic DPA and JSON serialization methods for derived classes to amend.
    While the abstract class cannot be instantiated, it's methods can be called from a derived class using super.

    Network address (nadr) specifies target device: 0 (coordinator), 1-239 (node), 252 (local device),
    254 (temporary address) and 255 (broadcast), other values are reserved. Values in range 0-255.

    Peripheral number (pnum) specifies peripheral to use: 0-31 are served for embedded peripherals and
    64-127 are reserved for IQRF standard peripherals. Peripheral number can be passed as a member of one
    of the peripheral enum class members (see iqrfpy.enums.peripherals) or plain integer. Values in range 0-255.

    Peripheral command (pcmd) specifies a command to execute, each peripheral implements different commands.
    See DPA framework document for specific command numbers. Peripheral command can be passed as a member of one
    of the peripheral command enum class members (see iqrfpy.enums.commands) or plain integer.
    Peripheral number and peripheral command are pre-defined for each command message this library implements,
    however they will be required for user-defined messages. Values in range 0-255, but note that only values
    0-127 are used for request commands, as response command value is equal to request command value plus 128 (0x80).

    Hardware profile ID (hwpid) specifies a unique device (by its functionality), this argument can be used to filter
    which devices execute a commend specified by request message. Only devices with matching hwpid will execute
    a command, unless the value 65535 (0xFFFF) is used, which ignores hwpid checking. Values in range 0-65535.

    Packet data (pdata) can be required or optional data sent with the request message, depending on the command.
    On a general level, packet data is treated as list of unsigned 1B integers. This means that when defining a user
    command and a request message, request data should be serialized into a list of previously mentioned
    format and stored in the pdata member.

    For more detailed information, see the IQRF DPA Framework documentation.

    Message type (m_type) is an optional argument, however, it is required when using JSON API as message type
    is equivalent to a combination of peripheral number and peripheral command (see iqrfpy.enums.message_types).
    For example, `OSMessages.READ` (iqrfEmbedOs_Read) is equivalent to `EmbedPeripherals.OS` (2) and
    `OSRequestCommands.READ` (0).

    Request parameters (params) is an optional dictionary argument, that is used when constructing a JSON API request.
    When creating a user message, use the params member to propagate your request parameters into the final
    JSON request object.

    DPA response time (dpa_rsp_time) is an optional argument specifying DPA request timeout, not time between reception
    of a request and delivery of response. Note that handling of this argument is the responsibility of a transport
    and system facilitating communication between the library and devices of the IQRF network.

    Device processing time (dev_process_time) is an optional argument used to specify time allotted to the device
    executing a task beyond simple data processing. For example, a device may need to measure some quantity
    for certain amount of time for the measured value to be valid. Note that handling of this argument
    is the responsibility of a transport and system facilitating communication between the library and devices
    of the IQRF network.

    Message ID (msgid) is an optional argument used only by the JSON API at this time. It is used to pair
    JSON API requests and responses as the message type argument only allows to pair requests of the same type,
    but not pairing a specific request and response, given the asynchronous nature of the JSON API.
    """

    __slots__ = '_nadr', '_pnum', '_pcmd', '_mtype', '_hwpid', '_pdata', '_msgid', '_params', '_dpa_rsp_time', \
        '_dev_process_time'

    def __init__(self, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int],
                 hwpid: int = dpa_constants.HWPID_MAX, pdata: Optional[List[int]] = None,
                 m_type: Optional[MessageType] = None, msgid: Optional[str] = None,
                 params: Optional[dict] = None, dpa_rsp_time: Optional[float] = None,
                 dev_process_time: Optional[float] = None):
        """IRequest constructor.

        Args:
            nadr (int): Network address.
            pnum (Union[Peripheral, int]): Peripheral number.
            pcmd (Union[Command, int]): Peripheral command.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            pdata (List[int], optional): DPA request data. Defaults to None.
            m_type (MessageType, optional): JSON API message type. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
            params (dict, optional): JSON API request data. Defaults to None.
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
        """
        self._nadr = nadr
        self._pnum = pnum
        self._pcmd = pcmd
        self._hwpid = hwpid
        self._pdata = pdata
        self._mtype = m_type
        self._msgid = msgid if msgid is not None else str(uuid4())
        self._params = params if params is not None else {}
        self._dpa_rsp_time = dpa_rsp_time
        self._dev_process_time = dev_process_time
        self._validate_base(nadr, pnum, pcmd, hwpid, dpa_rsp_time, dev_process_time)

    def _validate_base(self, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int,
                       dpa_rsp_time: Optional[float], dev_process_time: Optional[float]) -> None:
        """Shared members validation method.

        Validates shared request members to ensure the data can fit into the DPA packet and JSON request
        object and do not violate rules for expected format of these properties.

        Args:
            nadr (int): Network address.
            pnum (Union[Peripheral, int]): Peripheral number.
            pcmd (Union[Command, int]): Peripheral command.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
        """
        self._validate_nadr(nadr)
        self._validate_pnum(pnum)
        self._validate_pcmd(pcmd)
        self._validate_hwpid(hwpid)
        self._validate_dpa_rsp_time(dpa_rsp_time)
        self._validate_dev_process_time(dev_process_time)

    @staticmethod
    def _validate_nadr(nadr: int):
        """Validates network address parameter.

        Args:
            nadr (int): Network address value.

        Raises:
            RequestNadrInvalidError: If nadr is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= nadr <= dpa_constants.BYTE_MAX:
            raise RequestNadrInvalidError('NADR should be between 0 and 255.')

    @property
    def nadr(self) -> int:
        """:obj:`int`: Network address.

        Getter and setter.
        """
        return self._nadr

    @nadr.setter
    def nadr(self, value: int):
        self._validate_nadr(value)
        self._nadr = value

    @staticmethod
    def _validate_pnum(pnum: Union[Peripheral, int]):
        """Validates peripheral number parameter.

        Args:
            pnum (Union[Peripheral, int]): Peripheral number value.

        Raises:
            RequestPnumInvalidError: If pnum is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= pnum <= dpa_constants.BYTE_MAX:
            raise RequestPnumInvalidError('PNUM should be between 0 and 255.')

    @property
    def pnum(self) -> Union[Peripheral, int]:
        """:obj:`iqrfpy.enums.peripherals.Peripheral` of :obj:`int`: Peripheral number.

        Getter and setter.
        """
        return self._pnum

    @pnum.setter
    def pnum(self, value: Union[Peripheral, int]):
        self._validate_pnum(pnum=value)
        self._pnum = value

    @staticmethod
    def _validate_pcmd(pcmd: Union[Command, int]):
        """Validates peripheral command parameter.

        Args:
            pcmd (Union[Command, int]): Peripheral command value.

        Raises:
            RequestPcmdInvalidError: If pcmd is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= pcmd <= dpa_constants.BYTE_MAX:
            raise RequestPcmdInvalidError('PCMD should be between 0 and 255.')

    @property
    def pcmd(self) -> Union[Command, int]:
        """:obj:`iqrfpy.enums.commands.Command` or :obj:`int`: Peripheral command.

        Getter and setter.
        """
        return self._pcmd

    @pcmd.setter
    def pcmd(self, value: Union[Command, int]):
        self._validate_pcmd(pcmd=value)
        self._pcmd = value

    @staticmethod
    def _validate_hwpid(hwpid: int):
        """Validates Hardware profile ID parameter.

        Args:
            hwpid (int): Hardware profile ID value.

        Raises:
            RequestHwpidInvalidError: If hwpid is less than 0 or greater than 65535.
        """
        if not dpa_constants.HWPID_MIN <= hwpid <= dpa_constants.HWPID_MAX:
            raise RequestHwpidInvalidError('HWPID should be between 0 and 65535.')

    @property
    def hwpid(self) -> int:
        """:obj:`int`: Hardware profile ID.

        Getter and setter.
        """
        return self._hwpid

    @staticmethod
    def _validate_dpa_rsp_time(dpa_rsp_time: Optional[float] = None):
        """Validates dpa timeout parameter.

        Args:
            dpa_rsp_time (float, optional): DPA timeout value in seconds. Defaults to None.

        Raises:
            RequestParameterInvalidValueError: If dpa_rsp_time is not None and is less than 0.
        """
        if dpa_rsp_time is None:
            return
        if dpa_rsp_time < 0:
            raise RequestParameterInvalidValueError('DPA response time should a positive integer.')

    @property
    def dpa_rsp_time(self) -> Optional[float]:
        """:obj:`float` or :obj:`None`: DPA timeout.

        Getter and setter.
        """
        return self._dpa_rsp_time

    @dpa_rsp_time.setter
    def dpa_rsp_time(self, value: Optional[float] = None):
        self._validate_dpa_rsp_time(value)
        self._dpa_rsp_time = value

    @staticmethod
    def _validate_dev_process_time(dev_process_time: Optional[float] = None):
        """Validates device processing time parameter.

        Args:
            dev_process_time (float, optional): Device processing time value. Defaults to None.

        Raises:
            RequestParameterInvalidValueError: If dev_process_time is not None and is less than 0.
        """
        if dev_process_time is None:
            return
        if dev_process_time < 0:
            raise RequestParameterInvalidValueError('Device processing time should be a positive integer.')

    @property
    def dev_process_time(self) -> Optional[float]:
        """:obj:`float` or :obj:`None`: Device processing time.

        Getter and setter.
        """
        return self._dev_process_time

    @dev_process_time.setter
    def dev_process_time(self, value: Optional[float] = None):
        self._validate_dev_process_time(value)
        self._dev_process_time = value

    @property
    def msgid(self) -> str:
        """:obj:`str`: Message ID.

        Getter and setter.
        """
        return self._msgid

    @msgid.setter
    def msgid(self, value: str):
        self._msgid = value

    @property
    def mtype(self) -> MessageType:
        """:obj:`MessageType` Message type.

        Getter only.
        """
        return self._mtype

    @abstractmethod
    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Serializes a request to DPA request packet format. Each request contains the DPA request header.
        If pdata is specified, it is appended to the DPA request header. The request can be serialized
        into both mutable and immutable (default) byte formats.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        raise NotImplementedError('Abstract method not implemented.')

    @abstractmethod
    def to_json(self) -> dict:
        """JSON API request serialization method.

        Serializes a request to JSON API request object. Each request contains message type and data.
        Data carries message ID for pairing requests with responses, and `req` object that contains network address,
        hwpid and optional request parameters (equivalent to DPA packet data) if `params` is not None.
        If DPA timeout is specified, the value is multiplied by 1000 as JSON API accepts timeout in milliseconds.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        raise NotImplementedError('Abstract method not implemented')
