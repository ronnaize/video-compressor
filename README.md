# Video Compressor Tool

This project contains both a **Command-Line Tool** and a **Flask Web App** to download and compress videos (e.g., from YouTube).

## Requirements

Install dependencies:

```bash
sudo apt install ffmpeg
pip install flask yt-dlp
```

## CLI Version

Run with:

```bash
python video_compressor_cli.py
```

Follow the prompts to input a URL and select the resolution.

## Web Version

Run with:

```bash
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

Use the form to enter a video URL and select the desired resolution.
