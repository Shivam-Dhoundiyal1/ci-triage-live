import numpy as np
import pytest
from ci_triage.metrics import (
    accuracy,
    recall,
    precision,
    roc_auc,
    brier_score,
    expected_calibration_error,
    cost_weighted_risk,
    coverage,
)


def test_constant_predictor_is_accurate_and_useless():
    # 3.2% positive flakiness rate
    y = np.zeros(1000)
    y[:32] = 1
    pred = np.zeros(1000)

    # High accuracy, zero recall
    assert accuracy(y, pred) > 0.94
    assert recall(y, pred) == 0.0


def test_ece_binning_trap_on_skewed_data():
    # 3.2% positive flakiness rate (32 positives, 968 negatives out of 1000)
    n = 1000
    y = np.zeros(n)
    probs = np.zeros(n)

    # 900 samples fall in bin 0 [0.0, 0.1)
    # 30 positives in this group gives acc = 30/900 = 0.0333
    y[:30] = 1
    probs[:450] = 0.005
    probs[450:900] = 0.061  # Mean prob in bin 0 is ~0.033, masking miscalibration in equal-width!

    # Upper 100 samples have 2 positives, but model overconfidently predicts 0.30
    y[900:902] = 1
    probs[900:1000] = 0.30

    ew_ece = expected_calibration_error(y, probs, n_bins=10, scheme="equal_width")
    ef_ece = expected_calibration_error(y, probs, n_bins=10, scheme="equal_frequency")

    # Equal frequency binning exposes miscalibration that equal-width buries in the pooled zero bin
    assert ef_ece > ew_ece
    assert ew_ece < 0.04
    assert ef_ece > 0.08


def test_cost_weighted_risk_asymmetry():
    y_true = np.array([0, 1])  # 0: Defect, 1: Flaky

    # Defect misclassified as Flaky (costs 20.0)
    risk_false_flaky = cost_weighted_risk(np.array([0]), np.array([1]))
    assert risk_false_flaky == 20.0

    # Flaky misclassified as Defect (costs 4.0)
    risk_false_defect = cost_weighted_risk(np.array([1]), np.array([0]))
    assert risk_false_defect == 4.0

    # Abstain costs 1.0
    risk_abstain = cost_weighted_risk(y_true, np.array([-1, -1]))
    assert risk_abstain == 1.0


def test_coverage_metric():
    preds = np.array([1, 0, -1, 1, -1])  # 3 answered, 2 abstained
    assert coverage(preds, abstain_val=-1) == 0.6
