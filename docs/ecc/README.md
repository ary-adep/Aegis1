# ECC integration audit and rollout

## Baselines

- Aegis1 baseline is the local `aegis1-standalone-pilot` checkout at
  `3daca30563ac628f6380be333e3b7930ba40f544` with the existing uncommitted
  SDD and impact-analysis work. The baseline passed 49 unit tests, static
  validation, enumeration of 35 evaluation cases, and `git diff --check`.
  The checked-in model matrix still does not establish live parity.
- ECC baseline is [2.2.3 at 4adeee6732a12d1540f49a4d50a38ce8c97f9a53](https://github.com/affaan-m/ECC/tree/4adeee6732a12d1540f49a4d50a38ce8c97f9a53).
  Its source was inspected in a temporary checkout. No ECC installer,
  runtime hook, learning observer, model call, or dependency install ran.
  The root license is MIT, copyright 2026 Affaan Mustafa. Check individual
  component and dependency licenses before copying code.

## Catalog and audit depth

- [Component and dependency matrix](components.tsv) covers all 97 installer
  components, 49 installer modules, and seven profiles. Component dependencies
  are installer modules. Module dependencies come from the pinned manifest.
- [Hook matrix](hooks.tsv) classifies the 28 Claude Code sidecar entries and
  the separate Codex hook entry. These cover the two supported host paths.
- [Source inventory](source-inventory.tsv) assigns a provisional disposition
  to all 4,951 tracked paths. It includes 328 canonical skill entry points,
  agent definitions, commands, rules, alternate host assets and supporting
  code. Inventory does not establish runtime behavior or imply that all
  supporting files were reviewed line by line.

**Keep** preserves an Aegis1 capability or baseline evidence. **Import**
means an isolated upstream file is a candidate for a literal import.
**Adapt** means extract a bounded behavior for the existing Aegis1 path.
**Replace** means use the corresponding Aegis1 surface in the combined
framework. **Exclude** means outside the integration boundary or a duplicate
that should not install. These are review dispositions. All unreviewed runtime
paths stay disabled.

## Source findings and dependencies

| Area | Pinned surface inspected | Decision |
| --- | --- | --- |
| Agents, skills, commands, rules | `agents/`, `skills/`, `commands/`, `rules/`, install components and modules | Keep Aegis1 specialists and governance. Adapt narrowly where a candidate closes a measured gap. Replace duplicate command and rule trees with Aegis1 routing. |
| Hooks | `hooks/hooks.json`, `hooks/hooks.metadata.json`, `hooks/codex-hooks.json`, `scripts/hooks/` | Adapt individually. Claude has a runtime hook graph; Codex has a distinct bootstrap. The Aegis1 installer writes skills and agents without installing host hooks. Do not enable an ECC hook until matcher, effects, conflicts, host behavior, and rollback are verified. |
| AgentShield | `SECURITY.md`, `skills/security-scan`, README runner provenance | Adapt defensive configuration review only after separately pinning and auditing the AgentShield source and package integrity. ECC documents the separate runner and does not supply an audited runner pin. Exclude automated exploitation workflows and automatic fixes. |
| Learning and instincts | `skills/continuous-learning-v2/hooks/observe.sh`, `scripts/lib/instinct-relevance.js` | Adapt reviewed promotion and project relevance later. ECC observes tool events through hooks. Keep Aegis1's explicit save and recall policy, and exclude implicit recording and automatic policy or skill edits. |
| Memory and context | `scripts/lib/memory-vault.js`, `context-selection.js`, `context-retrieval.js` | Adapt export or retrieval only with synthetic data and redaction tests. ECC memory uses a separate CLI/runtime. Context selection includes local libraries and YAML manifests. Keep Aegis1's existing project-local SQLite storage until a candidate demonstrates a measurable gain. |
| Tokens and models | `scripts/hooks/cost-tracker.js`, `scripts/lib/session-cost-snapshot.js`, `src/llm/` | Adapt measurement first. ECC accounts for repeated Claude message events and separates cache counters. Its hook also reads transcripts and writes metrics. Use explicit log inputs, no writes, and existing Aegis1 model permissions. Keep provider pricing and auto-routing out of batch 1. |
| Evaluators and verifiers | `scripts/lib/eval-harness/{envelope,gate,receipt,replay}.js` | Adapt evidence semantics after comparing with Aegis1 records and SDD. Keep the existing verifier, score criteria, and handoff gate. Neither framework's records alone prove authority or correctness. |
| Orchestration and host support | `.codex-plugin/`, `.claude-plugin/`, `scripts/lib/harness-capabilities.js`, `scripts/lib/session-adapters/`, `scripts/orchestrate-worktrees.js` | Adapt host capability checks for Claude and Codex first. Exclude unattended worktree orchestration, other host adapters, and external operator services from initial parity. |
| Installation and upgrade | `scripts/install-plan.js`, module and profile manifests, `scripts/lib/install/`, `install-lifecycle.js` | Adapt plan/dry-run and provenance ideas into the existing fingerprinting installer. Avoid installing two frameworks into the same user configuration. |
| Runtime and packages | `package.json`, lockfiles, `pyproject.toml`, `ecc2/Cargo.toml` | ECC's JS runtime requires Node 18+ and declares TOML, YAML, JSON schema, SQL.js and Zod dependencies. It also includes Python and Rust surfaces. Aegis1 is Python-based. Review dependency closure per imported unit, avoid wholesale Node/Rust adoption, and prefer a standard-library adaptation where sufficient. |

## Incremental delivery and approval gates

1. **Token accounting.** Adapt explicit, read-only accounting for supplied
   Claude and Codex JSONL. Normalize input, output, and cache counters without
   double-counting repeated events. Keep unknown counters explicit. Tests
   require known synthetic totals, duplicate events, incomplete data, and the
   current Aegis1 suite. Retain the pinned source citation and license notice.
2. **Install planning and host inventory.** Add a read-only change plan and
   test it against disposable Claude and Codex configurations with pre-existing
   files. Require explicit approval before changing actual host configuration.
3. **Verification evidence.** Evaluate ECC review receipts and evidence
   envelopes on the same fixtures as Aegis1. Consolidate compatible behavior
   into existing records. Require negative controls for stale and missing
   evidence and scoped writes.
4. **Defensive hooks and configuration review.** Identify one enforcement
   owner per hook event and compare normalized matchers. Test allow, block,
   unavailable host, and uninstall or rollback. Approve enabling each hook
   separately. Treat AgentShield as a separate, pinned dependency.
5. **Memory, learning, and orchestration.** Begin with opt-in, redacted
   synthetic records. Validate project isolation, bounded context, explicit
   promotion, and host permission inheritance. Any transcript collection,
   external service use, or unattended delegation needs separate approval.

After each batch, run structural and unit checks, installation/update/rollback
checks for changed paths, and a focused regression proving the behavior.
For parity, run standalone ECC and integrated Aegis1 on clean, separate host
profiles with the same pinned model, fixture, permissions, and grading rubric.
Track successful criteria, unauthorized effects, evidence gaps, and token
usage where observable. Mark unexecuted comparisons explicitly.

## Upstream synchronization and development freeze

Update from the audited commit, not a moving tag. Review a new revision in a
separate checkout, diff relevant upstream paths and lockfiles, regenerate the
inventory, and record source paths, commit IDs, content hashes, license and
local changes for each imported component. Require the batch tests before
updating the pin. Keep both prior and replacement pins available for rollback.
This is the sync procedure for review. Automating it and verifying a real
upgrade remains open.

Keep the existing SDD and scope safeguards available. Freeze new persistent
Graphify work, SDD extensions, advanced cross-service impact analysis,
architecture and documentation drift features, decision intelligence, and
advanced autonomy until the ECC integration stabilizes.

## Batch 1: explicit token accounting

`scripts/evaluate.py usage` adapts message-level deduplication and cache
accounting from ECC's [cost tracker at the audited commit](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/hooks/cost-tracker.js).
The adaptation lives in `scripts/token_usage.py`. Retain the
[upstream MIT license and copyright notice](LICENSE-ECC). The batch uses
Python's standard library and does not install the ECC hook or reuse its
transcript discovery, pricing, or metrics writes.

Local regression tests use synthetic host records. A standalone ECC
comparison requires approved equivalent log inputs and an isolated runtime.
Live host usage parity and token savings remain unmeasured.

## Batch 2: install planning and host inventory

The installer now exposes `--plan`, following the preview-first approach in
[ECC's pinned install planner](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/install-plan.js).
The implementation uses Aegis1's existing Python installer and
fingerprinting logic. Claude Code preview and application share the same
file classification. A preview also reports known legacy link relocation.
Codex inventory lists configuration entries by name and reports the
available Aegis1 workflow entry points. It does not infer live permissions
or read the contents of host settings. Codex installation remains outside
this batch.

Disposable checks cover fresh installation, repeated preview, known managed
updates, user-file conflicts, legacy links, and Codex configuration
preservation. Actual host registrations and standalone ECC comparisons
remain pending.

## Batch 3: evaluation evidence receipts

This batch adapts the evidence-receipt approach from
[ECC's pinned evaluation receipt](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/eval-harness/receipt.js)
to Aegis1's existing evaluation format. A separate reviewer-held receipt binds
the scoring case, result, and evidence contents. The evaluation pass gate
checks that receipt. Historical record inspection still works without one.
No runtime dependency, host hook, or host configuration change is required.
See [evaluation commands](../../evaluations/README.md) for usage and limits.

## Batch 4: AgentShield and host configuration audit

Reviewed [AgentShield 1.6.0 at b0891303bdcd6037376a94263d45cfd2ff3dfb98](https://github.com/affaan-m/agentshield/tree/b0891303bdcd6037376a94263d45cfd2ff3dfb98)
as a separate source checkout. This is a source pin for the audit. Registry
artifact integrity and the full dependency closure have not been verified.
The project is MIT-licensed and declares Node 20 or newer plus seven direct
dependencies, including the Anthropic SDK, TOML and YAML parsers, and Zod.

| Surface | Source finding | Decision |
| --- | --- | --- |
| Static scanner | `src/scanner/index.ts` discovers configuration and applies rules. `src/scanner/discovery.ts` walks the root and handles linked entries. | Adapt a narrow, explicit project scan before assessing any upstream runtime bundle. Test symlinks and report redaction. |
| Host coverage | `src/harness-adapters/index.ts` recognizes both Claude Code and Codex conventions. The default discovery path is Claude-oriented. | Require separate fixtures and coverage notes for both hosts. Host identification does not establish effective protection. |
| CLI modes | `src/index.ts` offers file writes, auto-fix, network features, model calls, active checks, and hook execution as separate options. | Keep these modes outside the proposed integration. Review static configuration only. |
| Runtime boundary | Aegis1's install planner reads presence only. The Claude runner sets an explicit tool list and empty MCP config. The Codex runner requests read-only mode. | Keep the hosts as enforcement owners. A static finding or clean scan cannot establish the effective permission policy. |

Proposed first implementation: a dependency-free, read-only configuration
check for explicitly selected project files. Start with malformed config,
out-of-scope links, declared hooks and MCP servers, and explicit permission
settings. Reports name paths and finding IDs without printing configuration
values. Validate on synthetic Claude and Codex fixtures with unchanged
before/after snapshots. Review this implementation separately from any
decision to enable hooks or install an AgentShield package.

### Implemented static configuration check

Run the standard-library checker from the Aegis1 checkout:

```sh
python3 -B scripts/config_check.py --project /path/to/project --host claude \
  --file .claude/settings.json --file .mcp.json
python3.11 -B scripts/config_check.py --project /path/to/project --host codex \
  --file .codex/config.toml --file .codex/hooks.json
```

Select only files you intend to inspect. The checker recognizes common
project settings, MCP declarations, and hook files. Exit 0 means inspection
completed with no warnings, exit 1 means a warning was found, and exit 2
means at least one file could not be inspected. JSON inspection supports
Python 3.9+. TOML requires Python 3.11+ for its standard-library parser.
Results show selected relative paths, finding IDs, and levels. Treat these
as static findings, since the host resolves and enforces its own effective
configuration. The checker is an Aegis1 implementation of the audited
approach. AgentShield's runtime package and host hooks remain separate
approval and verification items.

## Batch 5 increment 1: portable project memory

The [local memory helper](../../skills/aegis/memory.py) now supports explicit
transfer of selected findings between checkouts. This is a standard-library
adaptation of the cross-harness memory concept in
[ECC's pinned memory vault](https://github.com/affaan-m/ECC/blob/4adeee6732a12d1540f49a4d50a38ce8c97f9a53/scripts/lib/memory-vault.js).
It uses the existing Aegis1 store and does not import the ECC vault or runtime.

```sh
python3 -B skills/aegis/memory.py --project /path/to/source export \
  --id FINDING_ID --output /private/path/findings.json
python3 -B skills/aegis/memory.py --project /path/to/destination import \
  /private/path/findings.json
```

Repeat `--id` to select multiple findings. Claude Code can use the installed
copy under `.claude/skills/aegis/`. Codex can invoke the same command from
the Aegis1 checkout. Review the bundle before sharing it. It includes
finding text and source fingerprints, with paths relative to the checkout.
Exports require a new output file. Imports validate the entire bundle before
writing, preserve source fingerprints, flag changed or missing evidence, and
recognize repeated imports into the same checkout. A matching fingerprint
does not establish that an imported claim is true.

Verified one Claude Code to Codex handoff on disposable checkouts. Claude
reported verifying and exporting one finding backed by `service.txt`. Codex
reported importing it, recalling port 8088 with `stale: false`, and preserving
the file on import. After the destination file changed, a read-only Codex
recall returned the original 8088 finding with `stale: true`. Reading the
current source confirmed port 9099. This is one observed handoff, with no
token comparison. Automatic learning, context injection, and orchestration
remain open.

## Batch 5 increment 2: reviewed learning

Aegis1 can propose a lesson from a current, cited project finding. The human
reviewer inspects the proposal and records a one-time decision. Approved
lessons become available on explicit recall while their sources still match.
Pending, rejected, and stale lessons are excluded from recall. Deleting
the finding also deletes its dependent lessons.

```sh
python3 -B skills/aegis/memory.py --project /path/to/project \
  propose-lesson --finding-id FINDING_ID --lesson "Check the old handler against the new contract"
python3 -B skills/aegis/memory.py --project /path/to/project list-lessons
python3 -B skills/aegis/memory.py --project /path/to/project \
  review-lesson PROPOSAL_ID --decision approve --by "Reviewer name"
python3 -B skills/aegis/memory.py --project /path/to/project recall-lessons
```

This adapts ECC's opt-in review and relevance concepts into Aegis1's existing
memory store. The reviewer name is an attestation. Access control for the
store stays with the host. Lesson proposals and decisions are local to that
checkout. The portable finding format remains unchanged. Automated
observation, context injection, and orchestration are separate items.

## Batch 5 increment 3: task context preview

```sh
python3 -B skills/aegis/memory.py --project /path/to/project \
  preview-context --task "Verify payment retries" --max-lessons 3 --max-bytes 2400
```

The preview adapts ECC's relevance selection using local term matching.
It returns a JSON list of matching approved lessons with current source
fingerprints, including each lesson's matched terms and source paths. The
byte budget covers the full serialized result. The same helper can be called
explicitly from Claude Code or Codex for human review. Preview does not change
memory or inject the result into a session. The budget bounds output size.
Live token savings and standalone ECC parity remain unmeasured.

On 2026-11-24, Claude Code and Codex in VS Code both reported one lesson
from the same disposable preview script. Both returned lesson
`14de73ca7fa345f1bb2fa93e712d5357` from `policy.txt` with matches
`payment` and `retries`. A local rerun reproduced the output and confirmed
that `project/delay.txt` exists and its approved lesson is stale. The hosts
therefore agreed on the preview result. Codex separately reported that
`delay.txt` was absent from its working directory. The fixture places that
file under `project/`. This check covers explicit script execution in each
host.

## Pilot release checklist

- [x] Preview and install into a disposable project with installer 0.2.6.
  Preview created no `.claude` directory. Install added 45 files. Reinstall
  added and updated zero files. Installed SDD and memory helpers matched the
  checkout, and previewing a project with no memory returned an empty list.
- [ ] Pin and package the candidate, including attribution and a file inventory.
- [x] Upgrade and restore the committed baseline in a disposable project.
  Both snapshots identify as installer 0.2.6. The upgrade added five files
  and replaced five. Manual restoration used the installer backup and
  removed only the five newly installed files. Every prior file and an
  unrelated project file matched the baseline byte for byte. A cross-version
  upgrade from an older deployment remains untested.
- [ ] Confirm the intended host configuration and permissions. Claude Code
  has a project installer. Codex can run shared helpers explicitly and has
  read-only installer inventory.
- [ ] Execute a governed pilot change through independent review and handoff.

Standalone ECC parity and token savings remain unverified. Runtime hooks and
automated learning remain outside the pilot release scope.

## Proportional read-only review

The architecture specialist uses a focused assessment for a bounded question
and opens the architecture-dimensions reference when the scope requires it.
Schema and event change assessments still load the change-impact workflow.
Reports lead with the decision, source evidence, and next check.

Use ARCH-01 for proportional scope, ARCH-02 for consequential distributed
risks, and IMPACT-01 for mixed-version compatibility and rollback. The
configured focused instruction path is 1,095 bytes smaller when the
architecture-dimensions reference is unnecessary. This compares the changed
orchestrator and specialist files plus the previously required reference.
Shared governance is identical on both paths. Post-change model behavior
and token use have yet to be measured.
