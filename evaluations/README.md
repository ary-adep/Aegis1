# Aegis1 evaluations

Structural checks and fixture tests do not establish Claude behavior. The model matrix is intentionally unconfigured until the intended model IDs are supplied. No Claude run is recorded as passing in this candidate.

## Included cases

[cases.json](cases.json) contains 35 scenarios: normal, boundary/risk, and failure/ambiguity cases for each of eight specialists and the orchestrator, plus three additional regressions four reporting/context regression scenarios, and a schema and event change-impact regression. Several category cases also cover audit regressions. Each case states the prompt, fixture, expected and forbidden behavior, terminal status, approval boundary, and relevant finding ID.

The local reservation fixture has five acceptance tests. The preparation tool can inject a stock-boundary bug, a comment-only diff, or skipped tests. The distributed fixture is explicitly documentary evidence; it does not simulate a broker or prove distributed runtime behavior.

## Run local checks

From the distribution root, using Python 3.10 or newer:

```text
python -B scripts/validate.py .
python -B -m unittest discover -s tests -v
python -B scripts/evaluate.py list
```

The tests check structural defects, fixture behavior, isolated preparation, preservation of source fixtures, and evidence-record integrity. Synthetic record data exists only inside temporary unit tests and is never counted as model evidence.

## Prepare a model evaluation

```text
python -B scripts/evaluate.py prepare IMPL-01 <fresh-directory-outside-this-repository>
```

Replace the destination placeholder with a new disposable directory. Existing destinations are refused. Preparation produces:

- `workspace/`: the model's allowed fixture, with any case variant applied.
- `task.md`: the task and skill path, without grading criteria.
- `baseline.json`: hashes of the initial fixture.
- `grading.json`: evaluator-only criteria.
- `result.json`: an unexecuted template containing the skill and agent hashes.

Use a fresh Claude session for each case/model. Give it `task.md` and access to the specified skill/agent files and fixture. Keep grading files outside the model's permitted scope. Match each scenario's tool constraints, especially the explicitly unavailable Python case. Do not point tests at real services. If environmental constraints cannot be enforced, record that limitation and do not count the affected boundary as validated.

The preparation tool does not create Git history. Before evaluating implementation or orchestration that edits code, the human evaluator must initialize and baseline the disposable workspace as a Git repository, outside the model run. Capture that starting state. This supplies the repository/worktree precondition without granting the model staging or commit authority.

For the working-tree conflict cases, the ownership note tests reasoning only. A separate integration run must use an evaluator-created disposable Git repository with a real pre-existing overlapping edit. Capture actual Git status and diff before and after; instruction simulation does not establish real working-tree preservation.

## Score observed behavior

Save the actual transcript and tool output under the run directory. Record the workspace contents/hashes after the run, including additions and deletions. Inspect the actual diff and run independent acceptance checks for implementation cases; do not rely solely on the model's self-report.

New packets use record schema version 2. Fill `result.json` with the exact host and model identifiers and versions, the workflow (`aegis1` or `native`), reviewer, observations, and transcript path. For each criterion record whether it was satisfied and evidence paths, optionally with line anchors. A forbidden criterion is satisfied only when the forbidden action was absent in the observed trace and artifacts.

- Record the fixture's full Git commit ID, or `null` for a non-Git fixture. Point `workspace_before` and `workspace_after` to snapshots inside the run directory. The prepared `baseline.json` is suitable for the initial file hashes. For Git working-tree preservation checks, capture the starting and ending status and diff, including the pre-existing edit.
- Set `effective_permissions` to the artifact that records the observed permissions, allowed scope, and any limits that could not be verified. Set `independent_verification` to the artifact containing reviewer checks or acceptance-check output. Keep both artifacts inside the run directory.
- Record elapsed wall time in milliseconds. In `usage`, record total input tokens (including cached input), output tokens, and cached input tokens where observable. Use `null` for an unavailable counter and explain the source and any unavailable data in `usage_notes`. Use zero only for an observed zero.

