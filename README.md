# AutoBackUp
Backup Script programado en Python para salvar todo tipo de archivos importantes.

Backup Script con FTP y Compresión ZIP
Este script en Python automatiza la creación de backups de carpetas, los comprime en un archivo ZIP con contraseña y los sube a un servidor FTP. Además, incluye una barra de progreso y mensajes detallados en consola para facilitar el seguimiento del proceso.


Características
Compresión con contraseña: Los backups se comprimen en formato ZIP protegido con la contraseña chuekos.
Automatización completa: Copia, compresión y subida al servidor FTP con un solo comando.
Progreso visual: Muestra el porcentaje completado para la compresión y la subida al FTP.
Nombres personalizados: Los archivos ZIP tienen nombres como diciembre-6-2024.zip.



Requisitos
Sistema Operativo: Linux, macOS o Windows.
Python: Versión 3.7 o superior.
Bibliotecas de Python:
pyzipper para compresión con contraseña.
tqdm para barras de progreso.



Configura el script:

Abre el archivo backup_script.py y modifica las variables de configuración del FTP:
python
Copy code
FTP_HOST = "ftp.tuservidor.com"
FTP_USER = "tu_usuario"
FTP_PASS = "tu_contraseña"
FTP_REMOTE_DIR = "/ruta/en/ftp"


¿Dudas?
Contacto: info@kevinkorduner.com
