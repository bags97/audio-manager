# 🎨 Icona Personalizzata (Opzionale)

L'applicazione funziona perfettamente **senza icona personalizzata** (usa l'icona di default Python/Windows).

Se desideri aggiungere un'icona personalizzata al tuo eseguibile:

## 📋 Requisiti Icona

### Windows (.ico)
- **Formato:** ICO (Windows Icon)
- **Dimensioni consigliate:** 256x256 pixel (può contenere multiple risoluzioni)
- **Nome file:** `icon.ico`
- **Posizione:** Root del progetto (stessa cartella di `main.py`)

### macOS (.icns)
- **Formato:** ICNS (Apple Icon)
- **Dimensioni:** Multiple (16x16 fino a 1024x1024)
- **Nome file:** `icon.icns`
- **Posizione:** Root del progetto

### Linux
Linux generalmente non richiede icona nel binario (usa .desktop file invece).

## 🎨 Come Creare un'Icona

### Opzione 1: Convertitore Online (Facile)

1. **Crea/trova un'immagine:**
   - Dimensione minima: 256x256 pixel
   - Formato: PNG, JPG, SVG
   - Tema: Simbolo audio/teatro (es. 🎭, 🎵, 🔊)

2. **Converti online:**
   - **Per Windows (.ico):**
     - https://convertio.co/it/png-ico/
     - https://www.icoconverter.com/
   - **Per macOS (.icns):**
     - https://cloudconvert.com/png-to-icns
     - https://iconverticons.com/online/

3. **Scarica e rinomina:**
   - Scarica il file convertito
   - Rinomina in `icon.ico` (Windows) o `icon.icns` (macOS)
   - Copia nella root del progetto

4. **Rebuilda:**
   ```bash
   # Windows
   build.bat
   
   # macOS
   ./build.sh
   ```

### Opzione 2: Tool da Linea di Comando

#### Windows - ImageMagick
```bash
# Installa ImageMagick
# https://imagemagick.org/script/download.php

# Converti immagine in .ico
magick convert input.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

#### macOS - iconutil (Built-in)
```bash
# Crea un iconset
mkdir AudioManager.iconset

# Crea varie dimensioni (esempio con sips)
sips -z 16 16     input.png --out AudioManager.iconset/icon_16x16.png
sips -z 32 32     input.png --out AudioManager.iconset/icon_16x16@2x.png
sips -z 32 32     input.png --out AudioManager.iconset/icon_32x32.png
sips -z 64 64     input.png --out AudioManager.iconset/icon_32x32@2x.png
sips -z 128 128   input.png --out AudioManager.iconset/icon_128x128.png
sips -z 256 256   input.png --out AudioManager.iconset/icon_128x128@2x.png
sips -z 256 256   input.png --out AudioManager.iconset/icon_256x256.png
sips -z 512 512   input.png --out AudioManager.iconset/icon_256x256@2x.png
sips -z 512 512   input.png --out AudioManager.iconset/icon_512x512.png
sips -z 1024 1024 input.png --out AudioManager.iconset/icon_512x512@2x.png

# Converti in .icns
iconutil -c icns AudioManager.iconset
mv AudioManager.icns icon.icns
```

### Opzione 3: Photoshop/GIMP (Avanzato)

**Photoshop:**
1. Crea immagine 256x256 o 1024x1024
2. Salva come PNG
3. Usa plugin ICO format per salvare direttamente come .ico

**GIMP:**
1. Crea immagine 256x256
2. File → Export As → `icon.ico`
3. Seleziona "Microsoft Windows Icon"
4. Seleziona risoluzioni multiple (16, 32, 48, 256)

## 🎨 Design Consigliati

Idee per l'icona di Audio Manager Teatrale:

### Tema 1: Teatro + Audio
- 🎭 Maschere teatrali + onde sonore
- Colori: Oro/Rosso velluto

### Tema 2: Professionale Audio
- 🎚️ Fader audio stilizzato
- 🔊 Speaker/altoparlante
- Colori: Blu scuro + Bianco

### Tema 3: Playlist
- 📋 Lista + nota musicale
- ▶️ Play button prominente
- Colori: Verde + Grigio scuro

### Tema 4: Minimalista
- Semplice forma d'onda
- Lettera "A" stilizzata
- Colori: Monocromatico

## 📁 Posizionamento File

```
audio-manager/
├── main.py
├── audio_manager.py
├── ...
├── icon.ico          ← Windows (se presente)
├── icon.icns         ← macOS (se presente)
└── build.bat
```

## ✅ Verifica

Dopo aver aggiunto l'icona e rebuildata:

**Windows:**
```cmd
# Controlla che l'exe abbia l'icona
# Guarda l'icona in Esplora File
dir dist\AudioManager.exe
```

**macOS:**
```bash
# Controlla il bundle
ls -la dist/AudioManager.app/Contents/Resources/
```

## 🎨 Risorse Gratuite

### Icone Royalty-Free:
- **Flaticon:** https://www.flaticon.com/ (ricerca: "theater", "audio", "playlist")
- **Icons8:** https://icons8.com/ (filtro: gratis)
- **FontAwesome:** https://fontawesome.com/icons (download SVG)

### Generator AI:
- **Stable Diffusion:** Genera icona custom
- **DALL-E 3:** Crea design unico
- Prompt: "minimalist app icon for theater audio management, professional, clean design"

## ⚠️ Note Importanti

1. **Senza icona = Funziona perfettamente**
   - L'app usa l'icona di default
   - Nessun impatto sulla funzionalità

2. **Licenze:**
   - Assicurati di avere diritti sull'immagine usata
   - Icone royalty-free OK
   - Icone create da te OK

3. **Dimensioni:**
   - .ico dovrebbe includere 16x16, 32x32, 48x48, 256x256
   - .icns dovrebbe includere tutte le dimensioni da 16 a 1024

4. **Trasparenza:**
   - Usa PNG con sfondo trasparente come base
   - L'icona si adatta meglio a temi chiari/scuri

## 🔄 Update Icona

Per cambiare icona dopo la build:

**Windows:**
```bash
# Metodo 1: Rebuilda tutto
build.bat

# Metodo 2: Tool di terze parti
# Usa Resource Hacker per modificare .exe esistente
# https://www.angusj.com/resourcehacker/
```

**macOS:**
```bash
# Rebuilda
./build.sh
```

---

**Ricorda:** L'icona è completamente **opzionale**. L'applicazione funziona perfettamente senza! 🎭✨
