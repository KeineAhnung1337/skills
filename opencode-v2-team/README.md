# OpenCode v2 coding team

This configuration adapts your supplied `bosys` setup into one coding lead and eight selectable specialists. It is prepared for your target system; it has not been installed there or tested against your gateway.

| Agent | Route / effort | Assignment |
| --- | --- | --- |
| gatekeeper (primary) | bosys_xhigh_reason / xhigh | Planning, delegation, integration, final verification |
| explorer | bosys_low_reason / low | Locate code paths, conventions, and existing tests |
| debugger | bosys_xhigh_reason / xhigh | Investigate root causes and discriminating regression cases |
| implementer | bosys_reason / medium | Implement a bounded production change |
| test-writer | bosys_reason / medium | Write behavioral and regression tests |
| reviewer | bosys_xhigh_reason / xhigh | Check correctness and regressions |
| security-reviewer | bosys_xhigh_reason / xhigh | Trace concrete trust-boundary risks |
| janitor | bosys_non_reason / thinking disabled by request | Mechanical formatting and import cleanup |
| scribe | bosys_low_reason / low | Maintain documentation and docstrings |

All agents still use your Qwen deployment. Different roles and effort requests do not turn it into a larger or more capable base model. This setup conserves cloud usage if the gateway routes all four aliases locally; local inference, retries, and coordination still consume tokens and time. Eight roles do not imply eight simultaneous requests.

## Install on the target

1. Use the full skills repository checkout on the target so the offline reference files are available.
2. Run `python3 opencode-v2-team/install.py --check` from its root, then render a preview with `python3 opencode-v2-team/install.py --output /tmp/opencode-team-preview.jsonc`. The installer resolves the checkout's absolute skill paths and retains the API-key environment reference.
3. Install with `python3 opencode-v2-team/install.py --output ~/.config/opencode/opencode.jsonc` on Linux/macOS, or choose the actual target config path. An existing output requires `--replace`, which saves a timestamped backup and replaces the full config without merging. Compare the preview and retain any additional machine-specific settings first. If `opencode.json` already exists at that location, select that path instead of creating a conflicting JSONC config. See `WORKFLOWS.md` for details.
4. Keep `LLM_API_KEY_BOSYS` configured in the environment of the OpenCode server process. The existing endpoint `https://chat/litellm/v1` must resolve from that system.
5. Reload the server/configuration and start a fresh session. Confirm `gatekeeper` and `bosys/bosys_xhigh_reason#xhigh` are selected; an existing session can retain its previous model independently of the selected agent.
6. Ask the lead to use `explorer` to locate a known function and load a relevant offline skill. Confirm a child session runs on the low route and can read the skill's references.
7. Run `/bootstrap` in the target project to discover real commands and merge concise `AGENTS.md` guidance. The original `templates/AGENTS.md.template` remains available for manual setup; do not copy unresolved placeholders as project facts.
8. Try `/fix`, `/feature`, `/review`, and `/verify`. Follow `EVALUATION.md` for gateway probes and a comparison of real coding tasks. The workflow definitions are already embedded in the config; helper documents and test fixtures do not need to be added to session instructions.

Example task:

> Fix the failing login test. Use explorer only if needed to locate the flow, debugger for the root cause, implementer for the bounded fix, test-writer for the regression case, and reviewer for the final diff. Choose only useful specialists, keep writers sequential, and report the checks actually run.

The default instructions start with one active worker and permit up to two independent readers. This is a prompt-level coordination policy, not an enforced concurrency setting. No worker may launch more workers. File ownership for writers is also an instruction; write-capable roles have project edit access and must receive explicit assignments.

The eight existing offline skills are registered for on-demand loading, with explicit skill-ID permissions and external-reference paths. The portable source config uses `{env:OPENCODE_SKILLS_DIR}`; prefer the installer so no extra environment variable is needed in the rendered config. See `WORKFLOWS.md` for the skill list, command behavior, and installation smoke test.

## Corrections from the supplied config

