#coding:utf-8
from Crypto.Cipher import AES
import time
import hashlib
import requests
import json
_md5=hashlib.md5()


secret="298204673dbbf749"
apiKey="06c2949cee984912ac49a75c13c00ae5"
url="http://www.tuling123.com/openapi/api"

#cmd="你好！"
#data="{\"key\":\""+apiKey+"\",\"info\":\""+cmd+"\"}"

#timestamp=str(int(time.time()))

#keyParam = secret+timestamp+apiKey

#_md5.update(keyParam)
#key=_md5.strdigest()

def chat(meg):
        payload={"key":apiKey,
                "info": meg,
                 "loc":"四川省成都市",
                 "userid":"123456"}

        r=requests.post(url,payload)
        text=json.loads(r.text)
        print text['code'],text['text']
        code=text['code']
        res=''
        if code==100000:
                res=text['text']
        if code==200000:
                res=text['text']+u'但是我们没办法显示给你'
        if code==302000:
                res=text['text']
                newslist=text['list']
                count=0
                for i in newslist:
                        count+=1
                        res+=u'来自'+i['source']+u'的新闻：'+i['article']+u'。'
                        if count >3:
                                break

        if code==308000:
                res=text['text']+text['list'][0]['name']+u',需要使用'+text['list'][0]['info']+u'。'

        print res
        return res



if __name__ == 'main':
        print "test the turing robot API!"
        payload={"key":apiKey,
        "info": "今天天气怎么样",
        "loc":"四川省成都市",
        "userid":"123456"}

        r=requests.post(url,payload)

        print r.text

