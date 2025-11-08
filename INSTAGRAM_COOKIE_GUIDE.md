# Instagram Cookie Setup Guide

## Why Do I Need This?

Instagram aggressively rate-limits automated downloads. After a few requests, Instagram blocks the server's IP address and requires authentication. By adding your Instagram session cookie, you bypass rate limits while keeping all processing local (sovereignty principle).

---

## How to Get Your Instagram Cookie (5 Simple Steps)

### Method 1: Chrome/Edge Developer Tools

1. **Open Instagram** in your browser and **log in**
2. **Press F12** (or right-click → Inspect) to open Developer Tools
3. Click the **Application** tab at the top
4. In the left sidebar, expand **Cookies** → click **https://www.instagram.com**
5. Find **sessionid** in the list → copy the **Value** column (long string of letters/numbers)

### Method 2: Firefox Developer Tools

1. **Open Instagram** in Firefox and **log in**
2. **Press F12** to open Developer Tools
3. Click the **Storage** tab at the top
4. In the left sidebar, expand **Cookies** → click **https://www.instagram.com**
5. Find **sessionid** → copy the **Value** (long string)

### Method 3: Safari

1. **Enable Developer Menu**: Safari → Settings → Advanced → Show Develop menu
2. **Open Instagram** and **log in**
3. **Develop menu** → Show Web Inspector
4. Click the **Storage** tab → **Cookies** → **https://www.instagram.com**
5. Find **sessionid** → copy the **Value**

---

## How to Add Your Cookie to DAWT-Transcribe

1. Click the **⚙ INSTAGRAM** button (top-right of homepage)
2. Paste your **sessionid** value into the text field
3. Optionally add a note (e.g., "Added 2025-11-08")
4. Click **SAVE COOKIE →**

✅ **Done!** Instagram downloads should now work reliably.

---

## Cookie Security & Privacy

- **Encrypted Storage**: Your cookie is encrypted using Fernet (symmetric encryption) with the `SESSION_SECRET` environment variable before being stored in the PostgreSQL database
- **Local Only**: The cookie never leaves your Replit server - no external API calls
- **Session Isolation**: Each cookie is tied to your Instagram account session
- **Expiry**: Instagram cookies typically last **30-90 days**
- **Easy Removal**: Click DELETE in the settings modal to remove your cookie instantly

---

## Cookie Maintenance

### When to Update Your Cookie

Update your cookie when you see errors like:
```
⚠️ Instagram Block: Instagram is temporarily blocking downloads
```
or
```
rate-limit reached or login required
```

### How Often?

- **Normal**: Every 30-90 days (when Instagram expires the session)
- **After logout**: If you log out of Instagram on your browser
- **After password change**: Instagram invalidates old sessions

### Best Practices

1. **Don't share your cookie** - It's like a temporary password
2. **Update when needed** - The UI will show when it was last used
3. **Delete if unused** - Remove the cookie if you're not using Instagram transcription

---

## Troubleshooting

### "Instagram Block" error even with cookie

**Solutions:**
1. **Refresh your cookie** - Open Instagram, F12, get a fresh sessionid value
2. **Check expiry** - Cookie might have expired (30-90 day lifespan)
3. **Try different Reel** - The specific video might be private/blocked
4. **Wait 10 minutes** - Instagram might still be rate-limiting temporarily

### Cookie won't save

**Solutions:**
1. **Check format** - Make sure you copied just the Value, not the whole row
2. **Check length** - Instagram sessionid is typically 30-50 characters long
3. **No spaces** - Remove any leading/trailing spaces
4. **Try browser incognito** - Re-login to Instagram in incognito mode and get fresh cookie

---

## Alternative: TikTok and YouTube

If you don't want to manage Instagram cookies, **TikTok and YouTube work reliably without authentication**:

- ✅ **TikTok**: No rate limits, no cookies needed
- ✅ **YouTube**: No rate limits, no cookies needed
- ⚠️ **Instagram**: Requires cookie for reliable access

---

## Technical Details

### What is sessionid?

The `sessionid` cookie is Instagram's authentication token. When you log in to Instagram, they give you this cookie to prove you're authenticated. By including it in download requests, Instagram treats the server as your authenticated browser session.

### Encryption Details

- **Algorithm**: Fernet (symmetric encryption using AES-128 in CBC mode with HMAC)
- **Key Derivation**: SHA-256 hash of `SESSION_SECRET` environment variable
- **Storage**: Encrypted in PostgreSQL `instagram_cookies` table
- **Decryption**: Only happens during yt-dlp requests, never exposed in API responses

### Privacy Guarantee

Your Instagram cookie:
- ✅ **Never sent to external APIs** (100% local processing)
- ✅ **Never logged in plaintext**
- ✅ **Encrypted at rest** in database
- ✅ **Only decrypted** when downloading Instagram Reels
- ✅ **Deletable anytime** via settings modal

---

## FAQ

**Q: Is this safe?**  
A: Yes. The cookie is encrypted and only used locally for Instagram downloads. It's never sent to external services.

**Q: Can someone hack my Instagram?**  
A: No. The sessionid is temporary and only works while the session is valid. Even if someone got it, Instagram requires device verification for sensitive actions.

**Q: What if I change my Instagram password?**  
A: Instagram will invalidate your old sessionid. You'll need to get a fresh one after changing your password.

**Q: Can I use multiple Instagram accounts?**  
A: Currently, DAWT-Transcribe stores one cookie at a time. Adding a new cookie deactivates the previous one.

**Q: Does this violate Instagram's Terms of Service?**  
A: This uses the same sessionid you'd use in your browser. You're essentially "logging in" to download public content. However, use responsibly and avoid excessive requests.

---

## Sovereignty Principle

This solution maintains DAWT-Transcribe's sovereignty principle:

- **✅ Local Processing**: Cookie is stored and encrypted locally
- **✅ No Cloud APIs**: No external authentication services
- **✅ User Control**: You own and manage your credentials
- **✅ Transparency**: Open-source encryption (crypto_utils.py)
- **✅ Deletable**: Remove your cookie anytime

---

**Questions or issues?** Check the error messages - they guide you to solutions.
