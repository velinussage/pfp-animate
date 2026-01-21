# PFP Animate

Claude Code skill to generate animated videos from static profile pictures using AI.

## Installation

```bash
# Clone and add to Claude Code
git clone https://github.com/velinussage/pfp-animate.git
```

Then add the skill directory to your Claude Code settings.

## Requirements

- Python 3.9+
- [Replicate API token](https://replicate.com/account/api-tokens) with billing enabled
- PIL/Pillow (`brew install pillow` on macOS)

## Quick Start

```bash
# Set your Replicate token
export REPLICATE_API_TOKEN="r8_your_token_here"

# Animate with preset
python scripts/animate_pfp.py image.png output.mp4 --motion nod

# Keyframe mode (precise gestures)
python scripts/animate_keyframe.py image.png output.gif --motion nod_wink
```

## Structure

```
pfp-animate/
├── SKILL.md              # Claude Code skill definition
├── scripts/
│   ├── animate_pfp.py    # Video mode (Kling v2.5)
│   ├── animate_keyframe.py # Keyframe mode (expression-editor)
│   └── presets.json      # Motion preset definitions
├── workflows/
│   ├── setup.md          # Replicate account setup
│   ├── animate.md        # Video animation workflow
│   └── keyframe.md       # Keyframe animation workflow
└── references/
    ├── presets.md        # Motion preset docs
    ├── pricing.md        # API costs
    └── troubleshooting.md
```

## Presets

| Preset | Description |
|--------|-------------|
| `nod` | Head nod |
| `wave` | Friendly wave |
| `wink` | Playful wink |
| `laugh` | Laughing |
| `shake_no` | Head shake |
| `nod_wink` | Nod + wink combo |

## Pricing

- Video (5s): ~$0.35
- Video (10s): ~$0.70
- Keyframe (10 frames): ~$0.02

## License

MIT
