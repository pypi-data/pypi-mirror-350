"""Response message class abstraction."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union
from iqrfpy.enums.commands import Command
from iqrfpy.enums.message_types import MessageType
from iqrfpy.enums.peripherals import Peripheral
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.validators import DpaValidator

__all__ = ['IResponse', 'IResponseGetterMixin']


class IResponse(ABC):
    """This class serves as an interface for embedded peripherals and standards response messages.

    This class does not provide any deserialization logic in its factory methods as they simply serve as abstracts.

    Once a factory method is implemented, it should be used to parse responses and create response message objects.
    """

    ASYNC_MSGID = 'async'

    def __init__(self, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int],
                 hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 pdata: Optional[List[int]] = None, m_type: Optional[Union[MessageType, str]] = None,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        self._nadr = nadr
        self._pnum = pnum
        self._pcmd = pcmd
        self._mtype = m_type
        self._hwpid = hwpid
        self._rcode = rcode
        self._dpa_value = dpa_value
        self._pdata = pdata
        self._msgid = msgid
        self._result = result

    @property
    @abstractmethod
    def nadr(self) -> int:
        """:obj:`int`: Device address.

        Getter only.
        """
        return self._nadr

    @property
    @abstractmethod
    def pnum(self) -> Union[Peripheral, int]:
        """:obj:`Peripheral` or :obj:`int`: Peripheral number.

        Getter only.
        """
        return self._pnum

    @property
    @abstractmethod
    def pcmd(self) -> Union[Command, int]:
        """:obj:`Command` or :obj:`int`: Peripheral command.

        Getter only.
        """
        return self._pcmd

    @property
    @abstractmethod
    def mtype(self) -> Optional[Union[MessageType, str]]:
        """:obj:`MessageType` or :obj:`str` or :obj:`None`: Message type.

        Getter only.
        """
        return self._mtype

    @property
    @abstractmethod
    def hwpid(self) -> int:
        """:obj:`int`: Hardware profile ID.

        Getter only.
        """
        return self._hwpid

    @property
    @abstractmethod
    def rcode(self) -> int:
        """:obj:`int`: DPA error code.

        Getter only.
        """
        return self._rcode

    @property
    @abstractmethod
    def dpa_value(self) -> int:
        """:obj:`int`: DPA value.

        Getter only.
        """
        return self._dpa_value

    @property
    @abstractmethod
    def pdata(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int`: DPA response data.

        Getter only.
        """
        return self._pdata

    @property
    @abstractmethod
    def result(self) -> Optional[dict]:
        """:obj:`dict` or :obj:`None`: JSON API response data.

        Getter only.
        """
        return self._result

    @property
    @abstractmethod
    def msgid(self) -> Optional[str]:
        """:obj:`str` or :obj:`None`: Message ID.

        Getter only.
        """
        return self._msgid

    @staticmethod
    def validate_dpa_response(data: bytes) -> None:
        """Validate DPA response for base response length.

        Args:
            data (bytes): DPA response.
        """
        DpaValidator.base_response_length(data)

    @classmethod
    @abstractmethod
    def from_dpa(cls, dpa: bytes) -> 'IResponse':
        """Factory method. Parse DPA response into Response object.

        Args:
            dpa (bytes): DPA response.
        """

    @classmethod
    @abstractmethod
    def from_json(cls, json: dict) -> 'IResponse':
        """Factory method. Parse JSON response into Response object.

        Args:
            json (dict): JSON API response.
        """


class IResponseGetterMixin(IResponse):
    """Response mixin."""

    @property
    def nadr(self) -> int:
        """:obj:`int`: Device address.

        Getter only.
        """
        return super().nadr

    @property
    def pnum(self) -> Union[Peripheral, int]:
        """:obj:`Peripheral` or :obj:`int`: Peripheral number.

        Getter only.
        """
        return super().pnum

    @property
    def pcmd(self) -> Union[Command, int]:
        """:obj:`Command` or :obj:`int`: Peripheral command.

        Getter only.
        """
        return super().pcmd

    @property
    def mtype(self) -> Union[MessageType, str]:
        """:obj:`MessageType` or :obj:`str` or :obj:`None`: Message type.

        Getter only.
        """
        return super().mtype

    @property
    def hwpid(self) -> int:
        """:obj:`int`: Hardware profile ID.

        Getter only.
        """
        return super().hwpid

    @property
    def rcode(self) -> int:
        """:obj:`int`: DPA error code.

        Getter only.
        """
        return super().rcode

    def get_rcode_as_string(self) -> str:
        """Return rcode as string.

        Returns:
            str: String representation of rcode.
        """
        return dpa_constants.ResponseCodes.to_string(self.rcode)

    @property
    def dpa_value(self) -> int:
        """:obj:`int`: DPA value.

        Getter only.
        """
        return super().dpa_value

    @property
    def pdata(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int`: DPA response data.

        Getter only.
        """
        return super().pdata

    @property
    def result(self) -> Optional[dict]:
        """:obj:`dict` or :obj:`None`: JSON API response data.

        Getter only.
        """
        return super().result

    @property
    def msgid(self) -> Optional[str]:
        """:obj:`str` or :obj:`None`: Message ID.

        Getter only.
        """
        return super().msgid

    @classmethod
    def from_dpa(cls, dpa: bytes) -> IResponse:
        """Factory method. Parse DPA response into Response object.

        Args:
            dpa (bytes): DPA response.

        Raises:
            NotImplementedError: Factory method for mixin not implemented.
        """
        raise NotImplementedError('from_dpa() method not implemented.')

    @classmethod
    def from_json(cls, json: dict) -> IResponse:
        """Factory method. Parse JSON response into Response object.

        Args:
            json (dict): JSON API response.

        Raises:
            NotImplementedError: Factory method for mixin not implemented.
        """
        raise NotImplementedError('from_json() method not implemented.')
