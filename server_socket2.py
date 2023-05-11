import socket
import threading

HEADER = 64
PORT = 100
SERVER = '192.168.210.61'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr, mac):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg == '92-32-4B-41-57-81':
                print(f"CONEXION ESTABLECIDA, LA MAC {msg} COINCIDE.\n")
                mac = msg

            if mac == "0":
                print(f"CONEXION FALLIDA, LA MAC {msg} NO COINCIDE.")
                connected = False
                conn.close()
            elif mac == '92-32-4B-41-57-81':
                print(f"[{addr}] {msg}")
                conn.send("Msg received".encode(FORMAT))

    conn.close()


def start():
    mac = "0"
    server.listen()
    print(f"[LISTEN] Server is listening on address {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, mac))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is running.....")
start()

