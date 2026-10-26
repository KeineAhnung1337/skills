---
name: osgi-offline
description: Build, diagnose, test, and evolve framework-neutral OSGi applications and bundles using local sources, caches, runtimes, and documentation. Use for bundle resolution, class spaces, Declarative Services, service dynamics, Config Admin, manifests, bnd-based builds, package versioning, and Equinox or Apache Felix runtime failures. For Eclipse RCP UI, workbench, product, SWT, or e3/e4 concerns, use the Eclipse RCP skill instead.
---

# OSGi offline engineering

Work entirely from the project's local source, built artifacts, dependency caches, runtime, and documentation. Do not search the web, download dependencies, add remote repositories, or silently replace the selected framework or build system. The current stable reference baseline is OSGi Core Release 8 and Compendium Release 8.1, but the project's actual framework, API bundles, and service specification versions are authoritative.

## Establish the system boundary

Before editing, identify:

- the framework and version (for example Equinox or Apache Felix), Java runtime, launch mechanism, and deployment unit;
- the build style: bnd/Bndtools, Maven, Gradle, PDE/Tycho, or hand-maintained manifests;
- bundle manifests or bnd instructions, DS component descriptors/annotations, framework configuration, repositories/target platform, tests, and the exact failing artifact;
- whether the request concerns plain OSGi or an Eclipse RCP product. Route workbench, SWT/JFace, e3/e4, `plugin.xml`, feature, and product behavior to the Eclipse RCP skill while retaining this skill for the underlying OSGi failure.

Do not infer capabilities from a marketing or aggregate release number. Read the resolved API package versions and the runtime's implemented service versions.

## Diagnose by layer

Classify the first concrete failure before changing metadata:

1. **Build/package:** compilation, generated manifest, DS descriptor, or repository assembly is wrong.
2. **Resolution:** requirements cannot be wired to compatible capabilities, including package versions, execution environment, native code, or `uses` constraints.
3. **Lifecycle:** a resolved bundle fails to start, stop, update, or activate.
4. **Service/component:** DS cannot satisfy a reference or configuration, a service changes dynamically, or activation code fails.
5. **Application:** bundles and components are healthy but domain behavior is wrong.

Capture the original resolver or SCR diagnostic, bundle states, relevant headers, component description/configuration state, service properties, and exception chain. Inspect the built JAR rather than trusting only source metadata. Keep package identity and class loader boundaries in view: the same class name loaded from different package wirings is not the same Java type.

Read [resolution and versioning](references/resolution-and-versioning.md) for unresolved bundles, linkage/class-cast errors, exports/imports, fragments, or compatibility changes. Read [services and components](references/services-and-components.md) for DS, service registry, Config Admin, activation, and concurrency. Read [build and validation](references/build-and-validation.md) before modifying build metadata or claiming a fix works.

## Make the narrowest durable fix

- Prefer explicit package capabilities and services over implementation coupling. Preserve the project's established tooling and descriptor style.
- Treat `DynamicImport-Package: *`, broad boot delegation, start-level manipulation, forced eager activation, fragments, and widened version ranges as diagnostic clues or last-resort compatibility measures, not routine fixes.
- Do not replace `Import-Package` with `Require-Bundle` merely to silence resolution. Do not export implementation packages or create split packages to make classes visible.
- Prefer Declarative Services for ordinary service publication and consumption when the project already supports it. Keep activators small and use the service registry's dynamic model rather than global singletons or cached framework objects.
- Preserve lifecycle symmetry: unregister/close/unget resources, stop executors, remove listeners, and make activation failure leave no partial state.
- Version exported API packages deliberately and baseline released APIs when local prior artifacts are available. Do not derive compatibility from bundle version alone.

## Verify offline

Use only the project's existing offline-capable build and test commands after confirming their required repositories/caches are local. Validate the generated bundle, resolver state, component activation/deactivation, service arrival and departure, configuration updates, and clean shutdown as applicable. For API changes, compare against a locally available released baseline. Report commands and observable results; if dependencies or a runnable framework are absent, state exactly what could not be verified.
