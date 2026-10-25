import os
import sys
import json
import time
import requests
import subprocess
import threading
import select
import vosk
from vosk import Model, KaldiRecognizer, SetLogLevel

# --- Configuration ---
VOSK_MODEL_PATH = "/mnt/ai-storage/voice-models/vosk-model-small-en-us-0.15"
PIPER_MODEL_PATH = "/mnt/ai-storage/voice-models/en_US-lessac-medium.onnx"
OLLAMA_MODEL = "qwen2.5:1.5b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# --- Initialize Models ---
SetLogLevel(-1)
print("Loading Vosk model...")
model = Model(VOSK_MODEL_PATH)

is_ai_speaking = threading.Event()
wake_word_detected = threading.Event()
voice_input = ""

def recognize_speech():
    global voice_input

    # 44100 Hz to match most commoon microphones, changable per preference
    rec = vosk.KaldiRecognizer(model, 44100)
    print("\n[Listening...] say 'Hey/Yo/Hello Or just gala' or start typing to the Chat")

    command_rec = vosk.KaldiRecognizer(model, 44100)
    capturing_command = False

    while True:
        if is_ai_speaking.is_set():
            time.sleep(0.1)
            continue

        # Record 2 seconds of raw 44100Hz audio directly from the splitter/ raw can be edited based on prefrance, WAV/MP3
        subprocess.run(
            ["arecord", "-q", "-D", "plughw:0,0", "-d", "2", "-f", "S16_LE", "-r", "44100", "-c", "1", "-t", "raw", "/dev/shm/chunk.raw"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        try:
            with open("/dev/shm/chunk.raw", "rb") as f:
                data = f.read()
        except FileNotFoundError:
            continue

        if not capturing_command:
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").strip().lower()
                
                # Wake the AI here/ change AI commands here to if you want a different AI 
                if "hey gala" in text or "yo gala" in text or "hello gala" in text or "gala" in text:
                    print("\n [Wake word heard! Listening for command comrade]")
                    capturing_command = True
                    command_rec = vosk.KaldiRecognizer(model, 44100)

        else:
            if command_rec.AcceptWaveform(data):
                result = json.loads(command_rec.Result())
                text = result.get("text", "").strip()
                if text:
                    voice_input = text
                    wake_word_detected.set()
                    capturing_command = False

def get_ollama_response(prompt):
    is_ai_speaking.set()
    print(f"\nComrade: '{prompt}'")
    print("Thinking...")
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": 1024}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        json_response = response.json()
        return json_response.get("response", "").strip()
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

def speak(text):
    print(f"AI: {text}")
    out_file = "/mnt/ai-storage/audio-output/response.wav"

    # Generate the audio
    cmd = ["piper", "--model", PIPER_MODEL_PATH, "--output_file", out_file]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    process.communicate(input=text.encode('utf-8'))

    time.sleep(0.5)

    subprocess.run(["aplay", "-q", "-D", "plughw:0,0", out_file])

    time.sleep(0.5)

    is_ai_speaking.clear()
    print("\n[System Ready] Say 'Hey/Yo/Hello Smoke' or type here:")


if __name__ == "__main__":
    listener_thread = threading.Thread(target=recognize_speech, daemon=True)
    listener_thread.start()

    while True:
        try:
            if wake_word_detected.is_set():
                wake_word_detected.clear()
                ai_response = get_ollama_response(voice_input)
                speak(ai_response)
                continue

            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                text_input = sys.stdin.readline().strip()
                if text_input.lower() in ["exit", "quit"]:
                    print ("Exiting.")
                    break

                if text_input:
                    ai_response = get_ollama_response(text_input)
                    speak(ai_response)

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
