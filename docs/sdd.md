# Spec-driven development in Aegis1

SDD records connect an approved requirement to scope, implementation, and independent verification. Use this for bounded changes in an existing Git worktree with a HEAD commit. Keep review files in a separate folder. Codex and Claude Code can both use the Python CLI from the Aegis1 checkout.

## 1. Draft and approve

Create `spec.json` in the separate folder. For example:

```json
{
  "schema_version": 1,
  "id": "payment-migration-compatibility",
  "title": "Preserve old Payment inserts during schema rollout",
  "scope": ["payment-service/src/main/resources/db/migration/V2__payment_attempts.sql"],
  "requirements": [
    {"id": "REQ-1", "text": "The old Payment insert must work against the upgraded schema."}
  ],
  "criteria": [
    {"id": "AC-1", "requirement": "REQ-1", "check": "In disposable PostgreSQL, migrate a copy of the old schema and execute the old insert and duplicate delivery. Capture exit status and row counts."}
  ]
}
```

If the user explicitly approves editing a scoped path that already has local changes, list it in `allow_existing_changes`. Capture the approval before editing. The named approver is responsible for the scope and criteria.

```sh
python3 -B /path/to/Aegis1/skills/aegis/sdd.py validate spec.json
python3 -B /path/to/Aegis1/skills/aegis/sdd.py approve spec.json \
  --workspace /path/to/git-root --approval approval.json --by 'approver-name'
```

## 2. Implement and review

The agent runs `check-scope` before editing and again before review. It reports changed paths and a workspace fingerprint. Changes outside exact approved paths and changes to HEAD or the Git index fail the gate. The check compares tracked and non-ignored untracked files, including pre-existing changes. Keep the workspace still during approval and verification.

```sh
python3 -B /path/to/Aegis1/skills/aegis/sdd.py check-scope spec.json \
  --workspace /path/to/git-root --approval approval.json
```

A reviewer independent of the implementer evaluates the checks against the current workspace. Save the output of the checks under the review folder. Record the observed results in `review.json`:

```json
{
  "implemented_by": "implementation-agent",
  "reviewed_by": "independent-reviewer",
  "workspace_sha256": "<workspace_sha256 from check-scope>",
  "criteria": {
    "AC-1": {
      "result": "PASS",
      "observations": "Old insert succeeded and duplicate delivery preserved one payment.",
      "evidence": ["artifacts/compatibility.txt"]
    }
  }
}
```

The CLI requires a passing result with a nonempty evidence file for every criterion. A failed or unavailable check leaves the work gated. Keep a failed review as a record of what was observed.

## 3. Verify and check before handoff

```sh
python3 -B /path/to/Aegis1/skills/aegis/sdd.py verify spec.json \
  --workspace /path/to/git-root --approval approval.json \
  --review review.json --verification verification.json
python3 -B /path/to/Aegis1/skills/aegis/sdd.py check spec.json \
  --workspace /path/to/git-root --approval approval.json \
  --review review.json --verification verification.json
```

`check` exits nonzero unless the approved spec, worktree, review, and evidence still match the verification record. A changed spec requires a new approval and any changed verified work requires a new review. Record creation refuses to overwrite prior records. The CLI checks file state and record integrity. It relies on the host for permissions and on the reviewer for test execution and judgment. Approval and reviewer names are attestations. Use host access controls to protect those records if enforcing a separation of duties.

## Use project-owned checks

Describe how to verify each acceptance criterion in the spec. Reuse the
target project's existing checks when they cover the criterion. Run those
checks in the approved environment and attach their output to the review.
For a migration, that could be the project's compatibility probe in
disposable PostgreSQL. For an API change, it could be an existing contract
suite. Aegis1 checks the trace from the approved criterion to the reviewed
workspace and its evidence.

### Review-ready criteria from impact analysis

Retain the criterion's `check` summary and add this `verification` object when
turning a source finding into an implementation handoff:

```json
{
  "setup": "Apply the baseline and the candidate migration in disposable PostgreSQL.",
  "action": "Run the previous worker's insert twice with the same key.",
  "expected": "Both calls succeed and exactly one pending row remains.",
  "source_paths": ["worker/legacy.py", "migrations/002_partition_pending.sql"],
  "existing_checks": ["checks/legacy_enqueue.sql"],
  "coverage_gap": "Check a database seeded with a pending row before migration."
}
```

Run `sdd.py validate spec.json --review-ready` before review and include
`--review-ready` when approving. If no existing check covers a criterion,
use an empty `existing_checks` list and describe the missing assertion in
`coverage_gap`. Approval checks that referenced paths are captured project
files, and verification checks that referenced reusable checks still exist.
The existing free-text criterion format remains supported.
