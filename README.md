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
agent definition. An identical install can be repeated. If a destination file
differs, installation stops before copying files. Review the existing copy and
back it up before upgrading. The original Windows Git Bash installer remains
available.

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

The orchestrator is explicitly invoked. Specialist skills retain normal automatic discovery. The `/aegis` entry point runs inline in the main conversation, reads the governance body, and disables the Agent tool for its invoking turn without granting permissions. Direct `/implementation` retains its existing custom-agent fork and is not covered by this invocation fix. Within Aegis, specialists are read and applied in the current context. `/code-review` may also name a bundled Claude skill; use `/aegis Review ...` and confirm the Aegis specialist path when identity matters.

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

### Graphify-assisted discovery

Pass `--graph /path/to/graphify-out/graph.json` to use an existing Graphify
export for the same checkout. Aegis1 uses matching symbols and neighboring
nodes to rank tracked paths for the live model. It still verifies quoted
evidence from repository reads. The graph itself is read locally, is never
sent to the model, and does not grant additional file access. The export may
be stale, so regenerate it separately when the repository changes. The
simulated model uses its fixed read sequence.
