## Review
1. slice fit   — Created a standalone evaluation component independent of any model class or feature representation.
2. correctness — Implements the full 7-rung metric ladder with asymmetric cost-weighting from Phase 01.
3. ML validity — Exposes the equal-width binning trap; ensures calibration is measured without distortion.
4. necessity   — Standard instruments must exist before running experiments on real CI data.

## Proposed
Oversample the minority class (e.g. using synthetic data or SMOTE) to force a 50/50 balance so standard accuracy and precision/recall become easier to optimize.

## Rejected / narrowed to
Rejected artificial rebalancing; preserved the natural ~3% empirical base rate and evaluated using cost-weighted risk and equal-frequency ECE.

## Because
This is the scale trap: the loudest in the class is not always the correct one. Artificially rebalancing changes the base rate the system observes, which severely distorts probability calibration and breaks the cost-weighted risk calculations in real deployment at 02:47.

## Ponytail pass
Delegated standard metrics (accuracy, ROC AUC, precision, recall, Brier score) to `sklearn.metrics`. Implemented only custom calibration (with selectable binning) and cost-weighted risk/coverage, keeping `ci_triage/metrics.py` to exactly 80 lines.
