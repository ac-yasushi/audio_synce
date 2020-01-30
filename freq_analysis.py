# -*- coding: utf-8 -*-

import numpy as np
import pyaudio
import matplotlib.pyplot as plt


def rec_audio():
    rec_time = 1            # 録音時間[s]
    size=2**12

    fmt = pyaudio.paInt16  # 音声のフォーマット
    ch = 1              # チャンネル1(モノラル)
    sampling_rate = 44100 # サンプリング周波数
    chunk = 2**11       # チャンク（データ点数）
    audio = pyaudio.PyAudio()
    index = 1 # 録音デバイスのインデックス番号（デフォルト1）

    stream = audio.open(format=fmt, channels=ch, rate=sampling_rate, input=True,
                        input_device_index = index,
                        frames_per_buffer=chunk)
    # 録音処理
    frames = np.array([])
    for i in range(0, int(sampling_rate / chunk * rec_time)):
        data = stream.read(chunk)
        frames=np.append(frames, data)

    # 録音終了処理
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    ndarray_from_byte=np.frombuffer(frames, dtype=np.int16)
    
    hammingWindow = np.hamming(size)    # ハミング窓
    fs = 44100 #サンプリングレート
    d = 1.0 / fs #サンプリングレートの逆数
    freqList = np.fft.fftfreq(size, d)
    
    
    st=0
    windowedData = hammingWindow * ndarray_from_byte[st:st+size]  # 切り出した波形データ（窓関数あり）
    sample_data = np.fft.fft(windowedData)
    sample_data = sample_data / max(abs(sample_data)) # 0~1正規化
        

    return freqList, sample_data


if __name__ == "__main__":
    
    freq, data=rec_audio()
    
    plt.plot(freq, abs(data))
         
    plt.axis([0,44100/8,0,1]) #第二引数でグラフのy軸方向の範囲指定
    plt.title("audio_FFT_data")
    plt.xlabel("Frequency[Hz]")
    plt.ylabel("amplitude spectrum")
    plt.show()