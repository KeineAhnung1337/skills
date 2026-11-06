# Verify the setup and measure code quality

## Offline check

Run from this package directory:

```bash
python3 verify_setup.py
```

This checks strict JSON syntax, agent/model references, delegation, and the intended edit restrictions. It is not full OpenCode schema validation or proof of runtime behavior. The prepared `.jsonc` uses strict JSON so Python needs no extra dependencies. After adding JSONC comments, use a JSONC-aware parser or keep a strict-JSON copy for this script.

## Gateway tool-call probe

Run on the target system where the existing API key is available to the process. No repository files, source code, credentials, or reasoning text are printed by the probe. Only synthetic messages are sent to the configured gateway; returned reasoning fields are forwarded on the tool-call follow-up to check protocol compatibility.

Start with one route:

```bash
python3 verify_setup.py --live --model bosys/bosys_low_reason#low
```

Then check all four distinct routes used by the team:

```bash
python3 verify_setup.py --live
```

Each selected route makes two inference requests and consumes gateway/model tokens. The probe validates a structured tool call, its arguments and ID, and a follow-up using the actual synthetic tool result. It never runs a model-selected command or accesses project files. Output includes elapsed time, token usage when returned, and whether a reasoning field was observed, without revealing its contents. The default per-request timeout is 45 seconds and the output cap is 4,096 tokens. If high-effort probes hit the cap, retry only that route with `--max-tokens 8192` or `--max-tokens 16384`, within your server's limits; a truncated probe is incomplete, not proof of a broken model.

A pass checks a direct LiteLLM conversation. It does not prove that OpenCode preserves reasoning, uses the same request body, or selects the expected child model. Verify the actual OpenCode path in a fresh session:

> Use explorer to find a known function in this repository. Then send a follow-up to that same child asking it to inspect one caller. Return both file references and any unresolved questions. Make no changes.

Inspect OpenCode's child activity and gateway/backend logs for the route, `reasoning_effort`, sampling, thinking flags, tool calls, and follow-up. Compare low/medium/xhigh on the same small task. Their token counts may differ, but a difference alone does not prove the controls are honored. Confirm backend interpretation. The non-thinking route should suppress thinking because its request includes `chat_template_kwargs.enable_thinking: false`; an absent reasoning field by itself is insufficient evidence.

The explicit `chat_template_kwargs`, `min_p`, `top_k`, and `repetition_penalty` fields require backend support. If the proxy rejects them, configure equivalent values on its backend or remove unsupported request fields. Do not simply ignore the errors or silently route to a cloud model. Keep the existing priority fields only if your gateway supports them.

## Five representative coding tasks

Choose real tasks from your repository. Keep task descriptions and expected behavior fixed across configuration comparisons. Use a clean branch/worktree or your normal isolated checkout for each run and preserve any pre-existing user work. Use the same starting commit, dependencies, test environment, and task prompt. Save the starting revision with the results.

| Case | Choose a real task | Acceptance evidence |
| --- | --- | --- |
| Regression | A known reproducible bug | Focused check fails before the fix and passes afterward |
| Feature | A small behavior with clear requirements | Normal, boundary, and failure-path checks pass |
| Refactor | Restructure a bounded module | Existing behavior and public API remain covered and passing |
| Integration | A bug involving two modules or a data boundary | Integration reproduction passes; affected existing tests remain passing |
| Maintenance | A mechanical change plus a documentation update | Targeted formatter/checks pass; diff preserves behavior and docs match code |

Record one row per run in `evaluation-results.csv`. Leave unavailable metrics empty rather than inventing measurements. Include all child sessions, retries, follow-ups, and compaction when measuring total tokens/time. Generated-token count is the gateway's reported total; do not add reasoning-token subtotals again when already included in completion usage. TPS alone is insufficient: fast output that fails acceptance checks is not a completed task.

Compare the present config with one changed setting at a time. Repeat promising candidates on more than one task/run because sampling introduces variation. Prefer configurations that satisfy more acceptance checks with fewer regressions; compare total tokens and completion time among similarly correct results. Have someone other than the implementing agent inspect the final patch where possible. Multiple roles sharing Qwen provide additional perspectives, not independent correctness evidence.

## Output and context limits

The configuration retains your declared 117,760-token context and 16,384-token output limits. A client declaration does not enlarge the serving engine's limits. Look for `finish_reason: length`, unfinished tool arguments, incomplete patches, or explicit agent step-budget exhaustion. Increase the affected limit only when the backend supports it and a real task demonstrates truncation; do not raise every route to the model card's maximum.

Compaction now retains approximately 8,000 recent tokens. Increase toward 12,000 if long tasks repeatedly lose exact requirements or recent decisions, while keeping short durable summaries. Start a fresh session for unrelated tasks. Keep agents' tool output and final summaries focused so fixed instructions and logs do not crowd out useful code.
