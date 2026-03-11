# Fluency AI

Talk to an AI in English — it listens, understands, and talks back. Everything runs on your own computer. No internet required after setup.

## Demo

<div align="center">
  <a href="https://youtube.com/shorts/kIwkFEdDo54?feature=share">
    <img src="https://img.youtube.com/vi/kIwkFEdDo54/0.jpg" alt="Fluency AI Demo" width="400">
    <br>
    <strong>▶ Click to watch demo</strong>
  </a>
</div>

---

## What you need before starting

Install these programs first. Click each link, download, and run the installer:

1. **Python 3.13** — https://www.python.org/downloads/
   - During install, **check the box that says "Add Python to PATH"**

2. **Git** — https://git-scm.com/downloads
   - Use the default options during install

3. **Ollama** — https://ollama.com/download
   - After installing, it runs in the background automatically

4. **uv** (Python package manager) — open **PowerShell** (press `Windows key`, type `PowerShell`, press Enter) and paste this:
   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   ```
   Then **close PowerShell and open a new one** so the change takes effect.

---

## Step-by-step setup (do this once)

Open **PowerShell** and run these commands one at a time:

### Step 1 — Clone the project
```powershell
git clone https://github.com/frhnsdk/fluency-ai.git
cd fluency-ai
```

### Step 2 — Download the AI model
```powershell
ollama pull mistral:7b-instruct
```
This downloads the AI brain. **Wait a few minutes** the first time — it's a large file (~4 GB).

### Step 3 — Install Python dependencies
```powershell
uv sync
```
This installs everything the app needs. Wait for it to finish.

### Step 4 — Allow the app through the firewall (one-time, for phone access)
```powershell
New-NetFirewallRule -DisplayName "Fluency AI" -Direction Inbound -Protocol TCP -LocalPort 7860 -Action Allow
```

---

## Running the app (every time)

### 1. Start the app
```powershell
cd fluency-ai
uv run python app.py
```

Wait until you see this line in the output:
```
* Running on local URL:  https://0.0.0.0:7860
```

### 2. Open in browser

- **On this PC**: go to → `https://localhost:7860`
- **On phone or other devices** (same Wi-Fi): go to → `https://<your-pc-ip>:7860`

> To find your PC's IP, run `ipconfig` in PowerShell and look for **IPv4 Address** under your Wi-Fi adapter.

> **Browser warning**: The browser will show a security warning the first time.
> Click **Advanced** → **Proceed to ... (unsafe)** — this is safe, it's just because we use a self-made certificate.

---

## How to use it

1. Click the **microphone icon** to start recording
2. Speak your message in English
3. Click the **Stop button** (square icon) when you're done speaking
4. Wait a few seconds — the AI will reply in the chat **and speak out loud**

Click **Clear** to start a new conversation.

---

## Stopping the app

Press `Ctrl + C` in the PowerShell window.

---

## Is my data private?

**Yes, completely.** Nothing leaves your computer:
- Speech recognition runs locally (Moonshine)
- AI thinking runs locally (Mistral 7B via Ollama)
- Voice generation runs locally (Kokoro)
- No accounts, no API keys, no cloud

When you speak, your audio is:
1. Transcribed to text using Moonshine
2. Sent to a local LLM via Ollama for processing
3. The LLM response is converted back to speech with Kokoro
4. The audio response is streamed back to you via FastRTC
