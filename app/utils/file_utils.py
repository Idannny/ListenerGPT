# app/utils/file_utils.py
import os
import shutil
from app.settings import settings

class FileUtils:
    def __init__(self, destination_folder=settings.UPLOAD_FOLDER):
        self.destination_folder = destination_folder
        if not os.path.exists(self.destination_folder):
            os.makedirs(self.destination_folder)

    def upload_file(self, file_path):
        """Simulate file upload by copying the file to the destination folder."""
        if os.path.exists(file_path):
            try:
                shutil.copy(file_path, self.destination_folder)
                print(f"File '{file_path}' uploaded successfully to {self.destination_folder}.")
                return True
            except Exception as e:
                print(f"Failed to upload file: {e}")
                return False
        else:
            print("File not found.")
            return False

    def download_file(self, file_name, destination_path=settings.DOWNLOAD_FOLDER):
        """Simulate file download by copying a file from the destination folder to the specified path."""
        source_file = os.path.join(self.destination_folder, file_name)
        if os.path.exists(source_file):
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            try:
                shutil.copy(source_file, destination_path)
                print(f"File '{file_name}' downloaded successfully to {destination_path}.")
                return True
            except Exception as e:
                print(f"Failed to download file: {e}")
                return False
        else:
            print("File not found.")
            return False
