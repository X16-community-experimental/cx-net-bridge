#
# config
# 
# Configuration items for CXNet Bridge
# 
import transport
import pyserial
import os.path
import json
import pathlib

class Config():
    config_file = "bridge.ini"
    ini_data = {}

    # defaults
    local_net_data_port = 1623
    local_net_stat_port = 1624

    local_ser_port = "COM3"
    local_ser_baudrate = 115200
    local_ser_bytesize = pyserial.EIGHTBITS
    local_ser_parity = pyserial.PARITY_NONE
    local_ser_stopbits = pyserial.STOPBITS_1
    local_ser_xonxoff = False
    local_ser_rtscts = False
    local_ser_dsrdtr = False

    remote_host = ""
    remote_port = 23

    local_ser = transport.SerialPort()
    local_tcp = transport.TcpPort()
    remote_port = transport.TcpPort()
    command_port = transport.CommandPort()
    files_port = transport.FileServerApp()

    def __init__(self) -> None:
        if os.path.exists(self.config_file):
            self.read_config(self.config_file)
            self.apply_config()

    def read_config(self):
        if not os.path.exists(self.config_file):
            return
        
        f = open(self.config_file,"r")
        section = ""
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith("["):
                section = line[1:-1]
            elif line.startswith(";"):
                pass # comment
            else:
                pos = line.find('=')
                if pos >= 0:
                    key = section + "." + line[0:pos]
                    value = line[pos+1:]
                else:
                    key = section + "." + line
                    value = ""
                self.ini_data[key] = value

    def save_config(self):
        pass