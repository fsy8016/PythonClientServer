import socket
import sys
import os
import os.path
from os import path

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Address = ('localhost', 2035)
sock.connect(Address)

try:
    prompt = '> '
    print "Please Enter Username and Password in the form Username,Password"
    login = raw_input(prompt)

    if login == 'quit':
        os._exit(1)


    sock.sendall(login)

    data = sock.recv(100)
    print >>sys.stderr, data
    
    #check for authentication
    if data == 'CONNECTION FAILED':
        sock.close()
    if data == 'CONNECTION ACCEPTED':
        while True:
            command = raw_input(prompt)
            keyword = command.split(' ', 1)[0]
            
            if keyword == 'upload':
                filename = command.split(' ', 1)[1]
                if os.path.isfile(filename):
                    sock.sendall(keyword+' '+filename)
                    newfile = open(filename, 'r')
                    contents = newfile.read()
                    sock.sendall(contents)
                    print "Upload Complete!\n"
                else:
                    print "Not a valid file!"
            elif keyword == 'download':
                filename = command.split(' ', 1)[1]
                sock.sendall(keyword+' '+filename)
                stuff = sock.recv(100)
                if stuff == 'ERROR':
                    print "Unknown file! Cannot download!"
                else:
                    file = open(filename, "w")
                    file.write(stuff)
                    file.close()
                    print "Download Complete!\n"
            elif keyword == 'quit':
                os._exit(1)
            elif keyword == 'list':
                
                print "List of Files:"
                path = os.getcwd()
                dirs = os.listdir( path )
        
            # This would print all the files and directories
                for file in dirs:
                    print file
            else:
                print 'Invalid command!'
        
    

finally:
    sock.close()
