## Review
1. slice fit   — Defines the external contract, mapping discrete diagnoses to operational actions and costs.
2. correctness — Real-world costs of CI failures are heavily asymmetric; accuracy cannot express this.
3. ML validity — Accuracy is flawed under high class imbalance and treats all errors as identical.
4. necessity   — Establishing cost-weighted risk is mandatory before measuring models in Slice 02.

## Proposed
Optimize the classifier to maximize standard classification accuracy across all test failure diagnoses.

## Rejected / narrowed to
Rejected accuracy entirely; narrowed the objective to minimizing expected cost-weighted risk with an explicit `ABSTAIN` (manual triage) output.

## Because
Accuracy treats decisions as binary right/wrong, ignoring that a false negative (defect leak costing ~20 hours) is 5x more damaging than a false positive (halted release costing ~4 hours), and cannot price the value of abstention under thin evidence (~1 hour).

## Ponytail pass
None (no code in Phase 01).
