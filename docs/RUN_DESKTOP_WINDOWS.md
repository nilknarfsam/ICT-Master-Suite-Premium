# Executar Desktop no Windows

Este guia padroniza a execucao local do app desktop Premium em Windows sem depender de ativacao manual da venv.

## Opcao recomendada (CMD/BAT)

Use o runner oficial:

- `scripts\run_desktop.bat`

Esse script:

- cria `.venv` se nao existir
- instala/atualiza dependencias de `requirements.txt`
- executa `run_desktop.py` com `.venv\Scripts\python.exe`
- mantem o terminal aberto ao final (`pause`)

## PowerShell

Execute com bypass de policy:

- `powershell -ExecutionPolicy Bypass -File scripts\run_desktop.ps1`

Observacoes:

- o script **nao depende** de ativar venv
- ele usa diretamente `.venv\Scripts\python.exe`
- caso o app feche imediatamente, avisa no terminal e orienta checar `crash_log.txt`

## Manual (avancado)

- `.venv\Scripts\python.exe run_desktop.py`

## Sobre ativacao da venv no PowerShell

No PowerShell, o ativador correto e:

- `.venv\Scripts\Activate.ps1`

Nao use `.\.venv\Scripts\activate` no PowerShell (esse nome e comum em outros shells).

## Dica importante

Nao execute `.\run_desktop.py` diretamente, pois o Windows pode associar `.py` a outro aplicativo.
Prefira sempre chamar via Python:

- `.venv\Scripts\python.exe run_desktop.py`
