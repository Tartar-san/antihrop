from sys import byteorder
from array import array
from struct import pack
from datetime import datetime
from recognizer import recognizeSnore
from client import RESTClient
from random import randint

import math
import pygame
import pyaudio
import wave


THRESHOLD = 9000
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

def play_music(volume=0.2, sound_file="file.wav"):
    #play prepared audiofile
    pygame.mixer.init()
    s = pygame.mixer.Sound(sound_file)
    s.play()
    pygame.time.wait(int(math.ceil(s.get_length()*1000)))
    
def send_json():
    pass

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
    jsonder = RESTClient("localhost", 8000, "/api/hraps")
    volume = 0
    snor_iteration = 0
    start_of_snor = 0
    end_of_snor = 0
    while 1:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=1, rate=RATE,
            input=True, output=True,
            frames_per_buffer=CHUNK_SIZE)
        num_snoaring = 0
        num_silent = 0
        silent = True
        r = array('h')
        print("Waiting for your snoring")
        print("_________________________")
        
        #waiting for sound
        while silent:
            snd_data = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)
            silent = is_silent(snd_data)
        start_time = datetime.now()
        print("You snored at" + str(start_time))
        #record snor or something for 10 seconds
        while (datetime.now()-start_time).total_seconds() < 10:
            snd_data = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)
            
        sample_width = p.get_sample_size(FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        r = normalize(r)
        r = trim(r)
        r = add_silence(r, 0.5)
        record_to_file("1.wav", sample_width, r)
        
        snor = recognizeSnore("1.wav")
        
        if snor:
            if snor_iteration == 0:
                start_of_snor = datetime.now()
            print("TRUE")
            volume += 0.1
            snor_iteration += 1
            #play_music(volume, "file-0"+str(snor_iteration)+".wav")
        else:
            if snor_iteration != 0:
                data_dict = {}
                end_of_snor = datetime.now()
                data_dict["time"] = start_of_snor
                data_dict["period"] = (end_of_snor-start_of_snor).total_seconds()
                data_dict["response"] = (end_of_snor-start_of_snor).total_seconds()-10
                data_dict["intensity"] = randint(30,90)
                data_dict["track_name"] = "Edward Grieg - Morning"
                data_dict["volume_track"] = volume * 100
                jsonder.send_data_in_POST(data_dict)
            volume = 0
            snor_iteration = 0
        
if __name__ == '__main__':
    main()

