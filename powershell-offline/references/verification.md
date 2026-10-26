# Offline verification and debugging

## Inventory the local toolchain

Run probes without profiles so personal startup code cannot hide dependencies or change semantics:

```powershell
$PSVersionTable | Format-List PSVersion, PSEdition, Platform, OS
Get-Command -Name Pester, Invoke-Pester, Invoke-ScriptAnalyzer -ErrorAction SilentlyContinue
Get-Module -ListAvailable | Sort-Object Name, Version | Select-Object Name, Version, Path
```

Use `pwsh -NoLogo -NoProfile -NonInteractive` for PowerShell 7+ and `powershell.exe -NoLogo -NoProfile -NonInteractive` for Windows PowerShell. Do not change `PSModulePath` or install a missing checker just to validate.

## Parse before execution

Run the included parser from the skill directory:

```powershell
pwsh -NoLogo -NoProfile -NonInteractive -File ./scripts/Test-PowerShellSyntax.ps1 ./path/to/file.ps1
```

The script performs parsing only; it does not prove imports, name resolution, module availability, runtime behavior, or compatibility with another PowerShell version. Invoke the parser with each target executable that is locally available.

For a `.psd1`, parsing proves only PowerShell syntax. If it is trusted and intended as a data file, `Import-PowerShellDataFile` provides a stronger structural check without importing a module. Do not execute or import an untrusted manifest.

## Module smoke test

Use a clean child process and import the exact changed path. Check import errors, exported commands, and removal/re-import when lifecycle behavior matters. Avoid `-Force` as the first test because it can conceal load-order assumptions.

If the module uses classes or parse-time `using module`, start a fresh process for every material test; types cannot always be unloaded or redefined reliably in one session.

## Pester and static analysis

- Detect the locally installed Pester version and follow the repository's existing invocation. Pester 4 and 5 have meaningful syntax, discovery, scoping, and configuration differences.
- Prefer focused unit tests with mocks at process, filesystem, registry, service, CIM/WMI, and network boundaries. Integration tests should use disposable resources and state their platform/privilege prerequisites.
- Test emitted objects and error records, not formatted console text, unless console presentation is the actual contract.
- If PSScriptAnalyzer is installed, use the repository settings file when present. Treat analyzer output as evidence to assess, not an automatic rewrite mandate; rules can conflict with an older version target or an intentional public API.

## Debug from the first failure

Reproduce with the same executable, version, OS, architecture, host, working directory, environment, module versions, inputs, and privilege level. Capture the first relevant error record, including exception type, fully qualified error ID, category, invocation information, and script stack trace. For native tools, also capture the exact argument array, stdout/stderr separately where practical, and the immediate exit code.

Do not add broad `try { ... } catch {}` blocks, `-ErrorAction SilentlyContinue`, or preference-variable changes merely to remove visible symptoms. Trace whether the defect is parsing, binding, pipeline enumeration, scope, stream handling, external-process behavior, platform/version compatibility, or state left by an earlier run.

## Completion evidence

State exactly which shell executable and version ran each check. Distinguish:

- parsed successfully;
- imported successfully;
- focused tests passed;
- static analysis completed with stated findings;
- integration behavior was exercised on a named platform;
- compatibility remains unverified because the required runtime, module, service, privilege, or platform was unavailable.
