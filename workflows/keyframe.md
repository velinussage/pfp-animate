# Workflow: Keyframe Animation (Precise Gestures)

Generate GIF animations with precise control over facial expressions using expression-editor.

<when_to_use>
Use keyframe mode when you need:
- **Exact gestures**: specific nod, wink, head shake
- **Precise timing**: control over each frame
- **Consistent results**: same motion every time
- **Lower cost**: ~$0.02 for 10 frames vs ~$0.35 for video

Use video mode (`workflows/animate.md`) when you want:
- Cinematic, AI-generated motion
- Full body movement
- More natural, varied results
</when_to_use>

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

Get the path to the image:
- Best for: portraits, profile pictures, character art
- Face should be clearly visible
- Works with any aspect ratio

Ask user: "What image do you want to animate?"
</step_1>

<step_2>
**Choose Keyframe Preset**

Available presets:

| Preset | Description | Frames |
|--------|-------------|--------|
| `nod` | Clear nodding yes motion | 8 |
| `wink` | Playful wink with smile | 8 |
| `shake_no` | Shaking head no | 10 |
| `nod_wink` | Nod followed by wink | 10 |
| `look_around` | Looking left then right | 10 |
| `surprise` | Surprised expression | 8 |
| `laugh` | Laughing with head tilt | 10 |

```bash
python scripts/animate_keyframe.py INPUT OUTPUT.gif --motion PRESET
```
</step_2>

<step_3>
**Run Keyframe Animation**

Execute the command:
```bash
python scripts/animate_keyframe.py INPUT.png OUTPUT.gif --motion nod_wink
```

Generation time: ~15-20 seconds per frame (2-3 minutes total for 10 frames)

The script shows progress for each frame.
</step_3>

<step_4>
**Verify Output**

Check the generated GIF:
```bash
ls -lh OUTPUT.gif
```

Preview the animation to verify the gesture matches expectations.
</step_4>

</process>

<examples>

**Simple nod:**
```bash
python scripts/animate_keyframe.py pfp.png nod.gif --motion nod
```

**Nod followed by wink:**
```bash
python scripts/animate_keyframe.py avatar.png nod_wink.gif --motion nod_wink
```

**Head shake (no):**
```bash
python scripts/animate_keyframe.py photo.jpg shake.gif --motion shake_no
```

</examples>

<advanced>
**Custom keyframes** (for developers):

Edit `scripts/animate_keyframe.py` to create custom presets. Available parameters:
- `rotate_pitch`: head tilt up/down (-20 to 20)
- `rotate_yaw`: head turn left/right (-20 to 20)
- `rotate_roll`: head tilt side to side (-20 to 20)
- `wink`: wink amount (0 to 25)
- `smile`: smile intensity (0 to 1.3)
- `blink`: blink amount (-20 to 5)
- `eyebrow`: eyebrow raise (-10 to 15)
- `pupil_x`: eye look left/right (-15 to 15)
- `pupil_y`: eye look up/down (-15 to 15)
- `aaa`: mouth open amount (0 to 1)
</advanced>

<troubleshooting>
**"Rate limited" or 429 error**
→ Account has <$5 credit (6 req/min limit). Add more credits or wait.

**Frames look distorted**
→ Try a clearer input image with visible face

**Animation too fast/slow**
→ Adjust `fps` parameter in preset (default: 10-12)

See `references/troubleshooting.md` for more solutions.
</troubleshooting>

<success_criteria>
- [ ] Input image located and accessible
- [ ] Keyframe command executed without errors
- [ ] Output GIF file created
- [ ] Animation shows expected gesture
</success_criteria>
