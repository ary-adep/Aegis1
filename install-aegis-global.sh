#!/usr/bin/env bash
# Windows only. Run in Git Bash: bash install-aegis-global.sh
set -euo pipefail

finish() {
    code=$?
    trap - EXIT
    if [[ -t 0 ]]; then
        printf '\nPress Enter to close...'
        read -r _ || true
    fi
    exit "$code"
}
trap finish EXIT

case "$(uname -s)" in
    MINGW*|MSYS*) ;;
    *) printf 'This installer requires Git Bash on Windows.\n' >&2; exit 1 ;;
esac
command -v powershell.exe >/dev/null || {
    printf 'Windows PowerShell was not found.\n' >&2; exit 1;
}

printf 'Aegis global installer for Windows\n'
printf 'Close active Claude sessions before installing.\n'
printf 'Repository path (example: D:\\aravind\\Aegis1): '
IFS= read -r repo
# Accept paths pasted with matching surrounding quotes.
repo="${repo%$'\r'}"
if [[ "$repo" == \"*\" && "$repo" == *\" ]]; then
    repo="${repo:1:${#repo}-2}"
elif [[ "$repo" == \'*\' && "$repo" == *\' ]]; then
    repo="${repo:1:${#repo}-2}"
fi
[[ -n "$repo" ]] || { printf 'No repository path supplied.\n' >&2; exit 1; }
export AEGIS_INSTALL_REPO
AEGIS_INSTALL_REPO="$(cygpath -aw -- "$repo")"

# Pass the path as data, never interpolate it into PowerShell source.
MSYS_NO_PATHCONV=1 powershell.exe -NoProfile -NonInteractive -Command - <<'POWERSHELL'
$ErrorActionPreference = 'Stop'
try {
    $repo = (Resolve-Path -LiteralPath $env:AEGIS_INSTALL_REPO).ProviderPath
    $skillNames = @(
        'aegis', 'system-discovery', 'requirements-analysis',
        'architecture-analysis', 'implementation-planning',
        'implementation', 'testing-verification', 'code-review', 'debugging'
    )
    $globalRoot = Join-Path $env:USERPROFILE '.claude'
    $skillRoot = Join-Path $globalRoot 'skills'
    $agentRoot = Join-Path $globalRoot 'agents'
    $agentSource = Join-Path $repo 'agents\aegis1.md'

    function Find-Entry([string]$path) {
        $parent = Split-Path -Parent $path
        if (Test-Path -LiteralPath $parent) {
            Get-ChildItem -LiteralPath $parent -Force |
                Where-Object { $_.Name -eq (Split-Path -Leaf $path) } |
                Select-Object -First 1
        }
    }
    function Same-Link($entry, [string]$target) {
        if (-not $entry -or -not $entry.LinkType) { return $false }
        $actual = @($entry.Target)[0]
        if (-not $actual) { return $false }
        return $actual.TrimEnd('\') -ieq $target.TrimEnd('\')
    }

    # Validate the complete source and all destinations before creating links.
    if (-not (Test-Path -LiteralPath $agentSource -PathType Leaf)) {
        throw "Missing agent file: $agentSource"
    }
    $plan = @()
    $conflicts = @()
    foreach ($name in $skillNames) {
        $source = Join-Path $repo "skills\$name"
        if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md') -PathType Leaf)) {
            throw "Missing required skill: $source"
        }
        $destination = Join-Path $skillRoot $name
        $entry = Find-Entry $destination
        if ($entry -and -not (Same-Link $entry $source)) {
            $conflicts += $destination
        }
        $plan += [pscustomobject]@{
            Source = $source; Destination = $destination; Exists = [bool]$entry
        }
    }
    $agentDestination = Join-Path $agentRoot 'aegis1.md'
    $agentEntry = Find-Entry $agentDestination
    $agentLinked = Same-Link $agentEntry $agentSource
    $agentIdentical = $false
    if ($agentEntry -and -not $agentEntry.LinkType -and -not $agentEntry.PSIsContainer) {
        $agentIdentical = (Get-FileHash -LiteralPath $agentDestination).Hash -eq
                          (Get-FileHash -LiteralPath $agentSource).Hash
    }
    if ($agentEntry -and -not $agentLinked -and -not $agentIdentical) {
        $conflicts += $agentDestination
    }
    if ($conflicts.Count) {
        Write-Host 'No installation changes made. Existing destinations need review:'
        $conflicts | ForEach-Object { Write-Host "  $_" }
        throw 'Compare and back up existing copies or links before retrying. Nothing is overwritten automatically.'
    }

    New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $agentRoot -Force | Out-Null
    foreach ($item in $plan) {
        if ($item.Exists) {
            Write-Host "Already linked: $($item.Destination)"
        } else {
            New-Item -ItemType Junction -Path $item.Destination -Target $item.Source | Out-Null
            Write-Host "Linked: $($item.Destination)"
        }
    }
    if ($agentLinked) {
        Write-Host 'Agent: already linked.'
    } elseif ($agentIdentical) {
        Write-Host 'Agent: existing identical copy retained; future repository updates will not update this copy.'
    } else {
        try {
            New-Item -ItemType SymbolicLink -Path $agentDestination -Target $agentSource | Out-Null
            Write-Host 'Agent: linked.'
        } catch {
            # File symlinks may require Developer Mode or administrator rights.
            # Never overwrite anything after a failed link operation.
            if (Find-Entry $agentDestination) { throw }
            [IO.File]::Copy($agentSource, $agentDestination, $false)
            Write-Host 'Agent: copied because Windows did not allow the file symbolic link.'
            Write-Host 'After future git pulls, compare/update this agent copy separately.'
        }
    }

    foreach ($item in $plan) {
        if (-not (Same-Link (Find-Entry $item.Destination) $item.Source)) {
            throw "Link verification failed: $($item.Destination)"
        }
    }
    if ((Get-FileHash -LiteralPath $agentDestination).Hash -ne
        (Get-FileHash -LiteralPath $agentSource).Hash) {
        throw 'Agent content verification failed.'
    }
    Write-Host "`nInstallation verified."
    Write-Host 'No permission settings, hooks, or unrelated skills were changed.'
    Write-Host 'Keep this repository at its current path. Git pull updates linked files.'
    Write-Host 'Check your application for older project-local Aegis copies that could shadow these global skills.'
    Write-Host 'Start a fresh Claude session and run:'
    Write-Host '/aegis Check that the global orchestrator, governance and system-discovery instructions load. Report exact paths. Do not inspect application code or modify files.'
    exit 0
} catch {
    Write-Error -Message $_.Exception.Message -ErrorAction Continue
    Write-Host 'If creation failed partway through, already-created links were retained; rerunning is safe.'
    exit 1
}
POWERSHELL
