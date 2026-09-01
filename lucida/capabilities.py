"""Pure, host-agnostic capability facades for the LUCIDA surface."""

from __future__ import annotations

from typing import Any

from adapters.vj.contracts import VJEvent, VJProposal, VJState

from .contracts import CapabilityReport


class _BaseCapability:
    name = ""
    phases: tuple[str, ...] = ()
    operation = ""
    risk = "low"
    expected = ""

    def supports(self, event: VJEvent) -> bool:
        return event.phase in self.phases

    def evaluate(self, event: VJEvent, state: VJState) -> CapabilityReport:
        if not self.supports(event):
            return CapabilityReport(
                capability=self.name,
                observed=(f"Sin evento dirigido a {self.name} en esta transición.",),
                state={"status": "idle", "last_phase": state.phase},
                expected_results=(),
                unknowns=(f"No hay evidencia de {self.name} para este evento.",),
            )

        payload = event.payload
        proposal = VJProposal(
            proposal_id=f"lucida-{self.name.lower()}-{event.event_id}",
            event_id=event.event_id,
            phase=event.phase,
            operation=self.operation,
            reason=self._reason(event),
            risk=self.risk,
            evidence=("lucida", self.name.lower(), "offline-observation"),
        )
        return CapabilityReport(
            capability=self.name,
            observed=self._observed(event),
            state={"status": "observed", "phase": event.phase, **self._state(payload)},
            proposals=(proposal,),
            expected_results=(self.expected,),
            unknowns=self._unknowns(),
        )

    def _observed(self, event: VJEvent) -> tuple[str, ...]:
        return (f"{self.name} observó {event.event_type} en fase {event.phase}.",)

    def _reason(self, event: VJEvent) -> str:
        return f"Sugerir una revisión de {self.name} basada en el evento {event.event_id}."

    def _state(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"payload_status": payload.get("status", "unknown")}

    def _unknowns(self) -> tuple[str, ...]:
        return ("La aplicación host y el hardware externo no están conectados en modo offline.",)


class InstarCapability(_BaseCapability):
    """Preflight de medios, formato y preparación de superficies."""

    name = "INSTAR"
    phases = ("preflight",)
    operation = "review-media-and-mapping"
    expected = "El operador confirma medios, proporciones y mapping antes de continuar."

    def _state(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "media_status": payload.get("media_status", payload.get("status", "unknown")),
            "mapping_status": payload.get("mapping_status", "unknown"),
        }


class NayadeCapability(_BaseCapability):
    """Soundcheck de señal, procesador y coexistencia de superficies."""

    name = "NAYADE"
    phases = ("preparation",)
    operation = "review-soundcheck-signal"
    risk = "medium"
    expected = "El operador confirma señal, geometría y color sin escribir en el procesador."

    def _state(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "signal_status": payload.get("signal_status", payload.get("status", "unknown")),
            "processor_status": payload.get("processor_status", "unknown"),
        }


class ImagoCapability(_BaseCapability):
    """Observación del show, incidentes y recuperación en vivo."""

    name = "IMAGO"
    phases = ("show", "incident", "recovery", "closure")
    operation = "review-live-visual-state"
    expected = "El operador confirma la propuesta o registra el resultado observado."

    def _state(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "show_mode": payload.get("mode", "unknown"),
            "incident_category": payload.get("category", "none"),
        }
