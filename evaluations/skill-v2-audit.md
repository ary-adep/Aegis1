# Aegis1 Skill V2 Audit Checklist

## Anthropic structure

- [ ] `name` is valid and concise.
- [ ] `description` is third-person, specific, and includes when to use.
- [ ] `SKILL.md` body is under 500 lines.
- [ ] Detailed material is progressively disclosed.
- [ ] References are one level deep from `SKILL.md`.
- [ ] Every reference is directly linked from `SKILL.md`.
- [ ] Every reference over 100 lines has a contents section.
- [ ] Paths use `/`, not Windows backslashes.
- [ ] Terminology is consistent.
- [ ] Options are minimized; a default approach is given where appropriate.

## Workflow quality

- [ ] Trigger is clear.
- [ ] Non-trigger/boundary is clear.
- [ ] Workflow is sequential where sequence matters.
- [ ] Checklists exist for complex workflows.
- [ ] Feedback loop exists where output can be validated and corrected.
- [ ] Degree of freedom matches task fragility.

## Aegis1 governance

- [ ] Evidence model preserved.
- [ ] Human decision gates preserved.
- [ ] Working-tree safety preserved.
- [ ] Human Git boundary preserved.
- [ ] Production boundary preserved.
- [ ] Environment side effects classified by actual effect.
- [ ] Exact specialist terminal status preserved.

## Distributed systems

- [ ] CAP invoked only when relevant.
- [ ] Consistency requirements identified where relevant.
- [ ] Availability requirements identified where relevant.
- [ ] Partition behavior considered where relevant.
- [ ] Idempotency/retry/message semantics considered where relevant.
- [ ] No distributed infrastructure introduced without justification.

## Evaluation

- [ ] Normal scenario.
- [ ] Boundary/risk scenario.
- [ ] Failure/ambiguity scenario.
- [ ] Regression scenario where a previous defect/gap existed.
- [ ] Tested on each intended Claude model.
- [ ] Real-work observation captured.
