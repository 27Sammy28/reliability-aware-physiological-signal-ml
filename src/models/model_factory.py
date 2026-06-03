"""Model factory."""
from src.models.logistic_regression import LogisticRegressionGD

def create_model(name: str = "logistic_regression_gd"):
    normalized = name.lower().strip()
    if normalized in {"logistic", "logistic_regression", "logistic_regression_gd"}:
        return LogisticRegressionGD()
    raise ValueError(f"Unknown or unavailable model: {name}")
