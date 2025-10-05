# 🎭 Audio Manager Teatrale

Sistema professionale di gestione audio per spettacoli teatrali con doppia uscita audio (main + preview), playlist avanzate, waveform visualization e controlli professionali.

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

## 🌟 Funzionalità Principali

### 🔊 Audio
- **Doppia Uscita**: Output principale (jack) + Preview (Bluetooth/altro device)
- **Formati Supportati**: MP3, WAV, OGG, FLAC
- **Controllo Volume**: Indipendente per main e preview, anche per singola traccia
- **Trim Non-Distruttivo**: Taglia tracce senza modificare file originali
- **Loop Mode**: Ripetizione automatica di tracce specifiche

### 📋 Playlist & Organizzazione
- **Gestione Completa**: Aggiungi, rimuovi, riordina, inverti
- **Color Coding**: Etichette colorate per categorizzazione visiva
- **Note per Traccia**: Appunti e cue per ogni traccia
- **Hotkey F1-F12 e 1-9**: Accesso rapido alle tracce
- **Auto-Assign F1-F12**: Assegnazione automatica in ordine

### 💾 Persistenza & Backup
- **Salva/Carica Playlist**: Configurazioni complete in formato JSON
- **Auto-Backup**: Salvataggio automatico ogni 5 minuti
- **Configurazione Audio**: Dispositivi salvati nella playlist
- **Restore Session**: Ripristina l'ultima sessione all'avvio

### 🎨 Interfaccia
- **Dark Theme**: Ottimizzata per uso teatrale al buio
- **Waveform Real-time**: Visualizzazione con indicatore di posizione rosso
- **Controlli Professionali**: Play, Pause, Stop, Preview, Skip
- **Visualizzazione Dettagliata**: Tabella con 8 colonne informative

## 📦 Installazione

### Opzione 1: Eseguibile Standalone (Raccomandato)

**Nessuna installazione richiesta!** Scarica l'eseguibile per il tuo sistema operativo:

| Sistema | File | Download |
|---------|------|----------|
| 🪟 Windows | `AudioManager.exe` | [Crea con build.bat](#build-eseguibile) |
| 🍎 macOS | `AudioManager.app` | [Crea con build.sh](#build-eseguibile) |
| 🐧 Linux | `AudioManager` | [Crea con build.sh](#build-eseguibile) |

### Opzione 2: Esegui da Sorgente Python

**Requisiti:**
- Python 3.8 o superiore
- pip (gestore pacchetti Python)

**Setup:**
```bash
# Installa le dipendenze
pip install -r requirements.txt

# Esegui l'applicazione
python main.py
```

## 🚀 Build Eseguibile

Per creare un eseguibile standalone per il tuo sistema operativo:

### Windows
```cmd
build.bat
```

### macOS / Linux
```bash
chmod +x build.sh
./build.sh
```

L'eseguibile sarà creato in `dist/AudioManager` (o `dist/AudioManager.exe` su Windows, `dist/AudioManager.app` su macOS).

**Lo script esegue automaticamente:**
1. Installazione dipendenze
2. Pulizia build precedenti
3. Creazione eseguibile con PyInstaller
4. Validazione del risultato

## 📖 Guida Utilizzo

### Primo Avvio

1. **Configura Dispositivi Audio:**
   - Seleziona dispositivo principale (es. uscita jack)
   - Seleziona dispositivo preview (es. Bluetooth)
   - Le impostazioni vengono salvate con la playlist

2. **Carica Tracce:**
   - Click su "➕ Aggiungi"
   - Seleziona file audio (MP3, WAV, OGG, FLAC)
   - Le tracce vengono precaricate in memoria

3. **Organizza Playlist:**
   - Riordina con "⬆️ Su" / "⬇️ Giù"
   - Inverti ordine con "🔄 Inverti"
   - Auto-assegna hotkey con "Auto F1-F12"

### Controlli Principali

| Pulsante | Funzione |
|----------|----------|
| ▶️ Play | Riproduzione su output principale |
| 👂 Preview | Riproduzione su output preview |
| ⏸️ Pausa | Pausa/Riprendi |
| ⏹️ Stop | Ferma riproduzione |
| ⏮️ Prev / ⏭️ Next | Traccia precedente/successiva |
| ✂️ Taglia | Imposta punto inizio/fine traccia |
| ✏️ Modifica | Modifica note, colore, volume |
| ⌨️ Hotkey | Assegna tasto rapido |
| 🔁 Loop | Attiva/disattiva ripetizione |

### Hotkey Globali

| Tasto | Funzione |
|-------|----------|
| **Spazio** | Play/Pausa |
| **S** | Stop |
| **P** | Preview |
| **←** | Traccia precedente |
| **→** | Traccia successiva |
| **F1-F12** | Salta a traccia assegnata |
| **1-9** | Salta a traccia 1-9 |

### Funzioni Avanzate

#### ✂️ Trim (Taglia Traccia)
Taglia tracce senza modificare i file originali:
1. Seleziona traccia → "✂️ Taglia"
2. Imposta inizio/fine in secondi
3. La traccia si riproduce solo nella sezione selezionata

#### 🎨 Color Coding & Note
Organizza visivamente le tracce:
- **Rosso**: Emergenze, effetti critici
- **Verde**: Musica di sottofondo
- **Blu**: Effetti atmosferici
- **Giallo**: Transizioni
- Aggiungi note con cue scenici

#### 💾 Salvataggio Sessione
La playlist salva **tutto**:
- Tracce e ordine
- Dispositivi audio configurati
- Volumi main/preview per traccia
- Note, colori, hotkey
- Trim settings
- Loop mode

## 🔧 Risoluzione Problemi

### Nessun Suono
1. Verifica dispositivi audio selezionati
2. Controlla volume sistema operativo
3. Prova a ricaricare la playlist

### Latenza Elevata
1. Su Windows usa driver ASIO se disponibile
2. Chiudi altre applicazioni audio
3. Usa file WAV invece di MP3

### File MP3 Non Supportati
Su alcuni sistemi potrebbe servire ffmpeg:
- **Windows**: Generalmente funziona out-of-the-box
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## 📁 Struttura Progetto

```
audio-manager/
├── main.py                # GUI principale
├── audio_manager.py       # Engine audio doppia uscita
├── playlist_manager.py    # Gestione playlist
├── auto_backup.py         # Sistema backup
├── requirements.txt       # Dipendenze Python
├── audio_manager.spec     # Config PyInstaller
├── build.bat             # Build Windows
├── build.sh              # Build macOS/Linux
├── README.md             # Documentazione
└── backups/              # Backup automatici
```

## 🌍 Compatibilità

### Sistemi Operativi Testati
- ✅ Windows 10/11 (64-bit)
- ✅ macOS 11+ (Intel e Apple Silicon)
- ✅ Ubuntu 20.04+
- ✅ Debian 11+
- ✅ Fedora 35+

### Dipendenze
- Python 3.8+
- sounddevice 0.4.6+
- soundfile 0.12.1+
- numpy 1.24+
- matplotlib 3.7+
- tkinter (incluso in Python)

## 📜 Licenza

MIT License - Libero per uso personale e commerciale

## 🙏 Crediti

Sviluppato con ❤️ per la comunità teatrale italiana

---

**Note Tecniche:**
- Testato con playlist fino a 100 tracce
- File audio fino a 30 minuti
- Aggiornamento waveform real-time a 10Hz
- Auto-backup ogni 5 minuti (ultimi 10 backup conservati)
