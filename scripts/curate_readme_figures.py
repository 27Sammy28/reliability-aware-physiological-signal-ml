"""Copy selected generated figures into docs/assets for README display."""

from __future__ import annotations

from pathlib import Path
import shutil

FIGURES = [
    "class_distribution.png",
    "representative_waveforms.png",
    "reliability_diagram.png",
    "robustness_ece_curve.png",
]


def main() -> None:
    source_dir = Path("results/figures")
    target_dir = Path("docs/assets")
    target_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for name in FIGURES:
        source = source_dir / name
        if not source.exists():
            continue
        target = target_dir / name
        shutil.copy2(source, target)
        copied.append(target)
    if not copied:
        raise SystemExit("No generated figures found. Run `python scripts/generate_figures.py` first.")
    print("Copied curated figures:")
    for path in copied:
        print(f"- {path}")


if __name__ == "__main__":
    main()
