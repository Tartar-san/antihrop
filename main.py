from sys import byteorder
from array import array
from struct import pack
from datetime import datetime

import pyaudio
import wave


THRESHOLD = 8000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')

    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in xrange(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in xrange(int(seconds*RATE))])
    return r



def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def record_to_file(path, sample_width, data):
    "Records from the microphone and outputs the resulting data to 'path'"
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def main():
    while 1:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=1, rate=RATE,
            input=True, output=True,
            frames_per_buffer=CHUNK_SIZE)
        num_snoaring = 0
        num_silent = 0
        snd_started = False
        r = array('h')
        print("Waiting for your snoring")
        print("_________________________")
        while 1:
            # little endian, signed short
            snd_data = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = is_silent(snd_data)
 
            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True
                print("You are snoring... ZZzzZzzzZ!")
            elif not silent and snd_started:
                num_snoaring += 1
            if snd_started and num_silent > 1000:
                break
    
        sample_width = p.get_sample_size(FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        r = normalize(r)
        r = trim(r)
        r = add_silence(r, 0.5)
        record_to_file(str(datetime.now())+".wav", sample_width, r)
        
if __name__ == '__main__':
    main()

