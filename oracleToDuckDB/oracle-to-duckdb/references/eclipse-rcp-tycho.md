# Eclipse RCP, OSGi, and Tycho integration

Use this when the application is built with Maven/Tycho and the DuckDB JDBC driver is supplied as a local JAR. The goal is a reproducible offline product, not merely a compile-time Maven dependency.

## Audit first

Locate parent and module POMs, target definitions, `MANIFEST.MF`, `build.properties`, feature definitions, product definitions, p2 repositories, launch configurations, and CI build commands. Determine which bundle owns persistence and every OS/architecture the product packages.

For the supplied JAR:

1. Record its path, version, size, and SHA-256 in the audit report.
2. Inspect `META-INF/MANIFEST.MF`, `META-INF/services`, `org/duckdb` packages, and bundled native-library paths.
3. Check whether it is already a valid OSGi bundle and whether its symbolic name, exported packages, execution environment, and native contents work with the target platform.
4. Confirm redistribution policy and that one approved artifact covers every product platform. Never fetch a replacement from the internet.

## Packaging choices

Prefer the least invasive option that works in the exported application:

### Existing OSGi bundle

If the JAR has usable OSGi metadata, expose it through the project's offline target/p2 or existing third-party dependency mechanism. Add the bundle to the consuming bundle's requirements and to every relevant feature/product. Do not rely on a dependency that is visible only to Maven tests.

### Embed in the persistence bundle

For a non-OSGi JAR, embedding is suitable when only one bundle needs the driver:

- place the approved JAR under a repository convention such as `lib/` in that bundle;
- include it in `Bundle-ClassPath` alongside `.` and in `build.properties` `bin.includes`;
- keep persistence code in that bundle so its class loader can see DuckDB classes;
- explicitly call `Class.forName("org.duckdb.DuckDBDriver")` before the first connection when service discovery does not cross the bundle boundary.

### Wrapper bundle

Use a dedicated third-party wrapper when several bundles require DuckDB APIs or the repository already wraps external JARs. Embed the JAR, export only the packages actually consumed, include it in the wrapper build, and add the wrapper to features/products. Generate or verify package metadata with tooling already available offline; do not guess an incomplete package list.

Do not both embed and separately install the same driver. That can create distinct class loaders, duplicate native loading, and confusing connection behavior.

## Build and runtime checks

- Keep the vendored JAR at a stable project-relative path and avoid dependencies on a developer's local Maven cache.
- Ensure Tycho includes the JAR and its native entries without unpacking, filtering, re-signing, or stripping them unexpectedly.
- Verify the runtime temporary directory is writable and compatible with native-library extraction. Capture startup errors clearly rather than falling back to Oracle.
- Update feature/product configuration for all launch modes, including tests and the exported product.
- Avoid adding Oracle and DuckDB drivers simultaneously to mask incomplete migration; a deliberately time-boxed transition must be explicit in the approved audit.
- Run the normal build offline, for example `mvn -o verify`, then launch or exercise the exported product and open a temporary DuckDB database through the actual application bundle.
- On every supported OS/architecture, smoke-test driver loading, connection creation, schema creation, an insert/query, clean close, reopen, and file deletion after close. This catches missing native libraries and lingering file handles.

Before removing Oracle artifacts, search manifests, POMs, target files, features, products, launch configurations, source, SQL resources, and deployment configuration. Remove credentials and Oracle connection settings only after all consumers have moved.
