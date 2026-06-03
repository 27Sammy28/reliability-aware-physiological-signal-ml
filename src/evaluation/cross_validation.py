import numpy as np
def kfold_indices(n_samples: int, n_splits: int = 5, seed: int = 42):
    rng=np.random.default_rng(seed); idx=np.arange(n_samples); rng.shuffle(idx); folds=np.array_split(idx,n_splits); return [(np.concatenate([f for j,f in enumerate(folds) if j!=i]), folds[i]) for i in range(n_splits)]
