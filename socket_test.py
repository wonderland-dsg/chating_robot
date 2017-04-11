import socket
from array import array
import getAudio
IP_PORT=("192.168.4.138",8080)

web=socket.socket()
reuse=5
web.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, reuse)
web.bind(IP_PORT)


web.listen(500)
conn=None
corr_flag=0
r = array('h')
data=[]
try:
    print "begin listen..."
    conn,addr=web.accept()
    
    rece=conn.recv(10)
    if(len(rece)!=4):
        print "header error:",len(rece)
    i=0
    data=rece
    print len(rece)
    if(ord(data[i+0])==0xAA and ord(data[i+1])==0xAB and ord(data[i+2])==0xAC and ord(data[i+3])==0xAD):
        conn.send("you can send!\r\n")
        rece=conn.recv(1024)
        while(len(rece)>0):
            print "len:",len(rece)
            j=0
            while((j+1)<len(rece)):
                d=(ord(rece[j+1])+256*ord(rece[j]))
                if(d>32767):
                    d=d-65535
                print d
                r.append(d)
                j=j+2
            rece=conn.recv(1024)

    '''while True:
        rece=conn.recv(32*1024)
        i=0
        print "receive from:",addr,"len:",len(rece)
        data.extend(rece)
        if(len(data)>1024*16):
            while(i<len(data)):
                if(ord(data[i+0])==0xAA and ord(data[i+1])==0xAB and ord(data[i+2])==0xAC and ord(data[i+3])==0xAD):
                    i=i+4
                    corr_flag=1
                    break
                else:
                    i=i+1

            while((i+2)<len(data)):
                d=(ord(data[i])+256*ord(data[i+1]))
                if(d>32767):
                    d=d-65535
                r.append(d)
                print "%x %x %d" %(ord(data[i]),ord(data[i+1]),d)
                i=i+2
            data=[]'''
except:
    print "store!"
    getAudio.record_to_file2(2,r,"test4.wav")
    conn.close()
