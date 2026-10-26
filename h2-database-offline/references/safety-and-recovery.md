# Existing database safety, upgrade, and recovery

Read this reference before opening, copying, upgrading, or recovering an existing H2 database.

## Establish a safe working copy

1. Resolve the exact database path and enumerate its related files without changing them.
2. Identify the engine version that last wrote the database using project artifacts, logs, manifests, or supplied provenance. Do not probe the only copy with assorted H2 versions.
3. Determine whether an application, console, test runner, or H2 server has the database open. Stop cleanly through the owning application when authorized.
4. Prefer a logical SQL script or an H2-supported consistent backup created by the matching old engine. If a file-level copy is necessary, first shut down every user cleanly and copy the complete related file set to a new restricted directory.
5. Record hashes, sizes, timestamps, source version, and the exact commands used. Protect the untouched source copy from writes.
6. Perform every import, upgrade, or recovery attempt on another copy or into a new target path.

A filesystem copy taken while MVStore is active may be inconsistent even when the main file looks complete. Copying only the obvious `.mv.db` file can also discard useful diagnostics or related artifacts. Never call a copy a backup until a restore into an isolated target has succeeded.

## Upgrade path

For major-version transitions, especially H2 1.4.x to 2.x, prefer logical migration:

1. With the old matching H2 engine, export the database to a logical SQL script using the locally documented `Script` tool or SQL command.
2. Inspect the script as sensitive, untrusted input. Keep it outside source control and do not execute Java aliases or unexpected initialization code blindly.
3. Create a new empty database with the target H2 engine at a different path.
4. Import using the target version's locally documented `RunScript` workflow.
5. Run migrations needed by the application, then validate schemas, constraints, indexes, sequences/identities, row counts, representative queries, and application startup.
6. Test a second clean export/import or other restore procedure before accepting the new database.

Do not rely on a newer engine opening and rewriting an older file in place. Do not overwrite or rename the original into the target location until validation is complete and the user has authorized the cutover.

## Recovery

Recovery is a last resort after normal open and restore paths fail. Preserve the original and work on a duplicate. Use only the `Recover` capability supplied by the matching local H2 version, following its own `-help` output. Recovery output may include credentials, literals, and customer data; keep it access-restricted and sanitize excerpts.

After recovery, import into a fresh database rather than treating recovered artifacts as a repaired live database. Validate more than row counts: check referential integrity, unique constraints, indexes, LOB accessibility, identities/sequences, application invariants, and representative reads and writes. Clearly report missing or damaged objects and never imply that successful import proves full recovery.

## Mutating operations

Writing migrations or configuration files is different from applying them to valuable data. Before executing DDL, DML, migration, compact, shutdown, restore, or conversion against an existing database:

- confirm that execution—not only code preparation—is requested;
- show the sanitized target and expected scope;
- ensure rollback or restore is possible;
- use a transaction when the installed H2 behavior and operation support it;
- stop on the first unexpected result rather than retrying destructive steps;
- capture only sanitized diagnostics.

Never directly modify `.mv.db`, `.trace.db`, or lock files. Never use lock-file deletion, hex editing, or repeated opening with different engines as a recovery strategy.
