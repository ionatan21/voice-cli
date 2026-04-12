# Voice CLI - Transcripción de Audio con Whisper

Una herramienta de línea de comandos para grabar audio y transcribirlo automáticamente usando OpenAI Whisper.

## Requisitos del Sistema

### Dependencias Básicas
```bash
pip install openai-whisper sounddevice scipy numpy
```

### Dependencias Opcionales (Versión PRO)
```bash
pip install pynput pyperclip
```

### FFmpeg
Instalar FFmpeg en el sistema y asegurarse de que esté en el PATH.

## Verificación de Instalación

Antes de usar el programa, ejecutar el script de diagnóstico:

```bash
python setup.py
```

Este script verifica todas las dependencias y te guía para instalar las que falten.

## Estructura del Proyecto

```
voice-cli/
├── main.py           # Programa principal
├── main_pro.py       # Versión con funcionalidades avanzadas
├── recorder.py       # Módulo de grabación de audio
├── transcriber.py    # Módulo de transcripción con Whisper
├── hotkeys.py        # Manejo de teclas globales (PRO)
├── setup.py          # Script de verificación
├── diagnose.py       # Diagnóstico de dispositivos de audio
├── diagnose_rate.py  # Diagnóstico de frecuencias de muestreo
├── test_record.py    # Prueba de grabación directa
├── recordings/       # Directorio de archivos de audio
├── history.txt       # Historial de transcripciones
└── requirements.txt  # Lista de dependencias
```

## Cómo Empezar

### 1. Ejecutar el Programa

**Versión básica:**
```bash
python main.py
```

**Versión PRO (con hotkeys y funcionalidades avanzadas):**
```bash
python main_pro.py
```

### 2. Configuración Inicial

Al iniciar el programa verás algo como:

```
Bienvenido a Voice CLI
=============================================
Inicializando Whisper modelo 'base'...
Idioma por defecto: es
Modelo 'base' cargado correctamente
Sistema inicializado correctamente
Modelo Whisper: base
Idioma por defecto: Español (es)
Sample rate: 44100Hz

Escribe 'help' para ver los comandos disponibles
Escribe 'start' para comenzar a grabar

voice-cli> 
```

### 3. Verificar Estado del Sistema

```bash
voice-cli> status
```

Este comando muestra:
- Estado de grabación actual
- Modelo de Whisper en uso
- Idioma configurado
- Frecuencia de muestreo
- Número de archivos de audio guardados
- Estado del historial

## Configuración de Dispositivos de Audio

### Listar Dispositivos Disponibles

```bash
voice-cli> devices
```

Esto muestra todos los dispositivos de audio con su ID y capacidades.

### Cambiar Dispositivo de Audio

```bash
voice-cli> device 5
```

Usar el número ID del dispositivo que aparece en la lista.

### Probar Dispositivo Actual

```bash
voice-cli> test
```

O probar un dispositivo específico:

```bash
voice-cli> test 5
```

### Solución de Problemas de Audio

Si tienes problemas con el micrófono:

1. **Diagnóstico completo:**
   ```bash
   python diagnose.py
   ```

2. **Diagnóstico de frecuencias:**
   ```bash
   python diagnose_rate.py
   ```

3. **Prueba de grabación directa:**
   ```bash
   python test_record.py
   ```

### Configuración de Frecuencia de Muestreo

Ver frecuencia actual:
```bash
voice-cli> sample-rate
```

Cambiar frecuencia:
```bash
voice-cli> sample-rate 48000
```

Frecuencias comunes: 8000, 16000, 22050, 44100, 48000

## Grabación y Transcripción

### Proceso Básico

1. **Iniciar grabación:**
   ```bash
   voice-cli> start
   ```

2. **Hablar al micrófono**

3. **Detener grabación y transcribir:**
   ```bash
   voice-cli> stop
   ```

### Ejemplo de Sesión Completa

```
voice-cli> start
Grabando audio... (Sample rate: 44100Hz)
Usando dispositivo: Micrófono (USB Audio Device)
Probando: 44100Hz, <class 'numpy.float32'>
Configuración exitosa: 44100Hz, <class 'numpy.float32'>

voice-cli> stop
Deteniendo grabación...
Audio guardado: recordings\recording_1776034596.wav
Duración: 5.34 segundos
Nivel máximo: 0.234
Nivel de audio óptimo
Contenido de voz: 87.2%

Iniciando transcripción...
Transcribiendo: recordings\recording_1776034596.wav
Idioma configurado: es
Tamaño archivo: 580.3 KB
Transcripción completada en 1.45s
Idioma detectado: es
Texto: Este es un ejemplo de transcripción en español
Guardado en historial: history.txt

TRANSCRIPCIÓN COMPLETA:
Idioma: es
Tiempo: 1.45s
Texto: Este es un ejemplo de transcripción en español
```

