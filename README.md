# FULL Installation & Setup Guide
***Note: SKIP TO STEP 5&6 if you have the dependence or your own model***

1. *** System Dependencies ***
You need the ALSA audio tools and SoX for audio processing:
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv alsa-utils sox
```

2. *** Python Environment ***
Clone the repo and set up a virtual environment:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
python3 -m venv voice-env
source voice-env/bin/activate
pip install -r requirements.txt
```

3. *** Download the Models ***
You need the Vosk speech model and the Piper voice model.
*** Create a folder for models ***
```bash
mkdir -p /mnt/ai-storage/voice-models
cd /mnt/ai-storage/voice-models
```

* Download Vosk (English) *
```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

* Download Piper (English Voice) *
```bash
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

* Install Ollama *
Ollama runs the AI brain. Since it's an ARM64 board, download the standalone binary:

```bash
cd /mnt/ai-storage
curl -fsSL https://ollama.com/download/ollama-linux-arm64.tar.zst -o ollama.tar.zst
tar --zstd -xf ollama.tar.zst
rm ollama.tar.zst
```

5. *** Run the AI Server ***
Start the Ollama server in the background, pointing to your SD card:

```bash
export OLLAMA_MODELS=/mnt/ai-storage/models
export OLLAMA_HOST=0.0.0.0:11434
/mnt/ai-storage/bin/ollama serve > /mnt/ai-storage/ollama.log 2>&1 &
```

* Pull the Qwen model *
```bash
/mnt/ai-storage/bin/ollama pull qwen2.5:1.5b
```

6. *** Start the Assistant ***
Make sure your audio card number matches the script (run aplay -l to check if it's plughw:0,0 or plughw:1,0). Then run:

```bash
source /mnt/ai-storage/voice-env/bin/activate
python3 voice_assistant.py
```

* Say "Hey Potato" to wake it up! *

# Technical Specifications & Environment

Here is the exact hardware and software environment this project was built and tested on:

*   **Hardware**: Hardkernel ODROID-C2 (Amlogic S905, Quad-Core ARM Cortex-A53, 2GB RAM)
*   **Storage**: 8GB eMMC (OS) + 60GB SD Card (AI Models & Storage)
*   **Total Storage Used**: ~4.3 GB (OS, AI models, Python environment, and voice models)
*   **OS**: Armbian (Minimal / CLI)
*   **Linux Kernel**: 6.12.58 (Amlogic Meson 64-bit)
*   **Python Version**: Python 3.13
*   **Ollama Version**: Standalone ARM64 Binary (Latest)

---

# Local Voice Assistant on ODROID-C2 (2GB RAM)
A completely offline, voice-activated AI assistant running on a humble ODROID-C2 single-board computer. It utilizes **Vosk** for Speech-to-Text, **Ollama (Qwen 2.5 1.5B)** for the AI brain, and **Piper TTS** for Text-to-Speech. 

# Features
- 100% Offline and Private (No cloud APIs).
- Custom Wake Word ("Hey Smoke").
- Runs entirely on a CPU with only 2GB of RAM.
- Uses lightweight native Linux audio commands (`arecord` / `aplay`) to prevent CPU bottlenecks.

# Prerequisites
- ODROID-C2 (or similar ARM64 board).
- Armbian OS (Minimal/CLI).
- USB Microphone / Speaker.
- Vosk Models (`vosk-model-small-en-us-0.15`).
- Piper TTS Voice (`en_US-lessac-medium.onnx`).
- Ollama ARM64 binary.

---
