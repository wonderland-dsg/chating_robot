import wave
import json
import urllib2
import base64
import getAudio
import requests


import test


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

getAudio.record_to_file("demo.wav")
fp=wave.open("demo.wav",'rb')
nf=fp.getnframes()
f_len=nf*2
audio_data = fp.readframes(nf)


audio_data_base64=base64.b64encode(audio_data)

mtoken=get_token()

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

r=requests.post(url,data=json.dumps(upload),headers=header)
text=json.loads(r.text)
text=text['result'][0]
print r
print text

res_text=test.chat(text)
 


url_text2audio="http://tsn.baidu.com/text2audio"
upload_text2audio={'tex':res_text,
        'lan':'zh',
        'tok':mtoken,
        'ctp':'1',
        'cuid':'dangsuoguitest',
}

#r=requests.post(url_text2audio,data=json.dumps(upload_text2audio))
r=requests.get(url_text2audio+"?"+"tex="+res_text+
               "&lan=zh"+"&cuid=dangsuoguitest"+"&ctp=1&tok="+mtoken)
#print r.headers
#print r.encoding

'''import pygame
pygame.mixer.init()
track = pygame.mixer.music.load(url_text2audio+"?"+"tex="+res_text+
               "&lan=zh"+"&cuid=dangsuoguitest"+"&ctp=1&tok="+mtoken)
pygame.mixer.music.play()'''


from urllib2 import urlopen

res_text_utf=res_text.encode('utf-8')
res_text_utf=urllib2.quote(res_text_utf)
res=urlopen(url_text2audio+"?"+"tex="+res_text_utf+"&lan=zh"+"&cuid=dangsuoguitest"+"&ctp=1&tok="+mtoken)
buffer=res.read()

length=len(buffer)
import ctypes
align=ctypes.CDLL('mp3_decoder.so')
align.play_audio(buffer,length)



f=file(r"res.mp3",'wb')
f.write(buffer)
f.close()

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

