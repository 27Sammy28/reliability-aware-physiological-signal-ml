from src.experiment import ExperimentConfig, run_experiment
def run_noise_benchmark(noise_levels=(0.0,0.05,0.1,0.2,0.4), use_synthetic=True):
    return run_experiment(ExperimentConfig(use_synthetic=use_synthetic, noise_levels=tuple(noise_levels)))
