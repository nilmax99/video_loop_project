import os
from utils import extract_frames, get_video_duration
from loop_creator import find_best_loop

video_path = "input.mp4"
frame_rate = 5
frame_folder = "frames"
output_folder = "output"
output_video = os.path.join(output_folder, "loop_blurplus.mp4")

loop_min_duration = 10.0
loop_max_duration = 12.0

print("🎬 Starting loop detection and blur-plus effect generation...")
extract_frames(video_path, frame_rate, frame_folder)
loop_info = find_best_loop(frame_folder, loop_min_duration, loop_max_duration)
os.makedirs(output_folder, exist_ok=True)

video_duration = get_video_duration(video_path)

if loop_info:
    start_time, end_time, transition_type = loop_info
    duration = end_time - start_time

    # Clamp loop duration to actual video length
    if end_time > video_duration:
        end_time = video_duration
        duration = end_time - start_time
else:
    print("⚠️ No valid loop detected. Using default fallback...")
    start_time = 0.0
    duration = loop_min_duration
    transition_type = "blurplus"

# Generate final effect using the predefined blur+brightness profile
if transition_type == "blurplus":
    sections = [
        (0.00, 0.10, 30, 0.07), (0.10, 0.20, 20, 0.05), (0.20, 0.30, 12, 0.03),
        (0.30, 0.40, 6, 0.015), (0.40, 0.50, 2, 0),
        (0.50, 3.50, 0, 0), (3.50, 3.60, 0, 0),
        (3.60, 3.70, 0, 0), (3.70, 3.80, 0, 0),
        (3.80, 3.90, 0, 0), (3.90, 4.00, 0, 0),
        (4.00, 4.10, 0, 0), (4.10, 4.20, 0, 0),
        (4.20, 4.30, 0, 0), (4.30, 4.40, 0, 0),
        (4.40, duration, 0, 0)
    ]

    filters, maps = [], []

    for idx, (start, end, sigma, brightness) in enumerate(sections):
        chain = [f"trim=start={start:.2f}:end={end:.2f}", "setpts=PTS-STARTPTS"]
        if sigma > 0:
            chain.append(f"gblur=sigma={sigma}")
        if brightness > 0:
            chain.append(f"eq=brightness={brightness}")
        filters.append(f"[0:v]{','.join(chain)}[v{idx}]")
        maps.append(f"[v{idx}]")

    filter_text = ";".join(filters)
    concat_text = "".join(maps)

    cmd = (
        f"ffmpeg -ss {start_time:.2f} -t {duration:.2f} -i {video_path} "
        f"-filter_complex \"{filter_text};{concat_text}concat=n={len(maps)}:v=1:a=0[outv]\" "
        f"-map \"[outv]\" -c:v libx264 -y {output_video}"
    )

    os.system(cmd)
    print(f"\n✅ Final output created at: {output_video}")
else:
    print("❌ Unsupported effect type:", transition_type)
