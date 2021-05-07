import socket
import threading


class Streamer(threading.Thread):

    def __init__(self, hostname, port):
        threading.Thread.__init__(self)

        self.hostname = hostname
        self.port = port
        self.running = False
        self.streaming = False
        #self.s = s
        #self.payload_size = payload_size

    def run(self):

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        self.s.bind((self.hostname, self.port))
        print('Socket bind complete')

        #self.payload_size = struct.calcsize("Q")

        self.s.listen(10)
        print('Socket now listening')

        self.running = True

        while self.running:

            print('Start listening for connections...')

            conn, addr = self.s.accept()
            print("New connection accepted.")

            while True:
                data = conn.recv(1024)
                #print(data.decode())
                if data:
                    if data.decode()=='left':
                        print('left')
                else:
                    break
        print('Exit thread.')

    def stop(self):
        self.running = False

    def sendmessage(self,message):
        outdata = str(message)
        self.s.sendall(outdata.encode())