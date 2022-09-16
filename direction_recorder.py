import numpy as np
import sounddevice as sd
import soundfile as sf


def record_sound(filename, duration=50, fs=44100):
    print("Recording %s..." % filename)
    sd.play(np.sin(2 * np.pi * 940 * np.arange(fs) / fs), samplerate=fs, blocking=True)
    sd.play(np.zeros(int(fs * 0.2)), samplerate=fs, blocking=True)
    data = sd.rec(frames=duration * fs, samplerate=fs, channels=1, blocking=True)
    sf.write(filename, data=data, samplerate=fs)
    print("Done")


record_sound("left.wav")
