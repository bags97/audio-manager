#!/bin/bash
# Script di build per macOS e Linux
# Crea un eseguibile standalone di Audio Manager

set -e  # Esci in caso di errore

echo "======================================"
echo "Audio Manager Teatrale - Build Unix"
echo "======================================"
echo ""

# Controlla se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "ERRORE: Python 3 non trovato! Installa Python 3.8+"
    exit 1
fi

echo "Python trovato: $(python3 --version)"
echo ""

echo "[1/4] Installazione dipendenze..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "[2/4] Pulizia build precedenti..."
rm -rf build dist

echo ""
echo "[3/4] Creazione eseguibile con PyInstaller..."
python3 -m PyInstaller --clean audio_manager.spec

echo ""
echo "[4/4] Build completata!"
echo ""

# Messaggio specifico per piattaforma
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Applicazione creata in: dist/AudioManager.app"
    echo ""
    echo "Per testare l'applicazione, esegui: open dist/AudioManager.app"
else
    echo "Eseguibile creato in: dist/AudioManager"
    echo ""
    echo "Per testare l'applicazione, esegui: ./dist/AudioManager"
    chmod +x dist/AudioManager
fi

echo ""
echo "Build completata con successo!"
