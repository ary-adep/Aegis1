# Schema and event change impact

Use the proposed diff, migration, contract, or requested change as the starting
point. Check only affected compatibility surfaces. This workflow produces an
assessment and proposed checks. Use the active task's authority for execution.

1. **Establish the change.** Compare the current and proposed behavior. Identify
   the owning service, affected tables, constraints, fields, and event versions.
   Establish which application versions, rows, and messages must coexist.
2. **Follow source dependencies.** Search for the actual names and literals.
   Open the referenced definitions and callers before drawing conclusions.
   For SQL, inspect explicit insert and update columns, defaults and nullability,
   constraints and index predicates, conflict targets, and result mappings.
   For events, trace producer construction, serialization, consumer parsing and
   validation, and outbox, dead-letter and replay paths where present.
   Check deploy configuration when it controls order, overlap, or rollback.
   A graph or filename match can point to evidence. Confirm material edges in
   source and identify gaps when relevant code or deployments are unavailable.
3. **Evaluate version overlap.** For each affected dependency, ask what fails
   when old code meets the new schema or new consumers meet old records.
   Assess new producers against old consumers and whether the rollback version
   can handle state already written. Distinguish compatibility of API payloads,
   persisted state, and event replay. Flag an unsafe intermediate step even
   when the final design appears sound.
4. **Choose decisive verification.** Find existing project-owned checks and
   inspect what they actually assert. Prefer the narrowest check that uses the
   affected old or new entry point and expected input. A clean-schema check
   alone cannot establish an upgrade path. A test that constructs a current
   event cannot establish compatibility with historical serialized events.
   Identify the uncovered behavior if a new check is needed. Keep static
   reasoning, prior run evidence, and newly executed results distinct.

For each material finding, record the change, affected dependency with source
citations, failure conditions, and decisive check. Draft an SDD requirement
and an observable criterion for each decision-critical risk. Each criterion
needs a setup, action, and expected result. Name the project check to reuse,
or state the missing assertion. Treat the criteria as proposals until approved.
For a spec-driven handoff, put the cited paths and check coverage into the
structured verification plan described by the
[SDD workflow](../../aegis/references/spec-driven-development.md).

For consequential changes, state the rollout precondition, how the actual
running version will be verified when relevant, and what prevents rollback.
Keep narrow assessments inline and stop once the requested impact and evidence
gaps are covered.
