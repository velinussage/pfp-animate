#!/usr/bin/env python3
"""
PFP Animate (Veo) - Generate videos with synchronized audio using Google Veo 3.1.

Single-model solution that generates video AND audio from image + text prompt.
Uses google/veo-3.1 on Replicate (~$0.40/sec with audio, ~$0.20/sec without).

Usage:
    python animate_veo.py IMAGE OUTPUT --prompt "description of what happens"
    python animate_veo.py photo.png video.mp4 --prompt "person speaks to camera"
    python animate_veo.py photo.png video.mp4 --prompt "person waves hello" --no-audio
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


# Veo 3.1 model
VEO_MODEL = "google/veo-3.1"


def check_token():
    """Verify REPLICATE_API_TOKEN is set."""
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("ERROR: REPLICATE_API_TOKEN environment variable not set.")
        print("Get your token at: https://replicate.com/account/api-tokens")
        sys.exit(1)
    return token


def load_image_as_uri(file_path: str) -> str:
    """Load image and return as data URI."""
    if file_path.startswith(("http://", "https://")):
        return file_path

    path = Path(file_path)
    if not path.exists():
        print(f"ERROR: Image file not found: {file_path}")
        sys.exit(1)

    suffix = path.suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    mime_type = mime_types.get(suffix, "image/png")

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{data}"


def api_call(method: str, url: str, data: dict = None, retries: int = 3) -> dict:
    """Make API request with retry on rate limit."""
    token = os.environ.get("REPLICATE_API_TOKEN")

    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8') if data else None,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            method=method
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            error_body = e.read().decode('utf-8') if e.fp else str(e)
            print(f"ERROR: API request failed: {e.code}")
            print(f"Details: {error_body}")
            sys.exit(1)


def wait_for_prediction(prediction_id: str, timeout: int = 600) -> dict:
    """Wait for prediction to complete."""
    token = os.environ.get("REPLICATE_API_TOKEN")
    url = f"https://api.replicate.com/v1/predictions/{prediction_id}"

    start = time.time()
    last_status = None

    while time.time() - start < timeout:
        result = api_call("GET", url)
        status = result.get("status")

        if status != last_status:
            elapsed = time.time() - start
            print(f"  Status: {status} ({elapsed:.0f}s)")
            last_status = status

        if status == "succeeded":
            return result
        elif status in ["failed", "canceled"]:
            error = result.get("error", "Unknown error")
            print(f"ERROR: Prediction {status}: {error}")
            return result

        time.sleep(5)

    return {"status": "timeout", "error": f"Prediction timed out after {timeout}s"}


def animate_veo(
    input_image: str,
    output_path: str,
    prompt: str,
    duration: int = 8,
    resolution: str = "1080p",
    aspect_ratio: str = "9:16",
    generate_audio: bool = True,
    reference_images: list = None,
    end_image: str = None,
) -> str:
    """Generate video with Veo 3.1."""

    check_token()

    # Load start image
    print(f"Loading image: {input_image}")
    image_uri = load_image_as_uri(input_image)

    # Calculate cost
    cost_per_sec = 0.40 if generate_audio else 0.20
    est_cost = duration * cost_per_sec
    print(f"\nDuration: {duration}s")
    print(f"Resolution: {resolution}")
    print(f"Aspect ratio: {aspect_ratio}")
    print(f"Audio: {'yes' if generate_audio else 'no'}")
    print(f"Estimated cost: ~${est_cost:.2f}")
    print(f"\nPrompt: {prompt}")

    # Build input
    input_data = {
        "prompt": prompt,
        "start_image": image_uri,
        "duration": duration,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "generate_audio": generate_audio,
    }

    # Optional: reference images for style consistency
    if reference_images:
        ref_uris = [load_image_as_uri(img) for img in reference_images]
        input_data["reference_images"] = ref_uris
        print(f"Reference images: {len(ref_uris)}")

    # Optional: end image for transitions
    if end_image:
        input_data["end_image"] = load_image_as_uri(end_image)
        print(f"End image: {end_image}")

    # Create prediction
    print(f"\nStarting Veo 3.1 generation...")
    url = f"https://api.replicate.com/v1/models/{VEO_MODEL}/predictions"
    prediction = api_call("POST", url, {"input": input_data})

    prediction_id = prediction.get("id")
    if not prediction_id:
        print(f"ERROR: Failed to create prediction: {prediction}")
        sys.exit(1)

    print(f"Prediction ID: {prediction_id}")

    # Wait for completion
    result = wait_for_prediction(prediction_id)

    if result.get("status") != "succeeded":
        error = result.get("error", "Unknown error")
        print(f"ERROR: Generation failed: {error}")
        sys.exit(1)

    # Get output URL
    output_url = result.get("output")
    if isinstance(output_url, list):
        output_url = output_url[0]

    if not output_url:
        print("ERROR: No output URL in response")
        sys.exit(1)

    # Ensure output path has .mp4 extension
    if not output_path.lower().endswith(".mp4"):
        output_path += ".mp4"

    # Download video
    print(f"Downloading video...")
    try:
        with urllib.request.urlopen(output_url) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        file_size = Path(output_path).stat().st_size / (1024 * 1024)
        print(f"\nSUCCESS: Video saved to {output_path}")
        print(f"File size: {file_size:.1f} MB")
        return output_path
    except Exception as e:
        print(f"ERROR: Failed to download video: {e}")
        print(f"Video URL (download manually): {output_url}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate videos with synchronized audio using Veo 3.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s photo.png video.mp4 --prompt "person speaks to camera saying hello"
  %(prog)s avatar.png intro.mp4 --prompt "character waves and smiles" --duration 6
  %(prog)s pfp.png story.mp4 --prompt "dramatic reveal" --aspect 16:9

Prompt tips:
  - Describe the motion/action you want to see
  - Include speech in quotes: 'person says "Hello world"'
  - Mention audio: "with wind sounds", "upbeat music"
  - Camera movements: "camera slowly zooms in"

Cost: ~$0.40/sec with audio, ~$0.20/sec without
      8 second video with audio = ~$3.20
"""
    )

    parser.add_argument("image", help="Input image path or URL")
    parser.add_argument("output", help="Output video path (.mp4)")
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Description of what happens in the video"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        choices=[4, 6, 8],
        default=8,
        help="Video duration in seconds (default: 8)"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["720p", "1080p"],
        default="1080p",
        help="Video resolution (default: 1080p)"
    )
    parser.add_argument(
        "--aspect", "-a",
        choices=["16:9", "9:16"],
        default="9:16",
        help="Aspect ratio (default: 9:16 portrait)"
    )
    parser.add_argument(
        "--no-audio",
        action="store_true",
        help="Disable audio generation (cheaper)"
    )
    parser.add_argument(
        "--reference", "-ref",
        nargs="+",
        help="Reference images for style consistency (up to 3)"
    )
    parser.add_argument(
        "--end-image",
        help="End frame image for transitions"
    )

    args = parser.parse_args()

    animate_veo(
        input_image=args.image,
        output_path=args.output,
        prompt=args.prompt,
        duration=args.duration,
        resolution=args.resolution,
        aspect_ratio=args.aspect,
        generate_audio=not args.no_audio,
        reference_images=args.reference,
        end_image=args.end_image,
    )


if __name__ == "__main__":
    main()
