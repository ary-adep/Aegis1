# Token accounting requirements

The evaluation CLI accepts `usage --host claude|codex LOG` and summarizes
one user-selected UTF-8 JSONL file. It reads locally without changing the
input, making network calls, or printing prompts or replies. The existing
command and result fields remain compatible with evaluation records.

| Requirement | Acceptance check |
| --- | --- |
| Count each Claude assistant message ID once using its latest available usage. | Supply two reports for one ID and one report for a second ID. Require two counted messages and totals from the latest usage for each. |
| Count Claude cache reads and writes in total input. Report cache reads in `cached_input_tokens` and writes in `cache_write_input_tokens`. | Supply two messages with fresh inputs 4 and 3, reads 10 and 0, and writes 6 and 2. Require total input 25, cached input 10, and cache writes 8. |
| Sum completed Codex turns from a single thread. Codex input already includes cached input. | Supply completed turns with input 22 and 20, cached input 10 and 0, and output 3 and 5. Require input 42, cached input 10, and output 8. Report writes separately when present. |
| Preserve uncertainty. | A missing, negative, or noninteger counter is unknown, including a Boolean. A cached input count greater than known input is unknown. Represent unknowns as JSON `null` and reserve zero for observed zero. |
| Avoid reporting partial counts as complete totals. | Supply malformed JSONL, a Claude assistant record without an ID, an unterminated or failed Codex turn, or multiple start-of-thread events. Require unknown totals and a diagnostic that omits log contents. |
| Bound individual input records. | Reject a line larger than 16 MiB with a diagnostic that identifies its line number and omits its contents. |

Output includes `host`, a nested `usage` object with `input_tokens`,
`cached_input_tokens`, and `output_tokens`, the separate
`cache_write_input_tokens` counter, `usage_records`, and `usage_notes`.
The notes identify unavailable fields and the scope of the report.

Implement from this brief and synthetic host event examples. For an
independent replacement, provide the implementer this brief and the CLI
contract without upstream or prior implementation source. After delivery,
the reviewer runs the existing compatibility suite, checks the new source
and packaged contents for provenance, and records the candidate commit.
