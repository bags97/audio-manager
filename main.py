"""
Main Application - Audio Manager per Spettacoli Teatrali
Interfaccia grafica principale con tutte le funzionalità avanzate
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, simpledialog
import threading
import time
from pathlib import Path
from audio_manager import DualAudioManager
from playlist_manager import PlaylistManager
from auto_backup import AutoBackup
from typing import Optional
import json

# Import matplotlib per waveform (opzionale)
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib non disponibile - visualizzazione waveform disabilitata")


class AudioManagerGUI:
    """Interfaccia grafica principale"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Manager - Gestione Tracce Teatrali")
        self.root.geometry("1200x800")
        
        # Tema scuro per uso teatrale al buio
        self._setup_dark_theme()
        
        # Percorsi file di configurazione
        self.config_dir = Path.home() / ".audio_manager"
        self.config_dir.mkdir(exist_ok=True)
        self.last_session_file = self.config_dir / "last_session.json"
        
        # Managers
        self.audio_manager = DualAudioManager()
        self.playlist_manager = PlaylistManager()
        self.auto_backup = AutoBackup(interval_seconds=300)  # Backup ogni 5 minuti
        
        # Stato
        self.is_playing = False
        self.is_preview = False
        self.update_thread = None
        self.running = True
        self.hotkey_map = {}  # Mappa hotkey -> track index
        
        # Waveform
        self.waveform_figure = None
        self.waveform_canvas = None
        self.waveform_frame = None
        
        # Setup UI
        self._setup_ui()
        self._setup_keyboard_shortcuts()
        self._load_audio_devices()
        
        # Carica ultima sessione se disponibile (DOPO aver caricato i dispositivi)
        self._load_last_session()
        
        # Avvia backup automatico
        self._start_auto_backup()
        
        # Avvia thread di aggiornamento
        self._start_update_thread()
        
        # Gestione chiusura
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_dark_theme(self):
        """Configura il tema scuro per uso teatrale al buio"""
        # Colori del tema scuro
        self.colors = {
            'bg': '#1e1e1e',           # Sfondo principale scuro
            'bg_light': '#2d2d2d',     # Sfondo secondario
            'bg_widget': '#252526',    # Sfondo widget
            'fg': '#d4d4d4',           # Testo principale
            'fg_dim': '#808080',       # Testo secondario
            'select_bg': '#094771',    # Selezione
            'select_fg': '#ffffff',    # Testo selezionato
            'button_bg': '#0e639c',    # Pulsanti
            'button_fg': '#ffffff',    # Testo pulsanti
            'border': '#3e3e3e',       # Bordi
            'accent': '#007acc',       # Colore accento
            'success': '#4ec9b0',      # Verde successo
            'warning': '#dcdcaa',      # Giallo avviso
            'error': '#f48771'         # Rosso errore
        }
        
        # Configura lo sfondo della finestra principale
        self.root.configure(bg=self.colors['bg'])
        
        # Configura lo stile ttk per il tema scuro
        style = ttk.Style()
        style.theme_use('clam')  # Base theme
        
        # Frame
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabelframe', background=self.colors['bg'], 
                       foreground=self.colors['fg'], bordercolor=self.colors['border'])
        style.configure('TLabelframe.Label', background=self.colors['bg'], 
                       foreground=self.colors['fg'])
        
        # Label
        style.configure('TLabel', background=self.colors['bg'], 
                       foreground=self.colors['fg'])
        
        # Button
        style.configure('TButton', background=self.colors['button_bg'], 
                       foreground=self.colors['button_fg'], bordercolor=self.colors['border'],
                       focuscolor=self.colors['accent'])
        style.map('TButton', background=[('active', self.colors['accent'])])
        
        # Combobox
        style.configure('TCombobox', fieldbackground=self.colors['bg_widget'], 
                       background=self.colors['bg_widget'], foreground=self.colors['fg'],
                       arrowcolor=self.colors['fg'], bordercolor=self.colors['border'])
        style.map('TCombobox', fieldbackground=[('readonly', self.colors['bg_widget'])],
                 selectbackground=[('readonly', self.colors['select_bg'])],
                 selectforeground=[('readonly', self.colors['select_fg'])])
        
        # Scale (sliders)
        style.configure('TScale', background=self.colors['bg'], 
                       troughcolor=self.colors['bg_widget'], bordercolor=self.colors['border'])
        
        # Treeview (tabella tracce)
        style.configure('Treeview', background=self.colors['bg_widget'], 
                       foreground=self.colors['fg'], fieldbackground=self.colors['bg_widget'],
                       bordercolor=self.colors['border'])
        style.configure('Treeview.Heading', background=self.colors['bg_light'], 
                       foreground=self.colors['fg'], bordercolor=self.colors['border'])
        style.map('Treeview', background=[('selected', self.colors['select_bg'])],
                 foreground=[('selected', self.colors['select_fg'])])
        
        # PanedWindow
        style.configure('TPanedwindow', background=self.colors['bg'])
        style.configure('Sash', sashthickness=5, background=self.colors['border'])
        
        # Separator
        style.configure('TSeparator', background=self.colors['border'])
        
        # Checkbutton
        style.configure('TCheckbutton', background=self.colors['bg'], 
                       foreground=self.colors['fg'])
        style.map('TCheckbutton', background=[('active', self.colors['bg'])])
        
        # Progressbar
        style.configure('TProgressbar', background=self.colors['accent'], 
                       troughcolor=self.colors['bg_widget'], bordercolor=self.colors['border'],
                       lightcolor=self.colors['accent'], darkcolor=self.colors['accent'])
        
    def _setup_ui(self):
        """Configura l'interfaccia utente"""
        
        # === MENU BAR ===
        menubar = tk.Menu(self.root, bg=self.colors['bg_light'], fg=self.colors['fg'],
                         activebackground=self.colors['select_bg'], 
                         activeforeground=self.colors['select_fg'])
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg_widget'], 
                           fg=self.colors['fg'], activebackground=self.colors['select_bg'],
                           activeforeground=self.colors['select_fg'])
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Aggiungi Tracce...", command=self._add_tracks)
        file_menu.add_command(label="Salva Playlist...", command=self._save_playlist)
        file_menu.add_command(label="Carica Playlist...", command=self._load_playlist)
        file_menu.add_separator()
        file_menu.add_command(label="Ripristina Backup...", command=self._restore_backup)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self._on_closing)
        
        # === FRAME DISPOSITIVI ===
        devices_frame = ttk.LabelFrame(self.root, text="Dispositivi Audio", padding=10)
        devices_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Main Output
        ttk.Label(devices_frame, text="Uscita Principale (Jack):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.main_device_var = tk.StringVar()
        self.main_device_combo = ttk.Combobox(devices_frame, textvariable=self.main_device_var, 
                                               state='readonly', width=40)
        self.main_device_combo.grid(row=0, column=1, padx=5, pady=2)
        self.main_device_combo.bind('<<ComboboxSelected>>', self._on_main_device_changed)
        
        # Volume Main
        ttk.Label(devices_frame, text="Volume:").grid(row=0, column=2, padx=(10, 5))
        self.main_volume_var = tk.DoubleVar(value=100)
        self.main_volume_scale = ttk.Scale(devices_frame, from_=0, to=100, 
                                            variable=self.main_volume_var,
                                            orient=tk.HORIZONTAL, length=150,
                                            command=self._on_main_volume_changed)
        self.main_volume_scale.grid(row=0, column=3, padx=5)
        self.main_volume_label = ttk.Label(devices_frame, text="100%", width=5)
        self.main_volume_label.grid(row=0, column=4, padx=5)
        
        # Preview Output
        ttk.Label(devices_frame, text="Uscita Preview (Bluetooth):").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.preview_device_var = tk.StringVar()
        self.preview_device_combo = ttk.Combobox(devices_frame, textvariable=self.preview_device_var,
                                                  state='readonly', width=40)
        self.preview_device_combo.grid(row=1, column=1, padx=5, pady=2)
        self.preview_device_combo.bind('<<ComboboxSelected>>', self._on_preview_device_changed)
        
        # Volume Preview
        ttk.Label(devices_frame, text="Volume:").grid(row=1, column=2, padx=(10, 5))
        self.preview_volume_var = tk.DoubleVar(value=100)
        self.preview_volume_scale = ttk.Scale(devices_frame, from_=0, to=100,
                                               variable=self.preview_volume_var,
                                               orient=tk.HORIZONTAL, length=150,
                                               command=self._on_preview_volume_changed)
        self.preview_volume_scale.grid(row=1, column=3, padx=5)
        self.preview_volume_label = ttk.Label(devices_frame, text="100%", width=5)
        self.preview_volume_label.grid(row=1, column=4, padx=5)
        
        ttk.Button(devices_frame, text="Aggiorna", command=self._load_audio_devices).grid(
            row=0, column=5, rowspan=2, padx=5)
        
        # === CONTENITORE PRINCIPALE ===
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # === FRAME PLAYLIST (SINISTRA) ===
        playlist_frame = ttk.LabelFrame(main_container, text="Playlist", padding=10)
        main_container.add(playlist_frame, weight=2)
        
        # Toolbar playlist
        toolbar = ttk.Frame(playlist_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(toolbar, text="➕ Aggiungi", command=self._add_tracks).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="➖ Rimuovi", command=self._remove_track).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="⬆ Su", command=self._move_track_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="⬇ Giù", command=self._move_track_down).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔄 Inverti", command=self._reverse_tracks).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑 Pulisci", command=self._clear_playlist).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="📝 Note", command=self._edit_track_notes).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🎨 Colore", command=self._edit_track_color).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔊 Volume", command=self._edit_track_volume).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="✂️ Taglia", command=self._edit_track_trim).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="⌨️ Hotkey", command=self._edit_track_hotkey).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🎹 Auto F1-F12", command=self._auto_assign_hotkeys).pack(side=tk.LEFT, padx=2)
        
        # Lista tracce
        list_frame = ttk.Frame(playlist_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview per le tracce
        self.track_tree = ttk.Treeview(list_frame, columns=('index', 'title', 'duration', 'trim', 'loop', 'hotkey', 'volume', 'notes'),
                                        show='headings', yscrollcommand=scrollbar.set)
        self.track_tree.heading('index', text='#')
        self.track_tree.heading('title', text='Titolo')
        self.track_tree.heading('duration', text='Durata')
        self.track_tree.heading('trim', text='Trim')
        self.track_tree.heading('loop', text='Loop')
        self.track_tree.heading('hotkey', text='Key')
        self.track_tree.heading('volume', text='Vol%')
        self.track_tree.heading('notes', text='Note')
        
        self.track_tree.column('index', width=40, anchor=tk.CENTER)
        self.track_tree.column('title', width=230)
        self.track_tree.column('duration', width=70, anchor=tk.CENTER)
        self.track_tree.column('trim', width=90, anchor=tk.CENTER)
        self.track_tree.column('loop', width=50, anchor=tk.CENTER)
        self.track_tree.column('hotkey', width=50, anchor=tk.CENTER)
        self.track_tree.column('volume', width=50, anchor=tk.CENTER)
        self.track_tree.column('notes', width=120)
        
        self.track_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.track_tree.yview)
        
        # Doppio click per caricare traccia
        self.track_tree.bind('<Double-1>', self._on_track_double_click)
        
        # === FRAME WAVEFORM (DESTRA) ===
        if MATPLOTLIB_AVAILABLE:
            self.waveform_frame = ttk.LabelFrame(main_container, text="Forma d'Onda", padding=10)
            main_container.add(self.waveform_frame, weight=1)
            self._setup_waveform()
        
        # === FRAME CONTROLLI ===
        controls_frame = ttk.LabelFrame(self.root, text="Controlli Riproduzione", padding=10)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Info traccia corrente
        info_frame = ttk.Frame(controls_frame)
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.current_track_label = ttk.Label(info_frame, text="Nessuna traccia caricata",
                                              font=('Arial', 10, 'bold'))
        self.current_track_label.pack(side=tk.LEFT)
        
        # Loop checkbox
        self.loop_var = tk.BooleanVar()
        self.loop_check = ttk.Checkbutton(info_frame, text="🔁 Loop", variable=self.loop_var,
                                          command=self._on_loop_changed)
        self.loop_check.pack(side=tk.RIGHT, padx=10)
        
        # Progress bar
        progress_frame = ttk.Frame(controls_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.time_label = ttk.Label(progress_frame, text="00:00")
        self.time_label.pack(side=tk.LEFT, padx=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                             maximum=100, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.duration_label = ttk.Label(progress_frame, text="00:00")
        self.duration_label.pack(side=tk.LEFT, padx=5)
        
        # Pulsanti controllo
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack()
        
        self.prev_btn = ttk.Button(buttons_frame, text="⏮ Precedente", command=self._previous_track, width=15)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.play_btn = ttk.Button(buttons_frame, text="▶ Play Main", command=self._play_main, width=15)
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        self.preview_btn = ttk.Button(buttons_frame, text="🎧 Preview", command=self._play_preview, width=15)
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = ttk.Button(buttons_frame, text="⏸ Pausa", command=self._pause, width=15)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(buttons_frame, text="⏹ Stop", command=self._stop, width=15)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = ttk.Button(buttons_frame, text="Successivo ⏭", command=self._next_track, width=15)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_label = ttk.Label(self.root, text="Pronto | Backup automatico attivo ogni 5 minuti", 
                                       relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
    def _setup_waveform(self):
        """Setup visualizzazione forma d'onda"""
        if not MATPLOTLIB_AVAILABLE:
            return
            
        # Configura stile scuro per matplotlib
        self.waveform_figure = Figure(figsize=(5, 4), dpi=80, facecolor=self.colors['bg'])
        self.waveform_ax = self.waveform_figure.add_subplot(111)
        self.waveform_ax.set_facecolor(self.colors['bg_widget'])
        self.waveform_ax.set_title("Forma d'Onda", color=self.colors['fg'])
        self.waveform_ax.set_xlabel("Tempo (s)", color=self.colors['fg'])
        self.waveform_ax.set_ylabel("Ampiezza", color=self.colors['fg'])
        self.waveform_ax.tick_params(colors=self.colors['fg'], which='both')
        self.waveform_ax.spines['bottom'].set_color(self.colors['border'])
        self.waveform_ax.spines['top'].set_color(self.colors['border'])
        self.waveform_ax.spines['left'].set_color(self.colors['border'])
        self.waveform_ax.spines['right'].set_color(self.colors['border'])
        
        self.waveform_canvas = FigureCanvasTkAgg(self.waveform_figure, self.waveform_frame)
        self.waveform_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def _update_waveform(self):
        """Aggiorna la visualizzazione della forma d'onda"""
        if not MATPLOTLIB_AVAILABLE or not self.waveform_ax:
            return
            
        self.waveform_ax.clear()
        
        # Riapplica stile scuro dopo clear
        self.waveform_ax.set_facecolor(self.colors['bg_widget'])
        self.waveform_ax.tick_params(colors=self.colors['fg'], which='both')
        self.waveform_ax.spines['bottom'].set_color(self.colors['border'])
        self.waveform_ax.spines['top'].set_color(self.colors['border'])
        self.waveform_ax.spines['left'].set_color(self.colors['border'])
        self.waveform_ax.spines['right'].set_color(self.colors['border'])
        
        # Ottieni i dati audio
        if self.audio_manager.main_output.audio_data is not None:
            audio_data = self.audio_manager.main_output.audio_data
            sample_rate = self.audio_manager.main_output.sample_rate
            
            # Downsampling per visualizzazione (max 10000 punti)
            if len(audio_data) > 10000:
                step = len(audio_data) // 10000
                audio_data = audio_data[::step]
            
            # Converti in mono se stereo
            if len(audio_data.shape) > 1:
                audio_data = audio_data.mean(axis=1)
            
            # Crea asse temporale
            time_axis = np.arange(len(audio_data)) / sample_rate * (len(self.audio_manager.main_output.audio_data) / len(audio_data))
            
            # Plotta con colore accento
            self.waveform_ax.plot(time_axis, audio_data, linewidth=0.5, color=self.colors['accent'])
            self.waveform_ax.set_title("Forma d'Onda", color=self.colors['fg'])
            self.waveform_ax.set_xlabel("Tempo (s)", color=self.colors['fg'])
            self.waveform_ax.set_ylabel("Ampiezza", color=self.colors['fg'])
            self.waveform_ax.grid(True, alpha=0.2, color=self.colors['fg_dim'])
            
        else:
            self.waveform_ax.text(0.5, 0.5, 'Nessun audio caricato', 
                                  ha='center', va='center', transform=self.waveform_ax.transAxes,
                                  color=self.colors['fg_dim'])
        
        self.waveform_canvas.draw()
        
    def _setup_keyboard_shortcuts(self):
        """Configura le scorciatoie da tastiera"""
        self.root.bind('<space>', lambda e: self._toggle_play())
        self.root.bind('s', lambda e: self._stop())
        self.root.bind('n', lambda e: self._next_track())
        self.root.bind('p', lambda e: self._previous_track())
        self.root.bind('<Control-o>', lambda e: self._add_tracks())
        # Controlli volume
        self.root.bind('<Up>', lambda e: self._volume_up_main())
        self.root.bind('<Down>', lambda e: self._volume_down_main())
        self.root.bind('<Control-Up>', lambda e: self._volume_up_preview())
        self.root.bind('<Control-Down>', lambda e: self._volume_down_preview())
        # Hotkeys numerici (1-9)
        for i in range(1, 10):
            self.root.bind(str(i), self._make_hotkey_callback(str(i)))
        # Hotkeys F1-F12 (usando factory per evitare problemi con F11)
        for i in range(1, 13):
            self.root.bind(f'<F{i}>', self._make_hotkey_callback(f'F{i}'))

    def _make_hotkey_callback(self, key):
        """Factory per callback hotkey, risolve problemi di late binding"""
        return lambda e: self._hotkey_pressed(key)
            
    def _hotkey_pressed(self, key: str):
        """Gestisce la pressione di un hotkey - SEMPRE su canale principale"""
        track = self.playlist_manager.get_track_by_hotkey(key)
        if track:
            # Ferma eventuale riproduzione corrente
            self._stop()
            
            # Carica la traccia
            self.playlist_manager.set_current_track(track.index)
            if self._load_current_track():
                # SEMPRE play main per hotkeys
                self._play_main()
                self._set_status(f"Hotkey {key}: {track.title} → MAIN")
        
    def _load_audio_devices(self):
        """Carica i dispositivi audio disponibili"""
        devices = DualAudioManager.get_audio_devices()
        device_names = [f"{d['id']}: {d['name']}" for d in devices]
        
        self.audio_devices = devices
        self.main_device_combo['values'] = device_names
        self.preview_device_combo['values'] = device_names
        
        # Imposta dispositivi di default solo se non già impostati
        if device_names:
            # Controlla se è già stato impostato un dispositivo
            if self.main_device_combo.current() < 0:
                self.main_device_combo.current(0)
                self._on_main_device_changed()
            
            if self.preview_device_combo.current() < 0:
                self.preview_device_combo.current(min(1, len(device_names) - 1))
                self._on_preview_device_changed()
            
    def _on_main_device_changed(self, event=None):
        """Callback cambio dispositivo main"""
        idx = self.main_device_combo.current()
        if idx >= 0:
            device_id = self.audio_devices[idx]['id']
            self.audio_manager.set_main_device(device_id)
            self._set_status(f"Uscita principale: {self.audio_devices[idx]['name']}")
            
    def _on_preview_device_changed(self, event=None):
        """Callback cambio dispositivo preview"""
        idx = self.preview_device_combo.current()
        if idx >= 0:
            device_id = self.audio_devices[idx]['id']
            self.audio_manager.set_preview_device(device_id)
            self._set_status(f"Uscita preview: {self.audio_devices[idx]['name']}")
    
    def _on_main_volume_changed(self, value=None):
        """Callback cambio volume main"""
        volume = self.main_volume_var.get() / 100.0
        self.audio_manager.set_main_volume(volume)
        self.main_volume_label.config(text=f"{int(self.main_volume_var.get())}%")
    
    def _on_preview_volume_changed(self, value=None):
        """Callback cambio volume preview"""
        volume = self.preview_volume_var.get() / 100.0
        self.audio_manager.set_preview_volume(volume)
        self.preview_volume_label.config(text=f"{int(self.preview_volume_var.get())}%")
    
    def _volume_up_main(self):
        """Aumenta volume main di 5%"""
        current = self.main_volume_var.get()
        new_volume = min(100, current + 5)
        self.main_volume_var.set(new_volume)
        self._on_main_volume_changed()
    
    def _volume_down_main(self):
        """Diminuisci volume main di 5%"""
        current = self.main_volume_var.get()
        new_volume = max(0, current - 5)
        self.main_volume_var.set(new_volume)
        self._on_main_volume_changed()
    
    def _volume_up_preview(self):
        """Aumenta volume preview di 5%"""
        current = self.preview_volume_var.get()
        new_volume = min(100, current + 5)
        self.preview_volume_var.set(new_volume)
        self._on_preview_volume_changed()
    
    def _volume_down_preview(self):
        """Diminuisci volume preview di 5%"""
        current = self.preview_volume_var.get()
        new_volume = max(0, current - 5)
        self.preview_volume_var.set(new_volume)
        self._on_preview_volume_changed()
    
    def _on_loop_changed(self):
        """Callback cambio modalità loop"""
        loop_enabled = self.loop_var.get()
        self.audio_manager.set_loop(loop_enabled)
        
        # Aggiorna anche la traccia corrente
        track = self.playlist_manager.get_current_track()
        if track:
            self.playlist_manager.update_track_loop(track.index, loop_enabled)
            self._update_track_list()
        
        status = "attivato" if loop_enabled else "disattivato"
        self._set_status(f"Loop {status}")
            
    def _add_tracks(self):
        """Aggiungi tracce audio"""
        filepaths = filedialog.askopenfilenames(
            title="Seleziona file audio",
            filetypes=[
                ("File Audio", "*.mp3 *.wav *.ogg *.flac"),
                ("WAV", "*.wav"),
                ("MP3", "*.mp3"),
                ("OGG", "*.ogg"),
                ("FLAC", "*.flac"),
                ("Tutti i file", "*.*")
            ]
        )
        
        if filepaths:
            tracks = self.playlist_manager.add_tracks(list(filepaths))
            self._update_track_list()
            self._set_status(f"Aggiunte {len(tracks)} tracce")
            
    def _remove_track(self):
        """Rimuovi la traccia selezionata"""
        selection = self.track_tree.selection()
        if not selection:
            return
            
        item = self.track_tree.item(selection[0])
        index = int(item['values'][0]) - 1
        
        if self.playlist_manager.remove_track(index):
            self._update_track_list()
            self._rebuild_hotkey_map()
            self._set_status("Traccia rimossa")
            
    def _move_track_up(self):
        """Sposta la traccia selezionata verso l'alto"""
        selection = self.track_tree.selection()
        if not selection:
            return
            
        item = self.track_tree.item(selection[0])
        index = int(item['values'][0]) - 1
        
        if index > 0 and self.playlist_manager.move_track(index, index - 1):
            self._update_track_list()
            # Riseleziona l'item
            new_iid = self.track_tree.get_children()[index - 1]
            self.track_tree.selection_set(new_iid)
            
    def _move_track_down(self):
        """Sposta la traccia selezionata verso il basso"""
        selection = self.track_tree.selection()
        if not selection:
            return
            
        item = self.track_tree.item(selection[0])
        index = int(item['values'][0]) - 1
        
        if index < self.playlist_manager.get_track_count() - 1:
            if self.playlist_manager.move_track(index, index + 1):
                self._update_track_list()
                # Riseleziona l'item
                new_iid = self.track_tree.get_children()[index + 1]
                self.track_tree.selection_set(new_iid)
                
    def _clear_playlist(self):
        """Pulisci la playlist"""
        if messagebox.askyesno("Conferma", "Vuoi davvero svuotare la playlist?"):
            self.playlist_manager.clear()
            self._update_track_list()
            self._stop()
            self._set_status("Playlist svuotata")
    
    def _reverse_tracks(self):
        """Inverti l'ordine della playlist"""
        if self.playlist_manager.get_track_count() == 0:
            messagebox.showinfo("Info", "La playlist è vuota.")
            return
            
        if messagebox.askyesno("Conferma", "Vuoi invertire completamente l'ordine delle tracce?"):
            self.playlist_manager.reverse_tracks()
            self._update_track_list()
            self._rebuild_hotkey_map()
            self._set_status("Playlist invertita")
            
    def _edit_track_notes(self):
        """Modifica le note della traccia selezionata"""
        selection = self.track_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Seleziona una traccia")
            return
            
        item = self.track_tree.item(selection[0])
        index = int(item['values'][0]) - 1
        track = self.playlist_manager.get_track(index)
        
        if track:
            # Dialog per inserire note
            notes = simpledialog.askstring("Note Traccia", 
                                          f"Note per '{track.title}':",
                                          initialvalue=track.notes or "")
            if notes is not None:
                self.playlist_manager.update_track_notes(index, notes)
                self._update_track_list()
                self._set_status(f"Note aggiornate per: {track.title}")
                
    def _edit_track_color(self):
        """Modifica il colore della traccia selezionata"""
        selection = self.track_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Seleziona una traccia")
            return
            
        item = self.track_tree.item(selection[0])
        index = int(item['values'][0]) - 1
        track = self.playlist_manager.get_track(index)
        
        if track:
            # Color picker
            color = colorchooser.askcolor(title=f"Colore per '{track.title}'",
                                         initialcolor=track.color or "#FFFFFF")
            if color[1]:
                self.playlist_manager.update_track_color(index, color[1])
                self._update_track_list()
                self._set_status(f"Colore aggiornato per: {track.title}")
    
    def _edit_track_volume(self):
        """Modifica il volume della traccia selezionata"""
        selection = self.track_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Seleziona una traccia")
            return
            
        item = self.track_tree.item(selection[0])
        index = int(item['values'][0]) - 1
        track = self.playlist_manager.get_track(index)
        
        if track:
            # Dialog per volume (0-100)
            volume = simpledialog.askinteger("Volume Traccia",
                                            f"Volume per '{track.title}' (0-100%):",
                                            initialvalue=track.volume,
                                            minvalue=0,
                                            maxvalue=100)
            if volume is not None:
                self.playlist_manager.update_track_volume(index, volume)
                self._update_track_list()
                self._set_status(f"Volume impostato a {volume}% per: {track.title}")
    
    def _edit_track_trim(self):
        """Modifica i punti di inizio e fine della traccia selezionata"""
        selection = self.track_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Seleziona una traccia")
            return
            
        item = self.track_tree.item(selection[0])
        index = int(item['values'][0]) - 1
        track = self.playlist_manager.get_track(index)
        
        if track:
            # Crea finestra di dialogo personalizzata
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Taglia Traccia: {track.title}")
            dialog.geometry("400x200")
            dialog.configure(bg=self.colors['bg'])
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Frame principale
            main_frame = ttk.Frame(dialog, padding=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Durata totale
            duration_text = self._format_time(track.duration) if track.duration > 0 else "non caricata"
            ttk.Label(main_frame, text=f"Durata totale: {duration_text}").pack(pady=(0, 10))
            
            # Punto di inizio
            start_frame = ttk.Frame(main_frame)
            start_frame.pack(fill=tk.X, pady=5)
            ttk.Label(start_frame, text="Inizio (secondi):").pack(side=tk.LEFT, padx=(0, 10))
            start_var = tk.DoubleVar(value=track.start_time)
            start_spin = ttk.Spinbox(start_frame, from_=0, to=track.duration if track.duration > 0 else 9999,
                                    textvariable=start_var, width=10, increment=0.1)
            start_spin.pack(side=tk.LEFT)
            ttk.Label(start_frame, text=f"({self._format_time(track.start_time)})").pack(side=tk.LEFT, padx=(5, 0))
            
            # Punto di fine
            end_frame = ttk.Frame(main_frame)
            end_frame.pack(fill=tk.X, pady=5)
            ttk.Label(end_frame, text="Fine (secondi):").pack(side=tk.LEFT, padx=(0, 10))
            end_var = tk.DoubleVar(value=track.end_time if track.end_time > 0 else track.duration)
            end_spin = ttk.Spinbox(end_frame, from_=0, to=track.duration if track.duration > 0 else 9999,
                                  textvariable=end_var, width=10, increment=0.1)
            end_spin.pack(side=tk.LEFT)
            end_label = ttk.Label(end_frame, text=f"({self._format_time(track.end_time if track.end_time > 0 else track.duration)})")
            end_label.pack(side=tk.LEFT, padx=(5, 0))
            
            ttk.Label(main_frame, text="(0 per fine = fino alla fine naturale)", 
                     foreground=self.colors['fg_dim']).pack(pady=(5, 10))
            
            # Pulsanti
            def save_trim():
                start = start_var.get()
                end = end_var.get()
                
                # Validazione
                if start < 0:
                    messagebox.showerror("Errore", "Il punto di inizio deve essere >= 0")
                    return
                if end > 0 and end <= start:
                    messagebox.showerror("Errore", "Il punto di fine deve essere maggiore dell'inizio")
                    return
                
                self.playlist_manager.update_track_trim(index, start, end)
                self._update_track_list()
                self._set_status(f"Trim impostato per: {track.title}")
                dialog.destroy()
            
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(pady=(10, 0))
            ttk.Button(button_frame, text="Salva", command=save_trim).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Annulla", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
                
    def _edit_track_hotkey(self):
        """Modifica l'hotkey della traccia selezionata"""
        selection = self.track_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Seleziona una traccia")
            return
            
        item = self.track_tree.item(selection[0])
        index = int(item['values'][0]) - 1
        track = self.playlist_manager.get_track(index)
        
        if track:
            # Dialog per inserire hotkey
            hotkey = simpledialog.askstring("Hotkey Traccia",
                                           f"Hotkey per '{track.title}' (1-9 o F1-F12):",
                                           initialvalue=track.hotkey or "")
            if hotkey is not None:
                # Valida hotkey
                valid_keys = [str(i) for i in range(1, 10)] + [f'F{i}' for i in range(1, 13)]
                if hotkey == "" or hotkey in valid_keys:
                    self.playlist_manager.update_track_hotkey(index, hotkey)
                    self._rebuild_hotkey_map()
                    self._update_track_list()
                    self._set_status(f"Hotkey '{hotkey}' assegnata a: {track.title}")
                else:
                    messagebox.showerror("Errore", "Hotkey non valida. Usa 1-9 o F1-F12")
    
    def _auto_assign_hotkeys(self):
        """Assegna automaticamente F1-F12 alle prime 12 tracce"""
        tracks = self.playlist_manager.tracks
        if not tracks:
            messagebox.showinfo("Info", "Nessuna traccia nella playlist")
            return
        
        # Chiedi conferma
        num_tracks = min(len(tracks), 12)
        if messagebox.askyesno("Auto-assegnazione Hotkeys", 
                               f"Assegnare F1-F{num_tracks} alle prime {num_tracks} tracce?\n"
                               f"Le hotkeys esistenti verranno sovrascritte."):
            for i in range(num_tracks):
                hotkey = f"F{i+1}"
                self.playlist_manager.update_track_hotkey(i, hotkey)
            
            self._rebuild_hotkey_map()
            self._update_track_list()
            self._set_status(f"Hotkeys F1-F{num_tracks} assegnate automaticamente")
                    
    def _rebuild_hotkey_map(self):
        """Ricostruisce la mappa degli hotkey"""
        self.hotkey_map = {}
        for track in self.playlist_manager.tracks:
            if track.hotkey:
                self.hotkey_map[track.hotkey] = track.index
            
    def _update_track_list(self):
        """Aggiorna la visualizzazione della playlist"""
        # Pulisci la lista
        for item in self.track_tree.get_children():
            self.track_tree.delete(item)
            
        # Aggiungi le tracce
        for track in self.playlist_manager.tracks:
            duration_str = self._format_time(track.duration) if track.duration > 0 else "--:--"
            
            # Formatta trim
            if track.start_time > 0 or track.end_time > 0:
                start_str = self._format_time(track.start_time)
                end_str = self._format_time(track.end_time) if track.end_time > 0 else "fine"
                trim_str = f"{start_str}-{end_str}"
            else:
                trim_str = ""
            
            loop_str = "🔁" if track.loop else ""
            hotkey_str = track.hotkey or ""
            volume_str = f"{track.volume}%"
            notes_str = track.notes[:30] + "..." if len(track.notes) > 30 else track.notes
            
            iid = self.track_tree.insert('', tk.END, values=(
                track.index + 1,
                track.title,
                duration_str,
                trim_str,
                loop_str,
                hotkey_str,
                volume_str,
                notes_str
            ))
            
            # Applica colore se presente
            if track.color:
                self.track_tree.tag_configure(f'color_{track.index}', background=track.color)
                self.track_tree.item(iid, tags=(f'color_{track.index}',))
            
    def _on_track_double_click(self, event):
        """Carica e riproduci la traccia con doppio click"""
        selection = self.track_tree.selection()
        if not selection:
            return
            
        item = self.track_tree.item(selection[0])
        index = int(item['values'][0]) - 1
        
        track = self.playlist_manager.set_current_track(index)
        if track:
            self._load_current_track()
            
    def _load_current_track(self):
        """Carica la traccia corrente nell'audio manager"""
        track = self.playlist_manager.get_current_track()
        if not track:
            return False
            
        if self.audio_manager.load_audio_file(track.filepath):
            # Aggiorna la durata
            duration = self.audio_manager.get_duration()
            self.playlist_manager.update_track_duration(track.index, duration)
            self._update_track_list()
            
            # Aggiorna loop
            self.loop_var.set(track.loop)
            self.audio_manager.set_loop(track.loop)
            
            # Applica trim se impostato
            self.audio_manager.set_trim(track.start_time, track.end_time)
            
            # Applica il volume della traccia al canale principale
            self.main_volume_var.set(track.volume)
            self.audio_manager.set_main_volume(track.volume / 100.0)
            self.main_volume_label.config(text=f"{track.volume}%")
            
            self.current_track_label.config(text=f"🎵 {track.title}")
            self.duration_label.config(text=self._format_time(duration))
            self._set_status(f"Caricata: {track.title}")
            
            # Aggiorna waveform
            if MATPLOTLIB_AVAILABLE:
                self._update_waveform()
            
            return True
        else:
            messagebox.showerror("Errore", f"Impossibile caricare: {track.filepath}")
            return False
            
    def _play_main(self):
        """Riproduci sul canale principale"""
        if not self._ensure_track_loaded():
            return
            
        if self.audio_manager.play_main():
            self.is_playing = True
            self.is_preview = False
            self.play_btn.config(state=tk.DISABLED)
            self.preview_btn.config(state=tk.DISABLED)
            self._set_status("▶ Riproduzione su uscita PRINCIPALE")
            
    def _play_preview(self):
        """Riproduci sul canale preview"""
        if not self._ensure_track_loaded():
            return
            
        if self.audio_manager.play_preview():
            self.is_playing = True
            self.is_preview = True
            self.play_btn.config(state=tk.DISABLED)
            self.preview_btn.config(state=tk.DISABLED)
            self._set_status("🎧 Riproduzione su uscita PREVIEW")
            
    def _pause(self):
        """Pausa la riproduzione"""
        self.audio_manager.pause()
        self.is_playing = False
        self.play_btn.config(state=tk.NORMAL)
        self.preview_btn.config(state=tk.NORMAL)
        self._set_status("⏸ Pausa")
        
    def _stop(self):
        """Ferma la riproduzione"""
        self.audio_manager.stop()
        self.is_playing = False
        self.is_preview = False
        self.play_btn.config(state=tk.NORMAL)
        self.preview_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.time_label.config(text="00:00")
        self._set_status("⏹ Stop")
        
    def _toggle_play(self):
        """Toggle play/pause"""
        if self.is_playing:
            self._pause()
        else:
            self._play_main()
            
    def _next_track(self):
        """Traccia successiva"""
        track = self.playlist_manager.next_track()
        if track:
            was_playing = self.is_playing
            was_preview = self.is_preview
            self._stop()
            
            if self._load_current_track():
                if was_playing:
                    if was_preview:
                        self._play_preview()
                    else:
                        self._play_main()
        else:
            self._set_status("Fine playlist")
            
    def _previous_track(self):
        """Traccia precedente"""
        track = self.playlist_manager.previous_track()
        if track:
            was_playing = self.is_playing
            was_preview = self.is_preview
            self._stop()
            
            if self._load_current_track():
                if was_playing:
                    if was_preview:
                        self._play_preview()
                    else:
                        self._play_main()
                        
    def _ensure_track_loaded(self) -> bool:
        """Assicura che una traccia sia caricata"""
        if self.audio_manager.current_audio is not None:
            return True
            
        # Prova a caricare la traccia corrente
        if self.playlist_manager.current_index >= 0:
            return self._load_current_track()
            
        # Prova a caricare la prima traccia
        if self.playlist_manager.get_track_count() > 0:
            self.playlist_manager.set_current_track(0)
            return self._load_current_track()
            
        messagebox.showinfo("Info", "Nessuna traccia disponibile.\nAggiungi tracce alla playlist.")
        return False
        
    def _save_playlist(self):
        """Salva la playlist con configurazione audio"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Playlist JSON", "*.json"), ("Tutti i file", "*.*")]
        )
        
        if filepath:
            # Prepara configurazione audio
            audio_config = self._get_audio_config()
            
            if self.playlist_manager.save_playlist(filepath, audio_config):
                self._set_status(f"Playlist salvata: {Path(filepath).name}")
            else:
                messagebox.showerror("Errore", "Impossibile salvare la playlist")
    
    def _get_audio_config(self):
        """Ottiene la configurazione audio corrente"""
        config = {}
        
        # Salva device ID
        if hasattr(self, 'audio_devices'):
            idx = self.main_device_combo.current()
            if idx >= 0 and idx < len(self.audio_devices):
                config['main_device_id'] = self.audio_devices[idx]['id']
                config['main_device_name'] = self.audio_devices[idx]['name']
            
            idx = self.preview_device_combo.current()
            if idx >= 0 and idx < len(self.audio_devices):
                config['preview_device_id'] = self.audio_devices[idx]['id']
                config['preview_device_name'] = self.audio_devices[idx]['name']
        
        # Salva volumi
        if hasattr(self, 'main_volume_var'):
            config['main_volume'] = self.main_volume_var.get()
        if hasattr(self, 'preview_volume_var'):
            config['preview_volume'] = self.preview_volume_var.get()
        
        return config
                
    def _load_playlist(self):
        """Carica una playlist con configurazione audio"""
        filepath = filedialog.askopenfilename(
            filetypes=[("Playlist JSON", "*.json"), ("Tutti i file", "*.*")]
        )
        
        if filepath:
            result = self.playlist_manager.load_playlist(filepath)
            
            # Gestisce il nuovo formato con tupla (success, audio_config)
            if isinstance(result, tuple):
                success, audio_config = result
            else:
                # Retrocompatibilità con vecchio formato
                success = result
                audio_config = None
            
            if success:
                self._update_track_list()
                self._rebuild_hotkey_map()
                
                # Applica configurazione audio se presente
                if audio_config:
                    self._apply_audio_config(audio_config)
                
                self._set_status(f"Playlist caricata: {Path(filepath).name}")
            else:
                messagebox.showerror("Errore", "Impossibile caricare la playlist")
    
    def _apply_audio_config(self, config):
        """Applica la configurazione audio caricata"""
        if not config or not hasattr(self, 'audio_devices'):
            return
        
        # Ripristina main device
        if 'main_device_id' in config:
            device_id = config['main_device_id']
            device_name = config.get('main_device_name', 'sconosciuto')
            
            for idx, device in enumerate(self.audio_devices):
                if device['id'] == device_id:
                    self.main_device_combo.current(idx)
                    self._on_main_device_changed()
                    print(f"✓ Main device ripristinato: {device['name']}")
                    break
            else:
                print(f"⚠ Main device '{device_name}' (ID: {device_id}) non trovato")
        
        # Ripristina preview device
        if 'preview_device_id' in config:
            device_id = config['preview_device_id']
            device_name = config.get('preview_device_name', 'sconosciuto')
            
            for idx, device in enumerate(self.audio_devices):
                if device['id'] == device_id:
                    self.preview_device_combo.current(idx)
                    self._on_preview_device_changed()
                    print(f"✓ Preview device ripristinato: {device['name']}")
                    break
            else:
                print(f"⚠ Preview device '{device_name}' (ID: {device_id}) non trovato")
        
        # Ripristina volumi
        if 'main_volume' in config and hasattr(self, 'main_volume_var'):
            self.main_volume_var.set(config['main_volume'])
            self._on_main_volume_changed()
        
        if 'preview_volume' in config and hasattr(self, 'preview_volume_var'):
            self.preview_volume_var.set(config['preview_volume'])
            self._on_preview_volume_changed()
                
    def _restore_backup(self):
        """Ripristina dall'ultimo backup"""
        playlist_path, config_path = self.auto_backup.get_latest_backup()
        
        if not playlist_path:
            messagebox.showinfo("Info", "Nessun backup disponibile")
            return
            
        if messagebox.askyesno("Conferma", "Ripristinare l'ultimo backup?"):
            if self.playlist_manager.load_playlist(playlist_path):
                self._update_track_list()
                self._rebuild_hotkey_map()
                self._set_status("Backup ripristinato")
            else:
                messagebox.showerror("Errore", "Impossibile ripristinare il backup")
                
    def _start_auto_backup(self):
        """Avvia il backup automatico"""
        config_data = {
            'main_device': self.main_device_combo.current() if hasattr(self, 'main_device_combo') else 0,
            'preview_device': self.preview_device_combo.current() if hasattr(self, 'preview_device_combo') else 0,
            'main_volume': self.main_volume_var.get() if hasattr(self, 'main_volume_var') else 100,
            'preview_volume': self.preview_volume_var.get() if hasattr(self, 'preview_volume_var') else 100
        }
        self.auto_backup.start(self.playlist_manager, config_data)
        
    def _start_update_thread(self):
        """Avvia il thread di aggiornamento UI"""
        def update_loop():
            while self.running:
                if self.is_playing and self.audio_manager.is_playing():
                    position = self.audio_manager.get_position()
                    duration = self.audio_manager.get_duration()
                    
                    if duration > 0:
                        progress = (position / duration) * 100
                        self.progress_var.set(progress)
                        self.time_label.config(text=self._format_time(position))
                        
                        # Auto next track quando finisce (se non loop)
                        if not self.audio_manager.is_loop_enabled() and position >= duration - 0.1:
                            self.root.after(0, self._handle_track_end)
                            
                time.sleep(0.1)
                
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()
        
    def _handle_track_end(self):
        """Gestisce la fine della traccia - si ferma invece di avanzare automaticamente"""
        self._stop()
        self._set_status("Traccia terminata")
            
    def _format_time(self, seconds: float) -> str:
        """Formatta i secondi in MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
        
    def _set_status(self, message: str):
        """Imposta il messaggio di stato"""
        backup_msg = " | Backup automatico attivo ogni 5 minuti"
        self.status_label.config(text=message + backup_msg)
    
    def _save_last_session(self):
        """Salva la configurazione della sessione corrente"""
        try:
            # Salva i device ID invece degli indici
            main_device_id = None
            preview_device_id = None
            
            if hasattr(self, 'main_device_combo') and hasattr(self, 'audio_devices'):
                idx = self.main_device_combo.current()
                if idx >= 0 and idx < len(self.audio_devices):
                    main_device_id = self.audio_devices[idx]['id']
                    print(f"Salvataggio main device: {self.audio_devices[idx]['name']} (ID: {main_device_id})")
            
            if hasattr(self, 'preview_device_combo') and hasattr(self, 'audio_devices'):
                idx = self.preview_device_combo.current()
                if idx >= 0 and idx < len(self.audio_devices):
                    preview_device_id = self.audio_devices[idx]['id']
                    print(f"Salvataggio preview device: {self.audio_devices[idx]['name']} (ID: {preview_device_id})")
            
            config = {
                'playlist': self.playlist_manager.to_dict()['tracks'],
                'main_device_id': main_device_id,
                'preview_device_id': preview_device_id,
                'main_volume': self.main_volume_var.get() if hasattr(self, 'main_volume_var') else 100,
                'preview_volume': self.preview_volume_var.get() if hasattr(self, 'preview_volume_var') else 100,
                'current_track_index': self.playlist_manager.current_index if self.playlist_manager.current_index >= 0 else None
            }
            
            with open(self.last_session_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"File salvato in: {self.last_session_file}")
            print(f"Config salvata: main_device_id={main_device_id}, preview_device_id={preview_device_id}")
            
            return True
        except Exception as e:
            print(f"Errore nel salvataggio della sessione: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _load_last_session(self):
        """Carica la configurazione dell'ultima sessione"""
        if not self.last_session_file.exists():
            print(f"Nessuna sessione precedente trovata in: {self.last_session_file}")
            return False
        
        print(f"Caricamento sessione da: {self.last_session_file}")
        
        try:
            with open(self.last_session_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"Config caricata: main_device_id={config.get('main_device_id')}, preview_device_id={config.get('preview_device_id')}")
            
            # Ripristina playlist
            if 'playlist' in config and config['playlist']:
                self.playlist_manager.from_dict({'tracks': config['playlist']})
                self._update_track_list()
                self._rebuild_hotkey_map()
            
            # Ripristina dispositivi audio cercando per device ID
            if hasattr(self, 'audio_devices'):
                # Ripristina main device
                if 'main_device_id' in config and config['main_device_id'] is not None:
                    print(f"Cercando main device ID: {config['main_device_id']}")
                    for idx, device in enumerate(self.audio_devices):
                        if device['id'] == config['main_device_id']:
                            try:
                                self.main_device_combo.current(idx)
                                self._on_main_device_changed()
                                print(f"✓ Main device ripristinato: {device['name']}")
                            except Exception as e:
                                print(f"Errore ripristino main device: {e}")
                            break
                    else:
                        print(f"⚠ Main device ID {config['main_device_id']} non trovato")
                
                # Ripristina preview device
                if 'preview_device_id' in config and config['preview_device_id'] is not None:
                    print(f"Cercando preview device ID: {config['preview_device_id']}")
                    for idx, device in enumerate(self.audio_devices):
                        if device['id'] == config['preview_device_id']:
                            try:
                                self.preview_device_combo.current(idx)
                                self._on_preview_device_changed()
                                print(f"✓ Preview device ripristinato: {device['name']}")
                            except Exception as e:
                                print(f"Errore ripristino preview device: {e}")
                            break
                    else:
                        print(f"⚠ Preview device ID {config['preview_device_id']} non trovato")
            
            # Ripristina volumi
            if hasattr(self, 'main_volume_var') and 'main_volume' in config:
                self.main_volume_var.set(config['main_volume'])
                self._on_main_volume_changed()
            
            if hasattr(self, 'preview_volume_var') and 'preview_volume' in config:
                self.preview_volume_var.set(config['preview_volume'])
                self._on_preview_volume_changed()
            
            # Ripristina traccia corrente (senza caricarla)
            if 'current_track_index' in config and config['current_track_index'] is not None:
                self.playlist_manager.current_index = config['current_track_index']
            
            self._set_status("Ultima sessione ripristinata")
            return True
            
        except Exception as e:
            print(f"Errore nel caricamento della sessione: {e}")
            return False
        
    def _on_closing(self):
        """Gestisce la chiusura dell'applicazione"""
        # Salva la sessione corrente
        if self._save_last_session():
            print("✓ Sessione salvata con successo (playlist + dispositivi audio)")
        
        # Crea backup finale
        self.auto_backup.create_backup()
        
        self.running = False
        self.auto_backup.stop()
        self._stop()
        self.root.destroy()


def main():
    """Funzione principale"""
    root = tk.Tk()
    app = AudioManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
