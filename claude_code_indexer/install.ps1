# PowerShell installer for Claude Code Indexer
# Usage: Run in PowerShell as Administrator

Write-Host "🚀 Installing Claude Code Indexer..." -ForegroundColor Cyan

# Check Python
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
            Write-Host "❌ Python 3.8+ required. You have $pythonVersion" -ForegroundColor Red
            exit 1
        }
        Write-Host "✅ $pythonVersion detected" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Install package
Write-Host "📦 Installing package..." -ForegroundColor Yellow
python -m pip install --user git+https://github.com/tuannx/claude-prompts.git#subdirectory=claude_code_indexer

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Installation failed" -ForegroundColor Red
    exit 1
}

# Add to PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$pythonScripts = "$env:APPDATA\Python\Python3*\Scripts"

if ($userPath -notlike "*$pythonScripts*") {
    Write-Host "🔧 Adding Python Scripts to PATH..." -ForegroundColor Yellow
    $newPath = "$userPath;$pythonScripts"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Create batch file for easy access
$batchContent = @"
@echo off
python -m claude_code_indexer.cli %*
"@

$batchPath = "$env:USERPROFILE\cci.bat"
Set-Content -Path $batchPath -Value $batchContent
Write-Host "✅ Created $batchPath" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  cci --help"
Write-Host "  cci index ."
Write-Host "  cci doctor"
Write-Host ""
Write-Host "If 'cci' not found, use:" -ForegroundColor Yellow
Write-Host "  python -m claude_code_indexer.cli --help"