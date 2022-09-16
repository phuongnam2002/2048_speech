import hmmlearn.hmm as hmm
import librosa
import numpy as np
import sounddevice as sd
import soundfile as sf


def record_sound(filename, duration=1, fs=44100, play=False):
    sd.play(np.sin(2 * np.pi * 940 * np.arange(fs) / fs), samplerate=fs, blocking=True)
    sd.play(np.zeros(int(fs * 0.2)), samplerate=fs, blocking=True)
    data = sd.rec(frames=duration * fs, samplerate=fs, channels=1, blocking=True)
    if play:
        sd.play(data, samplerate=fs, blocking=True)
    sf.write(filename, data=data, samplerate=fs)


def record_data(prefix, n=25, duration=1):
    for i in range(n):
        print('{}_{}.wav'.format(prefix, i))
        record_sound('{}_{}.wav'.format(prefix, i), duration=duration)
        if i % 5 == 4:
            input("Press Enter to continue...")


record_data('len')
record_data('xuong')


def get_mfcc(filename):
    data, fs = librosa.load(filename, sr=None)
    mfcc = librosa.feature.mfcc(data, sr=fs, n_fft=1024, hop_length=128)
    return mfcc.T


n_sample = 25
data_len = [get_mfcc('len_{}.wav'.format(i)) for i in range(n_sample)]
data_xuong = [get_mfcc('xuong_{}.wav'.format(i)) for i in range(n_sample)]

model_len = hmm.GaussianHMM(n_components=30, verbose=True, n_iter=200)
model_len.fit(X=np.vstack(data_len), lengths=[x.shape[0] for x in data_len])

model_xuong = hmm.GaussianHMM(n_components=30, verbose=True, n_iter=200)
model_xuong.fit(X=np.vstack(data_xuong), lengths=[x.shape[0] for x in data_xuong])

mfcc = get_mfcc('xuong_0.wav')
model_len.score(mfcc), model_xuong.score(mfcc)
