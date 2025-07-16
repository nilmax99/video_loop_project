import os
import subprocess
import ffmpeg

def extract_frames(video_path, fps, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    temp = os.path.join(output_folder, "raw")
    os.makedirs(temp, exist_ok=True)

    subprocess.run([
        "ffmpeg", "-i", video_path,
        "-vf", f"fps={fps},scale=300:300",
        f"{temp}/frame_%06d.png"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    raw_files = sorted(os.listdir(temp))
    for i, name in enumerate(raw_files):
        ts = i / fps
        src = os.path.join(temp, name)
        dst = os.path.join(output_folder, f"frame_{ts:.2f}.png")
        os.rename(src, dst)
    os.rmdir(temp)

def get_video_duration(path):
    try:
        info = ffmpeg.probe(path)
        return float(info["format"]["duration"])
    except:
        return 0.0
