# Fluency AI

Talk to an AI in English — it listens, understands, and talks back. Everything runs on your own computer. No internet required after setup.

---

## What you need before starting

Install these three programs first. Click each link, download, and run the installer:

1. **Python 3.13** — https://www.python.org/downloads/
   - During install, **check the box that says "Add Python to PATH"**

2. **Docker Desktop** — https://www.docker.com/products/docker-desktop/
   - After installing, open Docker Desktop and wait until it says **"Docker Desktop is running"** in the bottom-left corner

3. **uv** — open **PowerShell** (press `Windows key`, type `PowerShell`, press Enter) and paste this:
   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   ```
   Then **close PowerShell and open a new one** so the change takes effect.

---

## Step-by-step setup (do this once)

Open **PowerShell** and run these commands one at a time:

### Step 1 — Go to the project folder
```powershell
cd f:\Fluency-ai
```

### Step 2 — Start the AI brain (Ollama)
```powershell
docker compose up -d
```
This downloads and starts the AI model. **Wait about 2 minutes** the first time — it's downloading a large file.

You can check it's ready by running:
```powershell
docker ps
```
You should see `fluency-ollama` with status `healthy`.

### Step 3 — Install Python dependencies
```powershell
uv sync
```
This installs everything the app needs. Wait for it to finish.

### Step 4 — Allow the app through the firewall (one-time)
```powershell
New-NetFirewallRule -DisplayName "Fluency AI" -Direction Inbound -Protocol TCP -LocalPort 7860 -Action Allow
```

---

## Running the app (every time)

### 1. Make sure Docker Desktop is open and running

### 2. Start Ollama (if not already running)
```powershell
cd f:\Fluency-ai
docker compose up -d
```

### 3. Start the app
```powershell
cd f:\Fluency-ai
uv run python app.py
```

Wait until you see this line in the output:
```
* Running on local URL:  https://0.0.0.0:7860
```

### 4. Open in browser

- **On this PC**: open your browser and go to → `https://localhost:7860`
- **On phone or other devices** (same Wi-Fi): go to → `https://192.168.0.103:7860`

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

To stop the app, press `Ctrl + C` in the PowerShell window.

To stop Ollama:
```powershell
cd f:\Fluency-ai
docker compose down
```

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
