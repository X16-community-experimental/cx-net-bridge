# cx-net-bridge

CX-Net Bridge is a utility to connect a physical RS-232 port to an Internet
connection. Bridge should be able to handle TCP and UDP, and it will decode
http, Telnet, and ftp traffic, converting them to simple text streams that can
be viewed on an 8-bit computer.

The planned modules are:
* Virtual Modem: Dial up Telnet BBS's like it's 1989 again. Virtual Modem will
  accept a good old fashioned ATDT command and connect to any Telnet or Raw TCP
  server.
  * Telnet and TCP will be selectable per-connection, as part of the dial
    string: `ATD telnet://bbs.domain.com` or `ATD tcp://bbs.domain.com`
  * Answer an incoming connection request with ATA.
  * Auto-answer incoming requests to run a BBS or remote access server on your
    8-bit computer.
* Network shell: Send and receive multiple TCP and UDP streams. 
  * Messages will use a simple command protocol and will identify the sending
    host and port number, allowing games and server programs to easily sort out
    who's sending what.
* Browser: retrieve and send documents via http, with an HTTPS proxy and a
  special lightweight markup language for 8-bit computers.
* File Manager: transfer files to your PC using a fast and easy file manager.


## Virtual Modem

This will connect to a serial port on your PC and allow you to "dial" online
BBSs with standard AT commands. If you are using the x16 emulator, you can start
x16-emu with `-uart tcp` to connect internally to the bridge and use the
bridge's modem emulation without the need for a serial port.

