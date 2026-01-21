# Workflow: Veo 3.1 (Video + Generated Audio)

Generate videos with synchronized AI-generated audio using Google Veo 3.1.

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
- Supported formats: PNG, JPG, JPEG, WEBP
- Best results: Clear subject, good lighting, high resolution
- Face should be visible for speaking animations

Ask user: "What image do you want to animate?"
</step_1>

<step_2>
**Write the Prompt**

Veo 3.1 generates both video AND audio from your prompt. Include:

**Motion description:**
- "person speaks to camera"
- "slowly pulls down face covering, then speaks"
- "waves hello with a smile"

**Speech content (in quotes):**
- `person says "Hello, welcome to my channel"`
- `announces "Video generation coming soon"`

**Audio cues:**
- "with desert wind in background"
- "upbeat music playing"
- "calm narration voice"

**Camera movements:**
- "camera slowly zooms in"
- "medium shot, then close-up"

**Example prompts:**
```
"A man in desert clothing slowly reveals his face, then speaks
confidently to camera saying 'Velinus here. Video generation skills
coming soon to Sage Protocol.' Desert background, warm lighting."

"Person waves hello and says 'Welcome to my channel!' with
enthusiasm, slight head movements, friendly expression."
```
</step_2>

<step_3>
**Configure Options**

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--duration` | 4, 6, 8 | 8 | Video length in seconds |
| `--resolution` | 720p, 1080p | 1080p | Output resolution |
| `--aspect` | 16:9, 9:16 | 9:16 | Aspect ratio |
| `--no-audio` | flag | - | Disable audio (cheaper) |
| `--reference` | image(s) | - | Reference images for consistency |
| `--end-image` | image | - | End frame for transitions |

**Cost estimation:**
- With audio: ~$0.40/second ($3.20 for 8s)
- Without audio: ~$0.20/second ($1.60 for 8s)
</step_3>

<step_4>
**Run Generation**

**Basic command:**
```bash
python scripts/animate_veo.py IMAGE OUTPUT.mp4 --prompt "your prompt here"
```

**With reference image for character consistency:**
```bash
python scripts/animate_veo.py IMAGE OUTPUT.mp4 \
  --prompt "person speaks to camera" \
  --reference IMAGE
```

**Portrait video for social media:**
```bash
python scripts/animate_veo.py IMAGE OUTPUT.mp4 \
  --prompt "person announces something exciting" \
  --aspect 9:16 \
  --duration 8
```

Generation typically takes 2-3 minutes.
</step_4>

<step_5>
**Verify Output**

Check the generated video:
```bash
ls -lh OUTPUT.mp4
```

Play to verify:
- Video matches prompt description
- Audio is clear and synchronized
- No artifacts or distortions
</step_5>

</process>

<examples>

**Speaking announcement:**
```bash
python scripts/animate_veo.py ~/Downloads/pfp.png ~/Downloads/announcement.mp4 \
  --prompt "Person looks at camera and says 'Big news coming soon. Stay tuned.' with confident expression, slight head movements"
```

**Character introduction with reference:**
```bash
python scripts/animate_veo.py avatar.png intro.mp4 \
  --prompt "Character waves and introduces themselves saying 'Hey everyone, welcome!'" \
  --reference avatar.png
```

**Dramatic reveal:**
```bash
python scripts/animate_veo.py masked.png reveal.mp4 \
  --prompt "Person slowly removes mask, revealing face, then speaks mysteriously" \
  --duration 8 --aspect 16:9
```

**Silent video (cheaper):**
```bash
python scripts/animate_veo.py photo.png silent.mp4 \
  --prompt "Person nods thoughtfully, slight smile" \
  --no-audio
```

</examples>

<troubleshooting>
**"REPLICATE_API_TOKEN not set"**
→ Run `workflows/setup.md`

**"insufficient credit"**
→ Add credits at https://replicate.com/account/billing (Veo 3.1 costs ~$3.20/8s)

**Speech not clear**
→ Put speech in quotes: `says "exact words here"`

**Character looks different**
→ Use `--reference IMAGE` to maintain consistency

**Rate limited**
→ Script auto-retries. Add credits for higher limits.

See `references/troubleshooting.md` for more solutions.
</troubleshooting>

<success_criteria>
- [ ] Input image located and accessible
- [ ] Prompt describes motion, speech, and audio
- [ ] Video generated without errors
- [ ] Audio synchronized with video
</success_criteria>