- Model references use `provider/model#variant`, e.g. `bosys/bosys_xhigh_reason#xhigh`. The previous `bosys/bosys#bosys_xhigh_reason` pointed to an undefined model and variant.
- The lead invokes the actual `subagent` tool. Printing an `@` mention or a model name is not a programmatic handoff.
- New v2 fields are `agents.*.system`, `permissions`, `shell`, `subagent`, and `plugins`. Legacy `prompt`, `tools`, `permission`, and `plugin` entries are replaced.
- The provider uses the documented v2 OpenAI-compatible runtime package. Model aliases, endpoint, API-key variable, priority, declared capabilities, and model limits come from your config. Sampling is updated to Qwen's published thinking/non-thinking defaults.
- Raw sampling and `reasoning_effort` parameters are expressed in provider/model/variant `body` fields, so they are JSON request fields rather than potentially ignored SDK options. Body fields merge from provider to model to variant.
- Thinking routes request `chat_template_kwargs.enable_thinking: true` and `preserve_thinking: true`. The non-reasoning alias overrides `enable_thinking` to `false`. These are backend-facing controls, not a guarantee that the gateway forwards and honors them.
- Thinking sampling is temperature 1.0, top_p 0.95, top_k 20, min_p 0.0, presence_penalty 0.0, repetition_penalty 1.0. The non-thinking route overrides temperature to 0.7, top_p to 0.80, and presence_penalty to 1.5. Other shared sampling values remain the same.
- `buffer` is `"10%"`. A fractional value of `0.10` is not the v2 percentage format. Compaction retention is raised to 8,000 recent tokens; the lead is instructed to summarize requirements and decisions compactly.
- The lead establishes acceptance criteria, reproduces bugs before fixes when feasible, verifies real repository commands, and explicitly reports incomplete work or unrun checks. Test writing includes a before/after regression check where practical.
- `disabled_providers` becomes a provider-use policy, preserving the supplied restriction on `opencode`. Web fetch and web search remain disabled.
- The main config's `cli.session.tps` block is omitted because it is absent from the current v2 core schema. The TPS plugin declaration is retained under `plugins`; its v2 compatibility and any CLI-specific options need checking on your target. If it blocks startup, remove that plugin entry and reintroduce a compatible version separately.

## Verify thinking behavior

The gateway's route names and model labels do not prove that Qwen uses different thinking budgets. Qwen3.8 officially supports `low`, `medium`, and `xhigh`; verify in LiteLLM/backend logs that they arrive and affect generation. The gateway must also support the explicit thinking flags and sampling fields. If a route rejects a parameter, configure its equivalent on the backend or remove the unsupported request field, then verify behavior. Do not treat a successful response as evidence that a parameter was honored. See `EVALUATION.md` for the direct tool-call probe and the separate OpenCode child-session check.

Test on one real coding bug with a known regression case. Compare completion quality, test results, total generated tokens, and elapsed time. The lead and reviewers share a base model, so agreement alone is weak evidence; reproduction and tests matter more. Keep high effort for the lead and difficult analysis, use low for retrieval and documentation, and avoid delegating short tasks whose coordination costs more than doing them directly.

Your declared model context/output limits remain unchanged. A short final-answer instruction does not reduce the available internal reasoning budget, and output limits should be changed only after observing truncation and confirming server support.

## Sources

Configuration follows the official [v2 agent format](https://opencode.ai/v2/docs/agents), [provider setup](https://opencode.ai/v2/docs/providers), [model variants](https://opencode.ai/v2/docs/models), [permissions](https://opencode.ai/v2/docs/permissions), [commands](https://opencode.ai/v2/docs/commands), [skills](https://opencode.ai/v2/docs/skills), and [configuration format](https://opencode.ai/v2/docs/config). The [live JSON schema](https://opencode.ai/config.json) supplies field definitions. Sampling and thinking controls follow the [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B); project guidance and context retention follow the [instructions](https://opencode.ai/v2/docs/instructions) and [compaction](https://opencode.ai/v2/docs/compaction) documentation. Network behavior and TPS-plugin compatibility have not been verified on your target system.
