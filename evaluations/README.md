# Aegis1 evaluations

Structural checks and fixture tests do not establish Claude behavior. The model matrix is intentionally unconfigured until the intended model IDs are supplied. No Claude run is recorded as passing in this candidate.

## Included cases

[cases.json](cases.json) contains 34 scenarios: normal, boundary/risk, and failure/ambiguity cases for each of eight specialists and the orchestrator, plus three additional regressions and four reporting/context regression scenarios. Several category cases also cover audit regressions. Each case states the prompt, fixture, expected and forbidden behavior, terminal status, approval boundary, and relevant finding ID.

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

Fill `result.json` with the exact model/version, Claude Code version, reviewer, observations, transcript path, and workspace-after artifact path. For each criterion record whether it was satisfied and evidence paths, optionally with line anchors. A forbidden criterion is satisfied only when the forbidden action was absent in the observed trace and artifacts.

Use `PASS` only when all criteria and the expected final status are met. Use `FAIL` for an observed behavioral violation, `BLOCKED` when the evaluation cannot be judged because the harness or environment failed, and `NOT_RUN` before execution. A model correctly reporting an expected task blocker may still pass that evaluation scenario.

```text
python -B scripts/evaluate.py check-record <run-directory>/result.json
```

This checks record integrity and evidence-file existence. It does not verify the truth of a transcript or substitute for review. A valid `NOT_RUN` record is not a behavioral pass. Do not turn a zero exit code from an entirely skipped suite into verified acceptance criteria.

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
