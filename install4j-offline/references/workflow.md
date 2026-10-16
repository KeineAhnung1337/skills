# Project workflow (offline)

## Inventory

- Find the `.install4j` file, root version, installer/launcher applications, distribution tree and source directories, included JARs, JRE bundles, scripts/custom code, media definitions, compiler variables, and build scripts (Maven, Gradle, Ant, CI). For merged projects, inspect all local inputs.
- Inspect Git diff before and after editing. Paths may be absolute by default: in the installed IDE, **General Settings → Project Options** can save paths relative to the project for portable builds; do not blindly rewrite paths if the build intentionally uses absolute paths.
- Identify which installed toolchain produced the project. A generated vendor skill contains a pinned install4j version and compiler path; use only when it matches the project and installed compiler. Respect existing project `version` rather than silently changing it.
- Check the target OS, CPU, JRE (bundled vs discovered), service privileges, and whether source files are present offline. A compiler variable or referenced payload that is missing locally cannot be assumed valid.

## Editing

- The install4j IDE is the safest way to add unfamiliar beans/screens/actions or create a new project. Save an example project in the same version and compare its XML if direct editing is necessary. The version-matched vendor AI skill's schema and bean catalog are more reliable than unrelated snippets.
- Keep IDs and references stable; scripts can use IDs to address screens, actions, components, and media. Keep update and uninstall paths aligned with installer changes. Check behavior for silent and console modes if a screen or user prompt changes.
- For new projects, collect requirements and use a local installed template. If no local schema/sample/IDE is available, provide a concrete design and list missing inputs instead of manufacturing XML.

## Validation levels

1. `git diff --check` on edited text and XML parsing (e.g. `python3 -c 'import sys,xml.etree.ElementTree as ET; ET.parse(sys.argv[1])' path/to/project.install4j`). Parsing does not validate bean settings or referenced paths.
2. `install4jc --version` and `install4jc --help` from the matching local installation. Dry-run with `install4jc --test path/to/project.install4j` when safe. A dry run builds in a temporary directory rather than publishing media; it still needs local inputs and may have side effects from custom build logic.
3. On the correct OS, build only intended media where possible (`--build-ids=...` or `--media-types=...`, confirmed using the matching compiler help). A regular build can overwrite existing media; use an isolated destination and obtain consent if important output might be replaced.
4. In a disposable VM, test clean install, repeat install, upgrade from the oldest supported version, launcher/service startup, unattended/console behavior if supported, and uninstall. Check files, permissions, logs, and exit status. Tests on one OS do not prove another OS works.

Do not pass a license key, keystore password, or sensitive compiler variable on a command line: arguments can be visible to other users or saved in history/logs. Keep local secret/config files outside the repository and avoid printing their contents.
