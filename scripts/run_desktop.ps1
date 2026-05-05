$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $projectRoot

Write-Host "=============================================="
Write-Host "ICT Master Suite Premium - Desktop Runner PS"
Write-Host "=============================================="

$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

Write-Host "[1/4] Verificando ambiente virtual..."
if (-not (Test-Path $venvPython)) {
    Write-Host ".venv nao encontrado. Criando ambiente virtual..."
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao criar .venv com 'python -m venv .venv'."
    }
}

if (-not (Test-Path $venvPython)) {
    throw "Python da venv nao encontrado em '.venv\Scripts\python.exe'."
}

Write-Host "[2/4] Atualizando pip..."
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao atualizar pip."
}

Write-Host "[3/4] Instalando dependencias..."
& $venvPython -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao instalar requirements."
}

Write-Host "[4/4] Executando app desktop..."
$start = Get-Date
& $venvPython run_desktop.py
$exitCode = $LASTEXITCODE
$elapsed = ((Get-Date) - $start).TotalSeconds

if ($exitCode -ne 0) {
    Write-Error "Aplicacao encerrou com codigo $exitCode."
    if (Test-Path "crash_log.txt") {
        Write-Host "Verifique crash_log.txt para diagnostico."
    }
    exit $exitCode
}

if ($elapsed -lt 2) {
    Write-Host "Aviso: a aplicacao encerrou rapidamente ($([math]::Round($elapsed, 2))s)." -ForegroundColor Yellow
    if (Test-Path "crash_log.txt") {
        Write-Host "Verifique crash_log.txt para diagnostico."
    }
}

Write-Host "[OK] Execucao finalizada."
