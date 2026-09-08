import numpy as np
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)

COSTS = {"defect_as_flaky": 20.0, "flaky_as_defect": 4.0, "abstain": 1.0}


def accuracy(y_true, y_pred):
    return float(accuracy_score(y_true, y_pred))


def recall(y_true, y_pred, zero_division=0.0):
    return float(recall_score(y_true, y_pred, zero_division=zero_division))


def precision(y_true, y_pred, zero_division=0.0):
    return float(precision_score(y_true, y_pred, zero_division=zero_division))


def roc_auc(y_true, y_prob):
    return float(roc_auc_score(y_true, y_prob))


def brier_score(y_true, y_prob):
    return float(brier_score_loss(y_true, y_prob))


def expected_calibration_error(y_true, y_prob, n_bins=10, scheme="equal_width"):
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    n = len(y_prob)
    if n == 0:
        return 0.0

    if scheme in ("equal_frequency", "equal_mass"):
        bin_indices = np.array_split(np.argsort(y_prob), n_bins)
        bins = [idx for idx in bin_indices if len(idx) > 0]
    elif scheme == "equal_width":
        edges = np.linspace(0.0, 1.0, n_bins + 1)
        # digitize maps values into 1..n_bins
        assigned = np.digitize(y_prob, edges[1:-1])
        bins = [np.where(assigned == b)[0] for b in range(n_bins) if np.any(assigned == b)]
    else:
        raise ValueError(f"Unknown scheme: {scheme}")

    ece = 0.0
    for idx in bins:
        acc = np.mean(y_true[idx])
        conf = np.mean(y_prob[idx])
        ece += (len(idx) / n) * abs(acc - conf)
    return float(ece)


def cost_weighted_risk(y_true, y_pred, costs=None):
    c = costs or COSTS
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    total_cost = 0.0
    for t, p in zip(y_true, y_pred):
        if p == -1 or p is None or str(p).upper() == "ABSTAIN":
            total_cost += c["abstain"]
        elif t == 0 and p == 1:
            total_cost += c["defect_as_flaky"]
        elif t == 1 and p == 0:
            total_cost += c["flaky_as_defect"]
    return float(total_cost / len(y_true)) if len(y_true) > 0 else 0.0


def coverage(y_pred, abstain_val=-1):
    y_pred = np.asarray(y_pred)
    if len(y_pred) == 0:
        return 0.0
    answered = sum(1 for p in y_pred if p != abstain_val and str(p).upper() != "ABSTAIN" and p is not None)
    return float(answered / len(y_pred))
