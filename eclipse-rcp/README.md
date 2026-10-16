# Offline Eclipse RCP 4.40 skill

Copy this entire directory to `.opencode/skills/eclipse-rcp/` in a project or `~/.config/opencode/skills/eclipse-rcp/` globally. Load with `@eclipse-rcp`. Keep `vendor-docs/`, `references/`, and `SKILL.md` together. No installation script, network request, MCP server, or package manager is needed to read this skill.

## Included documentation

- **Compact subset** of the Eclipse Platform Plug-in Developer Guide **4.40.0.v20260527-1827**: all `guide/` pages, selected e3/e4/SWT/JFace/jobs Javadocs, selected workbench extension-point pages, and legal notices. Start with `references/index.md` for verified local navigation. The full Javadoc index and some links inside retained HTML may lead to omitted pages. For an omitted API consult your offline 4.40 SDK/target platform, not the web. This does **not** include JDT, EMF, Tycho or third-party documentation.
- Original upstream artifact (not bundled in this compact edition): `org.eclipse.platform.doc.isv_4.40.0.v20260527-1827.jar`; SHA-256: `6f2a712aadc05e4225baaf1950e024f7e1d57ac362ade08668ab811202f11848`.
- Source: `https://download.eclipse.org/releases/2026-06/202606101000/plugins/org.eclipse.platform.doc.isv_4.40.0.v20260527-1827.jar` (source citation only; never needed offline).
- Licensing/notices: `vendor-docs/platform-isv-4.40/about.html`, `vendor-docs/platform-isv-4.40/notices.html`, and the full Eclipse Public License 2.0 in `vendor-docs/EPL-2.0.txt`. Preserve these when copying or redistributing. The bundle's `about.html` governs the included content; check it for any exceptions.

The entire skill is under 25 MB. This size limit means it is **not** a complete offline Eclipse SDK reference. Keep the extracted tree, notices, and license when transferring. Links inside the original guide can point to documentation excluded by this compact edition.

**Important:** to run builds truly offline, bring a matching 4.40 target platform, JDK, Maven/Tycho or PDE dependencies and any required plugin sources/caches to the offline machine. A local model must be configured separately; the skill cannot make a remote LLM offline. This workspace does not contain the user's RCP application, so no application-specific optimization has been measured or verified.
