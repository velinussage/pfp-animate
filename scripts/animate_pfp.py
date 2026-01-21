#!/usr/bin/env python3
"""
PFP Animate - Generate animated videos from static images using Kling v2.5 Turbo Pro on Replicate.

Usage:
    python animate_pfp.py INPUT OUTPUT [OPTIONS]

Examples:
    python animate_pfp.py photo.png video.mp4
    python animate_pfp.py photo.png video.mp4 --motion wave
    python animate_pfp.py photo.png video.mp4 --prompt "slowly nodding"
    python animate_pfp.py photo.png video.mp4 --aspect 9:16 --guidance 0.7
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


# Load presets from JSON file
SCRIPT_DIR = Path(__file__).parent
PRESETS_FILE = SCRIPT_DIR / "presets.json"

def load_presets():
    """Load motion presets from JSON file."""
    if PRESETS_FILE.exists():
        with open(PRESETS_FILE) as f:
            return json.load(f)
    # Fallback presets if file not found
    return {
        "nod": {
            "prompt": "The subject gently nods their head in acknowledgment, subtle and natural movement",
            "negative": "distortion, blur, unnatural movement"
        },
        "wave": {
            "prompt": "The subject waves hello with a friendly gesture, natural arm movement",
            "negative": "distortion, blur, awkward movement"
        },
        "laugh": {
            "prompt": "The subject laughs naturally, eyes crinkling, shoulders moving slightly",
            "negative": "distortion, unnatural expression"
        },
        "idle": {
            "prompt": "The subject breathes naturally with very subtle movement, almost still but alive",
            "negative": "frozen, statue-like, jerky"
        }
    }


PRESETS = load_presets()


def check_token():
    """Verify REPLICATE_API_TOKEN is set."""
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("ERROR: REPLICATE_API_TOKEN environment variable not set.")
        print("Get your token from: https://replicate.com/account/api-tokens")
        print("Then run: export REPLICATE_API_TOKEN='r8_your_token_here'")
        sys.exit(1)
    return token


def load_image(image_path: str) -> str:
    """Load image and return as data URI or URL."""
    # If it's already a URL, return as-is
    if image_path.startswith(("http://", "https://")):
        return image_path

    # Load local file
    path = Path(image_path)
    if not path.exists():
        print(f"ERROR: Image file not found: {image_path}")
        sys.exit(1)

    # Determine MIME type
    suffix = path.suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }
    mime_type = mime_types.get(suffix, "image/png")

    # Read and encode
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{data}"


def download_video(url: str, output_path: str) -> bool:
    """Download video from URL to local file."""
    try:
        print(f"Downloading video to {output_path}...")
        urllib.request.urlretrieve(url, output_path)
        return True
    except Exception as e:
        print(f"ERROR: Failed to download video: {e}")
        return False


def animate(
    input_image: str,
    output_path: str,
    motion: str = "nod",
    prompt: str = None,
    duration: int = 5,
    negative_prompt: str = None,
    aspect_ratio: str = "1:1",
    guidance_scale: float = 0.5
) -> str:
    """
    Generate animated video from image using Kling v2.5 Turbo Pro.

    Args:
        input_image: Path to input image or URL
        output_path: Path for output video file
        motion: Motion preset name (nod, wave, laugh, think, surprise, idle)
        prompt: Custom prompt (overrides motion preset)
        duration: Video duration in seconds (5 or 10)
        negative_prompt: Things to avoid in generation
        aspect_ratio: Output aspect ratio (16:9, 9:16, or 1:1)
        guidance_scale: Prompt adherence (0.0-1.0, higher = stricter)

    Returns:
        Path to generated video file
    """
    check_token()

    # Determine prompt and negative prompt
    if prompt:
        final_prompt = prompt
        final_negative = negative_prompt or ""
    elif motion in PRESETS:
        preset = PRESETS[motion]
        final_prompt = preset["prompt"]
        final_negative = negative_prompt or preset.get("negative", "")
    else:
        print(f"WARNING: Unknown motion '{motion}', using 'nod' preset")
        preset = PRESETS["nod"]
        final_prompt = preset["prompt"]
        final_negative = negative_prompt or preset.get("negative", "")

    # Load image
    print(f"Loading image: {input_image}")
    image_data = load_image(input_image)

    # Prepare API parameters for Kling v2.5 Turbo Pro
    model = "kwaivgi/kling-v2.5-turbo-pro"
    input_params = {
        "prompt": final_prompt,
        "start_image": image_data,
        "duration": duration,
        "aspect_ratio": aspect_ratio,
        "guidance_scale": guidance_scale,
    }

    if final_negative:
        input_params["negative_prompt"] = final_negative

    # Run prediction using direct HTTP API
    print(f"Generating {duration}s video with '{motion}' motion...")
    print(f"Prompt: {final_prompt[:80]}...")
    print(f"Aspect ratio: {aspect_ratio}, Guidance: {guidance_scale}")
    print("This may take 30-120 seconds...")

    start_time = time.time()

    # Create prediction via Replicate API
    token = check_token()
    url = "https://api.replicate.com/v1/models/kwaivgi/kling-v2.5-turbo-pro/predictions"

    payload = json.dumps({"input": input_params}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "wait"  # Wait for completion
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        print(f"ERROR: Replicate API error ({e.code}): {error_body}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: Network error: {e}")
        sys.exit(1)

    # Poll for completion if not using wait preference
    while result.get("status") in ["starting", "processing"]:
        time.sleep(2)
        poll_url = result.get("urls", {}).get("get", f"https://api.replicate.com/v1/predictions/{result['id']}")
        poll_req = urllib.request.Request(
            poll_url,
            headers={"Authorization": f"Bearer {token}"},
            method="GET"
        )
        with urllib.request.urlopen(poll_req) as response:
            result = json.loads(response.read().decode('utf-8'))
        print(f"  Status: {result.get('status')}...")

    elapsed = time.time() - start_time
    print(f"Generation completed in {elapsed:.1f}s")

    if result.get("status") == "failed":
        print(f"ERROR: Generation failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)

    # Get output URL
    output = result.get("output")
    if not output:
        print("ERROR: No output returned from API")
        sys.exit(1)

    # Handle output - could be URL string or list
    video_url = output[0] if isinstance(output, list) else output

    if isinstance(video_url, str) and video_url.startswith(('http://', 'https://')):
        if download_video(video_url, output_path):
            print(f"SUCCESS: Video saved to {output_path}")
            return output_path
        else:
            print(f"Video URL (download manually): {video_url}")
            return video_url
    else:
        print(f"ERROR: Unexpected output format: {type(video_url)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate animated videos from static images using Kling v2.5 Turbo Pro",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Motion presets:
  nod       - Subtle head nod (default)
  wave      - Friendly wave
  laugh     - Laughing expression
  think     - Thoughtful head tilt
  surprise  - Surprised reaction
  idle      - Very subtle breathing/movement
  talking   - Speaking animation
  wink      - Playful wink

Examples:
  %(prog)s photo.png video.mp4
  %(prog)s photo.png video.mp4 --motion wave
  %(prog)s photo.png video.mp4 --prompt "slowly turning head"
  %(prog)s photo.png video.mp4 --duration 10 --aspect 9:16
  %(prog)s photo.png video.mp4 --guidance 0.8  # Higher prompt adherence
"""
    )

    parser.add_argument("input", nargs="?", help="Input image path or URL")
    parser.add_argument("output", nargs="?", help="Output video path (.mp4)")
    parser.add_argument(
        "--motion", "-m",
        default="nod",
        choices=list(PRESETS.keys()),
        help="Motion preset (default: nod)"
    )
    parser.add_argument(
        "--prompt", "-p",
        help="Custom motion prompt (overrides preset)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=5,
        choices=[5, 10],
        help="Video duration in seconds (default: 5)"
    )
    parser.add_argument(
        "--aspect", "-a",
        default="1:1",
        choices=["16:9", "9:16", "1:1"],
        help="Aspect ratio (default: 1:1)"
    )
    parser.add_argument(
        "--guidance", "-g",
        type=float,
        default=0.5,
        help="Guidance scale 0.0-1.0 for prompt adherence (default: 0.5)"
    )
    parser.add_argument(
        "--negative", "-n",
        help="Negative prompt (things to avoid)"
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List all available motion presets"
    )

    args = parser.parse_args()

    if args.list_presets:
        print("Available motion presets:\n")
        for name, preset in PRESETS.items():
            print(f"  {name}:")
            print(f"    {preset['prompt'][:70]}...")
            print()
        sys.exit(0)

    # Validate required args when not listing presets
    if not args.input or not args.output:
        parser.error("input and output are required")

    # Ensure output has .mp4 extension
    output = args.output
    if not output.lower().endswith(".mp4"):
        output += ".mp4"

    # Clamp guidance scale
    guidance = max(0.0, min(1.0, args.guidance))

    animate(
        input_image=args.input,
        output_path=output,
        motion=args.motion,
        prompt=args.prompt,
        duration=args.duration,
        negative_prompt=args.negative,
        aspect_ratio=args.aspect,
        guidance_scale=guidance
    )


if __name__ == "__main__":
    main()
