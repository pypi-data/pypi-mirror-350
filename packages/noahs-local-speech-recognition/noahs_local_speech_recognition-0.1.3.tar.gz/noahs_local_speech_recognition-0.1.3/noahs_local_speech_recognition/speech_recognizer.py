import os
import time
import json
import threading
from vosk import Model, KaldiRecognizer
import pyaudio
import requests
import zipfile
import shutil
from tqdm import tqdm

import platform
import subprocess
import sys

def check_and_prompt_portaudio_install():
    if platform.system() != "Linux":
        return  # Only check on Linux

    try:
        # Check if portaudio19-dev is installed
        result = subprocess.run(["dpkg", "-s", "portaudio19-dev"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("[WARNING] 'portaudio19-dev' is not installed.")
            user_input = input("Would you like to install 'portaudio19-dev'? [y/N]: ").strip().lower()
            if user_input in ['y', 'yes']:
                try:
                    subprocess.check_call(["sudo", "apt", "update"])
                    subprocess.check_call(["sudo", "apt", "install", "-y", "portaudio19-dev"])
                    print("[INFO] 'portaudio19-dev' installed successfully.")
                except subprocess.CalledProcessError:
                    print("[ERROR] Failed to install 'portaudio19-dev'. Please install it manually.")
                    sys.exit(1)
            else:
                print("[INFO] Skipping installation. You may encounter audio issues if 'portaudio19-dev' is not installed.")
        else:
            print("[INFO] 'portaudio19-dev' is already installed.")
    except FileNotFoundError:
        print("[WARNING] 'dpkg' not found. This check only works on Debian-based systems.")


check_and_prompt_portaudio_install()

# Globals
speech_log = []
speech_log_lock = threading.Lock()
listening_thread = None
stop_listening = threading.Event()
pause_listening = threading.Event()
transcript_file = None
start_timestamp_str = None

# # Load model
MODEL_NAME = "vosk-model-small-en-us-0.15"
MODEL_PATH = os.path.join(".", MODEL_NAME)

MODEL_URLS = {
    "vosk-model-small-en-us-0.15": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
    "vosk-model-en-us-0.22": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
    "vosk-model-en-us-0.22-lgraph": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip"
}

def download_and_extract_model(model_name, model_path):
    zip_path = model_path + ".zip"
    url = MODEL_URLS[model_name]
    print(f"[INFO] Downloading model from: {url}")

    # Stream download with progress
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(zip_path, "wb") as f, tqdm(
        desc=f"Downloading {model_name}",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

    print("[INFO] Extracting model...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(".")

    os.remove(zip_path)
    print(f"[INFO] Model extracted to: {model_path}")

# === Load or download model ===
if not os.path.exists(MODEL_PATH):
    if MODEL_NAME in MODEL_URLS:
        download_and_extract_model(MODEL_NAME, MODEL_PATH)
    else:
        raise FileNotFoundError(
            f"[ERROR] Model not found at '{MODEL_PATH}' and no download URL is known."
        )

# # Load the model
# model = Model(MODEL_PATH)

# Helper functions
def get_text_after_keyword(text, keyword):
    keyword = keyword.lower()
    words = text.strip().split()
    try:
        index = words.index(keyword)
        return " ".join(words[index + 1:])
    except ValueError:
        return ""

def list_microphones():
    p = pyaudio.PyAudio()
    print("Available input devices:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"  [{i}] {info['name']}")
    p.terminate()




def start_speech_listening(name="robot", stop_talking_delay=2, device_index=None, model_name="vosk-model-small-en-us-0.15"):
    global listening_thread, stop_listening, transcript_file, start_timestamp_str

    stop_listening.clear()

    # Prepare transcript file
    os.makedirs("transcripts", exist_ok=True)
    start_timestamp_str = time.strftime("%Y%m%d_%H%M%S")
    transcript_file = os.path.join("transcripts", f"transcript_{start_timestamp_str}.txt")
    with open(transcript_file, "w"): pass

    # Determine and check model
    model_path = os.path.join(".", model_name)
    if not os.path.exists(model_path):
        if model_name in MODEL_URLS:
            download_and_extract_model(model_name, model_path)
        else:
            raise FileNotFoundError(
                f"[ERROR] Model '{model_name}' not found and no download URL is known."
            )

    # Load the model
    local_model = Model(model_path)

    def listen():
        try:
            recognizer = KaldiRecognizer(local_model, 16000)
            recognizer.SetWords(True)

            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=16000,
                            input=True,
                            input_device_index=device_index,
                            frames_per_buffer=4000)

            keyword_detected = False
            transcribing = False
            transcription = []
            last_speech_time = time.time()

            print(f"Listening for the keyword '{name}'...")

            while not stop_listening.is_set():
                if pause_listening.is_set():
                    time.sleep(0.1)
                    continue

                data = stream.read(4000, exception_on_overflow=False)

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").lower()
                    timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S')

                    if text:
                        print(f"Recognized: {text}")
                        with open(transcript_file, "a") as f:
                            f.write(f"{text} | {timestamp_str}\n")

                        if name.lower() in text and not keyword_detected:
                            keyword_detected = True
                            transcribing = True
                            transcription = []
                            print(f"\n[{name} detected!] Now transcribing...\n")

                        if transcribing:
                            transcription.append(text)
                            last_speech_time = time.time()

                if transcribing and (time.time() - last_speech_time > stop_talking_delay):
                    entry = {
                        "timestamp": timestamp_str,
                        "content": get_text_after_keyword(" ".join(transcription), name),
                        "response": None
                    }
                    with speech_log_lock:
                        speech_log.append(entry)
                    print("\n[Silence detected] Transcription stopped.\n")
                    print("Final Transcription:", entry)
                    keyword_detected = False
                    transcribing = False
                    transcription = []
                    print(f"\nListening for '{name}' again...\n")

            stream.stop_stream()
            stream.close()
            p.terminate()

        except Exception as e:
            print(f"[ERROR in listening thread]: {e}")

    listening_thread = threading.Thread(target=listen, daemon=True)
    listening_thread.start()


def stop_speech_listening():
    global stop_listening, listening_thread, transcript_file, start_timestamp_str
    stop_listening.set()
    if listening_thread:
        listening_thread.join()
        listening_thread = None

    # Rename transcript file with start/end
    if transcript_file and start_timestamp_str:
        stop_timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        new_name = f"transcript_{start_timestamp_str}_{stop_timestamp_str}.txt"
        new_path = os.path.join("transcripts", new_name)
        os.rename(transcript_file, new_path)
        print(f"Transcript saved as: {new_path}")

    print("Speech listening stopped.")

# Log management
def get_speech_log():
    with speech_log_lock:
        return list(speech_log)

def get_speech_log_entry(i=-1):
    with speech_log_lock:
        return speech_log[i] if speech_log else None

def set_speech_log_response(response, i=-1):
    with speech_log_lock:
        if speech_log: speech_log[i]["response"] = response

def remove_speech_log_entry(i=-1):
    with speech_log_lock:
        if speech_log: del speech_log[i]

# Pause / Resume
def pause_speech_listening():
    pause_listening.set()

def resume_speech_listening():
    pause_listening.clear()


if __name__ == "__main__":

    print("Listing available microphone devices:")
    list_microphones()

    print("\nStarting speech recognition with default input device...")
    start_speech_listening(name="robot", stop_talking_delay=2, device_index=None, model_name="vosk-model-small-en-us-0.15")

    try:
        while True:
            time.sleep(2)
            print("_________________________")
            entry = get_speech_log_entry()
            if entry and entry["response"] is None:
                heard = entry["content"]
                print(f"I HEARD: {heard}")
                speech_log1 = get_speech_log()
                print(f"SPEECH LOG BEFORE SET RESPONSE: {speech_log1}")
                set_speech_log_response(heard)
                speech_log2 = get_speech_log()
                print(f"SPEECH LOG AFTER SET RESPONSE: {speech_log2}")
            if entry and entry["content"] in ["goodbye", "good bye", "bye", "quit", "end", "exit"]:
                break
    except KeyboardInterrupt:
        pass
    finally:
        stop_speech_listening()







