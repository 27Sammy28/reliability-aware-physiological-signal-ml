import numpy as np
from src.metrics import confusion_counts
def confusion_matrix_array(y_true, y_prob):
    c=confusion_counts(y_true,y_prob); return np.asarray([[c["tn"], c["fp"]], [c["fn"], c["tp"]]])
