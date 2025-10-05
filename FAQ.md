# ❓ Domande Frequenti (FAQ)

## 📥 Installazione & Setup

### Q: Devo installare Python per usare l'applicazione?
**A:** No, se usi l'eseguibile standalone (`.exe` su Windows, `.app` su macOS, binario su Linux). L'eseguibile include già tutto il necessario.

Se invece esegui da sorgente Python, sì, serve Python 3.8 o superiore.

### Q: Che file devo scaricare per il mio sistema operativo?
**A:** 
- **Windows:** `AudioManager.exe`
- **macOS:** `AudioManager.app` (tutto il bundle)
- **Linux:** `AudioManager` (binario eseguibile)

### Q: L'applicazione funziona su Windows 7?
**A:** No, è testata su Windows 10/11. Windows 7 potrebbe funzionare ma non è supportato ufficialmente.

### Q: Funziona su Apple Silicon (M1/M2/M3)?
**A:** Sì! L'applicazione è compatibile sia con Intel che con Apple Silicon (ARM64).

## 🔊 Audio & Dispositivi

### Q: Posso usare qualsiasi dispositivo audio?
**A:** Sì, l'applicazione rileva automaticamente tutti i dispositivi audio del sistema:
- Schede audio integrate
- Schede audio USB/Thunderbolt
- Dispositivi Bluetooth
- Interfacce audio professionali (ASIO su Windows)

### Q: Come configuro la doppia uscita (main + preview)?
**A:**
1. Avvia l'applicazione
2. Nella sezione "Dispositivi Audio", seleziona il dispositivo principale (es. uscita jack)
3. Seleziona il dispositivo preview (es. Bluetooth)
4. Salva la playlist per conservare le impostazioni

### Q: Posso usare lo stesso dispositivo per main e preview?
**A:** Sì, ma ascolterai il suono duplicato. È pensato per uscite separate (una per il pubblico, una per il tecnico).

### Q: Non sento audio, cosa posso fare?
**A:**
1. Verifica che i dispositivi audio siano selezionati
2. Controlla il volume del sistema operativo
3. Assicurati che i dispositivi non siano silenziati
4. Prova a cambiare dispositivo e riprova
5. Verifica che il file audio sia valido (riproducilo con altro player)

### Q: C'è troppa latenza/ritardo nell'audio
**A:** Su Windows, prova ad usare driver ASIO se la tua scheda audio li supporta. In alternativa:
- Chiudi altre applicazioni audio
- Usa file WAV invece di MP3 (minore CPU)
- Riduci le dimensioni file audio quando possibile

## 📁 File Audio

### Q: Che formati audio sono supportati?
**A:** 
- ✅ **WAV** (raccomandato per performance)
- ✅ **MP3**
- ✅ **OGG**
- ✅ **FLAC**

