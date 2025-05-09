from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import subprocess
import os
import uuid
import glob

app = Flask(__name__)
CORS(app)

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

    base_filename = f"ytboop_{uuid.uuid4().hex}"
    download_path = os.path.join(DOWNLOADS_DIR, f"{base_filename}.%(ext)s")

    cmd = ["yt-dlp", "-o", download_path, url]

    if os.path.exists("cookies.txt"):
        cmd += ["--cookies", "cookies.txt"]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        return jsonify({"error": "Download failed. Check URL or video restrictions."}), 500

    # Find the actual downloaded file
    downloaded_files = glob.glob(os.path.join(DOWNLOADS_DIR, f"{base_filename}.*"))
    if not downloaded_files:
        return jsonify({"error": "No output file found."}), 500

    actual_path = downloaded_files[0]
    actual_ext = os.path.splitext(actual_path)[1].lstrip(".").lower()
    final_path = os.path.join(DOWNLOADS_DIR, f"{base_filename}.{format_}")

    # If already in correct format, just return
    if actual_ext == format_:
        return send_file(actual_path, as_attachment=True)

    # Otherwise convert using ffmpeg
    try:
        subprocess.run(["ffmpeg", "-y", "-i", actual_path, final_path], check=True)
        os.remove(actual_path)
    except Exception:
        return jsonify({"error": "FFmpeg conversion failed."}), 500

    return send_file(final_path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)
