"""
Módulo para transcripción de audio usando Whisper
"""
import whisper
import os
from pathlib import Path
import time

class AudioTranscriber:
    def __init__(self, model_name="base", default_language="es"):
        """
        Inicializa el transcriptor con Whisper

        Args:
            model_name (str): Modelo de Whisper a usar
                - tiny: Más rápido, menos preciso (~39 MB)
                - base: Balance entre velocidad y precisión (~74 MB)
                - small: Buena precisión (~244 MB)
                - medium: Muy buena precisión (~769 MB)
                - large: Mejor precisión (~1550 MB)
            default_language (str): Idioma por defecto ("es" para español)
        """
        self.model_name = model_name
        self.model = None
        self.default_language = default_language
        self.history_file = Path("history.txt")

        print(f"🤖 Inicializando Whisper modelo '{model_name}'...")
        print(f"🌍 Idioma por defecto: {default_language}")
        self._load_model()

    def _load_model(self):
        """Carga el modelo de Whisper"""
        try:
            self.model = whisper.load_model(self.model_name)
            print(f"✅ Modelo '{self.model_name}' cargado correctamente")
        except Exception as e:
            print(f"❌ Error al cargar modelo Whisper: {e}")
            raise

    def transcribe_file(self, audio_file, language=None):
        """
        Transcribe un archivo de audio

        Args:
            audio_file (str): Ruta al archivo de audio
            language (str, optional): Idioma del audio ('es', 'en', etc.)
                                     Si no se especifica, usa el idioma por defecto

        Returns:
            dict: Resultado de la transcripción con texto y metadata
        """
        if not self.model:
            raise RuntimeError("Modelo no está cargado")

        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_file}")

        # Verificar archivo de audio
        file_size = os.path.getsize(audio_file)
        if file_size == 0:
            print("❌ El archivo de audio está vacío")
            return None

        if file_size < 1000:  # Menos de 1KB
            print("⚠️  El archivo de audio es muy pequeño, puede estar corrupto")

        # Usar idioma por defecto si no se especifica
        if language is None:
            language = self.default_language

        print(f"🔄 Transcribiendo: {audio_file}")
        print(f"🌍 Idioma configurado: {language}")
        print(f"📏 Tamaño archivo: {file_size / 1024:.1f} KB")

        start_time = time.time()

        try:
            # Realizar transcripción con idioma específico
            result = self.model.transcribe(
                audio_file,
                language=language,    # Forzar idioma
                verbose=True,         # Más información de debug
                word_timestamps=True  # Añadir timestamps de palabras
            )

            transcription_time = time.time() - start_time
            text = result["text"].strip()

            # Verificar que hay texto
            if not text:
                print("⚠️  Transcripción vacía - posibles causas:")
                print("   - Audio demasiado corto")
                print("   - Audio sin voz clara")
                print("   - Problemas con el micrófono")
                print("   - Archivo de audio corrupto")

                # Intentar sin especificar idioma para ver si detecta algo
                print("🔄 Intentando transcripción sin forzar idioma...")

                result_auto = self.model.transcribe(
                    audio_file,
                    verbose=True
                )

                if result_auto["text"].strip():
                    print(f"✅ Transcripción automática exitosa:")
                    print(f"   Idioma detectado: {result_auto.get('language', 'desconocido')}")
                    print(f"   Texto: {result_auto['text'].strip()}")
                    text = result_auto["text"].strip()
                    result = result_auto
                else:
                    return None

            # Información del resultado
            detected_language = result.get("language", "unknown")

            result_data = {
                "text": text,
                "language": detected_language,
                "transcription_time": transcription_time,
                "audio_file": audio_file,
                "segments": result.get("segments", []),
                "file_size": file_size
            }

            print(f"✅ Transcripción completada en {transcription_time:.2f}s")
            print(f"🌍 Idioma detectado: {detected_language}")
            print(f"📝 Texto: {text}")

            # Guardar en historial
            self._save_to_history(result_data)

            return result_data

        except Exception as e:
            print(f"❌ Error durante la transcripción: {e}")
            print(f"💡 Posibles soluciones:")
            print(f"   - Verificar que FFmpeg esté instalado")
            print(f"   - Probar con un modelo más pequeño (tiny)")
            print(f"   - Verificar el archivo de audio")
            return None

    def transcribe_with_timestamps(self, audio_file, language=None):
        """
        Transcribe con timestamps detallados

        Args:
            audio_file (str): Ruta al archivo de audio
            language (str, optional): Idioma del audio

        Returns:
            list: Lista de segmentos con timestamps
        """
        result = self.transcribe_file(audio_file, language)
        if not result:
            return []

        segments = result.get("segments", [])
        timestamped_text = []

        print("\n⏰ Transcripción con timestamps:")
        print("-" * 50)

        for segment in segments:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            timestamp_info = {
                "start": start,
                "end": end,
                "text": text,
                "formatted": f"[{start:06.2f} - {end:06.2f}] {text}"
            }

            timestamped_text.append(timestamp_info)
            print(timestamp_info["formatted"])

        return timestamped_text

    def _save_to_history(self, result_data):
        """Guarda la transcripción en el historial"""
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            audio_file = Path(result_data["audio_file"]).name

            history_entry = (
                f"\n{'='*60}\n"
                f"Fecha: {timestamp}\n"
                f"Archivo: {audio_file}\n"
                f"Idioma: {result_data['language']}\n"
                f"Duración transcripción: {result_data['transcription_time']:.2f}s\n"
                f"Texto: {result_data['text']}\n"
            )

            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(history_entry)

            print(f"📚 Guardado en historial: {self.history_file}")

        except Exception as e:
            print(f"⚠️  Error al guardar en historial: {e}")

    def get_history(self, limit=10):
        """
        Obtiene el historial de transcripciones

        Args:
            limit (int): Número máximo de entradas a mostrar

        Returns:
            list: Lista de entradas del historial
        """
        if not self.history_file.exists():
            print("📚 No hay historial disponible")
            return []

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Separar por bloques
            entries = content.split("=" * 60)
            entries = [entry.strip() for entry in entries if entry.strip()]

            # Tomar las últimas entradas
            recent_entries = entries[-limit:]

            print(f"📚 Últimas {len(recent_entries)} transcripciones:")
            for i, entry in enumerate(recent_entries, 1):
                print(f"\n--- Entrada {i} ---")
                print(entry)

            return recent_entries

        except Exception as e:
            print(f"❌ Error al leer historial: {e}")
            return []

    def clear_history(self):
        """Limpia el historial de transcripciones"""
        try:
            if self.history_file.exists():
                self.history_file.unlink()
                print("🗑️  Historial limpiado")
            else:
                print("📚 No hay historial para limpiar")
        except Exception as e:
            print(f"❌ Error al limpiar historial: {e}")

    def change_model(self, new_model_name):
        """
        Cambia el modelo de Whisper

        Args:
            new_model_name (str): Nombre del nuevo modelo
        """
        print(f"🔄 Cambiando modelo de '{self.model_name}' a '{new_model_name}'...")
        self.model_name = new_model_name
        self._load_model()

    def set_language(self, language):
        """
        Establece el idioma por defecto para transcripciones

        Args:
            language (str): Código de idioma ('es', 'en', 'fr', etc.)
        """
        self.default_language = language
        print(f"🌍 Idioma por defecto cambiado a: {language}")

    def get_available_models(self):
        """Retorna los modelos disponibles de Whisper"""
        models = ["tiny", "base", "small", "medium", "large"]
        sizes = ["~39 MB", "~74 MB", "~244 MB", "~769 MB", "~1550 MB"]

        print("🤖 Modelos de Whisper disponibles:")
        for model, size in zip(models, sizes):
            current = " (ACTUAL)" if model == self.model_name else ""
            print(f"  - {model}: {size}{current}")

        return models

    def get_supported_languages(self):
        """Retorna idiomas soportados por Whisper"""
        languages = {
            'es': 'Español',
            'en': 'English',
            'fr': 'Français',
            'de': 'Deutsch',
            'it': 'Italiano',
            'pt': 'Português',
            'ru': 'Русский',
            'ja': '日本語',
            'ko': '한국어',
            'zh': '中文',
            'ar': 'العربية',
            'hi': 'हिन्दी',
            'tr': 'Türkçe',
            'pl': 'Polski',
            'nl': 'Nederlands',
            'sv': 'Svenska',
            'da': 'Dansk',
            'no': 'Norsk',
            'fi': 'Suomi'
        }

        print("🌍 Idiomas soportados por Whisper:")
        print(f"   Actual: {languages.get(self.default_language, self.default_language)} ({self.default_language})")
        print("\nDisponibles:")
        for code, name in languages.items():
            current = " (ACTUAL)" if code == self.default_language else ""
            print(f"  - {code}: {name}{current}")

        return languages