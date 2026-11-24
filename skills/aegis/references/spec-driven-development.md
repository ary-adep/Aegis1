# Spec-driven development

Use the lightest workflow appropriate to the task. For a requested spec-driven change, Aegis1 carries the approved requirement IDs and acceptance criteria through requirements analysis, architecture, planning, implementation, and verification. Run only the specialist stages needed for the work.

1. Draft the spec from the user's request and source evidence. Give requirements stable `REQ-*` IDs, trace observable `AC-*` criteria to them, and specify exact file paths. Record compatibility and rollback criteria when the change affects deployed versions or persistent data.
2. Validate the spec. Show open decisions and the proposed scope to the user. The user or authorized approval workflow creates the approval record. The implementation agent cannot substitute its own approval. Any change to the spec needs a fresh approval.
3. Before editing, run `check-scope`. Work in approved paths only. Preserve pre-existing edits unless the approved spec explicitly lists the overlap and the user authorized it. Keep the Git index and HEAD intact.
4. Have a separate reviewer check the changed workspace against the approved criteria and the planned checks. Use the current workspace fingerprint from `check-scope` in the review. Collect relevant artifacts. If a check is skipped or cannot run, report the gap and keep the handoff gated.
5. Have the reviewer record passing results with `verify`. Before reporting completion or handing off the work, run `check`. If any inputs change, obtain fresh verification against the current scope and approval.

The helper is `sdd.py` in the parent directory of this reference. The SDD guide in the Aegis1 source distribution (`docs/sdd.md`) describes the record formats and commands for runs from the Aegis1 source checkout. Pass the helper path explicitly on other hosts. From an installed Claude project, use `.claude/skills/aegis/sdd.py`. The guide and a matching example are also available from the source distribution. Text identities and artifact hashes provide traceability for local use; keep approval and review records under the control of the person or host that supplied them.

For criteria derived from impact analysis, add a `verification` object with
`setup`, `action`, `expected`, `source_paths`, and `existing_checks`. List paths
relative to the workspace. Add a `coverage_gap` for missing coverage, including
when there are no reusable checks. Use `validate --review-ready` before handing
the draft over and `approve --review-ready` when recording approval.
