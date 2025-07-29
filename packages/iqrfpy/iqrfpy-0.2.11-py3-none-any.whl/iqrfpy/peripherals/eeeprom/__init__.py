"""Eeeprom peripheral request and response messages."""

from . import requests
from . import responses

from .requests import ReadRequest, WriteRequest
from .responses import ReadResponse, WriteResponse

__all__ = (
    'ReadRequest',
    'ReadResponse',
    'WriteRequest',
    'WriteResponse',
)
