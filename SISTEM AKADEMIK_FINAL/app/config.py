import os

SECRET_KEY = 'your_secret_key'
UPLOAD_FOLDER = '../uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'siakad'
}
