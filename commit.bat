@echo off
setlocal EnableDelayedExpansion

echo.
set /p COMMIT_MSG=Digite a mensagem do commit: 

if "%COMMIT_MSG%"=="" (
    echo Mensagem vazia. Commit cancelado.
    exit /b 1
)

echo.
git status
if errorlevel 1 (
    echo Erro ao executar git status.
    exit /b 1
)

echo.
git add .
if errorlevel 1 (
    echo Erro ao executar git add .
    exit /b 1
)

echo.
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo Erro ao executar git commit.
    exit /b 1
)

echo.
set /p DO_PUSH=Deseja executar git push agora? (s/n): 
if /I "%DO_PUSH%"=="s" (
    git push
) else (
    echo Push ignorado.
)

endlocal
