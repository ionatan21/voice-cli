@echo off
REM Voice CLI - Wrapper para Windows
REM Este archivo permite ejecutar 'voice' en Windows

REM Obtener directorio del script
set SCRIPT_DIR=%~dp0

REM Ejecutar el comando voice con Python
python "%SCRIPT_DIR%voice" %*