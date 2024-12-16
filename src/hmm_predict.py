import os
import pickle
import wave
import time

import numpy as np
import pyaudio
from pydub import AudioSegment
import preprocessing
from utils import get_all_words

class HMMRecognition:
    def __init__(self):
        self.model = {}

        self.class_names = get_all_words()
        self.audio_format = 'wav'

        self.model_path = 'models/demo'

        self.load_model()

    @staticmethod
    def detect_leading_silence(sound, silence_threshold=-42.0, chunk_size=10):
        trim_ms = 0  # ms

        assert chunk_size > 0  # to avoid infinite loop
        while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
            trim_ms += chunk_size

        return trim_ms
    
    def load_model(self):
        for key in self.class_names:
            name = f"{self.model_path}/model_{key}.pkl"
            with open(name, 'rb') as file:
                self.model[key] = pickle.load(file)

    def predict(self, file_name: str):
        # Predict
        record_mfcc = preprocessing.get_mfcc(file_name)
        scores = [self.model[cname].score(record_mfcc) for cname in self.class_names]
        print('scores', scores)
        predict_word = np.argmax(scores)
        print(self.class_names[predict_word])

if __name__ == '__main__':
    hmm_reg = HMMRecognition()
    hmm_reg.predict(file_name='datasets/split/co/A34.wav')