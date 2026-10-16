# Offline Oracle database analysis skill

Copy this directory to `.opencode/skills/oracle-db-offline/` in your private project or `~/.config/opencode/skills/oracle-db-offline/` globally. Load with `@oracle-db-offline`. Keep `references/` together with `SKILL.md`.

**No Oracle login is required.** For a first pass, provide Oracle version, schema name(s), a sanitized **metadata-only** DDL export, and your analysis goal. Optionally include sanitized slow SQL and matching execution plans. See `references/inputs.md` for what to export and how to handle sensitive contents. Put exports somewhere private, **not in this public skills repository**.

This initial skill does not connect to Oracle, execute SQL, create accounts, export data, change schema, or include Oracle client/driver or documentation. It cannot prove performance or data quality from DDL alone. If live checks become necessary later, design a separate explicitly approved workflow using a narrowly scoped account and a non-production environment first.

A local model provider is needed if the entire AI session must remain offline; the skill's instructions alone do not make a cloud AI model local.
