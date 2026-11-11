# Aegis1

Aegis1 is a governed software engineering agent for Claude Code. It routes work through eight specialists while preserving evidence, user work, human Git ownership, and production boundaries.

## Current status

This is a supervised pilot, not a production-certified developer replacement. It contains audited instructions, local structural checks, and evaluation fixtures. User-supplied Claude transcripts demonstrate feature implementation and review on a small Spring Boot application (148 application tests reported passing, with selected user-run MySQL smoke checks). Those observations are not a completed model evaluation matrix. The latest documentation-skill patch still needs a fresh-session behavioral retest. Kafka/Redis microservices and installation on another laptop remain unvalidated. Historical audit documents describe their dated scope, not the current installation state. See [audit findings](evaluations/audit-report.md), [validation results](evaluations/validation-results.md), and [evaluation instructions](evaluations/README.md).

## Install into a Claude Code project

This repository is the source distribution. Its root `skills/` and `agents/` folders are not automatically project skills merely because Claude Code is launched here.

The installer works with Python 3.9+ on macOS, Linux, and Windows.
Run it from this checkout and choose one scope:

```sh
python3 install-aegis.py --project "/path/to/project"
python3 install-aegis.py --personal
```

In Windows PowerShell, use `py -3 install-aegis.py --project "C:\path\to\project"`
or `py -3 install-aegis.py --personal`.

The installer copies the nine skills and their Markdown references plus the
agent definitions and local memory helper. An identical install can be repeated.

Check the installer version with `python3 install-aegis.py --version`.
Version 0.2.0 and later record the installed version and file fingerprints in
`.claude/.aegis1-install.json`. To upgrade a versioned installation, run the
new installer with the same scope. It only replaces files that match their
recorded fingerprints and backs them up under `~/.aegis1/install-backups/`.

For an unversioned copy-based install from the original main release
(`012e406`), run the new installer with the same scope. Version 0.2.1
recognizes its unchanged files automatically, including Windows line endings.
For other older versions, use a matching checkout to verify the existing files:

```sh
python3 install-aegis.py --personal --upgrade-from "/path/to/previous/Aegis1"
```

On Windows use `py -3` in place of `python3`. When run interactively,
the installer can back up and replace unrecognized files in an unversioned
copy-based install after asking for confirmation. Conflicts in a versioned
installation stop the upgrade. The Git Bash wrapper runs the same personal
installer. Recognized legacy Aegis1 junctions and agent symlinks are moved
into `.claude/.aegis1-link-backups/` before installing independent copies.
Their target checkout is preserved. Unrecognized linked contents stop the
migration. After installation, you can move or remove the source clone.
To update later, run the installer from a fresh clone of the desired release.

Project scope uses the project's `.claude/` directory. Personal scope uses
`~/.claude/`. Claude Code supplies the active model and permissions. Start
a fresh session, confirm `aegis1` appears in `/agents`, and run a read-only
`/aegis` discovery test.

## Use

```text
/aegis Discover this repository and explain the request-to-storage flow. Do not edit files.
/requirements-analysis Analyze the supplied requirement and identify unresolved business decisions.
/implementation-planning Plan the approved change using actual repository paths.
/implementation Implement the approved change and verify its acceptance criteria.
/testing-verification Verify the change against the supplied acceptance criteria.
```

The orchestrator is explicitly invoked. Specialist skills retain normal automatic discovery. The `/aegis` entry point runs inline in the main conversation, reads the governance body, and can delegate a bounded read-only investigation to the installed scout when the host permits it. Direct `/implementation` retains its existing custom-agent fork and is not covered by this invocation fix. Within Aegis, specialists are read and applied in the current context. `/code-review` may also name a bundled Claude skill; use `/aegis Review ...` and confirm the Aegis specialist path when identity matters.

Provide the repository, expected behavior, and constraints. Aegis investigates missing technical evidence, reports unknowns, and asks for consequential business or architecture decisions. Approval already supplied for an understood scope remains valid.

## Responsibilities

| Specialist | Primary output |
| --- | --- |
| system-discovery | Evidence-based map of what exists |
| requirements-analysis | Requirements, acceptance criteria, decisions |
| architecture-analysis | Boundaries, options, trade-offs |
| implementation-planning | Ordered changes and verification mappings |
| implementation | Scoped changes with verification evidence |
| testing-verification | Criterion-level verification results |
| code-review | Supported findings from the actual change |
| debugging | Confirmed cause or explicit evidence gap |

