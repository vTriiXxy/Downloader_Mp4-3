# 📥 YouTube Video Downloader

Un script de consola sencillo y potente para descargar videos de YouTube en formato de video (MP4) o solo audio (MP3), utilizando el poder de `yt-dlp`.

---

### ✨ Motivación

Este proyecto nació como una iniciativa personal para aprender y profundizar en el desarrollo de aplicaciones de consola con Python. El objetivo era crear una herramienta práctica que me permitiera explorar el manejo de procesos externos, la interacción con el usuario en la terminal y la gestión de descargas de archivos.

### 📋 Requisitos Previos

Antes de empezar, asegúrate de tener lo siguiente instalado en tu sistema:

1.  **Python 3.x**: El script está desarrollado y probado en Python 3. Puedes descargarlo desde [python.org](https://www.python.org/).
2.  **FFmpeg**: Esta es una dependencia **crítica** que `yt-dlp` utiliza para procesar y combinar los streams de video y audio.
    *   Puedes descargar FFmpeg desde su sitio web oficial: **[ffmpeg.org](https://ffmpeg.org/)**
    *   Asegúrate de que el ejecutable `ffmpeg` esté disponible en el PATH de tu sistema para que el script pueda encontrarlo.

### 🚀 Instalación y Uso

Sigue estos pasos para poner en marcha el descargador en tu máquina local.

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```
    *(Reemplaza la URL con el enlace a tu repositorio de GitHub una vez lo hayas subido)*

2.  **Crea un entorno virtual (recomendado) e instala las dependencias:**
    ```bash
    # Crea y activa el entorno virtual
    python -m venv venv
    .\venv\Scripts\activate  # En Windows

    # Instala los paquetes necesarios
    pip install -r requirements.txt
    ```

3.  **Ejecuta el script:**
    ```bash
    python downloader.py
    ```
    El script te guiará, pidiéndote la URL del video de YouTube y el formato en el que deseas descargarlo.

### ⚖️ Aviso Legal (Disclaimer)

Este script se proporciona con fines puramente educativos y de aprendizaje. Los usuarios son los únicos responsables de asegurarse de que no infringen los términos de servicio de YouTube ni los derechos de autor del contenido que descargan. El uso de esta herramienta es bajo tu propio riesgo.
