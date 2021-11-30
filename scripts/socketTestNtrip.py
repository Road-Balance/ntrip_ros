import socket
import base64
import datetime

verbose = True
V2 = True

def getMountPointBytes(mountpoint, useragent, user):
   mountPointString = "GET %s HTTP/1.1\r\nUser-Agent: %s\r\nAuthorization: Basic %s\r\n" % (mountpoint, useragent, user)
#        mountPointString = "GET %s HTTP/1.1\r\nUser-Agent: %s\r\n" % (self.mountpoint, useragent)
   # if self.host or self.V2:
   #    hostString = "Host: %s:%i\r\n" % (self.caster,self.port)
   #    mountPointString+=hostString
   if V2:
      mountPointString+="Ntrip-Version: Ntrip/2.0\r\n"
   mountPointString+="\r\n"
   if verbose:
      print(mountPointString)
   return mountPointString
   # return bytes(mountPointString,'ascii')

target_host = "gnssdata.or.kr" 
target_port = 2101  # create a socket object 
mountpoint = "SOUL-RTCM23"
useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
user = "tge1375@naver.com:gnss"

target_host = "fkp.ngii.go.kr" 
target_port = 2201  # create a socket object 
mountpoint = "SOUL-RTCM23"
useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
user = "tge1375@naver.com:gnss"

# user = base64.b64encode(bytes(user,'utf-8')).decode("utf-8")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

error_indicator = client.connect_ex((target_host,target_port))
if error_indicator == 0:
   sleepTime = 1
   connectTime=datetime.datetime.now()

   client.settimeout(10)
   # client.sendall(getMountPointBytes(mountpoint, useragent, user))
   client.send(getMountPointBytes(mountpoint, useragent, user).encode())

   toggle = True
   while toggle:
      casterResponse = client.recv(4096) #All the data
      header_lines = casterResponse.decode('utf-8').split("\r\n")
      print(header_lines)

      toggle = not toggle

client.close()
