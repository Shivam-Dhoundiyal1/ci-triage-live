# Decision 01 — Output Space, Cost Table, and Objective

## 1. Derivation of the Output Space

### The Three Initial Outputs
Starting from the three physical causes of a test failure:
1. `DEFECT` -> `HALT`: Code change broke the build; stop the release and page the author.
2. `FLAKY` -> `QUARANTINE`: Test is non-deterministic; isolate the test and proceed with the release.
3. `INFRA` -> `RERUN`: Execution runner/network failed; retry execution.

### The Case That Forces a Fourth Output
Consider a test failure at 02:47 where:
- The failing test was added in this exact commit (no historical run data).
- The log was truncated or contains an uninformative exit code (e.g. exit 1 without stack trace).
- The repository has never been indexed or seen by the triage system before.

If forced to choose among `{DEFECT, FLAKY, INFRA}`, the system must make a blind guess. A wrong guess produces severe real-world consequences:
- Guessing `FLAKY` risks shipping a broken build to production customers.
- Guessing `DEFECT` wakes up an innocent developer at 03:00 and halts the release line.

### The Fourth Output: ABSTAIN
The system emits `ABSTAIN` paired with `MANUAL_REVIEW`.
- **Purpose:** Explicitly acknowledge that evidence is insufficient to make a safe probabilistic call.
- **Downstream Action:** The on-call engineer (already on shift) performs a manual inspection (checks fleet-wide failures, reviews git diff, inspects runner health) to decide the next operational step.

---

## 2. Cost Table

Unit of measurement: **Engineer Hours**

| True Cause | Emitted Output & Recommendation | What Happens | Who Pays | Cost (Hours) |
|---|---|---|---|---|
| `DEFECT` | `FLAKY` -> `QUARANTINE` | Defect passes into production at 09:00; customers discover bug; emergency rollback & hotfix. | Customers, On-call, Release team | ~20.0 |
| `DEFECT` | `INFRA` -> `RERUN` | Test rerun delays discovery; if timing masks bug, defect might ship; otherwise burns compute & 30m delay. | On-call, Release pipeline | ~2.0 |
| `FLAKY` | `DEFECT` -> `HALT` | Release halted; author woken up at 03:00 to investigate ghost failure. | Commit author, Release team | ~4.0 |
| `FLAKY` | `INFRA` -> `RERUN` | Test rerun passes by luck, masking flakiness without quarantining; wastes CI cycle. | CI infrastructure, Release pipeline | ~0.5 |
| `INFRA` | `DEFECT` -> `HALT` | Release halted unnecessarily for transient runner/network hiccup; author paged. | Commit author, Release team | ~4.0 |
| `INFRA` | `FLAKY` -> `QUARANTINE` | Innocent test quarantined due to transient runner disk full/timeout; requires debugging to unquarantine later. | Test owners | ~1.5 |
| Any | `ABSTAIN` -> `MANUAL_REVIEW` | System refuses to guess; on-call engineer spends 1 hour investigating logs and fleet status before deciding. | On-call engineer | ~1.0 |
| `DEFECT` | `DEFECT` -> `HALT` | Correct call; defect caught before release. | — | 0.0 |
| `FLAKY` | `FLAKY` -> `QUARANTINE` | Correct call; flake isolated, release ships on time. | — | 0.0 |
| `INFRA` | `INFRA` -> `RERUN` | Correct call; job reruns and passes. | — | 0.0 |

### Properties of the Cost Table

1. **Heavily Asymmetric:**
   The cost of shipping a defect (~20 hours) is 5x more costly than an unnecessary release halt (~4 hours). The table is fundamentally asymmetric because external customer harm vastly outweighs internal developer inconvenience.

2. **ABSTAIN is Cheap, Not Free:**
   `ABSTAIN` costs ~1.0 engineer hour of the on-call engineer's attention. It is cheap compared to shipping a defect (20 hrs) or waking an author (4 hrs), but it is not free (0 hrs). If `ABSTAIN` were modeled as free, an optimizer would trivially abstain on every difficult prediction.

---

## 3. The Objective

**Objective:**
$$\text{Minimise } \mathbb{E}[\text{Cost}] = \sum_{y, \hat{y}} P(y, \hat{y}) \cdot \text{Cost}(y, \hat{y})$$

### Why Not Accuracy?
Standard classification accuracy treats decisions as binary right/wrong with equal penalties (treating a 20-hour defect leak identically to a 4-hour false alarm), completely ignores class imbalance (flakiness is a rare event), and provides no mechanism to value or govern `ABSTAIN`.
