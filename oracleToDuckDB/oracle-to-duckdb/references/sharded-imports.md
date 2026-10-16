# Immutable per-import shard architecture

Use this architecture when several Eclipse RCP processes may import simultaneously. DuckDB concurrency within one process does not make one native database file a safe drop-in multi-process Oracle server.

## Ownership and lifecycle

One import process exclusively owns one new shard. It must never open another process's shard for writing.

1. Resolve a configured shard directory and verify it is writable. Use a stable import identity from existing domain data when available; otherwise define a collision-resistant ID during the audit.
2. Create the working database in the final directory with a non-discoverable name such as `<import-id>.<uuid>.duckdb.tmp`. The temporary and final paths must be on the same filesystem.
3. Open the temporary file read-write. In one explicit transaction, create or migrate its schema, record the approved schema version/import metadata, decode the binary input, insert typed rows, and run integrity checks.
4. Commit only after the complete import validates. On failure, rollback, close every JDBC resource, and delete or quarantine the temporary file according to the approved retention policy. Never give it the completed suffix.
5. Close all connections and release the database before publication.
6. Publish with `Files.move(temp, final, ATOMIC_MOVE)` to a unique final name ending in `.duckdb`. Do not overwrite an existing completed shard. If atomic move is unsupported, leave the temporary file undiscoverable and report failure; use a readiness-marker protocol only if separately designed, tested, and approved for that filesystem.
7. Treat the final file as immutable. A correction produces a new shard or follows an explicitly designed replacement workflow while no reader can observe ambiguity.

Sanitize file-name components, keep the authoritative import identity inside the database, and do not infer trust from a filename. Decide duplicate-input behavior in the audit: reject, return the existing result, or publish a new version. Preserve the application's existing business rule.

Atomic rename and locking semantics can be unreliable on some network or synchronized filesystems. Test the actual deployment filesystem from separate processes. If it cannot guarantee publication visibility and immutable reads, stop and recommend a single-writer service or a supported staging/copy protocol rather than claiming safety.

## Shard contract

Every shard must contain the same approved analytical schema and a small metadata record sufficient to validate it before querying. Reuse an existing migration/version convention when present; otherwise propose the metadata table and columns in the audit rather than inventing them during implementation. At minimum the reader needs schema version, import identity, and completion provenance required by the application.

Do not place secrets, machine-specific absolute source paths, or unbounded decoder diagnostics in shard metadata. If source-file hashes are used for deduplication, define the algorithm and how sensitive inputs are handled.

## Analysis

1. Snapshot the directory listing at the start of an analysis operation. Accept only regular completed `.duckdb` files; ignore `.tmp`, failed, quarantine, and unrelated files.
2. Normalize and validate paths under the configured shard directory. Generate internal attachment aliases such as `shard_0001`; never derive SQL identifiers directly from filenames.
3. Open each shard read-only or attach it with read-only semantics supported by the vendored driver. Verify schema version and required tables/columns before including it.
4. Combine rows with `UNION ALL` by default. Use `UNION` or application-side deduplication only when the Oracle behavior actually removed duplicates.
5. Preserve deterministic ordering explicitly. Directory order, insertion order, and an unordered SQL result are not contracts.
6. Close result sets, statements, attachments, and connections promptly so retention or cleanup can proceed.

If a query must span many shards, measure attachment/startup cost and limits with realistic data. A later compaction job may read completed shards and publish a new immutable aggregate shard, but it must be a single writer and needs rules preventing double counting. Do not add compaction unless the audit shows it is necessary and the user approves it.

## Failure and concurrency tests

- Start two importer processes with different inputs and prove their temporary and final paths cannot collide.
- Kill or fault an importer during decode, insert, validation, commit, and pre-publication close; no partial file may be discoverable.
- Start analysis while another import is active; it must see the previous completed snapshot, never the temporary shard.
- Publish during analysis; the running analysis keeps its initial snapshot, and a later analysis sees the new shard.
- Attempt a duplicate import and verify the approved rule.
- Supply a corrupt or incompatible completed file; isolate it and report a useful error without silently returning partial results unless partial analysis was explicitly approved.
- Exercise the real deployment filesystem from separate processes, including atomic-move failure and file-handle cleanup.
