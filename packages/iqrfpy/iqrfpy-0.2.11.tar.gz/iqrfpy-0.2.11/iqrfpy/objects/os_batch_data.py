"""OS Batch Data parameters."""
from typing import List, Optional, Union
from iqrfpy.enums.commands import Command
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants


class OsBatchData:
    """Batch Data class."""

    __slots__ = '_pnum', '_pcmd', '_hwpid', '_pdata'

    def __init__(self, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int = dpa_constants.HWPID_MAX,
                 pdata: Optional[List[int]] = None):
        """Batch Data constructor.

        Args:
            pnum (Union[Peripheral, int]): Peripheral number.
            pcmd (Union[Command, int]): Peripheral command.
            hwpid (int): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            pdata (List[int], optional): Request data.
        """
        self._validate(pnum=pnum, pcmd=pcmd, hwpid=hwpid, pdata=pdata)
        self._pnum = pnum
        self._pcmd = pcmd
        self._hwpid = hwpid
        self._pdata = pdata if pdata is not None else []

    def _validate(self, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int,
                  pdata: Optional[List[int]] = None):
        """Validate batch parameters.

        Args:
            pnum (Union[Peripheral, int]): Peripheral number.
            pcmd (Union[Command, int]): Peripheral command.
            hwpid (int): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            pdata (List[int], optional): Request data.
        """
        self._validate_pnum(pnum)
        self._validate_pcmd(pcmd)
        self._validate_hwpid(hwpid)
        self._validate_pdata(pdata)

    @staticmethod
    def _validate_pnum(pnum: Union[Peripheral, int]):
        """Validate peripheral number parameter.

        Args:
            pnum (Union[Peripheral, int]): Peripheral number.

        Raises:
            RequestParameterInvalidValueError: If pnum is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= pnum <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('PNUM value should be between 0 and 255.')

    @property
    def pnum(self) -> Union[Peripheral, int]:
        """:obj:`Peripheral` or :obj:`int`: Peripheral number.

        Getter and setter.
        """
        return self._pnum

    @pnum.setter
    def pnum(self, value: Union[Peripheral, int]):
        self._validate_pnum(value)
        self._pnum = value

    @staticmethod
    def _validate_pcmd(pcmd: Union[Command, int]):
        """Validate peripheral command parameter.

        Args:
            pcmd (Union[Command, int]): Peripheral command.

        Raises:
            RequestParameterInvalidValueError: If pcmd is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= pcmd <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('PCMD value should be between 0 and 255.')

    @property
    def pcmd(self) -> Union[Command, int]:
        """:obj:`Command` or :obj:`int`: Peripheral command.

        Getter and setter.
        """
        return self._pcmd

    @pcmd.setter
    def pcmd(self, value: Union[Command, int]):
        self._validate_pcmd(value)
        self._pcmd = value

    @staticmethod
    def _validate_hwpid(hwpid: int):
        """Validate hardware profile ID parameter.

        Args:
            hwpid (int): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.

        Raises:
            RequestParameterInvalidValueError: If hwpid is less than 0 or greater than 65535.
        """
        if not dpa_constants.HWPID_MIN <= hwpid <= dpa_constants.HWPID_MAX:
            raise RequestParameterInvalidValueError('HWPID value should be between 0 and 65535.')

    @property
    def hwpid(self) -> int:
        """:obj:`int`: Hardware profile ID.

        Getter and setter.
        """
        return self._hwpid

    @hwpid.setter
    def hwpid(self, value: int):
        self._validate_hwpid(value)
        self._hwpid = value

    @staticmethod
    def _validate_pdata(pdata: Optional[List[int]] = None):
        """Validate pdata parameter.

        Args:
            pdata (List[int], optional): Request data.
        """
        if pdata is None:
            return
        if not Common.values_in_byte_range(pdata):
            raise RequestParameterInvalidValueError('PDATA values should be between 0 and 255.')

    @property
    def pdata(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int` or :obj:`None`: Request data.

        Getter and setter.
        """
        return self._pdata

    @pdata.setter
    def pdata(self, value: Optional[List[int]] = None):
        self._validate_pdata(value)
        self._pdata = value if value is not None else []

    def to_pdata(self) -> List[int]:
        """Serialize batch data into DPA request pdata.

        Returns:
            :obj:`list` of :obj:`int`: Serialized DPA request pdata.
        """
        data = [self._pnum, self._pcmd, self._hwpid & 0xFF, (self._hwpid >> 8) & 0xFF] + self._pdata
        return [len(data) + 1] + data

    def to_json(self) -> dict:
        """Serialize batch data into JSON API request data.

        Returns:
            :obj:`dict`: Serialized JSON API request data.
        """
        data = {
            'pnum': f'{self._pnum:02x}',
            'pcmd': f'{self._pcmd:02x}',
            'hwpid': f'{self._hwpid:04x}',
        }
        if self._pdata is not None and len(self._pdata) > 0:
            data['rdata'] = '.'.join([f'{x:02x}' for x in self._pdata])
        return data
