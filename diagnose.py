#!/usr/bin/env python3
"""
Script de diagnóstico de audio para Voice CLI
"""

import sounddevice as sd
import numpy as np
import time

def diagnose_audio():
    print("🔍 DIAGNÓSTICO COMPLETO DE AUDIO")
    print("=" * 50)

    # 1. Listar todos los dispositivos
    print("\n📱 DISPOSITIVOS DE AUDIO DISPONIBLES:")
    devices = sd.query_devices()

    input_devices = []
    for i, device in enumerate(devices):
        device_type = []
        if device['max_input_channels'] > 0:
            device_type.append('INPUT')
            input_devices.append(i)
        if device['max_output_channels'] > 0:
            device_type.append('OUTPUT')

        status = " (DEFAULT)" if i == sd.default.device[0] else ""
        print(f"  {i:2d}: {device['name'][:60]} | {'/'.join(device_type)}{status}")
        print(f"      Entrada: {device['max_input_channels']} ch | Salida: {device['max_output_channels']} ch")
        print(f"      Sample rate: {device['default_samplerate']} Hz")
        print()

    # 2. Mostrar configuración actual
    print(f"🎯 CONFIGURACIÓN ACTUAL:")
    print(f"   Dispositivo entrada por defecto: {sd.default.device[0]}")
    print(f"   Dispositivo salida por defecto: {sd.default.device[1]}")
    print(f"   Sample rate por defecto: {sd.default.samplerate}")
    print()

    # 3. Probar cada dispositivo de entrada
    print("🧪 PROBANDO DISPOSITIVOS DE ENTRADA...")

    for device_id in input_devices:
        device_info = sd.query_devices(device_id)
        print(f"\n🔬 Probando dispositivo {device_id}: {device_info['name']}")

        try:
            # Test corto de 2 segundos
            print("   Grabando 2 segundos...")

            recording_data = []

            def callback(indata, frames, time, status):
                if status:
                    print(f"     Status: {status}")
                recording_data.append(indata.copy())

            with sd.InputStream(
                device=device_id,
                samplerate=int(device_info['default_samplerate']),
                channels=1,
                callback=callback,
                blocksize=1024,
                dtype=np.float32
            ):
                print("   🎤 ¡HABLA AHORA! (2 segundos)")
                sd.sleep(2000)

            if recording_data:
                audio_data = np.concatenate(recording_data)
                max_level = np.max(np.abs(audio_data))
                rms_level = np.sqrt(np.mean(audio_data ** 2))

                print(f"   📊 Nivel máximo: {max_level:.4f}")
                print(f"   📊 Nivel RMS: {rms_level:.4f}")

                if max_level > 0.001:
                    print("   ✅ DISPOSITIVO FUNCIONAL - Audio detectado!")
                    silence_percentage = (np.sum(np.abs(audio_data) < 0.001) / len(audio_data)) * 100
                    print(f"   🎤 Contenido de voz: {100-silence_percentage:.1f}%")
                else:
                    print("   ❌ Sin audio detectado")
            else:
                print("   ❌ No se recibieron datos")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    # 4. Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    print(f"   1. Usa el dispositivo que mostró 'DISPOSITIVO FUNCIONAL'")
    print(f"   2. En Voice CLI usa: device <número_del_dispositivo>")
    print(f"   3. Si ninguno funciona, verifica permisos de micrófono")
    print(f"   4. En Windows: Configuración > Privacidad > Micrófono")

if __name__ == "__main__":
    diagnose_audio()