# I removed all the commented-out old parts/attempts (I still have the old version)
# However all the imports ever used are here

from numpy import real_if_close # I don't remember why this is here
import pyaudio
import wave
import vosk
import soundfile
import json
import time
from metaphone import doublemetaphone
from Levenshtein import ratio
from rapidfuzz import fuzz
from threading import Thread
from multiprocessing import Process, Value

def record(written):
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    chunk = 1024
    seconds = 5
    filename = "recording.wav"
    audio = pyaudio.PyAudio()
    while True:
        print("Recording...")

        stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

        frames = []

        for i in range(0, int(rate / chunk * seconds)): # Recording for X seconds (5 currently)
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        print("Recording stopped")

        with wave.open(filename, "wb") as wf: # Writing to .wave file
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        print(f"Recording saved in {filename}\n")
        written.value = False


def metaphone_string(text): # Simplifying metaphone later
    words = text.lower().split()
    return ' '.join([doublemetaphone(word)[0] for word in words])

def comparison(transcribed, find, threshold=80):
    find_meta = metaphone_string(find)
    transcribed_meta = metaphone_string(transcribed)

    similarity = fuzz.partial_ratio(transcribed_meta, find_meta) # Partial ratio checks the entire string for the phrase and reports similarity
    # Previously similarity comparison was by two words

    print(f"Current similarity is {similarity}") # More for debugging purposes

    if similarity >= threshold:
        return True, similarity
    
    return False, 0

def transcribe(written):
    model = vosk.Model("vosk-model-en-us-0.22") # Vosk model directory is in the same directory as the file
    filename = "recording.wav"
    commands = "lights off"
    while True:
        if written.value == True:
            time.sleep(0.5)
            continue
        else:
            vosk_data, samplerate = soundfile.read(filename)
            soundfile.write(filename, vosk_data, samplerate)
            with wave.open(filename, "rb") as wav_file:
                rec = vosk.KaldiRecognizer(model, wav_file.getframerate())
                texts = []
                while True:
                    check = wav_file.readframes(4000)
                    if len(check) == 0:
                        break
                    if rec.AcceptWaveform(check):
                        result = json.loads(rec.Result())
                        texts.append(result["text"])
            texts = " ".join(texts)
            with open("output.txt", "w") as fl:
                fl.write(texts)
                print("File written successfully")
            print(texts)
            written.value = True
            found, score = comparison(texts, commands, 80)
            print(f"Score is {score}")
            if found == True:
                print(f"Successfully found '{commands}' with a score of {score}")


if __name__ == "__main__":
    written_flag = Value('b', True) # Written variable across processes to check if recording has been transcribed or not (utilize less resources)

    record_proc = Process(target=record, args=(written_flag,))
    transcribe_proc = Process(target=transcribe, args=(written_flag,))

    record_proc.start()
    transcribe_proc.start()

    record_proc.join()
    transcribe_proc.join()

