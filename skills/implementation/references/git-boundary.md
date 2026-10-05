# Human Git Boundary

## Contents

- Agent responsibilities
- Human responsibilities
- Required stopping point

## Agent responsibilities

Aegis1 may:

- inspect Git state
- inspect diffs
- modify source/tests/configuration/migrations within scope
- run approved verification
- report results

## Human responsibilities

The human owns:

- staging
- commit creation
- push
- merge
- rebase
- pull request creation
- release
- deployment
- production operations

## Required stopping point

After verified implementation and diff review, stop.

Do not "helpfully" create a commit or PR unless the architecture of Aegis1 is explicitly changed in a future version to grant that authority.

This boundary is intentional and must not be inferred away from a user request phrased as "finish everything."
