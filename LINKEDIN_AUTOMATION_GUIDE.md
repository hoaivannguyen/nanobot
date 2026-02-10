# LinkedIn Automation Guide

## The Challenge

LinkedIn has strong anti-bot protection:
- CAPTCHA verification
- 2FA (Two-Factor Authentication)
- Bot detection algorithms
- Rate limiting

## Solution: Persistent Browser Sessions

I've enhanced the browser tool to **save your login session** so you don't have to log in every time!

---

## How It Works

### Step 1: Manual Login (One Time Only)

**Run the browser in NON-headless mode** to log in manually:

```python
# Temporarily modify loop.py line 101:
self.tools.register(BrowserTool(headless=False, user_data_dir=str(browser_data_dir)))
```

Then ask your bot:
```
"Go to linkedin.com and wait"
```

A **browser window will open**:
1. Manually log into LinkedIn
2. Complete any CAPTCHA/2FA
3. The session gets saved automatically
4. Close the browser

### Step 2: Switch Back to Headless Mode

```python
# Change back to headless mode:
self.tools.register(BrowserTool(headless=True, user_data_dir=str(browser_data_dir)))
```

### Step 3: Use LinkedIn While Staying Logged In!

Now your bot can use LinkedIn without logging in again:

```
"Go to my LinkedIn profile and extract my headline"
"Search for 'AI Engineer' jobs on LinkedIn"
"Visit linkedin.com/in/someprofile and get their experience"
```

**The cookies are saved**, so you stay logged in! 🎉

---

## Where Cookies Are Stored

Cookies and session data are saved in:
```
~/.nanobot/workspace/.browser_data/
```

This persists across bot restarts.

---

## Important Notes

### ⚠️ Security Warning

- **Login cookies are stored in plain text**
- Keep your workspace directory secure
- Don't share `.browser_data` folder
- Use at your own risk

### LinkedIn Terms of Service

- LinkedIn may ban accounts for automation
- Use responsibly and within LinkedIn's TOS
- Consider using LinkedIn's official API instead
- This is for personal use only

### Session Expiry

- Sessions may expire after some time
- If logged out, repeat Step 1 to log in again
- LinkedIn may force re-authentication periodically

---

## Alternative: LinkedIn API (Recommended)

For production use, consider:
- **LinkedIn API** - Official, compliant, reliable
- **RapidAPI LinkedIn Scrapers** - Third-party services
- **Manual browser extensions** - Less automated but safer

---

## Complete Example Workflow

### First Time Setup:

1. **Edit loop.py temporarily** (set `headless=False`)
2. **Restart nanobot**
3. **Ask bot:** "Go to linkedin.com"
4. **Log in manually** in the browser window
5. **Close browser** when done
6. **Edit loop.py back** (set `headless=True`)
7. **Restart nanobot**

### Daily Use:

```
"Go to linkedin.com/in/elonmusk and tell me about him"
"Search for Python jobs on LinkedIn"
"Check my LinkedIn notifications"
```

All while staying logged in! 🚀

---

## Troubleshooting

**"Access Denied" or CAPTCHA appears:**
- Repeat manual login (Step 1)
- LinkedIn detected the bot - wait a few hours

**"Session expired":**
- Delete `.browser_data` folder
- Repeat manual login process

**Bot still can't log in:**
- LinkedIn may have blocked automation from your IP
- Try using LinkedIn API instead
- Wait 24-48 hours before trying again

---

## Code Reference

Enhanced browser tool with persistent sessions:
- [browser.py](nanobot/agent/tools/browser.py) - Browser automation tool
- [loop.py:101](nanobot/agent/loop.py#L101) - Where BrowserTool is registered

---

**Remember:** LinkedIn automation is against their TOS. Use responsibly! ⚖️