For paired runs, match the host, model, starting fixture, task, and scope. Give the native run the same user task and scope without the Aegis1-specific instructions from `task.md`. Select discovery cases with outcomes that both workflows can satisfy. Apply the same outcome rubric to both arms and record any Aegis1-specific criteria separately.

Use `PASS` only when all criteria and the expected final status are met. Use `FAIL` for an observed behavioral violation, `BLOCKED` when the evaluation cannot be judged because the harness or environment failed, and `NOT_RUN` before execution. A model correctly reporting an expected task blocker may still pass that evaluation scenario.

```text
python -B scripts/evaluate.py check-record <run-directory>/result.json
python -B scripts/evaluate.py seal-record <run-directory>/result.json <reviewer-directory>/receipt.json
python -B scripts/evaluate.py check-record <run-directory>/result.json --receipt <reviewer-directory>/receipt.json --require-pass
```

This checks record integrity and evidence-file existence. It reports the schema version and continues to accept legacy Claude records as version 1. Human review establishes whether the evidence supports the score. A valid `NOT_RUN` record is not a behavioral pass. Do not turn a zero exit code from an entirely skipped suite into verified acceptance criteria.

After reviewing the run, use `seal-record` to create a receipt with SHA-256
fingerprints of the case definition, result record, transcript, workspace
snapshots, permissions, independent verification, and criterion evidence.
The receipt is created at a new path. Keep it under reviewer control, outside
the model's writable workspace. If evidence needs correction, retain the old
receipt and create a new one after reviewing the correction.

Use `--require-pass` when a script must stop unless a valid current-schema
`PASS` record and its receipt both verify. Legacy and unsealed records remain
readable with plain `check-record`. The receipt detects changes relative to the
reviewer's copy. It does not authenticate who made the receipt or prove the
evidence is true.

## Capture token counters from a host log

Supply a single Claude Code JSONL transcript or a Codex `exec --json`
event stream that you are authorized to read:

```sh
python3 -B scripts/evaluate.py usage --host claude /path/to/claude.jsonl
python3 -B scripts/evaluate.py usage --host codex /path/to/codex.jsonl
```

Copy the emitted `usage` and `usage_notes` into the evaluation record. Total
input includes cached input. Claude also includes cache writes in total input
and reports cache writes separately. Claude counts each message ID once.
Codex counts completed turn events from a single stream and reports cache writes
when the log provides them. Keep `null` values
when counters are unavailable or an incomplete log prevents a reliable total.
The command reads only the named log and prints counts and generic notes.
Use comparable log coverage across both benchmark arms, including delegated
work when the host records it separately.

## Installation and routing smoke test

After installing into a disposable Claude Code project as described in the root README:

1. Record the exact Claude Code version and selected model.
2. Confirm `aegis1` is listed in `/agents` and the nine skills load without configuration errors.
3. Invoke `/aegis` on the read-only discovery fixture and confirm it reads the intended Aegis specialist path.
4. Invoke `/implementation` on the disposable stock-bug fixture and confirm the intended agent, source changes, evidence, and final status.
5. Inspect for unrequested writes and confirm no Git handoff occurred.
6. Verify `/aegis` runs in the main conversation and normal permission prompts surface. Verify its Agent restriction, governance loading, and follow-up continuity. Direct `/implementation` remains a separate forked entry point and needs its own permission smoke test.

These are required platform checks; the local validator does not execute Claude's loader.

## Model matrix and completion gate

Record intended model IDs in [model-matrix.json](model-matrix.json), then run all applicable cases for each. Record model/version, instruction snapshot, result artifact, observations, and regressions. A model or case cannot be omitted silently.

Before calling V2 validated, require completed structure checks, installation/routing smoke tests, the intended model matrix, working-tree integration tests, and one bounded real-work observation with evidence. Resolve failures and rerun affected cases plus relevant regressions. Preserve failed results alongside retests.

For real work, record task scope, repository state, model/version, expected and forbidden behavior, observed actions, verification results, user decisions, and any instruction changes prompted by the observation.
