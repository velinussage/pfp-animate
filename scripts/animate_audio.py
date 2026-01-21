#!/usr/bin/env python3
"""
PFP Animate (Audio) - Generate lip-synced videos using OmniHuman 1.5.

Takes an image + audio file (or text for TTS) and generates realistic video with lip sync.
Uses bytedance/omni-human-1.5 on Replicate (~$0.16 per second of output).

Usage:
    # With audio file
    python animate_audio.py IMAGE AUDIO OUTPUT
    python animate_audio.py photo.png voice.mp3 output.mp4

    # With TTS (generates audio from text)
    python animate_audio.py IMAGE --tts "Hello world" OUTPUT
    python animate_audio.py photo.png --tts "Welcome to my channel" output.mp4 --voice Deep_Voice_Man
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


# Models
OMNI_HUMAN_MODEL = "bytedance/omni-human-1.5"
TTS_MODEL = "minimax/speech-02-turbo"

# Available TTS voices
TTS_VOICES = [
    "Deep_Voice_Man", "Calm_Woman", "Wise_Woman", "Friendly_Person",
    "Casual_Guy", "Lively_Girl", "Patient_Man", "Young_Knight",
    "Determined_Man", "Elegant_Man", "Sweet_Girl_2", "Exuberant_Girl"
]


def check_token():
    """Verify REPLICATE_API_TOKEN is set."""
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("ERROR: REPLICATE_API_TOKEN environment variable not set.")
        print("Get your token at: https://replicate.com/account/api-tokens")
        sys.exit(1)
    return token


def load_file_as_uri(file_path: str, file_type: str = "image") -> str:
    """Load file and return as data URI."""
    if file_path.startswith(("http://", "https://")):
        return file_path

    path = Path(file_path)
    if not path.exists():
        print(f"ERROR: {file_type.title()} file not found: {file_path}")
        sys.exit(1)

    suffix = path.suffix.lower()

    if file_type == "image":
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".gif": "image/gif",
        }
    else:  # audio
        mime_types = {
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".m4a": "audio/mp4",
            ".ogg": "audio/ogg",
            ".flac": "audio/flac",
        }

    mime_type = mime_types.get(suffix)
    if not mime_type:
        print(f"ERROR: Unsupported {file_type} format: {suffix}")
        print(f"Supported: {', '.join(mime_types.keys())}")
        sys.exit(1)

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{data}"


def get_audio_duration(audio_path: str) -> float:
    """Get audio duration in seconds (rough estimate from file size for mp3)."""
    if audio_path.startswith(("http://", "https://")):
        return 0  # Can't determine for URLs

    path = Path(audio_path)
    if not path.exists():
        return 0

    # Rough estimate: MP3 ~128kbps = 16KB/sec, WAV ~176KB/sec
    size_bytes = path.stat().st_size
    suffix = path.suffix.lower()

    if suffix == ".mp3":
        return size_bytes / 16000  # Rough estimate
    elif suffix == ".wav":
        return size_bytes / 176000  # Rough estimate
    else:
        return size_bytes / 20000  # Generic estimate


def generate_tts(text: str, voice: str = "Deep_Voice_Man", language: str = None, retries: int = 3) -> str:
    """Generate audio from text using TTS model."""
    token = os.environ.get("REPLICATE_API_TOKEN")
    url = f"https://api.replicate.com/v1/models/{TTS_MODEL}/predictions"

    input_data = {
        "text": text,
        "voice_id": voice,
        "emotion": "calm",
        "speed": 0.95,
    }

    if language:
        input_data["language_boost"] = language

    for attempt in range(retries):
        try:
            payload = json.dumps({"input": input_data}).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req) as response:
                prediction = json.loads(response.read().decode('utf-8'))
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            raise

    pred_id = prediction["id"]
    print(f"  TTS Prediction: {pred_id}")

    # Wait for TTS to complete
    poll_url = f"https://api.replicate.com/v1/predictions/{pred_id}"
    start = time.time()
    while time.time() - start < 120:
        req = urllib.request.Request(poll_url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))

        status = result.get("status")
        if status == "succeeded":
            return result["output"]
        elif status in ["failed", "canceled"]:
            raise Exception(f"TTS failed: {result.get('error')}")
        time.sleep(2)

    raise Exception("TTS timed out")


def create_prediction(image_uri: str, audio_uri: str, prompt: str = None, seed: int = None, fast_mode: bool = False, retries: int = 3) -> dict:
    """Create a prediction using direct HTTP API call with retry on rate limit."""
    token = os.environ.get("REPLICATE_API_TOKEN")
    url = f"https://api.replicate.com/v1/models/{OMNI_HUMAN_MODEL}/predictions"

    input_data = {
        "image": image_uri,
        "audio": audio_uri,
    }

    if prompt:
        input_data["prompt"] = prompt
    if seed is not None:
        input_data["seed"] = seed
    if fast_mode:
        input_data["fast_mode"] = True

    payload = json.dumps({"input": input_data}).encode('utf-8')

    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
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
    """Wait for prediction to complete (up to 10 minutes for longer videos)."""
    token = os.environ.get("REPLICATE_API_TOKEN")
    url = f"https://api.replicate.com/v1/predictions/{prediction_id}"

    start = time.time()
    last_status = None

    while time.time() - start < timeout:
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {token}"}
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print(f"Warning: Status check failed: {e.code}")
            time.sleep(5)
            continue

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


def download_video(url: str, output_path: str) -> bool:
    """Download video from URL to local file."""
    try:
        print(f"Downloading video...")
        with urllib.request.urlopen(url) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"ERROR: Failed to download video: {e}")
        return False


def animate_audio(
    input_image: str,
    input_audio: str = None,
    output_path: str = None,
    prompt: str = None,
    seed: int = None,
    fast_mode: bool = False,
    tts_text: str = None,
    tts_voice: str = "Deep_Voice_Man",
) -> str:
    """Generate lip-synced video using OmniHuman 1.5."""

    check_token()

    # Load image
    print(f"Loading image: {input_image}")
    image_uri = load_file_as_uri(input_image, "image")

    # Get audio - either from file or TTS
    if tts_text:
        print(f"\nGenerating TTS audio...")
        print(f"  Text: \"{tts_text}\"")
        print(f"  Voice: {tts_voice}")
        audio_uri = generate_tts(tts_text, tts_voice)
        print(f"  Audio URL: {audio_uri}")
        est_duration = len(tts_text) / 15  # Rough estimate: 15 chars/sec
    else:
        # Load audio file
        print(f"Loading audio: {input_audio}")
        audio_uri = load_file_as_uri(input_audio, "audio")

    # Estimate duration and cost
    if not tts_text:
        est_duration = get_audio_duration(input_audio)

    if est_duration > 0:
        est_cost = est_duration * 0.16
        print(f"\nEstimated duration: ~{est_duration:.1f}s")
        print(f"Estimated cost: ~${est_cost:.2f}")

        if est_duration > 35:
            print("WARNING: Audio exceeds 35 second limit. It will be truncated.")

    if prompt:
        print(f"Prompt: {prompt}")
    if fast_mode:
        print("Fast mode: enabled (faster but lower quality)")

    # Create prediction
    print(f"\nStarting OmniHuman 1.5 generation...")
    prediction = create_prediction(
        image_uri=image_uri,
        audio_uri=audio_uri,
        prompt=prompt,
        seed=seed,
        fast_mode=fast_mode,
    )

    prediction_id = prediction.get("id")
    if not prediction_id:
        print(f"ERROR: Failed to create prediction: {prediction}")
        sys.exit(1)

    print(f"Prediction ID: {prediction_id}")

    # Check if already completed (sync mode)
    if prediction.get("status") == "succeeded" and prediction.get("output"):
        result = prediction
    else:
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
    if download_video(output_url, output_path):
        file_size = Path(output_path).stat().st_size / (1024 * 1024)
        print(f"\nSUCCESS: Video saved to {output_path}")
        print(f"File size: {file_size:.1f} MB")
        return output_path
    else:
        print(f"Video URL (download manually): {output_url}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate lip-synced videos using OmniHuman 1.5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  # With audio file
  %(prog)s photo.png voice.mp3 output.mp4
  %(prog)s photo.png speech.wav talking.mp4 --prompt "slight nod while speaking"

  # With TTS (text-to-speech)
  %(prog)s photo.png --tts "Hello, welcome to my channel" output.mp4
  %(prog)s photo.png --tts "Breaking news" output.mp4 --voice Determined_Man

Available voices: {', '.join(TTS_VOICES)}

Cost: ~$0.16 per second of output video (+ ~$0.001/sec for TTS)
      10 second video = ~$1.60

Audio limit: 35 seconds max
"""
    )

    parser.add_argument("image", help="Input image path or URL")
    parser.add_argument("audio", nargs="?", help="Input audio path or URL (MP3, WAV)")
    parser.add_argument("output", nargs="?", help="Output video path (.mp4)")
    parser.add_argument(
        "--tts", "-t",
        metavar="TEXT",
        help="Generate audio from text (instead of audio file)"
    )
    parser.add_argument(
        "--voice", "-v",
        default="Deep_Voice_Man",
        choices=TTS_VOICES,
        help="TTS voice (default: Deep_Voice_Man)"
    )
    parser.add_argument(
        "--prompt", "-p",
        help="Optional prompt for movement/camera control"
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        help="Random seed for reproducible results"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Enable fast mode (faster but lower quality)"
    )

    args = parser.parse_args()

    # Handle TTS mode vs audio file mode
    if args.tts:
        if not args.output:
            # In TTS mode, second positional arg is output
            args.output = args.audio
        animate_audio(
            input_image=args.image,
            output_path=args.output,
            prompt=args.prompt,
            seed=args.seed,
            fast_mode=args.fast,
            tts_text=args.tts,
            tts_voice=args.voice,
        )
    else:
        if not args.audio or not args.output:
            parser.error("audio and output are required when not using --tts")
        animate_audio(
            input_image=args.image,
            input_audio=args.audio,
            output_path=args.output,
            prompt=args.prompt,
            seed=args.seed,
            fast_mode=args.fast,
        )


if __name__ == "__main__":
    main()
