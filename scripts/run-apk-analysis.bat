@echo off
setlocal
cd /d "%~dp0\.."

set ANALYZER=..\analyze_apks.py
set INPUT_DIR=IdleHeroTD-apk
set OUTPUT_DIR=IdleHeroTD-apk\apk_analysis

if not exist "%ANALYZER%" (
  echo Could not find analyze_apks.py at workspace root: %CD%\%ANALYZER%
  exit /b 1
)

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%ANALYZER%" --input "%INPUT_DIR%" --output "%OUTPUT_DIR%"
  goto done
)

where python >nul 2>nul
if %errorlevel%==0 (
  python "%ANALYZER%" --input "%INPUT_DIR%" --output "%OUTPUT_DIR%"
  goto done
)

where python3 >nul 2>nul
if %errorlevel%==0 (
  python3 "%ANALYZER%" --input "%INPUT_DIR%" --output "%OUTPUT_DIR%"
  goto done
)

echo Python 3 was not found. Install Python 3 or add it to PATH.
exit /b 1

:done
echo.
echo Done. Open %OUTPUT_DIR%\SUMMARY.md
echo Also check %OUTPUT_DIR%\mechanics_candidates.md
endlocal
