import math
import librosa
import numpy as np

def get_mfcc(file_path):
    y, sr = librosa.load(file_path) 
    hop_length = math.floor(sr * 0.015)  # 15ms hop
    win_length = math.floor(sr * 0.030)  # 30ms frame

    # Trích xuất MFCC
    mfcc = librosa.feature.mfcc(
        y=y, sr=sr, n_mfcc=12, n_fft=1024,
        hop_length=hop_length, win_length=win_length)
    
    # Trích xuất thành phần năng lượng và khớp kích thước
    energy = librosa.feature.rms(y=y, frame_length=win_length, hop_length=hop_length)
    if energy.shape[1] < mfcc.shape[1]:
        energy = np.pad(energy, ((0, 0), (0, mfcc.shape[1] - energy.shape[1])), mode='constant')
    elif energy.shape[1] > mfcc.shape[1]:
        mfcc = np.pad(mfcc, ((0, 0), (0, energy.shape[1] - mfcc.shape[1])), mode='constant')

    
    # Thêm thành phần năng lượng vào MFCC
    mfcc = np.vstack((mfcc, energy))

    # Chuẩn hóa MFCC bằng cách trừ đi giá trị trung bình
    mfcc = mfcc - np.mean(mfcc, axis=1).reshape((-1, 1))
    
    
    # Tính các hệ số delta và acceleration
    delta1 = librosa.feature.delta(mfcc, order=1)  # Đạo hàm bậc 1
    delta2 = librosa.feature.delta(mfcc, order=2)  # Đạo hàm bậc 2

        
    # Gộp MFCC, delta1, và delta2 lại thành một ma trận
    X = np.concatenate([mfcc, delta1, delta2], axis=0)  # Kết quả là ma trận (số đặc trưng, số khung)
    
    # Kết quả sẽ có kích thước (số khung, 39), phù hợp với định dạng mà hmmlearn yêu cầu (T x N), 
    # trong đó 
        # T là số khung thời gian
        # N là số đặc trưng
    return X.T
