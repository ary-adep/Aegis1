# Engineering documentation changes

Use for documentation creation, cleanup, and recording delivery evidence. Follow project documentation standards when present; do not change those standards or introduce a mandatory template without authorization.

## Evidence and scope

Before editing, identify the requested outcomes and the evidence actually available for each. Use supplied user-run results with that attribution; do not upgrade them to agent-observed or exhaustive verification. If referenced results are absent, complete independent cleanup, identify the missing input, and leave that outcome explicitly pending. Do not claim the results were recorded.

Preserve agreed requirements, decisions, unresolved limitations, and provenance. Separate human decisions from engineering choices. Do not silently turn an implementation limitation into an approved business requirement. Record requirements where the project expects them; avoid duplicate authoritative copies.

## Readable artifacts

Organize by reader need: requirements describe the contract, delivery records describe implementation and verification, and architecture describes the current system. Use short sections and links between them. Use compact tables for comparable facts; use lists or prose when long paths and paragraphs make tables hard to scan. Prefer working relative Markdown links over code-formatted navigation paths. Condense execution narration while retaining evidence needed to understand failures and limitations.

Document current behavior and qualify unmeasured performance or runtime claims. Avoid absolute claims such as every query performing a count or never using an index without supporting evidence.

## Completion check

Read the final changed artifacts, not just the write commands or completion summary.

- Map every requested outcome to its final section, or explicitly identify it as pending with a reason.
- Reconcile statements such as pending, not run, partial, and passed across affected documents. Distinguish historical results from current status; do not erase earlier evidence.
- Verify evidence attribution, links, and readable structure. Inspect rendered Markdown when available; otherwise disclose that only source readability was checked.
- Compare before/after content for the intended scope, including untracked files when relevant. Do not print secrets in comparisons.
- For prose-only edits, verify content and links; reuse dated test evidence rather than rerunning application tests merely to restate their count. Run relevant checks if executable examples, configuration, or generated behavior changed.

The final report must match the actual artifacts and distinguish completed outcomes from missing evidence. A documentation-only request does not authorize code fixes, database checks, or changes to global instructions.
