import pickle
import sys
import librosa
import numpy as np
import sounddevice as sd
import soundfile as sf


def record_sound(fileName, duration=1, fs=44100):
    sd.play(np.sin(2 * np.pi * 940 * np.arange(fs) / fs), samplerate=fs, blocking=True)
    sd.play(np.zeros(int(fs * 0.2)), samplerate=fs, blocking=True)
    data = sd.rec(frames=duration * fs, samplerate=fs, channels=1, blocking=True)
    sf.write(fileName, data=data, samplerate=fs)


def load_mfcc(fileName):
    data, fs = librosa.load(fileName, sr=None)
    mfcc = librosa.feature.mfcc(data, sr=fs, n_fft=1024, hop_length=128)
    return mfcc.T


def load_model(prefix):
    print("Loading model %s..." % prefix, file=sys.stderr)
    fileName = "%s.model" % prefix
    with open(fileName, "rb") as model_file:
        model = pickle.load(model_file)
        return model


def get_direction(dirs, models):
    inputFile = "input.wav"
    record_sound(inputFile, duration=1)
    mfcc = load_mfcc(inputFile)

    score = [models[i].score(mfcc) for i in range(4)]
    print(score, file=sys.stderr)
    best = 0
    for i in range(4):
        if score[i] > score[best]:
            best = i
    print(dirs[best], file=sys.stderr)
    return best


dirs = ["left", "up", "right", "down"]
models = [load_model(prefix) for prefix in dirs]

while (True):
    print("Processing...", file=sys.stderr)
    state = int(input())
    print(state, file=sys.stderr)
    if state == "-1":
        sys.exit(0)

    print("Waiting for moves...", file=sys.stderr)
    print(get_direction(dirs, models))
