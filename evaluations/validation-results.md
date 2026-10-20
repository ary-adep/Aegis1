# Validation results

Date: 2026-10-13. Scope: candidate in the Codex outputs workspace. Original `D:/aravind/Aegis1` remains unchanged; all 38 original non-Git file hashes match the captured baseline.

## Executed local checks

| Check | Actual result | Evidence |
| --- | --- | --- |
| Distribution metadata, links, required files, reference layout, and lengths | PASS; nine skills and one agent; zero reported errors | [Structural output](local-results/structure.json) |
| Validation/evaluation tooling regression suite | PASS; 25 tests | [Full test log](local-results/tests.txt) |
| Evaluation scenario loading | PASS; 30 scenarios loaded | [Case list](local-results/case-list.txt) |
| Unmodified fixture | All five acceptance tests pass | Test log: test_baseline_fixture_passes_all_five_tests |
| Injected full-stock bug | Expected failure observed: equality request raises ValueError | Test log: test_bug_fixture_fails_at_full_stock |
| All-skipped suite | Zero process exit but five skipped tests, kept distinct from executed criteria | Test log: test_skipped_fixture_has_zero_exit_but_no_acceptance_execution |
| Source fixture preservation | All 30 packets prepared without changing source fixtures | Test log: test_every_packet_prepares_without_expected_answers_in_task |
| Evidence integrity | False passes rejected for missing execution/evidence, failed criteria, wrong status, removed criteria, and escaped/missing evidence paths | Full test log |

Python runtime: 3.12.14. Checks use the standard library and no network services. The structural validator accepts this distribution's restricted JSON-scalar YAML frontmatter. No package installation was performed.

## Not executed / not established

- No Claude model ran these scenarios. The 30 cases are authored, not passed behavioral tests.
- Claude was not found on the session command path or the checked user-local native/npm installation paths. This does not prove Claude is absent from every location on the computer.
- Intended Claude model IDs were not supplied. The [model matrix](model-matrix.json) remains NOT_CONFIGURED.
- Claude Code installation, actual agent/skill loading, routing, and foreground operation have not been smoke-tested.
- Working-tree preservation requires a real dirty-worktree model evaluation; supplied ownership notes test reasoning only.
- No distributed runtime was exercised; the architecture fixture is documentary evidence.
- No bounded real-work observation is recorded.
- The candidate has not been applied to `D:/aravind/Aegis1` because this session lacks write permission there.

V2 is not declared validated. Local checks support the structure and tooling only; see [evaluation instructions](README.md) for remaining gates.
