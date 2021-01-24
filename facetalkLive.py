import pyaudio
import wave
import numpy as np
from datetime import datetime
import cv2
from pynput.keyboard import Key, Listener
import threading
import time

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

ontalk = cv2.imread("ontalk.png")
offtalk = cv2.imread("offtalk.png")
cry = cv2.imread("cry.png")
hert = cv2.imread("hert.png")
oko = cv2.imread("oko.png")
wao = cv2.imread("wao.png")
kutibue = cv2.imread("kutibue.png")
mabataki = cv2.imread("mabataki.png")
sleepimg = cv2.imread("sleep.png")

threshold = 0.08
p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = chunk
)

print(ontalk)

facenum = 0

def keylog():
    def on_press(key):
        global facenum
        #print(key.char)
        try:
            if key.char == '1':
                facenum = 1
                print('INFO: 表情「泣く」を表示しています。')
            elif key.char == '2':
                facenum = 2
                print('INFO: 表情「好き」を表示しています。')
            elif key.char == '3':
                facenum = 3
                print('INFO: 表情「怒る」を表示しています。')
            elif key.char == '4':
                facenum = 4
                print('INFO: 表情「驚く」を表示しています。')
            elif key.char == '5':
                facenum = 5
                print('INFO: 表情「口笛」を表示しています。')
            elif key.char == '6':
                facenum = 6
                print('INFO: 表情「睡眠」を表示しています。')
            else:print('DEBUG: {0}キーが押されました。'.format(key.char))
            '''
            elif key.char == '7':facenum = 7
            elif key.char == '8':facenum = 8
            elif key.char == '9':facenum = 9
            '''
        except:
            print('DEBUG: {0}キーが押されました。'.format(key))
    def on_release(key):
        global facenum
        facenum = 0        
    with Listener(
        on_press = on_press,
        on_release= on_release
    ) as listener:
        listener.join()
    print('スレッドが終了しました。')

th = threading.Thread(target=keylog)
th.setDaemon(True) 
th.start()

cnt = 0
waitcnt = 0

while True:
    cnt += 1
    data = stream.read(chunk)
    x = np.frombuffer(data, dtype="int16") / 32768.0
    if facenum == 0:
        if x.max() > threshold:
            cv2.imshow('FacetalkLive',ontalk)
            print('INFO: あなたが喋っているのを検知しました。')
        else:
            if cnt >= 350:
                cv2.imshow('FacetalkLive',mabataki)
                cv2.waitKey(250)
                cnt = 0
                waitcnt = 1
            else:
                cv2.imshow('FacetalkLive',offtalk)
    elif facenum == 1:
        cv2.imshow('FacetalkLive',cry)
    elif facenum == 2:
        cv2.imshow('FacetalkLive',hert)
    elif facenum == 3:
        cv2.imshow('FacetalkLive',oko)
    elif facenum == 4:
        cv2.imshow('FacetalkLive',wao)
    elif facenum == 5:
        cv2.imshow('FacetalkLive',kutibue)
    elif facenum == 6:
        cv2.imshow('FacetalkLive',sleepimg)
    if waitcnt == 0:
        k = cv2.waitKey(1)
    else:
        print('INFO: まばたきを行います。')
        waitcnt = 0
    if k == 27:
        break

stream.close()
p.terminate()
cv2.destroyAllWindows()
exit()
