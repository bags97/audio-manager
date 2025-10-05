#!/usr/bin/env python3
"""
Test di compatibilità multi-piattaforma
Verifica che tutte le dipendenze siano installate correttamente
"""

import sys
import platform

def test_imports():
    """Testa l'importazione di tutte le dipendenze"""
    print("=" * 60)
    print("Test Compatibilità Audio Manager")
    print("=" * 60)
    print(f"\nPython: {sys.version}")
    print(f"Piattaforma: {platform.system()} {platform.release()}")
    print(f"Architettura: {platform.machine()}\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test tkinter (GUI)
    try:
        import tkinter as tk
        from tkinter import ttk
        print("✓ tkinter (GUI)")
        tests_passed += 1
    except ImportError as e:
        print(f"✗ tkinter (GUI) - ERRORE: {e}")
        tests_failed += 1
    
    # Test sounddevice (audio I/O)
    try:
        import sounddevice as sd
        print(f"✓ sounddevice {sd.__version__} (Audio I/O)")
        tests_passed += 1
    except ImportError as e:
        print(f"✗ sounddevice - ERRORE: {e}")
        tests_failed += 1
    
    # Test soundfile (lettura file audio)
    try:
        import soundfile as sf
        print(f"✓ soundfile {sf.__version__} (File Audio)")
        tests_passed += 1
    except ImportError as e:
        print(f"✗ soundfile - ERRORE: {e}")
        tests_failed += 1
    
    # Test numpy (elaborazione audio)
    try:
        import numpy as np
        print(f"✓ numpy {np.__version__} (Elaborazione)")
        tests_passed += 1
    except ImportError as e:
        print(f"✗ numpy - ERRORE: {e}")
        tests_failed += 1
    
    # Test matplotlib (waveform - opzionale)
    try:
        import matplotlib
        print(f"✓ matplotlib {matplotlib.__version__} (Waveform - opzionale)")
        tests_passed += 1
    except ImportError:
        print("⚠ matplotlib non disponibile (waveform disabilitato)")
    
    # Test pathlib (gestione path cross-platform)
    try:
        from pathlib import Path
        test_path = Path.home() / ".audio_manager_test"
        print(f"✓ pathlib (Path: {test_path})")
        tests_passed += 1
    except Exception as e:
        print(f"✗ pathlib - ERRORE: {e}")
        tests_failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test completati: {tests_passed + tests_failed}")
    print(f"✓ Successi: {tests_passed}")
    print(f"✗ Fallimenti: {tests_failed}")
    print("=" * 60)
    
    if tests_failed > 0:
        print("\n⚠ ATTENZIONE: Alcune dipendenze non sono installate!")
        print("Esegui: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ Tutte le dipendenze sono installate correttamente!")
        print("Il programma è pronto per l'uso.")
        return True


def test_audio_devices():
    """Testa la disponibilità di dispositivi audio"""
    try:
        import sounddevice as sd
        print("\n" + "=" * 60)
        print("Dispositivi Audio Disponibili")
        print("=" * 60)
        devices = sd.query_devices()
        
        input_devices = []
        output_devices = []
        
        for i, device in enumerate(devices):
            if device['max_output_channels'] > 0:
                output_devices.append((i, device['name']))
                print(f"Output {i}: {device['name']}")
        
        if not output_devices:
            print("⚠ ATTENZIONE: Nessun dispositivo di output trovato!")
            return False
        
        print(f"\n✓ Trovati {len(output_devices)} dispositivi di output")
        return True
        
    except Exception as e:
        print(f"\n✗ Errore nel rilevamento dispositivi: {e}")
        return False


def main():
    """Funzione principale"""
    imports_ok = test_imports()
    
    if imports_ok:
        audio_ok = test_audio_devices()
        
        if audio_ok:
            print("\n" + "=" * 60)
            print("✓ SISTEMA PRONTO!")
            print("=" * 60)
            print("\nPuoi avviare l'applicazione con:")
            print("  python main.py")
            print("\nOppure crea un eseguibile con:")
            if platform.system() == "Windows":
                print("  build.bat")
            else:
                print("  ./build.sh")
            return 0
    
    print("\n" + "=" * 60)
    print("✗ CONFIGURAZIONE INCOMPLETA")
    print("=" * 60)
    print("\nRisolvi i problemi segnalati e riprova.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
