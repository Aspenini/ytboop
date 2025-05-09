from flask import Flask, request, send_file
from flask_cors import CORS
import subprocess
import os
import urllib.parse
import uuid
import shutil

app = Flask(__name__)
CORS(app)

# Path to user's Downloads folder
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "YTBoop")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    media_type = request.form.get('type')
    format_ = request.form.get('format')

    if not url or not media_type or not format_:
        return "Missing parameters", 400

    # Use a random filename
    base_filename = f"ytboop_{uuid.uuid4().hex}"
    temp_path = os.path.join(DOWNLOADS_DIR, f"{base_filename}.temp")
    final_path = os.path.join(DOWNLOADS_DIR, f"{base_filename}.{format_}")

    # Download best format using yt-dlp
    download_cmd = ['yt-dlp', '-f', 'best', '-o', temp_path, url]
    subprocess.run(download_cmd)

    # Convert using ffmpeg
    convert_cmd = ['ffmpeg', '-y', '-i', temp_path, final_path]
    subprocess.run(convert_cmd)

    # Remove temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    return send_file(final_path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)
