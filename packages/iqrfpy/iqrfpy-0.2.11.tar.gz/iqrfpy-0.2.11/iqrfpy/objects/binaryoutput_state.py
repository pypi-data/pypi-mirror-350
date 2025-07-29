"""Binary Output State parameters."""
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants


class BinaryOutputState:
    """Binary Output State class."""

    __slots__ = '_index', '_state'

    def __init__(self, index: int, state: int):
        """Binary Output State constructor.

        Each binary output can be configured using the :obj:`state` value as follows:
        - 0 - sets output to OFF state
        - 1 - sets output to ON state
        - 2-127 - sets output to ON state for the next 2-127 minutes
        - 128 - reserved
        - 129-255 - sets output to ON state for the next 1-127 seconds

        Args:
            index (int): Binary output index.
            state (int): State to set.
        """
        self._validate(index=index, state=state)
        self._index = index
        self._state = state

    def _validate(self, index: int, state: int):
        """Validate binary output state parameters.

        Args:
            index (int): Binary output index.
            state (int): State to set.
        """
        self._validate_index(index=index)
        self._validate_state(state=state)

    @staticmethod
    def _validate_index(index: int):
        """Validate binary output index parameter.

        Args:
            index (int): Binary output index.

        Raises:
            RequestParameterInvalidValueError: If index is less than 0 or greater than 31.
        """
        if not dpa_constants.BINOUT_INDEX_MIN <= index <= dpa_constants.BINOUT_INDEX_MAX:
            raise RequestParameterInvalidValueError('Index value should be between 0 and 31.')

    @property
    def index(self) -> int:
        """:obj:`int`: Binary output index.

        Getter and setter.
        """
        return self._index

    @index.setter
    def index(self, value: int):
        self._validate_index(index=value)
        self._index = value

    @staticmethod
    def _validate_state(state: int):
        """Validate binary output state parameter.

        Args:
            state (int): State to set.

        Raises:
            RequestParameterInvalidValueError: If state is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= state <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('State value should be between 0 and 255.')

    @property
    def state(self) -> int:
        """:obj:`int`: Binary output state.

        Getter and setter.
        """
        return self._state

    @state.setter
    def state(self, value: int):
        self._validate_state(state=value)
        self._state = value

    def to_json(self) -> dict:
        """Serialize Binary Output State to JSON API param.

        Returns:
            dict: JSON-serialized Binary Output State
        """
        record = {
            'index': self.index,
            'state': self.state > 0,
        }
        if 2 <= self.state <= 127:
            record['time'] = self.state * 60
        elif 128 <= self.state <= 255:
            record['time'] = self.state - 128
        return record
