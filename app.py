import streamlit as st
import whisper
import tempfile
import os
import math
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Transcriptor Whisper",
    page_icon="🎤",
    layout="centered"
)

def format_time(seconds):
    """Convierte segundos a formato SRT (HH:MM:SS,sss)"""
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def generate_srt(segments):
    """Genera contenido SRT desde segmentos"""
    srt_content = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment['start'])
        segment_end = format_time(segment['end'])
        srt_content += f"{index + 1}\n"
        srt_content += f"{segment_start} --> {segment_end}\n"
        srt_content += f"{segment['text'].strip()}\n"
        srt_content += "\n"
    return srt_content

@st.cache_resource
def load_whisper_model(model_name):
    """Carga el modelo Whisper seleccionado (con caché)"""
    return whisper.load_model(model_name)

# Interfaz principal
st.title("🎤 Transcriptor de Audio con Whisper")
st.markdown("Convierte audio a texto o subtítulos SRT con timestamps precisos")

# Barra lateral con opciones
st.sidebar.header("⚙️ Configuración")

# Selector de modelo
model_options = {
    "tiny": "Tiny (39M) - Más rápido",
    "base": "Base (74M) - Balance",
    "small": "Small (244M) - Buena precisión",
    "medium": "Medium (769M) - Alta precisión",
    "large": "Large (1550M) - Máxima precisión"
}

selected_model = st.sidebar.selectbox(
    "Selecciona el modelo Whisper:",
    options=list(model_options.keys()),
    format_func=lambda x: model_options[x],
    index=1
)

# Selector de formato de salida
output_format = st.sidebar.radio(
    "Formato de salida:",
    options=["TXT", "SRT"],
    help="TXT: Texto plano\nSRT: Subtítulos con timestamps"
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Formatos soportados:**\n"
    "- MP3\n"
    "- WAV\n"
    "- MP4\n"
    "- M4A\n"
    "- OGG"
    "*Máx 8gb el archivo"
)

# Área principal
st.markdown("### 📁 Cargar archivo de audio")

uploaded_file = st.file_uploader(
    "Selecciona un archivo de audio",
    type=["mp3", "wav", "mp4", "m4a", "ogg"],
    help="Sube un archivo de audio para transcribir"
)

# Mostrar preview del audio si se carga
if uploaded_file is not None:
    st.audio(uploaded_file, format=f'audio/{uploaded_file.name.split(".")[-1]}')

    file_details = {
        "Nombre": uploaded_file.name,
        "Tamaño": f"{uploaded_file.size / (1024*1024):.2f} MB",
        "Tipo": uploaded_file.type
    }
    st.json(file_details)

# Botón de transcripción
if st.button("🚀 Transcribir Audio", type="primary", use_container_width=True):
    if uploaded_file is None:
        st.error("❌ Por favor, carga un archivo de audio primero")
    else:
        try:
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            # Cargar modelo
            with st.spinner(f"⏳ Cargando modelo {selected_model}..."):
                model = load_whisper_model(selected_model)

            st.success(f"✅ Modelo {selected_model} cargado correctamente")

            # Transcribir
            with st.spinner("🎙️ Transcribiendo audio... Esto puede tomar unos minutos"):
                result = model.transcribe(tmp_file_path)

            st.success("✅ Transcripción completada!")

            # Mostrar idioma detectado
            st.info(f"**Idioma detectado:** {result['language']}")

            # Generar salida según formato seleccionado
            if output_format == "TXT":
                st.markdown("### 📄 Texto transcrito")
                st.text_area(
                    "Transcripción",
                    value=result['text'],
                    height=300,
                    label_visibility="collapsed"
                )

                # Botón de descarga
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"transcripcion_{timestamp}.txt"

                st.download_button(
                    label="⬇️ Descargar TXT",
                    data=result['text'],
                    file_name=filename,
                    mime="text/plain",
                    use_container_width=True
                )

            else:  # SRT
                srt_content = generate_srt(result['segments'])

                st.markdown("### 🎬 Subtítulos SRT generados")
                st.text_area(
                    "Vista previa SRT",
                    value=srt_content[:1000] + ("..." if len(srt_content) > 1000 else ""),
                    height=300,
                    label_visibility="collapsed",
                    help="Vista previa de los primeros 1000 caracteres"
                )

                # Mostrar estadísticas
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Segmentos", len(result['segments']))
                with col2:
                    duration = result['segments'][-1]['end']
                    st.metric("Duración", f"{duration:.1f}s")

                # Botón de descarga
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"subtitulos_{timestamp}.srt"

                st.download_button(
                    label="⬇️ Descargar SRT",
                    data=srt_content,
                    file_name=filename,
                    mime="application/x-subrip",
                    use_container_width=True
                )

            # Limpiar archivo temporal
            os.unlink(tmp_file_path)

        except Exception as e:
            st.error(f"❌ Error durante la transcripción: {str(e)}")
            if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>Desarrollado con Streamlit y OpenAI Whisper por Juan Pablo González</small>
    </div>
    """,
    unsafe_allow_html=True
)
