import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
import time
import torch

# SETTINGS
SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.005   # adjust if needed
SILENCE_DURATION = 1.5     # seconds

# model = whisper.load_model("small", device="cuda")
model = None

def get_model():
    global model
    if model is None:
        print("//Loading Whisper model...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("small", device=device)
    return model

def record_until_silence():
    print('Listening...')

    recording = []
    silence_start = None
    speaking = False

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32") as stream:
        while True:
            data, _ = stream.read(1024)

            # Proper RMS energy calculation
            volume = np.sqrt(np.mean(data**2))
            #print("RMS:", volume)

            if volume > SILENCE_THRESHOLD:
                speaking = True
                silence_start = None
                recording.append(data)
            
            elif speaking:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > SILENCE_DURATION:
                    break
                recording.append(data)

                #this will send 1 sec silence if no input came in mic so it doesnt crash whisper with valueerror without an audio file.
    if recording:
        return np.concatenate(recording, axis=0)
    else:
        return np.zeros((SAMPLE_RATE,), dtype="float32")

def listen():
    audio_data = record_until_silence()

    # Avoid amplifying silence
    max_amp = np.max(np.abs(audio_data))
    if max_amp > 0.01:
        audio_data = audio_data / max_amp

    wav.write("temp.wav", SAMPLE_RATE, audio_data)

    print("//Sending signals in brain to Process...")

    model = get_model()
    result = model.transcribe("temp.wav", language="en", task="transcribe")

    print("Raw Whisper output:", result)

    text = result["text"].strip()
    print("Final transcribed text:", text)

    return text