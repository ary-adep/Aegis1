# Pilot provenance review

This review covers the 41 paths changed from pre-integration commit
`3daca30563ac628f6380be333e3b7930ba40f544` to pilot commit
`3ad281f7a8efc5bc105d478afa7e79d4327c4ac8`. It compares the committed
snapshot to ECC at `4adeee6732a12d1540f49a4d50a38ce8c97f9a53` and
AgentShield at `b0891303bdcd6037376a94263d45cfd2ff3dfb98`.

## Observed overlap

Compared 38 changed pilot files against all 4,951 tracked ECC files and 244
tracked AgentShield files. The comparison used full-file SHA-256 and groups
of three lines after trimming and normalizing whitespace and filtering out
lines shorter than 20 bytes. The only matching pilot file was
`LICENSE-ECC`. It matched the ECC license byte for byte and shared standard
MIT language with other upstream license files.

The three remaining paths are audit tables. They contain upstream file
paths, component IDs, hook names, and dependency metadata. Keep that
provenance visible. The tables are documentation for the audit.

## Implementation comparison

| Aegis1 capability | Observed implementation | Assessment |
| --- | --- | --- |
| Token accounting | Python reader for a named Claude or Codex log, with explicit unknown totals. ECC's JavaScript hook deduplicates Claude messages and calculates model pricing. Both group usage by message ID. | Documented adaptation. No matching code block detected. Review this algorithm first if replacing all ECC-informed implementation is a release requirement. |
| Installer preview | Extends the existing Python installer and managed-file fingerprints. ECC's planner resolves its profile and module catalog. | Common preview behavior with different installation models. |
| Evidence receipts | Hashes the Aegis1 evaluation case, result, and named evidence files. ECC binds capsule projections and journal state and supports a detached signer. | Common integrity goal with different data models and verification paths. |
| Configuration inspection | Reads explicitly selected Claude or Codex configuration files. AgentShield discovers files and applies its broader rule pipeline. | Different inspection scope and implementation. The pilot adds no AgentShield runtime dependency. |
| Memory, reviewed lessons, and context preview | Extends Aegis1's SQLite store, fingerprints cited sources, and bounds explicit lesson previews. ECC's reference vault uses filesystem records and its own search and context modules. | Distinct storage and workflow, with documented behavioral inspiration. |

## Limits and release decision

Whole-file and text checks detect literal overlap. They can miss short
excerpts, paraphrases, translations, and reused structure. The comparison
covers the integration diff and the two pinned repositories. It cannot
establish ownership of every contribution or authorize company use.

No literal implementation copy was found in this review. Keep the existing
ECC notice. For a release with a stricter provenance requirement, write the
required behavior as Aegis1 acceptance tests and commission a separable
implementation of any remaining disputed adaptation. The next candidate to
review at that level is token accounting. Preserve existing notices in
published snapshots.

## Stricter release criteria

Use the [standalone token accounting brief](../token-usage-requirements.md)
for an independently authored replacement. The implementer receives the
behavioral contract and synthetic inputs. The reviewer runs the existing
compatibility tests and compares the delivered source with the pinned
upstream and previous implementation.

Before calling a new archive ready, record the origin and disposition of
each disputed adaptation, inspect the exact payload for upstream code and
wording, and verify the packaged installer and regression suite. Preserve
the historical attribution and audit trail. This is a source provenance
standard. Permission to distribute Aegis1 and approval to use it at work
are separate decisions.

The current working tree contains a replacement based on the behavioral
brief. The implementer had already seen the earlier Aegis1 and ECC sources
while auditing them. Record this as a specification-based rewrite. The
stronger source isolation described above has yet to be demonstrated.
