import socket

sock = socket.socket()

sock.connect(('localhost', 9000))
while True:
    data = bytes(input("message: "), 'utf-8')
    sock.send(data)