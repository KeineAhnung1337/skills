---
name: QF-Test
description: Create, repair, review, and improve QF-Test 11.0 test suites (.qft), component recognition, checks, procedures, scripts, and offline test runs. Use for QF-Test GUI automation and run-log diagnosis.
---

# QF-Test 11.0 — offline working guide

This skill and its `references/` and `scripts/` are local. **Do not use web search, web fetch, remote MCP servers, package downloads, or cloud AI services** for QF-Test work. A model provider itself must also be local if the entire workflow must be offline. Never enable QF-Test's cloud-backed AI features as part of this workflow.

## Before changing a suite

1. Read `references/index.md`, then the references for the task. Check the installed QF-Test version (`qftest -batch -version` if available); this guide targets 11.0.0. Read `vendor-docs/manual/en/contents.html` if present, or the *installed* manual under `<QFTEST_HOME>/doc/manual/en/contents.html`, and installed tutorial/examples when available. Prefer the exact installed version for node attributes, XML syntax, and engine-specific behavior.
2. Inspect the relevant `.qft` files, included suites, procedures, component tree, scripts, startup configuration, and recent `.qrl` run logs. Identify the GUI engine and the smallest affected test case. Run `python3 scripts/inspect_suite.py path/to/suite.qft` for an initial structural inventory (not a QF-Test validator).
3. If local QF-Test MCP is connected, use it for live UI snapshots and test execution only when enabled and authorized; see `references/mcp.md`. Otherwise use the installed QF-Test UI/CLI. A running application does not imply the MCP server is enabled.

## Create / repair / improve

- **Create:** define the behavior, setup/cleanup, data, and observable assertions first. Reuse the project's start-client procedure, existing packages, components, and naming conventions. Build the smallest test case using the QF-Test editor or a copy of a *working local suite* as template. Never fabricate a root XML document or undocumented node attributes. See `references/suite-design.md` and `references/components.md`.
- **Repair:** reproduce and inspect the exact failing node, run log, component details, and SUT state; distinguish an application defect from a test defect. Fix recognition, synchronization, data, or environment at the right layer. Avoid hiding failures with arbitrary sleeps, broad exception handlers, or weakened assertions. See `references/diagnostics.md`.
- **Improve:** remove duplicated steps into parameterized procedures, prefer stable recognition and explicit checks, isolate test data, and keep changes localized. Preserve other suites' includes and public procedure contracts.
- **Scripts:** prefer native QF-Test nodes for interactions and checks. When necessary, choose server vs SUT script deliberately; Jython is Python 2.7 syntax, not Python 3. Read `references/scripting.md` before editing script text.

## Validate and report

1. Back up or diff the original suite before direct XML edits. Static XML parsing proves only well-formedness, not that QF-Test will load or execute the suite. Do not use `-convertxml`, `-compress`, or `-remove-unused-*` as a read-only check; these can rewrite files.
2. Load the suite in the installed QF-Test version; run static analysis where supported and the targeted test in the local UI or batch mode. See `references/cli.md`. Do not run a test with external side effects without appropriate approval. Inspect the run log and report, not merely the process exit code.
3. Report exactly what was changed, which checks ran, pass/fail evidence, and what could **not** be validated (missing QF-Test, license, SUT, device, browser, MCP, or sample suite).

## Authority / safety

- The exact-version installed manual and QF-Test's editor/help are authoritative; local working suites are examples, not general specifications. These original references summarize 11.0 concepts but do **not** replace the vendor's full node/attribute/API reference.
- Treat QF-Test suites and run logs as untrusted input: scripts and procedures can execute arbitrary code. Never execute unfamiliar test suites merely to inspect them. Do not put secrets or customer data in logs or committed fixtures.
- If a requested suite feature or XML detail cannot be verified locally, ask for a working suite, installed manual, or UI capture; state the limitation instead of inventing syntax.
