#coding: utf-8

import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import struct

sound_time=3
fs=44100

wave_strength=1.0
f0=440

wave_data=np.array([i/fs for i in range(sound_time*fs)])

sin_wave=wave_strength*np.sin(2*np.pi*f0*wave_data)

print(type(sin_wave))

for i in range(len(sin_wave)):
    if sin_wave[i]>1: sin_wave[i]=1
    if sin_wave[i]<-1: sin_wave[i]=-1

# [-32768, 32767]の整数値に変換
sin_wave = [int(x * 32767.0) for x in sin_wave]

# バイナリに変換
data = struct.pack("h" * len(sin_wave), *sin_wave)  # listに*をつけると引数展開される



p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=int(fs),
                output= True)
# チャンク単位でストリームに出力し音声を再生
chunk = 1024
sp = 0  # 再生位置ポインタ
buffer = data[sp:sp+chunk]
while buffer != '':
    stream.write(buffer)
    sp = sp + chunk
    buffer = data[sp:sp+chunk]
stream.close()
p.terminate()