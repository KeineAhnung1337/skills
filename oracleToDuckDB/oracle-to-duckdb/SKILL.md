---
name: oracle-to-duckdb
description: Audit and migrate Maven/Tycho Eclipse RCP applications from Oracle JDBC and Oracle SQL to offline, embedded DuckDB, including immutable per-import database shards. Use for code-and-schema migrations; do not use for historical Oracle data transfer or live multi-process writes to one DuckDB file.
metadata:
  audience: java-eclipse-rcp-maintainers
  platform: opencode
  workflow: audit-then-migrate
---

# Oracle to DuckDB

Migrate the application's persistence boundary without changing its binary decoder or analytical meaning. Work offline: use only repository content, installed tools, and the user-supplied DuckDB JDBC JAR.

## Non-negotiable architecture

- Never make several OS processes write the same native DuckDB file.
- Give every completed import its own immutable DuckDB file. An importer owns its temporary file exclusively, closes it, then publishes it atomically. Analysis reads completed files only.
- If the application requires queries to see in-progress imports, updates to published imports, or one transaction spanning importers, stop: this design is unsuitable. Report that a single-writer service or another database is required.
- Historical Oracle data transfer is outside scope unless the user explicitly adds it.

Read [references/sharded-imports.md](references/sharded-imports.md) before designing file ownership, import publication, or cross-shard analysis.

## Phase 1: audit without editing

Inspect the repository before asking questions. Do not change application files in this phase, even when the initial request says to migrate.

1. Read repository instructions and identify the Java version, target OS/architectures, Maven/Tycho version, modules, bundles, features, products, launch configurations, and test commands.
2. Locate the binary decoder, database write path, analysis read path, connection factories/pools, transaction boundaries, schema creation/migrations, SQL resources, and configuration or secrets.
3. Search source and build metadata for Oracle dependencies and behavior. Include `oracle.jdbc`, `ojdbc`, JDBC URLs, driver class names, `VARCHAR2`, `NUMBER`, `RAW`, `BLOB`, `CLOB`, sequences, triggers, procedures, packages, synonyms, `DUAL`, `ROWNUM`, `NVL`, `DECODE`, `SYSDATE`, `SYSTIMESTAMP`, `MERGE`, `CONNECT BY`, `(+)`, `RETURNING INTO`, and Oracle exception handling.
4. Record every affected table and query, its callers, parameter/result Java types, ordering assumptions, null/empty-string behavior, generated-key behavior, expected volume, and existing test coverage.
5. Trace concurrency across processes and threads. Confirm that each importer can own a unique shard and that analysis needs completed imports only.
6. Locate the vendored DuckDB JDBC JAR. Record its version and checksum, inspect its manifest and contained native libraries, and verify that it supports every packaged OS/architecture. Do not download a dependency or silently choose a version.

For SQL and JDBC decisions, read [references/oracle-duckdb-mapping.md](references/oracle-duckdb-mapping.md). For bundle and product changes, read [references/eclipse-rcp-tycho.md](references/eclipse-rcp-tycho.md).

## Approval gate

Present a concise audit report before editing. It must contain:

- affected modules and persistence entry points;
- Oracle-to-DuckDB schema and query mapping, with uncertain semantics called out;
- the shard naming, location, import identity, publication, discovery, and retention design;
- the proposed vendored-JAR/OSGi packaging method;
- tests that establish import and analysis parity;
- blockers, especially stored database logic, unsupported native platforms, or live multi-process writes.

Ask the user to approve or correct this report. Do not start Phase 2 until they explicitly approve it. Approval covers only the reported migration; do not expand into historical data migration or unrelated refactoring.

## Phase 2: migrate the approved design

1. Add the JDBC JAR to the approved Tycho/OSGi packaging path and prove that the driver loads in an exported RCP product, not only in a unit-test classpath.
2. Introduce one application-owned connection boundary. Use `jdbc:duckdb:<absolute-path>` for persistent shards and load `org.duckdb.DuckDBDriver` explicitly when OSGi service discovery is unreliable.
3. Translate the schema and SQL from the approved mapping. Preserve precision, time semantics, ordering, empty-string behavior, keys, and transaction boundaries deliberately rather than by textual substitution.
4. Keep decoding separate from storage. Feed decoded records to the DuckDB writer using typed parameters. Use try-with-resources and rollback the import on any decode, validation, or database failure.
5. Implement the temporary-write, close, and publish lifecycle exactly as specified in the shard reference. Published shards are immutable.
6. Make analysis take a snapshot of completed shards, verify compatible schema versions, and query with `UNION ALL` unless existing behavior explicitly deduplicates. Open/attach shards read-only.
7. Remove Oracle dependencies, credentials, URLs, configuration, and dead compatibility code only after searches and tests show that no remaining component uses them.
8. Update operator-facing configuration and error messages for shard directory, unwritable paths, duplicate imports, incompatible schemas, corrupt shards, and publication failures.

Prefer the existing project structure and migration/test conventions. Do not introduce an ORM, service, or framework solely for this conversion.

## Verification and stopping conditions

Run the narrow tests during implementation, then the repository's offline full build and product-level smoke test. At minimum verify:

- a representative binary fixture decodes to expected row counts and values;
- nulls, empty strings, numeric boundaries, timestamps/time zones, binary values, generated identifiers, and duplicate-import behavior match the approved semantics;
- an import failure never produces a discoverable shard;
- concurrent importer processes publish different files without sharing a write connection;
- analysis ignores temporary files, rejects incompatible schemas, and returns the expected cross-shard result and order;
- the packaged RCP application loads the JDBC driver with no network access;
- no Oracle driver, URL, credential, import, or executable Oracle SQL remains in the migrated path;
- `mvn -o verify` (or the repository's equivalent offline command) succeeds.

Do not weaken assertions or silently change expected results to make tests pass. Stop and report evidence when source behavior is ambiguous, the JDBC artifact is missing/incompatible, atomic publication cannot be guaranteed, or parity cannot be demonstrated.
