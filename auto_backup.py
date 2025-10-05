"""
Auto Backup Module
Gestisce il salvataggio automatico della playlist e configurazione
"""

import os
import json
import threading
import time
from datetime import datetime
from pathlib import Path


class AutoBackup:
    """Gestisce il backup automatico"""
    
    def __init__(self, backup_dir: str = "backups", interval_seconds: int = 300):
        self.backup_dir = backup_dir
        self.interval = interval_seconds
        self.running = False
        self.thread = None
        self.playlist_manager = None
        self.config_data = {}
        
        # Crea la directory di backup se non esiste
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def start(self, playlist_manager, config_data: dict):
        """Avvia il backup automatico"""
        self.playlist_manager = playlist_manager
        self.config_data = config_data
        self.running = True
        self.thread = threading.Thread(target=self._backup_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Ferma il backup automatico"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
            
    def _backup_loop(self):
        """Loop di backup"""
        while self.running:
            time.sleep(self.interval)
            if self.running:
                self.create_backup()
                
    def create_backup(self):
        """Crea un backup della playlist e configurazione"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Backup playlist
            if self.playlist_manager and self.playlist_manager.get_track_count() > 0:
                playlist_backup = os.path.join(self.backup_dir, f"playlist_backup_{timestamp}.json")
                self.playlist_manager.save_playlist(playlist_backup)
                
            # Backup configurazione
            if self.config_data:
                config_backup = os.path.join(self.backup_dir, f"config_backup_{timestamp}.json")
                with open(config_backup, 'w', encoding='utf-8') as f:
                    json.dump(self.config_data, f, indent=2)
                    
            # Pulisci vecchi backup (mantieni solo gli ultimi 10)
            self._cleanup_old_backups()
            
            return True
        except Exception as e:
            print(f"Errore durante il backup: {e}")
            return False
            
    def _cleanup_old_backups(self):
        """Rimuove i backup più vecchi, mantenendo solo gli ultimi 10"""
        try:
            # Lista tutti i file di backup
            playlist_backups = sorted(
                [f for f in os.listdir(self.backup_dir) if f.startswith("playlist_backup_")],
                reverse=True
            )
            config_backups = sorted(
                [f for f in os.listdir(self.backup_dir) if f.startswith("config_backup_")],
                reverse=True
            )
            
            # Rimuovi i file più vecchi
            for backup_file in playlist_backups[10:]:
                os.remove(os.path.join(self.backup_dir, backup_file))
                
            for backup_file in config_backups[10:]:
                os.remove(os.path.join(self.backup_dir, backup_file))
                
        except Exception as e:
            print(f"Errore pulizia backup: {e}")
            
    def get_latest_backup(self) -> tuple:
        """Ritorna i path dell'ultimo backup (playlist, config)"""
        try:
            playlist_backups = sorted(
                [f for f in os.listdir(self.backup_dir) if f.startswith("playlist_backup_")],
                reverse=True
            )
            config_backups = sorted(
                [f for f in os.listdir(self.backup_dir) if f.startswith("config_backup_")],
                reverse=True
            )
            
            playlist_path = os.path.join(self.backup_dir, playlist_backups[0]) if playlist_backups else None
            config_path = os.path.join(self.backup_dir, config_backups[0]) if config_backups else None
            
            return playlist_path, config_path
        except Exception as e:
            print(f"Errore recupero backup: {e}")
            return None, None
