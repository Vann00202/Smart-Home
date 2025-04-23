import pyaudio
import vosk
import json
from metaphone import doublemetaphone
from rapidfuzz import fuzz
import multiprocessing as mp
import asyncio
import pyttsx3
import time

model_name = "vosk-model-small-en-us-0.15"
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

    if len(transcribed.split()) < 3:
        return False, None, 0

    max_similarity = 0
    max_command = None

    for i in command:
        command_meta = metaphone(i)
        similarity = fuzz.partial_ratio(transcribed_meta, command_meta)
        print(f"Current similarity is {similarity}")
        if similarity > max_similarity:
            max_similarity = similarity
            max_command = i

    if max_similarity >= threshold:
        return True, max_command, max_similarity

    return False, None, max_similarity


def transcribe(audio_queue, output_queue):
    model = vosk.Model(model_name)
    commands = ["module one off", "module one on", "module one toggle"]
    recognizer = vosk.KaldiRecognizer(model, sample_rate)
    recognizer.SetWords(True)
    audio_engine = pyttsx3.init()
    audio_engine.setProperty("rate", 15)

    print("Starting to transcribe...")

    while True:
        try:
            data = audio_queue.get(timeout=1)
        except audio_queue.Empty:
            continue

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text:
                print(f"Transcript: {text}")
                found, command, score = compare(text, commands, 80)
                if found == True:
                    audio_engine.stop()
                    if command == "module one on":
                        audio_engine.say("Module one is now on")
                        output_queue.put("SET_ON")
                    elif command == "module one off":
                        audio_engine.say("Module one is now off")
                        output_queue.put("SET_OFF")
                    elif command == "module one toggle":
                        audio_engine.say("Module has been toggled")
                        output_queue.put("TOGGLE")
                    audio_engine.runAndWait()
                    for i in range(7):
                        audio_queue.get(timeout=2)
                        time.sleep(0.1)
                    print(f"Successfully found {command} with {score}")


if __name__ == "__main__":
    mp.set_start_method("spawn")
    audio_queue = mp.Queue()
    output_queue = mp.Queue()

    record_proc = mp.Process(target=record, args=(audio_queue,))
    transcribe_proc = mp.Process(target=transcribe, args=(audio_queue, output_queue,))

    record_proc.start()
    transcribe_proc.start()

    record_proc.join()
    transcribe_proc.join()
