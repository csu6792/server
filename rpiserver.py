import socket
import threading



def recvall(sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    
class Streamer(threading.Thread):
    def __init__(self, hostname, port):
    #def __init__(self):
        threading.Thread.__init__(self)
        self.hostname = hostname
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
    def run(self):
        self.doConnect()
        #self.running = True
        while True:
            print('Start listening for connections...')
            try:
               self.conn, addr = self.s.accept()
               print("New connection accepted.")
               try:
                   data = self.conn.recv(1024)
                #print(data.decode())
                   '''if data:
                       if data.decode()=='left':
                           print('left')
                    else:
                       break'''
               except:
                   self.doConnect()
                   print('client disconnect')
                   #break
            except:
               print('wait client')
               pass
        print('Exit thread.')
        
    def  doConnect(self):
        while True:
            try:
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                #self.s.setblocking(False)
                self.s.bind((self.hostname, self.port))
                print('Socket bind complete')
                #self.payload_size = struct.calcsize("Q")
                self.s.listen(10)
                print('Socket now listening')
                break
            except:
                pass
        
    def sendmessage(self,message):
        outdata = str(message)
        try:
           self.conn.settimeout(2.0)
           self.conn.sendall(outdata.encode())
           return 'ok'
        except:
           return 'error'

    def getjpg(self,code):
        outdata = 'checkjpg'
        checkdata = 'getjpg'
        self.conn.settimeout(2.0)
        self.conn.sendall(outdata.encode())
        length = recvall(self.conn, 64)
        print(type(length),length)
        length1 = length.decode('utf-8')
        self.conn.sendall(checkdata.encode())
        stringData = recvall(self.conn, int(length1))
        print(stringData)
        return 'ok'
        
        
    def getgps(self,code):
        outdata = str(code)
        self.conn.sendall(outdata.encode())
        #print(code)
        self.conn.settimeout(2.0)
        indata = self.conn.recv(1024)
        #print(indata.decode())
        if indata:
            code = indata.decode()
        '''try:
            self.conn.sendall(outdata.encode())
            #print(code)
            self.conn.settimeout(2.0)
            indata = self.conn.recv(1024)
            print(indata.decode())
            if indata:
                code = indata.decode()
        except:
            self.doConnect()'''
            #pass
        return code
