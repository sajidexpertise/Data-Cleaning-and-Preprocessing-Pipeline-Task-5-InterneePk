@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Task 5 - Data Cleaning & Preprocessing

if /I "%~1"=="server" goto SERVER

echo ============================================================
echo  Internee.pk Task 5 - Data Cleaning ^& Preprocessing
echo  Author: Sajid Ali
echo ============================================================
echo.
if not exist "%~dp0index.html" (
  echo ERROR: index.html was not found in:
  echo %~dp0
  echo.
  pause
  exit /b 1
)

echo Opening the dashboard in your default browser...
start "" "%~dp0index.html"
echo.
echo Dashboard launched. If your browser blocks local files, run:
echo   OPEN_DASHBOARD.bat server
echo.
timeout /t 4 /nobreak >nul
exit /b 0

:SERVER
set "PYEXE="
if exist "C:\Python314\python.exe" set "PYEXE=C:\Python314\python.exe"
if defined PYEXE goto PYFOUND
where python >nul 2>nul && set "PYEXE=python"
if defined PYEXE goto PYFOUND
where py >nul 2>nul && set "PYEXE=py -3"
if defined PYEXE goto PYFOUND

echo ============================================================
echo ERROR: Python was not found.
echo ============================================================
echo Checked:
echo   C:\Python314\python.exe
echo   python command
echo   py -3 command
echo.
echo You do NOT need Python for normal use. Close this window and
 echo double-click index.html, or run OPEN_DASHBOARD.bat without "server".
echo.
pause
exit /b 1

:PYFOUND
echo Starting local server from:
echo %~dp0
echo Using Python: %PYEXE%
echo.
echo Dashboard URL: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server.
echo.
start "" "http://127.0.0.1:8000/"
%PYEXE% -m http.server 8000
if errorlevel 1 (
  echo.
  echo The local server stopped with an error.
  pause
)
endlocal
