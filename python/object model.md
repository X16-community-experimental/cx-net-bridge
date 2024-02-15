
# Object Model

The Bridge has the following main components:

* Event Loop: this reads from the local terminal and sends data to the remote
computer.


## Transport Class

Abstract class that handles all communication through the bridge.

Actions:  
* connect() Connect to a remote host using the parameters in the object.  
* open() Opens a port using the properties in the object (port, address, etc.)  
* listen() Opens a port to receive data. For TCP ports, this sets up a listener
	for incoming connections. For serial ports, this just opens the port.  
* get_transport(type:str "COMn" | "/dev/tty..." | "tcp") Returns a subclass
  based on the type name. 
  * "serial" will return a SerialPort object
  * "tcp" will ready a TCP network connection.
	
### SerialPort Classp

Inherits **Transport**
	
Connects to a serial port. Relevant properties are: baudrate, bytesize,
data_bits, parity, stopbits
	
On an RS-232 connection, there is no way for the serial port to raise and
lower the CD and RI pins, since there is no corresponding connection in a
null modem cable. However, if Modem is running on a microcontroller with
available pins, the following will happen:
	
* When Modem connects to a remote computer (BBS), the CD line will go high, and
  a CONNECT n message will be sent to the Local device. (n is the rate at which
  the modem and the terminal talk.)
* When Modem is in Listen mode, (ATA *port*), the RI line will raise for 1
  second, and RING will be sent to the local device. If Auto Answer is enabled
  (S0=1), then Modem will accept the incoming connection.

### NetPort(Transport)
	
Connects to a network server. Relevant properties are hostname, port schema,
protocol (TCP|UDP)

### CommandPort
	
read() and write() marshal commands and parameters and dispatch calls to Command
or Host objects.
	
### HostPort

read() and write() talk to the built-in Host Mode program. Use AT HOST or ATD
211 (if 211 is not overridden with a phone book entry) to start host mode. 

Host mode does *not* hang up the current connection, if there is one. This lets
you do things like enter host mode to grab a file, then exit host mode and
upload the file to a BBS. If you [Q]uit host mode, and return later, you will be
in the directory in which you left off.

If the user [Q]uits Host Mode while connected to a remote server, the sytem will
switch to Online mode. If the user [Q]uits Host Mode whle not conneted to a
remote server, the system will switch to Command Mode

The (pause)+++(pause) sequence is recognized by the main event loop, so this
always switches back to Command mode and prints an OK prompt. 


## Command Class
The Command object accepts AT commands and dispatches them to perform
various configuration or operational tasks. When in Host mode, data from
LocalPort is sent to HostPort When in online mode, data from LocalPort is
sent to RemotePort When in command mode, data read from LocalPort is sent to
CommandPort actions: write: send an AT command read: keyboard echo, returns
results of the last AT command

## FileServer

A simple file shell. List files and directories, upload, and download files.

* host_dirs: a list of directories the user can CD into. Format is
  "name":"C:\path\to\dir" this list will be shown at the top level
* file transfers will be available using standard protocols: XModem, YModem,
  ZModem, and Intel Hex dump.

## Event Loop 

* Terminal: the Transport that connects to the local terminal via a serial or
  TCP Transport object.
* Remote: The Transport that connects to the remote host. 

The event loop handles data exchange between the Local device, the Remote host,
and the Command processor. 

The loop looks something like this:

```
read from Localport 

while True:
	if HostMode: 
		write to HostPort 
		read from HostPort 
	elif Online: 
		write to RemotePort 
		read from RemotePort 
	elif Command Mode: 
		write to CommandPort 
		read from CommandPort 
	write to LocalPort
	read from LocalPort
	check for (pause)+++(pause):
		set Command Mode
	check for DTR drop:
		set mode based on S63
```
