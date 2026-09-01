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
from .overlay_consumer import (
    OverlayConsumer,
    OverlayConsumerConflictError,
    OverlayConsumerError,
    OverlayConsumerGapError,
    OverlayConsumerNotInitializedError,
    OverlayConsumerStaleError,
    OverlayConsumerState,
)
from .overlay_replay import (
    OverlayReplayError,
    replay_overlay_json,
    replay_overlay_path,
    replay_overlay_records,
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
    "OverlayConsumer",
    "OverlayConsumerConflictError",
    "OverlayConsumerError",
    "OverlayConsumerGapError",
    "OverlayConsumerNotInitializedError",
    "OverlayConsumerStaleError",
    "OverlayConsumerState",
    "OverlayReplayError",
    "replay_overlay_json",
    "replay_overlay_path",
    "replay_overlay_records",
]
