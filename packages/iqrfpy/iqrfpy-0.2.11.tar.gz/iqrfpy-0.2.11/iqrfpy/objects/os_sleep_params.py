"""OS Sleep request parameters."""
from typing import List
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants


class OsSleepParams:
    """OS Sleep Params class."""

    __slots__ = '_time', 'wake_up_on_negative_edge', 'calibrate_before_sleep', 'flash_led_after_sleep', \
        'wake_up_on_positive_edge', 'use_milliseconds', 'use_deep_sleep'

    def __init__(self, time: int = 0, wake_up_on_negative_edge: bool = False, calibrate_before_sleep: bool = False,
                 flash_led_after_sleep: bool = False, wake_up_on_positive_edge: bool = False,
                 use_milliseconds: bool = False, use_deep_sleep: bool = False):
        """Sleep Params constructor.

        Args:
            time (int): Sleep time.
            wake_up_on_negative_edge (bool): Wake up on PORT B, bit 4 negative edge change.
            calibrate_before_sleep (bool): Run calibration process before sleep.
            flash_led_after_sleep (bool): Flash green LED once after waking up.
            wake_up_on_positive_edge (bool): Wake up on PORT B, bit 4 positive edge change.
            use_milliseconds (bool): Use sleep time with unit of 32.768 ms instead of 2.097s.
            use_deep_sleep (bool): The IC is shutdown during sleep.
        """
        self._validate_time(time)
        self._time = time
        self.wake_up_on_negative_edge = wake_up_on_negative_edge
        """Wake up on PORT B, bit 4 negative edge change."""
        self.calibrate_before_sleep = calibrate_before_sleep
        """Run calibration process before sleep."""
        self.flash_led_after_sleep = flash_led_after_sleep
        """Flash green LED once after waking up."""
        self.wake_up_on_positive_edge = wake_up_on_positive_edge
        """Wake up on PORT B, bit 4 positive edge change."""
        self.use_milliseconds = use_milliseconds
        """Use sleep time with unit of 32.768 ms instead of 2.097s."""
        self.use_deep_sleep = use_deep_sleep
        """The IC is shutdown during sleep."""

    @staticmethod
    def _validate_time(time: int):
        """Validate sleep time parameter.

        Args:
            time (int): Sleep time.

        Raises:
            RequestParameterInvalidValueError: If time is less than 0 or greater than 255.
        """
        if not dpa_constants.WORD_MIN <= time <= dpa_constants.WORD_MAX:
            raise RequestParameterInvalidValueError('Time value should be between 0 and 65535.')

    @property
    def time(self) -> int:
        """:obj:`int`: Sleep time.

        Getter and setter.
        """
        return self._time

    @time.setter
    def time(self, value: int):
        self._validate_time(value)
        self._time = value

    def _calculate_control(self) -> int:
        """Convert flags into a single value.

        Returns:
            :obj:`int`: Flags value.
        """
        return self.wake_up_on_negative_edge | (self.calibrate_before_sleep << 1) | \
            (self.flash_led_after_sleep << 2) | (self.wake_up_on_positive_edge << 3) | \
            (self.use_milliseconds << 4) | (self.use_deep_sleep << 5)

    def to_pdata(self) -> List[int]:
        """Serialize sleep parameters into DPA request pdata.

        Returns:
            :obj:`list` of :obj:`int`: Serialized DPA request pdata.
        """
        return [self._time & 0xFF, (self.time >> 8) & 0xFF, self._calculate_control()]

    def to_json(self) -> dict:
        """Serializes sleep parameters into JSON API request data.

        Returns:
            :obj:`dict`: Serialized JSON API request data.
        """
        return {
            'time': self._time,
            'control': self._calculate_control()
        }
