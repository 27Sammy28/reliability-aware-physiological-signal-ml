from pathlib import Path
from src.data import synthetic_ecg_dataset
from src.figures import plot_class_distribution, plot_representative_waveforms
def generate_core_publication_figures(output_dir="results/figures"):
    output_dir=Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True); x,y=synthetic_ecg_dataset(); return [plot_class_distribution(y, output_dir/"class_distribution.png"), plot_representative_waveforms(x,y,output_dir/"representative_waveforms.png")]
