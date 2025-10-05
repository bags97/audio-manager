"""
Audio Manager Module
Gestisce la riproduzione audio su due canali separati: main e preview
"""

import sounddevice as sd
import numpy as np
import wave
import os
from typing import Optional, Tuple
import threading
import queue


class AudioOutput:
    """Gestisce un singolo canale di output audio"""
    
    def __init__(self, device_id: Optional[int] = None, name: str = "Output"):
        self.device_id = device_id
        self.name = name
        self.stream = None
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0
        self.audio_data = None
        self.sample_rate = 44100
        self.volume = 1.0  # Volume 0.0 - 1.0 (0% - 100%)
        self.loop_enabled = False  # Loop mode
        self.lock = threading.Lock()
        
    def load_audio(self, audio_data: np.ndarray, sample_rate: int):
        """Carica un array audio in memoria"""
        with self.lock:
            # Normalizza a float32 se necessario
            if audio_data.dtype == np.int16:
                self.audio_data = audio_data.astype(np.float32) / 32768.0
            elif audio_data.dtype == np.int32:
                self.audio_data = audio_data.astype(np.float32) / 2147483648.0
            else:
                self.audio_data = audio_data.astype(np.float32)
                
            self.sample_rate = sample_rate
            self.current_position = 0
    
    def set_volume(self, volume: float):
        """Imposta il volume (0.0 - 1.0)"""
        with self.lock:
            self.volume = max(0.0, min(1.0, volume))
    
    def set_loop(self, loop: bool):
        """Imposta la modalità loop"""
        with self.lock:
            self.loop_enabled = loop
            
    def play(self):
        """Avvia la riproduzione"""
        with self.lock:
            if self.audio_data is None:
                return False
                
            if self.is_paused:
                self.is_paused = False
                return True
                
            self.is_playing = True
            self._start_stream()
            return True
            
    def pause(self):
        """Mette in pausa la riproduzione"""
        with self.lock:
            self.is_paused = True
            
    def stop(self):
        """Ferma la riproduzione"""
        with self.lock:
            self.is_playing = False
            self.is_paused = False
            self.current_position = 0
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None
                
    def _start_stream(self):
        """Avvia lo stream audio"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            
        def callback(outdata, frames, time_info, status):
            with self.lock:
                if not self.is_playing or self.is_paused:
                    outdata.fill(0)
                    return
                    
                if self.audio_data is None:
                    outdata.fill(0)
                    return
                    
                remaining = len(self.audio_data) - self.current_position
                if remaining <= 0:
                    # Gestione loop
                    if self.loop_enabled:
                        self.current_position = 0
                        remaining = len(self.audio_data)
                    else:
                        outdata.fill(0)
                        self.is_playing = False
                        return
                    
                chunk_size = min(frames, remaining)
                chunk = self.audio_data[self.current_position:self.current_position + chunk_size]
                # Applica il volume
                outdata[:chunk_size] = chunk * self.volume
                
                if chunk_size < frames:
                    outdata[chunk_size:].fill(0)
                    
                self.current_position += chunk_size
                
        try:
            channels = self.audio_data.shape[1] if len(self.audio_data.shape) > 1 else 1
            self.stream = sd.OutputStream(
                device=self.device_id,
                channels=channels,
                callback=callback,
                samplerate=self.sample_rate
            )
            self.stream.start()
        except Exception as e:
            print(f"Errore avvio stream {self.name}: {e}")
            self.is_playing = False
            
    def get_position(self) -> float:
        """Ritorna la posizione corrente in secondi"""
        with self.lock:
            if self.audio_data is None:
                return 0.0
            return self.current_position / self.sample_rate
            
    def get_duration(self) -> float:
        """Ritorna la durata totale in secondi"""
        with self.lock:
            if self.audio_data is None:
                return 0.0
            return len(self.audio_data) / self.sample_rate


class DualAudioManager:
    """Gestisce due canali audio separati: main e preview"""
    
    def __init__(self):
        self.main_output = AudioOutput(name="Main")
        self.preview_output = AudioOutput(name="Preview")
        self.current_audio = None
        self.preview_mode = False
        self.loop_enabled = False
        
    def set_main_device(self, device_id: int):
        """Imposta il dispositivo per l'uscita principale"""
        self.main_output.device_id = device_id
        
    def set_preview_device(self, device_id: int):
        """Imposta il dispositivo per l'uscita preview"""
        self.preview_output.device_id = device_id
    
    def set_main_volume(self, volume: float):
        """Imposta il volume dell'uscita principale (0.0 - 1.0)"""
        self.main_output.set_volume(volume)
    
    def set_preview_volume(self, volume: float):
        """Imposta il volume dell'uscita preview (0.0 - 1.0)"""
        self.preview_output.set_volume(volume)
    
    def get_main_volume(self) -> float:
        """Ottieni il volume dell'uscita principale"""
        return self.main_output.volume
    
    def get_preview_volume(self) -> float:
        """Ottieni il volume dell'uscita preview"""
        return self.preview_output.volume
    
    def set_loop(self, loop: bool):
        """Imposta la modalità loop per entrambi i canali"""
        self.loop_enabled = loop
        self.main_output.set_loop(loop)
        self.preview_output.set_loop(loop)
    
    def is_loop_enabled(self) -> bool:
        """Verifica se il loop è abilitato"""
        return self.loop_enabled
        
    def load_audio_file(self, filepath: str):
        """Carica un file audio (supporta WAV, MP3 con scipy)"""
        try:
            file_ext = os.path.splitext(filepath)[1].lower()
            
            if file_ext == '.wav':
                # Carica file WAV nativo
                audio_data, sample_rate = self._load_wav(filepath)
            elif file_ext in ['.mp3', '.ogg', '.flac']:
                # Prova a caricare con soundfile (supporta molti formati)
                try:
                    import soundfile as sf
                    audio_data, sample_rate = sf.read(filepath, dtype='float32')
                except ImportError:
                    raise Exception("Per file MP3/OGG/FLAC installa: pip install soundfile")
            else:
                raise Exception(f"Formato non supportato: {file_ext}")
            
            self.current_audio = filepath
            
            # Carica su entrambi i canali
            self.main_output.load_audio(audio_data, sample_rate)
            self.preview_output.load_audio(audio_data.copy(), sample_rate)
            return True
        except Exception as e:
            print(f"Errore caricamento audio: {e}")
            return False
    
    def _load_wav(self, filepath: str) -> Tuple[np.ndarray, int]:
        """Carica un file WAV"""
        with wave.open(filepath, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            n_channels = wav_file.getnchannels()
            n_frames = wav_file.getnframes()
            sample_width = wav_file.getsampwidth()
            
            # Leggi i dati audio
            audio_bytes = wav_file.readframes(n_frames)
            
            # Converti in numpy array
            if sample_width == 1:
                dtype = np.uint8
            elif sample_width == 2:
                dtype = np.int16
            elif sample_width == 4:
                dtype = np.int32
            else:
                raise Exception(f"Sample width non supportato: {sample_width}")
            
            audio_data = np.frombuffer(audio_bytes, dtype=dtype)
            
            # Reshape per stereo
            if n_channels == 2:
                audio_data = audio_data.reshape((-1, 2))
            elif n_channels == 1:
                audio_data = audio_data.reshape((-1, 1))
            
            return audio_data, sample_rate
            
    def play_main(self):
        """Riproduci sul canale principale"""
        self.preview_mode = False
        self.preview_output.stop()
        return self.main_output.play()
        
    def play_preview(self):
        """Riproduci sul canale preview"""
        self.preview_mode = True
        self.main_output.stop()
        return self.preview_output.play()
        
    def pause(self):
        """Metti in pausa il canale attivo"""
        if self.preview_mode:
            self.preview_output.pause()
        else:
            self.main_output.pause()
            
    def stop(self):
        """Ferma entrambi i canali"""
        self.main_output.stop()
        self.preview_output.stop()
        
    def get_position(self) -> float:
        """Ottieni la posizione corrente"""
        if self.preview_mode:
            return self.preview_output.get_position()
        return self.main_output.get_position()
        
    def get_duration(self) -> float:
        """Ottieni la durata totale"""
        return self.main_output.get_duration()
        
    def is_playing(self) -> bool:
        """Verifica se è in riproduzione"""
        return self.main_output.is_playing or self.preview_output.is_playing
        
    @staticmethod
    def get_audio_devices() -> list:
        """Ottieni la lista di tutti i dispositivi audio disponibili"""
        devices = sd.query_devices()
        output_devices = []
        
        for idx, device in enumerate(devices):
            if device['max_output_channels'] > 0:
                output_devices.append({
                    'id': idx,
                    'name': device['name'],
                    'channels': device['max_output_channels'],
                    'sample_rate': device['default_samplerate']
                })
                
        return output_devices
