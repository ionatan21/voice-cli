#!/usr/bin/env python3
"""
Voice CLI - Versión simplificada sin emojis y con modo silencioso
"""

import sys
import os
from pathlib import Path
import time

# Importar nuestros módulos
from recorder import AudioRecorder
from transcriber import AudioTranscriber

class VoiceCLIClean:
    def __init__(self, model_name="base", sample_rate=44100, quiet_mode=True):
        """Inicializa Voice CLI en modo limpio"""
        self.quiet_mode = quiet_mode
        self.running = True

        if not quiet_mode:
            print("Voice CLI - Inicializando sistema...")

        try:
            # Inicializar componentes
            self.recorder = AudioRecorder(sample_rate=sample_rate, quiet_mode=quiet_mode)
            self.transcriber = AudioTranscriber(model_name=model_name, default_language="es", quiet_mode=quiet_mode)

            if not quiet_mode:
                print(f"Sistema inicializado correctamente")
                print(f"Modelo Whisper: {model_name}")
                print(f"Idioma por defecto: Español (es)")
                print(f"Sample rate: {sample_rate}Hz")

        except Exception as e:
            print(f"Error al inicializar: {e}")
            sys.exit(1)

    def start_recording_clean(self):
        """Inicia grabación en modo limpio"""
        if self.recorder.is_recording():
            if not self.quiet_mode:
                print("Ya hay una grabación en proceso...")
            return False

        return self.recorder.start_recording()

    def stop_recording_clean(self):
        """Detiene grabación en modo limpio"""
        if not self.recorder.is_recording():
            if not self.quiet_mode:
                print("No hay grabación activa")
            return None

        return self.recorder.stop_recording()

    def transcribe_clean(self, audio_file):
        """Transcribe en modo limpio"""
        return self.transcriber.transcribe_file(audio_file)

    def copy_to_clipboard_clean(self, text):
        """Copia texto al portapapeles sin mensajes"""
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except ImportError:
            return False
        except Exception:
            return False

def create_clean_recorder(sample_rate=44100, quiet_mode=True):
    """Crea un grabador en modo limpio"""
    from pathlib import Path
    import threading
    import time
    import numpy as np
    import sounddevice as sd
    from scipy.io.wavfile import write

    class CleanRecorder:
        def __init__(self, sample_rate=44100, channels=1, quiet_mode=True):
            self.sample_rate = sample_rate
            self.channels = channels
            self.recording = False
            self.audio_data = []
            self.recording_thread = None
            self.quiet_mode = quiet_mode

            # Crear directorio de audios si no existe
            self.audio_dir = Path("recordings")
            self.audio_dir.mkdir(exist_ok=True)

        def start_recording(self):
            """Inicia la grabación de audio"""
            if self.recording:
                return False

            self.recording = True
            self.audio_data = []

            # Detectar sample rate adecuado del dispositivo
            try:
                current_device = sd.default.device[0] if sd.default.device[0] is not None else 0
                device_info = sd.query_devices(current_device)
                device_sample_rate = int(device_info['default_samplerate'])

                if device_sample_rate != self.sample_rate:
                    if not self.quiet_mode:
                        print(f"Ajustando sample rate: {self.sample_rate}Hz → {device_sample_rate}Hz")
                    self.sample_rate = device_sample_rate

            except Exception:
                pass

            # Iniciar grabación en un hilo separado
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()
            return True

        def _record_audio(self):
            """Función interna para grabar audio"""
            try:
                current_device = sd.default.device[0] if sd.default.device[0] is not None else 0
                device_info = sd.query_devices(current_device)
                suggested_sample_rate = int(device_info['default_samplerate'])
            except:
                suggested_sample_rate = 44100

            configs_to_try = [
                (suggested_sample_rate, np.float32),
                (48000, np.float32),
                (44100, np.float32),
            ]

            for sample_rate, audio_format in configs_to_try:
                try:
                    if sample_rate != self.sample_rate:
                        self.sample_rate = sample_rate

                    with sd.InputStream(
                        samplerate=sample_rate,
                        channels=self.channels,
                        callback=self._audio_callback,
                        blocksize=1024,
                        dtype=audio_format
                    ):
                        while self.recording:
                            time.sleep(0.1)
                        return
                except Exception:
                    continue

            if not self.quiet_mode:
                print("Error: No se pudo encontrar una configuración de audio compatible")
            self.recording = False

        def _audio_callback(self, indata, frames, time, status):
            """Callback para procesar datos de audio"""
            if self.recording:
                if indata.dtype != np.float32:
                    if indata.dtype == np.int16:
                        audio_data = indata.astype(np.float32) / 32768.0
                    else:
                        audio_data = indata.astype(np.float32)
                else:
                    audio_data = indata

                self.audio_data.append(audio_data.copy())

        def stop_recording(self):
            """Detiene la grabación y guarda el archivo"""
            if not self.recording:
                return None

            self.recording = False

            if self.recording_thread:
                self.recording_thread.join()

            if not self.audio_data:
                return None

            audio_array = np.concatenate(self.audio_data, axis=0)
            timestamp = int(time.time())
            filename = f"recording_{timestamp}.wav"
            filepath = self.audio_dir / filename

            audio_array = np.clip(audio_array, -1.0, 1.0)
            audio_normalized = (audio_array * 32767).astype(np.int16)

            try:
                write(str(filepath), self.sample_rate, audio_normalized)
                return str(filepath)
            except Exception:
                return None

        def is_recording(self):
            """Verifica si está grabando actualmente"""
            return self.recording

    return CleanRecorder(sample_rate=sample_rate, quiet_mode=quiet_mode)

