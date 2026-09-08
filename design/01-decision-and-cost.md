# Slice 01 — External Contract

## Responsibility
Emit diagnostic triage labels paired with operational action recommendations, or refuse by abstaining when evidence is insufficient.

## Reads
Triage evidence and calibrated failure probabilities across candidate causes (defect, flaky, infra).

## Emits
A structured diagnosis with an operational action recommendation:
- `DEFECT` -> `HALT`
- `FLAKY` -> `QUARANTINE`
- `INFRA` -> `RERUN`
- `ABSTAIN` -> `MANUAL_REVIEW`
accompanied by expected cost.

## Refuses
Emits `ABSTAIN -> MANUAL_REVIEW` whenever evidence is thin, missing, or confidence falls below the cost-optimal decision threshold.

## Constraint
Every emitted diagnosis must be paired with its explicit operational action recommendation, and `ABSTAIN` must always trigger human on-call review.

## Connects to
Consumes diagnosis signals from Slice 00 (System Boundary) and feeds downstream into Slice 02 (Evaluation Component & Cost Risk Metrics).