### Q: MP3 non funziona, cosa devo fare?
**A:** Su alcuni sistemi serve ffmpeg:
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`
- **Windows:** Generalmente funziona out-of-the-box

**Soluzione alternativa:** Converti in WAV con un convertitore audio.

### Q: Qual è il formato migliore per il teatro?
**A:** **WAV 44100Hz o 48000Hz, 16-bit o 24-bit**
- Migliore qualità
- Nessuna compressione
- Performance ottimali
- Caricamento più veloce

### Q: Posso usare file stereo?
**A:** Sì! L'applicazione supporta sia mono che stereo.

### Q: C'è un limite alla lunghezza delle tracce?
**A:** Non c'è un limite rigido, ma tracce molto lunghe (>30 minuti) consumano più RAM. Testato con successo fino a 30 minuti.

### Q: Quante tracce posso aggiungere alla playlist?
**A:** Testato con successo fino a 100 tracce. Più tracce = più RAM usata.

## 💾 Playlist & Salvataggio

### Q: Dove vengono salvate le playlist?
**A:** Dove vuoi tu! Quando salvi, scegli nome e posizione del file `.json`.

### Q: Cosa include il file playlist?
**A:** TUTTO:
- Lista tracce con percorsi
- Configurazione dispositivi audio
- Volumi main/preview per ogni traccia
- Note, colori, hotkey
- Trim (inizio/fine) per ogni traccia
- Loop mode

### Q: Se sposto i file audio, la playlist funziona ancora?
**A:** No, la playlist salva i percorsi assoluti. Se sposti i file audio, dovrai ricaricarli.

**Consiglio:** Tieni tutti i file audio in una cartella fissa (es. `C:\SpettacoloTeatro\Audio\`).

### Q: Dove vengono salvati i backup automatici?
**A:** Nella cartella `backups/` dentro la cartella del programma. Vengono conservati gli ultimi 10 backup.

### Q: Come ripristino un backup?
**A:** 
1. Vai in `backups/`
2. Trova il file `.json` con data/ora desiderata
3. Apri l'applicazione → "📂 Carica Playlist"
4. Seleziona il file di backup

## ⌨️ Hotkey & Controlli

### Q: Come assegno un hotkey a una traccia?
**A:** 
1. Seleziona la traccia
2. Click su "⌨️ Hotkey"
3. Premi il tasto desiderato (F1-F12, 1-9)

**Oppure:** Usa "Auto F1-F12" per assegnare automaticamente F1-F12 alle prime tracce in ordine.

### Q: Posso usare altri tasti oltre a F1-F12 e 1-9?
**A:** Attualmente solo F1-F12 e numeri 1-9. Altri tasti potrebbero essere aggiunti in futuro.

### Q: Le hotkey funzionano anche se la finestra non è in primo piano?
**A:** No, le hotkey funzionano solo quando l'applicazione ha il focus (è la finestra attiva).

### Q: Posso cambiare le hotkey predefinite (Spazio, S, P, ecc.)?
**A:** Le hotkey globali (Spazio=Play, S=Stop, ecc.) sono fisse. Solo F1-F12 e 1-9 sono personalizzabili per le tracce.

## ✂️ Trim & Editing

### Q: Il trim modifica il file originale?
**A:** **NO!** Il trim è completamente non-distruttivo. Il file originale rimane intatto.

### Q: Come funziona il trim?
**A:** L'applicazione legge il file completo ma riproduce solo la sezione specificata (es. da 0:05 a 2:30).

### Q: Posso trimmare un solo lato (solo inizio o solo fine)?
**A:** Sì:
- **Solo inizio:** Imposta start_time, lascia end_time a 0
- **Solo fine:** Lascia start_time a 0, imposta end_time

### Q: Il trim viene salvato nella playlist?
**A:** Sì! Quando salvi la playlist, tutte le impostazioni trim vengono salvate.

## 🎨 Organizzazione

### Q: A cosa servono i colori?
**A:** Per categorizzare visivamente le tracce. Esempi:
- 🔴 Rosso: Emergenze, allarmi
- 🟢 Verde: Musiche di sottofondo
- 🔵 Blu: Effetti atmosferici
- 🟡 Giallo: Transizioni
- ⚪ Bianco/Default: Tracce normali

### Q: Posso cercare tracce per colore?
**A:** Attualmente no, ma visivamente è facile identificarle nella tabella.

### Q: A cosa servono le note?
**A:** Per annotazioni di regia. Esempi:
- "Dopo battuta 35 protagonista"
- "Quando si spengono le luci"
- "Sfumare con fader manuale"
- "Loop fino a cambio scena"

## 🔁 Loop & Riproduzione

### Q: Cos'è il Loop Mode?
**A:** Quando attivato, la traccia si ripete all'infinito fino a quando non premi Stop.

### Q: Posso fare loop solo di una sezione (es. 30 secondi al centro)?
**A:** Sì! Combina Trim + Loop:
1. Taglia la traccia (es. da 1:00 a 1:30)
2. Attiva Loop
3. Risultato: loop infinito di quella sezione di 30 secondi

### Q: Finita una traccia, parte automaticamente la successiva?
**A:** **No**, di default si ferma. Questo è voluto per il controllo teatrale (aspetti il cue prima di far partire la prossima).

## 🎭 Uso Teatrale

### Q: Posso usarlo per musical?
**A:** Assolutamente sì! È pensato anche per quello:
- Hotkey per numeri musicali
- Trim per eliminare intro/outro
- Note con cue scenici
- Color coding per tipo brano

### Q: Funziona per spettacoli di prosa?
**A:** Sì! Ottimo per effetti sonori:
- Preview per verificare cue
- Loop per ambientazioni
- Hotkey per effetti rapidi
- Volume differenziato

### Q: Posso usarlo in diretta streaming?
**A:** Sì, basta usare un dispositivo audio virtuale (come VB-Cable su Windows) come output principale.

### Q: È abbastanza affidabile per uno spettacolo dal vivo?
**A:** Dipende:
- ✅ Testato con successo in ambiente teatrale
- ✅ Auto-backup ogni 5 minuti
- ✅ Nessun crash riportato in condizioni normali
- ⚠️ Sempre raccomandato avere un backup plan (player alternativo)

## 🔧 Problemi Comuni

### Q: L'interfaccia è troppo chiara/scura
**A:** L'interfaccia usa un tema scuro per non dare fastidio al buio in teatro. Al momento non è personalizzabile.

### Q: Il waveform non si vede
**A:** Il waveform richiede matplotlib. Se non installato, questa feature è disabilitata ma il resto funziona.

Per installare matplotlib:
```bash
pip install matplotlib
```

### Q: L'applicazione si blocca al caricamento
**A:**
- Controlla che i file audio siano accessibili (non su drive di rete lenti)
- Riduci il numero di tracce caricate contemporaneamente
- Verifica che i file audio non siano corrotti

### Q: "Dispositivo non disponibile"
**A:** Il dispositivo configurato non è più disponibile (disconnesso, disabilitato). Seleziona un altro dispositivo.

## 📱 Altro

### Q: Esiste una versione mobile (iOS/Android)?
**A:** No, solo desktop (Windows, macOS, Linux).

### Q: È open source?
**A:** Sì! Licenza MIT. Il codice è su GitHub.

### Q: Posso contribuire allo sviluppo?
**A:** Assolutamente! Pull request benvenute. Vedi README.md per dettagli.

### Q: Posso usarlo commercialmente?
**A:** Sì! Licenza MIT permette uso personale e commerciale, anche in produzioni a pagamento.

### Q: C'è un manuale utente dettagliato?
**A:** Vedi `README.md` per la guida completa d'uso.

### Q: Come segnalo un bug?
**A:** Apri una issue su GitHub con:
- Sistema operativo e versione
- Descrizione del problema
- Passi per riprodurre
- Screenshot se rilevante

---

**Non trovi la risposta? Apri una issue su GitHub!**
