#!/usr/bin/env python3
"""
Script de setup para Voice CLI
Instala dependencias opcionales y verifica la configuración
"""

import subprocess
import sys
import os

def check_dependency(package):
    """Verifica si un paquete está instalado"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def install_package(package):
    """Instala un paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_ffmpeg():
    """Verifica si FFmpeg está disponible"""
    try:
        subprocess.run(["ffmpeg", "-version"],
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL,
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("🎤 Voice CLI - Setup y verificación")
    print("=" * 50)

    # Verificar dependencias básicas
    print("\n📦 Verificando dependencias básicas...")
    basic_deps = [
        ("whisper", "openai-whisper"),
        ("sounddevice", "sounddevice"),
        ("scipy", "scipy"),
        ("numpy", "numpy")
    ]

    for module, package in basic_deps:
        if check_dependency(module):
            print(f"✅ {package}")
        else:
            print(f"❌ {package} - FALTA")

    # Verificar FFmpeg
    print("\n🎵 Verificando FFmpeg...")
    if check_ffmpeg():
        print("✅ FFmpeg disponible")
    else:
        print("❌ FFmpeg no encontrado")
        print("💡 Instala FFmpeg desde: https://ffmpeg.org/download.html")

    # Preguntar por dependencias PRO
    print("\n🌟 ¿Quieres instalar las funcionalidades PRO?")
    print("   - Hotkeys globales (pynput)")
    print("   - Portapapeles automático (pyperclip)")

    response = input("\n¿Instalar dependencias PRO? (y/n): ").lower().strip()

    if response in ['y', 'yes', 'sí', 's']:
        print("\n⬇️  Instalando dependencias PRO...")

        pro_deps = [
            ("pynput", "Para hotkeys globales"),
            ("pyperclip", "Para portapapeles automático")
        ]

        for package, description in pro_deps:
            print(f"\n📦 Instalando {package} ({description})...")
            if install_package(package):
                print(f"✅ {package} instalado correctamente")
            else:
                print(f"❌ Error instalando {package}")

    # Verificar estado final
    print("\n📊 ESTADO FINAL:")
    print("-" * 30)

    # Verificar todas las dependencias
    all_deps = [
        ("whisper", "Transcripción con Whisper", True),
        ("sounddevice", "Grabación de audio", True),
        ("scipy", "Procesamiento de señales", True),
        ("numpy", "Operaciones numéricas", True),
        ("pynput", "Hotkeys globales (PRO)", False),
        ("pyperclip", "Portapapeles (PRO)", False),
    ]

    basic_ok = True
    pro_available = True

    for module, description, required in all_deps:
        available = check_dependency(module)
        status = "✅" if available else "❌"
        req_text = "REQUERIDO" if required else "OPCIONAL"

        print(f"{status} {description} ({req_text})")

        if required and not available:
            basic_ok = False
        if not required and not available:
            pro_available = False

    # Verificar FFmpeg
    ffmpeg_ok = check_ffmpeg()
    ffmpeg_status = "✅" if ffmpeg_ok else "❌"
    print(f"{ffmpeg_status} FFmpeg (REQUERIDO)")

    if not ffmpeg_ok:
        basic_ok = False

    # Resumen
    print("\n🎯 RESUMEN:")
    if basic_ok:
        print("✅ Funcionalidades básicas: DISPONIBLES")
        print("   Puedes usar: python main.py")
    else:
        print("❌ Funcionalidades básicas: FALTAN DEPENDENCIAS")

    if basic_ok and pro_available:
        print("✅ Funcionalidades PRO: DISPONIBLES")
        print("   Puedes usar: python main_pro.py")
    elif basic_ok:
        print("⚠️  Funcionalidades PRO: PARCIALES")
        print("   Usa main.py o instala dependencias PRO")
    else:
        print("❌ Funcionalidades PRO: NO DISPONIBLES")

    # Instrucciones finales
    print("\n💡 PRÓXIMOS PASOS:")
    if basic_ok:
        print("1. python main.py              # Versión básica")
        if pro_available:
            print("2. python main_pro.py          # Versión PRO")
        print("3. Escribe 'help' para ver comandos")
        print("4. Escribe 'start' para grabar")
    else:
        print("1. Instalar dependencias faltantes")
        if not ffmpeg_ok:
            print("2. Instalar FFmpeg")
        print("3. Ejecutar este script nuevamente")

    print("\n🎉 ¡Setup completado!")

if __name__ == "__main__":
    main()