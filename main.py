#!/usr/bin/env python3
"""
Voice CLI - Grabación y transcripción de audio con Whisper
Comandos disponibles:
- start: Inicia grabación
- stop: Detiene grabación y transcribe
- status: Estado actual
- devices: Lista dispositivos de audio
- history: Muestra historial
- models: Lista modelos disponibles
- help: Muestra ayuda
- quit/exit: Salir del programa
"""

import sys
import os
from pathlib import Path
import argparse

# Importar nuestros módulos
from recorder import AudioRecorder
from transcriber import AudioTranscriber

class VoiceCLI:
    def __init__(self, model_name="base", sample_rate=44100):
        """Inicializa la interfaz de línea de comandos"""
        print("🎉 Bienvenido a Voice CLI")
        print("=" * 50)

        try:
            # Inicializar componentes
            self.recorder = AudioRecorder(sample_rate=sample_rate)
            self.transcriber = AudioTranscriber(model_name=model_name, default_language="es")  # Español por defecto
            self.running = True
            self.current_recording_file = None

            print(f"✅ Sistema inicializado correctamente")
            print(f"🎯 Modelo Whisper: {model_name}")
            print(f"🌍 Idioma por defecto: Español (es)")
            print(f"🎵 Sample rate: {sample_rate}Hz")

        except Exception as e:
            print(f"❌ Error al inicializar: {e}")
            sys.exit(1)

    def show_help(self):
        """Muestra ayuda de comandos"""
        help_text = """
🎤 VOICE CLI - COMANDOS DISPONIBLES:

📹 GRABACIÓN:
  start          - Inicia grabación de audio
  stop           - Detiene grabación y transcribe automáticamente
  status         - Muestra estado actual de grabación

🔧 CONFIGURACIÓN:
  devices        - Lista dispositivos de audio disponibles
  device <id>    - Selecciona dispositivo de entrada
  test [<id>]    - Prueba dispositivo de audio actual o específico
  sample-rate <hz> - Configura frecuencia de muestreo (ej: 48000)
  models         - Lista modelos de Whisper disponibles
  model <name>   - Cambia modelo de Whisper (tiny/base/small/medium/large)
  language <código> - Configura idioma (es/en/fr/de/etc.)
  languages      - Lista idiomas disponibles

📚 HISTORIAL:
  history        - Muestra últimas 10 transcripciones
  history <n>    - Muestra últimas n transcripciones
  clear-history  - Limpia el historial

🛠️  UTILIDADES:
  transcribe <archivo> - Transcribe un archivo de audio específico
  timestamps <archivo> - Transcribe con timestamps detallados
  lang <idioma>        - Establece idioma para transcripción (es, en, fr, etc.)

ℹ️  INFORMACIÓN:
  help           - Muestra esta ayuda
  quit/exit      - Salir del programa

💡 EJEMPLOS:
  start                    # Inicia grabación
  stop                     # Detiene y transcribe
  model small             # Cambia a modelo 'small'
  transcribe audio.wav    # Transcribe archivo específico
  history 5               # Muestra últimas 5 transcripciones
        """
        print(help_text)

    def cmd_start(self, args):
        """Comando para iniciar grabación"""
        if self.recorder.is_recording():
            print("⚠️  Ya hay una grabación en curso. Usa 'stop' para detenerla.")
            return

        success = self.recorder.start_recording()
        if success:
            print("🟢 Grabación iniciada. Usa 'stop' para finalizar.")
        else:
            print("❌ No se pudo iniciar la grabación")

    def cmd_stop(self, args):
        """Comando para detener grabación y transcribir"""
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

                # Intentar copiar al portapapeles si está disponible
                self._copy_to_clipboard(result["text"])

            else:
                print("❌ No se pudo transcribir el audio")

        except Exception as e:
            print(f"❌ Error durante la transcripción: {e}")

        # Limpiar archivo temporal (opcional)
        # self._cleanup_audio_file(audio_file)

    def cmd_status(self, args):
        """Muestra estado actual del sistema"""
        print("📊 ESTADO DEL SISTEMA:")
        print("-" * 30)

        # Estado de grabación
        if self.recorder.is_recording():
            print("🔴 Grabando audio...")
        else:
            print("⚫ Sin grabación activa")

        # Información del modelo y configuración
        print(f"🤖 Modelo Whisper: {self.transcriber.model_name}")
        print(f"🌍 Idioma configurado: {self.transcriber.default_language}")
        print(f"🎵 Sample rate: {self.recorder.sample_rate}Hz")

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

    def cmd_devices(self, args):
        """Lista dispositivos de audio"""
        self.recorder.list_devices()

    def cmd_test_device(self, args):
        """Prueba el dispositivo de audio actual"""
        device_id = None
        if args:
            try:
                device_id = int(args[0])
            except ValueError:
                print("❌ ID de dispositivo debe ser un número")
                return

        print("🔧 Probando dispositivo de audio...")
        self.recorder.test_device(device_id)

    def cmd_device(self, args):
        """Selecciona dispositivo de audio"""
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

    def cmd_models(self, args):
        """Lista modelos disponibles de Whisper"""
        self.transcriber.get_available_models()

    def cmd_model(self, args):
        """Cambia modelo de Whisper"""
        if not args:
            print("❌ Uso: model <nombre>")
            print("Modelos disponibles: tiny, base, small, medium, large")
            return

        model_name = args[0].lower()
        valid_models = ["tiny", "base", "small", "medium", "large"]

        if model_name not in valid_models:
            print(f"❌ Modelo '{model_name}' no válido")
            print(f"Modelos disponibles: {', '.join(valid_models)}")
            return

        try:
            self.transcriber.change_model(model_name)
            print(f"✅ Modelo cambiado a '{model_name}'")
        except Exception as e:
            print(f"❌ Error al cambiar modelo: {e}")

    def cmd_language(self, args):
        """Configura el idioma de transcripción"""
        if not args:
            print(f"🌍 Idioma actual: {self.transcriber.default_language}")
            print("💡 Uso: language <código> (ej: language es, language en)")
            print("📝 Usa 'languages' para ver idiomas disponibles")
            return

        language = args[0].lower()
        self.transcriber.set_language(language)

    def cmd_languages(self, args):
        """Lista idiomas disponibles"""
        self.transcriber.get_supported_languages()

    def cmd_sample_rate(self, args):
        """Configura el sample rate de grabación"""
        if not args:
            print(f"🎵 Sample rate actual: {self.recorder.sample_rate}Hz")
            print("💡 Uso: sample-rate <hz> (ej: sample-rate 48000)")
            print("📝 Rates comunes: 8000, 16000, 22050, 44100, 48000")
            return

        try:
            new_rate = int(args[0])
            if new_rate < 8000 or new_rate > 192000:
                print("❌ Sample rate debe estar entre 8000 y 192000 Hz")
                return

            old_rate = self.recorder.sample_rate
            self.recorder.sample_rate = new_rate
            print(f"🎵 Sample rate cambiado: {old_rate}Hz → {new_rate}Hz")
        except ValueError:
            print("❌ Sample rate debe ser un número")
        except Exception as e:
            print(f"❌ Error: {e}")

    def cmd_history(self, args):
        """Muestra historial de transcripciones"""
        limit = 10  # Valor por defecto
        if args:
            try:
                limit = int(args[0])
            except ValueError:
                print("❌ El límite debe ser un número")
                return

        self.transcriber.get_history(limit)

    def cmd_clear_history(self, args):
        """Limpia el historial"""
        print("⚠️  ¿Estás seguro de que quieres limpiar el historial? (y/n): ", end="")
        response = input().lower().strip()

        if response in ['y', 'yes', 'sí', 's']:
            self.transcriber.clear_history()
        else:
            print("❌ Operación cancelada")

    def cmd_transcribe(self, args):
        """Transcribe un archivo específico"""
        if not args:
            print("❌ Uso: transcribe <ruta_archivo>")
            return

        file_path = args[0]
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return

        try:
            result = self.transcriber.transcribe_file(file_path)
            if result:
                print(f"\n✅ Transcripción de '{file_path}' completada")
                self._copy_to_clipboard(result["text"])
        except Exception as e:
            print(f"❌ Error: {e}")

    def cmd_timestamps(self, args):
        """Transcribe con timestamps detallados"""
        if not args:
            print("❌ Uso: timestamps <ruta_archivo>")
            return

        file_path = args[0]
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return

        try:
            self.transcriber.transcribe_with_timestamps(file_path)
        except Exception as e:
            print(f"❌ Error: {e}")

    def cmd_quit(self, args):
        """Sale del programa"""
        if self.recorder.is_recording():
            print("⚠️  Hay una grabación activa. Deteniéndola...")
            self.recorder.stop_recording()

        print("👋 ¡Hasta luego!")
        self.running = False

    def _copy_to_clipboard(self, text):
        """Intenta copiar texto al portapapeles"""
        try:
            import pyperclip
            pyperclip.copy(text)
            print("📋 Texto copiado al portapapeles")
        except ImportError:
            print("💡 Para copiar automáticamente al portapapeles, instala: pip install pyperclip")
        except Exception as e:
            print(f"⚠️  No se pudo copiar al portapapeles: {e}")

    def parse_command(self, user_input):
        """Parsea y ejecute comandos del usuario"""
        if not user_input.strip():
            return

        parts = user_input.strip().split()
        command = parts[0].lower()
        args = parts[1:]

        # Mapeo de comandos
        commands = {
            'start': self.cmd_start,
            'stop': self.cmd_stop,
            'status': self.cmd_status,
            'devices': self.cmd_devices,
            'device': self.cmd_device,
            'test': self.cmd_test_device,
            'models': self.cmd_models,
            'model': self.cmd_model,
            'language': self.cmd_language,
            'languages': self.cmd_languages,
            'sample-rate': self.cmd_sample_rate,
            'history': self.cmd_history,
            'clear-history': self.cmd_clear_history,
            'transcribe': self.cmd_transcribe,
            'timestamps': self.cmd_timestamps,
            'help': lambda args: self.show_help(),
            'quit': self.cmd_quit,
            'exit': self.cmd_quit,
        }

        if command in commands:
            try:
                commands[command](args)
            except Exception as e:
                print(f"❌ Error ejecutando comando '{command}': {e}")
        else:
            print(f"❌ Comando desconocido: '{command}'")
            print("💡 Escribe 'help' para ver los comandos disponibles")

    def run_interactive(self):
        """Ejecuta el modo interactivo"""
        print("\n💡 Escribe 'help' para ver los comandos disponibles")
        print("🎯 Escribe 'start' para comenzar a grabar")

        while self.running:
            try:
                # Mostrar prompt
                status_indicator = "🔴" if self.recorder.is_recording() else "⚫"
                prompt = f"{status_indicator} voice-cli> "

                user_input = input(prompt)
                self.parse_command(user_input)

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
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Voice CLI - Grabación y transcripción de audio con Whisper",
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
        "--file", "-f",
        help="Transcribir un archivo específico y salir"
    )

    args = parser.parse_args()

    # Crear instancia de Voice CLI
    cli = VoiceCLI(model_name=args.model, sample_rate=args.sample_rate)

    # Si se especifica un archivo, transcribir y salir
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ Archivo no encontrado: {args.file}")
            sys.exit(1)

        try:
            result = cli.transcriber.transcribe_file(args.file)
            if result:
                print(result["text"])
                cli._copy_to_clipboard(result["text"])
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        # Modo interactivo
        cli.run_interactive()

if __name__ == "__main__":
    main()