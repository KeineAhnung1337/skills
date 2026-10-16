---
name: Eclipse RCP 4.40
description: Diagnose, optimize, and maintain Eclipse RCP 4.40 (2026-06) applications using e3, e4, or the compatibility layer; SWT/JFace, OSGi, jobs, startup, UI responsiveness, and memory. Offline documentation included.
---

# Eclipse RCP 4.40: offline engineering

Never use web search, network package downloads, HTTP documentation, or cloud-only tooling for this skill. The included `vendor-docs/platform-isv-4.40/` is a **curated subset** of the Eclipse Platform Plug-in Developer Guide and API/reference for 4.40: the complete guide plus selected e3/e4/SWT/JFace/jobs API pages and extension points. `references/` supplies task-oriented guidance. A fully offline *agent* also requires a locally hosted model and cached build dependencies.

## Identify architecture before editing

1. Read `references/index.md` and relevant task guide. Inspect `MANIFEST.MF`, `plugin.xml`, `*.product`, `*.feature`, `Application.e4xmi` / fragments, target platform, `pom.xml` or PDE/Gradle build and Java baseline.
2. Determine whether each affected area uses **e3 workbench APIs**, **native e4**, or **e3 compatibility on the e4 workbench**. e3 uses `org.eclipse.ui` extension points, `ViewPart`/`EditorPart`, `IWorkbench*`; e4 uses model, contexts/DI, parts/handlers, and `@*` lifecycle annotations. The presence of e4 bundles alone does *not* make a product pure e4. Do not translate one approach to the other without a request and migration plan.
3. Identify the target's precise versions. This documentation is **Platform 4.40**, not necessarily versions of third-party bundles, EMF, GEF, RAP, or the user's own product. For other APIs check the local target platform and source/Javadoc; never guess signatures or use `internal` classes as stable APIs.

## Optimization loop

1. Establish an observable baseline: environment, JVM, target platform, workspace state, cold/warm startup, operation, latency/heap/UI stall, and repeatable measurement. Read `references/performance.md`.
2. Profile/diagnose first. Capture thread dumps for UI freezes; inspect sampled CPU, allocation/heap, GC, logs, bundle activation, workspace jobs, and SWT resources depending on symptom. Protect customer data. Prioritize a measured bottleneck.
3. Implement the **smallest** correct change preserving behavior and compatibility. Keep SWT widget access on the UI thread; do heavy work in a `Job` or background service; handle cancellation, dispose listeners/resources, preserve model and DI lifecycles. See `references/e3.md`, `references/e4.md`, `references/swt-jface.md`, `references/osgi-build.md`.
4. Run project tests/build using only locally available tools/dependencies. Re-measure under comparable conditions, test e3/e4 integration as applicable, and report before/after values or say that improvement is not proven. Do not upgrade the target platform, remove dependencies, disable workbench features, or clear user workspace data as a shortcut.

## Finding answers offline

- Start with `references/index.md` for exact local links. Read the original guide under `vendor-docs/platform-isv-4.40/guide/` and available API pages under `vendor-docs/platform-isv-4.40/reference/api/` with normal filesystem search; use the included extension point docs and exact 4.40 Javadocs for signatures when present.
- The compact edition omits many API classes and extension points. Links within vendor HTML may point to omitted files. If an exact page is absent, consult the offline 4.40 SDK/target platform's documentation or sources; do not invent an API or fetch it online.
- Avoid treating example snippets as complete plugin/project templates: check the target manifest and extension schemas. For uncertain APIs verify the actual 4.40 API page and dependency bundle, or explicitly state the uncertainty.
- The vendor files retain `about.html`, `notices.html`, and license. See `README.md` for provenance and offline setup. Their online links are historical references, **not** dependencies.
