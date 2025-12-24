"""
Routes package for the Dark Souls API
"""

from .characters import router as characters_router
from .combat import router as combat_router
from .health import router as health_router

__all__ = ["characters_router", "combat_router", "health_router"]
