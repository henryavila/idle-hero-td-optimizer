param(
    [string]$InputDir = "",
    [string]$OutputDir = ""
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
$WorkspaceDir = Split-Path -Parent $ProjectDir
$Analyzer = Join-Path $WorkspaceDir "analyze_apks.py"

if (-not (Test-Path $Analyzer)) {
    throw "Could not find analyze_apks.py at workspace root: $Analyzer"
}

if ([string]::IsNullOrWhiteSpace($InputDir)) {
    $InputDir = Join-Path $ProjectDir "IdleHeroTD-apk"
}

if ([string]::IsNullOrWhiteSpace($OutputDir)) {
    $OutputDir = Join-Path $ProjectDir "IdleHeroTD-apk\apk_analysis"
}

function Test-PythonCommand {
    param([string]$Command, [string[]]$Args)

    try {
        $null = & $Command @Args --version 2>&1
        return $true
    } catch {
        return $false
    }
}

if (Test-PythonCommand "py" @("-3")) {
    Write-Host "Using Python launcher: py -3"
    & py -3 $Analyzer --input $InputDir --output $OutputDir
} elseif (Test-PythonCommand "python" @()) {
    Write-Host "Using python"
    & python $Analyzer --input $InputDir --output $OutputDir
} elseif (Test-PythonCommand "python3" @()) {
    Write-Host "Using python3"
    & python3 $Analyzer --input $InputDir --output $OutputDir
} else {
    throw "Python was not found. Install Python 3, or run this script from a shell where py/python/python3 is available."
}

Write-Host ""
Write-Host "Done. Open:"
Write-Host "  $OutputDir\SUMMARY.md"
Write-Host "  $OutputDir\mechanics_candidates.md"
Write-Host "  $OutputDir\file_index.csv"
