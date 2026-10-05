# Discovery Methods

## Contents

- Repository discovery
- Component discovery
- Dependency discovery
- Communication discovery
- Data discovery
- Configuration discovery
- Runtime discovery
- Integration discovery
- CAP-relevant discovery
- Completion checks

## Repository discovery

Identify every Git repository in scope independently.

For each repository determine:

- root
- branch/state when relevant
- build system
- major modules
- deployables
- libraries
- generated content
- tests
- configuration

Do not collapse separate repositories into one logical repository merely because they are related.

## Component discovery

Identify:

- applications
- services
- modules
- libraries
- adapters
- shared components
- background workers
- scheduled jobs
- deployables

Record responsibility from evidence rather than names alone.

## Dependency discovery

Inspect:

- Maven/Gradle/npm/etc. manifests
- parent and module relationships
- dependency versions
- internal libraries
- generated clients
- build plugins
- runtime dependencies

Distinguish compile-time dependency from runtime communication.

## Communication discovery

Look for:

- REST/HTTP
- WebClient/RestClient
- Feign
- gRPC
- Kafka/RabbitMQ/JMS
- database access
- cache access
- file/SFTP
- SDK calls

For important paths record caller, target, protocol, direction, synchronous/asynchronous behavior, and evidence.

## Data discovery

Identify:

- primary data stores
- schemas
- tables/collections
- ownership indicators
- migrations
- read/write paths
- caches
- replicated/read-only stores
- important state transitions

Do not infer data ownership solely from table names.

## Configuration discovery

Inspect:

- application configuration
- profiles
- environment variables
- secrets references
- feature flags
- endpoints
- timeouts
- retry settings
- connection settings

Do not expose secret values in the report.

## Runtime discovery

When runtime evidence is necessary, prefer read-only inspection.

Record what was observed and when. Do not create, restart, stop, or mutate infrastructure during pure discovery.

## Integration discovery

Map external:

- payment
- identity
- messaging
- notification
- partner
- storage
- analytics
- government/regulatory
- enterprise system

integrations when they affect the requested system understanding.

## CAP-relevant discovery

CAP analysis is conditional.

Look for evidence of:

- replicated state
- multiple authoritative writers
- distributed transactions
- asynchronous state propagation
- caches used as state
- read replicas
- partition-sensitive workflows
- service-to-service correctness dependencies

Do not label a system CP/AP merely because it has multiple services.

## Completion checks

Before completing discovery:

- important boundaries are identified
- important paths are traced
- evidence classification is explicit
- uncertainty is visible
- no recommendations were smuggled into discovery
- no repository/product state was modified
