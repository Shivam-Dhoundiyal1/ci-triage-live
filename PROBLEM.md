# Problem Definition: CI Flakiness Triage at 02:47

## 1. The Decision
At 02:47, an on-call engineer faces a red build on the release branch. The release is scheduled for 09:00. The decision to make before 09:00 is:
* Whether to halt the release and wake up the author/team, rerun the test to observe repeatability, or quarantine the test and proceed with the release.

## 2. The Actions
The on-call engineer can only take three concrete actions:
1. **Rerun the test / pipeline:** Spend CI time and compute to check if the failure reproduces or passes.
2. **Halt the release:** Block the merge/deployment and wake up the commit author for an emergency fix.
3. **Quarantine / skip the test:** Bypass the test failure so the release can ship on time.

## 3. The Prediction
* **What the system estimates:** The system estimates the probability that a specific failure is caused by test flakiness versus a real code defect.
* **Why prediction != decision:** The prediction is a probabilistic diagnosis. The decision is an operational action that balances that diagnosis against remaining time before 09:00 and asymmetric business costs.

## 4. The Cost
The costs of triage mistakes are heavily asymmetric:
* **Shipping a defect (false alarm on flakiness):** ~20 engineer hours. A defect reaches production customers, damages trust, requires an emergency rollback, and subjects developers to high-pressure hotfixing that risks introducing cascading mistakes.
* **Unnecessarily halting the release (false alarm on defect):** ~4 engineer hours. Waking an engineer in the middle of the night, stalling the release pipeline, and burning engineering time investigating a false alarm.
