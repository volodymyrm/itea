import socket

sock = socket.socket()
sock.bind(('localhost', 9000))
sock.listen(1)
client, address = sock.accept()
while True:
    size = 1024
    try:
        data = client.recv(size)
        if data:
            with open('socket.log', 'a') as file:
                print (client, address)
                file.write(str(data.decode('utf-8')+'\n'))
    except socket.error:
        client.close()