# Transcriptor de Audio con Whisper y Streamlit

Aplicación web para transcribir audio a texto plano o subtítulos SRT usando OpenAI Whisper.

## 🚀 Características

- **5 modelos de Whisper**: Desde tiny (más rápido) hasta large (máxima precisión)
- **Múltiples formatos**: Soporta MP3, WAV, MP4, M4A, OGG
- **Dos formatos de salida**: 
  - TXT: Texto plano
  - SRT: Subtítulos con timestamps precisos
- **Detección automática de idioma**
- **Interfaz intuitiva con Streamlit**

## 📦 Instalación

### Opción 1: Docker (Recomendado)

```bash
# Construir la imagen
docker build -t whisper-streamlit .

# Ejecutar el contenedor
docker run -p 8501:8501 whisper-streamlit
```

### Opción 2: Docker Compose

```bash
docker-compose up
```

### Opción 3: Instalación Local

```bash
# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install ffmpeg

# Instalar dependencias Python
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

## 🎯 Uso

1. Abre tu navegador en `http://localhost:8501`
2. Selecciona el modelo de Whisper en la barra lateral
3. Elige el formato de salida (TXT o SRT)
4. Carga un archivo de audio
5. Haz clic en "Transcribir Audio"
6. Descarga el resultado

## 📋 Modelos Disponibles

| Modelo | Tamaño | Velocidad | Precisión |
|--------|--------|-----------|-----------|
| tiny   | 39M    | ⚡⚡⚡⚡   | ⭐⭐     |
| base   | 74M    | ⚡⚡⚡     | ⭐⭐⭐   |
| small  | 244M   | ⚡⚡       | ⭐⭐⭐⭐ |
| medium | 769M   | ⚡         | ⭐⭐⭐⭐⭐ |
| large  | 1550M  | ⚡         | ⭐⭐⭐⭐⭐ |

## 🛠️ Tecnologías

- **Streamlit**: Interfaz web
- **OpenAI Whisper**: Motor de transcripción
- **Docker**: Contenerización
- **FFmpeg**: Procesamiento de audio
- **Python**: Backend

## 📝 Notas

- El modelo se descarga automáticamente la primera vez que se usa
- Los modelos más grandes requieren más RAM y tiempo de procesamiento
- Se recomienda usar GPU para modelos medium y large
- Tamaño máximo de archivo: 200MB (configurable)
- La dependencia correcta es `openai-whisper`; no agregues el paquete `whisper` al entorno.

## 🐛 Solución de Problemas

### Error de memoria
Si obtienes errores de memoria, prueba con un modelo más pequeño (tiny o base).

### Archivo muy grande
Aumenta el límite con:
```bash
streamlit run app.py --server.maxUploadSize=500
```

### Sin GPU
Los modelos tiny, base y small funcionan bien en CPU. Para modelos más grandes, considera usar un servidor con GPU.

## 📄 Licencia

MIT License

## 👨‍💻 Autor

Desarrollado con ❤️ usando Streamlit y OpenAI Whisper
