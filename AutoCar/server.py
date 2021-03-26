import socket, threading
ADDRESS = "127.0.0.1" #temporary until on cloud
PORT = 8001

class  cThread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
    def run(self):

        while True:
            resp = self.socket.recv(2048)
            msg = resp.decode()
            #parse msg
            print("from client", msg)
            self.socket.send(bytes(msg, 'UTF-8'))
        #on disconnect

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ADDRESS, PORT))
    while True:
        server.listen(1)
        cSocket, cAddress = server.accept()
        cThread(cSocket).start()
        



if __name__ == '__main__':
    main()