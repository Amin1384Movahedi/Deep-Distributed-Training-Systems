import os 
import zipfile 
import socket 

# zip files in folder log to log.zip
def zip_log():
    log_folder = 'log'

    with zipfile.ZipFile(f'{socket.gethostname()}_log.zip', 'w', zipfile.ZIP_DEFLATED) as logzip:
        for dir_path, dir_name, files in os.walk(log_folder):
            for file in files:
                logzip.write(os.path.join(dir_path, file))