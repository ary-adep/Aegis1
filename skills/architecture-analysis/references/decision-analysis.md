# Architecture Decision Analysis

## Contents

- Options
- Trade-offs
- Evidence
- Risks
- Human decisions
- Recommendation boundaries

## Options

Describe only viable options supported by the context.

For each option capture:

- approach
- benefits
- costs
- risks
- constraints
- affected components
- migration/rollout implications

## Trade-offs

Prefer explicit statements:

`Improves X at the cost of Y under condition Z.`

Avoid generic claims such as "more scalable" without explaining why.

## Evidence

Each material architectural claim should be grounded in:

- repository evidence
- runtime evidence
- requirement
- measured behavior
- established constraint
- explicit decision

## Risks

Describe:

- likelihood when meaningful
- impact
- affected boundary
- mitigation or decision needed

Do not invent numerical risk scores without a defined model.

## Human decisions

Escalate when architecture materially affects:

- business behavior
- data ownership
- security
- compliance
- compatibility
- consistency/availability
- irreversible migration
- operational cost
- production risk

## Recommendation boundaries

Pure architecture analysis may identify viable options and trade-offs.

Do not silently choose an option when the decision belongs to the human or the task only requests analysis.
