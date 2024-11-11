# app/settings/settings.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'data', 'uploads')
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'data', 'downloads')
