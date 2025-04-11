import streamlit as st
import tempfile
import os
import subprocess

st.title("🎬 Convertidor a Formato TikTok con Marca de Agua")

video_file = st.file_uploader("Sube tu video (.mp4)", type=["mp4"])
logo_path = "watermark.png"  # Reemplaza con la ruta a tu logo si está en otra carpeta

if video_file:
    if not os.path.exists(logo_path):
        st.error("⚠️ No se encontró el logo. Asegúrate de tener 'logo.png' en la misma carpeta del script.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(video_file.read())
            temp_video_path = temp_video.name

        st.video(temp_video_path)
        st.write("🎞️ Procesando video...")

        output_path = tempfile.mktemp(suffix=".mp4")

        # Comando con marca de agua en la esquina inferior derecha
        comando = [
            "ffmpeg", "-y",
            "-i", temp_video_path,
            "-i", logo_path,
            "-filter_complex", "[0:v]scale=-1:1920,crop=1080:1920[bg];[bg][1:v]overlay=W-w-20:H-h-20",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            output_path
        ]

        subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        st.success("✅ Conversión completada con marca de agua.")
        st.video(output_path)

        with open(output_path, "rb") as f:
            st.download_button(
                label="📥 Descargar Video TikTok con Logo",
                data=f.read(),
                file_name="video_tiktok_logo.mp4",
                mime="video/mp4"
            )
