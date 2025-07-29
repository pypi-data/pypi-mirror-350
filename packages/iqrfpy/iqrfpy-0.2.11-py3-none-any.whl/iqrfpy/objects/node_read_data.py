"""Node Read Data parameters."""
from dataclasses import dataclass


@dataclass
class NodeReadData:
    """Node Read Data class."""

    __slots__ = 'ntw_addr', 'ntw_vrn', 'ntw_zin', 'ntw_did', 'ntw_pvrn', 'ntw_useraddr', 'ntw_id', 'ntw_vrnfnz', \
        'ntw_cfg', 'flags'

    def __init__(self, data: dict):
        """Node Read Data constructor.

        Args:
            data (dict): Node read result.
        """
        self.ntw_addr: int = data['ntwADDR']
        """Logical node address."""
        self.ntw_vrn: int = data['ntwVRN']
        """Virtual routing number."""
        self.ntw_zin: int = data['ntwZIN']
        """Zone index (zone number + 1)."""
        self.ntw_did: int = data['ntwDID']
        """Discovery ID."""
        self.ntw_pvrn: int = data['ntwPVRN']
        """Parent virtual routing number."""
        self.ntw_useraddr: int = data['ntwUSERADDRESS']
        """User address."""
        self.ntw_id: int = data['ntwID']
        """Network identification."""
        self.ntw_vrnfnz: int = data['ntwVRNFNZ']
        """Virtual routing number of first node in zone."""
        self.ntw_cfg: int = data['ntwCFG']
        """Network configuration."""
        self.flags: int = data['flags']
        """Node flags."""
