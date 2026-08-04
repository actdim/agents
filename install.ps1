# install.ps1 — install the ACTDIM-AGENTS skills into Claude Code, Codex and/or OpenCode.
#
# Claude & Codex use the same ~/.<tool>/skills/<name>/SKILL.md format -> the skill folders are copied verbatim.
# OpenCode uses flat ~/.config/opencode/commands/<name>.md commands -> generated from the same SKILL.md bodies;
#   init-agents' helper files (protocol.md, init-agents.sh) go to ~/.config/opencode/actdim-agents/.
# The ACTDIM-AGENTS-PROTOCOL itself is picked up by all three natively via each repo's AGENTS.md.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1                  # all (default), copy
#   powershell ... -File install.ps1 -Target claude    # claude | codex | opencode | both | all
#   powershell ... -File install.ps1 -Symlink          # symlink skill folders (claude/codex)

param(
    [ValidateSet('claude', 'codex', 'opencode', 'both', 'all')][string]$Target = 'all',
    [switch]$Symlink,
    [string]$ClaudeHome   = (Join-Path $env:USERPROFILE '.claude'),
    [string]$CodexHome    = (Join-Path $env:USERPROFILE '.codex'),
    [string]$OpencodeHome = (Join-Path $env:USERPROFILE '.config\opencode')
)

$ErrorActionPreference = 'Stop'

$src = Join-Path $PSScriptRoot 'skills'
if (-not (Test-Path $src)) { throw "Source skills folder not found: $src" }

function Write-Utf8NoBom([string]$path, [string]$text) {
    [System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))
}

function Install-SkillFolders([string]$homeDir) {
    $dst = Join-Path $homeDir 'skills'
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Write-Host "-> $dst"
    foreach ($d in Get-ChildItem -Directory $src) {
        $target = Join-Path $dst $d.Name
        if (Test-Path $target) { Remove-Item -Recurse -Force $target }
        if ($Symlink) {
            New-Item -ItemType SymbolicLink -Path $target -Target $d.FullName | Out-Null
            Write-Host "   linked  $($d.Name)"
        }
        else {
            Copy-Item -Recurse $d.FullName $target
            Write-Host "   copied  $($d.Name)"
        }
    }
}

function Install-OpenCode {
    $cmddir = Join-Path $OpencodeHome 'commands'
    $helper = Join-Path $OpencodeHome 'actdim-agents'
    New-Item -ItemType Directory -Force -Path $cmddir | Out-Null
    New-Item -ItemType Directory -Force -Path $helper | Out-Null
    Write-Host "-> $cmddir (commands) + $helper (helper)"
    Copy-Item -Force (Join-Path $src 'init-agents\protocol.md')   (Join-Path $helper 'protocol.md')
    Copy-Item -Force (Join-Path $src 'init-agents\init-agents.sh') (Join-Path $helper 'init-agents.sh')
    foreach ($d in Get-ChildItem -Directory $src) {
        $raw = (Get-Content -Raw -Encoding UTF8 (Join-Path $d.FullName 'SKILL.md')) -replace "`r`n", "`n"
        $desc = ''
        $body = $raw
        if ($raw -match '(?s)^---\n(.*?)\n---\n(.*)$') {
            $fm = $matches[1]; $body = $matches[2]
            foreach ($line in ($fm -split "`n")) {
                if ($line -match '^description:\s*(.*)$') { $desc = $matches[1]; break }
            }
        }
        $note = ''
        if ($d.Name -eq 'init-agents') {
            $note = '> OpenCode: the helper script is at `' + $helper + '\init-agents.sh` and the protocol at `' + $helper + '\protocol.md`. Where the steps below say "this skill''s folder", use `' + $helper + '`.' + "`n`n"
        }
        $content = "---`n" + 'description: "' + $desc + '"' + "`n---`n`n" + $note + $body
        Write-Utf8NoBom (Join-Path $cmddir ($d.Name + '.md')) $content
        Write-Host "   command $($d.Name).md"
    }
}

$targets = switch ($Target) {
    'claude'   { @('claude') }
    'codex'    { @('codex') }
    'opencode' { @('opencode') }
    'both'     { @('claude', 'codex') }
    'all'      { @('claude', 'codex', 'opencode') }
}

foreach ($t in $targets) {
    switch ($t) {
        'claude'   { Install-SkillFolders $ClaudeHome }
        'codex'    { Install-SkillFolders $CodexHome }
        'opencode' { Install-OpenCode }
    }
}

Write-Host "Done. Claude/Codex skills register next session as /init-agents etc.; OpenCode picks up /commands and reads AGENTS.md natively."
