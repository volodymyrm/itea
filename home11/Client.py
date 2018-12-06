import socket

sock = socket.socket()
sock.connect(('localhost', 9000))
data = ''
while True:
    data = input("message: ")
    if data != '':
        sock.send(bytes(data, 'utf-8'))
    else:
        sock.close()
        break