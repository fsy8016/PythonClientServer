import socket
import sys
import threading
import os
import os.path
from os import path

#initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the socket to some port
Address = ('localhost', 2035)
sock.bind(Address)
def user():
    #print "USER THREAD"
    while True:
        prompt = '> '
        command = raw_input(prompt)
        
        if command == 'list':
            print "List of Files:"
            path = os.getcwd()
            dirs = os.listdir( path )
            
                # This would print all the files and directories
            for file in dirs:
                print file
        if command == 'quit':
            os._exit(1)
            break
        else:
            print "Invalid Command!"
def worker(conn,client_address):
    #print "WORKER THREAD"
    login = 0
    try:
        print >>sys.stderr, 'CONNECTION MADE WITH', client_address
        
    
        #while the data is made and data has been received
        data = conn.recv(16)
        if data:
            print >>sys.stderr, 'RECEIVED CREDENTIALS "%s"' % data
            with open("stuff.txt","r") as f:
                line = f.readlines()
                #print >>sys.stderr, 'array: "%s"' % line 
                for element in line:
                    element = element.rstrip('\n')
                    #print >>sys.stderr, 'element: "%s"' % element 
                    #print >>sys.stderr, 'Credentials: "%s"' % data
                    if data == element:
                        #print >>sys.stderr, 'MATCH FOUND!'
                        print "CONNECTION ACCEPTED!"
                        conn.sendall('CONNECTION ACCEPTED')
                        login = 1
                        while True:
                            command = conn.recv(100)
                            keyword = command.split(' ', 1)[0]
                            filename = command.split(' ', 1)[1]
                                
                            if keyword == 'upload':
                                contents = conn.recv(100)
                                uploadfile = open(filename, "w")
                                uploadfile.write(contents)
                                uploadfile.close()
                            if keyword == 'download':
                                #print "DOWNLOAD"
                                if os.path.isfile(filename):
                                    newfile = open(filename, 'r')
                                    contents = newfile.read()
                                    conn.sendall(contents)
                                else:
                                    conn.sendall('ERROR')
        if login == 0:
            conn.sendall('CONNECTION FAILED')
            conn.close()

                        
                

        
    finally:
        conn.close()
threads1 = []
u = threading.Thread(target=user)
threads1.append(u)
u.start()
#put it into a loop to listen for connections
sock.listen(1)


threads = []

while True:
    #accept a connection and bind the connection data and the client address to a variable
    conn, client_address = sock.accept()
    
    t = threading.Thread(target=worker, args=(conn,client_address,))
    threads.append(t)
    t.start()