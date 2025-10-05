@echo off
REM Script di setup rapido per Windows
REM Installa le dipendenze e testa la compatibilità

echo ========================================
echo Audio Manager Teatrale - Setup Windows
echo ========================================
echo.

REM Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo.
    echo Scarica e installa Python 3.8+ da: https://www.python.org/downloads/
    echo IMPORTANTE: Durante l'installazione, seleziona "Add Python to PATH"
    pause
    exit /b 1
)

echo Python trovato: 
python --version
echo.

echo [1/3] Aggiornamento pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Installazione dipendenze...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERRORE: Installazione fallita!
    echo Verifica la connessione internet e riprova.
    pause
    exit /b 1
)

echo.
echo [3/3] Test compatibilità...
python test_compatibility.py

if errorlevel 1 (
    echo.
    echo ATTENZIONE: Il test ha rilevato alcuni problemi.
    echo Controlla i messaggi sopra per dettagli.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completato con successo!
echo ========================================
echo.
echo Per avviare l'applicazione:
echo   python main.py
echo.
echo Per creare un eseguibile standalone:
echo   build.bat
echo.
pause
