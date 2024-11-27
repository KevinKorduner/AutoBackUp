import os
import shutil
import pyzipper
from ftplib import FTP
from datetime import datetime
import calendar
from tqdm import tqdm

def backup_and_upload(folder_to_backup):
    # Configuración del FTP
    FTP_HOST = "ftp.tuservidor.com"
    FTP_USER = "tu_usuario"
    FTP_PASS = "tu_contraseña"
    FTP_REMOTE_DIR = "/ruta/en/ftp"

    # Crear carpeta temporal para el backup
    print("Creando carpeta temporal para el backup...")
    temp_backup_dir = "/tmp/backup_temp"
    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)
    os.makedirs(temp_backup_dir)

    # Copiar la carpeta a la ubicación temporal
    print(f"Copiando la carpeta '{folder_to_backup}' a la ubicación temporal...")
    backup_folder_name = os.path.basename(folder_to_backup)
    temp_folder = os.path.join(temp_backup_dir, backup_folder_name)
    shutil.copytree(folder_to_backup, temp_folder)

    # Crear el archivo ZIP con contraseña
    print("Comprimiendo la carpeta en un archivo ZIP con contraseña...")
    now = datetime.now()
    month_name = calendar.month_name[now.month].lower()
    zip_filename = f"{month_name}-{now.day}-{now.year}.zip"
    zip_filepath = os.path.join(temp_backup_dir, zip_filename)
    password = b"chuekos"

    # Barra de progreso para la compresión
    total_files = sum([len(files) for _, _, files in os.walk(temp_folder)])
    with pyzipper.AESZipFile(zip_filepath, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password)
        with tqdm(total=total_files, desc="Comprimiendo archivos", unit="file") as pbar:
            for root, dirs, files in os.walk(temp_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_folder)
                    zipf.write(file_path, arcname)
                    pbar.update(1)

    print(f"Archivo ZIP creado: {zip_filepath}")

    # Subir el archivo ZIP al servidor FTP
    print("Conectando al servidor FTP y subiendo el archivo ZIP...")
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_REMOTE_DIR)

        # Barra de progreso para la subida
        file_size = os.path.getsize(zip_filepath)
        with open(zip_filepath, "rb") as f:
            with tqdm(total=file_size, desc="Subiendo al FTP", unit="B", unit_scale=True) as pbar:
                def callback(data):
                    pbar.update(len(data))

                ftp.storbinary(f"STOR {zip_filename}", f, callback=callback)

        print(f"Backup {zip_filename} subido correctamente al servidor FTP.")
        ftp.quit()
    except Exception as e:
        print(f"Error al subir el archivo al FTP: {e}")
    finally:
        # Limpiar carpeta temporal
        print("Limpiando archivos temporales...")
        if os.path.exists(temp_backup_dir):
            shutil.rmtree(temp_backup_dir)
        print("Proceso completado.")

# Solicitar la ruta de la carpeta a respaldar
if __name__ == "__main__":
    folder_path = input("Introduce la ruta de la carpeta a respaldar: ")
    if os.path.exists(folder_path):
        backup_and_upload(folder_path)
    else:
        print("La ruta proporcionada no existe. Por favor verifica e intenta de nuevo.")
