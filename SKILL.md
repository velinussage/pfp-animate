---
name: pfp-animate
description: Generate animated videos from static profile pictures using AI. Use when users want to animate images, create PFP videos, make meme videos, or turn portraits into short clips. Supports motion presets (nod, wave, wink) and custom prompts.
---

<overview>
PFP Animate generates 5-10 second animated videos from static images using Kling v2.5 Turbo Pro on Replicate.

**Two animation modes:**
- **Video mode**: AI-generated motion from text prompts (cinematic, flexible)
- **Keyframe mode**: Precise facial expression control (nod, wink, exact gestures)

**Requires**: `REPLICATE_API_TOKEN` environment variable
</overview>

<check_setup>
**Before any animation, verify setup:**
```bash
# Check if token is configured
echo $REPLICATE_API_TOKEN | head -c 10
```

If empty or missing, route to `workflows/setup.md`.
</check_setup>

<intake>
What would you like to do?

1. **Setup Replicate** - Create account, get API token, configure environment
2. **Animate an image** - Generate video from a local image file
3. **Use a motion preset** - Quick animation with predefined motions (nod, wave, wink)
4. **Custom animation** - Describe exactly what motion you want
5. **Keyframe animation** - Precise control over facial expressions (GIF output)
6. **List presets** - See all available motion presets

**Wait for user response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "setup", "install", "token", "account" | `workflows/setup.md` |
| 2, "animate", "video", "image" | `workflows/animate.md` |
| 3, "preset", "nod", "wave", "wink", "laugh" | `workflows/animate.md` (with preset) |
| 4, "custom", "prompt", "describe" | `workflows/animate.md` (with custom prompt) |
| 5, "keyframe", "precise", "expression", "gif" | `workflows/keyframe.md` |
| 6, "list", "presets", "options" | Show presets from `references/presets.md` |

**After reading the workflow, follow it exactly.**
</routing>

<quick_reference>
**Animate with preset:**
```bash
python scripts/animate_pfp.py INPUT.png OUTPUT.mp4 --motion nod
```

**Animate with custom prompt:**
```bash
python scripts/animate_pfp.py INPUT.png OUTPUT.mp4 --prompt "slowly winking and smiling"
```

**Keyframe animation (precise gestures):**
```bash
python scripts/animate_keyframe.py INPUT.png OUTPUT.gif --motion nod_wink
```

**Options:**
- `--duration 5|10` - Video length in seconds
- `--aspect 1:1|16:9|9:16` - Output aspect ratio
- `--guidance 0.0-1.0` - Prompt adherence (higher = stricter)
</quick_reference>

<reference_index>
**Presets:** `references/presets.md` - All motion presets with descriptions
**Troubleshooting:** `references/troubleshooting.md` - Common errors and fixes
**API Costs:** `references/pricing.md` - Replicate pricing reference
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| setup.md | Create Replicate account and configure API token |
| animate.md | Generate video from image using Kling v2.5 |
| keyframe.md | Precise facial expression control with expression-editor |
</workflows_index>

<success_criteria>
- Replicate API token configured (`echo $REPLICATE_API_TOKEN` shows value)
- Can run animation script without errors
- Output video/GIF saved to specified path
</success_criteria>
