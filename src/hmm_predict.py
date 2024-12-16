import os
import pickle
import wave
import time

import numpy as np
import pyaudio
from pydub import AudioSegment
import preprocessing
from utils import get_all_words, get_word

class HMMRecognition:
    def __init__(self):
        self.model = {}

        self.class_names = get_all_words(tiny=True)
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
        print('Predicted word:', get_word(self.class_names[predict_word]))

    @staticmethod
    def record(record_folder = 'temp/record'):
        os.makedirs(record_folder, exist_ok=True)

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 22050
        RECORD_SECONDS = 2

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        print('recording ...')
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print('stopped record!')
        stream.stop_stream()
        stream.close()
        p.terminate()

        now_str = time.strftime("%Y%m%d_%H%M%S")

        record_path = f"{record_folder}/audio_{now_str}.wav"

        wf = wave.open(record_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print('record_path:', record_path)

        trimmed_path = HMMRecognition.strim_audio(record_path)

        return record_path, trimmed_path
    
    @staticmethod
    def strim_audio(record_path: str):
        audio = AudioSegment.from_file(record_path, format='wav')
        start_trim = HMMRecognition.detect_leading_silence(audio)
        end_trim = HMMRecognition.detect_leading_silence(audio.reverse())

        duration = len(audio)
        trimmed_sound = audio[start_trim:duration - end_trim]

        trimmed_path = record_path.replace('record', 'trimmed')
        os.makedirs(os.path.dirname(trimmed_path), exist_ok=True)
        trimmed_sound.export(trimmed_path, format='wav')

        return trimmed_path

if __name__ == '__main__':
    hmm_reg = HMMRecognition()
    word = get_word('bai')
    hmm_reg.predict(file_name=f'datasets/split/{word["word"]}/A{str(word["id"]).zfill(2)}.wav')

    # record_path, trimmed_path = HMMRecognition.record()
    # hmm_reg.predict(trimmed_path)