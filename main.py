#coding:utf-8
'''
import urllib2
import json
from urllib2 import urlopen
import ctypes
def get_token():
    apiKey = "MWZ5zcIx5drugAMBx8Mu0rxO"
    secretKey = "37f46c3dda263a26597f6af9ef44fe24"

    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;

    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']
mtoken=get_token()
url_text2audio="http://tsn.baidu.com/text2audio"


while 1:
    res_text=u"我是哈哈哈哈哈"
    res_text_utf=res_text.encode('utf-8')

    _res_text_utf=urllib2.quote(res_text_utf)
    user='dssds'
    res=urlopen(url_text2audio+"?"+"tex="+_res_text_utf+"&lan=zh"+"&cuid="+user+"&ctp=1&tok="+mtoken)
    buffer=res.read()
    res_text_utf=None

    length=len(buffer)
    print length
    align=ctypes.cdll.LoadLibrary('mp3_decoder.so')
    align.play_audio(buffer,length)
    buffer=None
    align=None'''

import re
import codecs
f=codecs.open('data.txt','r','utf-8')

text=f.read()
#print text
f.close()
p=re.compile("(\d*\.\d*)")#u"(.*)[，？ ]*([0-9]*.[0-9]*) *([0-9]*.[0-9]*) *([0-9]*.[0-9]*) *([0-9]*.[0-9]*)\\n

match=p.findall(text)
if match:
    print match
y={'a':[],'b':[],'c':[],'d':[]}
i=0
print len(match)
while i < len(match):
   y['a'].append(float(match[i+0]))
   y['b'].append(float(match[i+1]))
   y['c'].append(float(match[i+2]))
   y['d'].append(float(match[i+3]))
   i=i+4
import matplotlib.pyplot as plt
import numpy as np
x=np.arange(0,len(y['a']),1)
plt.axis([0,60,0,50])
plt.xlabel("count")
plt.ylabel("time")
plt.title("time coat")
p1=plt.plot(x,y['a'])
p2=plt.plot(x,y['b'])
p3=plt.plot(x,y['c'])
p4=plt.plot(x,y['d'])
l1=plt.legend(p1,["read audio",] ,loc='upper left')
l2=plt.legend(p2,["audio to text",], loc='upper right')
l3=plt.legend(p3,["chat",], loc='upper center')
l4=plt.legend(p4,["play",], loc='lower right')
plt.gca().add_artist(l1)
plt.gca().add_artist(l2)
plt.gca().add_artist(l3)
plt.gca().add_artist(l4)

#plt.legend((p1,p2,p3,p4,), ["read audio","audio to text","chat","play",], loc='best')
plt.show()