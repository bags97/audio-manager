@echo off
REM Script di build per Windows
REM Crea un eseguibile standalone di Audio Manager

echo ======================================
echo Audio Manager Teatrale - Build Windows
echo ======================================
echo.

REM Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato! Installa Python 3.8+ da python.org
    pause
    exit /b 1
)

echo [1/4] Installazione dipendenze...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo ERRORE: Installazione dipendenze fallita!
    pause
    exit /b 1
)

echo.
echo [2/4] Pulizia build precedenti...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [3/4] Creazione eseguibile con PyInstaller...
python -m PyInstaller --clean audio_manager.spec

if errorlevel 1 (
    echo ERRORE: Build fallita!
    pause
    exit /b 1
)

echo.
echo [4/4] Build completata!
echo.
echo Eseguibile creato in: dist\AudioManager.exe
echo.
echo Per testare l'applicazione, esegui: dist\AudioManager.exe
echo.
pause
