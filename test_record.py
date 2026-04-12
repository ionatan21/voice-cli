"""
Versión alternativa del recorder usando método directo
"""
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time
from pathlib import Path

def record_direct(duration=10, device=None):
    """Grabación directa sin callbacks"""
    print(f"🎤 Grabación directa por {duration} segundos...")

    if device is not None:
        print(f"🎯 Usando dispositivo: {device}")

    try:
        # Grabación directa
        audio_data = sd.rec(
            int(duration * 44100),  # samples
            samplerate=44100,
            channels=1,
            device=device,
            dtype='float64'
        )

        print("🔴 ¡GRABANDO! Habla ahora...")
        sd.wait()  # Esperar hasta que termine

        # Verificar datos
        max_level = np.max(np.abs(audio_data))
        print(f"📊 Nivel detectado: {max_level:.4f}")

        if max_level > 0.001:
            print("✅ Audio grabado correctamente")

            # Guardar
            recordings_dir = Path("recordings")
            recordings_dir.mkdir(exist_ok=True)

            timestamp = int(time.time())
            filename = f"direct_recording_{timestamp}.wav"
            filepath = recordings_dir / filename

            # Normalizar y guardar
            audio_normalized = np.clip(audio_data * 32767, -32768, 32767).astype(np.int16)
            write(str(filepath), 44100, audio_normalized)

            print(f"💾 Guardado: {filepath}")
            return str(filepath)
        else:
            print("❌ No se detectó audio")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🧪 PRUEBA DE GRABACIÓN DIRECTA")

    # Listar dispositivos
    devices = sd.query_devices()
    input_devices = [i for i, d in enumerate(devices) if d['max_input_channels'] > 0]

    print("\nDispositivos de entrada:")
    for i in input_devices:
        print(f"  {i}: {devices[i]['name']}")

    # Pedir dispositivo
    device_input = input(f"\n¿Qué dispositivo usar? (Enter = por defecto): ").strip()
    device = int(device_input) if device_input else None

    # Grabar
    file_path = record_direct(duration=5, device=device)

    if file_path:
        print(f"\n✅ ¡Éxito! Archivo: {file_path}")
        print("Ahora prueba transcribirlo:")
        print(f"python main.py --file {file_path}")
    else:
        print("\n❌ Grabación falló")