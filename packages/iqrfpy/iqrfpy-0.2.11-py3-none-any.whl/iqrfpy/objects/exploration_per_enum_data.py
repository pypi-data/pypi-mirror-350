"""Exploration Peripheral Enumeration Data object."""
from dataclasses import dataclass
from typing import List


@dataclass
class ExplorationPerEnumData:
    """Exploration Peripheral Enumeration Data class."""

    __slots__ = 'dpa_version', 'user_per_nr', 'embedded_pers', 'hwpid', 'hwpid_ver', 'flags', 'user_per'

    def __init__(self, result: dict, os_read: bool = False):
        """Peripheral Enumeration Data constructor.

        Args:
            result (dict): Peripheral enumeration result.
            os_read (boolean): Data parsed from OS Read response.
        """
        self.dpa_version: int = result['dpaVer']
        """DPA version."""
        self.user_per_nr: int = result['perNr']
        """Number of non-embedded peripherals implemented by custom DPA handler."""
        self.embedded_pers: List[int] = result['embeddedPers']
        """List of embedded peripherals implemented by device."""
        self.hwpid: int = result['hwpid']
        """Hardware profile ID."""
        self.hwpid_ver: int = result['hwpidVer']
        """Hardware profile version."""
        self.flags: int = result['flagsEnum' if os_read else 'flags']
        """Device function flags."""
        self.user_per: List[int] = result['userPer']
        """List of non-embedded peripherals implemented by device."""
