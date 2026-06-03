"""Classical logistic regression baseline."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

def sigmoid(values: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-np.clip(values, -40, 40)))

@dataclass
class LogisticRegressionGD:
    learning_rate: float = 0.08
    epochs: int = 350
    l2: float = 0.001
    def fit(self, x_train: np.ndarray, y_train: np.ndarray) -> "LogisticRegressionGD":
        x_train = np.asarray(x_train, dtype=float); y_train = np.asarray(y_train, dtype=float)
        self.mean_ = np.mean(x_train, axis=0); std = np.std(x_train, axis=0); self.std_ = np.where(std == 0, 1, std)
        x_scaled = (x_train - self.mean_) / self.std_; self.weights_ = np.zeros(x_scaled.shape[1]); self.bias_ = 0.0
        for _ in range(self.epochs):
            prob = sigmoid(x_scaled @ self.weights_ + self.bias_); error = prob - y_train
            self.weights_ -= self.learning_rate * ((x_scaled.T @ error) / len(y_train) + self.l2 * self.weights_)
            self.bias_ -= self.learning_rate * float(np.mean(error))
        return self
    def predict_proba(self, x_test: np.ndarray) -> np.ndarray:
        x_scaled = (np.asarray(x_test, dtype=float) - self.mean_) / self.std_; positive = sigmoid(x_scaled @ self.weights_ + self.bias_)
        return np.column_stack([1 - positive, positive])
