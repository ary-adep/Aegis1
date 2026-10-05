# Implementation Verification

## Contents

- Test sequence
- Coverage
- Diff review
- Acceptance criteria
- Failure handling

## Test sequence

Prefer:

1. compile/build validation when appropriate
2. focused unit tests
3. focused integration/contract tests
4. relevant regression suite
5. broader verification when justified

Use project-native commands.

## Coverage

Use existing project coverage tooling.

Do not invent a threshold.

Report:

- tool used
- scope
- measured result
- whether a threshold exists
- limitations

Passing tests do not prove coverage was measured.

## Acceptance criteria

For each important criterion state the verification evidence.

## Diff review

Check:

- intended files only
- no accidental changes
- no debug artifacts
- no secrets
- no unrelated formatting churn
- no missing tests
- no unintended API/schema changes

## Failure handling

If verification fails:

- classify application vs environment/tooling/data/dependency failure
- preserve evidence
- do not claim success
- stop or fix within approved scope

If the failure requires consequential environment mutation, obtain human approval.
