# Reliable Manifold Learning for Health Signals

## Learning Robust Physiological Signal Representations Under Noise and Distribution Shift

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Unsupervised-green)
![Signal Processing](https://img.shields.io/badge/Signal%20Processing-Health-orange)
![Research](https://img.shields.io/badge/Research-Reproducible-red)

---

## Overview

Physiological signals contain complex latent structures that are often hidden within high-dimensional observations.

Traditional supervised learning approaches focus on prediction accuracy, but provide limited insight into the intrinsic organization of physiological signal populations.

This repository investigates representation learning and manifold discovery in physiological signals using modern dimensionality reduction and clustering techniques.

The project studies how latent signal representations evolve under noise, corruption, and distribution shift, with a particular focus on representation reliability.

---

## Research Motivation

Many healthcare machine learning systems assume that learned representations remain stable when signal quality deteriorates.

In practice, physiological measurements frequently contain:

* sensor noise
* motion artifacts
* missing observations
* acquisition variability
* cohort shift

These factors may distort latent signal structure and compromise downstream decision-making.

This project investigates whether physiological signal embeddings remain meaningful under realistic observational uncertainty.

---

## Research Questions

### RQ1

Can unsupervised representation learning reveal meaningful physiological signal structure?

### RQ2

How do PCA, UMAP, and t-SNE compare for health signal manifold discovery?

### RQ3

How stable are learned embeddings under progressively noisy signal conditions?

### RQ4

Can representation drift serve as an indicator of signal reliability?

---

## Methodology

### Representation Learning

The framework compares:

* Principal Component Analysis (PCA)
* Uniform Manifold Approximation and Projection (UMAP)
* t-Distributed Stochastic Neighbor Embedding (t-SNE)

### Clustering

Discovered manifolds are evaluated using:

* K-Means
* DBSCAN
* HDBSCAN

### Reliability Analysis

Embedding robustness is assessed through:

* Gaussian noise injection
* Temporal masking
* Missingness simulation
* Distribution shift experiments

---

## Experimental Pipeline

Raw ECG Signals
↓
Preprocessing
↓
Feature Extraction
↓
Representation Learning
(PCA / UMAP / t-SNE)
↓
Clustering Analysis
↓
Noise Injection
↓
Embedding Drift Analysis
↓
Representation Reliability Evaluation

---

## Repository Structure

```text
reliable-manifold-learning-for-health-signals/

├── data/
├── notebooks/
├── src/
│   ├── preprocessing/
│   ├── embeddings/
│   ├── clustering/
│   ├── robustness/
│   ├── evaluation/
│   └── visualization/
│
├── experiments/
├── results/
├── figures/
├── docs/
└── tests/
```

---

## Evaluation Metrics

### Embedding Quality

* Trustworthiness
* Continuity
* Silhouette Score
* Davies-Bouldin Index

### Reliability Metrics

* Embedding Drift Distance
* Cluster Stability
* Neighborhood Preservation
* Robustness Under Noise

---

## Expected Outputs

### UMAP Projection

Visualizing latent physiological structure.

### Cluster Discovery

Identification of naturally emerging signal groups.

### Embedding Drift Curves

Quantifying representation degradation as noise increases.

### Reliability Maps

Characterizing stable and unstable regions of the latent manifold.

---

## Scientific Contributions

This project explores:

* unsupervised physiological signal learning
* manifold analysis
* representation robustness
* trustworthy machine learning
* reliability-aware health AI

rather than conventional classification-focused benchmarking.



## Results

### Dataset

Experiments were conducted using the Kaggle MIT-BIH heartbeat dataset derived from the MIT-BIH Arrhythmia Database.

| Property         | Value                 |
| ---------------- | --------------------- |
| Training Samples | 87,554                |
| Test Samples     | 21,892                |
| Features         | 188                   |
| Task             | Binary Classification |
| Normal Class     | Label 0               |
| Arrhythmia Class | Labels 1–4            |

For the binary classification setting, normal beats were treated as the negative class, while all arrhythmia categories were grouped into a single positive class.

Models were trained on a stratified subset of 12,000 training samples and evaluated on the full held-out test set.

---

### Model Performance

| Model                  | Accuracy  | F1 Score  | AUROC     | AUPRC     | ECE   |
| ---------------------- | --------- | --------- | --------- | --------- | ----- |
| Logistic Regression    | 0.902     | 0.651     | 0.859     | 0.726     | 0.026 |
| Linear SVM             | 0.872     | 0.625     | 0.852     | 0.675     | 0.201 |
| Decision Tree          | 0.932     | 0.783     | 0.910     | 0.848     | 0.005 |
| Random Forest          | **0.938** | **0.784** | **0.945** | **0.890** | 0.059 |
| Gradient Boosted Trees | 0.828     | 0.000     | 0.834     | 0.527     | 0.112 |

---

### Calibration Analysis

Calibration quality varied substantially across models.

| Model                  | Expected Calibration Error (ECE) |
| ---------------------- | -------------------------------- |
| Decision Tree          | **0.005**                        |
| Logistic Regression    | 0.026                            |
| Random Forest          | 0.059                            |
| Gradient Boosted Trees | 0.112                            |
| Linear SVM             | 0.201                            |

Although Random Forest achieved the strongest overall predictive performance, Decision Trees produced the most reliable probability estimates according to Expected Calibration Error.

---

### Key Findings

* Random Forest achieved the highest overall classification performance.
* Decision Trees demonstrated exceptionally strong calibration quality.
* Logistic Regression remained competitive despite its simplicity.
* Linear SVM exhibited substantial calibration degradation.
* Model reliability cannot be assessed using accuracy alone.
* Calibration-aware evaluation provides additional insights beyond conventional performance metrics.

---

### Implications

These findings support the central hypothesis of this repository:

> Reliable physiological signal inference requires evaluating both predictive performance and probability quality.

Models with strong accuracy may still produce poorly calibrated confidence estimates, highlighting the importance of reliability-aware evaluation in healthcare machine learning systems.

---

## Long-Term Research Vision

The broader goal is to develop reliable machine learning systems for extracting actionable information from noisy observational signals.

Future extensions include:

* ECG signals
* respiratory audio
* cough signals
* speech biomarkers
* multimodal health sensing

with applications in healthcare monitoring and public-health surveillance.

---

## Author

Samuel Worku

Research Interests:

* Representation Learning
* Trustworthy AI
* Physiological Signal Processing
* Scientific Machine Learning
* Robust and Reliable Inference
