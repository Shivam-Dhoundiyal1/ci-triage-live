# Slice 00 — System Boundary

## Responsibility
Diagnose whether a red CI build failure is flaky or a real defect to assist the on-call engineer's release decision.

## Reads
CI build logs, past history of CI failures, and commit diff.

## Emits
Triage diagnosis (flaky vs. real defect) with supporting evidence, or an explicit ABSTAIN.

## Refuses
Abstains and requests human manual review when prior test run data or failure evidence is insufficient to make a decision.

## Constraint
Must never merge code, must never modify or emit code changes/patches, and must never mute or delete tests.

## Connects to
Reads from the CI runner and git repository; emits triage output directly to the on-call engineer at 02:47; connects downstream to Slice 01 (external contract).
