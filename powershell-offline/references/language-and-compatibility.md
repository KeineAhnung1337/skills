# Language and compatibility

## Version-aware implementation

- Treat Windows PowerShell 5.1 and PowerShell 7+ as different runtimes. If both are targets, write to 5.1 syntax unless a guarded, separately parsed file contains newer syntax. Runtime conditionals cannot protect syntax that the older parser cannot parse.
- PowerShell 7-only language features include the ternary operator, null-coalescing operators, and pipeline-chain operators. Avoid them for 5.1-compatible files.
- `$IsWindows`, `$IsLinux`, and `$IsMacOS` are not available in Windows PowerShell 5.1. Use edition/version information plus local platform APIs when 5.1 is in scope.
- Do not assume a cmdlet exists or has the same parameters across editions. Confirm with local `Get-Command` and `Get-Help`, or isolate edition-specific adapters.
- Do not change `#requires` casually: it rejects the entire script before execution. Use it only when the requirement is real and intended.

## Functions and parameters

- Use `[CmdletBinding()]` for reusable functions. Define parameter sets only when they represent genuinely exclusive invocation modes, and make the default unambiguous.
- Use `[Parameter(Mandatory)]`, pipeline binding, aliases, and validation only when they express the public contract. Avoid broad `[object]` inputs when a stable type is known.
- Distinguish `$null`, an empty string, an empty collection, and a missing argument. Put `$null` on the left of comparisons so collection comparison semantics do not silently change the result.
- Remember that scalar and collection results can collapse or expand through the pipeline. Use `@(...)` when callers require an array; use the unary comma only when a single array object, rather than its elements, is the intended output.
- Avoid `return` as a type guarantee. Every uncaptured success-stream expression is output. Capture or suppress incidental output from .NET methods and mutating commands.
- Do not use `Write-Host` for data. Emit objects on the success stream, use `Write-Verbose`/`Write-Debug` for diagnostics, `Write-Warning` for actionable warnings, and `Write-Information` for informational events when the version floor supports the intended behavior.

## Errors and cleanup

- PowerShell has terminating and non-terminating errors. `try`/`catch` handles terminating errors; apply `-ErrorAction Stop` at the call that must become catchable rather than changing global preferences without need.
- When rethrowing the current failure, use `throw` without an argument to retain its error record. Wrap only when the added context helps callers, and preserve the original exception as an inner exception when feasible.
- Use `try`/`finally` for cleanup of temporary files, locations, runspaces, streams, and disposable objects. Avoid global location changes; if unavoidable, restore state in `finally`.
- `Set-StrictMode` can expose defects but can also break callers or imported code. Scope it to code the project controls and match the repository's established policy instead of inserting it mechanically.

## Modules and public contracts

- Keep exports intentional through the module manifest or `Export-ModuleMember`. Private helpers should remain private.
- Avoid work with external side effects during module import. Import should define behavior, not mutate machine state or contact services.
- Preserve command names, parameter names and aliases, accepted pipeline input, output object shape/type names, error identifiers, and manifest metadata unless the requested change intentionally alters the public API.
- Classes and enums declared in modules have parse/import behavior that differs from ordinary functions. Use `using module` only when parse-time type visibility is required and compatible with the version floor.
