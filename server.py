'''  
  STUDENT NAME AND ID: JOSIAH BAJNATH - 816027332 
  STUDENT NAME AND ID: ISIS GONSALVES - 816026980   
                              
  COURSE NAME: COMP 2602 - Computer Networks 
  
  SEMESTER: 1 
                    
  DATE: 11/10/2021
                                         
  This module will listen for client socket connection. 
  The client will be allowed to enter various commands such as: 
  PUT, CREATE, LIST, SHOW, DELETE, SEARCH, WORDCOUNT and EXIT
  
  Each member contributed equally as this assignment was completed via Discord. 
'''

from socket import *
import os
from os import listdir
from os.path import isfile, join
from os.path import exists as file_exists

# random port number
serverPort = 12009

# create TCP welcoming socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))

# server begins listening for incoming TCP requests
serverSocket.listen(1)

# output to console that server is listening
print("Ready to receive file from client... ")


def search(filename, key):
    data = filename.read()  # read the data file received from the client
    if key in data:  # check to see if key is found
        outPut = ("found in file")
        connectionSocket.send(bytes(outPut, 'UTF-8'))  # send results to client
    else:
        outPut = ("not found in file")
        connectionSocket.send(bytes(outPut, 'UTF-8'))  # send results to client
    filename.close()

def wordcount(filename):
    data = filename.read()  # read the data file received from the client
    numWords = data.split()  # split the string
    size = len(numWords)  # find the length
    # print(size)
    connectionSocket.send((str(size).encode('UTF-8')))  # send results to client
    filename.close()

def delete(filename):
    if os.path.exists(toDelete):  # check to see if the file exists
        os.remove(toDelete)
        outPut = ("deleted...")
        connectionSocket.send(bytes(outPut, 'UTF-8'))  # send results to client
    else:
        outPut = ("not found...")
        connectionSocket.send(bytes(outPut, 'UTF-8'))  # send results to client


def show(filename):
    with open(filename) as f:  # open the file
        data = f.read()  # read the data file received from the client
        filename = str(filename, 'UTF-8')
        print("File Read:", filename)
        # send the contents of the file to client
        connectionSocket.send(bytes(data, 'UTF-8'))
        print("File contents sent to client:", data)

    f.close()


def list():
    print("Executing list command")
    files = os.listdir('.')  # list files in the current folder
    # convert to string and send to client
    connectionSocket.send((str(files).encode('UTF-8')))
    # print(files)


def createFile(filename):
    f = open(filename, "w+")
    # this calls the file and opens it of that name if the file does not exist, the "w+" writes the file and creates it.
    fileContext = connectionSocket.recv(1024)
    fileContext = fileContext.decode("UTF-8")
    fileContext = str(fileContext)
    f.write(fileContext)
    print("File is created")
    
    f.close()


# server waits for incoming requests; new socket created on return
connectionSocket, addr = serverSocket.accept()
print(addr, " has connected")

# receive command and convert to string

exitCommand=False;
#print(exitCommand) 

while (exitCommand==False):
    
    command = connectionSocket.recv(1024)
    command = str(command, 'UTF-8')

    if(command == "SEARCH"):

        # print(command)
        print("\nExecuting SEARCH command...")
        location = connectionSocket.recv(1024)  # receive location
        if(os.path.exists(location)):

            # if file exists, open it and receive a key to search for
            # search function is called

            existing = ("yes")
            # print(existing)
            connectionSocket.send(bytes(existing, 'UTF-8'))

            file = open(location, "r")
            print("File found")

            key = connectionSocket.recv(1024)
            key = str(key, 'UTF-8')
            print("Word to search for: ", key)
            search(file, key)
        else:
            existing = ("no")
            # print(existing)
            connectionSocket.send(bytes(existing, 'UTF-8'))

    elif(command == "WORDCOUNT"):

        print("\nExecuting WORDCOUNT command...")
        location = connectionSocket.recv(1024)  # receive location

        if(os.path.exists(location)):

            # if file exists, open it and wordcount function is called
            existing = ("yes")
            connectionSocket.send(bytes(existing, 'UTF-8'))

            file = open(location, "r")
            print("File found")

            wordcount(file)
        else:
            existing = ("no")
            connectionSocket.send(bytes(existing, 'UTF-8'))

    elif(command == "DELETE"):

        print("\nExecuting DELETE command...")
        toDelete = connectionSocket.recv(1024)  # receive file to delete
        delete(toDelete)

    elif(command == "SHOW"):

        print("\nExecuting SHOW command...")
        file = connectionSocket.recv(1024)  # receive location

        if(os.path.exists(file)):

            # if file exists, open it and show function is called
            existing = ("yes")
            connectionSocket.send(bytes(existing, 'UTF-8'))
            show(file)
        else:
            existing = ("no")
            connectionSocket.send(bytes(existing, 'UTF-8'))

    elif(command == "LIST"):

        print("\nExecuting LIST command...")
        list()

    elif (command == "CREATE"):

        print("\nExecuting CREATE command...")
        filename = connectionSocket.recv(1024)
        createFile(filename)

    elif (command == "PUT"):

        print("\nExecuting PUT command...")
        filename = connectionSocket.recv(1024)

        # code to receive whether file exists in server folder and converts it to string
        existing = connectionSocket.recv(1024)
        existing = existing.decode("utf-8")
        existing = str(existing)

        # if the file does exist
        if(existing == "yes"):

            f = open(filename, "w")
            print("Server received file: ", filename)

            file = connectionSocket.recv(1024)
            file = file.decode("utf-8")
            file = str(file)

            f.write(file)
            f.close()

            f = open(filename, "r")
            print("Contents: ", f.read())
            f.close()
        else:
            print("The file:", filename, "not found")
            
    elif(command == "EXIT"):
        print("User selected EXIT...Program Terminated")
        exitCommand = True


connectionSocket.close()



