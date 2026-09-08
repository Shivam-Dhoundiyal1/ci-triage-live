# Phase 01 — The Output Space and What a Mistake Costs

| Was | Now | Statement | Evidence |
|---|---|---|---|
| unknown | known | The external contract defines four outputs paired with concrete actions: DEFECT->HALT, FLAKY->QUARANTINE, INFRA->RERUN, ABSTAIN->MANUAL_REVIEW | design/01-decision-and-cost.md |
| unknown | known | The triage error costs are asymmetric (~20h for missed defect vs ~4h for false halt) and abstaining costs ~1.0h of engineer time | decisions/01-output-space.md |
| unknown | known | Standard classification accuracy is rejected as an evaluation objective because it treats errors as binary right/wrong and ignores asymmetric costs | ai-ledger/01-decision-and-cost.md |
| unknown | known | The system objective is minimising expected cost-weighted risk | decisions/01-output-space.md |
| unknown | known-unknown | The exact probability threshold at which the expected cost of taking action exceeds the cost of abstaining | — |
| unknown | known-unknown | The empirical prevalence of infra failures compared to test flakiness in the historical logs | — |
