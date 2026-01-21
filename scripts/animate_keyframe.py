#!/usr/bin/env python3
"""
PFP Animate (Keyframe) - Generate animated GIFs using expression-editor keyframes.

Much more precise control than Kling for facial expressions like nod, wink, shake.
Uses fofr/expression-editor on Replicate (~$0.002 per frame).

Usage:
    python animate_keyframe.py INPUT OUTPUT --motion nod
    python animate_keyframe.py INPUT OUTPUT --motion wink
    python animate_keyframe.py INPUT OUTPUT --motion shake_no
"""

import argparse
import base64
import io
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

try:
    from PIL import Image
    import urllib.request
    import urllib.error
except ImportError:
    print("ERROR: Required packages not installed. Run: pip install pillow")
    sys.exit(1)

# Expression-editor model version
EXPRESSION_EDITOR_VERSION = "bf913bc90e1c44ba288ba3942a538693b72e8cc7df576f3beebe56adc0a92b86"


# Keyframe presets - each is a list of parameter dicts
# Parameters: rotate_pitch, rotate_yaw, rotate_roll, blink, eyebrow, wink, pupil_x, pupil_y, aaa, eee, woo, smile
KEYFRAME_PRESETS = {
    "nod": {
        "description": "Clear nodding yes motion",
        "frames": [
            {"rotate_pitch": 0},                    # neutral
            {"rotate_pitch": -12},                  # down
            {"rotate_pitch": -15},                  # down more
            {"rotate_pitch": -10},                  # coming up
            {"rotate_pitch": 5},                    # up
            {"rotate_pitch": 8},                    # up more
            {"rotate_pitch": 3},                    # coming down
            {"rotate_pitch": -8},                   # down again
            {"rotate_pitch": -5},                   # up
            {"rotate_pitch": 0},                    # neutral
        ],
        "fps": 12,
    },
    "wink": {
        "description": "Playful wink with smile",
        "frames": [
            {"wink": 0, "smile": 0.3},              # neutral slight smile
            {"wink": 5, "smile": 0.5},              # starting wink
            {"wink": 15, "smile": 0.7},             # mid wink
            {"wink": 22, "smile": 0.9},             # full wink
            {"wink": 20, "smile": 1.0},             # hold
            {"wink": 15, "smile": 0.8},             # releasing
            {"wink": 8, "smile": 0.6},              # opening
            {"wink": 2, "smile": 0.5},              # almost open
            {"wink": 0, "smile": 0.4},              # neutral
            {"wink": 0, "smile": 0.3},              # end
        ],
        "fps": 10,
    },
    "shake_no": {
        "description": "Shaking head no",
        "frames": [
            {"rotate_yaw": 0},                      # center
            {"rotate_yaw": -8},                     # left
            {"rotate_yaw": -15},                    # far left
            {"rotate_yaw": -10},                    # coming back
            {"rotate_yaw": 5},                      # crossing center
            {"rotate_yaw": 12},                     # right
            {"rotate_yaw": 15},                     # far right
            {"rotate_yaw": 10},                     # coming back
            {"rotate_yaw": -5},                     # crossing center
            {"rotate_yaw": 0},                      # center
        ],
        "fps": 12,
    },
    "nod_wink": {
        "description": "Nod yes then wink",
        "frames": [
            {"rotate_pitch": 0, "wink": 0, "smile": 0.2},
            {"rotate_pitch": -10, "wink": 0, "smile": 0.3},
            {"rotate_pitch": -15, "wink": 0, "smile": 0.3},
            {"rotate_pitch": 5, "wink": 0, "smile": 0.4},
            {"rotate_pitch": 0, "wink": 0, "smile": 0.5},
            {"rotate_pitch": 0, "wink": 10, "smile": 0.7},
            {"rotate_pitch": 0, "wink": 22, "smile": 0.9},
            {"rotate_pitch": 0, "wink": 20, "smile": 1.0},
            {"rotate_pitch": 0, "wink": 8, "smile": 0.7},
            {"rotate_pitch": 0, "wink": 0, "smile": 0.4},
        ],
        "fps": 10,
    },
    "look_around": {
        "description": "Eyes looking around",
        "frames": [
            {"pupil_x": 0, "pupil_y": 0},           # center
            {"pupil_x": -10, "pupil_y": -5},        # upper left
            {"pupil_x": -12, "pupil_y": 0},         # left
            {"pupil_x": -8, "pupil_y": 8},          # lower left
            {"pupil_x": 0, "pupil_y": 10},          # down
            {"pupil_x": 10, "pupil_y": 8},          # lower right
            {"pupil_x": 12, "pupil_y": 0},          # right
            {"pupil_x": 8, "pupil_y": -8},          # upper right
            {"pupil_x": 0, "pupil_y": -8},          # up
            {"pupil_x": 0, "pupil_y": 0},           # center
        ],
        "fps": 8,
    },
    "surprise": {
        "description": "Surprised expression",
        "frames": [
            {"eyebrow": 0, "aaa": 0, "blink": 0},
            {"eyebrow": 5, "aaa": 10, "blink": -5},
            {"eyebrow": 10, "aaa": 30, "blink": -10},
            {"eyebrow": 12, "aaa": 50, "blink": -15},
            {"eyebrow": 12, "aaa": 40, "blink": -12},
            {"eyebrow": 10, "aaa": 30, "blink": -8},
            {"eyebrow": 8, "aaa": 20, "blink": -5},
            {"eyebrow": 5, "aaa": 10, "blink": -2},
            {"eyebrow": 2, "aaa": 5, "blink": 0},
            {"eyebrow": 0, "aaa": 0, "blink": 0},
        ],
        "fps": 12,
    },
    "laugh": {
        "description": "Laughing expression",
        "frames": [
            {"smile": 0.3, "aaa": 0, "rotate_pitch": 0},
            {"smile": 0.5, "aaa": 20, "rotate_pitch": -3},
            {"smile": 0.8, "aaa": 40, "rotate_pitch": -5},
            {"smile": 1.0, "aaa": 60, "rotate_pitch": -8},
            {"smile": 1.1, "aaa": 50, "rotate_pitch": -5},
            {"smile": 1.0, "aaa": 70, "rotate_pitch": -10},
            {"smile": 1.1, "aaa": 55, "rotate_pitch": -6},
            {"smile": 0.9, "aaa": 40, "rotate_pitch": -4},
            {"smile": 0.7, "aaa": 20, "rotate_pitch": -2},
            {"smile": 0.5, "aaa": 5, "rotate_pitch": 0},
        ],
        "fps": 10,
    },
}


