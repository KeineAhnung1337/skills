---
name: install4j offline engineering
description: Write, improve, debug, and validate install4j .install4j installer projects offline; screens, actions, scripts, launchers, bundled JREs, media, updates, signing, and installer failures.
---

# install4j: offline installer engineering

Work only with local project files, locally installed install4j and its documentation, local build artifacts, and local logs. Do not use web search, web fetch, remote MCP servers, package downloads, or cloud tooling for this workflow. For the **whole** session to be offline, the model and build dependencies must also be local.

## Establish the source of truth

1. Read `references/workflow.md` and the relevant part of `references/diagnostics.md`. Locate the `.install4j` project, its referenced files, build configuration, media definitions, and the installed `install4j`/`install4jc` version (`install4jc --version` if available). Do not assume this skill targets a particular install4j release.
2. Prefer install4j's own **Install AI Skill** action (in the installed IDE) to generate its version-pinned schema, bean catalog, samples, API, and documentation into a *separate* skill. If available, load/read that generated skill and match its version and compiler to the project. This skill is named `install4j-offline` to avoid overriding the vendor's skill. See `README.md` for setup.
3. Otherwise use the exact installed version's local help, schema, IDE-generated project or working project of the same version. Check the root `<install4j>` version and actual compiler version. If schema/property syntax cannot be established locally, ask for a matching project, vendor skill, local documentation, or IDE access; **never invent bean classes, XML attributes, IDs, script APIs, or project skeletons**.

## Make a focused change

- **Write:** gather target OS/architecture, install mode (GUI/console/unattended), Java runtime, payload, launchers/services, upgrade/uninstall behavior, privileges, signing, and offline requirements. Start from the installed IDE's project template or a compatible sample, then add the smallest required screens, actions, media, and launcher configuration. Keep source paths portable when required; verify each referenced file locally.
- **Improve:** inspect the existing installer flow and baseline before editing. Preserve application identity, element IDs referenced from scripts, upgrade paths, file overwrite rules, uninstall behavior, and per-platform overrides. Avoid incidental project-format upgrades, mass reformatting, or generated file rewrites.
- **Bugfix:** reproduce with the exact media, platform, JRE, invocation mode, compiler output, and installer log. Decide whether the failure is at compilation, extraction, action/script execution, launcher startup, update, or uninstall. Trace the first relevant error to a specific setting or action; change that setting, not the whole flow. See `references/diagnostics.md`.
- Treat project scripts, custom actions, and build hooks as executable code. Read before running. Never include passwords, license keys, signing material, private paths, or customer data in a public project, command line, test log, or response file. Do not turn on signing/notarization or a network updater in an offline test.

## Verify, then report

1. Check the diff and parse XML for well-formedness (not semantic correctness); verify referenced files, version compatibility, and intended platform/media selections. Do not normalize or serialize the whole project just to check XML.
2. If a matching local compiler and required local inputs/license exist, run `install4jc --test <project.install4j>` **only after** checking its configured scripts/hooks and temporary/output paths. `--test` performs a dry-run build and may execute custom build steps or write temporary files; it does not run an installer or prove install/uninstall behavior. Use the version-pinned compiler path if supplied by the vendor skill.
3. Run a generated installer, upgrade, or uninstaller only in a disposable local VM/test environment, after confirming the destination and side effects with the user. Validate GUI, console, and unattended modes as applicable; never install into a real user/system location just to test. Keep diagnostics local and redact them before sharing.
4. Report the change, exact versions/media/modes tested, compiler and runtime evidence, limitations (including missing install4j, license, runtime, payload, or target OS), and any remaining risk. Never claim a working installer from XML parsing or dry-run compilation alone.
