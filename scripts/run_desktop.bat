@echo off
setlocal

cd /d "%~dp0\.."

echo ==============================================
echo ICT Master Suite Premium - Desktop Runner
echo ==============================================
echo [1/4] Verificando ambiente virtual...
if not exist ".venv\Scripts\python.exe" (
    echo .venv nao encontrado. Criando ambiente virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar .venv com "python -m venv .venv".
        goto :end
    )
) else (
    echo .venv encontrado.
)

echo [2/4] Atualizando pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERRO] Falha ao atualizar pip.
    goto :end
)

echo [3/4] Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar requirements.
    goto :end
)

echo [4/4] Executando app desktop...
".venv\Scripts\python.exe" run_desktop.py
set "APP_EXIT=%ERRORLEVEL%"

if not "%APP_EXIT%"=="0" (
    echo [ERRO] Aplicacao encerrou com codigo %APP_EXIT%.
    if exist "crash_log.txt" (
        echo Verifique crash_log.txt para diagnostico.
    )
) else (
    echo [OK] Execucao finalizada com sucesso.
)

:end
echo.
pause
endlocal
