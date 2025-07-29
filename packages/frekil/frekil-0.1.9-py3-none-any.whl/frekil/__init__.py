"""
Frekil SDK for Python
"""

from .client import FrekilClient
from .api.allocations import AllocationsAPI

__version__ = "0.1.0"

__all__ = ["FrekilClient", "AllocationsAPI"]