After [configuring](#modem-configuration) your virtual modem, start Bridge at
the command line by running `cxbridge.sh` (linux) or `cxbridge.cmd` (Windows).
You can also run `python3 cxbridge.py` from the command line. 

Connect to the serial port from your Commander X16 (or start the emulator with
`x16emu -uart tcp`) and start a terminal program.

Once the program is started, enter terminal mode and type `AT`. You should get
the `OK` response from the modem.

Try typing `ATD telnet://vert.synchro.net`. You should then see a BBS's login
page.

At this point, you should probably familiarize yourself with the basic [AT
commands](#at-commands) and the built-in [phone book](#phone-book).

### Modem configuration
To start, edit `bridge-ini.py` and set the serial port and baud rate to your
preferences. 

* For Windows: set a COM port number
* For Linux: Set a /dev/tty port number
* For TCP2TCP: set an IP address in the form "tcp:0.0.0.0:1023"

The port number (1023) is configurable, so you can use whichever port you
prefer.

Example Windows configuration:

```
serial_port = "COM3"
serial_bps = 115200
serial_data_bits = 8 # type:int 7 or 8
serial_parity= "n"   # type:str n, e, m, s
serial_stop_bits = 1 # type:int 1 or 2
```

Example Linux configuration:

```
serial_port = "/dev/ttys1"
serial_bps = 115200
serial_data_bits = 8 # type:int 7 or 8
serial_parity= "n"   # type:str n, e, m, s
serial_stop_bits = 1 # type:int 1 or 2
```

Example TCP2TCP configuration:

```
serial_port = "tcp:0.0.0.0:1023"
serial_bps = 115200
serial_data_bits = 8 # type:int 7 or 8
serial_parity= "n"   # type:str n, e, m, s
serial_stop_bits = 1 # type:int 1 or 2
```

### AT Commands

AT commands are based on the Zimodem firmware at
https://github.com/bozimmerman/Zimodem. While we do not support the entire
Zimodem feature set, we have attempted to keep our commands compatible with the
official Zimdoem commands, to make it easy to switch to a hardware device.

(Note that Zimodem does not have 

**ATB *rate***: Set the baud rate used by the serial port. The default is
115200. This only affects communication between the Bridge and your terminal
(ie: Commander X16).

`ATB9600` sets 9600 baud.
`ATB1200` sets 1200 baud (for Commodore 64/128 using a standard User port serial
adapter.)

**ATA** answers an incoming connection request. 

**ATD** dials an outbound connection. Use a full URI to specify the connection type,
or use "T" for Telnet. Add "P" for PETSCII and "TP" for Telnet and PETSCII.

`ATDT bbs.commanderx16.com:23` dials a BBS in Telenet mode with ASCII encoding
on the default Telnet port (23).  
`ATDPT bbs.commanderx16.com:8064` calls the Commander X16 BBS in PETSCII mode
with the Telnet protocol.  
`ATDP telnet://bbs.commanderx16.com:8080` calls the Commander X16 BBS in PETSCII
mode with the Telnet protocol.  
`ATD https://www.commanderx16.com` downloads the Commander X16 home page. If you
have the TML browser enabled, you can browse the page and follow links.

In addition, "E" enables echo mode and "X" enables Xon/Xoff flow control. P, T,
E, and X modifiers can be added in any order, but there *must* be a space
between the ATD command and the first letter of a text dialing string.

`ATD 5551212` dials a phonbeook entry. See [phone book](#phone-book) for
instructions on using the phone book

**ATO** Goes back online after switching to command mode with +++ or a DTR drop.
(O is the letter O, not the numeral Zero.)

(pause) **+++** (pause) switches to Command mode when online. A 3 second pause
is required before and after the +++ for the sequence to work.

**AT&Dn** Set DTR mode. When DTR goes from High to Low state, the modem can drop
to command mode or disconnect.

* &D0 ignores DTR 
* &D1 go to command mode
* &D2 hang up 
* &D3 hang up and reset to the startup settings

**ATS63=n** does the same thing as AT&D. This is included for compatibility with
the Zimodem ESP32 firmware. (&D is the canonical Hayes command, but Zimodem uses
&D for something else.)

**ATP** lists phone number entries.

* `ATP` : Lists all existing phonebook entries, with the format phone number
followed by ATD modifiers, followed by the host and port.  Add ? to also get
notes.  
* `ATP"[NUMBER]=[HOSTNAME]:[PORT],[NOTES]"` : Adds or Modifies an entry to the
phonebook with the given 7 digit number, host, port, and notes. Use ATDnnnnn..
to connect.  
* `ATPP"[NUMBER]=[HOSTNAME]:[PORT],[NOTES]"` : Adding a P modifier causes
connection input to be translated to PETSCII  when connected to that entry.  
* `ATPT"[NUMBER]=[HOSTNAME]:[PORT],[NOTES]"` : Adding a T modifier causes
connection input to be translated per TELNET  when connected to that entry.
* `ATPE"[NUMBER]=[HOSTNAME]:[PORT],[NOTES]"` : Adding a E modifier causes
terminal echo to be enabled when connected to that entry.
* `ATPX"[NUMBER]=[HOSTNAME]:[PORT],[NOTES]"` : Adding a X modifier causes
XON/XOFF flow control to be enabled when connected to that entry.  
* `ATP"[NUMBER]=D"` : Removes the phonebook entry with the given number.

**AT&V** lists the current configuration settings

**AT&Wn** writes a preset.  All of the AT command settings (including
phonebooks) can be saved to different preset slots. Use ATY to choose which one
is loaded at startup, and use ATZ to choose a different preset while the bridge
is running.

`AT&W1` saves your current setup to slot 1
`ATY1` defaults the modem to slot 1
`ATZ64` temporarily switches to slot 64 (maybe for your Commodore 64?)
`AT&W` saves the currently loaded slot. Does not change the slot number.

**ATYn** Set a startup preset.

**ATZn** initializes the virtual modem to its startup settings. The optional
argument loads a preset.

### Phone Book

Some terminal programs won't let you put IP addresses and URLs in their phone
book. You can get around this problem by adding entries to Bridge's internal
phone book.

So you can create phone book entries to work around this problem. For example:

`ATPP"5551212=bbs.commanderx16.com:23,Commander X16 BBS"` adds a phone book
entry for the Commander X16 BBS.

If you connect a different computer to the
bridge (say, a Commodore 64 or an Amiga 500), you could still connect to this
BBS by dialing `ATD 5551212`.

To delete a phone book entry, re-assign the phonebook number with =D, like this:

`ATP"5551212=D"` or `ATP"5551212=DELETE"`

