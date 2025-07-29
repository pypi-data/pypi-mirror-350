"""TR configuration InitPHY data class."""

from dataclasses import dataclass
from typing import Optional

from ..utils.dpa import RfBands


@dataclass
class InitPhyData:
    """TR configuration InitPhy data class."""

    __slots__ = 'rf_band', 'thermometer_present', 'serial_eeprom_present', 'il_type', 'value'

    def __init__(self, val: int):
        """TR configuration InitPhy data constructor.

        Args:
            val (int): InitPhy value.
        """
        rf_band = val & 0x03
        self.rf_band: Optional[RfBands] = RfBands(rf_band) if rf_band in RfBands else None
        """RF Band."""
        self.thermometer_present = bool(val & 0x10)
        """Thermometer chip is present."""
        self.serial_eeprom_present = bool(val & 0x20)
        """Serial EEPROM chip is present."""
        self.il_type = bool(val & 0x40)
        """Transceiver for Israel region."""
        self.value: int = val
        """Raw value."""
