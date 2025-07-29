from abc import ABC, abstractmethod
from typing import Optional, Union

import iqrfpy.peripherals.binaryoutput.responses as bo_responses
import iqrfpy.peripherals.coordinator.responses as c_responses
import iqrfpy.peripherals.eeeprom.responses as eeeprom_responses
import iqrfpy.peripherals.eeprom.responses as eeprom_responses
import iqrfpy.peripherals.exploration.responses as exploration_responses
import iqrfpy.peripherals.frc.responses as frc_responses
import iqrfpy.peripherals.io.responses as io_responses
import iqrfpy.peripherals.ledg.responses as ledg_responses
import iqrfpy.peripherals.ledr.responses as ledr_responses
import iqrfpy.peripherals.node.responses as node_responses
import iqrfpy.peripherals.os.responses as os_responses
import iqrfpy.peripherals.ram.responses as ram_responses
import iqrfpy.peripherals.sensor.responses as sensor_responses
import iqrfpy.peripherals.thermometer.responses as thermometer_responses
import iqrfpy.peripherals.uart.responses as uart_responses
from iqrfpy.async_response import AsyncResponse
from iqrfpy.confirmation import Confirmation
from iqrfpy.enums.commands import *
from iqrfpy.enums.message_types import *
from iqrfpy.enums.peripherals import *
from iqrfpy.exceptions import UnsupportedMessageTypeError, UnsupportedPeripheralCommandError, UnsupportedPeripheralError
from iqrfpy.iresponse import IResponse
from iqrfpy.peripherals.generic.responses import GenericResponse
from iqrfpy.utils.common import Common
from iqrfpy.utils.dpa import BYTE_MAX, CONFIRMATION_PACKET_LEN, REQUEST_PCMD_MAX, RESPONSE_PCMD_MIN, ResponseCodes, \
    ResponsePacketMembers, PNUM_MAX

__all__ = [
    'ResponseFactory',
    'BaseFactory',
]


class BaseFactory(ABC):
    """Response factory class abstraction."""

    @staticmethod
    @abstractmethod
    def create_from_dpa(dpa: bytes) -> IResponse:
        """Returns a response object created from DPA message."""

    @staticmethod
    @abstractmethod
    def create_from_json(json: dict) -> IResponse:
        """Returns a response object created from JSON API message."""


# Generic factories
class GenericResponseFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> GenericResponse:
        return GenericResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> IResponse:
        return GenericResponse.from_json(json=json)


class AsyncResponseFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> IResponse:
        return AsyncResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> IResponse:
        return AsyncResponse.from_json(json=json)


class ConfirmationFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> Confirmation:
        return Confirmation.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> Confirmation:
        return Confirmation.from_json(json=json)


# Coordinator factories
class CoordinatorAddrInfoFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.AddrInfoResponse:
        return c_responses.AddrInfoResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.AddrInfoResponse:
        return c_responses.AddrInfoResponse.from_json(json=json)


class CoordinatorAuthorizeBondFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.AuthorizeBondResponse:
        return c_responses.AuthorizeBondResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.AuthorizeBondResponse:
        return c_responses.AuthorizeBondResponse.from_json(json=json)


class CoordinatorBackupFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.BackupResponse:
        return c_responses.BackupResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.BackupResponse:
        return c_responses.BackupResponse.from_json(json=json)


class CoordinatorBondedDevicesFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.BondedDevicesResponse:
        return c_responses.BondedDevicesResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.BondedDevicesResponse:
        return c_responses.BondedDevicesResponse.from_json(json=json)


class CoordinatorBondNodeFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.BondNodeResponse:
        return c_responses.BondNodeResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.BondNodeResponse:
        return c_responses.BondNodeResponse.from_json(json=json)


class CoordinatorClearAllBondsFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.ClearAllBondsResponse:
        return c_responses.ClearAllBondsResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.ClearAllBondsResponse:
        return c_responses.ClearAllBondsResponse.from_json(json=json)


class CoordinatorDiscoveredDevicesFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.DiscoveredDevicesResponse:
        return c_responses.DiscoveredDevicesResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.DiscoveredDevicesResponse:
        return c_responses.DiscoveredDevicesResponse.from_json(json=json)


class CoordinatorDiscoveryFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.DiscoveryResponse:
        return c_responses.DiscoveryResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.DiscoveryResponse:
        return c_responses.DiscoveryResponse.from_json(json=json)


class CoordinatorRemoveBondFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.RemoveBondResponse:
        return c_responses.RemoveBondResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.RemoveBondResponse:
        return c_responses.RemoveBondResponse.from_json(json=json)


class CoordinatorRestoreFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.RestoreResponse:
        return c_responses.RestoreResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.RestoreResponse:
        return c_responses.RestoreResponse.from_json(json=json)


class CoordinatorSetDpaParamsFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.SetDpaParamsResponse:
        return c_responses.SetDpaParamsResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.SetDpaParamsResponse:
        return c_responses.SetDpaParamsResponse.from_json(json=json)


class CoordinatorSetHopsFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.SetHopsResponse:
        return c_responses.SetHopsResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.SetHopsResponse:
        return c_responses.SetHopsResponse.from_json(json=json)


class CoordinatorSetMIDFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.SetMidResponse:
        return c_responses.SetMidResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.SetMidResponse:
        return c_responses.SetMidResponse.from_json(json=json)


class CoordinatorSmartConnectFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> c_responses.SmartConnectResponse:
        return c_responses.SmartConnectResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> c_responses.SmartConnectResponse:
        return c_responses.SmartConnectResponse.from_json(json=json)


# EEEPROM factories
class EeepromReadFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> eeeprom_responses.ReadResponse:
        return eeeprom_responses.ReadResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> eeeprom_responses.ReadResponse:
        return eeeprom_responses.ReadResponse.from_json(json=json)


class EeepromWriteFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> eeeprom_responses.WriteResponse:
        return eeeprom_responses.WriteResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> eeeprom_responses.WriteResponse:
        return eeeprom_responses.WriteResponse.from_json(json=json)


# EEPROM factories
class EepromReadFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> eeprom_responses.ReadResponse:
        return eeprom_responses.ReadResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> eeprom_responses.ReadResponse:
        return eeprom_responses.ReadResponse.from_json(json=json)


class EepromWriteFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> eeprom_responses.WriteResponse:
        return eeprom_responses.WriteResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> eeprom_responses.WriteResponse:
        return eeprom_responses.WriteResponse.from_json(json=json)


# Exploration factories
class ExplorationPeripheralEnumerationFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> exploration_responses.PeripheralEnumerationResponse:
        return exploration_responses.PeripheralEnumerationResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> exploration_responses.PeripheralEnumerationResponse:
        return exploration_responses.PeripheralEnumerationResponse.from_json(json=json)


class ExplorationPeripheralInformationFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> exploration_responses.PeripheralInformationResponse:
        return exploration_responses.PeripheralInformationResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> exploration_responses.PeripheralInformationResponse:
        return exploration_responses.PeripheralInformationResponse.from_json(json=json)


class ExplorationMorePeripheralsInformationFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> exploration_responses.MorePeripheralsInformationResponse:
        return exploration_responses.MorePeripheralsInformationResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> exploration_responses.MorePeripheralsInformationResponse:
        return exploration_responses.MorePeripheralsInformationResponse.from_json(json=json)


# FRC factories
class FrcSendFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> frc_responses.SendResponse:
        return frc_responses.SendResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> frc_responses.SendResponse:
        return frc_responses.SendResponse.from_json(json=json)


class FrcExtraResultFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> frc_responses.ExtraResultResponse:
        return frc_responses.ExtraResultResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> frc_responses.ExtraResultResponse:
        return frc_responses.ExtraResultResponse.from_json(json=json)


class FrcSendSelectiveFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> frc_responses.SendSelectiveResponse:
        return frc_responses.SendSelectiveResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> frc_responses.SendSelectiveResponse:
        return frc_responses.SendSelectiveResponse.from_json(json=json)


class FrcSetFrcParamsFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> frc_responses.SetFrcParamsResponse:
        return frc_responses.SetFrcParamsResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> frc_responses.SetFrcParamsResponse:
        return frc_responses.SetFrcParamsResponse.from_json(json=json)


# IO factories
class IoDirectionFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> io_responses.DirectionResponse:
        return io_responses.DirectionResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> io_responses.DirectionResponse:
        return io_responses.DirectionResponse.from_json(json=json)


class IoGetFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> io_responses.GetResponse:
        return io_responses.GetResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> io_responses.GetResponse:
        return io_responses.GetResponse.from_json(json=json)


class IoSetFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> io_responses.SetResponse:
        return io_responses.SetResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> io_responses.SetResponse:
        return io_responses.SetResponse.from_json(json=json)


# LEDG factories
class LedgSetOnFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ledg_responses.SetOnResponse:
        return ledg_responses.SetOnResponse.from_dpa(dpa)

    @staticmethod
    def create_from_json(json: dict) -> ledg_responses.SetOnResponse:
        return ledg_responses.SetOnResponse.from_json(json)


class LedgSetOffFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ledg_responses.SetOffResponse:
        return ledg_responses.SetOffResponse.from_dpa(dpa)

    @staticmethod
    def create_from_json(json: dict) -> ledg_responses.SetOffResponse:
        return ledg_responses.SetOffResponse.from_json(json)


class LedgPulseFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ledg_responses.PulseResponse:
        return ledg_responses.PulseResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> ledg_responses.PulseResponse:
        return ledg_responses.PulseResponse.from_json(json=json)


class LedgFlashingFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ledg_responses.FlashingResponse:
        return ledg_responses.FlashingResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> ledg_responses.FlashingResponse:
        return ledg_responses.FlashingResponse.from_json(json=json)


# LEDR factories
class LedrSetOnFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ledr_responses.SetOnResponse:
        return ledr_responses.SetOnResponse.from_dpa(dpa)

    @staticmethod
    def create_from_json(json: dict) -> ledr_responses.SetOnResponse:
        return ledr_responses.SetOnResponse.from_json(json)


class LedrSetOffFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ledr_responses.SetOffResponse:
        return ledr_responses.SetOffResponse.from_dpa(dpa)

    @staticmethod
    def create_from_json(json: dict) -> ledr_responses.SetOffResponse:
        return ledr_responses.SetOffResponse.from_json(json)


class LedrPulseFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ledr_responses.PulseResponse:
        return ledr_responses.PulseResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> ledr_responses.PulseResponse:
        return ledr_responses.PulseResponse.from_json(json=json)


class LedrFlashingFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ledr_responses.FlashingResponse:
        return ledr_responses.FlashingResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> ledr_responses.FlashingResponse:
        return ledr_responses.FlashingResponse.from_json(json=json)


# Node factories
class NodeReadFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> node_responses.ReadResponse:
        return node_responses.ReadResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> node_responses.ReadResponse:
        return node_responses.ReadResponse.from_json(json=json)


class NodeRemoveBondFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> node_responses.RemoveBondResponse:
        return node_responses.RemoveBondResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> node_responses.RemoveBondResponse:
        return node_responses.RemoveBondResponse.from_json(json=json)


class NodeBackupFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> node_responses.BackupResponse:
        return node_responses.BackupResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> node_responses.BackupResponse:
        return node_responses.BackupResponse.from_json(json=json)


class NodeRestoreFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> node_responses.RestoreResponse:
        return node_responses.RestoreResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> node_responses.RestoreResponse:
        return node_responses.RestoreResponse.from_json(json=json)


class NodeValidateBondsFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> node_responses.ValidateBondsResponse:
        return node_responses.ValidateBondsResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> node_responses.ValidateBondsResponse:
        return node_responses.ValidateBondsResponse.from_json(json=json)


# OS factories
class OSReadFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.ReadResponse:
        return os_responses.ReadResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.ReadResponse:
        return os_responses.ReadResponse.from_json(json=json)


class OSResetFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.ResetResponse:
        return os_responses.ResetResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.ResetResponse:
        return os_responses.ResetResponse.from_json(json=json)


class OSRestartFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.RestartResponse:
        return os_responses.RestartResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.RestartResponse:
        return os_responses.RestartResponse.from_json(json=json)


class OSReadTrConfFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.ReadTrConfResponse:
        return os_responses.ReadTrConfResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.ReadTrConfResponse:
        return os_responses.ReadTrConfResponse.from_json(json=json)


class OSWriteTrConfFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.WriteTrConfResponse:
        return os_responses.WriteTrConfResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.WriteTrConfResponse:
        return os_responses.WriteTrConfResponse.from_json(json=json)


class OsWriteTrConfByteFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.WriteTrConfByteResponse:
        return os_responses.WriteTrConfByteResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.WriteTrConfByteResponse:
        return os_responses.WriteTrConfByteResponse.from_json(json=json)


class OSRfpgmFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.RfpgmResponse:
        return os_responses.RfpgmResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.RfpgmResponse:
        return os_responses.RfpgmResponse.from_json(json=json)


class OSSleepFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.SleepResponse:
        return os_responses.SleepResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.SleepResponse:
        return os_responses.SleepResponse.from_json(json=json)


class OSSetSecurityFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.SetSecurityResponse:
        return os_responses.SetSecurityResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.SetSecurityResponse:
        return os_responses.SetSecurityResponse.from_json(json=json)


class OSBatchFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.BatchResponse:
        return os_responses.BatchResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.BatchResponse:
        return os_responses.BatchResponse.from_json(json=json)


class OSSelectiveBatchFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.SelectiveBatchResponse:
        return os_responses.SelectiveBatchResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.SelectiveBatchResponse:
        return os_responses.SelectiveBatchResponse.from_json(json=json)


class OSIndicateFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.IndicateResponse:
        return os_responses.IndicateResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.IndicateResponse:
        return os_responses.IndicateResponse.from_json(json=json)


class OSFactorySettingsFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.FactorySettingsResponse:
        return os_responses.FactorySettingsResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.FactorySettingsResponse:
        return os_responses.FactorySettingsResponse.from_json(json=json)


class OSTestRfSignalFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.TestRfSignalResponse:
        return os_responses.TestRfSignalResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.TestRfSignalResponse:
        return os_responses.TestRfSignalResponse.from_json(json=json)


class OsLoadCodeFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> os_responses.LoadCodeResponse:
        return os_responses.LoadCodeResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> os_responses.LoadCodeResponse:
        return os_responses.LoadCodeResponse.from_json(json=json)


# RAM factories
class RamReadFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ram_responses.ReadResponse:
        return ram_responses.ReadResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> ram_responses.ReadResponse:
        return ram_responses.ReadResponse.from_json(json=json)


class RamWriteFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ram_responses.WriteResponse:
        return ram_responses.WriteResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> ram_responses.WriteResponse:
        return ram_responses.WriteResponse.from_json(json=json)


class RamReadAnyFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> ram_responses.ReadAnyResponse:
        return ram_responses.ReadAnyResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> ram_responses.ReadAnyResponse:
        return ram_responses.ReadAnyResponse.from_json(json=json)


# Thermometer factories
class ThermometerReadFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> thermometer_responses.ReadResponse:
        return thermometer_responses.ReadResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> thermometer_responses.ReadResponse:
        return thermometer_responses.ReadResponse.from_json(json=json)


# UART factories
class UartOpenFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> uart_responses.OpenResponse:
        return uart_responses.OpenResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> uart_responses.OpenResponse:
        return uart_responses.OpenResponse.from_json(json=json)


class UartCloseFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> uart_responses.CloseResponse:
        return uart_responses.CloseResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> uart_responses.CloseResponse:
        return uart_responses.CloseResponse.from_json(json=json)


class UartWriteReadFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> uart_responses.WriteReadResponse:
        return uart_responses.WriteReadResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> uart_responses.WriteReadResponse:
        return uart_responses.WriteReadResponse.from_json(json=json)


class UartClearWriteReadFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> uart_responses.ClearWriteReadResponse:
        return uart_responses.ClearWriteReadResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> uart_responses.ClearWriteReadResponse:
        return uart_responses.ClearWriteReadResponse.from_json(json=json)


# BinaryOutput factories
class BinaryOutputEnumerateFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> bo_responses.EnumerateResponse:
        return bo_responses.EnumerateResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> bo_responses.EnumerateResponse:
        return bo_responses.EnumerateResponse.from_json(json=json)


class BinaryOutputSetFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> bo_responses.SetOutputResponse:
        return bo_responses.SetOutputResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> bo_responses.SetOutputResponse:
        return bo_responses.SetOutputResponse.from_json(json=json)


# Sensor factories
class SensorEnumerateFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> sensor_responses.EnumerateResponse:
        return sensor_responses.EnumerateResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> sensor_responses.EnumerateResponse:
        return sensor_responses.EnumerateResponse.from_json(json=json)


class SensorReadSensorsFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> sensor_responses.ReadSensorsResponse:
        return sensor_responses.ReadSensorsResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> sensor_responses.ReadSensorsResponse:
        return sensor_responses.ReadSensorsResponse.from_json(json=json)


class SensorReadSensorsWithTypesFactory(BaseFactory):

    @staticmethod
    def create_from_dpa(dpa: bytes) -> sensor_responses.ReadSensorsWithTypesResponse:
        return sensor_responses.ReadSensorsWithTypesResponse.from_dpa(dpa=dpa)

    @staticmethod
    def create_from_json(json: dict) -> sensor_responses.ReadSensorsWithTypesResponse:
        return sensor_responses.ReadSensorsWithTypesResponse.from_json(json=json)


class ResponseFactory:
    """Response factory class."""

    _dpa_factories: dict = {
        EmbedPeripherals.COORDINATOR: {
            CoordinatorResponseCommands.ADDR_INFO: CoordinatorAddrInfoFactory(),
            CoordinatorResponseCommands.AUTHORIZE_BOND: CoordinatorAuthorizeBondFactory(),
            CoordinatorResponseCommands.BACKUP: CoordinatorBackupFactory(),
            CoordinatorResponseCommands.BONDED_DEVICES: CoordinatorBondedDevicesFactory(),
            CoordinatorResponseCommands.BOND_NODE: CoordinatorBondNodeFactory(),
            CoordinatorResponseCommands.CLEAR_ALL_BONDS: CoordinatorClearAllBondsFactory(),
            CoordinatorResponseCommands.DISCOVERED_DEVICES: CoordinatorDiscoveredDevicesFactory(),
            CoordinatorResponseCommands.DISCOVERY: CoordinatorDiscoveryFactory(),
            CoordinatorResponseCommands.REMOVE_BOND: CoordinatorRemoveBondFactory(),
            CoordinatorResponseCommands.RESTORE: CoordinatorRestoreFactory(),
            CoordinatorResponseCommands.SET_DPA_PARAMS: CoordinatorSetDpaParamsFactory(),
            CoordinatorResponseCommands.SET_HOPS: CoordinatorSetHopsFactory(),
            CoordinatorResponseCommands.SET_MID: CoordinatorSetMIDFactory(),
            CoordinatorResponseCommands.SMART_CONNECT: CoordinatorSmartConnectFactory(),
        },
        EmbedPeripherals.EEEPROM: {
            EEEPROMResponseCommands.READ: EeepromReadFactory(),
            EEEPROMResponseCommands.WRITE: EeepromWriteFactory(),
        },
        EmbedPeripherals.EEPROM: {
            EEPROMResponseCommands.READ: EepromReadFactory(),
            EEPROMResponseCommands.WRITE: EepromWriteFactory(),
        },
        EmbedPeripherals.EXPLORATION: {
            ExplorationResponseCommands.PERIPHERALS_ENUMERATION_INFORMATION: ExplorationPeripheralEnumerationFactory(),
        },
        EmbedPeripherals.FRC: {
            FrcResponseCommands.SEND: FrcSendFactory(),
            FrcResponseCommands.EXTRA_RESULT: FrcExtraResultFactory(),
            FrcResponseCommands.SEND_SELECTIVE: FrcSendSelectiveFactory(),
            FrcResponseCommands.SET_PARAMS: FrcSetFrcParamsFactory(),
        },
        EmbedPeripherals.IO: {
            IOResponseCommands.DIRECTION: IoDirectionFactory(),
            IOResponseCommands.GET: IoGetFactory(),
            IOResponseCommands.SET: IoSetFactory(),
        },
        EmbedPeripherals.LEDG: {
            LEDResponseCommands.SET_ON: LedgSetOnFactory(),
            LEDResponseCommands.SET_OFF: LedgSetOffFactory(),
            LEDResponseCommands.PULSE: LedgPulseFactory(),
            LEDResponseCommands.FLASHING: LedgFlashingFactory(),
        },
        EmbedPeripherals.LEDR: {
            LEDResponseCommands.SET_ON: LedrSetOnFactory(),
            LEDResponseCommands.SET_OFF: LedrSetOffFactory(),
            LEDResponseCommands.PULSE: LedrPulseFactory(),
            LEDResponseCommands.FLASHING: LedrFlashingFactory(),
        },
        EmbedPeripherals.NODE: {
            NodeResponseCommands.READ: NodeReadFactory(),
            NodeResponseCommands.REMOVE_BOND: NodeRemoveBondFactory(),
            NodeResponseCommands.BACKUP: NodeBackupFactory(),
            NodeResponseCommands.RESTORE: NodeRestoreFactory(),
            NodeResponseCommands.VALIDATE_BONDS: NodeValidateBondsFactory(),
        },
        EmbedPeripherals.OS: {
            OSResponseCommands.READ: OSReadFactory(),
            OSResponseCommands.RESET: OSResetFactory(),
            OSResponseCommands.RESTART: OSRestartFactory(),
            OSResponseCommands.READ_CFG: OSReadTrConfFactory(),
            OSResponseCommands.WRITE_CFG: OSWriteTrConfFactory(),
            OSResponseCommands.WRITE_CFG_BYTE: OsWriteTrConfByteFactory(),
            OSResponseCommands.RFPGM: OSRfpgmFactory(),
            OSResponseCommands.SLEEP: OSSleepFactory(),
            OSResponseCommands.SET_SECURITY: OSSetSecurityFactory(),
            OSResponseCommands.BATCH: OSBatchFactory(),
            OSResponseCommands.SELECTIVE_BATCH: OSSelectiveBatchFactory(),
            OSResponseCommands.INDICATE: OSIndicateFactory(),
            OSResponseCommands.FACTORY_SETTINGS: OSFactorySettingsFactory(),
            OSResponseCommands.TEST_RF_SIGNAL: OSTestRfSignalFactory(),
            OSResponseCommands.LOAD_CODE: OsLoadCodeFactory(),
        },
        EmbedPeripherals.RAM: {
            RAMResponseCommands.READ: RamReadFactory(),
            RAMResponseCommands.WRITE: RamWriteFactory(),
            RAMResponseCommands.READ_ANY: RamReadAnyFactory(),
        },
        EmbedPeripherals.THERMOMETER: {
            ThermometerResponseCommands.READ: ThermometerReadFactory(),
        },
        EmbedPeripherals.UART: {
            UartResponseCommands.OPEN: UartOpenFactory(),
            UartResponseCommands.CLOSE: UartCloseFactory(),
            UartResponseCommands.WRITE_READ: UartWriteReadFactory(),
            UartResponseCommands.CLEAR_WRITE_READ: UartClearWriteReadFactory(),
        },
        Standards.BINARY_OUTPUT: {
            BinaryOutputResponseCommands.ENUMERATE_OUTPUTS: BinaryOutputEnumerateFactory(),
            BinaryOutputResponseCommands.SET_OUTPUT: BinaryOutputSetFactory(),
        },
        Standards.SENSOR: {
            SensorResponseCommands.ENUMERATE: SensorEnumerateFactory(),
            SensorResponseCommands.READ_SENSORS: SensorReadSensorsFactory(),
            SensorResponseCommands.READ_SENSORS_WITH_TYPES: SensorReadSensorsWithTypesFactory(),
        },
    }
    """DPA factories, dictionary (pnum) of dictionaries (pcmd)."""

    _json_factories: dict = {
        GenericMessages.RAW: GenericResponseFactory(),
        CoordinatorMessages.ADDR_INFO: CoordinatorAddrInfoFactory(),
        CoordinatorMessages.AUTHORIZE_BOND: CoordinatorAuthorizeBondFactory(),
        CoordinatorMessages.BACKUP: CoordinatorBackupFactory(),
        CoordinatorMessages.BONDED_DEVICES: CoordinatorBondedDevicesFactory(),
        CoordinatorMessages.BOND_NODE: CoordinatorBondNodeFactory(),
        CoordinatorMessages.CLEAR_ALL_BONDS: CoordinatorClearAllBondsFactory(),
        CoordinatorMessages.DISCOVERED_DEVICES: CoordinatorDiscoveredDevicesFactory(),
        CoordinatorMessages.DISCOVERY: CoordinatorDiscoveryFactory(),
        CoordinatorMessages.REMOVE_BOND: CoordinatorRemoveBondFactory(),
        CoordinatorMessages.RESTORE: CoordinatorRestoreFactory(),
        CoordinatorMessages.SET_DPA_PARAMS: CoordinatorSetDpaParamsFactory(),
        CoordinatorMessages.SET_HOPS: CoordinatorSetHopsFactory(),
        CoordinatorMessages.SET_MID: CoordinatorSetMIDFactory(),
        CoordinatorMessages.SMART_CONNECT: CoordinatorSmartConnectFactory(),
        EEEPROMMessages.READ: EeepromReadFactory(),
        EEEPROMMessages.WRITE: EeepromWriteFactory(),
        EEPROMMessages.READ: EepromReadFactory(),
        EEPROMMessages.WRITE: EepromWriteFactory(),
        ExplorationMessages.ENUMERATE: ExplorationPeripheralEnumerationFactory(),
        ExplorationMessages.PERIPHERAL_INFORMATION: ExplorationPeripheralInformationFactory(),
        ExplorationMessages.MORE_PERIPHERALS_INFORMATION: ExplorationMorePeripheralsInformationFactory(),
        FrcMessages.SEND: FrcSendFactory(),
        FrcMessages.EXTRA_RESULT: FrcExtraResultFactory(),
        FrcMessages.SEND_SELECTIVE: FrcSendSelectiveFactory(),
        FrcMessages.SET_PARAMS: FrcSetFrcParamsFactory(),
        IOMessages.DIRECTION: IoDirectionFactory(),
        IOMessages.GET: IoGetFactory(),
        IOMessages.SET: IoSetFactory(),
        LEDGMessages.SET_ON: LedgSetOnFactory(),
        LEDGMessages.SET_OFF: LedgSetOffFactory(),
        LEDGMessages.PULSE: LedgPulseFactory(),
        LEDGMessages.FLASHING: LedgFlashingFactory(),
        LEDRMessages.SET_ON: LedrSetOnFactory(),
        LEDRMessages.SET_OFF: LedrSetOffFactory(),
        LEDRMessages.PULSE: LedrPulseFactory(),
        LEDRMessages.FLASHING: LedrFlashingFactory(),
        NodeMessages.READ: NodeReadFactory(),
        NodeMessages.REMOVE_BOND: NodeRemoveBondFactory(),
        NodeMessages.BACKUP: NodeBackupFactory(),
        NodeMessages.RESTORE: NodeRestoreFactory(),
        NodeMessages.VALIDATE_BONDS: NodeValidateBondsFactory(),
        OSMessages.READ: OSReadFactory(),
        OSMessages.RESET: OSResetFactory(),
        OSMessages.RESTART: OSRestartFactory(),
        OSMessages.READ_CFG: OSReadTrConfFactory(),
        OSMessages.WRITE_CFG: OSWriteTrConfFactory(),
        OSMessages.WRITE_CFG_BYTE: OsWriteTrConfByteFactory(),
        OSMessages.RFPGM: OSRfpgmFactory(),
        OSMessages.SLEEP: OSSleepFactory(),
        OSMessages.SET_SECURITY: OSSetSecurityFactory(),
        OSMessages.BATCH: OSBatchFactory(),
        OSMessages.SELECTIVE_BATCH: OSSelectiveBatchFactory(),
        OSMessages.INDICATE: OSIndicateFactory(),
        OSMessages.FACTORY_SETTINGS: OSFactorySettingsFactory(),
        OSMessages.TEST_RF_SIGNAL: OSTestRfSignalFactory(),
        OSMessages.LOAD_CODE: OsLoadCodeFactory(),
        RAMMessages.READ: RamReadFactory(),
        RAMMessages.WRITE: RamWriteFactory(),
        ThermometerMessages.READ: ThermometerReadFactory(),
        UartMessages.OPEN: UartOpenFactory(),
        UartMessages.CLOSE: UartCloseFactory(),
        UartMessages.WRITE_READ: UartWriteReadFactory(),
        UartMessages.CLEAR_WRITE_READ: UartClearWriteReadFactory(),
        BinaryOutputMessages.ENUMERATE: BinaryOutputEnumerateFactory(),
        BinaryOutputMessages.SET_OUTPUT: BinaryOutputSetFactory(),
        SensorMessages.ENUMERATE: SensorEnumerateFactory(),
        SensorMessages.READ_SENSORS_WITH_TYPES: SensorReadSensorsWithTypesFactory(),
    }
    """JSON API factories, dictionary (message types)."""

    @classmethod
    def get_factory_from_dpa(cls, pnum: Union[Peripheral, int], pcmd: Union[Command, int],
                             allow_generic: bool = False) -> BaseFactory:
        """Find response factory by combination of pnum and pcmd.

        Args:
            pnum (Union[Peripheral int]): Peripheral number.
            pcmd (Union[Command, int]): Peripheral command.
            allow_generic (bool): Use generic response factory if a matching factory for pnum and pcmd does not exist.

        Returns:
            :obj:`BaseFactory`: Response factory.

        Raises:
            UnsupportedPeripheralError: If pnum does not exist in response factories and allow_generic is False.
            UnsupportedPeripheralCommandError: If pcmd does not exist in response factories and allow_generic is False.
        """
        if pnum in cls._dpa_factories:
            if pcmd in cls._dpa_factories[pnum]:
                return cls._dpa_factories[pnum][pcmd]
            else:
                if allow_generic:
                    return GenericResponseFactory()
                else:
                    raise UnsupportedPeripheralCommandError(f'Unknown or unsupported peripheral command: {pcmd}')
        else:
            if allow_generic:
                return GenericResponseFactory()
            else:
                raise UnsupportedPeripheralError(f'Unknown or unsupported peripheral: {pnum}')

    @classmethod
    def get_factory_from_mtype(cls, message_type: Union[MessageType, str], msgid: Optional[str] = None) -> BaseFactory:
        """Find response factory by message type.

        Args:
            message_type (Union[MessageType, str): Message type.
            msgid (str, optional): Message ID, used for error handling.

        Returns:
            :obj:`BaseFactory`: Response factory.

        Raises:
            UnsupportedMessageTypeError: If message type does not exist in response factories.
        """
        if message_type in cls._json_factories:
            return cls._json_factories[message_type]
        raise UnsupportedMessageTypeError(f'Unknown or unsupported message type: {message_type}', msgid)

    @classmethod
    def get_response_from_dpa(cls, dpa: bytes, allow_generic: bool = False) -> IResponse:
        """Process DPA response and return corresponding response message object.

        Args:
            dpa (bytes): DPA response.
            allow_generic (bool): Use generic response class if pnum or pcmd is unknown.

        Returns:
            :obj:`IResponse`: Response object.
        """
        IResponse.validate_dpa_response(dpa)
        pnum = dpa[ResponsePacketMembers.PNUM]
        pcmd = dpa[ResponsePacketMembers.PCMD]
        rcode = dpa[ResponsePacketMembers.RCODE]
        if rcode == ResponseCodes.CONFIRMATION and len(dpa) == CONFIRMATION_PACKET_LEN:
            factory = ConfirmationFactory()
        elif pcmd <= REQUEST_PCMD_MAX and rcode >= ResponseCodes.ASYNC_RESPONSE:
            factory = AsyncResponseFactory()
        elif pnum <= PNUM_MAX and pcmd == ExplorationResponseCommands.PERIPHERALS_ENUMERATION_INFORMATION:
            factory = ExplorationPeripheralInformationFactory()
        elif pnum == BYTE_MAX and pcmd >= RESPONSE_PCMD_MIN and \
                pcmd != ExplorationResponseCommands.PERIPHERALS_ENUMERATION_INFORMATION:
            factory = ExplorationMorePeripheralsInformationFactory()
        else:
            try:
                peripheral = Common.pnum_from_dpa(pnum)
                command = Common.response_pcmd_from_dpa(peripheral, pcmd)
                factory = cls.get_factory_from_dpa(peripheral, command, allow_generic=allow_generic)
            except (UnsupportedPeripheralError, UnsupportedPeripheralCommandError) as err:
                if not allow_generic:
                    raise err
                factory = GenericResponseFactory()
        return factory.create_from_dpa(dpa)

    @classmethod
    def get_response_from_json(cls, json: dict) -> IResponse:
        """Process JSON API response and return corresponding response message object.

        Args:
            json (dict): JSON API response.
        Response:
            :obj:`IResponse`: Response object.
        """
        msgid = Common.msgid_from_json(json)
        mtype = Common.mtype_str_from_json(json)
        if msgid == IResponse.ASYNC_MSGID and \
                mtype in GenericMessages and GenericMessages(mtype) == GenericMessages.RAW:
            factory = AsyncResponseFactory()
        else:
            message = Common.string_to_mtype(mtype)
            factory = cls.get_factory_from_mtype(message, msgid)
        return factory.create_from_json(json)
