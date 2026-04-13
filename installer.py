#!/usr/bin/env python3
"""
Instalador de Voice CLI como comando global
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import platform

def is_windows():
    """Detecta si está ejecutándose en Windows"""
    return platform.system().lower() == 'windows'

def get_user_bin_dir():
    """Obtiene directorio bin del usuario"""
    home = Path.home()

    if is_windows():
        # En Windows usamos un directorio en el usuario
        bin_dir = home / "bin"
    else:
        # En Unix-like usamos .local/bin
        bin_dir = home / ".local" / "bin"

    return bin_dir

def create_bin_directory(bin_dir):
    """Crea el directorio bin si no existe"""
    if not bin_dir.exists():
        print(f"Creando directorio: {bin_dir}")
        bin_dir.mkdir(parents=True, exist_ok=True)
        print("Directorio creado exitosamente")
    else:
        print(f"Directorio ya existe: {bin_dir}")

def copy_voice_files(bin_dir):
    """Copia archivos necesarios al directorio bin"""
    current_dir = Path(__file__).parent.absolute()

    # Archivos a copiar
    files_to_copy = [
        'voice',           # Ejecutable principal
        'recorder.py',     # Módulo de grabación
        'transcriber.py',  # Módulo de transcripción
        'main.py',         # Interfaz original
        'main_pro.py',     # Interfaz PRO
    ]

    # Archivos opcionales
    optional_files = [
        'hotkeys.py',      # Hotkeys (puede no estar)
    ]

    print("Copiando archivos necesarios...")

    for filename in files_to_copy:
        src = current_dir / filename
        dst = bin_dir / filename

        if src.exists():
            shutil.copy2(src, dst)
            print(f"  {filename} ✓")

            # Hacer ejecutable en Unix-like
            if not is_windows() and filename == 'voice':
                os.chmod(dst, 0o755)
        else:
            print(f"  {filename} ❌ (archivo no encontrado)")
            return False

    # Copiar archivos opcionales
    for filename in optional_files:
        src = current_dir / filename
        dst = bin_dir / filename

        if src.exists():
            shutil.copy2(src, dst)
            print(f"  {filename} ✓ (opcional)")

    return True

def create_windows_wrapper(bin_dir):
    """Crea wrapper .bat para Windows"""
    if not is_windows():
        return

    bat_content = f'''@echo off
python "{bin_dir}\\voice" %*
'''

    bat_file = bin_dir / "voice.bat"
    with open(bat_file, 'w') as f:
        f.write(bat_content)

    print(f"Wrapper de Windows creado: {bat_file}")

def add_to_path_windows(bin_dir):
    """Agrega directorio al PATH en Windows"""
    try:
        # Obtener PATH actual del usuario
        result = subprocess.run([
            'powershell', '-Command',
            f'[Environment]::GetEnvironmentVariable("PATH", "User")'
        ], capture_output=True, text=True, check=True)

        current_path = result.stdout.strip()
        bin_dir_str = str(bin_dir)

        # Verificar si ya está en PATH
        if bin_dir_str in current_path:
            print(f"El directorio ya está en PATH: {bin_dir_str}")
            return True

        # Agregar al PATH
        new_path = f"{current_path};{bin_dir_str}" if current_path else bin_dir_str

        subprocess.run([
            'powershell', '-Command',
            f'[Environment]::SetEnvironmentVariable("PATH", "{new_path}", "User")'
        ], check=True)

        print(f"Directorio agregado al PATH: {bin_dir_str}")
        print("⚠️  IMPORTANTE: Reinicia tu terminal para que los cambios tomen efecto")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error agregando al PATH: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def add_to_path_unix(bin_dir):
    """Agrega directorio al PATH en sistemas Unix-like"""
    shell_rc_files = [
        Path.home() / ".bashrc",
        Path.home() / ".zshrc",
        Path.home() / ".profile",
    ]

    bin_dir_str = str(bin_dir)
    export_line = f'export PATH="$PATH:{bin_dir_str}"'

    # Buscar archivo de configuración de shell que exista
    rc_file = None
    for rc in shell_rc_files:
        if rc.exists():
            rc_file = rc
            break

    if not rc_file:
        # Crear .profile si no existe ninguno
        rc_file = Path.home() / ".profile"
        print(f"Creando archivo de configuración: {rc_file}")

    # Verificar si ya está configurado
    try:
        if rc_file.exists():
            with open(rc_file, 'r') as f:
                content = f.read()
            if bin_dir_str in content:
                print(f"El directorio ya está configurado en {rc_file}")
                return True
    except Exception:
        pass

    # Agregar al archivo de configuración
    try:
        with open(rc_file, 'a') as f:
            f.write(f'\n# Voice CLI\n{export_line}\n')

        print(f"Directorio agregado al PATH en: {rc_file}")
        print("⚠️  IMPORTANTE: Ejecuta 'source ~/.profile' o reinicia tu terminal")
        return True

    except Exception as e:
        print(f"Error agregando al PATH: {e}")
        return False

def verify_installation(bin_dir):
    """Verifica que la instalación sea correcta"""
    print("\nVerificando instalación...")

    # Verificar archivos
    voice_executable = bin_dir / "voice"
    if not voice_executable.exists():
        print("❌ Archivo ejecutable 'voice' no encontrado")
        return False

    required_modules = ['recorder.py', 'transcriber.py']
    for module in required_modules:
        if not (bin_dir / module).exists():
            print(f"❌ Módulo requerido no encontrado: {module}")
            return False

    print("✓ Todos los archivos están en su lugar")

    # Probar importación de Python
    try:
        sys.path.insert(0, str(bin_dir))
        import recorder
        import transcriber
        print("✓ Módulos de Python se pueden importar")
    except Exception as e:
        print(f"❌ Error importando módulos: {e}")
        return False

    print("✓ Instalación verificada correctamente")
    return True

def show_usage_examples():
    """Muestra ejemplos de uso"""
    print("\n" + "="*50)
    print("🎉 ¡INSTALACIÓN COMPLETADA!")
    print("="*50)
    print("\nEjemplos de uso del comando global 'voice':")
    print()
    print("# Modo interactivo (recomendado)")
    print("voice")
    print()
    print("# Transcribir un archivo")
    print("voice transcribe audio.wav")
    print()
    print("# Transcribir en inglés")
    print("voice transcribe audio.wav --language en")
    print()
    print("# Transcribir lote de archivos")
    print("voice batch ./mis_audios")
    print()
    print("# Grabar 10 segundos y transcribir automáticamente")
    print("voice record --duration 10 --transcribe")
    print()
    print("# Ver dispositivos de audio")
    print("voice devices")
    print()
    print("# Ver ayuda completa")
    print("voice help")
    print()
    print("⚠️  IMPORTANTE: Reinicia tu terminal antes de usar el comando 'voice'")
    print()

def install_dependencies():
    """Opcionalmente instala dependencias"""
    print("\n¿Quieres instalar las dependencias opcionales para funciones PRO?")
    print("- pynput (hotkeys globales)")
    print("- pyperclip (portapapeles automático)")

    response = input("¿Instalar dependencias PRO? (y/n): ").lower().strip()

    if response in ['y', 'yes', 'sí', 's']:
        try:
            print("Instalando dependencias PRO...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pynput", "pyperclip"], check=True)
            print("✓ Dependencias PRO instaladas")
        except subprocess.CalledProcessError:
            print("❌ Error instalando dependencias PRO")
            print("Puedes instalarlas manualmente con: pip install pynput pyperclip")

def main():
    """Función principal del instalador"""
    print("🚀 INSTALADOR DE VOICE CLI")
    print("=" * 40)

    # Detectar sistema
    system = "Windows" if is_windows() else "Unix"
    print(f"Sistema detectado: {system}")

    # Obtener directorio bin
    bin_dir = get_user_bin_dir()
    print(f"Directorio de instalación: {bin_dir}")

    # Crear directorio
    create_bin_directory(bin_dir)

    # Copiar archivos
    if not copy_voice_files(bin_dir):
        print("❌ Error copiando archivos. Instalación fallida.")
        return

    # Crear wrapper para Windows
    if is_windows():
        create_windows_wrapper(bin_dir)

    # Configurar PATH
    print("\nConfigurando PATH del sistema...")
    if is_windows():
        path_success = add_to_path_windows(bin_dir)
    else:
        path_success = add_to_path_unix(bin_dir)

    if not path_success:
        print("❌ Error configurando PATH")
        print(f"Agrega manualmente este directorio a tu PATH: {bin_dir}")

    # Verificar instalación
    if verify_installation(bin_dir):
        # Instalar dependencias opcionales
        install_dependencies()

        # Mostrar ejemplos de uso
        show_usage_examples()
    else:
        print("❌ La instalación no se completó correctamente")

if __name__ == "__main__":
    main()