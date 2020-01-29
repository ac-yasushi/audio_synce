#coding: utf-8

import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import struct
import sys


def sin_wave(helz, strength, time):

    fs=44100

    if type(time) != int:
        print("time must be integer.")
        sys.exit()

    time_data=np.array([i/fs for i in range(time*fs)])

    wave_data=strength*np.sin(2*np.pi*helz*time_data)

    #print(type(sin_wave))

    return time_data, wave_data


def data_to_binary(wave_data):

    wave_data=wave_data/np.max(abs(wave_data))
    
    #print(np.max(wave_data), np.min(wave_data))

    # [-32768, 32767]の整数値に変換
    wave_data = [int(x * 32767.0) for x in wave_data]

    # バイナリに変換
    data = struct.pack("h" * len(wave_data), *wave_data)  # listに*をつけると引数展開される

    return data


def play_data(data):

    fs=44100

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=int(fs),
                    output= True)
    # チャンク単位でストリームに出力し音声を再生
    chunk = 1024
    sp = 0  # 再生位置ポインタ
    buffer = data[sp:sp+chunk]
    while len(buffer) >= chunk:
        stream.write(buffer)
        sp = sp + chunk
        buffer = data[sp:sp+chunk]
    stream.close()
    p.terminate()

    return


if __name__=="__main__":

    wave_strength=1.5
    f0=440
    sound_time=2

    timeline_data, wave_data=sin_wave(f0, wave_strength, sound_time)

    f1=880
    f2=1320
    add_wave1=sin_wave(f1, 0.5, sound_time)[1]
    add_wave2=sin_wave(f2, 0.25, sound_time)[1]

    wave_data = add_wave1 + add_wave2 + wave_data

    plt.plot(timeline_data, wave_data)
    plt.xlim(0, 0.01)
    plt.show()

    wave_data=data_to_binary(wave_data)

    play_data(wave_data)
