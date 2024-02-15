#
# host_app.py
#
# Host mode/mini BBS file server
# 

import transport

class HostApp(transport.Transport):
    def __init__(self) -> None:
        super().__init__()
        self.name = "host"
    
    # 
    # dequeue data from read buffer and send it to the terminal
    # set num=1 to read one byte
    #     num=-1 to read the entire buffer
    #     
    #
    def read(self, num = 1):
        if len(self.read_buffer) > 0:
            if num == transport.Transport.READ_ALL:
                return self.read_buffer
            elif num == transport.Transport.READ_LINE:
                b = self.read_buffer
