"""
Módulo para grabación de audio
"""
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import threading
import time
from pathlib import Path

class AudioRecorder:
    def __init__(self, sample_rate=44100, channels=1):
        """
        Inicializa el grabador de audio

        Args:
            sample_rate (int): Frecuencia de muestreo en Hz
            channels (int): Número de canales (1=mono, 2=estéreo)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data = []
        self.recording_thread = None

        # Crear directorio de audios si no existe
        self.audio_dir = Path("recordings")
        self.audio_dir.mkdir(exist_ok=True)

    def start_recording(self):
        """Inicia la grabación de audio"""
        if self.recording:
            print("Ya hay una grabación en proceso...")
            return False

        self.recording = True
        self.audio_data = []

        # Detectar sample rate adecuado del dispositivo
        try:
            current_device = sd.default.device[0] if sd.default.device[0] is not None else 0
            device_info = sd.query_devices(current_device)

            # Usar el sample rate por defecto del dispositivo
            device_sample_rate = int(device_info['default_samplerate'])

            # Si es diferente al configurado, ajustar
            if device_sample_rate != self.sample_rate:
                print(f"🔧 Ajustando sample rate: {self.sample_rate}Hz → {device_sample_rate}Hz")
                self.sample_rate = device_sample_rate

            print(f"🎤 Grabando audio... (Sample rate: {self.sample_rate}Hz)")
            print(f"🎧 Usando dispositivo: {device_info['name']}")
            print("💡 Usa 'stop' para detener la grabación")

        except Exception as e:
            print(f"⚠️  Advertencia dispositivo: {e}")
            print(f"🎤 Grabando audio... (Sample rate: {self.sample_rate}Hz)")
            print("💡 Usa 'stop' para detener la grabación")

        # Iniciar grabación en un hilo separado
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()
        return True

    def _record_audio(self):
        """Función interna para grabar audio en hilo separado"""
        # Obtener información del dispositivo actual
        try:
            current_device = sd.default.device[0] if sd.default.device[0] is not None else 0
            device_info = sd.query_devices(current_device)
            suggested_sample_rate = int(device_info['default_samplerate'])
        except:
            suggested_sample_rate = 44100

        # Lista de configuraciones a probar (sample_rate, formato)
        configs_to_try = [
            # Primero probar con sample rate del dispositivo
            (suggested_sample_rate, np.float32),
            (suggested_sample_rate, np.int16),
            (suggested_sample_rate, 'float64'),
            (suggested_sample_rate, 'int16'),

            # Luego probar sample rates comunes
            (48000, np.float32),
            (44100, np.float32),
            (22050, np.float32),
            (16000, np.float32),
            (8000, np.float32),

            (48000, np.int16),
            (44100, np.int16),
            (22050, np.int16),
            (16000, np.int16),
        ]

        for sample_rate, audio_format in configs_to_try:
            try:
                print(f"🔧 Probando: {sample_rate}Hz, {audio_format}")

                # Actualizar sample rate si es diferente
                if sample_rate != self.sample_rate:
                    self.sample_rate = sample_rate

                # Configurar stream de audio
                with sd.InputStream(
                    samplerate=sample_rate,
                    channels=self.channels,
                    callback=self._audio_callback,
                    blocksize=1024,
                    dtype=audio_format
                ):
                    print(f"✅ Configuración exitosa: {sample_rate}Hz, {audio_format}")
                    while self.recording:
                        time.sleep(0.1)
                    return  # Éxito, salir de la función

            except Exception as e:
                print(f"❌ Falló {sample_rate}Hz, {audio_format}: {e}")
                continue

        # Si llegamos aquí, ninguna configuración funcionó
        print(f"❌ Error: No se pudo encontrar una configuración de audio compatible")
        print(f"💡 Soluciones sugeridas:")
        print(f"   1. Cambiar dispositivo con 'devices' y 'device <id>'")
        print(f"   2. Verificar permisos de micrófono")
        print(f"   3. Reiniciar Python y probar de nuevo")
        self.recording = False

    def _audio_callback(self, indata, frames, time, status):
        """Callback para procesar datos de audio"""
        if status:
            print(f"⚠️  Audio callback status: {status}")

        if self.recording:
            # Convertir datos a float32 si no lo están ya
            if indata.dtype != np.float32:
                if indata.dtype == np.int16:
                    # Convertir int16 a float32
                    audio_data = indata.astype(np.float32) / 32768.0
                else:
                    # Para otros tipos, convertir directamente
                    audio_data = indata.astype(np.float32)
            else:
                audio_data = indata

            self.audio_data.append(audio_data.copy())

    def stop_recording(self):
        """Detiene la grabación y guarda el archivo"""
        if not self.recording:
            print("No hay grabación activa")
            return None

        print("⏹️  Deteniendo grabación...")
        self.recording = False

        # Esperar a que termine el hilo de grabación
        if self.recording_thread:
            self.recording_thread.join()

        if not self.audio_data:
            print("❌ No se grabó audio")
            return None

        # Convertir datos a array numpy
        audio_array = np.concatenate(self.audio_data, axis=0)

        # Generar nombre de archivo único
        timestamp = int(time.time())
        filename = f"recording_{timestamp}.wav"
        filepath = self.audio_dir / filename

        # Convertir de float32 a int16 para WAV
        # Asegurar que el audio esté en el rango correcto
        audio_array = np.clip(audio_array, -1.0, 1.0)
        audio_normalized = (audio_array * 32767).astype(np.int16)

        # Guardar archivo WAV
        try:
            write(str(filepath), self.sample_rate, audio_normalized)
            duration = len(audio_array) / self.sample_rate
            print(f"✅ Audio guardado: {filepath}")
            print(f"⏱️  Duración: {duration:.2f} segundos")

            # Verificar calidad del archivo
            self._verify_audio_quality(str(filepath), audio_normalized, duration)

            return str(filepath)
        except Exception as e:
            print(f"❌ Error al guardar audio: {e}")
            return None

    def _verify_audio_quality(self, filepath, audio_data, duration):
        """Verifica la calidad del archivo de audio grabado"""
        try:
            # Verificar duración mínima
            if duration < 0.5:
                print("⚠️  Advertencia: Grabación muy corta (< 0.5s)")

            # Verificar nivel de audio
            max_level = np.max(np.abs(audio_data))
            rms_level = np.sqrt(np.mean(audio_data.astype(np.float64) ** 2))

            print(f"🔊 Nivel máximo: {max_level/32767.0:.3f}")
            print(f"📊 Nivel RMS: {rms_level/32767.0:.3f}")

            # Advertencias sobre niveles de audio
            if max_level < 1000:  # Muy bajo
                print("⚠️  Advertencia: Nivel de audio muy bajo")
                print("   - Acércate más al micrófono")
                print("   - Aumenta el volumen del micrófono")

            elif max_level > 30000:  # Muy alto, posible distorsión
                print("⚠️  Advertencia: Nivel de audio muy alto (posible distorsión)")
                print("   - Aléjate del micrófono")
                print("   - Reduce el volumen del micrófono")

            else:
                print("✅ Nivel de audio óptimo")

            # Verificar si hay silencio
            silence_threshold = 100
            silence_samples = np.sum(np.abs(audio_data) < silence_threshold)
            silence_percentage = (silence_samples / len(audio_data)) * 100

            if silence_percentage > 80:
                print(f"⚠️  Advertencia: {silence_percentage:.1f}% silencio detectado")
            else:
                print(f"🎤 Contenido de voz: {100-silence_percentage:.1f}%")

        except Exception as e:
            print(f"⚠️  No se pudo verificar calidad del audio: {e}")

    def is_recording(self):
        """Verifica si está grabando actualmente"""
        return self.recording

    def list_devices(self):
        """Lista los dispositivos de audio disponibles"""
        print("🎧 Dispositivos de audio disponibles:")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            device_type = []
            if device['max_input_channels'] > 0:
                device_type.append('Input')
            if device['max_output_channels'] > 0:
                device_type.append('Output')

            print(f"  {i}: {device['name']} ({', '.join(device_type)})")

    def set_device(self, device_id):
        """Establece el dispositivo de entrada de audio"""
        try:
            sd.default.device[0] = device_id  # 0 para input
            device_info = sd.query_devices(device_id)
            print(f"✅ Dispositivo de entrada configurado: {device_info['name']}")
        except Exception as e:
            print(f"❌ Error al configurar dispositivo: {e}")

    def test_device(self, device_id=None):
        """Prueba un dispositivo de audio específico"""
        try:
            if device_id is not None:
                device_info = sd.query_devices(device_id)
            else:
                device_id = sd.default.device[0]
                device_info = sd.query_devices(device_id)

            print(f"🔧 Probando dispositivo: {device_info['name']}")
            print(f"   Canales entrada: {device_info['max_input_channels']}")
            print(f"   Sample rate por defecto: {device_info['default_samplerate']}")

            # Probar grabación corta
            test_duration = 0.5  # 0.5 segundos
            test_data = []

            def test_callback(indata, frames, time, status):
                test_data.append(indata.copy())

            print("🎤 Probando grabación por 0.5 segundos...")

            with sd.InputStream(
                device=device_id,
                samplerate=int(device_info['default_samplerate']),
                channels=1,
                callback=test_callback,
                blocksize=1024,
                dtype=np.float32
            ):
                sd.sleep(int(test_duration * 1000))

            if test_data:
                audio_level = np.max(np.abs(np.concatenate(test_data)))
                print(f"✅ Dispositivo funcional - Nivel de audio: {audio_level:.3f}")
                if audio_level < 0.001:
                    print("⚠️  Nivel muy bajo - verifica que el micrófono esté activo")
                return True
            else:
                print("❌ No se recibieron datos de audio")
                return False

        except Exception as e:
            print(f"❌ Error probando dispositivo: {e}")
            return False