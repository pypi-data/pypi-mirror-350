# BONSAI: Globally Optimized Shallow Decision Trees via Efficient Search and Modeling

This repository contains the implementation and experiments for the BONSAI algorithm, introduced in our NeurIPS 2025 paper:  
**"BONSAI: Globally Optimized Shallow Decision Trees via Efficient Search and Modeling"**.

BONSAI is an optimization-based decision tree algorithm that supports both numerical and categorical features, enables multi-way splits, and produces compact, interpretable trees under depth constraints.

## 🔗 Paper
You can find the full paper [TBD] (update with actual link if needed).

## 🧠 Key Features
- Supports **multi-way splits** on numerical features.
- Handles **categorical features natively** (no need for one-hot encoding).
- Employs a **slot-node framework** to reduce search space.
- Uses a **MIP formulation** to optimize accuracy and interpretability jointly.
- Scalable to medium-sized datasets via threshold sampling and pruning.

## 📦 Installation

BONSAI is distributed as a Python package. To install:

```bash
pip install bonsai-ml
```

For a detailed walkthrough of the repository, including how to run the
examples and tests, see [FIRST_TIME_USERS.md](FIRST_TIME_USERS.md).

