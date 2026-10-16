# Getting useful inputs without sharing a login

## Minimum for a first pass

- Oracle major version (for example 19c) and the exact schema(s) to review.
- A locally exported, **metadata-only** DDL file for tables, primary/foreign/unique constraints, and indexes. Include relevant views, triggers, sequences, and PL/SQL when those are part of the question. Keep object owner names or replace them consistently with aliases so cross-schema links remain understandable.
- What you want to learn: schema map, maintainability, suspected bug, or slow query. If you have no specific question, start with a schema inventory and high-confidence design risks.

For performance questions, additionally provide sanitized SQL text, the plan obtained for **that query and execution** when possible, rough table/row counts, bind data types and whether values are common/rare (not real values), observed timing and expected timing, and which environment produced the measurements. Explain whether plan row counts are estimates or actuals. Do not run heavy queries just to gather these inputs.

## Export safely

Use a **locally installed** database tool and an authorized account to export DDL/metadata only. For example, in Oracle SQL Developer use its database export workflow, select only the necessary schemas/objects, enable DDL, and **disable data export**. Names and UI options depend on the installed tool/version; review its local help or ask your DBA. Alternatively ask the DBA for schema DDL exported with their established process. Do not hand the AI a privileged database login or let it run metadata-extraction SQL against production.

The exported DDL can still contain sensitive content: comments, view definitions, PL/SQL literals, default values, test/example rows in INSERT statements, hostnames, links, encryption keys, and tokens. Check it locally and remove or replace these before analysis. Preserve datatype, constraints, index columns/order and meaningful SQL structure while redacting. Put files in a private project folder or temporary folder **outside the public skills Git repository**; don't commit exports, plans, logs, or credential files. If you need to share a query, mask customer identifiers, literal values, and connection information. Keep a private original for comparison.

Suggested local layout (optional; these are **user-provided** files, not part of this skill):

```text
private-oracle-review/
  schema/            # sanitized metadata-only .sql files
  queries/           # sanitized .sql files for specific slow queries
  plans/             # corresponding redacted plan text, if available
  context.md         # version, symptoms, volume estimates, environment
```

Do not mistake an offline DDL export for a current, complete snapshot: request export date, missing schemas, and whether the database was changing during export. If sharing any export is not permitted, the user can describe a small anonymized table/query example instead, and the analysis must be labeled limited.
