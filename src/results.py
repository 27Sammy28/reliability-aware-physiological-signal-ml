"""Result summarization and reliability report generation."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

LOWER_IS_BETTER = {"brier", "ece", "prediction_entropy"}


def select_baseline_row(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the clean baseline row when available."""
    if not rows:
        return {}
    return next(
        (
            row
            for row in rows
            if float(row.get("noise_level", 0.0)) == 0.0
            and float(row.get("missing_rate", 0.0)) == 0.0
            and float(row.get("segment_fraction", 0.0)) == 0.0
        ),
        rows[0],
    )


def select_worst_row(rows: list[dict[str, object]], metric: str = "ece") -> dict[str, object]:
    """Select the row with worst metric value."""
    if not rows:
        return {}
    reverse = metric not in LOWER_IS_BETTER
    return sorted(rows, key=lambda row: float(row.get(metric, 0.0)), reverse=reverse)[-1 if reverse else -1]


def metric_snapshot(row: dict[str, object]) -> dict[str, object]:
    """Extract key metrics for compact reporting."""
    keys = (
        "accuracy",
        "balanced_accuracy",
        "precision",
        "recall",
        "specificity",
        "f1",
        "brier",
        "ece",
        "calibration_slope",
        "prediction_entropy",
        "confidence_margin",
    )
    return {key: row[key] for key in keys if key in row}


def write_reliability_report(
    rows: list[dict[str, object]],
    output_path: str | Path,
    figure_paths: list[str | Path] | None = None,
    title: str = "Reliability Report",
) -> Path:
    """Write a Markdown report summarizing metric and figure outputs."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    baseline = select_baseline_row(rows)
    worst_ece = select_worst_row(rows, metric="ece")
    worst_accuracy = min(rows, key=lambda row: float(row.get("accuracy", 0.0))) if rows else {}
    figure_paths = figure_paths or []

    lines = [
        f"# {title}",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "## Summary",
        "",
        f"- Rows evaluated: {len(rows)}",
        f"- Baseline condition: noise={baseline.get('noise_level', 'NA')}, missing={baseline.get('missing_rate', 'NA')}, segment={baseline.get('segment_fraction', 'NA')}",
        f"- Worst ECE condition: noise={worst_ece.get('noise_level', 'NA')}, missing={worst_ece.get('missing_rate', 'NA')}, segment={worst_ece.get('segment_fraction', 'NA')}",
        f"- Lowest accuracy condition: noise={worst_accuracy.get('noise_level', 'NA')}, missing={worst_accuracy.get('missing_rate', 'NA')}, segment={worst_accuracy.get('segment_fraction', 'NA')}",
        "",
        "## Baseline Metrics",
        "",
    ]
    for key, value in metric_snapshot(baseline).items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Worst Calibration Metrics", ""])
    for key, value in metric_snapshot(worst_ece).items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Confusion Counts at Baseline", ""])
    for key in ("tp", "tn", "fp", "fn"):
        if key in baseline:
            lines.append(f"- {key}: {baseline[key]}")

    if figure_paths:
        lines.extend(["", "## Figures", ""])
        for path in figure_paths:
            path = Path(path)
            lines.append(f"- {path.name}: `{path}`")

    lines.extend(
        [
            "",
            "## Interpretation Notes",
            "",
            "- Accuracy and F1-score describe discrimination, but not probability reliability.",
            "- Brier score and ECE summarize probabilistic reliability under clean and corrupted signals.",
            "- Calibration slope and entropy help identify overconfidence or unstable confidence under perturbation.",
            "- This report is for research benchmarking only and is not a clinical diagnostic claim.",
        ]
    )
    output.write_text("\n".join(lines) + "\n")
    return output
