#
# test_client.py
#
# This just connects to a port, sends some test data, and disconnects
#

# based on example at https://realpython.com/python-sockets/#echo-client-and-server

import socket
import select

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 23  # The port used by the server

print("Attempting to connect to",HOST,"on port",PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    # s.setblocking(False)

    sock.sendall(b"Hello, world")
    while True:
        read_sockets, write_sockets, error_sockets = select.select([sock] , [], [], 0.01)

        while len(read_sockets) > 0:
            data = sock.recv(1024,)
            if not data:
                print("\nLost connection")
                break
            t = data.decode("ansi")
            print(t,end="")
        