def create_clean_transcriber(model_name="base", quiet_mode=True):
    """Crea un transcriptor en modo limpio"""
    import whisper
    import os
    from pathlib import Path
    import time

    class CleanTranscriber:
        def __init__(self, model_name="base", default_language="es", quiet_mode=True):
            self.model_name = model_name
            self.model = None
            self.default_language = default_language
            self.quiet_mode = quiet_mode

            if not quiet_mode:
                print(f"Inicializando Whisper modelo '{model_name}'...")
                print(f"Idioma por defecto: {default_language}")

            self._load_model()

        def _load_model(self):
            """Carga el modelo de Whisper"""
            try:
                self.model = whisper.load_model(self.model_name)
                if not self.quiet_mode:
                    print(f"Modelo '{self.model_name}' cargado correctamente")
            except Exception as e:
                print(f"Error al cargar modelo Whisper: {e}")
                raise

        def transcribe_file(self, audio_file, language=None, verbose=None):
            """Transcribe un archivo de audio"""
            if not self.model:
                raise RuntimeError("Modelo no está cargado")

            if not os.path.exists(audio_file):
                raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_file}")

            if language is None:
                language = self.default_language

            if verbose is None:
                verbose = not self.quiet_mode

            start_time = time.time()

            try:
                # Mostrar información solo si es verbose
                if verbose:
                    file_size = os.path.getsize(audio_file)
                    print(f"Transcribiendo: {audio_file}")
                    print(f"Idioma configurado: {language}")
                    print(f"Tamaño archivo: {file_size / 1024:.1f} KB")

                result = self.model.transcribe(
                    audio_file,
                    language=language,
                    verbose=verbose
                )

                transcription_time = time.time() - start_time
                text = result["text"].strip()

                if not text and verbose:
                    print("Transcripción vacía - intentando sin especificar idioma...")
                    result_auto = self.model.transcribe(audio_file, verbose=verbose)
                    if result_auto["text"].strip():
                        text = result_auto["text"].strip()
                        result = result_auto

                if not text:
                    return None

                detected_language = result.get("language", "unknown")

                result_data = {
                    "text": text,
                    "language": detected_language,
                    "transcription_time": transcription_time,
                    "audio_file": audio_file,
                    "file_size": os.path.getsize(audio_file) if os.path.exists(audio_file) else 0
                }

                if verbose:
                    print(f"Transcripción completada en {transcription_time:.2f}s")
                    print(f"Idioma detectado: {detected_language}")
                    print(f"Texto: {text}")

                return result_data

            except Exception as e:
                if verbose:
                    print(f"Error durante la transcripción: {e}")
                return None

    return CleanTranscriber(model_name=model_name, quiet_mode=quiet_mode)