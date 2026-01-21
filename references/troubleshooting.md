# Troubleshooting Guide

## Setup Issues

### "REPLICATE_API_TOKEN environment variable not set"

**Cause:** Token not configured in environment.

**Fix:**
```bash
export REPLICATE_API_TOKEN="r8_your_token_here"
```

For persistent setup, add to `~/.zshrc` or `~/.bashrc`:
```bash
echo 'export REPLICATE_API_TOKEN="r8_your_token"' >> ~/.zshrc
source ~/.zshrc
```

### Token set but still getting auth errors

**Check 1:** Verify token is correct
```bash
echo $REPLICATE_API_TOKEN
```
Should start with `r8_`

**Check 2:** Test API connection
```bash
curl -s -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/account
```
Should return JSON, not an error.

**Check 3:** Token may have expired or been revoked
→ Generate new token at https://replicate.com/account/api-tokens

---

## Billing Issues

### "insufficient credit" or payment required

**Cause:** Replicate account has no credits.

**Fix:**
1. Go to https://replicate.com/account/billing
2. Add a payment method
3. Add credits ($5-10 recommended)

### Rate limited (429 errors)

**Cause:** Accounts with <$5 credit have 6 requests/minute limit.

**Fix:**
- Add more credits to increase rate limit
- Wait 60 seconds between requests
- The keyframe script has built-in rate limiting

---

## Generation Issues

### Video doesn't match prompt

**Possible causes:**
1. Prompt too vague
2. Guidance scale too low
3. Model limitations

**Fixes:**
- Use higher guidance: `--guidance 0.8`
- Be more specific in prompt
- For precise gestures, use keyframe mode instead
- Add negative prompt: `--negative "distortion, blur"`

### Generation takes too long (>3 minutes)

**Normal:** 30-120 seconds for video mode

**If stuck:**
- Check https://replicate.com/status for outages
- Try again later
- Reduce duration to 5 seconds

### Output video is blank or corrupted

**Possible causes:**
- Network issue during download
- Disk full

**Fixes:**
```bash
# Check disk space
df -h

# Re-run the command
python scripts/animate_pfp.py ...
```

### Keyframe animation looks distorted

**Possible causes:**
- Input image quality
- Face not clearly visible
- Extreme parameter values

**Fixes:**
- Use higher quality input image
- Ensure face is front-facing and well-lit
- Try a different preset

---

## Python Issues

### "No module named 'replicate'" or PIL errors

**Note:** The scripts use direct HTTP calls and don't require the replicate package.

For keyframe mode, PIL is required:
```bash
# macOS with Homebrew
brew install pillow

# Or with pip (may need venv)
pip install pillow
```

### Python version compatibility

Scripts tested with Python 3.9+. If using older Python:
```bash
python3 --version
```

---

## File Issues

### "Image file not found"

**Check:** Path is correct and file exists
```bash
ls -la /path/to/your/image.png
```

**Common mistakes:**
- Relative vs absolute paths
- Spaces in filename (use quotes)
- Wrong extension

### Output file not created

**Check:** Output directory exists
```bash
# Create directory if needed
mkdir -p ~/Downloads/animations
```

### Permission denied

**Fix:** Check file permissions
```bash
chmod +w /path/to/output/directory
```

---

## Getting Help

If issues persist:
1. Check Replicate status: https://replicate.com/status
2. Review Replicate docs: https://replicate.com/docs
3. Check your usage: https://replicate.com/account/usage
