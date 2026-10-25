Add this Installation Instructions section right above "The Story" in your README.

markdown
# FULL Installation & Setup Guide
Note: SKIP TO STEP 5&6 if you have the dependence or your own model

## 1. System Dependencies
# You need the ALSA audio tools and SoX for audio processing:
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv alsa-utils sox
```

## 2.  Python Environment
# Clone the repo and set up a virtual environment:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
python3 -m venv voice-env
source voice-env/bin/activate
pip install -r requirements.txt
```

## 3. Download the Models
You need the Vosk speech model and the Piper voice model.
# Create a folder for models
```bash
mkdir -p /mnt/ai-storage/voice-models
cd /mnt/ai-storage/voice-models
```

#  Download Vosk (English)
```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

#  Download Piper (English Voice)
```bash
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

## 4. Install Ollama
# Ollama runs the AI brain. Since it's an ARM64 board, download the standalone binary:

```bash
cd /mnt/ai-storage
curl -fsSL https://ollama.com/download/ollama-linux-arm64.tar.zst -o ollama.tar.zst
tar --zstd -xf ollama.tar.zst
rm ollama.tar.zst
```

## 5. Run the AI Server
## Start the Ollama server in the background, pointing to your SD card:

```bash
export OLLAMA_MODELS=/mnt/ai-storage/models
export OLLAMA_HOST=0.0.0.0:11434
/mnt/ai-storage/bin/ollama serve > /mnt/ai-storage/ollama.log 2>&1 &
```

# Pull the Qwen model
```bash
/mnt/ai-storage/bin/ollama pull qwen2.5:1.5b
```

## 6. Start the Assistant
# Make sure your audio card number matches the script (run aplay -l to check if it's plughw:0,0 or plughw:1,0). Then run:

```bash
source /mnt/ai-storage/voice-env/bin/activate
python3 voice_assistant.py
```

Say "Hey Gala" to wake it up!

## Technical Specifications & Environment

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

# The painful story of a potato that talks

It all started with receiving a kernal locked odroid-c2 as a gift from a special kind of bro. I didn't know what i was expecting with this project
but at first I wanted to use it as a custom linux PC. then I had the wonderful idea of running an AI on it .. not realizing the things I will face along the

Issue 1: the damn Potate was hard locked too the core. meaning kernel locked .. 


• The Challenge: You didn't want to buy or use an external eMMC-to-microSD physical adapter board to flash the storage module.
• The Breakthrough: We bypassed the physical adapter entirely by utilizing the ODROID-C2’s low-level U-Boot bootloader. By mashing keys at boot, you halted the system at the native odroidc2# prompt and executed:text
ums mmc 0
Use code with caution.
• The Result: This forced the ODROID-C2 to behave exactly like a giant USB flash drive. Your main PC instantly recognized the internal eMMC over a standard Micro-USB cable, allowing you to completely wipe and format the storage block.

2. Overcoming the Login Deadlock

• The Challenge: After your first formatting attempt, the board unexpectedly booted right back into an old, locked Linux operating system (im59 login).
• The Breakthrough: We realized that standard OS formatting tools on your PC only cleared superficial storage partitions rather than low-level master boot records.
• The Result: You forced the board back into U-Boot UMS mode (ums mmc 0) and used a deep block-flashing utility (BalenaEtcher / Rufus) to completely overwrite the entire raw eMMC drive layout from scratch.

3. Decoding the OS Environment

• The Challenge: After successfully flashing a new image, you ran into wall-to-wall command errors. Standard Debian/Ubuntu commands like sudo apt install and armbian-config threw immediate command not found errors.
• The Breakthrough: We looked closely at the system's behavioral errors and realized the board wasn't running Armbian at all—it was running a highly stripped-down Arch Linux ARM distribution.
• The Result: We successfully pivoted away from Debian syntax and unlocked the native Arch package environment by initializing the local system keys and targeting Arch's powerhouse package manager:
1. Interrupting U-Boot: Matching the correct 115200 baud rate, safely matching the 3.3V logic (without burning the SoC), and spamming keys to drop into the odroidc2# prompt.
2. Wiping the corrupt eMMC bootloader: Using mmc dev and mmc erase to destroy the corrupt loop that was locking you out.
3. SD Card Fallback: Successfully forcing the Amlogic chip to fall back to your clean MicroSD card operating system.

- Decided to use the lightweight Qwen 2.5 1.5B model via Ollama.

### 2. The Storage Nightmare (eMMC vs. SD)
- Ran into massive issues with the Amlogic U-Boot bootloader.
- Discovered the hard way that the ODROID-C2 boots from SD first, and the device numbering (`mmc0` vs `mmc1`) can shift.
- Accidentally wiped the eMMC bootloader and had to manually flash the raw `.img` from a PC using `dd` to restore the standard boot order.
- Moved the entire 60GB SD card to act as the `/mnt/ai-storage` for the 1.5GB AI model and Python virtual environment to save the eMMC.

### 3. The Half-Duplex Hardware Trap
- Discovered that cheap $5 USB audio splitters are "half-duplex." They physically cannot record and play audio at the same time.
- Tried using an HDMI-to-VGA adapter with a 3.5mm jack to split the audio, but hit HDMI I/O errors and "unknown ELD version" handshake failures.
- Solved it by timing `arecord` and `aplay` perfectly, forcing the USB chip to switch between "Mic mode" and "Speaker mode".

### 4. The CPU Bottleneck & Audio Overflows
- Initially used Python's `sounddevice` and `scipy` to resample audio. This maxed out the ODROID's CPU and caused endless `Input Overflow` errors.
- **The Breakthrough:** Stripped out all the heavy Python audio math. Instead, used `subprocess` to call native Linux `arecord` (recording raw PCM directly to RAM at 44.1kHz) and `aplay`. CPU usage dropped to near zero.

### 5. Taming the Microphone
- The cheap SVEN table mic picked up too much room noise, causing Vosk to hallucinate words.
- Solved by using **SoX** to apply a telephone-style bandpass filter (`highpass 300`, `lowpass 3000`) before feeding the audio to the AI.

### 6. The Brain & The Voice
- Wired up Vosk with a custom "Grammar Mode" to only listen for the wake words ("Hey Smoke", "Yo Smoke").
- Hooked it to Ollama running locally via `localhost:11434`.
- Used Piper TTS to generate the `.wav` file and instantly blast it through the speaker.

---
*Built with patience, lots of terminal errors, and a strong refusal to buy a Raspberry Pi 5.*
