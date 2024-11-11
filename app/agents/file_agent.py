# file_agent.py

from app.utils.file_utils import FileUtils

class FileAgent:
    def __init__(self):
        self.file_utils = FileUtils()

    def upload_file(self, source_path):
        """Uploads a file by passing only the source path to FileUtils."""
        print("Uploading file...")
        success = self.file_utils.upload_file(source_path)
        if success:
            print("Upload successful.")
        else:
            print("Upload failed.")

    def download_file(self, file_name, destination_path=None):
        """Downloads a file by specifying the file name and optional destination path."""
        print("Downloading file...")
        success = self.file_utils.download_file(file_name, destination_path)
        if success:
            print("Download successful.")
        else:
            print("Download failed.")
