# Suite design and creation

## Inventory before edits

Find the top-level suite(s), includes, existing test sets and cases, startup/cleanup sequences, components, packages/procedures, data, and script modules. Note the target engine (Web, Swing/AWT, JavaFX, SWT, native Windows, Android, iOS, etc.). Look for established project conventions and reusable procedures in installed `qfs.qft` and project libraries. Do not rename public IDs or package/procedure paths casually; callers may be in included suites.

## Build a small test

Write a concrete scenario: preconditions → operation → expected observable result → cleanup. Make each case independent where practical, with predictable test data and cleanup. Start/attach the SUT using the project's existing configuration. Represent interactions as event nodes and outcomes as check nodes (or `rc.check` only when appropriate). Prefer one reason to fail per check, with useful diagnostic context. Parameterize stable workflows in procedures and use variables for varying data rather than copying recorded event sequences. Keep tests readable in QF-Test's editor.

Use the QF-Test UI's recorder and component inspector or its built-in 11.0 MCP UI snapshot for new components. For handwritten XML, derive the exact structure from an installed example or a freshly saved minimal suite created by the **same QF-Test version**, then reopen in QF-Test. XML parse success is not a compatibility check. Avoid bulk formatting the suite, changing binary payloads, or dropping namespace/encoding/DOCTYPE declarations. Diff a working copy before and after saves, since the editor may normalize the file.

## Includes and dependencies

Resolve included suites before moving components or procedures; ensure paths work on the destination offline host. Avoid absolute paths tied to this machine. For portability, use project-relative resources and locally installed libraries. Distinguish test data from confidential credentials and machine-specific connection details. To understand references in a suite, use QF-Test's analysis mode (see `cli.md`) after confirming flags against the local manual.

## Review checklist

- Clear test name, purpose, preconditions, teardown, and expected behavior.
- Stable component identifiers and narrow interaction scope; no unexplained coordinate clicks.
- Explicit meaningful checks, including negative and error cases where relevant.
- No brittle ordering or inter-test shared state; retries/timeouts only with a documented reason.
- Reusable procedures preserve parameter defaults and existing callers.
- Suite opens on 11.0.0, targeted test passes, and the result is visible in the run log.
