from flask import Flask, request
from flask_cors import CORS
import subprocess
import os
import urllib.parse
import json

app = Flask(__name__)
CORS(app)

DOWNLOADS_DIR = "downloads"
CONFIG_PATH = os.path.expanduser("~/.ytboop")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(CONFIG_PATH, exist_ok=True)

# Write active flag
with open(os.path.join(CONFIG_PATH, "active.json"), "w") as f:
    json.dump({"status": "running"}, f)

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

    output_path = os.path.join(DOWNLOADS_DIR, 'output.%(ext)s')
    cmd = ['yt-dlp', '-o', output_path, url]

    if media_type == 'audio':
        cmd += ['-x', '--audio-format', format_]
    else:
        cmd += ['-f', f'bestvideo[ext={format_}]+bestaudio/best']

    subprocess.run(cmd)
    return "Download started", 200

if __name__ == '__main__':
    app.run(port=5000)
