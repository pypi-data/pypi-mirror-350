"""OS Read Data object."""
from dataclasses import dataclass
from .exploration_per_enum_data import ExplorationPerEnumData
from .tr_mcu_type_data import TrMcuTypeData


@dataclass
class OsReadData:
    """OS Read Data class."""

    __slots__ = 'mid', 'os_version', 'tr_mcu_type', 'os_build', 'rssi', 'supply_voltage', 'flags', 'slot_limits', 'ibk', \
        'per_enum'

    def __init__(self, data: dict):
        """Read Data constructor.

        Args:
            data (dict): OS Read data.
        """
        self.mid: int = data['mid']
        """Module ID."""
        self.os_version: int = data['osVersion']
        """OS version."""
        self.tr_mcu_type: TrMcuTypeData = TrMcuTypeData(data['trMcuType'])
        """MCU type and TR series."""
        self.os_build: int = data['osBuild']
        """OS build."""
        self.rssi: int = data['rssi']
        """RSSI."""
        self.supply_voltage: int = data['supplyVoltage']
        """Supply voltage."""
        self.flags: int = data['flags']
        """OS flags."""
        self.slot_limits: int = data['slotLimits']
        """Slot limits."""
        self.ibk: int = data['ibk']
        """Individual bonding key."""
        self.per_enum: ExplorationPerEnumData = ExplorationPerEnumData(data, os_read=True)
        """Peripheral enumeration data."""
