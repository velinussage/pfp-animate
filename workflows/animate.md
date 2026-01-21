# Workflow: Animate Image (Video Mode)

Generate animated MP4 videos from static images using Kling v2.5 Turbo Pro.

<prerequisites>
**Verify before starting:**
```bash
echo $REPLICATE_API_TOKEN | head -c 10
```
If empty, complete `workflows/setup.md` first.
</prerequisites>

<process>

<step_1>
**Locate Input Image**

Get the path to the image you want to animate:
- Supported formats: PNG, JPG, JPEG, GIF, WEBP
- Best results: Clear subject/face, portrait orientation
- Can also use a URL instead of local path

Ask user: "What image do you want to animate? Provide the file path or URL."
</step_1>

<step_2>
**Choose Animation Type**

**Option A: Use a preset motion**
```bash
python scripts/animate_pfp.py INPUT OUTPUT.mp4 --motion PRESET
```

Available presets: `nod`, `wave`, `laugh`, `think`, `surprise`, `idle`, `talking`, `wink`

See `references/presets.md` for full descriptions.

**Option B: Custom prompt**
```bash
python scripts/animate_pfp.py INPUT OUTPUT.mp4 --prompt "your description here"
```

Tips for custom prompts:
- Focus on motion, not appearance
- Be specific: "slowly nodding yes" not just "nodding"
- Keep it simple: one or two actions work best
</step_2>

<step_3>
**Configure Options (Optional)**

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--duration` | 5, 10 | 5 | Video length in seconds |
| `--aspect` | 1:1, 16:9, 9:16 | 1:1 | Output aspect ratio |
| `--guidance` | 0.0-1.0 | 0.5 | Prompt adherence (higher = stricter) |
| `--negative` | text | none | Things to avoid |

**Example with options:**
```bash
python scripts/animate_pfp.py photo.png video.mp4 \
  --motion wave \
  --duration 5 \
  --aspect 1:1 \
  --guidance 0.7
```
</step_3>

<step_4>
**Run Animation**

Execute the command and wait for generation (30-120 seconds typically).

```bash
python scripts/animate_pfp.py INPUT OUTPUT.mp4 --motion PRESET
```

The script will show:
- Loading progress
- Generation status
- Download progress
- Final output path
</step_4>

<step_5>
**Verify Output**

Check the generated video:
```bash
ls -lh OUTPUT.mp4
```

If the video doesn't match expectations:
- Try higher `--guidance` (0.7-0.9) for better prompt adherence
- Use simpler, more specific prompts
- For precise gestures, use keyframe mode instead (`workflows/keyframe.md`)
</step_5>

</process>

<examples>

**Basic nod animation:**
```bash
python scripts/animate_pfp.py ~/Downloads/pfp.png ~/Downloads/pfp_nod.mp4 --motion nod
```

**Waving with longer duration:**
```bash
python scripts/animate_pfp.py avatar.png wave.mp4 --motion wave --duration 10
```

**Custom prompt with high guidance:**
```bash
python scripts/animate_pfp.py photo.jpg custom.mp4 \
  --prompt "slowly turning head left, then right, curious expression" \
  --guidance 0.8
```

**Vertical video for social media:**
```bash
python scripts/animate_pfp.py pfp.png story.mp4 --motion laugh --aspect 9:16
```

</examples>

<troubleshooting>
**"REPLICATE_API_TOKEN not set"**
→ Run `workflows/setup.md`

**"insufficient credit"**
→ Add credits at https://replicate.com/account/billing

**Video doesn't match prompt**
→ Try `--guidance 0.8` or use keyframe mode for precise control

**Generation taking too long**
→ Normal is 30-120s. Check Replicate status page if >3 minutes.

See `references/troubleshooting.md` for more solutions.
</troubleshooting>

<success_criteria>
- [ ] Input image located and accessible
- [ ] Animation command executed without errors
- [ ] Output MP4 file created at specified path
- [ ] Video shows expected motion
</success_criteria>
