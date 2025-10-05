# Script di installazione per Windows
# Esegui questo file per installare tutte le dipendenze

@echo off
echo ==========================================
echo Audio Manager - Installazione Dipendenze
echo ==========================================
echo.

echo Controllo Python...
python --version
if %errorlevel% neq 0 (
    echo ERRORE: Python non trovato!
    echo Installa Python da https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Installazione dipendenze...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ==========================================
echo Installazione completata!
echo ==========================================
echo.
echo Per avviare il programma esegui: python main.py
echo.
pause
