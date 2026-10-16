# Where to look (relative to `eclipse-rcp/`)

| Topic | Working notes | Platform 4.40 docs |
| --- | --- | --- |
| e3 workbench, legacy RCP | `references/e3.md` | `vendor-docs/platform-isv-4.40/guide/workbench.htm`, `guide/rcp.htm`, `reference/api/org/eclipse/ui/package-summary.html` |
| e4 workbench and DI | `references/e4.md` | `vendor-docs/platform-isv-4.40/reference/api/org/eclipse/e4/ui/workbench/package-summary.html`, `reference/api/org/eclipse/e4/core/contexts/package-summary.html`, `reference/api/org/eclipse/e4/ui/di/package-summary.html` |
| SWT/JFace/UI thread | `references/swt-jface.md` | `vendor-docs/platform-isv-4.40/guide/swt_threading.htm`, `guide/jface_viewers.htm`, `reference/api/org/eclipse/swt/widgets/Display.html` |
| Jobs, startup, OSGi | `references/performance.md`, `references/osgi-build.md` | `vendor-docs/platform-isv-4.40/guide/runtime_jobs.htm`, `guide/workbench_scalability.htm`, `guide/runtime_model_bundles.htm`, `guide/runtime_app_model.htm` (OSGi application container, **not** e4 UI model), `reference/api/org/eclipse/core/runtime/jobs/Job.html` |
| Selected XML extensions / APIs | `references/osgi-build.md` | `vendor-docs/platform-isv-4.40/reference/extension-points/`, selected pages under `reference/api/org/eclipse/` |

Search the extracted HTML for symbols or terms (`rg -l 'symbol' vendor-docs/platform-isv-4.40/guide vendor-docs/platform-isv-4.40/reference/api`). Refer to exact *available* class HTML files for thread, disposal, nullability, and lifecycle contracts. The entire upstream **guide** remains local, but the API/reference is intentionally selective; these authored notes are navigation and workflow, not a substitute for omitted API signatures. Some links in Javadoc will be broken. Use installed SDK sources for missing pages, not internet links.

This reference is platform version **4.40 / Eclipse 2026-06**. Verify the actual product's e3/e4 mix and bundle versions before proposing changes.
