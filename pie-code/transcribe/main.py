import pyaudio
import wave
import vosk
import soundfile
import json
from metaphone import doublemetaphone
from rapidfuzz import fuzz
import multiprocessing as mp

model_name = "vosk-model-en-us-0.22"
sample_rate = 16000
chunk_size = 4000
format = pyaudio.paInt16

def record(audio_queue):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
    print("Recording...")

    try:
        while True:
            data = stream.read(chunk_size, exception_on_overflow=False)
            audio_queue.put(data)
    except KeyboardInterrupt:
        print("Recording stopped")
        stream.stop_stream()
        stream.close()
        audio.terminate()

def metaphone(text):
    words = text.lower().split()
    return ' '.join([doublemetaphone(i)[0] for i in words])

def compare(transcribed, command, threshold):
    transcribed_meta = metaphone(transcribed)

    for i in command:
        command_meta = metaphone(i)
        similarity = fuzz.partial_ratio(transcribed_meta, command_meta)
        print(f"Current similarity is {similarity}")

        if similarity >= threshold:
            return True, i, similarity

    
    return False, None, similarity

def transcribe(audio_queue):
    model = vosk.Model(model_name)
    commands = ["module one on", "module one off"]
    recognizer = vosk.KaldiRecognizer(model, sample_rate)
    recognizer.SetWords(True)

    print("Starting to transcribe...")

    while True:
        try:
            data = audio_queue.get(timeout=1)
        except queue.Empty:
            continue

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text:
                print(f"Transcript: {text}")
                found, command, score = compare(text, commands, 80)
                if found == True:
                    print(f"Successfully found {command} with {score}")
                    # Put commmand execution here

if __name__ == "__main__":
    mp.set_start_method("spawn")
    audio_queue = mp.Queue()
    
    record_proc = mp.Process(target=record, args=(audio_queue,))
    transcribe_proc = mp.Process(target=transcribe, args=(audio_queue,))

    record_proc.start()
    transcribe_proc.start()

    record_proc.join()
    transcribe_proc.join()
