# Local CLI and validation

Locate the executable from the **offline host's** installation. On Linux/macOS it is commonly `qftest`; on Windows, use `qftestc.exe` for a console batch process (the GUI `qftest.exe` may return immediately). Quote paths. Confirm options with the installed 11.0.0 manual or `-help` first.

```sh
qftest -batch -version
qftest -batch -help
```

For a known safe test suite and available SUT, the documented 11.0-series form is:

```sh
qftest -batch -runlog run.qrl -report ./report ./suite.qft
```

This executes tests; it is **not** a read-only validation command. To restrict a run, the manual documents `-test <n>|<ID>`; check how your suite identifies its target before use. Exit status reflects result severity but may be changed by `-exitcode-ignore-*` options; review run log/report for failing nodes and unexpected skips. Only run after checking side effects and obtaining required approvals.

The manual also documents `qftest -batch -analyze ...` with switches such as `-analyze-references`, `-analyze-duplicates`, `-analyze-components`, `-analyze-procedures`, `-analyze-tests`, `-analyze-followincludes`, and `-analyze-target <directory>`. Confirm the precise behavior and selected options in the installed manual; use a dedicated output directory, inspect results, and do **not** add `-remove-unused-callables` or `-remove-unused-components` in a read-only analysis. Analysis is not proof of runtime correctness.

`-convertxml`, `-compress`, `-import`, and cleanup/removal options can write suites; never use them for validation without an explicit editing request and a backup. `scripts/inspect_suite.py` is an offline, read-only XML inventory only; its findings are hints, not QF-Test errors. Installed UI / exact-version batch execution is the final authority.
