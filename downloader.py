# Importa las bibliotecas necesarias:
# - os: Para interactuar con el sistema operativo, como crear carpetas.
# - pathlib.Path: Para manejar rutas de sistema de archivos de una manera orientada a objetos y multiplataforma.
# - yt_dlp: La biblioteca principal para descargar videos de YouTube y otros sitios.
# - tqdm: Para crear barras de progreso visuales y atractivas.
import os
from pathlib import Path
import yt_dlp
from tqdm import tqdm

# --- Lógica para la Barra de Progreso Personalizada ---
# Diccionario para almacenar las barras de progreso activas. La clave es el nombre del archivo.
progress_bars = {}

def progress_hook(d):
    """
    Esta función se ejecuta en diferentes etapas del proceso de descarga de yt-dlp.
    Se utiliza para actualizar la barra de progreso (tqdm).
    """
    # Obtiene el nombre base del archivo para usarlo como identificador único.
    file_key = os.path.basename(d.get('filename', 'unknown_file'))
    
    # Si el estado es 'downloading', se crea o actualiza la barra de progreso.
    if d['status'] == 'downloading':
        # Obtiene el tamaño total del archivo en bytes.
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        
        # Si no existe una barra de progreso para este archivo y se conoce el tamaño total, se crea una.
        if file_key not in progress_bars and total_bytes:
            progress_bars[file_key] = tqdm(
                total=total_bytes,          # Tamaño total de la descarga.
                unit='B',                   # Unidad (Bytes).
                unit_scale=True,            # Escala automáticamente a KB, MB, GB.
                desc=file_key,              # Descripción que aparece junto a la barra.
                colour='green',             # Color de la barra.
                bar_format='{l_bar}{bar:30}{r_bar}' # Formato visual de la barra.
            )
            
        # Si ya existe una barra para este archivo, se actualiza su progreso.
        if file_key in progress_bars:
            pbar = progress_bars[file_key]
            # `pbar.update` avanza la barra por la diferencia entre los bytes ya descargados y el estado anterior.
            pbar.update(d['downloaded_bytes'] - pbar.n)
            
    # Si el estado es 'finished', la descarga ha terminado.
    elif d['status'] == 'finished':
        # Si existe una barra de progreso, se completa al 100% y se cierra.
        if file_key in progress_bars:
            pbar = progress_bars[file_key]
            pbar.update(pbar.total - pbar.n) # Asegura que la barra llegue al final.
            pbar.close()
            # Se elimina la barra del diccionario para liberar memoria.
            del progress_bars[file_key]
            
    # Si ocurre un error durante la descarga.
    elif d['status'] == 'error':
        # Si hay una barra de progreso activa, se cierra y se elimina.
        if file_key in progress_bars:
            progress_bars[file_key].close()
            del progress_bars[file_key]
# --- Fin de la lógica de la barra de progreso ---

def get_download_path(mode):
    """
    Determina y devuelve la ruta de descarga según el modo ('audio' o 'video').
    Utiliza la carpeta 'Downloads' del usuario como base.
    """
    if mode == 'audio':
        # Para audio, la ruta es: C:\Users\TuUsuario\Downloads\Downloads MP3
        return Path.home() / "Downloads" / "Downloads MP3"
    else: # mode == 'video'
        # Para video, la ruta es: C:\Users\TuUsuario\Downloads\Downloads mp4
        return Path.home() / "Downloads" / "Downloads mp4"

def setup_download_directories():
    """
    Verifica si las carpetas de descarga existen y, si no, las crea.
    Esto previene errores si el script se ejecuta por primera vez.
    """
    print("Verificando directorios de descarga ('Downloads MP3' y 'Downloads mp4')...")
    try:
        # os.makedirs con exist_ok=True no lanza un error si la carpeta ya existe.
        os.makedirs(get_download_path('video'), exist_ok=True)
        os.makedirs(get_download_path('audio'), exist_ok=True)
        print("Directorios listos.")
        return True
    except OSError as e:
        # Captura errores de permisos o del sistema al crear las carpetas.
        print(f"Error al crear directorios: {e}")
        return False

