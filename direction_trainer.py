import pickle
import numpy as np
import librosa
import hmmlearn.hmm as hmm
from math import exp


def load_mfcc(fileName):
    data, fs = librosa.load(fileName, sr=None)
    mfcc = librosa.feature.mfcc(data, sr=fs, n_fft=1024, hop_length=128)
    return mfcc.T


def build_model(prefix, numSample, duration):
    print("Loading model %s, %d samples of duration %ds..." % (prefix, numSample, duration))
    data = [load_mfcc("%ds/%s_%02d.wav" % (duration, prefix, i + 1)) for i in range(numSample)]
    model = hmm.GaussianHMM(n_components=50, verbose=True, n_iter=150)
    model.fit(X=np.vstack(data), lengths=[x.shape[0] for x in data])
    with open("%s.model" % prefix, "wb") as model_file: pickle.dump(model, model_file)


build_model("up", 50, 1)
build_model("down", 50, 1)
build_model("left", 50, 1)
build_model("right", 50, 1)