Analysis and review do not edit product files. Implementation may edit within scope. Aegis does not stage, commit, push, merge, rebase, create PRs, release, deploy, or perform production operations. These are instruction-level boundaries; this distribution does not claim an operating-system sandbox or permission-hook enforcement.

## Local checks

Python 3.10 or newer, standard library only:

```text
python scripts/validate.py .
python -m unittest discover -s tests -v
python scripts/evaluate.py list
```

These check structure and evaluation tooling, not Claude behavior. See the evaluation guide for preparing isolated model runs and recording evidence. Do not declare V2 validated until the intended model matrix and real-work observation are complete.

## Platform references

Checked on 2026-10-13:

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)

The custom agent requires `name` and `description` frontmatter. Forked skills select it through `agent`. Actual compatibility with the user's installed Claude Code version remains part of the installation smoke test.

## Standalone discovery pilot

Install from this checkout into a virtual environment with Python 3.9 or
newer. Git must be available on the machine.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/aegis1 run --repo /path/to/git-checkout --model simulated "Map the entry points"
```

The pilot requires a Git working-tree root and can read tracked files only.
The simulated model exercises the tool and evidence loop and reports
`DISCOVERY BLOCKED` with exit status 1 because it cannot interpret the task.
The Claude Code installation instructions above still apply for live Claude
workflows.

To try a live discovery run, configure an OpenAI API key in
`OPENAI_API_KEY` and explicitly choose a model that supports Structured
Outputs in the Responses API:

```sh
.venv/bin/aegis1 run --repo /path/to/git-checkout --model openai/MODEL "Map the entry points"
```

Use only repositories approved for this provider. The adapter sends the task,
tracked path inventory, and bounded file excerpts to the provider. API usage
is billed according to the API account.

### Automatic standalone model selection

Use `--model auto` to query configured provider inventories and select a
known model suitable for read-only discovery. Set `OPENAI_API_KEY` for OpenAI
or `ANTHROPIC_API_KEY` for the Claude API. One configured provider is
sufficient. The optional `AEGIS1_APPROVED_MODELS` environment variable limits
both automatic and explicit live selections to its comma-separated list of
provider/model IDs. The result of automatic selection includes the requested
model. For explicit Claude selection use `--model claude/MODEL`.

### Pause and resume discovery

Keep the checkpoint outside the inspected repository. The checkpoint stores
the task, checkout path, revision, and fingerprints of the file prefixes
read so far. When resuming, Aegis1 rereads tracked files, reuses matching
evidence, and identifies changed or missing sources. Repeat the same task
and repository. You can select a different approved model on resume.

```sh
aegis1 run --repo /path/to/repo --model claude/MODEL \
  --checkpoint /path/outside/repo/run.json --pause-after 1 "Map the entry points"
aegis1 run --repo /path/to/repo --model openai/MODEL \
  --checkpoint /path/outside/repo/run.json --resume "Map the entry points"
