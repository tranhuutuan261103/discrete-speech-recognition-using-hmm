import math

import librosa
import numpy as np

def get_energy(y, sr, win_length, hop_length):
    energy = librosa.feature.rms(y=y, frame_length=win_length, hop_length=hop_length)
    return energy

def get_mfcc(file_path: str) -> np.ndarray:
    """
    Trích xuất đặc trưng MFCC từ một tệp .wav, bao gồm các đặc trưng MFCC gốc,
    Delta (bậc 1), và Delta-Delta (bậc 2). Đầu ra là ma trận T x 36 (số khung x số đặc trưng).
    
    Args:
        file_path (str): Đường dẫn tới tệp âm thanh (.wav).
    
    Returns:
        numpy.ndarray: Ma trận đặc trưng với kích thước T x 36.
    """
    y, sr = librosa.load(file_path)  # read .wav file

    # Pre-emphasis (tăng cường tần số cao)
    y_preemphasized = np.append(y[0], y[1:] - 0.95 * y[:-1])

    hop_length = math.floor(sr * 0.010)  # 10ms hop
    win_length = math.floor(sr * 0.025)  # 25ms frame
    # mfcc is 12 x T matrix
    mfcc = librosa.feature.mfcc(
        y=y_preemphasized, sr=sr, n_mfcc=12, n_fft=1024,
        hop_length=hop_length, win_length=win_length)
    
    energy = get_energy(y, sr, win_length, hop_length)
    if energy.shape[1] < mfcc.shape[1]:
        energy = np.pad(energy, ((0, 0), (0, mfcc.shape[1] - energy.shape[1])), mode='constant')
    elif energy.shape[1] > mfcc.shape[1]:
        mfcc = np.pad(mfcc, ((0, 0), (0, energy.shape[1] - mfcc.shape[1])), mode='constant')

    # add specific energy to MFCC
    mfcc = np.vstack((mfcc, energy))
    
    # subtract mean from mfcc --> normalize mfcc
    mfcc = mfcc - np.mean(mfcc, axis=1, keepdims=True)
    # delta feature 1st order and 2nd order
    delta1 = librosa.feature.delta(mfcc, order=1)
    delta2 = librosa.feature.delta(mfcc, order=2)
    # X is 36 x T
    X = np.concatenate([mfcc, delta1, delta2], axis=0)  # O^r
    # return T x 36 (transpose of X)
    return X.T  # hmmlearn use T x N matrix