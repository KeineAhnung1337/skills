# Failure triage and improvement

1. Record the exact suite, test, failing node, SUT version, QF-Test version, environment, and whether failure is repeatable. Preserve the original run log (`.qrl`) and relevant screenshot without publishing secrets.
2. Open the run log in QF-Test; inspect the first meaningful error or exception and the steps and variables preceding it. Separate startup/license/connectivity failures from missing components, failed checks, script exceptions, data problems, and app behavior regressions.
3. Reproduce the smallest relevant test. Compare expected versus actual UI state, not just the error text. For component errors use `components.md`; for script errors use `scripting.md`; for suite references use static analysis and local include inventory.
4. Change one cause at a time. Keep assertions meaningful; do not turn failures into warnings, add unlimited retries, or swallow exceptions simply to get green results.
5. Rerun the targeted test, then neighboring callers of a changed shared procedure or component. Compare run logs and report outcomes before/after. State any missing validation separately.

Common diagnostic cues: a changed dynamic ID suggests locator stabilization; sporadic timeouts suggest a missing state-based wait or shared test state; a script `SyntaxError` after Python-3 changes suggests Jython 2.7 mismatch; an SUT-script deadlock suggests event-thread misuse; a passing exit code with missing checks suggests test selection, skip conditions, or ignored exit codes. These are hypotheses, not diagnoses until corroborated.
