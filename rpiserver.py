import socket
import threading

class Streamer(threading.Thread):
    def __init__(self, hostname, port):
        threading.Thread.__init__(self)
        self.hostname = hostname
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
        #self.running = False
        #self.streaming = False
        #self.s = s
        #self.payload_size = payload_size
    def run(self):
        self.doConnect()
        #self.running = True
        while True:
            print('Start listening for connections...')
            self.conn, addr = self.s.accept()
            print("New connection accepted.")
            data = self.conn.recv(1024)
             #print(data.decode())
            if data:
                if data.decode()=='left':
                    print('left')
            else:
                break
        print('Exit thread.')
        
    def  doConnect(self):
        while True:
            try:
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        self.conn.sendall(outdata.encode())

    def getgps(self,code):
        outdata = str(code)
        try:
            self.conn.sendall(outdata.encode())
            #print(code)
            self.conn.settimeout(2.0)
            indata = self.conn.recv(1024)
            print(indata.decode())
            if indata:
                code = indata.decode()
        except:
            self.doConnect()
            #pass
        return code
