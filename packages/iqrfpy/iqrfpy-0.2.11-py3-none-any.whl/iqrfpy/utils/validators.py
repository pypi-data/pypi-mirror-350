"""Validators module.

This module classes for validation of DPA and JSON messages and their parameters.
"""

from iqrfpy.exceptions import DpaConfirmationPacketError, DpaConfirmationPacketLengthError, \
    DpaResponsePacketLengthError, MessageNotReceivedError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes


__all__ = [
    'DpaValidator',
    'JsonValidator'
]


class DpaValidator:
    """DPA message validator class."""

    @staticmethod
    def base_response_length(dpa: bytes) -> None:
        """Check if DPA response length is at least equal to general response containing no data.

        Args:
            dpa (bytes): DPA response
        Raises:
            DpaResponsePacketLengthError: Raised if DPA response is shorter than general response containing no data
        """
        if len(dpa) < dpa_constants.RESPONSE_GENERAL_LEN:
            raise DpaResponsePacketLengthError('DPA response packet too short.')

    @staticmethod
    def confirmation_length(dpa: bytes) -> None:
        """Check if DPA confirmation message length is correct.

        Args:
            dpa (bytes): DPA confirmation
        Raises:
            DpaConfirmationPacketLengthError: Raised if DPA confirmation message length is not correct.
        """
        if len(dpa) != dpa_constants.CONFIRMATION_PACKET_LEN:
            raise DpaConfirmationPacketLengthError('Invalid DPA confirmation packet length.')

    @staticmethod
    def confirmation_code(dpa: bytes) -> None:
        """Check if DPA confirmation message code is correct.

        Args:
            dpa (bytes): DPA confirmation
        Raises:
            DpaConfirmationPacketError: Raised if DPA confirmation code is incorrect.
        """
        if dpa[dpa_constants.ResponsePacketMembers.RCODE] != ResponseCodes.CONFIRMATION:
            raise DpaConfirmationPacketError('Invalid DPA confirmation packet error code.')

    @staticmethod
    def response_length(dpa: bytes, expected_len: int) -> None:
        """Check if DPA response length equals expected length.

        Args:
            dpa (bytes): DPA response
            expected_len (int): Expected response length
        Raises
            DpaResponsePacketLengthError: Raised if DPA response length does not equal expected length
        """
        if len(dpa) != expected_len:
            raise DpaResponsePacketLengthError(f'DPA response packet length invalid, '
                                               f'expected payload of {expected_len}B, got payload of {len(dpa)}B.')


class JsonValidator:
    """JSON API message validator class."""

    @staticmethod
    def response_received(json: dict) -> None:
        """Check if DPA response has been received.

        While DPA response may not be sent or received for one reason or another,
        JSON API will always send a response and it is necessary to check for DPA response data.

        Args:
            json (dict): JSON API response
        Raises:
            MessageNotReceivedError: Raised if JSON API response has been received, but DPA response has not been received
        """
        status = Common.status_from_json(json)
        msgid = Common.msgid_from_json(json)
        if status < dpa_constants.ResponseCodes.OK:
            raise MessageNotReceivedError('Response message not received.', msgid=msgid)
