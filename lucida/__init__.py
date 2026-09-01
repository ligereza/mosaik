"""Single-surface LUCIDA integration for the VJ adapter."""

from .capabilities import ImagoCapability, InstarCapability, NayadeCapability
from .contracts import CapabilityReport, LucidaState
from .orchestrator import LucidaOrchestrator
from .overlay import (
    OverlayCursorError,
    OverlayDiffError,
    build_overlay_cursor,
    build_overlay_view,
    diff_overlay_view,
)

__all__ = [
    "CapabilityReport",
    "ImagoCapability",
    "InstarCapability",
    "LucidaOrchestrator",
    "LucidaState",
    "NayadeCapability",
    "OverlayCursorError",
    "OverlayDiffError",
    "build_overlay_cursor",
    "build_overlay_view",
    "diff_overlay_view",
]
