# Reference map (all local)

| Need | Read |
| --- | --- |
| Creating/organizing cases, includes, procedures | `suite-design.md` |
| Component recognition, SmartIDs, synchronization | `components.md` |
| Variables, Jython/Groovy/JavaScript and run context | `scripting.md` |
| Batch execution, analysis, reports | `cli.md` |
| Triage of failing/flaky tests | `diagnostics.md` |
| Live instance via local MCP | `mcp.md` |
| Node names, attributes, rc API, complete examples | Installed QF-Test 11.0.0 manual and tutorial |

Paths above are relative to `references/`. The official manual installed with QF-Test is normally under `<QFTEST_HOME>/doc/manual/en/contents.html`; its *Reference manual* documents node attributes, and *Technical reference* documents CLI and scripting APIs. Locate the actual path on the offline host rather than assuming an install directory. `../vendor-docs/manual/en/contents.html` may hold an authorized local copy if you stage one yourself.

**Version boundaries:** these notes are based on QF-Test 11.0 concepts documented in the 11.0-series manual; they have not been verified against this user's exact 11.0.0 binary. Confirm every CLI flag or node field against the installed manual before use. XML details are intentionally not guessed.

**Source provenance (for the author, not an online dependency):** QFS 11.0-series manual chapters “Organizing the test suite”, “Components”, “Scripting”, “Problem analysis and debugging”, “Command line arguments and exit codes”, “MCP Server”; OpenCode V2 “Skills” and “MCP servers”. All actionable guidance required by the skill is provided locally or in the installed manual.
