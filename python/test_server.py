#
# test-server.py
# 
# Stand-alone program that just implements an Echo server
# Useful to test cxbridge.
#
# This module is based on a the example at
# https://realpython.com/python-sockets/#echo-client-and-server
#
# To use this module to help test your Telnet or TCP client, simply start it
# from the command line with `python3 test-server.py` or use the included shell
# or batch file
#


# https://docs.python.org/3/howto/sockets.html

import socket
import select

HOST = "127.0.0.1"  # Standard loopback interface address (localhost). 
PORT = 23  # Port to listen on (non-privileged ports are > 1023)

print("Host:",HOST)
print("Port:",PORT)

hello = bytes("Welcome to the X-Net Echo Test\r\n"\
              +"Text you type will be echoed back. Type ^Q to quit\r\n",
              "ansi")
will_echo = bytes([0XFF, 0X01])
bye = bytes("\r\nGoodbye\r\n","ansi")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
    listen_socket.bind((HOST, PORT))
    listen_socket.listen()
    conn, addr = listen_socket.accept()
    with conn:
        # conn.sendall(will_echo)
        conn.sendall(hello)
        print(f"Connected by {addr}")
        last = ""
        connected = True
        while connected:
            read_sockets, write_sockets, error_sockets =\
                    select.select([conn] , [], [], 0.01)
            
            while len(read_sockets) > 0:
                data = conn.recv(1024)
                if not data:
                    print("\nLost connection: no data")
                    break
                # echo data back
                conn.sendall(data)            

                # look for command sequence
                t = data.decode("ansi")
                print(t,end="")
                if t.find(chr(17)) >= 0:
                    print("\nDisconnect command received.")
                    conn.sendall(bye)
                    conn.shutdown(0)
                    conn.close()
                    connected = False
                    break

