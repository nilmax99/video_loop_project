# Video Loop Creator with Blur Transition

This project automatically finds the best loop point in a video and generates a seamless looping video with a smooth "blur-plus" transition effect. It's designed to create aesthetically pleasing, infinitely looping video clips suitable for backgrounds, social media, or digital displays.

## Features

-   **Automatic Loop Detection**: Analyzes video frames to find the most visually similar start and end points for a loop.
-   **Seamless Transition**: Applies a complex `ffmpeg` filtergraph that combines blur and brightness adjustments to create a smooth transition between the end and start of the loop.
-   **Configurable**: Easily adjust parameters like loop duration, frame rate for analysis, and input/output files.
-   **Efficient**: Uses `ffmpeg` for heavy lifting (frame extraction and video encoding) and `OpenCV` for efficient image comparison.

## Project Structure

```
.
├── input.mp4           # Your source video file
├── main.py             # Main script to run the process
├── loop_creator.py     # Logic for finding the best loop
├── utils.py            # Helper functions for video processing
├── requirements.txt    # Python dependencies
└── output/             # Directory for the final video (created on run)
```

## How It Works

1.  **Frame Extraction (`utils.py`)**: The input video is first broken down into individual frames at a specified frame rate. These frames are resized to a smaller dimension for faster processing.
2.  **Loop Finding (`loop_creator.py`)**: The script iterates through the extracted frames, calculating a similarity score (sum of absolute differences) between pairs of frames. It searches for the pair with the lowest difference (i.e., most similar) that falls within the desired loop duration (`loop_min_duration` and `loop_max_duration`).
3.  **Video Generation (`main.py`)**: Once the best start and end times for the loop are identified, a complex `ffmpeg` command is constructed. This command:
    -   Trims the original video to the loop segment.
    -   Applies a series of time-based blur and brightness filters to create a "dip to blur" effect at the beginning of the clip, masking the transition.
    -   Concatenates these filtered segments to produce the final, seamless looping video.

## Requirements

-   **Python 3.7+**
-   **FFmpeg**: You must have `ffmpeg` installed and accessible in your system's PATH. You can download it from ffmpeg.org.
-   Python libraries listed in `requirements.txt`.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd video_loop_project
    ```

2.  **Install FFmpeg:**
    -   **macOS (using Homebrew):** `brew install ffmpeg`
    -   **Linux (using apt):** `sudo apt update && sudo apt install ffmpeg`
    -   **Windows:** Download from the official site and add the `bin` directory to your system's PATH.

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Place your input video in the project's root directory and name it `input.mp4`, or change the `video_path` variable in `main.py`.

2.  Adjust the loop parameters in `main.py` as needed:
    ```python
    # main.py
    video_path = "input.mp4"
    frame_rate = 5  # Frames per second to analyze for loop detection. Higher is more accurate but slower.
    loop_min_duration = 10.0 # Minimum desired loop duration in seconds.
    loop_max_duration = 12.0 # Maximum desired loop duration in seconds.
    ```

3.  Run the main script:
    ```bash
    python main.py
    ```

4.  The script will print its progress. The final looping video will be saved as `output/loop_blurplus.mp4`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.