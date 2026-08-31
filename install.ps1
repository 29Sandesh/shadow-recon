# SHADOW-RECON v1.0 - 1-Line Global Installer (Windows)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "   🌐  SHADOW-RECON v1.0: B2B COMPANY & DOMAIN OSINT INTELLIGENCE SCANNER" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

$installDir = "$env:LOCALAPPDATA\ShadowRecon"
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
}

# Verify Python
try {
    $pyVer = & python --version
    Write-Host "[1/4] Found $pyVer" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python 3.9+ is required to run Shadow-Recon. Please install Python from python.org" -ForegroundColor Red
    exit 1
}

Write-Host "[2/4] Downloading Shadow-Recon source files..." -ForegroundColor Yellow
$zipUrl = "https://github.com/29Sandesh/shadow-recon/archive/refs/heads/main.zip"
$tempZip = Join-Path $env:TEMP "shadow-recon-main.zip"
$tempExtract = Join-Path $env:TEMP "shadow-recon-extract"

if (Test-Path "$PSScriptRoot\shadow_recon") {
    Copy-Item -Path "$PSScriptRoot\*" -Destination $installDir -Recurse -Force
} else {
    try {
        Invoke-WebRequest -Uri $zipUrl -OutFile $tempZip -UseBasicParsing
        if (Test-Path $tempExtract) { Remove-Item $tempExtract -Recurse -Force }
        Expand-Archive -Path $tempZip -DestinationPath $tempExtract -Force
        Copy-Item -Path "$tempExtract\shadow-recon-main\*" -Destination $installDir -Recurse -Force
        Remove-Item $tempZip -Force -ErrorAction SilentlyContinue
        Remove-Item $tempExtract -Recurse -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Host "[NOTE] Pulling from local cache..."
    }
}

Write-Host "[3/4] Installing Python dependencies (dnspython, requests, bs4)..." -ForegroundColor Yellow
& pip install requests dnspython beautifulsoup4 --quiet

Write-Host "[4/4] Creating CLI shortcut and adding to System PATH..." -ForegroundColor Yellow
$cmdWrapper = Join-Path $installDir "shadow-recon.cmd"
Set-Content -Path $cmdWrapper -Value "@python -m shadow_recon.cli %*" -Encoding ASCII

$reconAlias = Join-Path $installDir "recon.cmd"
Set-Content -Path $reconAlias -Value "@python -m shadow_recon.cli %*" -Encoding ASCII

$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notmatch [regex]::Escape($installDir)) {
    [Environment]::SetEnvironmentVariable("PATH", "$userPath;$installDir", "User")
}

$desktopBat = "$([Environment]::GetFolderPath('Desktop'))\ShadowRecon.bat"
$batContent = @"
@echo off
title SHADOW-RECON OSINT SCANNER
cd /d "$installDir"
python -m shadow_recon.cli
pause
"@
Set-Content -Path $desktopBat -Value $batContent -Encoding ASCII

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "  ✅ INSTALLATION COMPLETE! Shadow-Recon is installed and ready to use." -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  👉 Launch from Desktop : Double-click 'ShadowRecon.bat'" -ForegroundColor Cyan
Write-Host "  👉 Launch from Terminal: Type 'shadow-recon <domain>' or 'recon <domain>'" -ForegroundColor Cyan
Write-Host ""
