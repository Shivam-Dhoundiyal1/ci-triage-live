# Phase 02 — How Would We Know This Is Any Good?

| Was | Now | Statement | Evidence |
|---|---|---|---|
| unknown | known | A constant-negative predictor scores >94% accuracy while achieving 0.0 recall on a ~3.2% flakiness dataset | tests/test_metrics.py |
| unknown | known | Equal-width ECE hides miscalibration on rare classes due to bin-zero pooling; equal-frequency ECE exposes the error across quantiles | tests/test_metrics.py |
| unknown | known | The evaluation component is strictly decoupled from model objects to ensure baselines, heuristics, and ML models are judged on identical terms | design/02-measurement.md |
| unknown | known | Artificial class balancing (SMOTE / oversampling) is rejected because it distorts base rate calibration (the scale trap) | ai-ledger/02-measurement.md |
| unknown | known-unknown | The empirical calibration and ROC AUC achieved by the first baseline model on historical CI logs | — |
| unknown | known-unknown | The optimal confidence threshold for abstaining to achieve minimum cost-weighted risk | — |
