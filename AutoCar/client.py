import socket

SERVER_ADDR = "127.0.0.1" #temporary until on cloud
PORT = 8001

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_ADDR, PORT))
    client.sendall(bytes("This is from Client",'UTF-8'))
    while True:
        resp = client.recv(2048)
        print("recieved ", resp.decode())
        msg = input()
        client.sendall(bytes(msg, 'UTF-8'))
        #needs termination 
    client.close()


if __name__ == '__main__':
    main()