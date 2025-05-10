import subprocess
import uuid
import os

def download_video(url, output_path):
    subprocess.run([
        "yt-dlp", "-f", "best", "-o", output_path, url
    ], check=True)

def compress_video(input_path, output_path, crf=30, resolution="720p"):
    res_map = {
        "1080p": "1920:1080",
        "720p": "1280:720",
        "480p": "854:480"
    }
    scale = res_map.get(resolution, "1280:720")
    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-vf", f"scale={scale}",
        "-vcodec", "libx264", "-crf", str(crf),
        "-preset", "veryfast", "-acodec", "aac", "-b:a", "64k",
        output_path
    ], check=True)

def main():
    url = input("Enter video URL: ")
    resolution = input("Choose resolution (1080p, 720p, 480p): ").lower()
    video_id = str(uuid.uuid4())
    input_file = f"{video_id}.mp4"
    output_file = f"{video_id}_{resolution}.mp4"

    try:
        print("Downloading video...")
        download_video(url, input_file)
        print(f"Compressing to {resolution}...")
        compress_video(input_file, output_file, resolution=resolution)
        print(f"Done! Compressed file saved as: {output_file}")
    finally:
        if os.path.exists(input_file):
            os.remove(input_file)

if __name__ == "__main__":
    main()
