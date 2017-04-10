#coding=utf-8
import wave
import json
import urllib2
import base64
import getAudio
import requests

import re

import test

from urllib2 import urlopen

import ctypes
import threading
import music_api
import time
import codecs

RATE=getAudio.RATE

"""
MWZ5zcIx5drugAMBx8Mu0rxO

Secret Key: 37f46c3dda263a26597f6af9ef44fe24
"""
def get_token():
    apiKey = "MWZ5zcIx5drugAMBx8Mu0rxO"
    secretKey = "37f46c3dda263a26597f6af9ef44fe24"

    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;

    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']

def mwrite(f,text,t0,t1,t2,t3,t4):
    #f.write(unicode((text+'\t'+str(t1-t0)+'\t'+str(t2-t1)+'\t'+str(t3-t2)+'\n'),'utf-8'))
    f.write(text+'\t'+str(t1-t0)+'\t'+str(t2-t1)+'\t'+str(t3-t2)+'\t'+str(t4-t3)+'\n')

mtoken=get_token()
choose=1



f = codecs.open("data.txt", "a", "utf-8")
align=ctypes.CDLL('mp3_decoder.so')

t=None

try:
    while 1:
        t0=time.time()
        getAudio.record_to_file("demo.wav")
        fp=wave.open("demo.wav",'rb')
        nf=fp.getnframes()
        f_len=nf*2
        audio_data = fp.readframes(nf)


        audio_data_base64=base64.b64encode(audio_data)


        header={#'Content-Type':'application/json',
            'Content-Type':' audio/pcm; rate=8000',
            'Content-Length': f_len
        }
        upload={'format':'wav',
                'rate':RATE,
                'channel':1,
                'token':mtoken,
                'cuid':'dangsugouitest',
                'len':f_len,
                'speech':audio_data_base64,
                }

        url='http://vop.baidu.com/server_api'

        t1=time.time()
        r=requests.post(url,data=json.dumps(upload),headers=header)
        text=json.loads(r.text)
        text=text['result'][0]
        t2=time.time()
        #print r
        print text



        p=re.compile(u"(我想听)(.*)([，。！；‘/])")

        match=p.match(text)
        if match:
            print match.lastindex,match.group(2)
            #music_api.play(match.group(2))
            t=threading.Thread(target=music_api.play,args=(match.group(2),))
            t.setDaemon(True)
            t.start()
            t3=time.time()
            mwrite(f,text,t0,t1,t2,t3,t3)
        else:
            res_text=test.chat(text)
            t3=time.time()
            url_text2audio="http://tsn.baidu.com/text2audio"

            '''upload_text2audio={'tex':res_text_utf,
                               'lan':'zh',
                               'tok':mtoken,
                               'ctp':'1',
                               'cuid':'dangsuoguitest',
                               }

            r=requests.post(url_text2audio,data=json.dumps(upload_text2audio))
            #r=requests.get(url_text2audio+"?"+"tex="+res_text+ "&lan=zh"+"&cuid=dangsuoguitest"+"&ctp=1&tok="+mtoken)
            print r.headers
            #print r.encoding
            buffer=r.text
            print buffer'''

            '''import pygame
            pygame.mixer.init()
            track = pygame.mixer.music.load(url_text2audio+"?"+"tex="+res_text+
                           "&lan=zh"+"&cuid=dangsuoguitest"+"&ctp=1&tok="+mtoken)
            pygame.mixer.music.play()'''



            #res_text=u"我是哈哈哈哈哈"
            res_text_utf=res_text.encode('utf-8')

            _res_text_utf=urllib2.quote(res_text_utf)
            #print "response:",res_text_utf
            user1="dddd"
            user2="aaaa"
            user=user1
            if choose==1:
                user=user2
                choose=0
            #print url_text2audio+"?"+"tex="+_res_text_utf+"&lan=zh"+"&cuid="+user+"&ctp=1&tok="+mtoken
            res=urlopen(url_text2audio+"?"+"tex="+_res_text_utf+"&lan=zh"+"&cuid="+user+"&ctp=1&tok="+mtoken)
            buffer=res.read()
            res_text_utf=None

            length=len(buffer)

            align.play_audio(buffer,length)
            t4=time.time()
            mwrite(f,text,t0,t1,t2,t3,t4)
except:
    f.close()

#f2=file(r"res.mp3",'wb')
#f2.write(buffer)
#f2.close()

'''
import pygame
pygame.mixer.init()
track = pygame.mixer.music.load("res.mp3")
pygame.mixer.music.play(1)'''


'''
import mp3play
mp3=mp3play.load("res.mp3")
mp3.play()
import time
time.sleep(10)
mp3.stop()'''

