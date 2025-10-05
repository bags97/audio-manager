# Guida Rapida - Audio Manager

## 🎭 Benvenuto nell'Audio Manager per Spettacoli Teatrali

### Prima Configurazione

1. **Installa le dipendenze**
   - Doppio click su `install.bat`
   - Oppure da terminale: `pip install -r requirements.txt`

2. **Avvia l'applicazione**
   - Doppio click su `run.bat`
   - Oppure da terminale: `python main.py`

### Configurazione Dispositivi Audio

1. **Uscita Principale (Jack)**
   - Seleziona l'uscita audio del PC (quella collegata agli altoparlanti/mixer)
   - Questa sarà l'uscita per il pubblico
   - **Regola il volume** con lo slider a destra

2. **Uscita Preview (Bluetooth)**
   - Seleziona il dispositivo Bluetooth (cuffie/auricolari)
   - Questa ti permetterà di ascoltare in anteprima
   - **Regola il volume** indipendentemente dall'uscita principale

### Come Usarlo

#### Caricare le Tracce
1. Click su "Aggiungi" o `File → Aggiungi Tracce`
2. Seleziona i file audio (MP3, WAV, OGG, FLAC)
3. Le tracce appariranno nella lista

#### Personalizzare le Tracce
- **📝 Note**: Aggiungi descrizioni (es: "Scena 2 - Ingresso protagonista")
- **🎨 Colore**: Assegna colori per categorizzare (musica, effetti, voce)
- **⌨️ Hotkey**: Assegna tasti rapidi (1-9 o F1-F12) per avvio immediato
- **🔁 Loop**: Attiva checkbox per ripetere automaticamente la traccia

#### Riordinare le Tracce
1. Seleziona una traccia
2. Usa i pulsanti "⬆ Su" e "⬇ Giù"
3. Oppure rimuovi con "➖ Rimuovi"

#### Riprodurre le Tracce
- **Play Main**: Riproduce sulla uscita principale (pubblico)
- **Preview**: Riproduce solo in cuffia (anteprima privata)
- **Pausa**: Mette in pausa
- **Stop**: Ferma completamente
- **Precedente/Successivo**: Cambia traccia

#### Scorciatoie Tastiera
- `Spazio`: Play/Pausa
- `S`: Stop
- `N`: Traccia successiva
- `P`: Traccia precedente
- `Ctrl+O`: Aggiungi tracce
- **`↑` / `↓`: Volume principale (+/- 5%)**
- **`Ctrl+↑` / `Ctrl+↓`: Volume preview (+/- 5%)**

### Salvare e Caricare Playlist

#### Salvare
1. `File → Salva Playlist`
2. Scegli nome e posizione
3. Il file .json conterrà l'ordine, note, colori, hotkey e tutte le impostazioni

#### Caricare
1. `File → Carica Playlist`
2. Seleziona il file .json salvato in precedenza

#### Backup Automatico
- L'app salva automaticamente ogni 5 minuti in `backups/`
- `File → Ripristina Backup` per recuperare l'ultima versione
- Vengono mantenuti gli ultimi 10 backup

### Flusso di Lavoro Consigliato

1. **Pre-Spettacolo**
   - Carica tutte le tracce necessarie
   - Riordina secondo la sequenza dello spettacolo
   - Aggiungi note descrittive per ogni scena
   - Assegna colori per categorie (musica/effetti)
   - Configura hotkey per tracce di emergenza/effetti speciali
   - Imposta loop per musiche di sottofondo
   - Salva la playlist
   - Usa Preview per verificare ogni traccia

2. **Durante lo Spettacolo**
   - Doppio click sulla traccia da preparare
   - Usa Preview per ascoltarla in anticipo
   - Quando pronto, click su "Play Main"
   - Usa hotkey (es: F1) per effetti sonori immediati
   - Le tracce con loop attivato si ripeteranno automaticamente
   - Preparare la traccia successiva in anticipo

3. **Best Practices**
   - Usa file WAV per migliori performance
   - Testa l'audio prima dello spettacolo
   - Verifica che il Bluetooth sia connesso
   - **Regola i volumi nell'app, non solo sul mixer/PC**
   - Tieni il volume del PC/mixer adeguato e usa gli slider nell'app per il fine-tuning

### Risoluzione Problemi

#### Non sento audio
- Verifica che i dispositivi siano selezionati correttamente
- Controlla il volume del PC
- Assicurati che il Bluetooth sia connesso

#### Audio che "salta"
- Usa file WAV invece di MP3
- Chiudi altre applicazioni che usano l'audio
- Verifica che il PC non sia in modalità risparmio energetico

#### Bluetooth non si connette
- Accoppia il dispositivo Bluetooth prima di avviare l'app
- Click su "Aggiorna" nel pannello dispositivi
- Riavvia l'applicazione

### Formati File Consigliati

- **WAV**: Migliore qualità, nessuna compressione, uso consigliato
- **MP3**: Buona qualità, file più piccoli
- **FLAC**: Alta qualità, file medi
- **OGG**: Qualità variabile

---

📧 Per supporto o segnalazioni: controlla il README.md

🎵 Buono spettacolo!
