# Workflow: Audio Animation (Lip-Sync Mode)

Generate lip-synced MP4 videos from static images + audio using OmniHuman 1.5.

<prerequisites>
**Verify before starting:**
```bash
echo $REPLICATE_API_TOKEN | head -c 10
```
If empty, complete `workflows/setup.md` first.
</prerequisites>

<process>

<step_1>
**Locate Input Files**

You need TWO inputs:
1. **Image**: PNG, JPG, JPEG, or WEBP with a clear face
2. **Audio**: MP3 or WAV file (max 35 seconds)

Ask user: "What image and audio file do you want to combine? Provide both file paths."

**Tips:**
- Face should be clearly visible and forward-facing
- Audio quality affects lip-sync accuracy
- Shorter clips (<10s) are more cost-effective
</step_1>

<step_2>
**Estimate Cost**

**Pricing**: ~$0.16 per second of output video

| Duration | Cost |
|----------|------|
| 5 seconds | ~$0.80 |
| 10 seconds | ~$1.60 |
| 30 seconds | ~$4.80 |

The script automatically estimates cost based on audio length.
</step_2>

<step_3>
**Configure Options (Optional)**

| Option | Description |
|--------|-------------|
| `--prompt` | Movement/camera control (e.g., "slight head nod while speaking") |
| `--fast` | Faster generation, slightly lower quality |
| `--seed` | Fixed seed for reproducible results |

**Movement prompt tips:**
- Keep it simple: "subtle head movements", "slight nod"
- The model handles lip-sync automatically
- Prompts control body/head motion, not speech
</step_3>

<step_4>
**Run Animation**

**Basic command:**
```bash
python scripts/animate_audio.py IMAGE AUDIO OUTPUT.mp4
```

**With movement prompt:**
```bash
python scripts/animate_audio.py IMAGE AUDIO OUTPUT.mp4 --prompt "gentle head movements"
```

**Fast mode for testing:**
```bash
python scripts/animate_audio.py IMAGE AUDIO OUTPUT.mp4 --fast
```

Generation time: ~1-3 minutes depending on audio length.
</step_4>

<step_5>
**Verify Output**

Check the generated video:
```bash
ls -lh OUTPUT.mp4
```

Play the video to verify:
- Lip movements match audio
- Head/body movements look natural
- No artifacts or distortions
</step_5>

</process>

<examples>

**Basic lip-sync:**
```bash
python scripts/animate_audio.py ~/Downloads/pfp.png ~/Downloads/voice.mp3 ~/Downloads/talking.mp4
```

**With subtle movements:**
```bash
python scripts/animate_audio.py avatar.png narration.mp3 video.mp4 \
  --prompt "slight head tilts and nods while speaking"
```

**Fast mode for quick test:**
```bash
python scripts/animate_audio.py photo.jpg test.mp3 quick.mp4 --fast
```

**Reproducible result:**
```bash
python scripts/animate_audio.py pfp.png speech.wav output.mp4 --seed 42
```

</examples>

<troubleshooting>
**"REPLICATE_API_TOKEN not set"**
→ Run `workflows/setup.md`

**"insufficient credit"**
→ Add credits at https://replicate.com/account/billing

**Audio truncated**
→ OmniHuman 1.5 has 35 second max. Split longer audio.

**Lip sync looks off**
→ Try cleaner audio, or ensure face is clearly visible in image

**Generation taking too long**
→ Normal is 1-3 minutes. Use `--fast` for quicker results.

See `references/troubleshooting.md` for more solutions.
</troubleshooting>

<success_criteria>
- [ ] Input image and audio files located
- [ ] Animation command executed without errors
- [ ] Output MP4 file created at specified path
- [ ] Video has lip-synced audio
</success_criteria>
