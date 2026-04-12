"""
Módulo para manejo de hotkeys y teclas de acceso rápido
Requiere: pip install pynput
"""

import threading
import time
from pynput import keyboard
from pynput.keyboard import Key, Listener

class HotkeyManager:
    def __init__(self, voice_cli_instance):
        """
        Inicializa el manager de hotkeys

        Args:
            voice_cli_instance: Instancia del VoiceCLI para controlar
        """
        self.voice_cli = voice_cli_instance
        self.listener = None
        self.running = False
        self.hotkeys_enabled = True

        # Configuración de teclas
        self.hotkeys = {
            'toggle_recording': Key.space,      # Espacio para iniciar/detener
            'quick_transcribe': Key.f1,         # F1 para transcribir último archivo
            'show_status': Key.f2,              # F2 para mostrar estado
            'toggle_hotkeys': Key.f12,          # F12 para activar/desactivar hotkeys
        }

        # Estado de teclas presionadas
        self.pressed_keys = set()

    def start_hotkey_listener(self):
        """Inicia el listener de teclas globales"""
        if self.running:
            print("⚠️  Hotkeys ya están activos")
            return

        self.running = True
        print("⌨️  Hotkeys activados:")
        print("   🎤 ESPACIO: Iniciar/Detener grabación")
        print("   📄 F1: Transcribir último audio")
        print("   📊 F2: Mostrar estado")
        print("   🔧 F12: Activar/Desactivar hotkeys")
        print("   ❌ ESC: Salir del programa")

        def on_press(key):
            if not self.hotkeys_enabled:
                return

            try:
                # Agregar tecla al conjunto de presionadas
                self.pressed_keys.add(key)

                # Manejar hotkeys
                if key == self.hotkeys['toggle_recording']:
                    self._handle_toggle_recording()
                elif key == self.hotkeys['quick_transcribe']:
                    self._handle_quick_transcribe()
                elif key == self.hotkeys['show_status']:
                    self._handle_show_status()
                elif key == self.hotkeys['toggle_hotkeys']:
                    self._handle_toggle_hotkeys()
                elif key == Key.esc:
                    self._handle_exit()

            except Exception as e:
                print(f"⚠️  Error en hotkey: {e}")

        def on_release(key):
            # Remover tecla del conjunto de presionadas
            self.pressed_keys.discard(key)

        # Crear y iniciar listener
        self.listener = Listener(
            on_press=on_press,
            on_release=on_release,
            suppress=False  # No suprimir las teclas para otras aplicaciones
        )

        # Ejecutar listener en hilo separado
        listener_thread = threading.Thread(target=self._run_listener, daemon=True)
        listener_thread.start()

    def _run_listener(self):
        """Ejecuta el listener de teclas"""
        try:
            self.listener.start()
            self.listener.join()
        except Exception as e:
            print(f"❌ Error en listener de hotkeys: {e}")

    def stop_hotkey_listener(self):
        """Detiene el listener de teclas"""
        self.running = False
        if self.listener:
            try:
                self.listener.stop()
                print("⌨️  Hotkeys desactivados")
            except:
                pass

    def _handle_toggle_recording(self):
        """Maneja alternar grabación con tecla"""
        if not self.running:
            return

        try:
            if self.voice_cli.recorder.is_recording():
                print("\n🛑 [HOTKEY] Deteniendo grabación...")
                self.voice_cli.cmd_stop([])
            else:
                print("\n🎤 [HOTKEY] Iniciando grabación...")
                self.voice_cli.cmd_start([])
        except Exception as e:
            print(f"❌ Error en toggle recording: {e}")

    def _handle_quick_transcribe(self):
        """Transcribe el último archivo de audio grabado"""
        try:
            from pathlib import Path
            recordings_dir = Path("recordings")

            if not recordings_dir.exists():
                print("\n❌ [HOTKEY] No hay directorio de grabaciones")
                return

            # Buscar el último archivo WAV
            audio_files = list(recordings_dir.glob("*.wav"))
            if not audio_files:
                print("\n❌ [HOTKEY] No hay archivos de audio")
                return

            # Ordenar por tiempo de modificación (más reciente primero)
            latest_file = max(audio_files, key=lambda f: f.stat().st_mtime)

            print(f"\n🔄 [HOTKEY] Transcribiendo último archivo: {latest_file.name}")
            result = self.voice_cli.transcriber.transcribe_file(str(latest_file))

            if result:
                print(f"📝 Texto: {result['text']}")
                self.voice_cli._copy_to_clipboard(result['text'])

        except Exception as e:
            print(f"❌ Error en quick transcribe: {e}")

    def _handle_show_status(self):
        """Muestra estado del sistema con hotkey"""
        try:
            print("\n📊 [HOTKEY] Estado del sistema:")
            self.voice_cli.cmd_status([])
        except Exception as e:
            print(f"❌ Error en show status: {e}")

    def _handle_toggle_hotkeys(self):
        """Activa/desactiva hotkeys"""
        self.hotkeys_enabled = not self.hotkeys_enabled
        status = "activados" if self.hotkeys_enabled else "desactivados"
        print(f"\n⌨️  [HOTKEY] Hotkeys {status}")

    def _handle_exit(self):
        """Sale del programa con hotkey"""
        print("\n❌ [HOTKEY] Saliendo del programa...")
        self.voice_cli.cmd_quit([])
        self.stop_hotkey_listener()

    def is_running(self):
        """Verifica si los hotkeys están activos"""
        return self.running

    def configure_hotkey(self, action, key):
        """
        Configura una nueva tecla para una acción

        Args:
            action (str): Acción a configurar
            key: Nueva tecla a asignar
        """
        if action in self.hotkeys:
            old_key = self.hotkeys[action]
            self.hotkeys[action] = key
            print(f"✅ Hotkey '{action}' cambiado de {old_key} a {key}")
        else:
            print(f"❌ Acción '{action}' no existe")

    def get_hotkeys_info(self):
        """Retorna información sobre los hotkeys configurados"""
        info = {
            "enabled": self.hotkeys_enabled,
            "running": self.running,
            "hotkeys": self.hotkeys
        }
        return info