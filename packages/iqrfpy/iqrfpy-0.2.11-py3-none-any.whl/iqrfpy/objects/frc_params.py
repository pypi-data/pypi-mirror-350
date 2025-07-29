"""FRC Params parameters."""
from dataclasses import dataclass
from iqrfpy.utils.dpa import FrcResponseTimes


@dataclass
class FrcParams:
    """FRC Params class."""

    __slots__ = 'offline_frc', 'frc_response_time'

    def __init__(self, offline_frc: bool = False, frc_response_time: FrcResponseTimes = FrcResponseTimes.MS40):
        """FRC Params constructor.

        Args:
            offline_frc (bool): Offline FRC.
            frc_response_time (FrcResponseTimes): FRC response time.
        """
        self.offline_frc: bool = offline_frc
        """Offline FRC."""
        self.frc_response_time: FrcResponseTimes = frc_response_time
        """FRC response time."""

    @classmethod
    def from_int(cls, value: int) -> 'FrcParams':
        """Deserializes FRC Params integer value into FRC Params object.

        Args:
            value (int): FRC params integer value.
        """
        return cls(
            offline_frc=bool(value & 0x08),
            frc_response_time=FrcResponseTimes(value & 0x70)
        )

    def to_data(self) -> int:
        """Serialize FRC Params object into an integer value.

        Returns:
            :obj:`int`: Serialized FRC params value.
        """
        return self.frc_response_time | int(self.offline_frc) << 3
