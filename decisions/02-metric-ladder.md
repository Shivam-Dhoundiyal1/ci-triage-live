# Decision 02 — The Metric Ladder, Calibration, and Evaluation

## 1. The Constant Model Baseline

Before evaluating any learned model or heuristic, we establish the baseline floor using a constant predictor that ignores all evidence and always predicts `0` (not flaky).

### Prediction & Hypothesis
On a test suite with ~3.2% flakiness base rate (32 flaky tests out of 1,000 runs):
- **Accuracy:** > 96% (in this dataset, ~96.8% or ~94.4%).
- **Recall:** Exactly 0.0 (catches zero flaky tests).

This confirms that reporting accuracy alone is deceptive: a model that learns nothing and helps no one achieves stellar accuracy simply by exploiting class imbalance.

---

## 2. The Metric Ladder

Each rung answers a distinct question for the on-call engineer at 02:47:

| Rung | Metric | Source | The Question It Answers at 02:47 |
|---|---|---|---|
| 1 | **Accuracy** | `sklearn.metrics` | What fraction of predictions matched? *(Baseline control only)* |
| 2 | **ROC AUC** | `sklearn.metrics` | Does the model rank flaky tests higher than real defects, regardless of threshold? |
| 3 | **Precision & Recall** | `sklearn.metrics` | At a specific decision threshold: when we flag flaky, how often are we right; and what fraction of all flakes did we catch? |
| 4 | **Brier Score** | `sklearn.metrics` | What is the overall mean squared error on predicted probabilities? |
| 5 | **Expected Calibration Error (ECE)** | Custom (`ci_triage/metrics.py`) | When the model says 80% probability, does it flip 80% of the time? *(Evaluated with selectable binning)* |
| 6 | **Cost-Weighted Risk** | Custom (`ci_triage/metrics.py`) | How many engineer hours does this triage policy waste on average per failure according to the Phase 01 cost table? |
| 7 | **Risk–Coverage** | Custom (`ci_triage/metrics.py`) | What is the expected cost-weighted risk as a function of the fraction of decisions the system answers versus abstaining? |

---

## 3. The Binning Trap in ECE

Expected Calibration Error groups predictions into $M$ bins and computes the weighted gap between average confidence and true positive rate:
$$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} |\text{acc}(B_m) - \text{conf}(B_m)|$$

When evaluating a CI dataset with ~3% base rate:
1. **Equal-Width Bins:** Fixed intervals $[0.0, 0.1), [0.1, 0.2), \dots$. Nearly all predictions fall in bin 1 where predicted probabilities match the low base rate. The other 9 bins are virtually empty. The weighted average hides severe miscalibration in high-confidence predictions, reporting an artificially flattering low error (~0.029).
2. **Equal-Frequency (Equal-Mass) Bins:** Partitions predictions into quantiles such that every bin contains the same number of samples ($N/M$). This exposes miscalibration across all probability ranges (~0.115), preventing a single dominant zero-bin from drowning out errors.

**Decision:** Our ECE implementation must support selectable binning schemes (`equal_width` and `equal_frequency`), and production triage calibration must be validated using `equal_frequency`.

---

## 4. Cost-Weighted Risk and Coverage

Using the cost matrix elicited in Phase 01:
- Defect misclassified as Flaky (False Negative / bad release): **20.0 hours**
- Flaky misclassified as Defect (False Positive / unnecessary halt): **4.0 hours**
- Abstain (Manual on-call review): **1.0 hour**
- Correct classification: **0.0 hours**

$$\text{Risk}(\hat{y}, y) = \frac{1}{N} \sum_{i=1}^N \text{Cost}(\hat{y}_i, y_i)$$

Coverage is defined as:
$$\text{Coverage} = \frac{\text{Count}(\hat{y}_i \neq \text{ABSTAIN})}{N}$$
A triage system with low risk but 5% coverage has simply outsourced 95% of its job to the human on-call engineer at 02:47. Both risk and coverage must be reported together.
