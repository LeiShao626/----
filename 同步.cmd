@echo off
cd /d "%~dp0"
echo.
where pwsh >nul 2>&1
if %errorlevel%==0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1"
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1"
)
echo.
echo ----------------------------------------
echo Press any key to close this window...
pause >nul