## Configuración de Idiomas

### Ver Idioma Actual

```bash
voice-cli> language
```

### Cambiar Idioma

```bash
voice-cli> language es    # Español
voice-cli> language en    # Inglés
voice-cli> language fr    # Francés
```

### Ver Idiomas Disponibles

```bash
voice-cli> languages
```

### Idiomas Soportados

| Código | Idioma |
|--------|--------|
| es | Español |
| en | English |
| fr | Français |
| de | Deutsch |
| it | Italiano |
| pt | Português |
| ru | Русский |
| ja | 日本語 |
| ko | 한국어 |
| zh | 中文 |

## Modelos de Whisper

### Ver Modelo Actual

```bash
voice-cli> models
```

### Cambiar Modelo

```bash
voice-cli> model tiny     # Más rápido, menos preciso (~39 MB)
voice-cli> model base     # Balance recomendado (~74 MB)
voice-cli> model small    # Buena precisión (~244 MB)
voice-cli> model medium   # Muy buena precisión (~769 MB)
voice-cli> model large    # Mejor precisión (~1550 MB)
```

### Selección de Modelo

- **tiny**: Para pruebas rápidas o recursos limitados
- **base**: Recomendado para uso general
- **small**: Para mejor precisión sin usar mucho espacio
- **medium/large**: Para máxima precisión

## Historial de Transcripciones

### Ver Historial

Últimas 10 transcripciones:
```bash
voice-cli> history
```

Ver número específico:
```bash
voice-cli> history 5
```

### Buscar en Historial (Solo PRO)

```bash
voice-cli> history search reunión
```

### Limpiar Historial

```bash
voice-cli> clear-history
```

## Funcionalidades Avanzadas (PRO)

### Hotkeys Globales

Activar hotkeys:
```bash
voice-cli> hotkeys start
```

Teclas disponibles:
- **ESPACIO**: Iniciar/Detener grabación
- **F1**: Transcribir último archivo
- **F2**: Mostrar estado
- **F12**: Activar/Desactivar hotkeys
- **ESC**: Salir del programa

### Transcripción por Lotes

```bash
voice-cli> batch ./mi_directorio_de_audios
```

### Modo Grabación Rápida

```bash
voice-cli> quick-record
```

### Estadísticas de Uso

```bash
voice-cli> stats
```

### Configuración de Portapapeles

```bash
voice-cli> auto-copy on    # Activar copia automática
voice-cli> auto-copy off   # Desactivar
```

## Transcripción de Archivos Existentes

### Desde Línea de Comandos

```bash
python main.py --file audio.wav
python main_pro.py --file audio.wav
```

### Desde Interfaz

```bash
voice-cli> transcribe audio.wav
```

### Con Timestamps Detallados

```bash
voice-cli> timestamps audio.wav
```

### Transcripción por Lotes desde Terminal

```bash
python main_pro.py --batch ./directorio_audios
```

## Referencia de Comandos

### Comandos de Grabación
| Comando | Descripción |
|---------|-------------|
| start | Iniciar grabación |
| stop | Detener grabación y transcribir |
| status | Mostrar estado del sistema |

### Comandos de Configuración
| Comando | Descripción |
|---------|-------------|
| devices | Listar dispositivos de audio |
| device \<id\> | Seleccionar dispositivo |
| test [\<id\>] | Probar dispositivo |
| sample-rate [\<hz\>] | Ver/cambiar frecuencia de muestreo |
| models | Listar modelos de Whisper |
| model \<nombre\> | Cambiar modelo |
| language [\<código\>] | Ver/cambiar idioma |
| languages | Listar idiomas disponibles |

### Comandos de Historial
| Comando | Descripción |
|---------|-------------|
| history [\<n\>] | Ver historial |
| clear-history | Limpiar historial |

### Comandos de Transcripción
| Comando | Descripción |
|---------|-------------|
| transcribe \<archivo\> | Transcribir archivo específico |
| timestamps \<archivo\> | Transcribir con timestamps |

