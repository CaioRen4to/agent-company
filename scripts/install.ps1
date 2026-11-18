param(
    [string]$TargetDir = "$HOME\.claude\skills",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillsSource = Join-Path $RepoRoot "skills"

if (-not (Test-Path $SkillsSource)) {
    throw "Diretório de skills não encontrado: $SkillsSource"
}

New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

$Installed = 0
$Skipped = 0
Get-ChildItem -Path $SkillsSource -Directory | ForEach-Object {
    $Dest = Join-Path $TargetDir $_.Name
    if (Test-Path $Dest) {
        if (-not $Force) {
            Write-Warning "Skill já existe e foi preservada (use -Force para sobrescrever): $Dest"
            $Skipped++
            return
        }
        Remove-Item -Recurse -Force $Dest
    }
    Copy-Item -Recurse -Force $_.FullName $Dest
    Get-ChildItem -Path $Dest -Recurse -Force -Include "__pycache__", "*.pyc" -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Skill instalada: $($_.Name) -> $Dest"
    $Installed++
}

Write-Host "`nResumo: $Installed instalada(s), $Skipped preservada(s) em $TargetDir"
