<snippet>
  <content>
# FTP Server and Client for Ubuntu

#####This is a version of [this](https://github.com/ccmxy/FTP-Server-and-Client) which works on my Ubuntu 14.04.03  Amazon EC2 server.

A file transportation and directory listing service. 
This program uses a control-connection to send commands between
the client and server, and sends data back on the port 
specified by the client.

## Installation

gcc ftserver.c -o ftserver

## Usage
Start with the server:    
 ./ftserver SERVER_PORT

Repeatedly enter any combination of these two commands on the client until there is a terminating signal (SIGINT) on the server side:

To get a file that is in the directory that the server is in and save it to the directory that the client is in:
python ftclient.py SERVER_HOST SERVER_PORT -g FILENAME DATA_PORT

With SERVER_PORT as the port that was specified in the command line when starting the server,
 and DATA_PORT as the port that the client will receive file data through.        

To get a list of all files in the server directory:
python ftclient.py SERVER_HOST SERVER_PORT -g  DATA_PORT

## Example

### In directory where ftserver is
% ./ftserver 32137

### In directory where ftclient is

#### To retreive list of all files in server directory
% python ftclient.py localhost 32137 -l 26665
	
#### For file transporation
% python ftclient.py localhost 32137 -g fileThatExistsInServerDirectory.txt 26665

#### For getting back an error message indicating file does not exist:
% python ftclient.py localhost 32137 -g fileThatDoesntExistInServerDirectory.txt 26655

#### For getting back a bad command message:
% python ftclient.py localhost 32137 -NotReallyRealCommand 26665


</content>
</snippet>

