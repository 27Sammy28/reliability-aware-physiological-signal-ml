import numpy as np
def bootstrap_mean_ci(values, n_bootstrap: int = 200, confidence: float = 0.95, seed: int = 42):
    values=np.asarray(values,dtype=float); rng=np.random.default_rng(seed); means=[float(np.mean(rng.choice(values,size=len(values),replace=True))) for _ in range(n_bootstrap)]; alpha=(1-confidence)/2; return {"mean": float(np.mean(values)), "lower": float(np.quantile(means, alpha)), "upper": float(np.quantile(means, 1-alpha))}
