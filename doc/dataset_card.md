# Dataset Card: MIT-BIH Kaggle ECG Dataset

- Source: Kaggle
- Slug: `mondejar/mitbih-database`
- Local path: `data/raw/`

## Leakage Risks

- Duplicate or near-duplicate beats across splits
- Patient or record overlap across train/test partitions
- Preprocessing fitted on test data