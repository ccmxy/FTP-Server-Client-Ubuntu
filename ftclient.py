
import sys
import socket

#Arguments are global variables declared in main()
#They are be validated on the server side
def getArgs():
    host, port_p, command = (sys.argv[1]), (sys.argv[2]), (sys.argv[3])
    if (command == "-g"):
         file_name, port_q = (sys.argv[4]), (sys.argv[5])
    else:
         file_name, port_q = "", (sys.argv[4])
    return host, int(port_p), command, int(port_q), file_name

#runConnectionP is run immidiately after getArgs in main()
#It establishes the control connection with the server,
# sends the server the command and data port number specified in the
# command line args, and also establishes the data connection.
# It then calls runConnectionQ() to communicate over the data
# connection. Once runConnectionQ() is completed it closes the
# control connection.
def runConnectionP():
    controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    #connect to server:
    try:
        controlSocket.connect((host, port_p))
    except Exception as e:
        print "Error connecting to control socket!"
        print e
        sys.exit(1)
    print "Connection p established!"
    #send given data port to the server over control:
    print "Sending data port over connection P..."
    controlSocket.sendall(str(port_q))
    #send command over control:
    print "Sending command over connection P..."
    controlSocket.sendall(command + "\n")
    if (command == "-g"):
        controlSocket.sendall(file_name)

    inData = controlSocket.recv(500)
    if(inData == "ACK"):
        print "Server gave OK to sent in command and port."

    #Else if  error message  was sent...
    else:
        #Print the error
        print inData
        controlSocket.close()
        print "Control connection closed"
        sys.exit(1)

    #Create the data socket for the server to connect to:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Bind the localhost on specified port for data transfer:
    clientSocket.bind(('localhost', port_q))

    #Listen for connections...
    clientSocket.listen(5)

    #Accept incoming connection:
    dataSocket = clientSocket.accept()[0]
    print "Connection Q established!"

    ###     Function to run data connection called   ####
    runConnectionQ(dataSocket)

    #Close control connection once the runConnectionQ is done:
    try:
        controlSocket.close()
        print "Connection P Closed!"
    except Exception as e:
        print e
        sys.exit(1)

#This is where communication over the data connection happens.
# The connection was established in controlConnectionP
# and this is where either a list of directories is printed
#  or the text of a file specified in the command line args
# is received from the server and saved to a file.
def runConnectionQ(dataSocket):

    inTag = dataSocket.recv(500)
    #send ack for inTag
    dataSocket.sendall("ACK")
    #recv file name
    inData = dataSocket.recv(500)
    #send ack for file name
    dataSocket.sendall("ACK")

    # A list of file_names is being transferred.
    if inTag == "directories":
        print "ftclient: File listing on \"{0}\"".format(host, port_p)
        # Print all received file_names.
        while inTag != "DONE":
          print "  " + inData
          inTag = dataSocket.recv(500)
          #send ack for inTag
          dataSocket.sendall("ACK")
          #recv file name
          inData = dataSocket.recv(500)
          #send ack for file name
          dataSocket.sendall("ACK")

    # receive contents of file and write write
    elif inTag == "text_transfer":
        file_name = inData
        # Write received text to file.
        with open(file_name, "w") as outfile:
            inData = dataSocket.recv(500)
            outfile.write(inData)
        print "Requested file should now exist in this directory"
    elif inTag == "ERROR: ":
        # An error occurred.
        print inTag
        print inData

# Define script point of entry.
if __name__ == "__main__":
    # Provide global access to command-line arguments.
    global host
    global port_p
    global command
    global file_name
    global port_q

    host, port_p, command, port_q, file_name = getArgs()

    runConnectionP()

    sys.exit(0)
