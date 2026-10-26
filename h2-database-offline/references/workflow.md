# Offline H2 workflow

Use this reference to identify the local H2 installation, select a connection mode, and diagnose an application integration. Substitute real local paths; never paste a password into a command that will be logged or committed.

## Inventory before changing anything

Inspect the project's dependency declarations and resolved dependency graph without allowing downloads. Look for Maven or Gradle caches, application bundles, IDE plug-ins, or a supplied `h2-*.jar`. Determine the JAR version from locally observable evidence, for example its manifest or the output of a matching H2 tool. Prefer build-tool offline mode when resolving dependencies; if an artifact is missing, report it instead of fetching it.

Record:

- H2 version and JAR path
- JDK vendor and version
- application, framework, ORM, connection-pool, and migration-tool versions
- sanitized JDBC URL and the configuration source that wins at runtime
- in-memory, embedded file, or local TCP server mode
- database path resolved to an absolute path
- schema initialization order and migration history
- whether another process currently owns the database

H2 tool entry points commonly include `org.h2.tools.Shell`, `Console`, `Script`, `RunScript`, and `Recover`, but their flags and availability are version-dependent. Ask the matching local JAR for help before constructing a command, such as:

```text
java -cp /absolute/path/h2-VERSION.jar org.h2.tools.Shell -help
```

Do not infer the database engine version solely from a filename when stronger local evidence is available.

## Connection modes

Typical URL shapes are shown only as recognition aids; confirm parameters against the installed version.

```text
jdbc:h2:mem:logical-name
jdbc:h2:file:/absolute/path/to/database
jdbc:h2:tcp://localhost/absolute/path/to/database
```

- An in-memory named database is normally scoped to one JVM/class-loader context and can disappear when its last connection closes. Parameters that keep it alive change lifecycle and test isolation; add them only intentionally.
- Embedded file mode is the simplest persistent local arrangement but normally expects one engine/JVM owner. Do not open the same files independently from multiple processes.
- TCP mode supports multiple local clients through one H2 server process. Bind only to loopback for an offline workstation and start it only when required.
- Relative file URLs depend on the process working directory. Resolve and report the effective absolute path. Before first connection, verify whether the intended database already exists; a typo may otherwise create an empty database.
- Options such as automatic server mode, file encryption, auto-reconnect, delayed close, or compatibility `MODE` materially change behavior. Preserve existing options during diagnosis and verify each against the exact installed H2 version.

## Build and framework changes

Keep the existing dependency scope: test-only H2 should not leak into production runtime. Do not replace the production database dialect with H2 merely to make tests green. If H2 intentionally substitutes for another engine in tests, document known semantic gaps and keep critical SQL covered by tests against the real engine elsewhere.

When changing application configuration:

1. Trace configuration precedence and active profiles.
2. Keep secrets outside source-controlled URLs and files.
3. Confirm ORM dialect, identifier case/quoting, schema name, DDL generation, and migration ownership.
4. Avoid letting both an ORM auto-create facility and a migration tool own the same schema.
5. Use an explicit initialization order and fail on migration errors.

## Diagnostic order

1. Capture the complete exception chain and first H2-originated error without exposing secrets or row data.
2. Confirm the application actually loaded the expected JAR and JDBC URL.
3. Resolve the database path, owner process, permissions, and file state.
4. Reproduce on a disposable copy or newly initialized temporary database.
5. Reduce the issue to the smallest connection, migration, or statement that still fails.
6. Compare SQL, identifiers, data types, reserved words, and metadata assumptions with the installed version's local documentation or behavior.
7. For locking issues, identify the owning process and transaction. Do not delete lock artifacts.
8. For performance issues, capture schema, indexes, cardinalities, parameters by type/selectivity, plans, and timings. Change one factor and remeasure.

Do not claim production-engine compatibility from H2 acceptance alone. Pay special attention to null handling, identity/sequence behavior, transaction isolation, DDL transaction semantics, case folding and quoted identifiers, date/time types, JSON/LOB behavior, locking, and vendor-specific functions.
