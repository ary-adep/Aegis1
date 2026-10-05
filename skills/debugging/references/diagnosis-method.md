# Diagnosis Method

## Contents

- Failure capture
- Reproduction
- Localization
- Hypotheses
- Verification
- Root cause
- Reporting

## Failure capture

Record:

- expected
- actual
- exact error
- time/context
- affected component
- reproduction conditions

## Reproduction

Prefer the smallest safe reproduction.

Record whether reproduction is:

- deterministic
- intermittent
- unavailable

Do not weaken safety controls merely to force reproduction.

## Localization

Trace:

`input → boundary → operation → dependency → failure`

Use logs, stack traces, tests, code, and configuration.

## Hypotheses

Each hypothesis should predict evidence that would support or contradict it.

Avoid listing unsupported guesses.

## Verification

Run the smallest safe check that distinguishes hypotheses.

Examples:

- focused test
- configuration inspection
- dependency health check
- log correlation
- controlled read-only runtime inspection

## Root cause

A root cause should:

- explain the failure
- fit the observed evidence
- account for relevant reproduction
- survive reasonable alternative hypotheses

## Reporting

Report:

1. failure
2. reproduction
3. evidence
4. hypotheses tested
5. root cause or why unconfirmed
6. contributing factors
7. recommended next step
8. limitations
