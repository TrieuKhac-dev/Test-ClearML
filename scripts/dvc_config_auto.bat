@echo off
REM Detect if running on Windows or not
setlocal EnableDelayedExpansion
ver | find "Windows" >nul
if %ERRORLEVEL%==0 (
    powershell -ExecutionPolicy Bypass -File scripts/dvc_config_env.ps1 %*
) else (
    sh scripts/dvc_config_env.sh "$@"
)