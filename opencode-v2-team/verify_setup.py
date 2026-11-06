#!/usr/bin/env python3
"""Validate the prepared config; optionally probe synthetic tool calls on LiteLLM."""

import argparse
import copy
import fnmatch
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request


class ProbeError(Exception):
    pass


def merge(left, right):
    result = copy.deepcopy(left)
    for key, value in right.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def permission(config, agent, action, resource):
    effect = "ask"
    rules = config.get("permissions", []) + agent.get("permissions", [])
    for rule in rules:
        if fnmatch.fnmatchcase(action, rule["action"]) and fnmatch.fnmatchcase(
            resource, rule["resource"]
        ):
            effect = rule["effect"]
    return effect


def model_ref(config, ref):
    provider_id, rest = ref.split("/", 1)
    model_id, separator, variant_id = rest.partition("#")
    provider = config["providers"][provider_id]
    model = provider["models"][model_id]
    variant = {}
    if separator:
        variant = next(v for v in model.get("variants", []) if v["id"] == variant_id)
    body = merge(merge(provider.get("body", {}), model.get("body", {})), variant.get("body", {}))
    return provider, model.get("modelID", model_id), body


def validate(config):
    """Check routing and permission invariants, not the entire OpenCode schema."""
    agents = config["agents"]
    lead = agents[config["default_agent"]]
    if lead.get("mode") != "primary":
        raise ProbeError("The default agent must be primary.")
    workers = {name: a for name, a in agents.items() if a.get("mode") == "subagent"}
    if len(workers) < 8:
        raise ProbeError("Expected at least eight specialist subagents.")
    for name, agent in agents.items():
        model_ref(config, agent["model"])
        if not agent.get("system"):
            raise ProbeError(f"Missing system instructions: {name}")
        if {"prompt", "tools", "permission", "maxSteps"}.intersection(agent):
            raise ProbeError(f"Legacy v1 agent fields: {name}")
        if "steps" in agent and (type(agent["steps"]) is not int or agent["steps"] < 1):
            raise ProbeError(f"Invalid step budget: {name}")
    for name, agent in workers.items():
        if permission(config, lead, "subagent", name) != "allow":
            raise ProbeError(f"Lead cannot launch {name}.")
        if any(permission(config, agent, "subagent", child) != "deny" for child in workers):
            raise ProbeError(f"Recursive delegation is enabled for {name}.")
    for name in ("explorer", "debugger", "reviewer", "security-reviewer"):
        agent = workers[name]
        if permission(config, agent, "edit", "src/example.py") != "deny":
            raise ProbeError(f"Expected edits to be denied for {name}.")
        if permission(config, agent, "shell", "touch example") != "deny":
            raise ProbeError(f"Expected shell access to be denied for {name}.")
    print(f"PASS offline: {len(workers)} workers; model/variant references and routing checks passed.")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def post(base_url, key, headers, payload, timeout):
    request_headers = dict(headers)
    request_headers.update({"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    request = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode(),
        headers=request_headers,
        method="POST",
    )
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise ProbeError(f"Gateway HTTP {exc.code}; inspect gateway logs for details.") from None
    except (urllib.error.URLError, TimeoutError):
        raise ProbeError("Gateway connection failed or timed out.") from None
    except (ValueError, UnicodeError):
        raise ProbeError("Gateway did not return valid JSON.") from None


def choice(response):
    try:
        result = response["choices"][0]
        if result.get("finish_reason") == "length":
            raise ProbeError("Generation hit its output limit; this probe is incomplete.")
        return result["message"]
    except (KeyError, IndexError, TypeError):
        raise ProbeError("Gateway returned an unexpected chat-completions response.") from None


def probe(config, ref, timeout, max_tokens):
    provider, api_model, body = model_ref(config, ref)
    settings = provider["settings"]
    base_url = settings["baseURL"]
    parsed = urllib.parse.urlsplit(base_url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.query:
        raise ProbeError("Expected a plain HTTP(S) provider base URL without embedded credentials/query.")
    key_ref = settings.get("apiKey", "")
    if not (key_ref.startswith("{env:") and key_ref.endswith("}")):
        raise ProbeError("This probe requires an environment-referenced API key.")
    key_name = key_ref[5:-1]
    key = os.environ.get(key_name)
    if not key:
        raise ProbeError(f"{key_name} is not set in this process; run --live on your configured target.")
    tools = [{
        "type": "function",
        "function": {
            "name": "project_probe",
            "description": "Return the synthetic probe result for the supplied marker.",
            "parameters": {
                "type": "object",
                "properties": {"marker": {"type": "string", "enum": ["opencode-probe"]}},
                "required": ["marker"],
                "additionalProperties": False,
            },
        },
    }]
    messages = [{"role": "user", "content": (
        "Call project_probe once with marker opencode-probe. "
        "After receiving its result, reply with the returned text exactly."
    )}]
    payload = merge(body, {
        "model": api_model, "messages": messages, "tools": tools,
        "tool_choice": "required", "stream": False, "max_tokens": max_tokens,
    })
    started = time.monotonic()
    first = post(base_url, key, provider.get("headers", {}), payload, timeout)
    message = choice(first)
    calls = message.get("tool_calls", [])
    if len(calls) != 1 or calls[0].get("function", {}).get("name") != "project_probe":
        raise ProbeError("Expected one project_probe tool call; no host command was executed.")
    call = calls[0]
    try:
        arguments = json.loads(call["function"]["arguments"])
    except (KeyError, TypeError, ValueError):
        raise ProbeError("Tool arguments were not a JSON object.") from None
    if arguments != {"marker": "opencode-probe"} or not call.get("id"):
        raise ProbeError("Tool call arguments or ID did not match the synthetic probe.")
    # Preserve returned reasoning fields on the assistant tool-call turn.
    assistant = {k: message[k] for k in (
        "role", "content", "tool_calls", "reasoning_content", "reasoning"
    ) if k in message}
    assistant["role"] = "assistant"
    messages.extend([assistant, {"role": "tool", "tool_call_id": call["id"], "content": "probe_ok_47"}])
    payload.update({"messages": messages, "tool_choice": "none"})
    second = post(base_url, key, provider.get("headers", {}), payload, timeout)
    final = choice(second)
    if final.get("tool_calls") or str(final.get("content") or "").strip() != "probe_ok_47":
        raise ProbeError("The follow-up did not return the exact synthetic tool result.")
    return {
        "model": ref, "status": "pass", "seconds": round(time.monotonic() - started, 2),
        "reasoning_field_observed": any(message.get(k) or final.get(k) for k in ("reasoning_content", "reasoning")),
        "first_usage": first.get("usage", {}), "followup_usage": second.get("usage", {}),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("opencode.jsonc"))
    parser.add_argument("--live", action="store_true", help="Make two synthetic API requests per selected route.")
    parser.add_argument("--model", action="append", help="Probe one provider/model#variant; repeat to select more.")
    parser.add_argument("--timeout", type=float, default=45)
    parser.add_argument("--max-tokens", type=int, default=4096)
    args = parser.parse_args()
    if args.timeout <= 0 or args.max_tokens <= 0:
        parser.error("Timeout and max-tokens must be positive.")
    if args.model and not args.live:
        parser.error("--model requires --live.")
    try:
        # The supplied .jsonc intentionally contains strict JSON for stdlib parsing.
        config = json.loads(args.config.read_text())
        validate(config)
        if not args.live:
            return 0
        refs = args.model or list(dict.fromkeys(a["model"] for a in config["agents"].values()))
        failed = False
        for ref in refs:
            try:
                result = probe(config, ref, args.timeout, args.max_tokens)
            except (ProbeError, KeyError, StopIteration, ValueError, TypeError) as exc:
                detail = str(exc) if isinstance(exc, ProbeError) else "Unresolved model or malformed gateway response."
                result = {"model": ref, "status": "fail", "detail": detail}
                failed = True
            print(json.dumps(result))
        return int(failed)
    except (ProbeError, OSError, KeyError, StopIteration, ValueError, TypeError) as exc:
        detail = str(exc) if isinstance(exc, ProbeError) else "Could not load or validate the supplied configuration."
        print("FAIL:", detail)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
