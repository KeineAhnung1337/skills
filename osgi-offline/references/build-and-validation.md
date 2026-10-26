# Build and offline validation

## Preserve the existing toolchain

Identify which tool owns the generated manifest and DS descriptors before editing:

- bnd/Bndtools commonly uses `bnd.bnd`, workspace `cnf`, and generated manifests;
- Maven may use bnd tooling directly or through bundle plugins;
- Gradle may use a bnd workspace/plugin or custom JAR instructions;
- PDE/Tycho usually combines source manifests with a target platform and Eclipse metadata.

Do not introduce a second manifest-generation path. Determine which file wins when instructions appear in parents, workspace defaults, plugin configuration, or subprojects. Inspect the final JAR after every packaging change.

Before an offline build, confirm that the JDK, wrapper/distribution, plugin artifacts, dependency repository, target platform, baseline artifacts, and test runtime are already local. Run the build's offline mode where available. Never change repository URLs, relax verification, or remove tests to make an offline build appear successful.

## Artifact checks

For every changed bundle, verify as applicable:

- valid bundle symbolic name and version;
- package imports/exports and their attributes, directives, and versions;
- `Bundle-RequiredExecutionEnvironment` or effective execution-environment requirement;
- packaged DS XML and matching `Service-Component` header;
- absence of unintentionally embedded/duplicated API packages and split packages;
- bundle contents, licenses, native clauses, and reproducibility rules expected by the project;
- API baseline results against the intended local released artifact.

Warnings from bnd or the repository resolver are design feedback. Explain or fix them; do not suppress them globally without understanding the affected wiring.

## Runtime validation

Use the runtime's available local console, management API, logs, or test harness to record bundle state, wirings, services, and DS component state. Exact commands vary by framework/version; inspect the installed command help rather than assuming Equinox and Felix syntax is interchangeable.

Validate the smallest relevant matrix:

1. assemble the bundle/repository/application;
2. resolve all required bundles in a clean framework state;
3. start and activate the affected components;
4. exercise service and configuration transitions relevant to the change;
5. stop cleanly and check for leaked registrations, threads, listeners, or resources;
6. test update/refresh only if supported by the product's deployment model.

Report the framework and Java versions, build/test commands, whether caches were complete, and the observed result. A successful bundle build does not prove repository resolution or DS activation.
