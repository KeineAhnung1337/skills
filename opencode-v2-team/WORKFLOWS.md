# Coding workflows and offline skill integration

The team configuration includes five commands. They execute as prompts in the current `gatekeeper` session; the lead can delegate through the actual subagent tool. Command arguments are prompt text, with no automatic shell interpolation.

| Command | Example | Outcome |
| --- | --- | --- |
| `/bootstrap` | `/bootstrap focus on the desktop application` | Inspect real project facts and merge concise, accurate `AGENTS.md` guidance |
| `/fix` | `/fix importing the same backup twice creates duplicates` | Reproduce, trace the cause, implement a bounded fix, add a regression check, and review |
| `/feature` | `/feature add cancellation to the import job` | Define observable acceptance criteria, follow existing patterns, implement, test, and review |
| `/review` | `/review current staged changes` | Inspect the requested changes, affected callers, and relevant tests without modifying files |
| `/verify` | `/verify the changed import module` | Run appropriate discovered checks and report actual results without repairing source |

Run `/bootstrap` in a new target-project session first. It discovers commands from project instructions, manifests, CI, and existing scripts. It does not install dependencies, change production code, or run every expensive suite. If the project already has `AGENTS.md`, it preserves and merges its guidance. The workflow reports missing evidence rather than inventing executable commands.

`/fix` and `/feature` select only useful specialists. Writers receive explicit file ownership and run sequentially when scopes overlap. `/review` has the lead gather the diff and pass it to read-only specialists, whose shell access remains denied. `/verify` runs check-only options and records real command results; it reports failures without changing source or updating snapshots.

These are reusable instructions and agent-selection settings, not a deterministic workflow engine. An agent can fail to follow them. The permission rules enforce the configured specialist tool restrictions; review and verification must still be assessed against actual tool results. No workflow automatically commits or pushes.

## Approved offline skills

`skills.json` records the exact IDs and checkout-relative directories. OpenCode derives IDs from directory names rather than the frontmatter display name. In particular, the Eclipse skill's ID is `eclipse-rcp`, the QF-Test skill's ID is `qftest`, and the migration skill is `oracle-to-duckdb` under `oracleToDuckDB/oracle-to-duckdb`.

All nine team roles can load these eight skills when relevant:

- `eclipse-rcp`
- `h2-database-offline`
- `install4j-offline`
- `oracle-db-offline`
- `oracle-to-duckdb`
- `osgi-offline`
- `powershell-offline`
- `qftest`

Agents receive permission to read each skill's reference directory. The config denies edits addressed through those library paths and does not give read-only roles shell access. Shell-capable agents still act with host authority, so these rules are not a filesystem sandbox. The agents are instructed to treat the library as reference material. Additional local SDK/JAR/cache paths may need narrowly scoped external-read rules after `/bootstrap` identifies them; the setup does not grant specialists unrestricted external access.

Skills are loaded on demand. The main agent does not copy entire manuals into child prompts; it supplies the relevant skill ID, task facts, and source references so the child can load what it needs. Existing offline, version, and data-handling instructions in each skill continue to apply. The same Qwen routes and disabled web tools remain in use.

## Target installation

Use Python 3.9 or newer and the full skills repository checkout on the target; a copy of only `opencode-v2-team/` lacks the reference library. From the checkout root:

```bash
python3 opencode-v2-team/install.py --check
python3 opencode-v2-team/install.py --output /tmp/opencode-team-preview.jsonc
python3 opencode-v2-team/verify_setup.py --config /tmp/opencode-team-preview.jsonc
```

The installer derives the skills directory from its own checkout and checks every approved entry point. The preview contains absolute paths for that target and keeps the API key as `{env:LLM_API_KEY_BOSYS}`. It does not read the key, fetch packages, call a model, or modify project instructions.

On Linux/macOS, install globally with:

```bash
python3 opencode-v2-team/install.py --output ~/.config/opencode/opencode.jsonc
```

If that file already exists and you want to replace it with the full team configuration, add `--replace`. This makes a timestamped backup first. The installer does not merge settings: compare the preview and preserve additional machine-specific settings before replacement. If an alternate `opencode.json` already exists, use that path instead so two competing configs are not created. On Windows, pass the actual global config path for your installation, or choose the target project's `opencode.jsonc` explicitly.

The source `opencode.jsonc` is a portable template containing `{env:OPENCODE_SKILLS_DIR}`. Rendering is recommended: the installed config then needs no extra path environment variable, and moving the checkout simply requires rendering again. Never install a config rendered on another PC without updating its paths.

After reloading OpenCode and starting a new session, confirm that the commands are listed. Ask `explorer` to load one relevant skill, read its required local index/workflow, and summarize one reference with a file path. Confirm that a child actually runs and that no denied access is silently ignored. Then try `/bootstrap` followed by one small `/fix` or `/feature`, ending with `/review` and `/verify`. The live gateway probe in `EVALUATION.md` is still a separate check of the direct API path.

The command format follows the official [v2 commands documentation](https://opencode.ai/v2/docs/commands); discovery and IDs follow [skills](https://opencode.ai/v2/docs/skills), and tool access follows [permissions](https://opencode.ai/v2/docs/permissions).
