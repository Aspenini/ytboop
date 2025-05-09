# YTBoop

**YTBoop** is a self-hosted YouTube downloader with a browser-based UI.

## 💡 Features
- Paste any YouTube URL
- Choose audio/video + format
- One-click download via yt-dlp
- Frontend runs on GitHub Pages
- Backend runs locally (Python + Flask)

## 📁 Repo Structure

```
ytboop/
├── backend/   # Local Flask app (yt-dlp)
└── src/       # Static website (for GitHub Pages)
```

## 🚀 How to Use

1. Clone this repo
2. Run the backend locally:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

3. Visit [https://yourusername.github.io/ytboop/](https://yourusername.github.io/ytboop/)
4. Enjoy easy one-click YouTube downloads!

> Note: Only for personal use. Do not host this backend publicly or use it to violate YouTube’s Terms of Service.
