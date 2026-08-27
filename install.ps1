# install.ps1 - install the ACTDIM-AGENTS skills into Claude Code, Codex, OpenCode and/or Antigravity.
#
# Claude, Codex & Antigravity use the same ~/.<tool>/skills/<name>/SKILL.md format -> the skill folders are copied verbatim.
# OpenCode uses flat ~/.config/opencode/commands/<name>.md commands -> generated from the same SKILL.md bodies;
#   init-agents' helper files (protocol.md, init-agents.sh) go to ~/.config/opencode/actdim-agents/.
# The ACTDIM-AGENTS-PROTOCOL itself is picked up by all four natively via each repo's AGENTS.md.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1                  # all (default), copy
#   powershell ... -File install.ps1 -Target claude    # claude | codex | opencode | antigravity | both | all
#   powershell ... -File install.ps1 -Symlink          # symlink skill folders (claude/codex/antigravity)

param(
    [ValidateSet('claude', 'codex', 'opencode', 'antigravity', 'both', 'all')][string]$Target = 'all',
    [switch]$Symlink,
    [switch]$InstallDeps,
    [string]$ClaudeHome      = (Join-Path $env:USERPROFILE '.claude'),
    [string]$CodexHome       = (Join-Path $env:USERPROFILE '.codex'),
    [string]$OpencodeHome    = (Join-Path $env:USERPROFILE '.config\opencode'),
    [string]$AntigravityHome = (Join-Path $env:USERPROFILE '.gemini\config')
)

$ErrorActionPreference = 'Stop'

function Check-Dependencies {
    $uv = Get-Command 'uv' -ErrorAction SilentlyContinue
    if (-not $uv) {
        if ($InstallDeps) {
            Write-Host "-> Installing 'uv' package & Python version manager..."
            powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        }
        else {
            Write-Host "-> [Note] 'uv' is recommended for automatic Python/MCP tool management."
            Write-Host "   Install uv:  powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`""
            Write-Host "   Or run with: powershell ... -File install.ps1 -InstallDeps"
            Write-Host "   Or use mise: mise install"
        }
    }
    else {
        Write-Host "-> 'uv' detected: $($uv.Source)"
    }
}

Check-Dependencies

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
            try {
                New-Item -ItemType SymbolicLink -Path $target -Target $d.FullName -ErrorAction Stop | Out-Null
                Write-Host "   linked  $($d.Name)"
            }
            catch {
                $null = cmd /c mklink /J "`"$target`"" "`"$($d.FullName)`"" 2>&1
                if (Test-Path $target) {
                    Write-Host "   linked (junction)  $($d.Name)"
                }
                else {
                    Copy-Item -Recurse $d.FullName $target
                    Write-Host "   copied (fallback)  $($d.Name)"
                }
            }
        }
        else {
            Copy-Item -Recurse $d.FullName $target
            Write-Host "   copied  $($d.Name)"
        }
    }
}

function Install-RuleFolders([string]$homeDir) {
    $rulesSrc = Join-Path $PSScriptRoot 'rules'
    if (Test-Path $rulesSrc) {
        $dst = Join-Path $homeDir 'rules'
        if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
        New-Item -ItemType Directory -Force -Path $dst | Out-Null
        Copy-Item -Path "$rulesSrc\*" -Destination $dst -Recurse -Force
        Write-Host "   rules copied -> $dst"
    }
}

