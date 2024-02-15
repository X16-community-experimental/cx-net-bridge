import pyserial
import socket
import select

#
# Transport is the abstract class for talking to the serial or TCP ports.
#
class Transport():
    READ_ALL = -1
    READ_LINE = -2
    
    def __init__(self) -> None:
        self.type_name = "transport"
        self.read_buffer = bytearray()
        self.write_buffer = bytearray()

    def read() -> bytes:
        return None

    def write() -> bytes:
        pass

# 
# test port
#
# Just dumps some ANSI and PETSCII data for testing purposes
#
class TestPort(Transport):
    def __init__(self) -> None:
        super().__init__()
        self.type_name = "test"

# serial port
class SerialPort(Transport):
    def __init__(self) -> None:
        super().__init__()
        self.type_name = "serial"

# TCP network port
class TcpPort(Transport):
    def __init__(self) -> None:
        super().__init__()
        self.type_name = "tcp"

# The internal command processor (for AT commands)
class CommandPort(Transport):
    def __init__(self) -> None:
        super().__init__()
        self.type_name = "command"

# Host Mode port
class HostPort(Transport):
    def __init__(self) -> None:
        super().__init__()
        self.type_name = "host"

