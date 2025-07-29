"""FRC parser module.

Provides methods for parsing and processing FRC data.
"""
import math
from typing import List, Union
from iqrfpy.utils.dpa import FrcCommands


class FrcParser:
    """Class for handling FRC data."""

    @staticmethod
    def values_from_data(data: List[int], extra_data: List[int], frc_command: Union[int, FrcCommands]) -> List[int]:
        """Convert FRC data and extra result data into values collected by FRC commands.

        Note that the method expects raw data and a combined length of 64 bytes from FRC send and extra result requests.

        2 bit FRC commands produces 240 values. 1 byte FRC commands produce 64 values.
        2 byte FRC commands produces 32 values. 4 byte FRC commands produce 16 values.
        The first value should always be a dummy value 0.

        Args:
            data (List[int]): FRC Send request data
            extra_data (List[int]): FRC ExtraResult request data
            frc_command (Union[int, FrcCommands]): FRC command
        Returns:
            :obj:`list` of :obj`int`: Values from collected FRC data
        Raises:
            ValueError: Raised if combined data length is not 64 bytes
        """
        aux = data + extra_data
        if len(aux) != 64:
            raise ValueError('Combined length of FRC data and ExtraResult data should be 64 bytes.')
        if FrcCommands.FRC_2BIT_FROM <= frc_command <= FrcCommands.FRC_2BIT_TO:
            values = []
            for i in range(0, 240):
                mask = 1 << (i % 8)
                idx = math.floor(i / 8)
                val = 0
                if (aux[idx] & mask) != 0:
                    val = 1
                if (aux[idx + 32] & mask) != 0:
                    val |= 2
                values.append(val)
            return values
        if FrcCommands.FRC_1BYTE_FROM <= frc_command <= FrcCommands.FRC_1BYTE_TO:
            return aux
        if FrcCommands.FRC_2BYTE_FROM <= frc_command <= FrcCommands.FRC_2BYTE_TO:
            return [(aux[i + 1] << 8) + aux[i] for i in range(0, len(aux), 2)]
        return [(aux[i + 3] << 24) + (aux[i + 2] << 16) + (aux[i + 1] << 8) + aux[i] for i in range(0, len(aux), 4)]
