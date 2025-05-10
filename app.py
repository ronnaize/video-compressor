from flask import Flask, request, send_file, render_template_string
import subprocess
import os
import uuid

app = Flask(__name__)
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

HTML_FORM = '''
<h2>Compressed Video Downloader</h2>
<form method="post" action="/download">
  <input name="url" placeholder="Enter video URL" size="50" required><br><br>
  <label>Choose resolution:</label>
  <select name="resolution">
    <option value="1080p">1080p</option>
    <option value="720p" selected>720p</option>
    <option value="480p">480p</option>
  </select><br><br>
  <button type="submit">Download Compressed Video</button>
</form>
'''

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    resolution = request.form.get('resolution', '720p')
    res_map = {
        "1080p": "1920:1080",
        "720p": "1280:720",
        "480p": "854:480"
    }
    scale = res_map.get(resolution, "1280:720")

    video_id = str(uuid.uuid4())
    input_path = f"{TEMP_DIR}/{video_id}.mp4"
    output_path = f"{TEMP_DIR}/{video_id}_{resolution}.mp4"

    try:
        subprocess.run(["yt-dlp", "-f", "best", "-o", input_path, url], check=True)

        subprocess.run([
            "ffmpeg", "-i", input_path,
            "-vf", f"scale={scale}",
            "-vcodec", "libx264", "-crf", "30", "-preset", "veryfast",
            "-acodec", "aac", "-b:a", "64k", output_path
        ], check=True)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"<p>Error: {str(e)}</p>"

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

if __name__ == "__main__":
    app.run(debug=True)
