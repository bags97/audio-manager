#!/bin/bash
# Script di setup rapido per macOS e Linux
# Installa le dipendenze e testa la compatibilità

set -e  # Esci in caso di errore

echo "========================================"
echo "Audio Manager Teatrale - Setup Unix"
echo "========================================"
echo ""

# Determina il comando Python corretto
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERRORE: Python 3 non trovato!"
    echo ""
    echo "Installa Python 3.8+ per il tuo sistema:"
    echo "  macOS:  brew install python3"
    echo "  Ubuntu: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

echo "Python trovato: $($PYTHON_CMD --version)"
echo ""

# Verifica versione Python
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "ERRORE: Python $PYTHON_VERSION trovato, ma serve almeno Python $REQUIRED_VERSION"
    exit 1
fi

echo "[1/3] Aggiornamento pip..."
$PYTHON_CMD -m pip install --upgrade pip

echo ""
echo "[2/3] Installazione dipendenze..."
$PYTHON_CMD -m pip install -r requirements.txt

echo ""
echo "[3/3] Test compatibilità..."
$PYTHON_CMD test_compatibility.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ATTENZIONE: Il test ha rilevato alcuni problemi."
    echo "Controlla i messaggi sopra per dettagli."
    exit 1
fi

echo ""
echo "========================================"
echo "Setup completato con successo!"
echo "========================================"
echo ""
echo "Per avviare l'applicazione:"
echo "  $PYTHON_CMD main.py"
echo ""
echo "Per creare un eseguibile standalone:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "  ./build.sh"
else
    echo "  chmod +x build.sh"
    echo "  ./build.sh"
fi
echo ""
