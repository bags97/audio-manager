#!/usr/bin/env python3
"""
Verifica Portabilità - Audio Manager Teatrale
Mostra lo status del progetto e la readiness per distribuzione multi-piattaforma
"""

import os
import sys
from pathlib import Path

def check_mark(condition):
    """Restituisce checkmark o cross basato sulla condizione"""
    return "✓" if condition else "✗"

def main():
    print("=" * 70)
    print(" 🌍 VERIFICA PORTABILITÀ - AUDIO MANAGER TEATRALE")
    print("=" * 70)
    print()
    
    # Verifica file principali applicazione
    print("📱 FILE APPLICAZIONE:")
    app_files = {
        "main.py": "GUI principale",
        "audio_manager.py": "Engine audio dual-output",
        "playlist_manager.py": "Gestione playlist",
        "auto_backup.py": "Sistema backup automatico"
    }
    
    for file, desc in app_files.items():
        exists = Path(file).exists()
        print(f"  {check_mark(exists)} {file:25} - {desc}")
    
    print()
    
    # Verifica file build
    print("🔧 FILE BUILD & SETUP:")
    build_files = {
        "audio_manager.spec": "Config PyInstaller multi-platform",
        "build.bat": "Build script Windows",
        "build.sh": "Build script macOS/Linux",
        "setup.bat": "Setup rapido Windows",
        "setup.sh": "Setup rapido macOS/Linux",
        "requirements.txt": "Dipendenze Python"
    }
    
    for file, desc in build_files.items():
        exists = Path(file).exists()
        print(f"  {check_mark(exists)} {file:25} - {desc}")
    
    print()
    
    # Verifica documentazione
    print("📚 DOCUMENTAZIONE:")
    doc_files = {
        "README.md": "Guida principale completa",
        "BUILD.md": "Guida build & distribuzione",
        "FAQ.md": "Domande frequenti",
        "PORTABLE.md": "Dettagli portabilità",
        "QUICKSTART.md": "Quick start guide",
        "LICENSE": "Licenza MIT"
    }
    
    for file, desc in doc_files.items():
        exists = Path(file).exists()
        size = Path(file).stat().st_size if exists else 0
        print(f"  {check_mark(exists)} {file:25} - {desc} ({size} bytes)")
    
    print()
    
    # Verifica test
    print("🧪 FILE TEST:")
    test_files = {
        "test_compatibility.py": "Test compatibilità multi-platform"
    }
    
    for file, desc in test_files.items():
        exists = Path(file).exists()
        print(f"  {check_mark(exists)} {file:25} - {desc}")
    
    print()
    
    # Verifica configurazione
    print("⚙️ CONFIGURAZIONE:")
    config_files = {
        ".gitignore": "Esclusioni Git multi-platform"
    }
    
    for file, desc in config_files.items():
        exists = Path(file).exists()
        print(f"  {check_mark(exists)} {file:25} - {desc}")
    
    print()
    
    # Conteggio file
    total_py_files = len(list(Path(".").glob("*.py")))
    total_md_files = len(list(Path(".").glob("*.md")))
    total_bat_files = len(list(Path(".").glob("*.bat")))
    total_sh_files = len(list(Path(".").glob("*.sh")))
    
    print("📊 STATISTICHE:")
    print(f"  Python files (.py):     {total_py_files}")
    print(f"  Markdown docs (.md):    {total_md_files}")
    print(f"  Windows scripts (.bat): {total_bat_files}")
    print(f"  Unix scripts (.sh):     {total_sh_files}")
    print()
    
    # Verifica readiness
    print("=" * 70)
    print(" 🎯 READINESS PORTABILITÀ")
    print("=" * 70)
    print()
    
    checks = [
        (Path("audio_manager.spec").exists(), "PyInstaller spec configurato"),
        (Path("build.bat").exists() and Path("build.sh").exists(), "Build scripts per tutti gli OS"),
        (Path("requirements.txt").exists(), "Dipendenze documentate"),
        (Path("README.md").exists(), "Documentazione principale"),
        (Path("test_compatibility.py").exists(), "Test compatibilità disponibile"),
        (Path("LICENSE").exists(), "Licenza definita")
    ]
    
    passed = sum(1 for check, _ in checks if check)
    total = len(checks)
    
    for check, desc in checks:
        print(f"  {check_mark(check)} {desc}")
    
    print()
    print(f"  Score: {passed}/{total} ({passed*100//total}%)")
    print()
    
    if passed == total:
        print("  🎉 PRONTO PER DISTRIBUZIONE MULTI-PIATTAFORMA!")
        print()
        print("  Prossimi passi:")
        print("    1. Test build su ciascun OS target")
        print("    2. Validazione eseguibili")
        print("    3. Creazione release GitHub")
        print()
        return 0
    else:
        print("  ⚠️  Alcuni file mancanti - verifica setup")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
