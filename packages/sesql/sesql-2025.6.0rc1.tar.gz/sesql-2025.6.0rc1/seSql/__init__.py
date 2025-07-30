"""
Module initialization file that exports database connectivity and utility functions.
"""
from .__about__ import __version__ as version
from .sql import sql
from .dbc.Utilities import (
    mask,
    get_host_ip,
    get_hostname,
)

# Public API
PUBLIC_API = [
    'sql',
    'mask',
    'version',
    'get_host_ip',
    'get_hostname',
]

__version__ = version
__all__ = PUBLIC_API
