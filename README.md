# Audio Manager - Gestione Tracce Audio Teatrali

## Descrizione
Applicazione Windows per la gestione professionale delle tracce audio durante spettacoli teatrali.

## Funzionalità
- 🔊 **Dual Output**: Uscita principale (Jack audio) + Preview (Bluetooth)
- 📋 **Playlist Management**: Caricamento e riordino tracce audio
- ⏯️ **Controlli Playback**: Play, Pause, Stop, Skip
- 👁️ **Preview Mode**: Ascolta in anteprima senza inviare al pubblico
- 💾 **Precaricamento**: Carica tutte le tracce in memoria per transizioni veloci
- 🎚️ **Controllo Volume**: Regolazione indipendente per entrambe le uscite
- 🏷️ **Note/Marker**: Aggiungi note descrittive a ogni traccia (es: "Scena 2")
- 🎨 **Colori Tracce**: Evidenzia tracce per categoria con colori personalizzati
- 🔁 **Loop Mode**: Ripeti automaticamente tracce specifiche
- ⌨️ **Hotkeys Personalizzabili**: Assegna tasti (1-9, F1-F12) a tracce per avvio rapido
- 💾 **Backup Automatico**: Salvataggio automatico ogni 5 minuti con ripristino
- 📊 **Visualizzazione Waveform**: Forma d'onda della traccia corrente

## Installazione

### Requisiti
- Windows 10/11
- Python 3.8 o superiore

### Setup
```bash
pip install -r requirements.txt
```

**Nota**: Per supportare file MP3/OGG/FLAC, il pacchetto `soundfile` potrebbe richiedere librerie di sistema aggiuntive:
- **Windows**: Funziona out-of-the-box
- In caso di problemi, usa file **WAV** (raccomandato per performance)

## Utilizzo
```bash
python main.py
```

### Configurazione Audio
1. Seleziona l'uscita principale (Jack) dal menu dispositivi
2. Seleziona l'uscita preview (Bluetooth) dal menu dispositivi
3. Carica le tracce audio tramite il pulsante "Aggiungi Tracce"
4. Riordina le tracce trascinandole nella lista
5. Usa i controlli per la riproduzione

## Comandi Tastiera
- `Spazio`: Play/Pause
- `S`: Stop
- `N`: Traccia successiva
- `P`: Traccia precedente
- `Ctrl+O`: Apri file audio
- `↑` / `↓`: Volume uscita principale (+/- 5%)
- `Ctrl+↑` / `Ctrl+↓`: Volume uscita preview (+/- 5%)
- `1-9`: Avvia traccia con hotkey assegnato
- `F1-F12`: Avvia traccia con hotkey assegnato

## Formati Supportati
- MP3
- WAV
- OGG
- FLAC

## Note
Per un'esperienza ottimale, assicurati che:
- I driver audio siano aggiornati
- Il dispositivo Bluetooth sia accoppiato prima di avviare l'app
- Le tracce audio siano ottimizzate per le performance (WAV raccomandato)
