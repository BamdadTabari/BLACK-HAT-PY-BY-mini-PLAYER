# TCP Server
# Creating TCP servers in Python is just as easy as creating a client. You might
# want to use your own TCP server when writing command shells or crafting a
# proxy (both of which we’ll do later). Let’s start by creating a standard multi-
# threaded TCP server. Crank out the following code:

import socket
import threading
IP = '0.0.0.0'
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')
    while True:
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client,
        args=(client,))
        client_handler.start()
        
def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')
if __name__ == '__main__':
    main()