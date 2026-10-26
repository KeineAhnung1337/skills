# Native commands, paths, and data

## Native processes

- Resolve an executable deliberately with `Get-Command -CommandType Application` when command shadowing matters. Invoke it with the call operator and an argument array: `& $executable @arguments`.
- Never assemble an untrusted command string for `Invoke-Expression`. PowerShell quoting and the target program's argument parser are separate layers.
- Prefer direct invocation when output and exit status are needed. `Start-Process -ArgumentList` ultimately constructs a command line and can lose intended argument boundaries; use it only for process features it actually provides, then test arguments containing spaces, quotes, and empty values.
- Capture `$LASTEXITCODE` immediately after the native command, before another native invocation changes it. Treat success codes according to that program's documented local behavior rather than assuming every nonzero code has the same meaning.
- Do not rely on `--` as a universal PowerShell end-of-options marker. It is interpreted according to the invoked command.
- PowerShell 7.3+ changed native argument passing and exposes `$PSNativeCommandArgumentPassing`. When exact quoting matters, test in every target version instead of assuming behavior transfers between Windows PowerShell and modern `pwsh`.
- Separate stdout, stderr, PowerShell error records, and the process exit code. Do not parse colorized or localized display output when a structured or stable mode is available locally.

## Paths and filesystem behavior

- Use `-LiteralPath` for paths received as data. `-Path` treats wildcard characters as patterns.
- Build script-relative paths from `$PSScriptRoot`. Resolve a path only when it must already exist; `Resolve-Path` is not a constructor for new destinations.
- Account for case sensitivity, invalid characters, reserved names, symlinks/reparse points, long paths, file locks, and ACL differences on the declared target systems. Do not normalize case or separators as a substitute for testing.
- Before destructive or recursive operations, resolve and display the exact target, reject empty/root-like targets, avoid broad wildcards, and keep operations within the authorized scope. Prefer `ShouldProcess` and recoverable behavior.
- Preserve intentional encoding, BOM, newline style, and final-newline behavior. Windows PowerShell 5.1 and PowerShell 7 use different defaults for several file cmdlets, so specify a supported encoding when the file contract matters and test the resulting bytes.

## Structured data

- Keep objects as objects. Use `ConvertFrom-Json`, `Import-Csv`, XML APIs, or another format-aware parser instead of regular expressions over structured data.
- JSON depth, duplicate/case-variant keys, comments, date conversion, and numeric precision vary by PowerShell version. Confirm the accepted input and pass supported parameters explicitly; do not silently round-trip unknown JSON and claim preservation.
- CSV is culture- and delimiter-sensitive. Keep `Import-Csv`/`Export-Csv` settings paired and avoid formatting objects before export.
- For configuration files, preserve unknown fields and ordering only if the chosen parser/serializer actually does so. Avoid rewriting a whole file for a one-field change when lossless preservation matters.

## Secrets and trust boundaries

- Do not place secrets in source, command arguments, transcripts, debug output, or committed fixture files. Environment variables reduce accidental command-line exposure but are not a secure vault.
- `SecureString` does not by itself make a secret safe to persist or transmit. Platform-specific encryption such as Windows DPAPI is not portable; document the actual protection and scope when used.
- Validate untrusted values before using them as command names, paths, module names, registry locations, WMI/CIM queries, or arguments. Prefer allowlists at privilege boundaries.
- Do not load `.ps1`, `.psd1`, or `.psm1` content merely to inspect it: data files and manifests may contain expressions allowed by their loader. Parse or read text first when provenance is uncertain.
