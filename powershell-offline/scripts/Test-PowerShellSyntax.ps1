[CmdletBinding()]
param(
    [Parameter(Mandatory, Position = 0, ValueFromPipeline, ValueFromRemainingArguments)]
    [ValidateNotNullOrEmpty()]
    [string[]] $LiteralPath
)

begin {
    $hadErrors = $false
}

process {
    foreach ($path in $LiteralPath) {
        $resolvedPaths = @(Resolve-Path -LiteralPath $path -ErrorAction SilentlyContinue)
        if ($resolvedPaths.Count -eq 0) {
            Write-Error -Message "File not found: $path" -Category ObjectNotFound -TargetObject $path
            $hadErrors = $true
            continue
        }

        foreach ($resolvedPath in $resolvedPaths) {
            $tokens = $null
            $parseErrors = $null
            $null = [System.Management.Automation.Language.Parser]::ParseFile(
                $resolvedPath.ProviderPath,
                [ref] $tokens,
                [ref] $parseErrors
            )

            if ($parseErrors.Count -eq 0) {
                Write-Output ([pscustomobject]@{
                    Path   = $resolvedPath.ProviderPath
                    Parsed = $true
                    Errors = 0
                })
                continue
            }

            $hadErrors = $true
            foreach ($parseError in $parseErrors) {
                Write-Error -Message ('{0}:{1}:{2}: {3}' -f
                    $resolvedPath.ProviderPath,
                    $parseError.Extent.StartLineNumber,
                    $parseError.Extent.StartColumnNumber,
                    $parseError.Message
                ) -Category ParserError -TargetObject $resolvedPath.ProviderPath
            }
        }
    }
}

end {
    if ($hadErrors) {
        exit 1
    }
}
