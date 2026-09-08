# Slice 02 — Evaluation Component

## Responsibility
Compute calibration, discrimination, and cost-weighted risk metrics on predicted probabilities against true CI outcomes, strictly independent of any model or feature pipeline.

## Reads
Ground-truth binary labels ($y_{\text{true}}$), predicted probabilities ($p_{\text{pred}} \in [0.0, 1.0]$), optional decision outputs, and the cost table from Slice 01.

## Emits
A structured evaluation dictionary containing:
- Discrimination: Accuracy, ROC AUC, Precision, Recall at threshold
- Calibration: Brier Score, Expected Calibration Error (ECE with selectable binning: equal-width vs equal-frequency)
- Decision quality: Cost-weighted expected risk, coverage, and risk–coverage under abstention

## Refuses
Refuses evaluation if input arrays have mismatched lengths, if probabilities fall outside $[0.0, 1.0]$, or if true labels are non-binary.

## Constraint
Must never import or depend on any model class, training pipeline, or feature extractor.

## Connects to
Reads the external contract and cost definitions from Slice 01; evaluates all downstream observers (Slices 07, 08, 09) and fusion arbiters (Slice 11).
