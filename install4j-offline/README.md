# install4j offline skill

Copy this directory to `.opencode/skills/install4j-offline/` in your installer project or `~/.config/opencode/skills/install4j-offline/` for global use; invoke `@install4j-offline`. Keep the `references/` directory alongside `SKILL.md`.

This is a workflow/safety guide, **not** a bundled install4j schema or manual. For accurate `.install4j` editing without network access, open your installed install4j IDE and select **Install AI Skill** in its toolbar. Choose OpenCode (or Generic AI agent) and install at project or global scope. The vendor skill is generated from your installed version and includes the matching schema, bean catalog, samples, API and docs. It typically installs into `.agents/skills/` or `~/.agents/skills/` and can coexist with `install4j-offline`. Regenerate it after an install4j upgrade, and use its pinned compiler path with the matching local project. If that IDE action is unavailable in your version, use the locally installed help/IDE-generated sample project instead.

No install4j application, schema, documentation, license, installer project, or build payload is bundled here. You need an appropriately licensed local install4j and all build inputs for compilation; runtime verification needs a disposable test machine for each supported platform. A local model provider is also required for a fully offline AI session.

Source for setup and CLI guidance (provenance only; **not** needed when running this skill offline): ej-technologies install4j help, `concepts/aiAgentSkill.html`, `concepts/projects.html`, `concepts/build.html`, `cli/compiler.html`, and `installers/options.html` under `https://www.ej-technologies.com/resources/install4j/help/doc/`. Always defer to the installed version's documentation.
