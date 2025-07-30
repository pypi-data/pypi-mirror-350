r"""
ARDHI Framework: A foundational system designed to streamline land and property workflows,
enabling modular, secure, and auditable transactions in geospatial and administrative systems.
"""


__title__ = 'Ardhi framework'
__version__ = '0.1.1'
__author__ = 'kioko@geopro'
__license__ = 'MIT'
__copyright__ = 'Copyright 2025 Konza Silicone ltd'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'


class RemovedIn03Warning(PendingDeprecationWarning):
    """
    No longer used, but kept around for backwards compatibility.
    """
    pass