def check_token():
    """Verify REPLICATE_API_TOKEN is set."""
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("ERROR: REPLICATE_API_TOKEN environment variable not set.")
        sys.exit(1)
    return token


def load_image_as_uri(image_path: str) -> str:
    """Load image and return as data URI."""
    if image_path.startswith(("http://", "https://")):
        return image_path

    path = Path(image_path)
    if not path.exists():
        print(f"ERROR: Image file not found: {image_path}")
        sys.exit(1)

    suffix = path.suffix.lower()
    mime_types = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    mime_type = mime_types.get(suffix, "image/png")

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{data}"


def create_prediction(image_uri: str, params: Dict[str, Any]) -> dict:
    """Create a prediction using direct HTTP API call."""
    import json

    token = os.environ.get("REPLICATE_API_TOKEN")
    url = "https://api.replicate.com/v1/predictions"

    input_data = {
        "image": image_uri,
        "output_format": "png",
        "output_quality": 90,
        "rotate_pitch": params.get("rotate_pitch", 0),
        "rotate_yaw": params.get("rotate_yaw", 0),
        "rotate_roll": params.get("rotate_roll", 0),
        "blink": params.get("blink", 0),
        "eyebrow": params.get("eyebrow", 0),
        "wink": params.get("wink", 0),
        "pupil_x": params.get("pupil_x", 0),
        "pupil_y": params.get("pupil_y", 0),
        "aaa": params.get("aaa", 0),
        "eee": params.get("eee", 0),
        "woo": params.get("woo", 0),
        "smile": params.get("smile", 0),
    }

    payload = json.dumps({
        "version": EXPRESSION_EDITOR_VERSION,
        "input": input_data
    }).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))


def wait_for_prediction(prediction_id: str, timeout: int = 60) -> dict:
    """Wait for prediction to complete."""
    import json

    token = os.environ.get("REPLICATE_API_TOKEN")
    url = f"https://api.replicate.com/v1/predictions/{prediction_id}"

    start = time.time()
    while time.time() - start < timeout:
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Token {token}"}
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))

        if result["status"] in ["succeeded", "failed", "canceled"]:
            return result

        time.sleep(1)

    return {"status": "timeout", "error": "Prediction timed out"}


def generate_frame(image_uri: str, params: Dict[str, Any], frame_num: int, total: int, retry_delay: float = 12.0) -> Image.Image:
    """Generate a single frame using expression-editor with rate limit handling."""

    print(f"  Frame {frame_num}/{total}: {params}")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Create prediction
            prediction = create_prediction(image_uri, params)
            prediction_id = prediction["id"]

            # Wait for completion
            result = wait_for_prediction(prediction_id)

            if result["status"] == "succeeded" and result.get("output"):
                output_url = result["output"][0] if isinstance(result["output"], list) else result["output"]
                with urllib.request.urlopen(output_url) as response:
                    return Image.open(io.BytesIO(response.read()))
            elif result.get("error"):
                raise Exception(result["error"])
            else:
                raise Exception(f"Prediction failed with status: {result['status']}")

        except urllib.error.HTTPError as e:
            if e.code == 429:
                if attempt < max_retries - 1:
                    print(f"    Rate limited, waiting {retry_delay}s...")
                    time.sleep(retry_delay)
                    continue
            print(f"ERROR generating frame {frame_num}: HTTP {e.code}")
            return None
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "throttled" in error_str.lower():
                if attempt < max_retries - 1:
                    print(f"    Rate limited, waiting {retry_delay}s...")
                    time.sleep(retry_delay)
                    continue
            print(f"ERROR generating frame {frame_num}: {e}")
            return None

    return None


