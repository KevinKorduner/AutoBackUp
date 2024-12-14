import os
from ftplib import FTP
from datetime import datetime
from tqdm import tqdm

def upload_compressed_files():
    # Configuración del FTP
    FTP_HOST = "ftp.tuservidor.com"
    FTP_USER = "tu_usuario"
    FTP_PASS = "tu_contraseña"
    FTP_REMOTE_DIR = "/ruta/en/ftp"
    
    # Carpeta de origen para los archivos comprimidos
    folder_to_upload = "subir"
    
    # Validar si la carpeta existe
    if not os.path.exists(folder_to_upload):
        print(f"La carpeta '{folder_to_upload}' no existe. Por favor créala y agrega archivos comprimidos.")
        return

    # Obtener lista de archivos en la carpeta "subir"
    files_to_upload = [f for f in os.listdir(folder_to_upload) 
                       if f.endswith(".zip") or f.endswith(".rar")]

    if not files_to_upload:
        print("No se encontraron archivos .zip o .rar en la carpeta 'subir'.")
        return

    print(f"Archivos encontrados para subir: {files_to_upload}")

    # Conectarse al servidor FTP
    try:
        print("Conectándose al servidor FTP...")
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_REMOTE_DIR)
        print(f"Conexión al servidor FTP exitosa. Directorio remoto: {FTP_REMOTE_DIR}")
    except Exception as e:
        print(f"Error al conectar al servidor FTP: {e}")
        return

    # Subir cada archivo
    for file_name in files_to_upload:
        try:
            # Obtener la ruta completa del archivo
            local_file_path = os.path.join(folder_to_upload, file_name)

            # Generar nuevo nombre para el archivo con fecha
            now = datetime.now()
            date_suffix = f"-{now.day:02d}-{now.month:02d}-{now.year}"
            new_file_name = f"{os.path.splitext(file_name)[0]}{date_suffix}{os.path.splitext(file_name)[1]}"

            # Tamaño del archivo para la barra de progreso
            file_size = os.path.getsize(local_file_path)

            print(f"Subiendo {file_name} como {new_file_name}...")
            with open(local_file_path, "rb") as f:
                with tqdm(total=file_size, desc=f"Subiendo {file_name}", unit="B", unit_scale=True) as pbar:
                    def callback(data):
                        pbar.update(len(data))
                    ftp.storbinary(f"STOR {new_file_name}", f, callback=callback)
            print(f"Archivo {new_file_name} subido correctamente.")
        except Exception as e:
            print(f"Error al subir {file_name}: {e}")

    # Cerrar la conexión FTP
    try:
        ftp.quit()
        print("Conexión FTP cerrada.")
    except Exception as e:
        print(f"Error al cerrar la conexión FTP: {e}")

    print("Proceso de subida completado.")

# Ejecutar el script
if __name__ == "__main__":
    upload_compressed_files()
