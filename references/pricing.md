# API Pricing Reference

## Kling v2.5 Turbo Pro (Video Mode)

**Rate:** ~$0.07 per second of output video

| Duration | Approximate Cost |
|----------|------------------|
| 5 seconds | ~$0.35 |
| 10 seconds | ~$0.70 |

**Factors affecting cost:**
- Duration is the main factor
- Aspect ratio doesn't significantly affect price
- Failed generations are not charged

---

## Expression-Editor (Keyframe Mode)

**Rate:** ~$0.002 per frame

| Preset | Frames | Approximate Cost |
|--------|--------|------------------|
| nod | 8 | ~$0.016 |
| wink | 8 | ~$0.016 |
| shake_no | 10 | ~$0.020 |
| nod_wink | 10 | ~$0.020 |
| look_around | 10 | ~$0.020 |

---

## Cost Comparison

| Animation Type | Cost | Output |
|---------------|------|--------|
| 5s video (Kling) | ~$0.35 | MP4 |
| 10-frame keyframe | ~$0.02 | GIF |

**Keyframe is ~17x cheaper** for simple facial animations.

---

## Budget Examples

**$5 credit gets you approximately:**
- 14 five-second videos, OR
- 7 ten-second videos, OR
- 250 keyframe animations

**$10 credit gets you approximately:**
- 28 five-second videos, OR
- 14 ten-second videos, OR
- 500 keyframe animations

---

## Rate Limits

| Credit Balance | Rate Limit |
|---------------|------------|
| < $5 | 6 requests/minute |
| ≥ $5 | Higher limits |

The keyframe script includes built-in delays to respect rate limits.

---

## Monitoring Usage

Check your current usage:
https://replicate.com/account/usage

Check your credit balance:
https://replicate.com/account/billing