def create_gif(frames: List[Image.Image], output_path: str, fps: int = 10, loop: int = 0):
    """Create animated GIF from frames."""
    if not frames:
        print("ERROR: No frames to create GIF")
        return False

    duration = int(1000 / fps)  # milliseconds per frame

    # Ensure all frames are in the same mode
    processed_frames = []
    for frame in frames:
        if frame.mode != 'RGBA':
            frame = frame.convert('RGBA')
        processed_frames.append(frame)

    # Save as GIF
    processed_frames[0].save(
        output_path,
        save_all=True,
        append_images=processed_frames[1:],
        duration=duration,
        loop=loop,
        optimize=True
    )
    return True


def create_mp4(frames: List[Image.Image], output_path: str, fps: int = 10):
    """Create MP4 from frames using ffmpeg if available."""
    import subprocess
    import tempfile

    # Save frames to temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, frame in enumerate(frames):
            frame_path = os.path.join(tmpdir, f"frame_{i:04d}.png")
            if frame.mode == 'RGBA':
                frame = frame.convert('RGB')
            frame.save(frame_path)

        # Use ffmpeg to create MP4
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", os.path.join(tmpdir, "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "23",
            output_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Warning: ffmpeg failed, falling back to GIF: {e}")
            return False


def animate_keyframe(
    input_image: str,
    output_path: str,
    motion: str = "nod",
    output_format: str = "gif",
) -> str:
    """Generate animated GIF/MP4 using expression-editor keyframes."""

    check_token()

    if motion not in KEYFRAME_PRESETS:
        print(f"ERROR: Unknown motion '{motion}'")
        print(f"Available: {', '.join(KEYFRAME_PRESETS.keys())}")
        sys.exit(1)

    preset = KEYFRAME_PRESETS[motion]
    keyframes = preset["frames"]
    fps = preset["fps"]

    print(f"Loading image: {input_image}")
    image_uri = load_image_as_uri(input_image)

    print(f"Generating {len(keyframes)} frames for '{motion}' motion...")
    print(f"Estimated cost: ${len(keyframes) * 0.002:.3f}")

    start_time = time.time()
    frames = []

    for i, params in enumerate(keyframes):
        frame = generate_frame(image_uri, params, i + 1, len(keyframes))
        if frame:
            frames.append(frame)
        else:
            print(f"Warning: Failed to generate frame {i + 1}")

        # Add delay between frames to avoid rate limiting
        if i < len(keyframes) - 1:
            time.sleep(10)  # 10s delay = 6 requests/min safe

    elapsed = time.time() - start_time
    print(f"Generated {len(frames)} frames in {elapsed:.1f}s")

    if not frames:
        print("ERROR: No frames generated")
        sys.exit(1)

    # Determine output format
    if output_format == "mp4" or output_path.lower().endswith(".mp4"):
        if create_mp4(frames, output_path, fps):
            print(f"SUCCESS: MP4 saved to {output_path}")
            return output_path
        else:
            # Fallback to GIF
            gif_path = output_path.rsplit(".", 1)[0] + ".gif"
            create_gif(frames, gif_path, fps)
            print(f"SUCCESS: GIF saved to {gif_path} (ffmpeg not available for MP4)")
            return gif_path
    else:
        if not output_path.lower().endswith(".gif"):
            output_path += ".gif"
        create_gif(frames, output_path, fps)
        print(f"SUCCESS: GIF saved to {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate animated GIFs using expression-editor keyframes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Motion presets:
{chr(10).join(f'  {name:12} - {preset["description"]} ({len(preset["frames"])} frames)' for name, preset in KEYFRAME_PRESETS.items())}

Examples:
  %(prog)s photo.png output.gif --motion nod
  %(prog)s photo.png output.gif --motion wink
  %(prog)s photo.png output.mp4 --motion nod_wink
"""
    )

    parser.add_argument("input", help="Input image path or URL")
    parser.add_argument("output", help="Output file path (.gif or .mp4)")
    parser.add_argument(
        "--motion", "-m",
        default="nod",
        choices=list(KEYFRAME_PRESETS.keys()),
        help="Motion preset (default: nod)"
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List all available motion presets"
    )

    args = parser.parse_args()

    if args.list_presets:
        print("Available motion presets:\n")
        for name, preset in KEYFRAME_PRESETS.items():
            print(f"  {name}:")
            print(f"    {preset['description']}")
            print(f"    Frames: {len(preset['frames'])}, FPS: {preset['fps']}")
            print()
        sys.exit(0)

    animate_keyframe(
        input_image=args.input,
        output_path=args.output,
        motion=args.motion,
    )


if __name__ == "__main__":
    main()
