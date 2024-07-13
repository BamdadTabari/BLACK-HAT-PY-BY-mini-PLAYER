import socket
target_host = "www.google.com"
target_port = 80
# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# send some data
client.sendto(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n",(target_host,target_port))
# receive some data
data, addr = client.recvfrom(4096)
print(data.decode())
client.close()

# import socket

# # Create a UDP socket
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Bind the socket to a specific address and port
# server_address = ('127.0.0.1', 9999)  # Listen on all available interfaces
# server_socket.bind(server_address)

# while True:
#     print('\nWaiting to receive message')
#     data, address = server_socket.recvfrom(4096)

#     print('Received %s bytes from %s' % (len(data), address))
#     print(data)

#     if data:
#         sent = server_socket.sendto(b'Received', address)
#         print('Sent %s bytes back to %s' % (sent, address))

#         server_socket.close()
