---
name: powershell-offline
description: Write, review, debug, refactor, and test PowerShell scripts and modules without internet access. Use for .ps1, .psm1, .psd1, PowerShell automation, Windows PowerShell 5.1 compatibility, PowerShell 7+, native-command integration, Pester tests, and PSScriptAnalyzer findings.
metadata:
  audience: powershell-developers
  workflow: offline-development
---

# PowerShell engineering offline

Work from local source, installed PowerShell editions, local module caches, local help, tests, and logs. Do not browse, fetch remote documentation, install modules or tools, contact package repositories, or invoke remote endpoints or sessions. Code may implement network behavior when the user requests it, but do not exercise that behavior in an offline verification run.

## Establish the contract

Before editing, inspect repository instructions, nearby PowerShell style, manifests, tests, CI/build files, and the Git diff. Determine:

- target editions and minimum versions: Windows PowerShell (`powershell.exe`) or PowerShell (`pwsh`);
- target operating systems and hosts;
- whether the file is a script, module, class, configuration, build task, or test;
- input/output and pipeline contracts, error behavior, idempotency, privilege needs, and expected side effects;
- which required commands and modules are already available locally.

Use `$PSVersionTable` and `Get-Command` in the actual target shell when available. Do not infer compatibility from a file extension or the current host. Do not add syntax, parameters, types, modules, or external executables that the declared baseline does not support.

Read [references/language-and-compatibility.md](references/language-and-compatibility.md) when writing or reviewing PowerShell. Read [references/native-and-data.md](references/native-and-data.md) when invoking executables or handling paths, files, encodings, JSON, CSV, XML, or secrets. Read [references/verification.md](references/verification.md) before running checks or when debugging.

## Make the smallest coherent change

- Preserve the repository's established structure, naming, comment-help style, formatting, and compatibility floor. Avoid unrelated reformatting or line-ending churn.
- Prefer advanced functions with typed parameters, validation attributes, pipeline declarations, and explicit output behavior when building reusable commands. Use approved `Verb-Noun` names for exported functions.
- Prefer PowerShell objects throughout the pipeline. Format for people only at the presentation boundary; do not make reusable functions emit formatted tables or parse display text.
- Use `-LiteralPath` for user-controlled paths, `$PSScriptRoot` for script-relative resources, and `Join-Path` for composition. Do not assume the working directory or Windows-only separators.
- Handle expected failures deliberately. Convert non-terminating errors with `-ErrorAction Stop` only where the surrounding `try`/`catch` can add value or recover. Preserve useful error context instead of returning sentinel strings.
- For state-changing commands, support `ShouldProcess` when practical and ensure `-WhatIf` bypasses every mutation, not only the final command. Make repeated runs safe where the task requires automation.
- Do not use `Invoke-Expression` to construct commands. Do not embed credentials, weaken execution policy, suppress all errors, or trust file content merely because it is local.
- Treat scripts, profiles, module import hooks, build steps, and tests as executable code. Inspect them before running. Obtain user confirmation before administrator actions or material changes outside a disposable test location.

## Verify with local evidence

Use the narrowest checks that prove the requested behavior, in this order when applicable:

1. Parse every changed `.ps1`, `.psm1`, and `.psd1`; `scripts/Test-PowerShellSyntax.ps1` provides an offline parser check.
2. Import a changed module in a clean process and inspect its exports without loading the user's profile.
3. Run focused Pester tests if a compatible local Pester version exists.
4. Run PSScriptAnalyzer only if it is already installed; interpret findings against the project's version and compatibility requirements.
5. Exercise success, empty input, invalid input, failure, `-WhatIf`, and native nonzero-exit paths as relevant. Use disposable files and mock external systems.
6. Repeat material checks in every locally available target edition/version. Passing in `pwsh` does not prove Windows PowerShell 5.1 compatibility, or the reverse.

Do not modify the user's profile, machine policy, execution policy, module path, or global module installation to make checks pass. Never claim runtime compatibility for an edition, operating system, module version, privilege level, or external system that was not actually tested.

Report files changed, the declared compatibility target, exact shells/modules used for verification, commands or tests run, observed results, side effects, and remaining unverified assumptions.
