# Guida Rapida Build & Distribuzione

## 🚀 Setup Iniziale

### Windows
```cmd
setup.bat
```

### macOS / Linux
```bash
chmod +x setup.sh
./setup.sh
```

Lo script di setup esegue automaticamente:
1. Verifica installazione Python 3.8+
2. Installa tutte le dipendenze da `requirements.txt`
3. Testa la compatibilità del sistema

## 📦 Creazione Eseguibili

### Windows (.exe)
```cmd
build.bat
```
**Output:** `dist/AudioManager.exe` (circa 100-150 MB)

### macOS (.app)
```bash
./build.sh
```
**Output:** `dist/AudioManager.app` (bundle macOS)

### Linux (binario)
```bash
./build.sh
```
**Output:** `dist/AudioManager` (eseguibile Linux)

## 📋 Distribuzione

### Opzione 1: Eseguibile Singolo (Raccomandato)
Distribuisci solo il file dalla cartella `dist/`:
- **Windows:** `AudioManager.exe`
- **macOS:** `AudioManager.app` (bundle completo)
- **Linux:** `AudioManager`

**Vantaggi:**
- ✅ Nessuna installazione richiesta
- ✅ Tutte le dipendenze incluse
- ✅ Funziona out-of-the-box
- ✅ Dimensione ragionevole (100-150 MB)

### Opzione 2: Sorgente Python
Distribuisci l'intera cartella del progetto:
```
audio-manager/
├── main.py
├── audio_manager.py
├── playlist_manager.py
├── auto_backup.py
├── requirements.txt
└── README.md
```

**Istruzioni per utenti finali:**
1. Installa Python 3.8+
2. Esegui `pip install -r requirements.txt`
3. Lancia con `python main.py`

**Vantaggi:**
- ✅ Codice modificabile
- ✅ Dimensione ridotta
- ✅ Aggiornamenti facili

**Svantaggi:**
- ❌ Richiede Python installato
- ❌ Setup più complesso per utenti non tecnici

## 🔧 Test Prima della Distribuzione

### Test Compatibilità
```bash
python test_compatibility.py
```

Verifica:
- ✓ Tutte le dipendenze installate
- ✓ Dispositivi audio disponibili
- ✓ Versione Python corretta

### Test Funzionale
1. Avvia l'applicazione
2. Configura dispositivi audio (main + preview)
3. Carica una traccia di test
4. Verifica playback su entrambi i canali
5. Testa salvataggio/caricamento playlist
6. Verifica tutte le feature (trim, hotkey, loop, etc.)

## 📝 Checklist Distribuzione

Prima di rilasciare una nuova versione:

- [ ] Esegui `test_compatibility.py` su ogni OS target
- [ ] Verifica build su Windows, macOS, Linux
- [ ] Testa eseguibili su macchine pulite (senza Python)
- [ ] Controlla dimensione eseguibili (< 200 MB)
- [ ] Valida funzionalità complete
- [ ] Aggiorna `README.md` con note versione
- [ ] Tagga versione in Git: `git tag v1.0.0`

## 🌍 Compatibilità Testata

### Sistemi Operativi
| OS | Versione | Status |
|----|----------|--------|
| Windows 10 | 64-bit | ✅ Testato |
| Windows 11 | 64-bit | ✅ Testato |
| macOS Big Sur | 11.x | ✅ Compatibile |
| macOS Monterey | 12.x | ✅ Compatibile |
| macOS Ventura | 13.x | ✅ Compatibile |
| Ubuntu | 20.04+ | ✅ Compatibile |
| Debian | 11+ | ✅ Compatibile |
| Fedora | 35+ | ✅ Compatibile |

### Architetture
- ✅ x86_64 (Intel/AMD 64-bit)
- ✅ ARM64 (Apple Silicon M1/M2/M3)
- ⚠️ ARM32 (Raspberry Pi - non testato)

## 🐛 Risoluzione Problemi Build

### Windows: "PyInstaller non trovato"
```cmd
python -m pip install --upgrade pyinstaller
```

### macOS: "Permission denied"
```bash
chmod +x build.sh
./build.sh
```

### Linux: "libsndfile not found"
```bash
# Ubuntu/Debian
sudo apt install libsndfile1

# Fedora
sudo dnf install libsndfile
```

### Errore "matplotlib backend"
Se matplotlib causa problemi, il programma funziona comunque senza visualizzazione waveform.
Per disabilitare completamente matplotlib, rimuovila da `requirements.txt`.

### Eseguibile troppo grande
L'eseguibile include Python completo e tutte le librerie. Per ridurre la dimensione:
1. Rimuovi matplotlib da `requirements.txt` (risparmia ~50 MB)
2. Usa `upx=True` in `audio_manager.spec` (compressione)

## 📊 Dimensioni Attese

| Componente | Dimensione |
|------------|------------|
| Sorgente Python | ~100 KB |
| Dipendenze installate | ~300 MB |
| Eseguibile Windows | ~120 MB |
| Eseguibile macOS | ~150 MB |
| Eseguibile Linux | ~130 MB |

## 🔄 Aggiornamenti

Per rilasciare un aggiornamento:

1. Modifica il codice
2. Testa su tutti gli OS target
3. Incrementa versione in `main.py` (se presente)
4. Rebuilda gli eseguibili: `build.bat` / `./build.sh`
5. Distribuisci i nuovi eseguibili

Gli utenti possono semplicemente sostituire il vecchio eseguibile con quello nuovo.

## 📦 Packaging Opzionale

### Installer Windows (NSIS)
Per creare un installer `.exe` professionale:
```
pip install pynsist
pynsist installer.cfg
```

### DMG macOS
Per creare un'immagine disco `.dmg`:
```bash
hdiutil create -volname "Audio Manager" -srcfolder dist/AudioManager.app -ov -format UDZO AudioManager.dmg
```

### AppImage Linux
Per creare un AppImage portable:
```bash
# Usa appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
./appimagetool-x86_64.AppImage dist/AudioManager
```

## 📞 Supporto

Per problemi di build o distribuzione, controlla:
1. Log di build nella cartella `build/`
2. Warnings di PyInstaller
3. `test_compatibility.py` su sistema target
