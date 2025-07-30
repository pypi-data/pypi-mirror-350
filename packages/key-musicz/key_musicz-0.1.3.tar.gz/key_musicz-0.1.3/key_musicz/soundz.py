#coding=utf-8

import pyaudio
import numpy as np
import math

nbyte = 2
ndtype = np.int16

p = pyaudio.PyAudio()
def create(rate):
    return p.open(format=p.get_format_from_width(nbyte), channels=1, rate=rate, output=True)

pass

def close(stream):
    stream.stop_stream()
    stream.close()

pass

def release():
    p.terminate()

pass


class Sound:
    def __init__(self, stream = None, rate=327680):
        #print(f"sound rate:", rate)
        if stream is None:
            stream = create(rate)
        self.stream = stream
    def start(self):
        pass
    def add(self, data):
        if type(data)!=bytes:
            data = data.tobytes()
        self.stream.write(data)
    def close(self):
        close(self.stream)
        release()

pass