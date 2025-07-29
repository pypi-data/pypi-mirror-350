"""TR MCU type data."""

from dataclasses import dataclass
from typing import Optional, Union

from ..utils.dpa import McuTypes, TrDTypes, TrGTypes


@dataclass
class TrMcuTypeData:
    """TR MCU Type data class."""

    __slots__ = 'mcu_type', 'tr_series', 'fcc_certified', 'value'

    def __init__(self, val: int):
        """TR MCU Type constructor.

        Args:
            val (int): TR MCU Type value.
        """
        mcu_type = val & 0x07
        self.mcu_type: Optional[McuTypes] = McuTypes(mcu_type) if mcu_type in McuTypes else None
        """MCU type."""
        tr_series = (val & 0xF0) >> 4
        tr_series_val = None
        if self.mcu_type == McuTypes.PIC16LF1938 and tr_series in TrDTypes:
            tr_series_val = TrDTypes(tr_series)
        elif self.mcu_type == McuTypes.PIC16LF18877 and tr_series in TrGTypes:
            tr_series_val = TrGTypes(tr_series)
        self.tr_series: Optional[Union[TrDTypes, TrGTypes]] = tr_series_val
        """TR series."""
        self.fcc_certified = bool(val & 0x08)
        """FCC certified."""
        self.value: int = val
        """Raw value."""
