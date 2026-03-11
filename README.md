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

---

## How it works

```
┌─────────────────────────────────────────────────────────┐
│                     Your Browser                        │
│              (PC, Phone, Tablet — HTTPS)                │
│                                                         │
│   🎤 Microphone ──► Record ──► Send audio to server     │
│                                                         │
│   💬 Chat display ◄── text response                     │
│   🔊 Speaker      ◄── audio response                   │
└────────────────────────┬────────────────────────────────┘
                         │
                    HTTPS (LAN)
                         │
┌────────────────────────▼────────────────────────────────┐
│                   Gradio Server                         │
│                    (app.py)                              │
│                                                         │
│  ┌───────────┐   ┌───────────┐   ┌───────────────────┐ │
│  │ Moonshine │   │ Mistral   │   │      Kokoro       │ │
│  │   (STT)   │   │ 7B (LLM)  │   │      (TTS)       │ │
│  │           │   │           │   │                   │ │
│  │ Audio ──► │   │ Text ──►  │   │ Text ──► Audio    │ │
│  │ Text      │   │ Response  │   │ (spoken reply)    │ │
│  └─────┬─────┘   └─────┬─────┘   └────────┬──────────┘ │
│        │               │                   │            │
│        └──► step 1     └──► step 2         └──► step 3  │
│             "hello"         "Hi! How are         🔊     │
│                              you today?"                │
└─────────────────────────────────────────────────────────┘
         ▲                    │
         │              localhost:11434
         │                    ▼
    ┌────┴────────────────────────────┐
    │           Ollama                │
    │    (runs natively on your PC)   │
    │    Model: mistral:7b-instruct   │
    └─────────────────────────────────┘
```

### Pipeline: what happens when you speak

1. **You speak** → browser records audio via microphone
2. **Moonshine (STT)** → converts your speech to text using FastRTC's built-in speech-to-text model (runs on CPU via ONNX)
3. **Mistral 7B (LLM)** → your text is sent to Ollama, which generates a conversational English reply
4. **Kokoro (TTS)** → the reply text is converted to natural-sounding speech using FastRTC's text-to-speech model (runs on CPU via ONNX)
5. **Browser** → receives both the text (shown in chat) and audio (played out loud)

All 3 AI models run locally on your machine. No data leaves your computer.

---

## Tech stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Web UI** | [Gradio](https://gradio.app/) | Browser interface with mic input, chat, and audio playback |
| **Speech-to-Text** | [Moonshine](https://github.com/usefulsensors/moonshine) (via FastRTC) | Converts your voice to text — fast, lightweight, runs on CPU |
| **LLM** | [Mistral 7B Instruct](https://mistral.ai/) (via [Ollama](https://ollama.com/)) | Generates conversational English responses |
| **Text-to-Speech** | [Kokoro](https://github.com/hexgrad/kokoro) (via FastRTC) | Converts AI text response to natural speech |
| **Package manager** | [uv](https://docs.astral.sh/uv/) | Fast Python dependency management |
| **HTTPS** | Self-signed certificate (via `cryptography`) | Enables microphone access from phones/tablets on LAN |

When you speak, your audio is:
1. Transcribed to text using Moonshine
2. Sent to a local LLM via Ollama for processing
3. The LLM response is converted back to speech with Kokoro
4. The audio response is streamed back to you via FastRTC
