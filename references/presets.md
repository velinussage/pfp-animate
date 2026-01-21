# Motion Presets Reference

## Video Mode Presets (animate_pfp.py)

These presets use AI-generated motion via Kling v2.5 Turbo Pro.

| Preset | Prompt Used | Best For |
|--------|-------------|----------|
| `nod` | "The subject gently nods their head in acknowledgment, subtle and natural movement, maintaining eye contact" | Agreement, acknowledgment |
| `wave` | "The subject waves hello with a friendly gesture, natural arm and hand movement, warm expression" | Greetings, friendly reactions |
| `laugh` | "The subject laughs naturally, eyes crinkling with joy, shoulders moving slightly, genuine amusement" | Reactions, humor |
| `think` | "The subject tilts their head thoughtfully to one side, considering something, subtle chin movement" | Contemplation, pondering |
| `surprise` | "The subject reacts with mild surprise, eyebrows raising, eyes widening slightly, mouth opening a bit" | Reactions, reveals |
| `idle` | "The subject breathes naturally with very subtle movement, slight head sway, almost still but alive" | Ambient, background |
| `talking` | "The subject is speaking, natural lip movement, subtle facial expressions while talking" | Speaking animations |
| `wink` | "The subject gives a playful wink with one eye, slight smile, charming expression" | Playful, flirty |

### Usage
```bash
python scripts/animate_pfp.py image.png output.mp4 --motion nod
```

---

## Keyframe Mode Presets (animate_keyframe.py)

These presets use precise parameter control via expression-editor.

| Preset | Description | Frames | Parameters |
|--------|-------------|--------|------------|
| `nod` | Clear nodding yes motion | 8 | rotate_pitch: 0 → -15 → 5 → 0 |
| `wink` | Playful wink with smile | 8 | wink: 0 → 25 → 0, smile: 0 → 1 |
| `shake_no` | Shaking head no | 10 | rotate_yaw: 0 → -15 → 15 → 0 |
| `nod_wink` | Nod followed by wink | 10 | pitch nod then wink sequence |
| `look_around` | Looking left then right | 10 | rotate_yaw + pupil_x movement |
| `surprise` | Surprised expression | 8 | eyebrow up, eyes wide, mouth open |
| `laugh` | Laughing with head tilt | 10 | smile + pitch + eyebrow movement |

### Usage
```bash
python scripts/animate_keyframe.py image.png output.gif --motion nod_wink
```

---

## Choosing Between Modes

| Criteria | Video Mode | Keyframe Mode |
|----------|------------|---------------|
| **Output format** | MP4 video | GIF animation |
| **Motion type** | AI-generated, cinematic | Precise, repeatable |
| **Control level** | Prompt-based | Parameter-based |
| **Cost** | ~$0.35/video | ~$0.02/animation |
| **Best for** | Natural movement | Exact gestures |
| **Body movement** | Full body possible | Face only |

**Rule of thumb:**
- Need specific gesture (nod yes, wink) → Keyframe mode
- Want cinematic feel → Video mode
- Budget conscious → Keyframe mode
- Full body needed → Video mode
