# cx-net-bridge

CX-Net Bridge is a utility to connect a physical RS-232 port to an Internet connection. Bridge should be able to handle TCP and UDP, and it will decode http, Telnet, and ftp traffic, converting them to simple text streams that can be viewed on an 8-bit computer.

The planned modules are:
* Virtual Modem: Dial up Telnet BBS's like it's 1989 again. Virtual Modem will accept a good old fashioned ATDT command and connect to any Telnet or Raw TCP server.
  * Telnet and TCP will be selectable per-connection, as part of the dial string: `ATD telnet://bbs.domain.com` or `ATD tcp://bbs.domain.com`
  * Answer an incoming connection request with ATA.
  * Auto-answer incoming requests to run a BBS or remote access server on your 8-bit computer.
* Network shell: Send and receive multiple TCP and UDP streams. 
  * Messages will use a simple command protocol and will identify the sending host and port number, allowing games and server programs to easily sort out who's sending what.
* Browser: retrieve and send documents via http, with an HTTPS proxy and a special lightweight markup language for 8-bit computers.
* File Manager: transfer files to your PC using a fast and easy file manager.



