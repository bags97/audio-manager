# 🏗️ Prima Build - Istruzioni

## 📋 Prerequisiti Verificati

✅ Codice Python compatibile multi-piattaforma  
✅ PyInstaller configurato (audio_manager.spec)  
✅ Build scripts pronti (build.bat / build.sh)  
✅ Test di compatibilità funzionante  
✅ Documentazione completa  

## 🚀 Procedura Prima Build

### 1️⃣ Windows

**Apri PowerShell o CMD nella cartella del progetto:**

```cmd
# Assicurati di essere nella cartella corretta
cd C:\PROJECTS\PLATEA\audio-manager

# Esegui lo script di build
build.bat

# Attendi 2-5 minuti...

# Se tutto va bene, troverai:
# dist\AudioManager.exe (~120 MB)
```

**Test dell'eseguibile:**
```cmd
# Testa l'eseguibile appena creato
dist\AudioManager.exe
```

### 2️⃣ macOS (quando disponibile)

**Apri Terminal:**

```bash
# Vai nella cartella del progetto
cd ~/path/to/audio-manager

# Rendi eseguibile lo script
chmod +x build.sh

# Esegui la build
./build.sh

# Attendi 2-5 minuti...

# Se tutto va bene, troverai:
# dist/AudioManager.app
```

**Test dell'applicazione:**
```bash
# Apri l'app appena creata
open dist/AudioManager.app
```

### 3️⃣ Linux (quando disponibile)

**Apri Terminal:**

```bash
# Vai nella cartella del progetto
cd ~/path/to/audio-manager

# Rendi eseguibile lo script
chmod +x build.sh

# Esegui la build
./build.sh

# Attendi 2-5 minuti...

# Se tutto va bene, troverai:
# dist/AudioManager
```

**Test del binario:**
```bash
# Esegui il binario appena creato
./dist/AudioManager
```

## 🧪 Verifica Build

Dopo ogni build, verifica:

1. **✓ Eseguibile creato**
   - Windows: `dist\AudioManager.exe` esiste
   - macOS: `dist\AudioManager.app` esiste
   - Linux: `dist\AudioManager` esiste

2. **✓ Dimensione ragionevole**
   - Windows: ~100-150 MB
   - macOS: ~150-200 MB
   - Linux: ~100-150 MB

3. **✓ Eseguibile funzionante**
   - Si apre senza errori
   - Interfaccia grafica appare
   - Dispositivi audio rilevati
   - Carica una traccia di test
   - Riproduzione funziona

4. **✓ Funzionalità complete**
   - Doppia uscita audio (main + preview)
   - Caricamento playlist
   - Salvataggio playlist
   - Waveform visualizzato (se matplotlib presente)
   - Hotkey funzionanti
   - Trim funzionante

## 🐛 Risoluzione Problemi Build

### Errore: "PyInstaller not found"

```bash
pip install pyinstaller
```

### Errore: "soundfile binary not found"

Build dovrebbe includere automaticamente libsndfile.
Se non funziona, reinstalla:
```bash
pip uninstall soundfile
pip install soundfile --no-cache-dir
```

### Errore: "matplotlib backend"

Matplotlib è opzionale. Se causa problemi:
1. Rimuovila da requirements.txt
2. Il programma funzionerà senza waveform

### Build fallisce senza messaggio chiaro

```bash
# Pulisci e riprova
rmdir /s /q build dist  # Windows
rm -rf build dist       # macOS/Linux

# Riprova con verbose
python -m PyInstaller --clean --log-level DEBUG audio_manager.spec
```

### Eseguibile si apre e si chiude subito

Prova ad eseguire da terminale per vedere errori:
```bash
# Windows
dist\AudioManager.exe

# macOS
dist/AudioManager.app/Contents/MacOS/AudioManager

# Linux
./dist/AudioManager
```

## 📦 Distribuzione Post-Build

Una volta che la build funziona:

1. **Comprimi eseguibile (opzionale):**
   ```bash
   # Windows
   # Usa 7-Zip o WinRAR: AudioManager-v1.0.0-Windows.zip
   
   # macOS
   zip -r AudioManager-v1.0.0-macOS.zip dist/AudioManager.app
   
   # Linux
   tar -czf AudioManager-v1.0.0-Linux.tar.gz dist/AudioManager
   ```

2. **Carica su GitHub Release:**
   - Vai su GitHub → Releases → New Release
   - Tag: `v1.0.0`
   - Titolo: "Audio Manager Teatrale v1.0.0"
   - Descrizione: Note di release
   - Allega i file compressi per ogni OS

3. **Testa su macchina pulita:**
   - Scarica l'eseguibile
   - Esegui su PC senza Python/dipendenze
   - Verifica tutto funziona

## 📊 Checklist Prima Release

Prima di rilasciare ufficialmente:

- [ ] Build completata su tutti gli OS target
- [ ] Eseguibili testati su macchine pulite
- [ ] Tutte le funzionalità verificate
- [ ] Documentazione aggiornata
- [ ] README con link download
- [ ] FAQ completa
- [ ] Licenza MIT inclusa
- [ ] .gitignore aggiornato
- [ ] Tag versione in Git
- [ ] GitHub Release creata

## 🎯 Build Completata!

Se tutte le verifiche passano:

✅ **Hai un'applicazione completamente portable!**

Gli utenti possono:
- Scaricare l'eseguibile
- Eseguire senza installare nulla
- Usare immediatamente per spettacoli teatrali

## 📝 Note Finali

- **Dimensione:** ~120-150 MB è normale (include Python + librerie)
- **Velocità:** Prima apertura può essere lenta (decompressione)
- **Aggiornamenti:** Per aggiornare, basta sostituire l'eseguibile
- **Portabilità:** Funziona anche da USB stick

---

**Buona build!** 🏗️✨
