import pyserial
import socket
import select
import transport

class Bridge():
    def __init__(self) -> None:
        self.running = True
        pass

    def start(self):
        self.read_init()
        self.event_loop()

    def event_loop(self):
        while self.running:
            pass

if __name__ == "__main__":
    bridge = Bridge()
    bridge.start()