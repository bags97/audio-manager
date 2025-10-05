"""
Script per verificare il contenuto del file di sessione
"""
import json
from pathlib import Path

session_file = Path.home() / ".audio_manager" / "last_session.json"

if session_file.exists():
    print(f"✓ File trovato: {session_file}")
    print("\nContenuto:")
    
    with open(session_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print(json.dumps(config, indent=2, ensure_ascii=False))
    
    print("\n--- DISPOSITIVI AUDIO ---")
    print(f"Main device ID: {config.get('main_device_id')}")
    print(f"Preview device ID: {config.get('preview_device_id')}")
    print(f"Main volume: {config.get('main_volume')}")
    print(f"Preview volume: {config.get('preview_volume')}")
    print(f"Numero tracce: {len(config.get('playlist', []))}")
else:
    print(f"✗ File non trovato: {session_file}")
    print("\nProva a:")
    print("1. Avviare l'applicazione")
    print("2. Selezionare i dispositivi audio")
    print("3. Chiudere l'applicazione")
    print("4. Eseguire nuovamente questo script")
