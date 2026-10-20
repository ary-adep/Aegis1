# Aegis1 Skill V2 Audit Checklist

Checked items below mean static instruction/distribution checks completed for this candidate, or evaluation cases authored. They do not mean model behavior passed. See [audit report](audit-report.md) and [validation results](validation-results.md). Existing successful terminal statuses are preserved; blocked/decision statuses were added where missing.

## Anthropic structure

- [x] `name` is valid and concise.
- [x] `description` is third-person, specific, and includes when to use.
- [x] `SKILL.md` body is under 500 lines.
- [x] Detailed material is progressively disclosed.
- [x] References are one level deep from `SKILL.md`.
- [x] Every reference is directly linked from `SKILL.md`.
- [x] Every reference over 100 lines has a contents section.
- [x] Paths use `/`, not Windows backslashes.
- [x] Terminology is consistent.
- [x] Options are minimized; a default approach is given where appropriate.

## Workflow quality

- [x] Trigger is clear.
- [x] Non-trigger/boundary is clear.
- [x] Workflow is sequential where sequence matters.
- [x] Checklists exist for complex workflows.
- [x] Feedback loop exists where output can be validated and corrected.
- [x] Degree of freedom matches task fragility.

## Aegis1 governance

- [x] Evidence model preserved.
- [x] Human decision gates preserved.
- [x] Working-tree safety preserved.
- [x] Human Git boundary preserved.
- [x] Production boundary preserved.
- [x] Environment side effects classified by actual effect.
- [x] Exact specialist terminal status preserved.

## Distributed systems

- [x] CAP invoked only when relevant.
- [x] Consistency requirements identified where relevant.
- [x] Availability requirements identified where relevant.
- [x] Partition behavior considered where relevant.
- [x] Idempotency/retry/message semantics considered where relevant.
- [x] No distributed infrastructure introduced without justification.

## Evaluation

- [x] Normal scenario.
- [x] Boundary/risk scenario.
- [x] Failure/ambiguity scenario.
- [x] Regression scenario where a previous defect/gap existed.
- [ ] Tested on each intended Claude model.
- [ ] Real-work observation captured.

## Platform and integration gates

- [ ] Claude Code installation and agent/skill loading smoke-tested.
- [ ] Routing and foreground behavior observed on the installed version.
- [ ] Actual dirty-worktree preservation evaluated.
- [ ] Intended model IDs supplied and full model matrix executed.