### Comandos PRO
| Comando | Descripción |
|---------|-------------|
| hotkeys \<start\|stop\|status\> | Controlar hotkeys |
| batch \<directorio\> | Transcribir lote de archivos |
| quick-record | Grabación rápida |
| stats | Estadísticas de uso |
| auto-copy \<on\|off\> | Configurar copia automática |
| history search \<término\> | Buscar en historial |

### Comandos Generales
| Comando | Descripción |
|---------|-------------|
| help | Mostrar ayuda |
| quit, exit | Salir del programa |

## Parámetros de Línea de Comandos

### main.py

```bash
python main.py [opciones]

Opciones:
  --model, -m {tiny,base,small,medium,large}
                        Modelo de Whisper (default: base)
  --sample-rate, -sr SAMPLE_RATE
                        Frecuencia de muestreo en Hz (default: 44100)
  --file, -f FILE       Transcribir archivo específico y salir
```

### main_pro.py

```bash
python main_pro.py [opciones]

Opciones:
  --model, -m {tiny,base,small,medium,large}
                        Modelo de Whisper (default: base)
  --sample-rate, -sr SAMPLE_RATE
                        Frecuencia de muestreo en Hz (default: 44100)
  --no-hotkeys          Deshabilitar hotkeys globales
  --file, -f FILE       Transcribir archivo específico y salir
  --batch, -b BATCH     Transcribir todos los archivos de un directorio
```

## Solución de Problemas Comunes

### Error: No se detecta audio

1. Verificar permisos de micrófono en el sistema
2. Ejecutar `python diagnose.py` para identificar dispositivos
3. Cambiar dispositivo con `device <id>`
4. Probar con `test`

### Error: Invalid sample rate

1. Ejecutar `python diagnose_rate.py`
2. Usar la frecuencia recomendada: `sample-rate <hz>`
3. Probar grabación con `start`

### Error: Transcripción vacía

1. Verificar nivel de audio con `test`
2. Acercarse más al micrófono
3. Aumentar volumen del micrófono en sistema
4. Verificar que se está hablando durante la grabación

### Error: Idioma incorrecto

1. Configurar idioma explícitamente: `language es`
2. Verificar configuración con `status`
3. Para mejor detección, usar modelo más grande: `model small`

### Hotkeys no funcionan

1. Instalar dependencia: `pip install pynput`
2. Ejecutar como administrador si es necesario
3. Verificar permisos de accesibilidad (macOS/Linux)

### Portapapeles no funciona

1. Instalar dependencia: `pip install pyperclip`
2. En Linux instalar `xclip` o `xsel`

## Archivos de Configuración

### recordings/
Directorio donde se guardan todas las grabaciones de audio en formato WAV.

### history.txt
Archivo de texto con el historial completo de transcripciones, incluyendo:
- Fecha y hora
- Archivo de origen
- Idioma detectado
- Tiempo de transcripción
- Texto transcrito

### Estructura del Historial

```
============================================================
Fecha: 2024-04-12 16:25:30
Archivo: recording_1776034596.wav
Idioma: es
Duración transcripción: 1.45s
Texto: Este es un ejemplo de transcripción en español
```

## Mejores Prácticas

### Para Mejor Calidad de Transcripción

1. **Ambiente silencioso**: Grabar en lugar con poco ruido de fondo
2. **Distancia apropiada**: Hablar a 15-30 cm del micrófono
3. **Volumen adecuado**: Verificar niveles con comando `test`
4. **Duración mínima**: Grabaciones de al menos 1-2 segundos
5. **Habla clara**: Pronunciar claramente y a velocidad normal

### Para Mejor Rendimiento

1. **Modelo apropiado**: Usar `tiny` para pruebas, `base` para uso general
2. **Sample rate óptimo**: Usar el nativo del dispositivo
3. **Idioma específico**: Configurar idioma correcto antes de grabar
4. **Archivos organizados**: Usar nombres descriptivos para transcripciones importantes

### Para Uso Productivo

1. **Hotkeys**: Usar versión PRO con hotkeys para mayor eficiencia
2. **Historial**: Revisar regularmente y limpiar cuando sea necesario
3. **Lotes**: Procesar múltiples archivos con comando `batch`
4. **Backup**: Respaldar archivos importantes de `recordings/` y `history.txt`