```

### Graphify-assisted discovery

Pass `--graph /path/to/graphify-out/graph.json` to use an existing Graphify
export for the same checkout. Aegis1 uses matching symbols and neighboring
nodes to rank tracked paths for the live model. It still verifies quoted
evidence from repository reads. The graph itself is read locally, is never
sent to the model, and does not grant additional file access. The export may
be stale, so regenerate it separately when the repository changes. The
simulated model uses its fixed read sequence.

## Local project memory in Claude Code

Use `/aegis` to explicitly remember a verified finding, recall project
findings, or delete a record by ID. For example, ask Aegis1 to remember a
verified entry-point finding and name its source file. In a fresh session in
the same project, ask it to recall that finding.

Records live in `~/.aegis1/memory.sqlite3`. The helper scopes them to the
resolved project path. A finding can cite several source files, and recall
marks it stale if any cited file changes or disappears. Memory is local to this laptop and saves only explicit findings.

## Read-only Claude Code scout

The Python installer includes the `aegis1-scout` custom subagent. Start a fresh
Claude Code session and check that it appears in `/agents`. From the regular
Claude Code conversation, ask:

> Use the aegis1-scout subagent to locate where /aegis selects a specialist.
> Cite files and lines. Read only within this checkout.

The scout inherits the session model by default and has Read, Glob, and Grep tools.
`/aegis` can also select the scout automatically for a scoped investigation. Both installer entry points include the scout.

## Multi-repository discovery in Claude Code

Open the common parent folder of the relevant service checkouts. You can add
a `WORKSPACE.md` with service names, relative checkout paths, and contract
locations. Aegis1 uses the map to find evidence in the checked-out files.
For cross-repo findings it reports each repository's branch, commit, and
local changes when available, plus any missing checkout or revision.

Example: `/aegis What would adding a required field to OrderPlaced affect?`
If you explicitly save a cross-repo finding, recall it from the same workspace
root. Cite each relevant source so changes in either repository can mark it
stale. The standalone CLI takes one Git repository per run.

## Independent verification in Claude Code

For consequential changes, such as changes to an event shared across
repositories, `/aegis` can delegate an evidence check to `aegis1-verifier`.
The verifier inherits the session model by default and has Read, Glob, and Grep tools.
Aegis1 hands it the scope, change, acceptance criteria, and available test
evidence. The main session owns any authorized runtime checks and reports
the final status. Focused verification can stay inline.

## Model selection in Claude Code

Aegis1 keeps narrow tasks in the main session. For delegated work it selects
among models the host exposes as approved and available, using the task and
any capability, cost, or latency evidence available. When the host provides
no usable inventory or override, the scout and verifier inherit the session
model. A Claude-only session with one approved model can use both roles.
Ordinary task prompts require no model names or role-to-model settings.

When needed for delegated work, the installed helper queries Claude Code's
model menu through the CLI or VS Code extension executable. It initializes
a host connection without submitting a task. The session's model and policy
restrictions still apply. If the helper cannot reach the host, the role
inherits the session model.

## Compatibility with the work guard

If your existing guard permits `aegis-scout` and `aegis-verifier` and both
read-only agents are installed, opt in by putting the single line
`work-guard` in `~/.aegis1/delegation-profile`. The pilot then calls the
existing role names and leaves model selection to their host configuration.
The guard still controls delegation. If a role is denied or unavailable,
Aegis1 uses an allowed inline check or reports a blocker.

Test with a project-scoped installation first. In a fresh Claude Code
session, ask Aegis1 to show the exact skill file it loaded and use the scout
for a bounded read-only question. Confirm the pilot skill path and an
actual `aegis-scout` invocation. Use a consequential verification task to
check `aegis-verifier` separately. Keep the existing marketplace checkout
available while it supplies the guard plugin.

## Local discovery UI

From the Aegis1 checkout, launch the local UI with Python 3.9 or later:

```sh
python3 scripts/aegis1_ui.py --workspace-root "$HOME/Desktop/Aravind"
```

Open the loopback URL printed in the terminal. Select Claude Code or Codex,
browse for a workspace, choose a suggestion, or enter a relative or absolute folder path
inside the configured workspace root, and start a read-only chat. Browse opens\nthe system picker on macOS and Windows, and uses Zenity or KDialog on\nLinux when available. A browser-based picker is available as a fallback. Each chat keeps its
workspace. Switch hosts between messages, or use New chat to change the
workspace. Select a saved chat in History to resume it or use Delete to remove it from this browser. Copy saves an
individual response to the clipboard as Markdown. Follow-up requests
include the last six non-local messages, with each capped at 4,000
characters. History is stored by the browser for this URL and workspace
root. Private browsing may clear history when its windows close.
The UI uses the installed host's existing sign-in and default model. Claude Code is
limited to file tools and Codex runs in its read-only sandbox. Press Ctrl+C
in the terminal to stop the server.

## Development handoff between hosts

Use the standalone command to save a local checkpoint after an implementation
step. List each authorized file with a separate `--scope`. The checkpoint
contains the scoped Git diff, base revision, file fingerprints, supplied check
results, and remaining work. Store it outside the inspected checkout.

```sh
aegis1 handoff save --repo /path/to/repo --checkpoint /path/to/handoff.json \\
  --scope stock.py --goal "Reject nonpositive reservations" \\
  --evidence "Valid and invalid requests checked" --pending "Independent review"
aegis1 handoff check --repo /path/to/repo --checkpoint /path/to/handoff.json
```

Use the review command to check the snapshot and pass a current checkpoint
to a signed-in host in one step.

```sh
aegis1 handoff review --repo /path/to/repo --checkpoint /path/to/handoff.json --host codex
```

Use \`--host claude\` for Claude Code. A stale snapshot stops the review before
launching the host. If the checkout changes during review, Aegis1 discards the
result and reports the stale snapshot. This verifies that the recorded checkout state still matches. It
does not rerun supplied checks. A stale checkpoint suppresses the earlier
check results in the command output. Recheck the changed work before relying
on those results. The commands use Git and local files.
