# PFP Animate

Generate animated videos from static profile pictures (PFPs) using AI. Transform any image into a short, expressive video with customizable motions.

## Quick Start

1. **Setup Replicate** (one-time)
   - Create account at https://replicate.com
   - Get API token from https://replicate.com/account/api-tokens
   - Add credits at https://replicate.com/account/billing
   - Set environment variable:
     ```bash
     export REPLICATE_API_TOKEN="r8_your_token_here"
     ```

2. **Animate an image**
   ```bash
   python scripts/animate_pfp.py image.png output.mp4 --motion nod
   ```

## Two Animation Modes

### Video Mode (MP4)
AI-generated cinematic motion using Kling v2.5 Turbo Pro.

```bash
python scripts/animate_pfp.py image.png output.mp4 --motion wave
python scripts/animate_pfp.py image.png output.mp4 --prompt "slowly winking"
```

**Options:** `--duration 5|10`, `--aspect 1:1|16:9|9:16`, `--guidance 0.0-1.0`

### Keyframe Mode (GIF)
Precise facial expression control using expression-editor.

```bash
python scripts/animate_keyframe.py image.png output.gif --motion nod_wink
```

**Presets:** `nod`, `wink`, `shake_no`, `nod_wink`, `look_around`, `surprise`, `laugh`

## Motion Presets

| Preset | Description | Mode |
|--------|-------------|------|
| `nod` | Subtle head nod | Both |
| `wave` | Friendly wave | Video |
| `wink` | Playful wink | Both |
| `laugh` | Laughing expression | Both |
| `think` | Thoughtful head tilt | Video |
| `surprise` | Surprised reaction | Both |
| `shake_no` | Shaking head no | Keyframe |
| `nod_wink` | Nod followed by wink | Keyframe |

## Pricing

| Mode | Cost | Output |
|------|------|--------|
| Video (5s) | ~$0.35 | MP4 |
| Video (10s) | ~$0.70 | MP4 |
| Keyframe (10 frames) | ~$0.02 | GIF |

## Skill Structure

```
pfp-animate/
├── SKILL.md                    # Claude Code skill (intake menu + routing)
├── scripts/
│   ├── animate_pfp.py          # Video mode (Kling v2.5)
│   ├── animate_keyframe.py     # Keyframe mode (expression-editor)
│   └── presets.json            # Motion preset definitions
├── workflows/
│   ├── setup.md                # Replicate account setup guide
│   ├── animate.md              # Video animation workflow
│   └── keyframe.md             # Keyframe animation workflow
└── references/
    ├── presets.md              # Full preset documentation
    ├── pricing.md              # Cost reference
    └── troubleshooting.md      # Common issues and fixes
```

## As a Claude Code Skill

Install and use with Claude Code:

```bash
# Install skill
scroll skill add /path/to/pfp-animate

# Then just ask Claude:
"Animate my profile picture with a wink"
"Create a nodding video from ~/Downloads/avatar.png"
```

## Requirements

- Python 3.9+
- Replicate API token (with billing set up)
- PIL/Pillow (for keyframe mode)

```bash
# macOS
brew install pillow

# Or create venv
python3 -m venv .venv && source .venv/bin/activate
pip install pillow
```

## License

MIT

## Credits

- [Replicate](https://replicate.com/) - AI model hosting
- [Kling v2.5 Turbo Pro](https://replicate.com/kwaivgi/kling-v2.5-turbo-pro) - Video generation
- [expression-editor](https://replicate.com/fofr/expression-editor) - Facial expression control
