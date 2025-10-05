"""
Playlist Manager Module
Gestisce la lista di tracce audio, l'ordine e il caricamento
"""

import json
import os
from typing import List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class AudioTrack:
    """Rappresenta una singola traccia audio"""
    filepath: str
    title: str
    duration: float = 0.0
    index: int = 0
    notes: str = ""  # Note/marker per identificare la scena
    color: str = ""  # Colore per categorizzazione (hex: #RRGGBB)
    loop: bool = False  # Se true, la traccia si ripete in loop
    hotkey: str = ""  # Tasto rapido (1-9, F1-F12, etc)
    volume: int = 100  # Volume personalizzato per questa traccia (0-100)
    
    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict):
        return AudioTrack(**data)


class PlaylistManager:
    """Gestisce la playlist di tracce audio"""
    
    def __init__(self):
        self.tracks: List[AudioTrack] = []
        self.current_index: int = -1
        self.playlist_file: Optional[str] = None
        
    def add_track(self, filepath: str, title: Optional[str] = None) -> AudioTrack:
        """Aggiunge una traccia alla playlist"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File non trovato: {filepath}")
            
        # Usa il nome del file se non viene fornito un titolo
        if title is None:
            title = Path(filepath).stem
            
        # Calcola la durata (verrà aggiornata quando caricata)
        track = AudioTrack(
            filepath=filepath,
            title=title,
            index=len(self.tracks)
        )
        
        self.tracks.append(track)
        self._update_indices()
        return track
        
    def add_tracks(self, filepaths: List[str]) -> List[AudioTrack]:
        """Aggiunge multiple tracce alla playlist"""
        added_tracks = []
        for filepath in filepaths:
            try:
                track = self.add_track(filepath)
                added_tracks.append(track)
            except Exception as e:
                print(f"Errore aggiunta traccia {filepath}: {e}")
        return added_tracks
        
    def remove_track(self, index: int) -> bool:
        """Rimuove una traccia dalla playlist"""
        if 0 <= index < len(self.tracks):
            self.tracks.pop(index)
            self._update_indices()
            
            # Aggiusta l'indice corrente se necessario
            if self.current_index >= len(self.tracks):
                self.current_index = len(self.tracks) - 1
            elif self.current_index > index:
                self.current_index -= 1
                
            return True
        return False
        
    def move_track(self, from_index: int, to_index: int) -> bool:
        """Sposta una traccia da una posizione ad un'altra"""
        if not (0 <= from_index < len(self.tracks) and 0 <= to_index < len(self.tracks)):
            return False
            
        track = self.tracks.pop(from_index)
        self.tracks.insert(to_index, track)
        self._update_indices()
        
        # Aggiusta l'indice corrente
        if self.current_index == from_index:
            self.current_index = to_index
        elif from_index < self.current_index <= to_index:
            self.current_index -= 1
        elif to_index <= self.current_index < from_index:
            self.current_index += 1
            
        return True
    
    def reverse_tracks(self):
        """Inverte completamente l'ordine delle tracce"""
        if len(self.tracks) == 0:
            return False
            
        self.tracks.reverse()
        self._update_indices()
        
        # Aggiorna l'indice corrente se una traccia è selezionata
        if self.current_index >= 0:
            self.current_index = len(self.tracks) - 1 - self.current_index
            
        return True
        
    def get_track(self, index: int) -> Optional[AudioTrack]:
        """Ottiene una traccia per indice"""
        if 0 <= index < len(self.tracks):
            return self.tracks[index]
        return None
        
    def get_current_track(self) -> Optional[AudioTrack]:
        """Ottiene la traccia corrente"""
        return self.get_track(self.current_index)
        
    def next_track(self) -> Optional[AudioTrack]:
        """Passa alla traccia successiva"""
        if self.current_index < len(self.tracks) - 1:
            self.current_index += 1
            return self.get_current_track()
        return None
        
    def previous_track(self) -> Optional[AudioTrack]:
        """Passa alla traccia precedente"""
        if self.current_index > 0:
            self.current_index -= 1
            return self.get_current_track()
        return None
        
    def set_current_track(self, index: int) -> Optional[AudioTrack]:
        """Imposta la traccia corrente per indice"""
        if 0 <= index < len(self.tracks):
            self.current_index = index
            return self.get_current_track()
        return None
        
    def has_next(self) -> bool:
        """Verifica se c'è una traccia successiva"""
        return self.current_index < len(self.tracks) - 1
        
    def has_previous(self) -> bool:
        """Verifica se c'è una traccia precedente"""
        return self.current_index > 0
        
    def clear(self):
        """Svuota la playlist"""
        self.tracks.clear()
        self.current_index = -1
        
    def get_track_count(self) -> int:
        """Ritorna il numero di tracce"""
        return len(self.tracks)
        
    def save_playlist(self, filepath: str) -> bool:
        """Salva la playlist in un file JSON"""
        try:
            data = {
                'tracks': [track.to_dict() for track in self.tracks],
                'current_index': self.current_index
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            self.playlist_file = filepath
            return True
        except Exception as e:
            print(f"Errore salvataggio playlist: {e}")
            return False
            
    def load_playlist(self, filepath: str) -> bool:
        """Carica una playlist da un file JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.tracks = [AudioTrack.from_dict(track_data) for track_data in data['tracks']]
            self.current_index = data.get('current_index', -1)
            self._update_indices()
            
            self.playlist_file = filepath
            return True
        except Exception as e:
            print(f"Errore caricamento playlist: {e}")
            return False
            
    def _update_indices(self):
        """Aggiorna gli indici di tutte le tracce"""
        for i, track in enumerate(self.tracks):
            track.index = i
            
    def update_track_duration(self, index: int, duration: float):
        """Aggiorna la durata di una traccia"""
        track = self.get_track(index)
        if track:
            track.duration = duration
    
    def update_track_notes(self, index: int, notes: str):
        """Aggiorna le note di una traccia"""
        track = self.get_track(index)
        if track:
            track.notes = notes
            
    def update_track_color(self, index: int, color: str):
        """Aggiorna il colore di una traccia"""
        track = self.get_track(index)
        if track:
            track.color = color
            
    def update_track_loop(self, index: int, loop: bool):
        """Aggiorna lo stato loop di una traccia"""
        track = self.get_track(index)
        if track:
            track.loop = loop
            
    def update_track_hotkey(self, index: int, hotkey: str):
        """Aggiorna l'hotkey di una traccia"""
        track = self.get_track(index)
        if track:
            track.hotkey = hotkey
    
    def update_track_volume(self, index: int, volume: int):
        """Aggiorna il volume personalizzato di una traccia (0-100)"""
        track = self.get_track(index)
        if track:
            track.volume = max(0, min(100, volume))
            
    def get_track_by_hotkey(self, hotkey: str) -> Optional[AudioTrack]:
        """Trova una traccia per hotkey"""
        for track in self.tracks:
            if track.hotkey == hotkey:
                return track
        return None
