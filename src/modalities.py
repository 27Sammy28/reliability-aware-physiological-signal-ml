"""Health-signal modality definitions."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class HealthSignalModality:
    name: str
    signal_type: str
    example_features: tuple[str, ...]
    reliability_risks: tuple[str, ...]
SUPPORTED_MODALITIES = (
    HealthSignalModality("ECG", "physiological_time_series", ("heartbeat morphology", "RR intervals"), ("sensor noise", "missing segments", "device shift")),
    HealthSignalModality("voice", "acoustic_time_series", ("pitch", "jitter", "shimmer"), ("microphone mismatch", "background noise")),
    HealthSignalModality("speech_language", "acoustic_linguistic_sequence", ("pause rate", "lexical diversity"), ("task mismatch", "transcription errors")),
)
def modality_summary() -> list[dict[str, object]]:
    return [{"name": m.name, "signal_type": m.signal_type, "example_features": list(m.example_features), "reliability_risks": list(m.reliability_risks)} for m in SUPPORTED_MODALITIES]
