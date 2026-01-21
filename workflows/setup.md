# Workflow: Setup Replicate

This workflow walks you through creating a Replicate account and configuring your API token.

<process>

<step_1>
**Create Replicate Account**

1. Go to https://replicate.com
2. Click "Sign in" → "Sign up"
3. Sign up with GitHub, Google, or email

Already have an account? Skip to Step 2.
</step_1>

<step_2>
**Get Your API Token**

1. Go to https://replicate.com/account/api-tokens
2. Click "Create token"
3. Give it a name (e.g., "pfp-animate")
4. Copy the token (starts with `r8_`)

**Important:** Save this token securely. You won't be able to see it again.
</step_2>

<step_3>
**Add Billing (Required for Generation)**

Replicate requires billing setup before running models.

1. Go to https://replicate.com/account/billing
2. Add a payment method
3. Add credits ($5-10 is enough for many animations)

**Pricing reference:**
- Kling v2.5 (video): ~$0.35 per 5s video
- Expression-editor (keyframe): ~$0.002 per frame
</step_3>

<step_4>
**Configure Environment Variable**

Choose ONE method to set your token:

**Option A: Export in terminal (temporary, current session only)**
```bash
export REPLICATE_API_TOKEN="r8_your_token_here"
```

**Option B: Add to shell profile (persistent)**
```bash
# For zsh (default on macOS)
echo 'export REPLICATE_API_TOKEN="r8_your_token_here"' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export REPLICATE_API_TOKEN="r8_your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

**Option C: Use direnv (project-specific)**
```bash
# Install direnv if needed: brew install direnv
echo 'export REPLICATE_API_TOKEN="r8_your_token_here"' > .envrc
direnv allow
```

**Option D: Use 1Password CLI (secure)**
```bash
export REPLICATE_API_TOKEN=$(op read "op://Vault/Replicate/api_token")
```
</step_4>

<step_5>
**Verify Setup**

Test that your token is configured:
```bash
echo $REPLICATE_API_TOKEN | head -c 10
```

Should output something like: `r8_aBcDeF...`

If empty, the token is not set. Return to Step 4.
</step_5>

<step_6>
**Test API Connection**

Run a quick test to verify everything works:
```bash
curl -s -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/account | head -c 100
```

Should return JSON with your account info. If you see an error, check:
- Token is correct (no extra spaces)
- Billing is set up
- Account is not suspended
</step_6>

</process>

<success_criteria>
- [ ] Replicate account created
- [ ] API token generated and saved securely
- [ ] Billing/credits added to account
- [ ] `REPLICATE_API_TOKEN` environment variable set
- [ ] `echo $REPLICATE_API_TOKEN | head -c 10` shows token prefix
- [ ] API test returns account info (not error)
</success_criteria>

<next_steps>
Setup complete! You can now:
- Run `python scripts/animate_pfp.py image.png output.mp4 --motion nod`
- See `workflows/animate.md` for full animation workflow
- See `references/presets.md` for available motion presets
</next_steps>
