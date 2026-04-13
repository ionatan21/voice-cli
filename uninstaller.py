#!/usr/bin/env python3
"""
Desinstalador de Voice CLI
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
        bin_dir = home / "bin"
    else:
        bin_dir = home / ".local" / "bin"

    return bin_dir

def remove_files(bin_dir):
    """Elimina archivos de Voice CLI del directorio bin"""
    files_to_remove = [
        'voice',
        'voice.bat',
        'recorder.py',
        'transcriber.py',
        'main.py',
        'main_pro.py',
        'hotkeys.py',
    ]

    print("Eliminando archivos de Voice CLI...")

    removed_count = 0
    for filename in files_to_remove:
        file_path = bin_dir / filename
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"  {filename} ✓")
                removed_count += 1
            except Exception as e:
                print(f"  {filename} ❌ (Error: {e})")
        else:
            print(f"  {filename} - (no encontrado)")

    return removed_count

def remove_from_path_windows(bin_dir):
    """Elimina directorio del PATH en Windows"""
    try:
        # Obtener PATH actual del usuario
        result = subprocess.run([
            'powershell', '-Command',
            f'[Environment]::GetEnvironmentVariable("PATH", "User")'
        ], capture_output=True, text=True, check=True)

        current_path = result.stdout.strip()
        bin_dir_str = str(bin_dir)

        # Verificar si está en PATH
        if bin_dir_str not in current_path:
            print("El directorio no estaba en PATH")
            return True

        # Eliminar del PATH
        path_parts = current_path.split(';')
        new_path_parts = [part for part in path_parts if part != bin_dir_str]
        new_path = ';'.join(new_path_parts)

        subprocess.run([
            'powershell', '-Command',
            f'[Environment]::SetEnvironmentVariable("PATH", "{new_path}", "User")'
        ], check=True)

        print(f"Directorio eliminado del PATH: {bin_dir_str}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error eliminando del PATH: {e}")
        return False

def remove_from_path_unix(bin_dir):
    """Elimina directorio del PATH en sistemas Unix-like"""
    shell_rc_files = [
        Path.home() / ".bashrc",
        Path.home() / ".zshrc",
        Path.home() / ".profile",
    ]

    bin_dir_str = str(bin_dir)
    removed_from = []

    for rc_file in shell_rc_files:
        if rc_file.exists():
            try:
                with open(rc_file, 'r') as f:
                    lines = f.readlines()

                # Filtrar líneas que contengan la referencia a Voice CLI
                filtered_lines = []
                skip_next = False

                for line in lines:
                    if skip_next and line.strip() == '':
                        skip_next = False
                        continue

                    if '# Voice CLI' in line:
                        skip_next = True
                        continue
                    elif bin_dir_str in line and 'export PATH' in line:
                        continue

                    filtered_lines.append(line)
                    skip_next = False

                # Escribir archivo filtrado
                if len(filtered_lines) != len(lines):
                    with open(rc_file, 'w') as f:
                        f.writelines(filtered_lines)
                    removed_from.append(str(rc_file))

            except Exception as e:
                print(f"Error procesando {rc_file}: {e}")

    if removed_from:
        print(f"Referencias eliminadas de: {', '.join(removed_from)}")
    else:
        print("No se encontraron referencias en archivos de configuración")

def main():
    """Función principal del desinstalador"""
    print("🗑️  DESINSTALADOR DE VOICE CLI")
    print("=" * 40)

    # Confirmar desinstalación
    print("Esto eliminará Voice CLI del sistema.")
    response = input("¿Continuar con la desinstalación? (y/n): ").lower().strip()

    if response not in ['y', 'yes', 'sí', 's']:
        print("Desinstalación cancelada")
        return

    # Obtener directorio bin
    bin_dir = get_user_bin_dir()
    print(f"Directorio de instalación: {bin_dir}")

    # Verificar si existe instalación
    if not bin_dir.exists():
        print("No se encontró instalación de Voice CLI")
        return

    # Eliminar archivos
    removed_count = remove_files(bin_dir)

    # Eliminar del PATH
    print("\nEliminando del PATH del sistema...")
    if is_windows():
        remove_from_path_windows(bin_dir)
    else:
        remove_from_path_unix(bin_dir)

    # Resumen
    print(f"\n✓ Desinstalación completada")
    print(f"  Archivos eliminados: {removed_count}")

    # Eliminar directorio si está vacío
    try:
        if bin_dir.exists() and not any(bin_dir.iterdir()):
            bin_dir.rmdir()
            print(f"  Directorio eliminado: {bin_dir}")
    except:
        pass

    print("\n⚠️  IMPORTANTE: Reinicia tu terminal para que los cambios tomen efecto")

if __name__ == "__main__":
    main()