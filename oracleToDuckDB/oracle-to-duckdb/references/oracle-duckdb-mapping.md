# Oracle-to-DuckDB mapping guide

Use this during the audit and migration of JDBC schema, bind values, result reads, and SQL. It is a decision guide, not a blind replacement table: derive each mapping from declared Oracle metadata, Java types, representative values, and required semantics.

## Data types and values

| Oracle construct | DuckDB candidate | Required check |
| --- | --- | --- |
| `NUMBER(p,0)` | `SMALLINT`, `INTEGER`, `BIGINT`, `HUGEINT`, or `DECIMAL(p,0)` | Choose from the full allowed/observed range, not sample convenience. Preserve identifiers exactly. |
| `NUMBER(p,s)` | `DECIMAL(p,s)` | Check rounding, overflow, negative scale, and Java `BigDecimal` usage. |
| unconstrained `NUMBER` | Usually an explicit `DECIMAL`; sometimes `DOUBLE` | Infer domain requirements. Never choose floating point for exact identifiers or money. |
| `BINARY_FLOAT` / `BINARY_DOUBLE` | `FLOAT` / `DOUBLE` | Test NaN, infinities, and comparison/aggregation behavior if present. |
| `VARCHAR2`, `NVARCHAR2` | `VARCHAR` | Oracle treats zero-length strings as `NULL`; DuckDB does not. Normalize deliberately at writes or in affected predicates. |
| `CHAR`, `NCHAR` | `VARCHAR` or fixed-width-compatible logic | Test trailing-space comparison and padding; do not assume it is irrelevant. |
| `DATE` | Usually `TIMESTAMP` | Oracle `DATE` contains date and time to seconds. Use DuckDB `DATE` only when time is intentionally discarded. |
| `TIMESTAMP` | `TIMESTAMP` | Check precision and Java conversion. |
| `TIMESTAMP WITH TIME ZONE` | `TIMESTAMPTZ` or an instant plus zone column | Verify whether the original zone/offset must be reproduced; storing the instant alone can lose it. |
| `RAW`, `LONG RAW`, `BLOB` | `BLOB` | Use `setBytes`, binary streams, or the proven project equivalent; compare bytes in tests. |
| `CLOB`, `NCLOB`, `LONG` | `VARCHAR` | Check size, encoding, streaming, and memory behavior with realistic inputs. |
| `XMLTYPE`, object, collection, spatial types | No automatic mapping | Model explicitly or stop for a domain decision. |

Also inspect column defaults, `NOT NULL`, primary/foreign/unique/check constraints, indexes, comments used by tooling, and identifier quoting. Do not carry over Oracle tablespaces, storage clauses, database links, grants, synonyms, or partition syntax as if DuckDB implemented the same operational model.

## SQL rewrites

- Remove `FROM DUAL` where the expression can be selected directly.
- Replace `NVL(a,b)` with `COALESCE(a,b)` only after checking implicit type conversion.
- Rewrite Oracle SQL `DECODE(...)` as a searched or simple `CASE`. Do not confuse it with the application's binary decoder.
- Replace `ROWNUM` pagination with deterministic `ORDER BY` plus `LIMIT`/`OFFSET`, or use `row_number()` when row numbering is part of the result. A limit without a stable order does not preserve result identity.
- Rewrite legacy `(+)` joins as explicit ANSI joins and test null-producing rows.
- Map `MINUS` to `EXCEPT` only after checking duplicate semantics.
- Evaluate `LISTAGG` uses individually and map to `string_agg` with explicit ordering and null handling.
- Rewrite `CONNECT BY` as a recursive CTE and test roots, cycles, depth, sibling ordering, and duplicate paths.
- Treat `MERGE`, `RETURNING`, upsert syntax, and generated-key retrieval as version- and driver-sensitive. Verify them against the vendored JDBC JAR; otherwise use a transactionally equivalent explicit sequence.
- Translate `SYSDATE`, `SYSTIMESTAMP`, `CURRENT_DATE`, date arithmetic, `TRUNC`, `TO_DATE`, and `TO_CHAR` from their intended time zone and formatting semantics. Do not substitute names alone.
- Replace Oracle sequence expressions with an approved DuckDB sequence or application-assigned identifier. Preserve allocation, retry, and uniqueness behavior; test JDBC key retrieval.
- Rewrite PL/SQL blocks, packages, stored procedures, and database-side business triggers into explicit Java or schema behavior. Stop for approval when their business meaning is unclear.
- Remove Oracle optimizer hints only after documenting whether they encode correctness assumptions such as ordering or join shape.

Search dynamic SQL construction as well as `.sql` files. Parameterize values; never repair translated SQL by concatenating decoded data or paths.

## JDBC boundary

- Centralize connection creation so tests can identify every database file and access mode.
- Use absolute normalized paths from application configuration. Do not embed credentials in the replacement URL; DuckDB does not need Oracle-style usernames/passwords for a local file.
- Explicitly load `org.duckdb.DuckDBDriver` if OSGi prevents JDBC service-provider discovery.
- Bind values with types that match the approved schema, especially `BigDecimal`, timestamps, nulls, and blobs. Review `getObject` casts that depended on Oracle classes.
- Replace Oracle-specific APIs, array/struct types, LOB helpers, exception codes, connection unwrapping, and session statements. Do not catch generic errors and pretend Oracle recovery behavior still applies.
- Use try-with-resources for connections, statements, and result sets. Bound the import with an explicit transaction; rollback on decode, insert, validation, or publication preparation failure.
- Prepared batches are the portable baseline. For large imports, benchmark and consider DuckDB's appender only after proving identical null/type/transaction behavior with the exact vendored driver.
- Do not copy Oracle pool sizing into an embedded database. Multiple connections in one JVM may share an instance, but all writes for one shard must remain in its owning process and follow the application's transaction design.

## Semantic parity checklist

For every migrated query, capture its caller and assert the behavior that matters: selected values, duplicates, nulls, order, numeric scale, timestamps, aggregates, and empty result handling. Compare representative Oracle baseline results when available, but normalize only differences that the audit explicitly approved. A passing row count alone is not parity.
