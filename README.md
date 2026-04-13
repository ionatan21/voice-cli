# Voice CLI - Transcripción de Audio con Whisper

Una herramienta de línea de comandos para grabar audio y transcribirlo automáticamente usando OpenAI Whisper. Permite grabaciones interactivas, transcripción de archivos existentes, y se puede usar como comando global del sistema.

## 🚀 Instalación Rápida

### Opción 1: Instalación como Comando Global (Recomendado)

**1. Instalar dependencias:**
```bash
pip install openai-whisper sounddevice scipy numpy
```

**Para versión PRO (hotkeys y funcionalidades avanzadas):**
```bash
pip install pynput pyperclip
```

**2. Instalar FFmpeg:**
Descargar e instalar FFmpeg y asegurarse de que esté en el PATH del sistema.

**3. Ejecutar el instalador automático:**
```bash
python installer.py
```

El instalador automáticamente:
- Crea el directorio `C:\Users\TuUsuario\bin` (Windows) o `~/.local/bin` (Unix)
- Copia todos los archivos necesarios
- Configura la variable PATH automáticamente
- Crea wrapper scripts para Windows si es necesario

**4. Reiniciar la terminal**

**5. ¡Usar desde cualquier lugar!**
```bash
voice                          # Modo interactivo
voice transcribe audio.wav     # Transcribir archivo
voice help                     # Ver ayuda completa
```

### Opción 2: Instalación Local

Para usar sin instalar como comando global:

**1. Clonar/descargar el proyecto**
**2. Instalar dependencias (mismo proceso anterior)**
**3. Ejecutar directamente:**
```bash
python main.py      # Versión básica
python main_pro.py  # Versión PRO
```

### Verificación de Instalación

Probar la instalación con el script de diagnóstico:

```bash
python setup.py
```

Este script verifica todas las dependencias y te guía para instalar las que falten.

### Desinstalación

Para desinstalar completamente la instalación global:

```bash
python uninstaller.py
```

## 📦 Uso como Comando Global

Después de la instalación global, puedes usar `voice` desde cualquier directorio:

### Comandos Principales
```bash
voice                                    # Modo interactivo completo
voice transcribe archivo.wav             # Transcribir archivo específico
voice transcribe archivo.wav -l en       # Transcribir en inglés
voice batch ./directorio_audios          # Transcribir lote de archivos
voice devices                           # Ver dispositivos de audio
voice config                            # Ver configuración actual
voice help                              # Ayuda completa
voice version                           # Ver versión
```

### Grabación Rápida
```bash
voice start                             # Grabación interactiva
voice record -d 10                      # Grabar 10 segundos
voice record -d 5 --transcribe          # Grabar y transcribir automáticamente
```

### Opciones Avanzadas
```bash
# Especificar modelo, idioma y frecuencia de muestreo
voice transcribe audio.wav --model small --language en --sample-rate 48000

# Verificar configuración
voice config
```

## 📁 Estructura del Proyecto

