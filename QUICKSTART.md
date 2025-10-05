# 🚀 Quick Start - Audio Manager Teatrale

## 1️⃣ Per Utenti (Voglio solo usare il programma)

### Windows
```cmd
1. Scarica AudioManager.exe
2. Doppio click
3. Fatto! 🎭
```

### macOS
```bash
1. Scarica AudioManager.app
2. Doppio click
3. (Se richiesto, vai in Preferenze → Sicurezza → Apri comunque)
4. Fatto! 🎭
```

### Linux
```bash
1. Scarica AudioManager
2. chmod +x AudioManager
3. ./AudioManager
4. Fatto! 🎭
```

## 2️⃣ Per Sviluppatori (Voglio modificare/testare il codice)

### Setup Iniziale

**Windows:**
```cmd
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Esegui da Sorgente
```bash
python main.py
```

### Crea Eseguibile

**Windows:**
```cmd
build.bat
```

**macOS/Linux:**
```bash
./build.sh
```

Output in `dist/`

## 3️⃣ Uso Base

1. **Configura Audio**
   - Dispositivo Main (pubblico)
   - Dispositivo Preview (tecnico)

2. **Carica Tracce**
   - ➕ Aggiungi → Seleziona file audio

3. **Organizza**
   - ⬆️⬇️ Riordina
   - ✏️ Modifica (note, colori)
   - ⌨️ Hotkey (F1-F12)

4. **Riproduci**
   - ▶️ Play (output main)
   - 👂 Preview (output preview)
   - ⏸️ Pausa / ⏹️ Stop

5. **Salva**
   - 💾 Salva Playlist → file .json
   - (Auto-backup ogni 5 min)

## 📚 Documentazione Completa

- **README.md** → Guida utente completa
- **BUILD.md** → Guida build & distribuzione
- **FAQ.md** → Domande frequenti
- **PORTABLE.md** → Dettagli portabilità

## 🆘 Problemi?

```bash
# Test compatibilità
python test_compatibility.py
```

Vedi **FAQ.md** per problemi comuni.

## 🎯 Hotkey Rapide

| Tasto | Azione |
|-------|--------|
| Spazio | Play/Pausa |
| S | Stop |
| P | Preview |
| ← → | Prev/Next |
| F1-F12 | Traccia assegnata |
| 1-9 | Traccia 1-9 |

---

**Più info?** Leggi README.md

**Pronto per il teatro!** 🎭✨
