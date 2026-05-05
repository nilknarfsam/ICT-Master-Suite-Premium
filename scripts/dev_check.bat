@echo off
setlocal

echo [1/3] Compilando modulos Python...
python -m compileall src
if errorlevel 1 goto :error

echo [2/3] Executando smoke check...
python scripts/smoke_check.py
if errorlevel 1 goto :error

echo [3/3] Executando testes...
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo pytest nao instalado. Rode: pip install pytest
) else (
    python -m pytest tests
    if errorlevel 1 goto :error
)

echo.
echo DEV CHECK CONCLUIDO COM SUCESSO.
exit /b 0

:error
echo.
echo DEV CHECK FALHOU.
exit /b 1
