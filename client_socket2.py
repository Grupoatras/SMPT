import socket
HEADER = 64
PORT = 100
SERVER = '192.168.210.61'
MAC = '92-32-4B-41-57-81'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

def send(msg):
    message=msg.encode(FORMAT)

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    send_length += b' '*(HEADER-len(send_length))

    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send(MAC)
input()
send('hello')
input()
send('asdfasdf')
input()
send(DISCONNECT_MESSAGE)


