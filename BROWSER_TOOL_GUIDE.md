# Browser Automation Tool Guide

## Installation

### 1. Install Playwright

```bash
pip install playwright>=1.40.0
playwright install chromium
```

Or reinstall nanobot with the new dependency:

```bash
pip install -e .
playwright install chromium
```

### 2. Restart your nanobot

After installation, restart your nanobot service for the tool to be available.

---

## Usage Examples

Once installed, your bot can use browser automation! Here are example commands:

### Navigate to a website

```
"Go to https://example.com and tell me what you see"
```

The bot will use:
```python
browser(action="navigate", url="https://example.com")
```

### Click a button

```
"Click the 'Login' button on the current page"
```

The bot will use:
```python
browser(action="click", selector="button:has-text('Login')")
```

### Fill a form

```
"Fill in the search box with 'AI tools'"
```

The bot will use:
```python
browser(action="fill", selector="input[type='search']", text="AI tools")
```

### Extract content

```
"Extract all the article titles from the page"
```

The bot will use:
```python
browser(action="extract", selector="h2.article-title")
```

### Take a screenshot

```
"Take a screenshot of the current page"
```

The bot will use:
```python
browser(action="screenshot", screenshot_path="page.png")
```

---

## Complete Workflow Example

User: *"Go to news.ycombinator.com, find the top story title, and take a screenshot"*

Bot will:
1. `browser(action="navigate", url="https://news.ycombinator.com")`
2. `browser(action="extract", selector=".titleline > a")`
3. `browser(action="screenshot", screenshot_path="hackernews.png")`

---

## Available Actions

| Action | Description | Required Parameters |
|--------|-------------|---------------------|
| `navigate` | Go to a URL | `url` |
| `click` | Click an element | `selector` |
| `fill` | Fill a form field | `selector`, `text` |
| `extract` | Get text from elements | `selector` |
| `screenshot` | Save page screenshot | `screenshot_path` (optional) |

---

## CSS Selectors

The tool uses CSS selectors to find elements:

- **By ID:** `#my-element`
- **By class:** `.my-class`
- **By tag:** `button`, `input`, `h1`
- **By attribute:** `[type="submit"]`
- **By text:** `button:has-text("Login")`
- **Combination:** `form.login button[type="submit"]`

---

## Tips

1. **Headless mode:** Browser runs invisibly by default (faster, works on servers)
2. **Timeouts:** Default is 30 seconds, adjustable with `wait_timeout` parameter
3. **Screenshots:** Saved to workspace directory by default
4. **Persistent session:** Browser stays open between commands for efficiency

---

## Security Note

⚠️ **Only use browser automation with trusted websites**
- The bot can interact with any website
- Be cautious about filling forms with sensitive data
- Consider restricting access via the `allow_from` config

---

## Deploy to Railway

If deploying to Railway, you'll need to install Playwright in your Railway environment:

### Option 1: Add to Dockerfile (if using Docker)

```dockerfile
RUN pip install playwright && playwright install chromium --with-deps
```

### Option 2: Use Railway's Nixpacks

Create a `.nixpacks/setup.sh`:

```bash
#!/bin/bash
playwright install chromium --with-deps
```

Make it executable:
```bash
chmod +x .nixpacks/setup.sh
```

---

## Troubleshooting

**Error: "Browser not found"**
- Run: `playwright install chromium`

**Error: "Missing dependencies"**
- Run: `playwright install-deps chromium`
- Or on Railway, use `--with-deps` flag

**Timeout errors**
- Increase `wait_timeout` parameter
- Check if the website is accessible
- Try with `headless=False` locally to see what's happening

---

## Advanced: Custom Browser Settings

To modify browser settings, edit [nanobot/agent/tools/browser.py](nanobot/agent/tools/browser.py):

```python
# Example: Run in non-headless mode (shows browser window)
self.tools.register(BrowserTool(headless=False))
```

---

**You're all set!** 🎉 Your nanobot can now automate browser tasks!