```
voice-cli/
├── installer.py      # Instalador automático
├── uninstaller.py    # Desinstalador
├── voice            # Ejecutable para Unix/Linux
├── voice.bat         # Wrapper para Windows
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

## 🛠️ Instalación Manual (Alternativa)

Si prefieres instalar manualmente la configuración global:

### Windows:

1. **Crear directorio:**
   ```cmd
   mkdir C:\Users\%USERNAME%\bin
   ```

2. **Copiar archivos:**
   Copiar estos archivos a `C:\Users\%USERNAME%\bin`:
   - `voice` (sin extensión)
   - `voice.bat`
   - `recorder.py`
   - `transcriber.py`
   - `main.py`
   - `main_pro.py`
   - `hotkeys.py` (opcional)

3. **Agregar al PATH:**
   ```powershell
   [Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";C:\Users\$env:USERNAME\bin", "User")
   ```

### Unix/Linux/macOS:

1. **Crear directorio:**
   ```bash
   mkdir -p ~/.local/bin
   ```

2. **Copiar archivos:**
   ```bash
   cp voice recorder.py transcriber.py main.py main_pro.py ~/.local/bin/
   cp hotkeys.py ~/.local/bin/  # opcional
   chmod +x ~/.local/bin/voice
   ```

3. **Agregar al PATH:**
   ```bash
   echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.profile
   source ~/.profile
   ```

## 🚀 Cómo Empezar

### 1. Modo Comando Global (Después de Instalación)

```bash
voice config    # Verificar configuración
voice devices   # Ver dispositivos de audio disponibles
voice start     # Iniciar grabación interactiva
```

### 2. Modo Python Local

**Versión básica:**
```bash
python main.py
```

**Versión PRO (con hotkeys y funcionalidades avanzadas):**
```bash
python main_pro.py
```

### 3. Configuración Inicial

**Con comando global:**
```bash
voice config
```

**Con Python local:**
Al iniciar cualquiera de las versiones verás algo como:

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

### 4. Verificar Estado del Sistema

**Comando global:**
```bash
voice config
```

**Modo interactivo (Python local o global):**
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

## 🔧 Solución de Problemas de Instalación

### "voice no se reconoce como comando"

**Windows:**
- Verificar que `C:\Users\%USERNAME%\bin` está en el PATH
- Reiniciar la terminal completamente
- Verificar que `voice.bat` existe en el directorio
- Ejecutar: `echo %PATH%` para confirmar que el directorio está incluido

**Unix/Linux/macOS:**
- Verificar que `~/.local/bin` está en el PATH
- Ejecutar: `source ~/.profile` para recargar el PATH
- Verificar permisos: `chmod +x ~/.local/bin/voice`
- Ejecutar: `echo $PATH` para confirmar que el directorio está incluido

### "No module named 'recorder'"

- Verificar que todos los archivos `.py` están en la misma carpeta que `voice`
- Re-ejecutar el instalador: `python installer.py`
- Verificar que los archivos no se corrompieron durante la copia

### Permisos en Unix

```bash
chmod +x ~/.local/bin/voice
```

### Verificar Instalación Global

Para confirmar que la instalación global funciona correctamente:

```bash
voice config
```

Debería mostrar:
```
Configuración de Voice CLI:
Directorio de trabajo: [ruta de instalación]
Hotkeys disponibles: Sí/No
Portapapeles disponible: Sí/No
```

---

## 🎤 Configuración de Dispositivos de Audio

### Listar Dispositivos Disponibles

**Comando global:**
```bash
voice devices
```

**Modo interactivo:**
```bash
voice-cli> devices
```

Esto muestra todos los dispositivos de audio con su ID y capacidades.

### Cambiar Dispositivo de Audio

**Modo interactivo:**
```bash
voice-cli> device 5
```

Usar el número ID del dispositivo que aparece en la lista.

### Probar Dispositivo Actual

**Modo interactivo:**
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

**Modo interactivo:**
```bash
voice-cli> sample-rate              # Ver frecuencia actual
voice-cli> sample-rate 48000        # Cambiar frecuencia
```

Frecuencias comunes: 8000, 16000, 22050, 44100, 48000

## 🎙️ Grabación y Transcripción

### Proceso Básico

**Comando global - Grabación rápida:**
```bash
voice start                         # Modo interactivo
voice record -d 10                  # Grabar 10 segundos
voice record -d 5 --transcribe      # Grabar y transcribir
```

**Modo interactivo:**
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

## 🌐 Configuración de Idiomas

### Ver Idioma Actual

**Modo interactivo:**
```bash
voice-cli> language
```

### Cambiar Idioma

**Comando global (durante transcripción):**
```bash
voice transcribe archivo.wav -l es     # Español
voice transcribe archivo.wav -l en     # Inglés
voice transcribe archivo.wav -l fr     # Francés
```

**Modo interactivo:**
```bash
voice-cli> language es    # Español
voice-cli> language en    # Inglés
voice-cli> language fr    # Francés
```

### Ver Idiomas Disponibles

**Modo interactivo:**
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

## 🤖 Modelos de Whisper

### Ver Modelo Actual

**Modo interactivo:**
```bash
voice-cli> models
```

### Cambiar Modelo

**Comando global (durante transcripción):**
```bash
voice transcribe archivo.wav --model tiny      # Más rápido, menos preciso (~39 MB)
voice transcribe archivo.wav --model base      # Balance recomendado (~74 MB)
voice transcribe archivo.wav --model small     # Buena precisión (~244 MB)
```

**Modo interactivo:**
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

## 📁 Transcripción de Archivos Existentes

### Comando Global (Recomendado)

```bash
voice transcribe audio.wav                              # Transcripción básica
voice transcribe audio.wav -l en                        # Especificar idioma
voice transcribe audio.wav --model small                # Especificar modelo
voice transcribe audio.wav --model small -l en          # Combinación completa
voice batch ./directorio_audios                         # Transcribir lote de archivos
```

### Desde Python

```bash
python main.py --file audio.wav
python main_pro.py --file audio.wav
```

### Desde Modo Interactivo

```bash
voice-cli> transcribe audio.wav
```

### Con Timestamps Detallados

**Modo interactivo:**
```bash
voice-cli> timestamps audio.wav
```

### Transcripción por Lotes

**Comando global:**
```bash
voice batch ./directorio_audios
```

**Modo interactivo:**
```bash
voice-cli> batch ./mi_directorio_de_audios
```

**Desde Python:**
```bash
python main_pro.py --batch ./directorio_audios
```

## 📋 Referencia de Comandos

### Comandos Globales (después de instalación)

| Comando | Descripción |
|---------|-------------|
| `voice` | Iniciar modo interactivo completo |
| `voice transcribe <archivo>` | Transcribir archivo específico |
| `voice transcribe <archivo> -l <idioma>` | Transcribir con idioma específico |
| `voice transcribe <archivo> --model <modelo>` | Transcribir con modelo específico |
| `voice batch <directorio>` | Transcribir lote de archivos |
| `voice devices` | Listar dispositivos de audio |
| `voice start` | Iniciar grabación interactiva |
| `voice record -d <segundos>` | Grabar por tiempo determinado |
| `voice record -d <segundos> --transcribe` | Grabar y transcribir automáticamente |
| `voice config` | Ver configuración actual |
| `voice help` | Mostrar ayuda completa |
| `voice version` | Ver versión del software |

### Comandos de Modo Interactivo

#### Comandos de Grabación
| Comando | Descripción |
|---------|-------------|
| `start` | Iniciar grabación |
| `stop` | Detener grabación y transcribir |
| `status` | Mostrar estado del sistema |

#### Comandos de Configuración
| Comando | Descripción |
|---------|-------------|
| `devices` | Listar dispositivos de audio |
| `device <id>` | Seleccionar dispositivo |
| `test [<id>]` | Probar dispositivo |
| `sample-rate [<hz>]` | Ver/cambiar frecuencia de muestreo |
| `models` | Listar modelos de Whisper |
| `model <nombre>` | Cambiar modelo |
| `language [<código>]` | Ver/cambiar idioma |
| `languages` | Listar idiomas disponibles |

#### Comandos de Historial
| Comando | Descripción |
|---------|-------------|
| `history [<n>]` | Ver historial |
| `clear-history` | Limpiar historial |

#### Comandos de Transcripción
| Comando | Descripción |
|---------|-------------|
| `transcribe <archivo>` | Transcribir archivo específico |
| `timestamps <archivo>` | Transcribir con timestamps |

#### Comandos PRO (Funcionalidades Avanzadas)
| Comando | Descripción |
|---------|-------------|
| `hotkeys <start|stop|status>` | Controlar hotkeys |
| `batch <directorio>` | Transcribir lote de archivos |
| `quick-record` | Grabación rápida |
| `stats` | Estadísticas de uso |
| `auto-copy <on|off>` | Configurar copia automática |
| `history search <término>` | Buscar en historial |

#### Comandos Generales
| Comando | Descripción |
|---------|-------------|
| `help` | Mostrar ayuda |
| `quit`, `exit` | Salir del programa |

## 🛠️ Parámetros de Línea de Comandos

### Comando Global

```bash
voice transcribe [archivo] [opciones]

