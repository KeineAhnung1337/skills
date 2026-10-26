# Resolution, class spaces, and versioning

## Read the resolver evidence

Start with the unresolved requirement and the candidate capabilities. A missing package is only one failure mode: the candidate may be filtered out by its version, execution environment, attributes/directives, singleton collision, native-code clause, or a transitive `uses` constraint. Record the complete resolver explanation before editing a manifest.

The identity of a Java type depends on both its binary name and defining class loader. For `ClassCastException`, `LinkageError`, `NoClassDefFoundError`, or loader-constraint violations, trace the package wiring of both consumer and provider. Look for duplicate embedded API classes, split packages, stale refreshed bundles, or the same API exported by multiple bundles. Restarting can confirm stale wiring, but it is not a metadata fix.

Inspect the built JAR's `META-INF/MANIFEST.MF`, contents, embedded libraries, and generated service-component headers. Source `MANIFEST.MF` or `bnd.bnd` files may not equal the packaged result.

## Dependency metadata

- Prefer `Import-Package` for normal code dependencies because it expresses the actual package capability and allows providers to vary. Reserve `Require-Bundle` for an intentional bundle-level contract.
- Keep implementation packages private. Export only supported consumer/provider APIs, and avoid split packages across bundles.
- Use optional imports only when code genuinely operates without that package and guards every access path. An optional unresolved import can become a runtime class-loading failure.
- Avoid wildcard dynamic imports. They defer errors from deterministic resolution to runtime and make wiring dependent on timing and installed bundles.
- Treat fragments as host class-space contributions with coupled lifecycle, not general dependency injection. Verify the host range and whether the framework must refresh the host.
- Do not use boot delegation or system-package exports to conceal duplicated dependencies unless the runtime contract explicitly requires them.

## Versions and compatibility

OSGi versions have `major.minor.micro.qualifier` form. Version exported API packages independently of the containing bundle. Use the project's established annotations or package metadata and let its existing bnd tooling calculate imports where configured.

For an API package:

- increment major for a change incompatible with existing consumers;
- increment minor for compatible additions that can require provider changes;
- increment micro for compatible fixes with no API contract expansion;
- use qualifiers to distinguish builds without changing semantic compatibility.

Provider and consumer compatibility ranges differ; do not invent a range without identifying which role the importing bundle has. If prior released bundles are available locally, use the project's bnd baseline configuration or equivalent binary-compatibility check. Review the reported API delta instead of applying version suggestions blindly.

After metadata changes, resolve the complete application/repository, not just the edited bundle. Test update/refresh behavior if the deployment supports in-place updates.
