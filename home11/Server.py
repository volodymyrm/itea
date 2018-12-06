import socket
import threading
class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                print(str(data.decode('utf-8') + '\n'))
                if data:
                    with open('data.txt', 'a') as file:
                        print (client, address)
                        file.write(str(data.decode('utf-8')+'\n'))
                else:
                    raise Exception('Client disconnected')
            except:
                client.close()
                return False


ThreadedServer('localhost', 9000).listen()