"""Eeeprom peripheral request messages."""

from .read import ReadRequest
from .write import WriteRequest

__all__ = (
    'ReadRequest',
    'WriteRequest',
)