def start_download(url, mode):
    """
    Función principal de descarga. Configura y ejecuta yt-dlp.
    'mode' define si se descarga un 'video' completo o solo el 'audio'.
    """
    # Obtiene la ruta de destino correcta según el modo.
    download_path = get_download_path(mode)
    print(f"\nPreparando descarga en modo '{mode.upper()}' a: {download_path}")

    # --- Configuración de Opciones para yt-dlp (ydl_opts) ---
    if mode == 'audio':
        # Opciones específicas para descargar y convertir a MP3.
        ydl_opts = {
            'cookies_from_browser': ('chrome',),
            # 'format': 'bestaudio/best' -> Selecciona la mejor calidad de solo audio.
            'format': 'bestaudio/best',
            # 'postprocessors': Define acciones a realizar después de la descarga.
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',      # Usa FFmpeg para extraer el audio.
                'preferredcodec': 'mp3',          # Convierte el audio a formato MP3.
                'preferredquality': '192',        # Calidad del MP3 en kbps.
            }],
            # 'outtmpl': Plantilla para el nombre del archivo de salida.
            # '%(title)s' es el título del video, '%(ext)s' es la extensión final (mp3).
            'outtmpl': str(download_path / '%(title)s.%(ext)s'),
            # 'progress_hooks': Lista de funciones a llamar para seguir el progreso.
            'progress_hooks': [progress_hook],
            # Opciones para una salida más limpia en la consola.
            'noprogress': True, # Desactiva la barra de progreso nativa de yt-dlp.
            'quiet': True,      # Suprime mensajes de yt-dlp.
        }
    else: # modo 'video'
        # Opciones para descargar el video en la mejor calidad posible (MP4).
        ydl_opts = {
            'cookies_from_browser': ('chrome',),
            # 'format': Intenta descargar el mejor video en MP4 y el mejor audio en M4A,
            # y si no, la mejor versión que ya venga unida en formato MP4.
            'format': "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            # 'merge_output_format': Si se descargan video y audio por separado, los une en un archivo MP4.
            'merge_output_format': 'mp4',
            'outtmpl': str(download_path / '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'noprogress': True,
            'quiet': True,
        }

    try:
        # 'with' asegura que los recursos de YoutubeDL se manejen correctamente.
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Inicia la descarga de la URL o lista de URLs.
            ydl.download([url])
        print(f"¡Proceso finalizado para {url}!")
        return True
    except yt_dlp.utils.DownloadError as e:
        # Error específico de yt-dlp (URL inválida, video no disponible, etc.).
        print(f"\n--- ERROR DE DESCARGA ---")
        print(f"No se pudo procesar la URL. Revisa que sea correcta. (Detalles: {e})")
        return False
    except Exception as e:
        # Cualquier otro error inesperado durante el proceso.
        print(f"Ocurrió un error inesperado: {e}")
        return False

def show_menu():
    """Muestra el menú de opciones principal y retorna la elección del usuario."""
    print("\n" + "="*147)
    print("¿Qué te gustaría hacer?")
    print("[1] Descargar Video (MP4)")
    print("[2] Descargar solo Audio (MP3)")
    print("[i] Ver Instrucciones de Nuevo")
    print("[q] Salir del programa")
    # .lower() convierte la entrada a minúsculas para simplificar la comparación.
    return input("Elige una opción: ").lower()

def clear_screen():
    """Limpia la pantalla de la consola, compatible con Windows, Mac y Linux."""
    # Para Windows, el comando es 'cls'. Para otros sistemas (Mac/Linux), es 'clear'.
    os.system('cls' if os.name == 'nt' else 'clear')

def show_instructions():
    """Muestra el mensaje de bienvenida y las instrucciones de instalación."""
    clear_screen()
    print("--- Descargador de Videos de YouTube (v3.1 con Carpetas Personalizadas) ---")
    # Mensaje informativo sobre las dependencias del script.
    print("""
===================================================================================================================================================
¡Bienvenido! Antes de empezar, asegúrate de tener todo lo necesario.

Este script depende de tres herramientas externas:
* "yt-dlp":   El motor que descarga los videos.
* "tqdm":     La librería que crea las barras de progreso visuales.
* "FFmpeg":   Una herramienta para procesar audio y video (unir, convertir 
              a MP3, etc.).

--- PASOS DE INSTALACIÓN (Realizar una sola vez) ---

1. Abre una terminal (Símbolo del sistema, PowerShell o Terminal de Windows).

2. Instala las librerías de Python con este comando:
   pip install yt-dlp tqdm

3. Instala FFmpeg (necesario para audio y video). El modo más fácil en Windows es:
   winget install Gyan.FFmpeg

   Si no tienes 'winget', puedes descargarlo desde https://ffmpeg.org y asegurarte
   de que el ejecutable esté accesible en el PATH de tu sistema.
===================================================================================================================================================
""")
    input("\nPresiona Enter para volver al menú principal...")


def main():
    """Función principal que orquesta la ejecución del script."""
    # Muestra las instrucciones por primera vez.
    clear_screen()
    print("--- Descargador de Videos de YouTube (v3.1 con Carpetas Personalizadas) ---")
    print("""
===================================================================================================================================================
¡Bienvenido! Antes de empezar, asegúrate de tener todo lo necesario.

Este script depende de tres herramientas externas:
* "yt-dlp":   El motor que descarga los videos.
* "tqdm":     La librería que crea las barras de progreso visuales.
* "FFmpeg":   Una herramienta para procesar audio y video (unir, convertir 
              a MP3, etc.).

--- PASOS DE INSTALACIÓN (Realizar una sola vez) ---

1. Abre una terminal (Símbolo del sistema, PowerShell o Terminal de Windows).

2. Instala las librerías de Python con este comando:
   pip install yt-dlp tqdm

3. Instala FFmpeg (necesario para audio y video). El modo más fácil en Windows es:
   winget install Gyan.FFmpeg

   Si no tienes 'winget', puedes descargarlo desde https://ffmpeg.org y asegurarte
   de que el ejecutable esté accesible en el PATH de tu sistema.
===================================================================================================================================================
""")
    
    # Prepara los directorios de descarga. Si falla, el programa termina.
    if not setup_download_directories():
        return

    # Pausa para que el usuario pueda leer las instrucciones antes de limpiar.
    input("\nPresiona Enter para continuar al menú principal...")

    # Bucle principal del programa que muestra el menú y procesa la entrada.
    while True:
        clear_screen() # Limpia la pantalla en cada repetición del menú.
        choice = show_menu()
        
        if choice == '1':
            mode = 'video'
        elif choice == '2':
            mode = 'audio'
        elif choice == 'i':
            show_instructions()
            continue
        elif choice == 'q':
            print("Saliendo del programa. ¡Hasta luego!")
            break # Rompe el bucle y finaliza el script.
        else:
            print("Opción no válida, por favor intenta de nuevo.")
            # Pausa para que el usuario vea el mensaje de error.
            input("Presiona Enter para volver al menú...")
            continue # Salta al inicio del bucle.

        # Pide al usuario la URL del video a descargar.
        url = input(f"Introduce la URL para descargar en modo '{mode.upper()}': ")
        if url:
            # Si se proporciona una URL, comienza la descarga.
            start_download(url, mode)
            # Pausa después de la descarga para ver el resultado.
            input("\nProceso terminado. Presiona Enter para volver al menú...")
        else:
            # Si no se introduce nada, informa al usuario y vuelve al menú.
            print("No se introdujo URL. Volviendo al menú.")
            input("Presiona Enter para continuar...")

# Punto de entrada del script:
# Si el archivo se ejecuta directamente (no importado), se llama a la función main().
if __name__ == "__main__":
    main()