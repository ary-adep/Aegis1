# Review Evidence

## Contents

- Evidence sources
- False-positive control
- Finding proof
- Scope
- Recommendations

## Evidence sources

Prefer:

1. changed code
2. surrounding code
3. tests
4. requirements
5. schemas/contracts
6. build/configuration
7. runtime evidence when relevant

## False-positive control

Before reporting a finding:

- inspect surrounding code
- search for callers/consumers
- check project conventions
- check tests
- determine whether the alleged condition can actually occur
- identify whether another layer intentionally handles it

## Finding proof

A strong finding explains:

`location → observed behavior → failure mechanism → impact`

## Scope

Review only the requested change and necessary context.

Do not turn a focused review into an unrelated architecture audit.

## Recommendations

Recommendations should address the identified problem.

If several fixes are possible, give the simplest reasonable direction unless the user asks for alternatives.
