import sys
import socket
import base64
import datetime

verbose = True
V2 = True

def calcultateCheckSum(stringToCheck):
   xsum_calc = 0
   for char in stringToCheck:
      xsum_calc = xsum_calc ^ ord(char)
   return "%02X" % xsum_calc

def getGGABytes():
   now = datetime.datetime.utcnow()
   ggaString= "GPGGA,%02d%02d%04.2f,3734.087,N,12702.603,E,1,12,1.0,0.0,M,0.0,M,," % \
      (now.hour,now.minute,now.second)

   checksum = calcultateCheckSum(ggaString)
   # if self.verbose:
   #    print  ("$%s*%s\r\n" % (ggaString, checksum))
   return bytes("$%s*%s\r\n" % (ggaString, checksum),'ascii')

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

target_host = "www.gnssdata.or.kr" 
target_port = 2101  # create a socket object 
mountpoint = "SOUL-RTCM31"
useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
user = "tge1375@naver.com:gnss"

target_host = "fkp.ngii.go.kr" 
target_port = 2201  # create a socket object 
mountpoint = "VRS_V32"
useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
user = "tge1375@naver.com:gnss"

# user = base64.b64encode(bytes(user,'utf-8')).decode("utf-8")

found_header = False

try:
   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

   error_indicator = client.connect_ex((target_host,target_port))
   if error_indicator == 0:
      sleepTime = 1
      connectTime=datetime.datetime.now()

      client.settimeout(10)
      client.send(getMountPointBytes(mountpoint, useragent, user).encode())
      while not found_header:
         casterResponse = client.recv(4096) #All the data
         header_lines = casterResponse.decode('utf-8').split("\r\n")
         print(header_lines)

         for line in header_lines:
            if line=="":
               if not found_header:
                  found_header=True
                  # if self.verbose:
                  #       sys.stderr.write("End Of Header"+"\n")
            # else:
            #    if self.verbose:
            #       sys.stderr.write("Header: " + line+"\n")
            # if self.headerOutput:
            #    self.headerFile.write(line+"\n")

         for line in header_lines:
            if line.find("SOURCETABLE")>=0:
               sys.stderr.write("Mount point does not exist")
               sys.exit(1)
            elif line.find("401 Unauthorized")>=0:
               sys.stderr.write("Unauthorized request\n")
               sys.exit(1)
            elif line.find("404 Not Found")>=0:
               sys.stderr.write("Mount Point does not exist\n")
               sys.exit(2)
            elif line.find("ICY 200 OK")>=0:
               #Request was valid
               client.sendall(getGGABytes())
            elif line.find("HTTP/1.0 200 OK")>=0:
               #Request was valid
               client.sendall(getGGABytes())
            elif line.find("HTTP/1.1 200 OK")>=0:
               #Request was valid
               client.sendall(getGGABytes())


      data = "Initial data"
      while data:
         try:
            data = client.recv(50)
            print(data)
            # self.out.write(data)
            # self.out.buffer.write(data)
            # if self.UDP_socket:
            #    self.UDP_socket.sendto(data, ('<broadcast>', self.UDP_Port))
            # if self.maxConnectTime :
            #    if datetime.datetime.now() > connectTime+EndConnect:
            #       if self.verbose:
            #             sys.stderr.write("Connection Time exceeded\n")
            #       sys.exit(0)
            # self.socket.sendall(self.getGGAString())
         except socket.timeout:
               # if self.verbose:
               #    sys.stderr.write('Connection TimedOut\n')
               data = False
         except socket.error:
               # if self.verbose:
               #    sys.stderr.write('Connection Error\n')
               data = False


except KeyboardInterrupt:
   if client:
      client.close()
   sys.exit()


client.close()
