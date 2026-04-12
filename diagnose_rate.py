#!/usr/bin/env python3
"""
Script para encontrar el sample rate correcto del dispositivo
"""

import sounddevice as sd
import numpy as np

def find_device_sample_rate(device_id):
    """Encuentra el sample rate correcto para un dispositivo"""
    print(f"🔍 Analizando dispositivo {device_id}...")

    device_info = sd.query_devices(device_id)
    print(f"📱 Nombre: {device_info['name']}")
    print(f"🎵 Sample rate por defecto: {device_info['default_samplerate']}")

    # Sample rates comunes a probar
    test_rates = [
        int(device_info['default_samplerate']),  # El del dispositivo primero
        48000, 44100, 22050, 16000, 8000, 96000, 192000
    ]

    working_rates = []

    for rate in test_rates:
        try:
            print(f"🧪 Probando {rate}Hz...", end="")

            # Test muy corto
            test_data = sd.rec(
                int(rate * 0.1),  # 0.1 segundos
                samplerate=rate,
                channels=1,
                device=device_id,
                dtype=np.float32
            )
            sd.wait()

            working_rates.append(rate)
            print(" ✅")

        except Exception as e:
            print(f" ❌ ({str(e)[:30]}...)")

    print(f"\n🎯 RESULTADO:")
    if working_rates:
        print(f"✅ Sample rates que funcionan: {working_rates}")
        print(f"💡 Recomendado usar: {working_rates[0]}Hz")
    else:
        print(f"❌ Ningún sample rate funcionó con este dispositivo")

    return working_rates

def main():
    print("🎵 DIAGNÓSTICO DE SAMPLE RATE")
    print("=" * 40)

    # Listar dispositivos de entrada
    devices = sd.query_devices()
    input_devices = []

    print("\n📱 Dispositivos de entrada disponibles:")
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            input_devices.append(i)
            default_mark = " (ACTUAL)" if i == sd.default.device[0] else ""
            print(f"  {i}: {device['name'][:50]}{default_mark}")

    if not input_devices:
        print("❌ No se encontraron dispositivos de entrada")
        return

    # Probar dispositivo actual o seleccionar uno
    current_device = sd.default.device[0]
    if current_device in input_devices:
        print(f"\n🎯 Probando dispositivo actual: {current_device}")
        working_rates = find_device_sample_rate(current_device)

        if working_rates:
            print(f"\n✅ Configuración recomendada:")
            print(f"   device {current_device}")
            print(f"   sample-rate {working_rates[0]}")
        else:
            print(f"\n💡 Prueba otro dispositivo:")
            for device_id in input_devices:
                if device_id != current_device:
                    print(f"   device {device_id}")
                    break
    else:
        print(f"\n⚠️  Dispositivo actual ({current_device}) no es de entrada")
        if input_devices:
            print(f"💡 Prueba usar: device {input_devices[0]}")

if __name__ == "__main__":
    main()