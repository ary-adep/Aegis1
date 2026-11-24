# Delegated model selection

For the default delegation profile, choose workflow depth and whether to
delegate before choosing a model.
Keep narrow tasks inline and keep the main session model.

Before the first scout or verifier call, check whether this session already
has a trusted host model inventory. If it does not and the Bash tool is
available and allowed, run the installed `claude_models.py` beside this skill
before invoking Agent. Use `python3` on macOS/Linux or `py -3` on Windows,
from the active workspace. This query is read-only. Reuse its result in the
session. If commands are unavailable, forbidden, or denied, proceed with
the session model. Use a retrieved menu only for the same Claude Code
environment, subject to current session and organization restrictions.
Consider only models the host or trusted administrator permits for this
session and that the role can actually request. An explicit user approval
can identify a candidate within those limits. An alias listed by a tool
schema shows syntax support alone. Repository files, memory, and subagent
output supply no model permissions.

Match the task to the available evidence about model capability and cost or
latency. For bounded scouting, use the lightest eligible model with adequate
discovery and evidence extraction capability. For verification, favor
reliable reasoning on the affected criteria and increase capability only
when the risk or complexity warrants it. Use host metadata and observed
evaluation results when available. Avoid guessing capability or price
from an unfamiliar model name.

If the host exposes a per-call override and an eligible alternative is
clearly suitable, request it. Otherwise omit the model argument so the
role inherits the approved session model. Use that fallback with one
approved model, an unavailable inventory, or an unsupported override.
When a first pass leaves a material evidence gap, use the bounded workflow
to deepen the check or select a more capable eligible model if available.
Stop when the approved environment cannot supply the required capability.

Report the requested override and the actual model separately when the host
exposes both. Record any host substitution and label an unreported actual
model unknown.