Opciones:
  -l, --language IDIOMA     Idioma para transcripción (es, en, fr, etc.)
  --model MODELO            Modelo Whisper (tiny, base, small, medium, large)
  --sample-rate HZ          Frecuencia de muestreo (default: 44100)
  -d, --duration SEGUNDOS   Duración de grabación para 'voice record'
  --transcribe              Auto-transcribir después de grabar
```

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

## ⚠️ Solución de Problemas Comunes

### 🔧 Problemas de Instalación

**"voice no se reconoce como comando"**
- **Windows**: Verificar que `C:\Users\%USERNAME%\bin` está en el PATH, reiniciar terminal, verificar que `voice.bat` existe
- **Unix/Linux/macOS**: Ejecutar `source ~/.profile`, verificar permisos con `chmod +x ~/.local/bin/voice`
- Verificar PATH con `echo %PATH%` (Windows) o `echo $PATH` (Unix)

**"No module named 'recorder'"**
- Re-ejecutar el instalador: `python installer.py`
- Verificar que todos los archivos `.py` están en la carpeta correcta

### 🎙️ Problemas de Audio

**Error: No se detecta audio**
1. Verificar permisos de micrófono en el sistema
2. Ejecutar `python diagnose.py` para identificar dispositivos
3. Cambiar dispositivo: `voice devices` (global) o `device <id>` (interactivo)
4. Probar con `test`

**Error: Invalid sample rate**
1. Ejecutar `python diagnose_rate.py`
2. Usar la frecuencia recomendada: `sample-rate <hz>`
3. Probar grabación con `start`

**Error: Transcripción vacía**
1. Verificar nivel de audio con `test`
2. Acercarse más al micrófono
3. Aumentar volumen del micrófono en sistema
4. Verificar que se está hablando durante la grabación

### 🌐 Problemas de Transcripción

**Error: Idioma incorrecto**
1. **Comando global**: `voice transcribe archivo.wav -l es`
2. **Modo interactivo**: `language es`
3. Verificar configuración con `voice config` o `status`
4. Para mejor detección, usar modelo más grande: `model small`

### 🔧 Problemas de Funcionalidades PRO

**Hotkeys no funcionan**
1. Instalar dependencia: `pip install pynput`
2. Ejecutar como administrador si es necesario
3. Verificar permisos de accesibilidad (macOS/Linux)

**Portapapeles no funciona**
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

## 💡 Mejores Prácticas

### Para Mejor Calidad de Transcripción

1. **Ambiente silencioso**: Grabar en lugar con poco ruido de fondo
2. **Distancia apropiada**: Hablar a 15-30 cm del micrófono
3. **Volumen adecuado**: Verificar niveles con `voice devices` o comando `test`
4. **Duración mínima**: Grabaciones de al menos 1-2 segundos
5. **Habla clara**: Pronunciar claramente y a velocidad normal

### Para Mejor Rendimiento

1. **Modelo apropiado**: Usar `tiny` para pruebas, `base` para uso general
2. **Sample rate óptimo**: Usar el nativo del dispositivo
3. **Idioma específico**: 
   - **Global**: `voice transcribe archivo.wav -l es`
   - **Interactivo**: `language es`
4. **Archivos organizados**: Usar nombres descriptivos para transcripciones importantes

### Para Uso Productivo

1. **Instalación global**: Usar `python installer.py` para acceso rápido desde cualquier directorio
2. **Hotkeys**: Activar versión PRO con hotkeys para mayor eficiencia
3. **Lotes**: Procesar múltiples archivos con `voice batch ./directorio`
4. **Historial**: Revisar regularmente y limpiar cuando sea necesario
5. **Backup**: Respaldar archivos importantes de `recordings/` y `history.txt`

## 🗂️ Archivos y Directorios

### Instalación Global
- **Windows**: `C:\Users\TuUsuario\bin\` - Contiene todos los ejecutables y scripts
- **Unix/Linux**: `~/.local/bin/` - Contiene todos los ejecutables y scripts

### Datos del Proyecto
- `recordings/` - Directorio donde se guardan todas las grabaciones en formato WAV
- `history.txt` - Historial completo de transcripciones con metadatos

### Estructura del Historial
```
============================================================
Fecha: 2024-04-12 16:25:30
Archivo: recording_1776034596.wav
Idioma: es
Duración transcripción: 1.45s
Texto: Este es un ejemplo de transcripción en español
```

---

## 🆘 Soporte y Contribuciones

**¿Problemas o sugerencias?**
- Ejecuta `python setup.py` para diagnóstico automático
- Revisa la sección "Solución de Problemas" de este README
- Usa los scripts de diagnóstico específicos (`diagnose.py`, `diagnose_rate.py`)

**Para desarrolladores:**
- El proyecto está estructurado en módulos independientes
- `recorder.py` - Manejo de dispositivos y grabación
- `transcriber.py` - Integración con Whisper
- `main.py` / `main_pro.py` - Interfaces de usuario

**Características principales:**
✅ Transcripción offline con OpenAI Whisper  
✅ Instalación como comando global del sistema  
✅ Soporte para múltiples idiomas y modelos  
✅ Grabación interactiva y transcripción de archivos  
✅ Funcionalidades PRO con hotkeys y procesamiento por lotes  
✅ Diagnóstico automático de problemas  
✅ Historial completo de transcripciones  

---

*Voice CLI - Tu herramienta de transcripción de audio inteligente* 🎙️→📝