function Install-OpenCode {
    $cmddir = Join-Path $OpencodeHome 'commands'
    $helper = Join-Path $OpencodeHome 'actdim-agents'
    New-Item -ItemType Directory -Force -Path $cmddir | Out-Null
    New-Item -ItemType Directory -Force -Path $helper | Out-Null
    Copy-Item -Force (Join-Path $src 'init-agents\protocol.md')       (Join-Path $helper 'protocol.md')
    Copy-Item -Force (Join-Path $src 'init-agents\init-agents.sh')     (Join-Path $helper 'init-agents.sh')
    Copy-Item -Force (Join-Path $src 'init-agents\migrate_protocol.py') (Join-Path $helper 'migrate_protocol.py')
    Copy-Item -Force (Join-Path $src 'update-agents\update_agents.py')  (Join-Path $helper 'update_agents.py')
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

function Set-McpConfigJson([string]$filePath) {
    try {
        $parent = Split-Path -Parent $filePath
        if ($parent -and -not (Test-Path $parent)) {
            New-Item -ItemType Directory -Force -Path $parent | Out-Null
        }
        
        $py = Get-Command 'python' -ErrorAction SilentlyContinue
        if ($py) {
            $script = @"
import json, os, sys
path = sys.argv[1]
data = {}
if os.path.exists(path) and os.path.getsize(path) > 0:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}
if not isinstance(data, dict):
    data = {}
if 'mcpServers' not in data or not isinstance(data['mcpServers'], dict):
    data['mcpServers'] = {}
if 'code-review-graph' not in data['mcpServers']:
    data['mcpServers']['code-review-graph'] = {
        'command': 'uvx',
        'args': ['code-review-graph']
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'   registered code-review-graph MCP in {path}')
else:
    print(f'   code-review-graph MCP already configured in {path}')
"@
            & python -c $script $filePath
            return
        }

        $json = $null
        if (Test-Path $filePath) {
            $raw = Get-Content -Raw -Encoding UTF8 $filePath
            if ($raw -and $raw.Trim()) {
                $json = $raw | ConvertFrom-Json
            }
        }
        if (-not $json) {
            $json = [PSCustomObject]@{}
        }
        if (-not $json.PSObject.Properties['mcpServers']) {
            $json | Add-Member -MemberType NoteProperty -Name 'mcpServers' -Value ([PSCustomObject]@{}) -Force
        }
        if (-not $json.mcpServers.PSObject.Properties['code-review-graph']) {
            $crg = [PSCustomObject]@{
                command = 'uvx'
                args = @('code-review-graph')
            }
            $json.mcpServers | Add-Member -MemberType NoteProperty -Name 'code-review-graph' -Value $crg -Force
            $out = $json | ConvertTo-Json -Depth 10
            Write-Utf8NoBom $filePath $out
            Write-Host "   registered code-review-graph MCP in $filePath"
        }
        else {
            Write-Host "   code-review-graph MCP already configured in $filePath"
        }
    }
    catch {
        Write-Host "   (note: could not update $filePath - $_)"
    }
}

$targets = switch ($Target) {
    'claude'      { @('claude') }
    'codex'       { @('codex') }
    'opencode'    { @('opencode') }
    'antigravity' { @('antigravity') }
    'both'        { @('claude', 'codex') }
    'all'         { @('claude', 'codex', 'opencode', 'antigravity') }
}

foreach ($t in $targets) {
    switch ($t) {
        'claude' {
            Install-SkillFolders $ClaudeHome
            Install-RuleFolders $ClaudeHome
            Set-McpConfigJson (Join-Path $env:USERPROFILE '.claude.json')
            Set-McpConfigJson (Join-Path $ClaudeHome 'mcp_config.json')
        }
        'codex' {
            Install-SkillFolders $CodexHome
            Install-RuleFolders $CodexHome
            Set-McpConfigJson (Join-Path $CodexHome 'mcp_config.json')
        }
        'opencode' {
            Install-OpenCode
            Set-McpConfigJson (Join-Path $OpencodeHome 'mcp_config.json')
        }
        'antigravity' {
            Install-SkillFolders $AntigravityHome
            Install-RuleFolders $AntigravityHome
            Set-McpConfigJson (Join-Path $AntigravityHome 'mcp_config.json')
        }
    }
}

# --- Auto-migrate current repository .agents/ metadata if present ---
$py = Get-Command 'python' -ErrorAction SilentlyContinue
if ($py -and (Test-Path (Join-Path $PSScriptRoot '.agents'))) {
    Write-Host "-> Running .agents/ versioned protocol migration for v1.5.0 compatibility..."
    & python (Join-Path $src 'init-agents\migrate_protocol.py') $PSScriptRoot
}

Write-Host "Done. Claude/Codex/Antigravity skills register next session as /init-agents etc.; OpenCode picks up /commands, code-review-graph MCP is configured, and all read AGENTS.md natively."

