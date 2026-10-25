# The painful story of a potato that talks

It all started with receiving a kernel-locked ODROID-C2 as a gift from a special kind of bro. I didn't know what I was expecting with this project, but at first, I wanted to use it as a custom Linux PC. Then, I had the wonderful idea of running an AI on it... not realizing the things I would face along the way.

Issue 1: The damn Potato was hard-locked to the core. Meaning it was kernel locked... that means I had no way into the eMMC that came with the board. I hope it had no Bitcoin, because what I did basically erased everything on it, including the boot order. At that point, I didn't care what system or games it had. I just wanted to call it mine.

Issue 2: Finances. Very limited budget, and just to break into the U-Boot (core boot) I had to buy a couple of things, excluding the one thing that would have made things a lot easier (an eMMC to USB reader...). Yeah, I totally ignored that as I already bought a USB to TTL converter instead... and it just overcomplicated things to the point where I had to sleep on my chair lel. But anyways, I'm not complaining, I learned a few things! Overall costs were: $25 for reformatting and getting the mic plus speakers to work, which is not too bad, but for me, it is too much.

Issue 1 was solved by interrupting U-Boot after trying to brute force the password... using the USB to TTL to interrupt and most definitely shorting a couple of things with soldering and totally wrong wiring... like if I had infinite lives and infinite bombs to defuse. I probably would have failed at 99 out of a 100 of them... So I got extremely lucky to not brick it or totally just destroy the board. Eventually, I interrupted the Potato from just bursting out from the heat of the situation. One thing that helped later was making a multimeter using a bootleg Arduino I have. It gave me the info I needed, and hey, Issue 1 solved!

After interrupting U-Boot and accessing the core of the root, the eMMC was hardcoded to have to be mmc0... meaning it will always boot first no matter what. So I'll recap this process with the help of Deep and Google for assistance:

# Potato head steps:
- By leveraging built-in hardware overrides and decoding the exact operating system under the hood, I successfully transformed a locked, legacy eMMC board into an open, updated headless Armbian Linux ARM server.
- Interrupting U-Boot: I matched the correct 115200 baud rate, safely matched the 3.3V logic (without burning the SoC), and spammed keys to drop into the odroidc2# prompt.
- Wiping the corrupt eMMC bootloader: I used mmc dev and mmc erase to destroy the corrupt loop that was locking me out.
- SD Card Fallback: I successfully forced the Amlogic chip to fall back to the clean MicroSD card operating system.
- The Result: This forced the ODROID-C2 to behave exactly like a giant USB flash drive. My main PC instantly recognized the internal eMMC over a standard Micro-USB cable, allowing me to completely wipe and format the storage block.

# The Challenges:
After successfully flashing a new image, I ran into wall-to-wall command errors. Standard Debian/Ubuntu commands like sudo apt install and armbian-config threw immediate command not found errors.
I looked closely at the system's behavioral errors and realized the board wasn't running Armbian at all—it was running a highly stripped-down Arch Linux ARM distribution.
We successfully pivoted away from Debian syntax and unlocked the native Arch package environment by initializing the local system keys and targeting Arch's powerhouse package manager.
then I moved TO Ambian minimal enviroment as it solved most of the boot and compatiblity issues since arch was no longer supported for odroid

**The monitor** .. and oh boy. let me just say Never use a VGA monitor from 20 years back for this device unless you want to suffer. well yeah one thing i had to do is resolder an HDMI to VGA adapter to hot wire it to a use so it can receive more Volts .. hence making the HDMI work without black screens. i failed and i had to buy a specific adapter. which solved the problem with the hdmi not pulling enough power. and also ambianOS just worked perfectly with everything. including not having to edit a single boot.ini file. it's just so RETRO FRIENDLY

**The Storage tragedy (eMMC vs. SD)**
- I ran into massive issues with the Amlogic U-Boot bootloader.
- I discovered the hard way that the ODROID-C2 boots from the SD card first, and the device numbering (mmc0 vs mmc1) can shift.
- I accidentally wiped the eMMC bootloader and had to manually flash the raw .img from a PC using dd to restore the standard boot order.
- I moved the entire 60GB SD card to act as the /mnt/ai-storage for the 1.5GB AI model and Python virtual environment to save space on the eMMC.

**The Half-Duplex Hardware Trap**
- I discovered that cheap $5 USB audio splitters are "half-duplex." They physically cannot record and play audio at the same time.
- I tried using an HDMI-to-VGA adapter with a 3.5mm jack to split the audio, but hit HDMI I/O errors and "unknown ELD version" handshake failures.
- I solved it by timing arecord and aplay perfectly, forcing the USB chip to switch between "Mic mode" and "Speaker mode".

**The CPU Bottleneck & Audio Overflows**
- Initially, I used Python's sounddevice and scipy to resample audio. This maxed out the ODROID's CPU and caused endless Input Overflow errors.
- The Breakthrough: I stripped out all the heavy Python audio math. Instead, I used subprocess to call native Linux arecord (recording raw PCM directly to RAM at 44.1kHz) and aplay. CPU usage dropped to near zero.

**Taming the Microphone**
- The cheap SVEN table mic picked up too much room noise, causing Vosk to hallucinate words.
- I solved this by using SoX to apply a telephone-style bandpass filter (highpass 300, lowpass 3000) before feeding the audio to the AI.

**The Brain & The Voice**
- I wired up Vosk with a custom "Grammar Mode" to only listen for the wake words ("Hey Smoke", "Yo Smoke"). Yes i called it smoke because of how much I had to inhale tobbacoo because oof it
- I hooked it to Ollama running locally via localhost:11434.
- I used Piper TTS to generate the .wav file and instantly blast it through the speaker.

Eventually I will upload a video soon to my YouTube and here to see how it works at its current V 0.1 state! 
