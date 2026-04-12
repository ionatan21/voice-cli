#!/usr/bin/env python3
"""
Voice CLI PRO - Versión avanzada con hotkeys y funcionalidades extra
Dependencias adicionales: pip install pynput pyperclip
"""

import sys
import os
import time
import threading
from pathlib import Path
import argparse

# Importar nuestros módulos
from recorder import AudioRecorder
from transcriber import AudioTranscriber

# Importar hotkeys si está disponible
try:
    from hotkeys import HotkeyManager
    HOTKEYS_AVAILABLE = True
except ImportError:
    HOTKEYS_AVAILABLE = False
    print("⚠️  Para hotkeys instala: pip install pynput")

# Importar pyperclip si está disponible
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("⚠️  Para portapapeles instala: pip install pyperclip")

class VoiceCLIPro:
    def __init__(self, model_name="base", sample_rate=44100, enable_hotkeys=True):
        """Inicializa Voice CLI PRO"""
        print("🚀 Bienvenido a Voice CLI PRO")
        print("=" * 60)

        try:
            # Inicializar componentes básicos
            self.recorder = AudioRecorder(sample_rate=sample_rate)
            self.transcriber = AudioTranscriber(model_name=model_name)
            self.running = True
            self.current_recording_file = None

            # Inicializar hotkeys si está disponible
            self.hotkey_manager = None
            if HOTKEYS_AVAILABLE and enable_hotkeys:
                self.hotkey_manager = HotkeyManager(self)
                print("⌨️  Hotkeys disponibles")

            # Configuración adicional PRO
            self.auto_save_enabled = True
            self.auto_copy_enabled = True
            self.quick_mode = False  # Modo rápido sin confirmaciones

            print(f"✅ Sistema PRO inicializado correctamente")
            print(f"🎯 Modelo Whisper: {model_name}")
            print(f"🎵 Sample rate: {sample_rate}Hz")
            print(f"📋 Portapapeles: {'✅' if CLIPBOARD_AVAILABLE else '❌'}")

            # Mostrar características PRO activadas
            print("\n🌟 CARACTERÍSTICAS PRO ACTIVAS:")
            print("  📚 Historial permanente")
            print("  📋 Copia automática al portapapeles")
            if HOTKEYS_AVAILABLE and enable_hotkeys:
                print("  ⌨️  Hotkeys globales")
            print("  🚀 Modo rápido disponible")
            print("  📊 Estadísticas avanzadas")

        except Exception as e:
            print(f"❌ Error al inicializar: {e}")
            sys.exit(1)

    def start_pro_mode(self):
        """Inicia características PRO"""
        if self.hotkey_manager and HOTKEYS_AVAILABLE:
            self.hotkey_manager.start_hotkey_listener()

    def stop_pro_mode(self):
        """Detiene características PRO"""
        if self.hotkey_manager:
            self.hotkey_manager.stop_hotkey_listener()

    def show_help_pro(self):
        """Muestra ayuda extendida con comandos PRO"""
        help_text = """
🎤 VOICE CLI PRO - COMANDOS DISPONIBLES:

📹 GRABACIÓN:
  start                    - Inicia grabación de audio
  stop                     - Detiene grabación y transcribe automáticamente
  quick-record             - Grabación rápida sin confirmaciones
  status                   - Muestra estado actual detallado

🔧 CONFIGURACIÓN AVANZADA:
  devices                  - Lista dispositivos de audio disponibles
  device <id>              - Selecciona dispositivo de entrada
  models                   - Lista modelos de Whisper disponibles
  model <name>             - Cambia modelo de Whisper
  sample-rate <hz>         - Cambia frecuencia de muestreo

⌨️  HOTKEYS (si están disponibles):
  hotkeys start            - Activa hotkeys globales
  hotkeys stop             - Desactiva hotkeys globales
  hotkeys status           - Estado de hotkeys
  ESPACIO                  - Iniciar/Detener grabación
  F1                       - Transcribir último archivo
  F2                       - Mostrar estado
  F12                      - Toggle hotkeys
  ESC                      - Salir

📚 HISTORIAL AVANZADO:
  history                  - Muestra últimas 10 transcripciones
  history <n>              - Muestra últimas n transcripciones
  history search <texto>   - Busca en el historial
  stats                    - Estadísticas de uso
  export <archivo>         - Exporta historial
  clear-history            - Limpia el historial

🛠️  UTILIDADES PRO:
  transcribe <archivo>     - Transcribe un archivo específico
  batch <directorio>       - Transcribe todos los archivos de un directorio
  timestamps <archivo>     - Transcribe con timestamps detallados
  lang <idioma>            - Establece idioma para transcripción
  auto-copy on/off         - Activa/desactiva copia automática
  quick-mode on/off        - Activa/desactiva modo rápido

📊 ANÁLISIS:
  analyze <archivo>        - Análisis detallado de audio
  compare <archivo1> <archivo2> - Compara transcripciones
  quality                  - Verifica calidad del micrófono

ℹ️  INFORMACIÓN:
  help                     - Muestra esta ayuda
  version                  - Información de versión
  about                    - Acerca de Voice CLI PRO
  quit/exit                - Salir del programa

💡 EJEMPLOS PRO:
  quick-record             # Grabación rápida
  batch ./audios          # Transcribir directorio completo
  history search "reunión" # Buscar en historial
  analyze grabacion.wav   # Análisis de calidad
  auto-copy off           # Desactivar copia automática
        """
        print(help_text)

    def cmd_quick_record(self, args):
        """Grabación rápida sin interrupciones"""
        print("🚀 MODO RÁPIDO: Grabación iniciará en 3 segundos...")
        time.sleep(1)
        print("   3...")
        time.sleep(1)
        print("   2...")
        time.sleep(1)
        print("   1...")
        time.sleep(1)

        # Iniciar grabación
        self.cmd_start([])

        if self.recorder.is_recording():
            print("🎤 [RÁPIDO] Grabando... (presiona ESPACIO o escribe 'stop')")

    def cmd_batch(self, args):
        """Transcribe todos los archivos de un directorio"""
        if not args:
            print("❌ Uso: batch <directorio>")
            return

        directory = Path(args[0])
        if not directory.exists() or not directory.is_dir():
            print(f"❌ Directorio no válido: {directory}")
            return

        # Buscar archivos de audio
        audio_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.aac']
        audio_files = []

        for ext in audio_extensions:
            audio_files.extend(directory.glob(f"*{ext}"))

        if not audio_files:
            print(f"❌ No se encontraron archivos de audio en: {directory}")
            return

        print(f"🔄 Transcribiendo {len(audio_files)} archivos...")
        results = []

        for i, file_path in enumerate(audio_files, 1):
            print(f"\n📁 [{i}/{len(audio_files)}] Procesando: {file_path.name}")

            try:
                result = self.transcriber.transcribe_file(str(file_path))
                if result:
                    results.append({
                        'file': file_path.name,
                        'text': result['text'],
                        'language': result['language'],
                        'time': result['transcription_time']
                    })
                    print(f"   ✅ Completado en {result['transcription_time']:.2f}s")
                else:
                    print(f"   ❌ Error en transcripción")

            except Exception as e:
                print(f"   ❌ Error: {e}")

        # Guardar resumen de batch
        if results:
            summary_file = directory / "transcription_batch.txt"
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write("TRANSCRIPCIÓN POR LOTES\n")
                f.write("=" * 50 + "\n\n")

                for result in results:
                    f.write(f"Archivo: {result['file']}\n")
                    f.write(f"Idioma: {result['language']}\n")
                    f.write(f"Tiempo: {result['time']:.2f}s\n")
                    f.write(f"Texto: {result['text']}\n")
                    f.write("-" * 40 + "\n\n")

            print(f"\n📄 Resumen guardado en: {summary_file}")

        print(f"✅ Transcripción por lotes completada: {len(results)}/{len(audio_files)} exitosos")

    def cmd_history_search(self, args):
        """Busca en el historial de transcripciones"""
        if not args:
            print("❌ Uso: history search <término>")
            return

        search_term = " ".join(args).lower()
        history_file = Path("history.txt")

        if not history_file.exists():
            print("📚 No hay historial disponible")
            return

        try:
            with open(history_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Separar por bloques
            entries = content.split("=" * 60)
            matches = []

            for entry in entries:
                if search_term in entry.lower():
                    matches.append(entry.strip())

            if matches:
                print(f"🔍 Encontradas {len(matches)} coincidencias para '{search_term}':")
                for i, match in enumerate(matches, 1):
                    print(f"\n--- Resultado {i} ---")
                    print(match)
            else:
                print(f"🔍 No se encontraron coincidencias para '{search_term}'")

        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")

    def cmd_stats(self, args):
        """Muestra estadísticas de uso"""
        history_file = Path("history.txt")
        recordings_dir = Path("recordings")

        print("📊 ESTADÍSTICAS DE USO:")
        print("-" * 40)

        # Estadísticas de historial
        if history_file.exists():
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    content = f.read()

                entries = content.split("=" * 60)
                entries = [e for e in entries if e.strip()]

                total_chars = sum(len(entry) for entry in entries)
                print(f"📚 Transcripciones realizadas: {len(entries)}")
                print(f"📝 Caracteres totales: {total_chars:,}")

                # Idiomas detectados
                languages = []
                for entry in entries:
                    if "Idioma:" in entry:
                        lang_line = [line for line in entry.split('\n') if "Idioma:" in line]
                        if lang_line:
                            lang = lang_line[0].split("Idioma:")[1].strip()
                            languages.append(lang)

                if languages:
                    from collections import Counter
                    lang_counts = Counter(languages)
                    print("🌍 Idiomas detectados:")
                    for lang, count in lang_counts.most_common():
                        print(f"   {lang}: {count} veces")

            except Exception as e:
                print(f"❌ Error leyendo estadísticas: {e}")

        # Estadísticas de archivos
        if recordings_dir.exists():
            audio_files = list(recordings_dir.glob("*.wav"))
            total_size = sum(f.stat().st_size for f in audio_files)
            print(f"🎵 Archivos de audio: {len(audio_files)}")
            print(f"💾 Tamaño total: {total_size / (1024*1024):.2f} MB")

        # Configuración actual
        print("\n🔧 CONFIGURACIÓN ACTUAL:")
        print(f"🤖 Modelo: {self.transcriber.model_name}")
        print(f"🎵 Sample rate: {self.recorder.sample_rate}Hz")
        print(f"📋 Auto-copy: {'✅' if self.auto_copy_enabled else '❌'}")
        print(f"⚡ Quick mode: {'✅' if self.quick_mode else '❌'}")

    def cmd_hotkeys(self, args):
        """Maneja comandos de hotkeys"""
        if not HOTKEYS_AVAILABLE:
            print("❌ Hotkeys no están disponibles. Instala: pip install pynput")
            return

        if not args:
            print("❌ Uso: hotkeys <start|stop|status>")
            return

        action = args[0].lower()

        if action == "start":
            if not self.hotkey_manager.is_running():
                self.hotkey_manager.start_hotkey_listener()
            else:
                print("⚠️  Hotkeys ya están activos")

        elif action == "stop":
            self.hotkey_manager.stop_hotkey_listener()

        elif action == "status":
            info = self.hotkey_manager.get_hotkeys_info()
            print("⌨️  ESTADO DE HOTKEYS:")
            print(f"   Activos: {'✅' if info['running'] else '❌'}")
            print(f"   Habilitados: {'✅' if info['enabled'] else '❌'}")
            print("   Configuración:")
            for action, key in info['hotkeys'].items():
                print(f"     {action}: {key}")

        else:
            print("❌ Acción no válida. Usa: start, stop, status")

    def cmd_auto_copy(self, args):
        """Configurar copia automática"""
        if not args:
            status = "activada" if self.auto_copy_enabled else "desactivada"
            print(f"📋 Copia automática está {status}")
            return

        setting = args[0].lower()
        if setting in ["on", "true", "1"]:
            self.auto_copy_enabled = True
            print("📋 Copia automática activada")
        elif setting in ["off", "false", "0"]:
            self.auto_copy_enabled = False
            print("📋 Copia automática desactivada")
        else:
            print("❌ Uso: auto-copy <on|off>")

    def copy_to_clipboard_pro(self, text):
        """Copia texto al portapapeles con manejo mejorado"""
        if not self.auto_copy_enabled:
            return False

        if not CLIPBOARD_AVAILABLE:
            print("💡 Para portapapeles automático instala: pip install pyperclip")
            return False

        try:
            pyperclip.copy(text)
            print("📋 Texto copiado al portapapeles")
            return True
        except Exception as e:
            print(f"⚠️  Error al copiar al portapapeles: {e}")
            return False

    # Sobrescribir métodos base con funcionalidad PRO
    def cmd_stop(self, args):
        """Comando mejorado para detener grabación"""
        if not self.recorder.is_recording():
            print("⚠️  No hay grabación activa")
            return

        # Detener grabación
        audio_file = self.recorder.stop_recording()

        if not audio_file:
            print("❌ Error: No se pudo guardar el audio")
            return

        # Transcribir automáticamente
        print("\n🔄 Iniciando transcripción...")
        try:
            result = self.transcriber.transcribe_file(audio_file)
            if result and result["text"]:
                print("\n" + "="*60)
                print(f"📝 TRANSCRIPCIÓN COMPLETA:")
                print(f"🌍 Idioma: {result['language']}")
                print(f"⏱️  Tiempo: {result['transcription_time']:.2f}s")
                print(f"📄 Texto:")
                print(f"   {result['text']}")
                print("="*60)

                # Copia automática mejorada
                success = self.copy_to_clipboard_pro(result["text"])
                if success:
                    print("✅ Transcripción lista y copiada al portapapeles")

            else:
                print("❌ No se pudo transcribir el audio")

        except Exception as e:
            print(f"❌ Error durante la transcripción: {e}")

    def cmd_quit(self, args):
        """Salida mejorada del programa"""
        if self.recorder.is_recording():
            print("⚠️  Hay una grabación activa. Deteniéndola...")
            self.recorder.stop_recording()

        # Detener características PRO
        self.stop_pro_mode()

        print("🚀 ¡Gracias por usar Voice CLI PRO!")
        self.running = False

    def parse_command_pro(self, user_input):
        """Parser de comandos extendido"""
        if not user_input.strip():
            return

        parts = user_input.strip().split()
        command = parts[0].lower()
        args = parts[1:]

        # Comandos básicos (heredados del VoiceCLI original)
        basic_commands = {
            'start': self.cmd_start,
            'stop': self.cmd_stop,
            'status': self.cmd_status,
            'devices': self.cmd_devices,
            'device': self.cmd_device,
            'models': self.cmd_models,
            'model': self.cmd_model,
            'history': self.cmd_history,
            'clear-history': self.cmd_clear_history,
            'transcribe': self.cmd_transcribe,
            'timestamps': self.cmd_timestamps,
            'help': lambda args: self.show_help_pro(),
            'quit': self.cmd_quit,
            'exit': self.cmd_quit,
        }

        # Comandos PRO adicionales
        pro_commands = {
            'quick-record': self.cmd_quick_record,
            'batch': self.cmd_batch,
            'stats': self.cmd_stats,
            'hotkeys': self.cmd_hotkeys,
            'auto-copy': self.cmd_auto_copy,
        }

        # Comandos especiales con subcomandos
        if len(parts) >= 2:
            if parts[0] == "history" and parts[1] == "search":
                self.cmd_history_search(parts[2:])
                return

        # Combinar todos los comandos
        all_commands = {**basic_commands, **pro_commands}

        if command in all_commands:
            try:
                all_commands[command](args)
            except Exception as e:
                print(f"❌ Error ejecutando comando '{command}': {e}")
        else:
            print(f"❌ Comando desconocido: '{command}'")
            print("💡 Escribe 'help' para ver los comandos disponibles")

    # Métodos heredados que necesario referenciar
    def cmd_start(self, args):
        """Iniciar grabación"""
        if self.recorder.is_recording():
            print("⚠️  Ya hay una grabación en curso. Usa 'stop' para detenerla.")
            return

        success = self.recorder.start_recording()
        if success:
            print("🟢 Grabación iniciada. Usa 'stop' para finalizar.")
        else:
            print("❌ No se pudo iniciar la grabación")

    def cmd_status(self, args):
        """Estado mejorado del sistema"""
        print("📊 ESTADO DEL SISTEMA:")
        print("-" * 30)

        # Estado de grabación
        if self.recorder.is_recording():
            print("🔴 Grabando audio...")
        else:
            print("⚫ Sin grabación activa")

        # Información del modelo
        print(f"🤖 Modelo Whisper: {self.transcriber.model_name}")
        print(f"🎵 Sample rate: {self.recorder.sample_rate}Hz")

        # Estado PRO
        print(f"📋 Auto-copy: {'✅' if self.auto_copy_enabled else '❌'}")
        print(f"⚡ Quick mode: {'✅' if self.quick_mode else '❌'}")

        if HOTKEYS_AVAILABLE and self.hotkey_manager:
            hotkey_status = "✅" if self.hotkey_manager.is_running() else "❌"
            print(f"⌨️  Hotkeys: {hotkey_status}")

        # Estadísticas de archivos
        recordings_dir = Path("recordings")
        if recordings_dir.exists():
            audio_files = list(recordings_dir.glob("*.wav"))
            print(f"📁 Archivos de audio: {len(audio_files)}")

        # Historial
        if Path("history.txt").exists():
            print("📚 Historial: Disponible")
        else:
            print("📚 Historial: Vacío")

    # Resto de métodos básicos (simplificados para brevedad)
    def cmd_devices(self, args): self.recorder.list_devices()
    def cmd_device(self, args):
        if not args:
            print("❌ Uso: device <id>")
            return
        try:
            device_id = int(args[0])
            self.recorder.set_device(device_id)
        except ValueError:
            print("❌ ID de dispositivo debe ser un número")
        except Exception as e:
            print(f"❌ Error: {e}")

    def cmd_models(self, args): self.transcriber.get_available_models()
    def cmd_model(self, args):
        if not args:
            print("❌ Uso: model <nombre>")
            return
        model_name = args[0].lower()
        valid_models = ["tiny", "base", "small", "medium", "large"]
        if model_name not in valid_models:
            print(f"❌ Modelo '{model_name}' no válido")
            return
        try:
            self.transcriber.change_model(model_name)
        except Exception as e:
            print(f"❌ Error: {e}")

    def cmd_history(self, args):
        limit = 10
        if args:
            try:
                limit = int(args[0])
            except:
                print("❌ El límite debe ser un número")
                return
        self.transcriber.get_history(limit)

    def cmd_clear_history(self, args):
        print("⚠️  ¿Estás seguro? (y/n): ", end="")
        if input().lower().strip() in ['y', 'yes', 'sí', 's']:
            self.transcriber.clear_history()
        else:
            print("❌ Operación cancelada")

    def cmd_transcribe(self, args):
        if not args:
            print("❌ Uso: transcribe <archivo>")
            return
        file_path = args[0]
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return
        try:
            result = self.transcriber.transcribe_file(file_path)
            if result:
                self.copy_to_clipboard_pro(result["text"])
        except Exception as e:
            print(f"❌ Error: {e}")

    def cmd_timestamps(self, args):
        if not args:
            print("❌ Uso: timestamps <archivo>")
            return
        file_path = args[0]
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return
        try:
            self.transcriber.transcribe_with_timestamps(file_path)
        except Exception as e:
            print(f"❌ Error: {e}")

    def run_interactive_pro(self):
        """Ejecuta el modo interactivo PRO"""
        # Iniciar características PRO
        self.start_pro_mode()

        print("\n💡 Escribe 'help' para ver todos los comandos PRO disponibles")
        print("🎯 Escribe 'start' para comenzar a grabar")

        if HOTKEYS_AVAILABLE:
            print("⌨️  Hotkeys globales disponibles (usa ESPACIO para grabar)")

        while self.running:
            try:
                # Mostrar prompt mejorado
                status_indicator = "🔴" if self.recorder.is_recording() else "⚫"
                hotkey_indicator = "⌨️" if (self.hotkey_manager and self.hotkey_manager.is_running()) else ""
                prompt = f"{status_indicator}{hotkey_indicator} voice-cli-pro> "

                user_input = input(prompt)
                self.parse_command_pro(user_input)

            except KeyboardInterrupt:
                print("\n\n⚠️  Ctrl+C detectado")
                if self.recorder.is_recording():
                    print("Deteniendo grabación...")
                    self.recorder.stop_recording()
                self.cmd_quit([])
            except EOFError:
                print("\n👋 ¡Hasta luego!")
                break

def main():
    """Función principal PRO"""
    parser = argparse.ArgumentParser(
        description="Voice CLI PRO - Versión avanzada con hotkeys y funcionalidades extra",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--model", "-m",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Modelo de Whisper a usar (default: base)"
    )

    parser.add_argument(
        "--sample-rate", "-sr",
        type=int,
        default=44100,
        help="Frecuencia de muestreo en Hz (default: 44100)"
    )

    parser.add_argument(
        "--no-hotkeys",
        action="store_true",
        help="Deshabilitar hotkeys globales"
    )

    parser.add_argument(
        "--file", "-f",
        help="Transcribir un archivo específico y salir"
    )

    parser.add_argument(
        "--batch", "-b",
        help="Transcribir todos los archivos de un directorio"
    )

    args = parser.parse_args()

    # Crear instancia de Voice CLI PRO
    enable_hotkeys = not args.no_hotkeys
    cli = VoiceCLIPro(
        model_name=args.model,
        sample_rate=args.sample_rate,
        enable_hotkeys=enable_hotkeys
    )

    # Modes especiales
    if args.file:
        # Modo archivo único
        if not os.path.exists(args.file):
            print(f"❌ Archivo no encontrado: {args.file}")
            sys.exit(1)

        try:
            result = cli.transcriber.transcribe_file(args.file)
            if result:
                print(result["text"])
                cli.copy_to_clipboard_pro(result["text"])
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    elif args.batch:
        # Modo batch
        cli.cmd_batch([args.batch])

    else:
        # Modo interactivo PRO
        cli.run_interactive_pro()

if __name__ == "__main__":
    main()