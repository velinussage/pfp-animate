# API Pricing Reference

## Veo 3.1 (Recommended - Video + Generated Audio)

**Rate:**
- With audio: ~$0.40 per second
- Without audio: ~$0.20 per second

| Duration | With Audio | Without Audio |
|----------|------------|---------------|
| 4 seconds | ~$1.60 | ~$0.80 |
| 6 seconds | ~$2.40 | ~$1.20 |
| 8 seconds | ~$3.20 | ~$1.60 |

**Features:**
- Generates video AND synchronized audio from text prompt
- Include speech in quotes: `says "Hello world"`
- Reference images for character consistency
- 720p or 1080p resolution
- 16:9 or 9:16 aspect ratio

---

## OmniHuman 1.5 (Lip-Sync to Existing Audio)

**Rate:** ~$0.16 per second of output video

| Duration | Approximate Cost |
|----------|------------------|
| 5 seconds | ~$0.80 |
| 10 seconds | ~$1.60 |
| 30 seconds | ~$4.80 |

**Features:**
- Lip-synced video from image + audio file
- Supports MP3, WAV audio (max 35 seconds)
- Optional TTS generation (~$0.001/sec extra)
- Fast mode available

---

## Kling v2.5 Turbo Pro (Silent Video)

**Rate:** ~$0.07 per second of output video

| Duration | Approximate Cost |
|----------|------------------|
| 5 seconds | ~$0.35 |
| 10 seconds | ~$0.70 |

**Features:**
- Video from image + text prompt (no audio)
- Motion presets available
- Good for gestures, movement

---

## Expression-Editor (Keyframe Mode)

**Rate:** ~$0.002 per frame

| Preset | Frames | Approximate Cost |
|--------|--------|------------------|
| nod | 10 | ~$0.020 |
| wink | 10 | ~$0.020 |
| scared_scream | 12 | ~$0.024 |
| nod_wink | 10 | ~$0.020 |

**Features:**
- Precise facial expression control
- GIF output
- Custom keyframes supported

---

## Model Comparison

| Model | Audio | Duration | Cost | Best For |
|-------|-------|----------|------|----------|
| Veo 3.1 | Generated | 4-8s | $1.60-$3.20 | Speaking videos, announcements |
| OmniHuman 1.5 | Lip-sync | Up to 35s | ~$0.16/s | Sync to specific audio |
| Kling v2.5 | None | 5-10s | ~$0.35-$0.70 | Silent motion, gestures |
| Expression-editor | None | ~1s GIF | ~$0.02 | Precise facial control |

**Veo 3.1** is best for speaking videos with AI-generated voice.
**OmniHuman** is best when you have specific audio to lip-sync.
**Keyframe** is cheapest for simple facial animations.

---

## Budget Examples

**$10 credit gets you approximately:**
- 3 Veo 3.1 videos (8s with audio), OR
- 6 OmniHuman videos (10s each), OR
- 28 Kling videos (5s each), OR
- 500 keyframe animations

---

## Rate Limits

| Credit Balance | Rate Limit |
|---------------|------------|
| < $5 | 6 requests/minute |
| ≥ $5 | Higher limits |

Scripts include built-in retry logic for rate limits.

---

## Monitoring Usage

- Usage: https://replicate.com/account/usage
- Billing: https://replicate.com/account/billing
