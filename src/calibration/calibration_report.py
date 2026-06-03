from src.metrics import reliability_metrics
def calibration_report(y_true, y_prob, n_bins: int = 10):
    return reliability_metrics(y_true, y_prob, n_bins=n_bins)
