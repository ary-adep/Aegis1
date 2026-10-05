# Aegis1 Skill Evaluations

Aegis1 uses evaluation-driven Skill development.

## Purpose

Evaluations are the source of truth for whether a Skill preserves intended behavior after refactoring.

## Method

For each specialist maintain representative scenarios covering:

1. normal case
2. boundary/risk case
3. failure or ambiguity case

For each scenario record:

- query/task
- repository or fixture
- expected behavior
- forbidden behavior
- terminal status
- human approval expectations
- important evidence

## Model matrix

Test each Skill with every Claude model intended for actual use.

Record:

- model
- Skill version
- scenario
- result
- observations
- regressions

Do not encode a model assumption into Skill frontmatter unless the platform explicitly supports and requires it.

## Observe → refine → retest

After real usage:

1. record unexpected behavior
2. determine whether the Skill caused or failed to prevent it
3. make the smallest useful instruction/structure change
4. rerun the scenario
5. add a regression scenario when appropriate

## Quality gates

A Skill should not be considered V2-complete merely because it is shorter.

It must also preserve:

- safety boundaries
- terminal status
- specialist responsibility
- evidence discipline
- human approval boundaries
- relevant distributed-system reasoning
