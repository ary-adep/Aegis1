# Coverage Verification

## Contents

- Coverage purpose
- Existing tooling
- Measurement
- Thresholds
- Interpretation
- Limitations

## Coverage purpose

Coverage helps identify exercised code paths. It does not prove correctness.

## Existing tooling

Use the project's existing coverage mechanism when available, such as its configured Maven/Gradle/other coverage tooling.

Do not introduce a new coverage system merely to satisfy a request unless that is within scope.

## Measurement

Record:

- coverage tool
- report type
- measured scope
- line/branch/method metrics when available
- exclusions when material

## Thresholds

Do not invent a threshold.

If the project has a configured threshold, report whether it passed.

If no threshold exists, report measured coverage without declaring it inadequate solely because it is below an arbitrary value.

## Interpretation

Low coverage can identify risk but is not itself a defect.

High coverage can still miss incorrect assertions or important scenarios.

Combine coverage with acceptance criteria and risk-based tests.

## Limitations

If coverage cannot be generated:

- state why
- preserve test results
- do not claim coverage was verified

Passing tests and coverage measurement are separate evidence categories.
