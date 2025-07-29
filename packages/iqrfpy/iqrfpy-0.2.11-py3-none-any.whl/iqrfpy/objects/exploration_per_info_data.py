"""Exploration Peripheral Information Data object."""
from dataclasses import dataclass
from typing import Union
from iqrfpy.utils.dpa import PeripheralTypes


@dataclass
class ExplorationPerInfoData:
    """Exploration Peripheral Information Data class."""

    __slots__ = 'perte', 'pert', 'par1', 'par2'

    def __init__(self, result: dict):
        """Peripheral Information Data constructor.

        Args:
            result (dict): Peripheral enumeration result.
        """
        self.perte: int = result['perTe']
        """Extended peripheral characteristic."""
        self.pert: Union[PeripheralTypes, int] = result['perT']
        """Peripheral type. If the peripheral is not supported or enabled, value is equal
        to :obj:`PERIPHERAL_TYPE_DUMMY`."""
        self.par1 = result['par1']
        """Optional peripheral specific information."""
        self.par2 = result['par2']
        """Optional peripheral specific information."""
