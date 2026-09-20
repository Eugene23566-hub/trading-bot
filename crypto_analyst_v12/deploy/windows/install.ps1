$ErrorActionPreference = "Stop"
$Repo = "https://github.com/Eugene23566-hub/trading-bot.git"
$Tmp = Join-Path $env:TEMP "crypto-analyst-repo"
$App = "C:\CryptoAnalyst"

function Need($cmd) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        throw "$cmd is not installed or not in PATH."
    }
}

Need git
if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is not installed or not in PATH."
}

if (Test-Path $Tmp) { Remove-Item $Tmp -Recurse -Force }
git clone --depth 1 $Repo $Tmp

if (-not (Test-Path $App)) { New-Item -ItemType Directory -Path $App | Out-Null }
robocopy "$Tmp\crypto_analyst_v12" $App /MIR /XD ".venv" "state" "secrets" /XF ".env" | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed with exit code $LASTEXITCODE" }

New-Item -ItemType Directory -Force -Path "$App\state","$App\secrets" | Out-Null

if (Get-Command py -ErrorAction SilentlyContinue) {
    py -3 -m venv "$App\.venv"
} else {
    python -m venv "$App\.venv"
}

& "$App\.venv\Scripts\python.exe" -m pip install --upgrade pip
& "$App\.venv\Scripts\python.exe" -m pip install -r "$App\requirements.txt"

if (-not (Test-Path "$App\.env")) {
    Copy-Item "$App\.env.example" "$App\.env"
}

$TaskName = "Crypto Analyst v1.2"
$Cmd = "$App\deploy\windows\run_cycle.cmd"
schtasks.exe /Create /TN $TaskName /TR $Cmd /SC MINUTE /MO 15 /F | Out-Null

Write-Host ""
Write-Host "Installed to $App"
Write-Host "Next:"
Write-Host "1. notepad C:\CryptoAnalyst\.env"
Write-Host "2. Put OPENAI_API_KEY in the file and save it."
Write-Host "3. Test once:"
Write-Host "   C:\CryptoAnalyst\.venv\Scripts\python.exe C:\CryptoAnalyst\run_cycle.py"
Write-Host "4. Check task:"
Write-Host '   schtasks /Query /TN "Crypto Analyst v1.2" /V /FO LIST'
