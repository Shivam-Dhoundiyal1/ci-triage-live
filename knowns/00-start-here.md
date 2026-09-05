# Phase 00 — The Decision at 2:47am

| Was | Now | Statement | Evidence |
|---|---|---|---|
| unknown | known | The decision at 02:47 is an operational choice (rerun, halt release, or quarantine test) made by an on-call engineer before 09:00 | PROBLEM.md |
| unknown | known | The cost of shipping a defect (~20h) is roughly 5x the cost of an unnecessary release halt (~4h) | PROBLEM.md |
| unknown | known | The system boundary strictly forbids auto-merging code, modifying/emitting code, or muting/deleting tests | design/00-start-here.md |
| unknown | known | When prior data or failure evidence is insufficient, the system must abstain and ask for human review | design/00-start-here.md |
| unknown | known-unknown | Empirical base rate of flakiness versus real code defects in this repository's test suite | — |
