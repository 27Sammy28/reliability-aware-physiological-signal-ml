import numpy as np
def paired_difference_summary(a, b):
    diff=np.asarray(a,dtype=float)-np.asarray(b,dtype=float); return {"mean_difference": float(np.mean(diff)), "std_difference": float(np.std(diff)), "median_difference": float(np.median(diff))}
