"""Generic request and response messages.

The purpose of the generic request is to allow for a construction of any existing request,
but also custom requests for user peripherals.
"""

from . import requests
from . import responses

from .requests import GenericRequest
from .responses import GenericResponse

__all__ = (
    'GenericRequest',
    'GenericResponse',
)
