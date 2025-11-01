"""Router package initialization."""

from .rabbis import router as rabbis_router
from .series import router as series_router

__all__ = ["rabbis_router", "series_router"]
