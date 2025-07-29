"""OS TR Configuration data."""
from typing import List, Optional, Union
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.objects.os_tr_conf_byte import OsTrConfByte
from iqrfpy.utils.common import Common
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.dpa import TrConfByteAddrs, TrConfBitMasks


class OsTrConfData:
    """OS TR Configuration data."""

    __slots__ = '_embedded_peripherals', '_custom_dpa_handler', '_dpa_peer_to_peer', '_routing_off', '_io_setup', \
        '_user_peer_to_peer', '_stay_awake_when_not_bonded', '_std_and_lp_network', '_rf_output_power', \
        '_rf_signal_filter', '_lp_rf_timeout', '_uart_baud_rate', '_alternative_dsm_channel', '_local_frc', \
        '_rf_channel_a', '_rf_channel_b', '_reserved_block_0', '_reserved_block_1', '_reserved_block_2'

    def __init__(self, embedded_peripherals: Optional[List[Union[EmbedPeripherals, int]]] = None,
                 custom_dpa_handler: bool = False, dpa_peer_to_peer: bool = False, routing_off: bool = False,
                 io_setup: bool = False, user_peer_to_peer: bool = False, stay_awake_when_not_bonded: bool = False,
                 std_and_lp_network: bool = False, rf_output_power: int = 7, rf_signal_filter: int = 5,
                 lp_rf_timeout: int = 6,
                 uart_baud_rate: Union[dpa_constants.BaudRates, int] = dpa_constants.BaudRates.B9600,
                 alternative_dsm_channel: int = 0, local_frc: bool = False, rf_channel_a: int = 52,
                 rf_channel_b: int = 2, reserved_block_0: Optional[List[int]] = None,
                 reserved_block_1: Optional[List[int]] = None, reserved_block_2: Optional[List[int]] = None):
        """TR Configuration data constructor.

        Args:
            embedded_peripherals (List[int]): Enabled embedded peripherals.
            custom_dpa_handler (bool): Custom DPA handler in use.
            dpa_peer_to_peer (bool): DPA peer-to-peer enabled.
            routing_off (bool): Node does not route packets in background.
            io_setup (bool): Run IO Setup early during module boot time.
            user_peer_to_peer (bool): Receive peer-to-peer packets and raise PeerToPeer event.
            stay_awake_when_not_bonded (bool): Stay awake during bonding process.
            std_and_lp_network (bool): Control STD+LP network.
            rf_output_power (int): RF output power.
            rf_signal_filter (int): RF signal filter.
            lp_rf_timeout (int): LP RF timeout.
            uart_baud_rate (Union[dpa_constants.BaudRates, int]): UART baud rate.
            alternative_dsm_channel (int): Alternative DSM channel.
            local_frc (bool): Local FRC reception enabled.
            rf_channel_a (int): RF Channel A.
            rf_channel_b (int): RF Channel B.
            reserved_block_0 (List[int], optional): Reserved data block.
            reserved_block_1 (List[int], optional): Reserved data block.
            reserved_block_2 (List[int], optional): Reserved data block.
        """
        if embedded_peripherals is None:
            embedded_peripherals = []
        if reserved_block_0 is None:
            reserved_block_0 = [0] * 2
        if reserved_block_1 is None:
            reserved_block_1 = [0] * 3
        if reserved_block_2 is None:
            reserved_block_2 = [0] * 13
        self._validate(embedded_peripherals=embedded_peripherals, rf_output_power=rf_output_power,
                       rf_signal_filter=rf_signal_filter, lp_rf_timeout=lp_rf_timeout, baud_rate=uart_baud_rate,
                       alternative_dsm=alternative_dsm_channel, rf_channel_a=rf_channel_a, rf_channel_b=rf_channel_b,
                       reserved_block_0=reserved_block_0, reserved_block_1=reserved_block_1,
                       reserved_block_2=reserved_block_2)
        self._embedded_peripherals = embedded_peripherals
        self._custom_dpa_handler = custom_dpa_handler
        self._dpa_peer_to_peer = dpa_peer_to_peer
        self._routing_off = routing_off
        self._io_setup = io_setup
        self._user_peer_to_peer = user_peer_to_peer
        self._stay_awake_when_not_bonded = stay_awake_when_not_bonded
        self._std_and_lp_network = std_and_lp_network
        self._rf_output_power = rf_output_power
        self._rf_signal_filter = rf_signal_filter
        self._lp_rf_timeout = lp_rf_timeout
        self._uart_baud_rate = uart_baud_rate
        self._alternative_dsm_channel = alternative_dsm_channel
        self._local_frc = local_frc
        self._rf_channel_a = rf_channel_a
        self._rf_channel_b = rf_channel_b
        self._reserved_block_0 = reserved_block_0
        self._reserved_block_1 = reserved_block_1
        self._reserved_block_2 = reserved_block_2

    def __eq__(self, other: 'OsTrConfData'):
        """Rich comparison method, comparing this and another object to determine equality based on properties.

        Args:
            other (OsTrConfData): Object to compare with.

        Returns:
            bool: True if the objects are equivalent, False otherwise.
        """
        return self._embedded_peripherals == other._embedded_peripherals and \
            self._custom_dpa_handler == other._custom_dpa_handler and \
            self._dpa_peer_to_peer == other._dpa_peer_to_peer and \
            self._routing_off == other.routing_off and \
            self._io_setup == other._io_setup and \
            self._user_peer_to_peer == other._user_peer_to_peer and \
            self._stay_awake_when_not_bonded == other._stay_awake_when_not_bonded and \
            self._std_and_lp_network == other._std_and_lp_network and \
            self._rf_output_power == other._rf_output_power and \
            self._rf_signal_filter == other._rf_signal_filter and \
            self._lp_rf_timeout == other._lp_rf_timeout and \
            self._uart_baud_rate == other._uart_baud_rate and \
            self._alternative_dsm_channel == other._alternative_dsm_channel and \
            self._local_frc == other._local_frc and \
            self._rf_channel_a == other._rf_channel_a and \
            self._rf_channel_b == other._rf_channel_b and \
            self._reserved_block_0 == other._reserved_block_0 and \
            self._reserved_block_1 == other._reserved_block_1 and \
            self._reserved_block_2 == other._reserved_block_2

    def _validate(self, embedded_peripherals: List[int], rf_output_power: int, rf_signal_filter: int,
                  lp_rf_timeout: int, baud_rate: Union[dpa_constants.BaudRates, int], alternative_dsm: int,
                  rf_channel_a: int, rf_channel_b: int, reserved_block_0: List[int],
                  reserved_block_1: List[int], reserved_block_2: List[int]):
        self._validate_embedded_peripherals(embedded_peripherals)
        self._validate_rf_output_power(rf_output_power)
        self._validate_rf_signal_filter(rf_signal_filter)
        self._validate_lp_rf_timeout(lp_rf_timeout)
        self._validate_uart_baud_rate(baud_rate)
        self._validate_alternative_dsm_channel(alternative_dsm)
        self._validate_rf_channel_a(rf_channel_a)
        self._validate_rf_channel_b(rf_channel_b)
        self._validate_reserved_block_0(reserved_block_0)
        self._validate_reserved_block_1(reserved_block_1)
        self._validate_reserved_block_2(reserved_block_2)

    @staticmethod
    def _validate_embedded_peripherals(embedded_peripherals: List[Union[EmbedPeripherals, int]]) -> None:
        if len(embedded_peripherals) > 32:
            raise RequestParameterInvalidValueError('Embedded peripherals should be at most 32 values.')
        if min(embedded_peripherals, default=0) < 0 or max(embedded_peripherals, default=0) > 31:
            raise RequestParameterInvalidValueError('Embedded peripherals values should be between 0 and 31.')

    @property
    def embedded_peripherals(self) -> List[Union[EmbedPeripherals, int]]:
        """:obj:`list` of :obj:`EmbedPeripherals` or :obj:`int`: Enabled embedded peripherals.

        Getter and setter.
        """
        return self._embedded_peripherals

    @embedded_peripherals.setter
    def embedded_peripherals(self, value: List[Union[EmbedPeripherals, int]]):
        self._validate_embedded_peripherals(embedded_peripherals=value)
        self._embedded_peripherals = value

    def enable_embedded_peripheral(self, peripheral: Union[EmbedPeripherals, int]) -> None:
        """Enables embedded peripheral.

        Args:
            peripheral (:obj:`EmbeddedPeripherals` or :obj:`int`): Embedded peripheral.

        Raises:
            ValueError: If peripheral value is less than 0 or greater than 31.
        """
        if not (0 <= peripheral <= 31):
            raise ValueError('Peripheral value should be between 0 and 31')
        if peripheral not in self._embedded_peripherals:
            self._embedded_peripherals.append(peripheral)

    def disable_embedded_peripheral(self, peripheral: Union[EmbedPeripherals, int]) -> None:
        """Disables embedded peripheral.

        Args:
            peripheral (:obj:`EmbeddedPeripherals` or :obj:`int`): Embedded peripheral.

        Raises:
            ValueError: If peripheral value is less than 0 or greater than 31.
        """
        if not (0 <= peripheral <= 31):
            raise ValueError('Peripheral value should be between 0 and 31')
        if peripheral in self._embedded_peripherals:
            self._embedded_peripherals.remove(peripheral)

    def get_embedded_peripheral_byte(self, peripheral: Union[EmbedPeripherals, int]) -> OsTrConfByte:
        """Returns embedded peripheral configuration byte.

        Args:
            peripheral (:obj:`EmbeddedPeripherals` or :obj:`int`): Embedded peripheral.

        Raises:
            ValueError: If peripheral value is less than 0 or greater than 31.

        Returns:
            :obj:`OsTrConfByte`: Embedded peripheral configuration byte.
        """
        if not (0 <= peripheral <= 31):
            raise ValueError('Peripheral value should be between 0 and 31')
        if 0 <= peripheral <= 7:
            address = 1
        elif 8 <= peripheral <= 15:
            address = 2
        elif 16 <= peripheral <= 23:
            address = 3
        else:
            address = 4
        value = 1 << (peripheral % 8) if peripheral in self._embedded_peripherals else 0
        return OsTrConfByte(
            address=address,
            value=value,
            mask=value
        )

    @property
    def custom_dpa_handler(self) -> bool:
        """:obj:`bool`: Custom DPA handler in use.

        Getter and setter.
        """
        return self._custom_dpa_handler

    @custom_dpa_handler.setter
    def custom_dpa_handler(self, value: bool):
        self._custom_dpa_handler = value

    def get_custom_dpa_handler_byte(self) -> OsTrConfByte:
        """Returns custom DPA handler configuration byte.

        Returns:
            :obj:`OsTrConfByte`: Custom DPA handler configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
            value=1 if self._custom_dpa_handler else 0,
            mask=TrConfBitMasks.CUSTOM_DPA_HANDLER
        )

    @property
    def dpa_peer_to_peer(self) -> bool:
        """:obj:`bool`: DPA peer-to-peer enabled.

        Getter and setter.
        """
        return self._dpa_peer_to_peer

    @dpa_peer_to_peer.setter
    def dpa_peer_to_peer(self, value: bool):
        self._dpa_peer_to_peer = value

    def get_dpa_peer_to_peer_byte(self) -> OsTrConfByte:
        """Return DPA peer-to-peer configuration byte.

        Returns:
            :obj:`OsTrConfByte`: DPA peer-to-peer configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
            value=2 if self._dpa_peer_to_peer else 0,
            mask=TrConfBitMasks.DPA_PEER_TO_PEER
        )

    @property
    def routing_off(self) -> bool:
        """:obj:`bool`: Node does not route packets in background.

        Getter and setter.
        """
        return self._routing_off

    @routing_off.setter
    def routing_off(self, value: bool):
        self._routing_off = value

    def get_routing_off_byte(self) -> OsTrConfByte:
        """Returns routing off configuration byte.

        Returns:
            :obj:`OsTrConfByte`: Routing off configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
            value=8 if self._routing_off else 0,
            mask=TrConfBitMasks.ROUTING_OFF
        )

    @property
    def io_setup(self) -> bool:
        """:obj:`bool`: Run IO Setup early during module boot time.

        Getter and setter.
        """
        return self._io_setup

    @io_setup.setter
    def io_setup(self, value: bool):
        self._io_setup = value

    def get_io_setup_byte(self) -> OsTrConfByte:
        """Returns IO setup configuration byte.

        Returns:
            :obj:`OsTrConfByte`: IO setup configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
            value=16 if self._io_setup else 0,
            mask=TrConfBitMasks.IO_SETUP
        )

    @property
    def user_peer_to_peer(self) -> bool:
        """:obj:`bool`: Receive peer-to-peer packets and raise PeerToPeer event.

        Getter and setter.
        """
        return self._user_peer_to_peer

    @user_peer_to_peer.setter
    def user_peer_to_peer(self, value: bool):
        self._user_peer_to_peer = value

    def get_user_peer_to_peer_byte(self) -> OsTrConfByte:
        """Returns user peer-to-peer configuration byte.

        Returns:
            :obj:`OsTrConfByte`: User peer-to-peer configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
            value=32 if self._user_peer_to_peer else 0,
            mask=TrConfBitMasks.USER_PEER_TO_PEER,
        )

    @property
    def stay_awake_when_not_bonded(self) -> bool:
        """:obj:`bool`: Stay awake during bonding process.

        Getter and setter.
        """
        return self._stay_awake_when_not_bonded

    @stay_awake_when_not_bonded.setter
    def stay_awake_when_not_bonded(self, value: bool):
        self._stay_awake_when_not_bonded = value

    def get_stay_awake_when_not_bonded_byte(self) -> OsTrConfByte:
        """Returns stay awake when not bonded configuration byte.

        Returns:
            :obj:`OsTrConfByte`: Stay awake when not bonded configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
            value=64 if self._stay_awake_when_not_bonded else 0,
            mask=TrConfBitMasks.STAY_AWAKE_WHEN_NOT_BONDED,
        )

    @property
    def std_and_lp_network(self) -> bool:
        """:obj:`bool`: Control STD+LP network.

        Getter and setter.
        """
        return self._std_and_lp_network

    @std_and_lp_network.setter
    def std_and_lp_network(self, value: bool):
        self._std_and_lp_network = value

    def get_std_and_lp_network_byte(self) -> OsTrConfByte:
        """Returns STD and LP network configuration byte.

        Returns:
            :obj:`OsTrConfByte`: STD and LP network configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
            value=128 if self._std_and_lp_network else 0,
            mask=TrConfBitMasks.STD_AND_LP_NETWORK
        )

    @staticmethod
    def _validate_rf_output_power(rf_output_power: int) -> None:
        """Validate rf output power parameter.

        Args:
            rf_output_power (int): RF output power.

        Raises:
            RequestParameterInvalidValueError: If rf_output_power is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= rf_output_power <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('RF output power value should be between 0 and 255.')

    @property
    def rf_output_power(self) -> int:
        """:obj:`int`: RF output power.

        Getter and setter.
        """
        return self._rf_output_power

    @rf_output_power.setter
    def rf_output_power(self, value: int):
        self._validate_rf_output_power(rf_output_power=value)
        self._rf_output_power = value

    def get_rf_output_power_byte(self) -> OsTrConfByte:
        """Returns RF output power configuration byte.

        Returns:
            :obj:`OsTrConfByte`: RF output power configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.RF_OUTPUT_POWER,
            value=self._rf_output_power,
            mask=0xFF
        )

    @staticmethod
    def _validate_rf_signal_filter(rf_signal_filter: int) -> None:
        """Validate rf signal filter parameter.

        Args:
            rf_signal_filter (int): RF signal filter.

        Raises:
            RequestParameterInvalidValueError: If rf_signal_filter is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= rf_signal_filter <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('RF signal filter value should be between 0 and 255.')

    @property
    def rf_signal_filter(self) -> int:
        """:obj:`int`: RF signal filter.

        Getter and setter.
        """
        return self._rf_signal_filter

    @rf_signal_filter.setter
    def rf_signal_filter(self, value: int):
        self._validate_rf_signal_filter(rf_signal_filter=value)
        self._rf_signal_filter = value

    def get_rf_signal_filter_byte(self) -> OsTrConfByte:
        """Returns RF signal filter configuration byte.

        Returns:
            :obj:`OsTrConfByte`: RF signal filter configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.RF_SIGNAL_FILTER,
            value=self._rf_signal_filter,
            mask=0xFF
        )

    @staticmethod
    def _validate_lp_rf_timeout(lp_rf_timeout: int) -> None:
        """Validate lp rf timeout parameter.

        Args:
            lp_rf_timeout (int): LP RF timeout.

        Raises:
            RequestParameterInvalidValueError: If lp_rf_timeout is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= lp_rf_timeout <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('LP RF timeout value should be between 0 and 255.')

    @property
    def lp_rf_timeout(self) -> int:
        """:obj:`int`: LP RF timeout.

        Getter and setter.
        """
        return self._lp_rf_timeout

    @lp_rf_timeout.setter
    def lp_rf_timeout(self, value: int):
        self._validate_lp_rf_timeout(lp_rf_timeout=value)
        self._lp_rf_timeout = value

    def get_lp_rf_timeout_byte(self) -> OsTrConfByte:
        """Returns LP RF timeout configuration byte.

        Returns:
            :obj:`OsTrConfByte`: LP RF timeout configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.LP_RF_TIMEOUT,
            value=self._lp_rf_timeout,
            mask=0xFF
        )

    @staticmethod
    def _validate_uart_baud_rate(uart_baud_rate: Union[dpa_constants.BaudRates, int]) -> None:
        """Validate uart baud rate parameter.

        Args:
            uart_baud_rate (Union[BaudRates, int]): UART Baud rate.

        Raises:
            RequestParameterInvalidValueError: If uart_baud_rate is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= uart_baud_rate <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('UART baud rate value should be between 0 and 255.')

    @property
    def uart_baud_rate(self) -> Union[dpa_constants.BaudRates, int]:
        """:obj:`BaudRates` or :obj:`int`: UART baud rate.

        Getter and setter.
        """
        return self._uart_baud_rate

    @uart_baud_rate.setter
    def uart_baud_rate(self, value: Union[dpa_constants.BaudRates, int]):
        self._validate_uart_baud_rate(uart_baud_rate=value)
        self._uart_baud_rate = value

    def get_uart_baud_rate_byte(self) -> OsTrConfByte:
        """Returns UART baud rate configuration byte.

        Returns:
            :obj:`OsTrConfByte`: UART baud rate configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.UART_BAUD_RATE,
            value=self._uart_baud_rate,
            mask=0xFF
        )

    @staticmethod
    def _validate_alternative_dsm_channel(alternative_dsm_channels: int) -> None:
        """Validate alternative dsm channel parameters.

        Args:
            alternative_dsm_channels (int): Alternative DSM channel.

        Raises:
            RequestParameterInvalidValueError: If alternative_dsm_channels is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= alternative_dsm_channels <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Alternative DMS channel value should be between 0 and 255.')

    @property
    def alternative_dsm_channel(self) -> int:
        """:obj:`int`: Alternative DSM channel.

        Getter and setter.
        """
        return self._alternative_dsm_channel

    @alternative_dsm_channel.setter
    def alternative_dsm_channel(self, value: int):
        self._validate_alternative_dsm_channel(alternative_dsm_channels=value)
        self._alternative_dsm_channel = value

    def get_alternative_dsm_channel_byte(self) -> OsTrConfByte:
        """Returns alternative DSM channel configuration byte.

        Returns:
            :obj:`OsTrConfByte`: Alternative DSM channel configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.ALTERNATIVE_DSM_CHANNEL,
            value=self._alternative_dsm_channel,
            mask=0xFF
        )

    @property
    def local_frc(self) -> bool:
        """:obj:`bool`: Local FRC reception enabled.

        Getter and setter.
        """
        return self._local_frc

    @local_frc.setter
    def local_frc(self, value: bool):
        self._local_frc = value

    def get_local_frc_byte(self) -> OsTrConfByte:
        """Returns local FRC configuration byte.

        Returns:
            :obj:`OsTrConfByte`: Local FRC configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.DPA_CONFIG_BITS_1,
            value=1 if self._local_frc else 0,
            mask=TrConfBitMasks.LOCAL_FRC
        )

    @staticmethod
    def _validate_rf_channel_a(rf_channel_a: int) -> None:
        """Validate RF Channel A Parameter.

        Args:
            rf_channel_a (int): RF Channel A.

        Raises:
            RequestParameterInvalidValueError: If rf_channel_a is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= rf_channel_a <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('RF channel A value should be between 0 and 255.')

    @property
    def rf_channel_a(self) -> int:
        """:obj:`int`: RF Channel A.

        Getter and setter.
        """
        return self._rf_channel_a

    @rf_channel_a.setter
    def rf_channel_a(self, value: int):
        self._validate_rf_channel_a(rf_channel_a=value)
        self._rf_channel_a = value

    def get_rf_channel_a_byte(self) -> OsTrConfByte:
        """Returns RF channel A configuration byte.

        Returns:
            :obj:`OsTrConfByte`: RF channel A configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.RF_CHANNEL_A,
            value=self._rf_channel_a,
            mask=0xFF
        )

    @staticmethod
    def _validate_rf_channel_b(rf_channel_b: int) -> None:
        """Validate RF Channel B Parameter.

        Args:
            rf_channel_b (int): RF Channel B.

        Raises:
            RequestParameterInvalidValueError: If rf_channel_b is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= rf_channel_b <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('RF channel B value should be between 0 and 255.')

    @property
    def rf_channel_b(self) -> int:
        """:obj:`int`: RF Channel B.

        Getter and setter.
        """
        return self._rf_channel_b

    @rf_channel_b.setter
    def rf_channel_b(self, value: int):
        self._validate_rf_channel_b(rf_channel_b=value)
        self._rf_channel_b = value

    def get_rf_channel_b_byte(self) -> OsTrConfByte:
        """Returns RF channel B configuration byte.

        Returns:
            :obj:`OsTrConfByte`: RF channel B configuration byte.
        """
        return OsTrConfByte(
            address=TrConfByteAddrs.RF_CHANNEL_B,
            value=self._rf_channel_b,
            mask=0xFF
        )

    @staticmethod
    def _validate_reserved_block_0(data: List[int]) -> None:
        """Validate undocumented data bytes.

        Args:
            data (List[int]): Reserved data bytes.

        Raises:
            RequestParameterInvalidValueError: If data does not contain 2 values or if values are not
            in range from 0 to 255.
        """
        if len(data) != 2:
            raise RequestParameterInvalidValueError('Reserved block 0 should be 2B long.')
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Reserved block 0 values should be between 0 and 255.')

    @staticmethod
    def _validate_reserved_block_1(data: List[int]) -> None:
        """Validate undocumented data bytes.

        Args:
            data (List[int]): Reserved data bytes.

        Raises:
            RequestParameterInvalidValueError: If data does not contain 3 values or if values are not
            in range from 0 to 255.
        """
        if len(data) != 3:
            raise RequestParameterInvalidValueError('Reserved block 1 should be 3B long.')
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Reserved block 1 values should be between 0 and 255.')

    @staticmethod
    def _validate_reserved_block_2(data: List[int]) -> None:
        """Validate undocumented data bytes.

        Args:
            data (List[int]): Reserved data bytes.

        Raises:
            RequestParameterInvalidValueError: If data does not contain 13 values or if values are not
            in range from 0 to 255.
        """
        if len(data) != 13:
            raise RequestParameterInvalidValueError('Reserved block 2 should be 13B long.')
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Reserved block 2 values should be between 0 and 255.')

    @classmethod
    def from_pdata(cls, data: Union[List[int], bytearray]) -> 'OsTrConfData':
        """Deserialize DPA response pdata into OS TR Configuration data object.

        Returns:
            :obj:`OsTrConfData`: Deserialized OS TR Configuration data object.
        """
        if isinstance(data, bytearray):
            data = list(data)
        embed_pers_data = data[0:4]
        embedded_pers = []
        for i in range(0, len(embed_pers_data * 8)):
            if embed_pers_data[int(i / 8)] & (1 << (i % 8)):
                if i in EmbedPeripherals:
                    embedded_pers.append(EmbedPeripherals(i))
                else:
                    embedded_pers.append(i)
        embedded_peripherals = embedded_pers
        custom_dpa_handler = bool(data[4] & 1)
        dpa_peer_to_peer = bool(data[4] & 2)
        routing_off = bool(data[4] & 8)
        io_setup = bool(data[4] & 16)
        user_peer_to_peer = bool(data[4] & 32)
        stay_awake_when_not_bonded = bool(data[4] & 64)
        std_and_lp_network = bool(data[4] & 128)
        rf_output_power = data[7]
        rf_signal_filter = data[8]
        lp_rf_timeout = data[9]
        uart_baud_rate = data[10]
        alternative_dsm_channel = data[11]
        local_frc = bool(data[12] & 1)
        rf_channel_a = data[16]
        rf_channel_b = data[17]
        reserved_block_0 = data[5:7]
        reserved_block_1 = data[13:16]
        reserved_block_2 = data[18:]
        return cls(embedded_peripherals=embedded_peripherals, custom_dpa_handler=custom_dpa_handler,
                   dpa_peer_to_peer=dpa_peer_to_peer, routing_off=routing_off, io_setup=io_setup,
                   user_peer_to_peer=user_peer_to_peer, stay_awake_when_not_bonded=stay_awake_when_not_bonded,
                   std_and_lp_network=std_and_lp_network, rf_output_power=rf_output_power,
                   rf_signal_filter=rf_signal_filter, lp_rf_timeout=lp_rf_timeout,
                   uart_baud_rate=uart_baud_rate, alternative_dsm_channel=alternative_dsm_channel,
                   local_frc=local_frc, rf_channel_a=rf_channel_a, rf_channel_b=rf_channel_b,
                   reserved_block_0=reserved_block_0, reserved_block_1=reserved_block_1,
                   reserved_block_2=reserved_block_2)

    def to_pdata(self, to_bytes: bool = False) -> Union[List[int], bytearray]:
        """Serialize OS TR Configuration data object to DPA request pdata.

        Args:
            to_bytes (bool): Serialize into bytes.

        Returns:
            :obj:`list` of :obj:`int`: Serialized OS TR Configuration data.\n
            :obj:`bytearray`: Serialize OS TR Configuration data bytes if to_bytes is True.
        """
        embed_pers = Common.peripheral_list_to_bitmap(self.embedded_peripherals)
        conf_bits_0 = int(self.custom_dpa_handler) | int(self.dpa_peer_to_peer) << 1 | int(self.routing_off) << 3 | \
            int(self.io_setup) << 4 | int(self.user_peer_to_peer) << 5 | \
            int(self.stay_awake_when_not_bonded) << 6 | int(self.std_and_lp_network) << 7
        pdata = embed_pers + [conf_bits_0] + self._reserved_block_0 + \
            [
                self.rf_output_power,
                self.rf_signal_filter,
                self.lp_rf_timeout,
                self.uart_baud_rate,
                self.alternative_dsm_channel,
                int(self.local_frc)
            ] + self._reserved_block_1 + \
            [
                self.rf_channel_a,
                self.rf_channel_b
            ] + self._reserved_block_2
        if to_bytes:
            return bytearray(pdata)
        return pdata

    @staticmethod
    def calculate_checksum(data: List[int]) -> int:
        """Calculates checksum from TR configuration data.

        Args:
            data (List[int]): List of integers representing TR configuration data.

        Returns:
            int: Checksum value.
        """
        checksum = 0x5F
        for val in data:
            checksum ^= val
        return checksum
