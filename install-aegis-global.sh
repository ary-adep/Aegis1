#!/usr/bin/env bash
# Windows Git Bash. Uses the directory containing this script, not the terminal cwd.
set -euo pipefail
log_file=''
finish() {
    code=$?
    trap - EXIT
    if (( code == 0 )); then
        message='SUCCESS: Aegis global installation verified.'
    else
        message="FAILED: Aegis installation did not complete (exit $code). See the errors above."
    fi
    printf '\n%s\n' "$message"
    if [[ -n "$log_file" ]]; then
        printf '%s\n' "$message" >> "$log_file"
        printf 'Log file: %s\n' "$(cygpath -aw -- "$log_file")"
    fi
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
for required in powershell.exe cygpath iconv base64 tee; do
    command -v "$required" >/dev/null || {
        printf 'Required command not found: %s\n' "$required" >&2; exit 1;
    }
done
repo="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
export AEGIS_INSTALL_REPO
AEGIS_INSTALL_REPO="$(cygpath -aw -- "$repo")"
log_root="$(cygpath -u -- "${LOCALAPPDATA:?LOCALAPPDATA is unavailable}")/Aegis/logs"
mkdir -p -- "$log_root"
log_file="$(mktemp "$log_root/install-$(date +%Y%m%d-%H%M%S)-XXXXXX.log")"
{
    printf 'Aegis Windows global installer\nStarted: %s\n' "$(date -Iseconds)"
    printf 'Repository: %s\n' "$AEGIS_INSTALL_REPO"
    printf 'Close active Claude sessions before installation.\n'
} | tee -a "$log_file"

# Encode the complete script so PowerShell executes one block, not interactive stdin.
# The repository path is environment data, never interpolated into executable source.
ps_source=$(cat <<'POWERSHELL'
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
function Log([string]$message) {
    [Console]::WriteLine(('[{0}] {1}' -f [DateTimeOffset]::Now.ToString('yyyy-MM-dd HH:mm:ss zzz'), $message))
}
try {
    $repo = (Resolve-Path -LiteralPath $env:AEGIS_INSTALL_REPO).ProviderPath
    $skillNames = @(
        'aegis', 'system-discovery', 'requirements-analysis',
        'architecture-analysis', 'implementation-planning',
        'implementation', 'testing-verification', 'code-review', 'debugging'
    )
    $globalRoot = Join-Path $env:USERPROFILE '.claude'
    Log "Repository: $repo"
    Log "Global installation: $globalRoot"
    $skillRoot = Join-Path $globalRoot 'skills'
    $agentRoot = Join-Path $globalRoot 'agents'
    $agentSource = Join-Path $repo 'agents\aegis1.md'

    function File-Hash([string]$path) {
        $algorithm = [Security.Cryptography.SHA256]::Create()
        $stream = [IO.File]::OpenRead($path)
        try { return [BitConverter]::ToString($algorithm.ComputeHash($stream)) }
        finally { $stream.Dispose(); $algorithm.Dispose() }
    }
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
        $agentIdentical = (File-Hash $agentDestination) -eq
                          (File-Hash $agentSource)
    }
    if ($agentEntry -and -not $agentLinked -and -not $agentIdentical) {
        $conflicts += $agentDestination
    }
    if ($conflicts.Count) {
        Log 'No installation changes made. Existing destinations need review:'
        $conflicts | ForEach-Object { Log "  $_" }
        throw 'Compare and back up existing copies or links before retrying. Nothing is overwritten automatically.'
    }

    New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $agentRoot -Force | Out-Null
    foreach ($item in $plan) {
        if ($item.Exists) {
            Log "Already linked: $($item.Destination)"
        } else {
            New-Item -ItemType Junction -Path $item.Destination -Target $item.Source | Out-Null
            Log "Linked: $($item.Destination)"
        }
    }
    if ($agentLinked) {
        Log 'Agent: already linked.'
    } elseif ($agentIdentical) {
        Log 'Agent: existing identical copy retained; future repository updates will not update this copy.'
    } else {
        try {
            New-Item -ItemType SymbolicLink -Path $agentDestination -Target $agentSource | Out-Null
            Log 'Agent: linked.'
        } catch {
            # File symlinks may require Developer Mode or administrator rights.
            # Never overwrite anything after a failed link operation.
            if (Find-Entry $agentDestination) { throw }
            [IO.File]::Copy($agentSource, $agentDestination, $false)
            Log 'Agent: copied because Windows did not allow the file symbolic link.'
            Log 'After future git pulls, compare/update this agent copy separately.'
        }
    }

    foreach ($item in $plan) {
        if (-not (Same-Link (Find-Entry $item.Destination) $item.Source)) {
            throw "Link verification failed: $($item.Destination)"
        }
    }
    if ((File-Hash $agentDestination) -ne
        (File-Hash $agentSource)) {
        throw 'Agent content verification failed.'
    }
    Log "`nInstallation verified."
    Log 'No permission settings, hooks, or unrelated skills were changed.'
    Log 'Keep this repository at its current path. Git pull updates linked files.'
    Log 'Check your application for older project-local Aegis copies that could shadow these global skills.'
    Log 'Start a fresh Claude session and run:'
    Log '/aegis Check that the global orchestrator, governance and system-discovery instructions load. Report exact paths. Do not inspect application code or modify files.'
    exit 0
} catch {
    Log ('ERROR: ' + $_.Exception.Message)
    Log 'If creation failed partway through, already-created links were retained; rerunning is safe.'
    exit 1
}
POWERSHELL
)
encoded="$(printf '%s' "$ps_source" | iconv -f UTF-8 -t UTF-16LE | base64 | tr -d '\r\n')"
set +e
MSYS_NO_PATHCONV=1 powershell.exe -NoProfile -NonInteractive -OutputFormat Text -EncodedCommand "$encoded" 2>&1 | tee -a "$log_file"
results=("${PIPESTATUS[@]}")
set -e
if (( results[1] != 0 )); then
    printf 'ERROR: Could not write the complete installation log.\n' >&2
    exit 1
fi
exit "${results[0]}"
