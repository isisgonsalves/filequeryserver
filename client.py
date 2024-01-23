'''  
  STUDENT NAME AND ID: JOSIAH BAJNATH - 816027332
  STUDENT NAME AND ID: ISIS GONSALVES - 816026980   
                              
  COURSE NAME: COMP 2602 - Computer Networks 
  
  SEMESTER: 1 
                    
  DATE: 11/10/2021
                                         
  This module will listen for client socket connections. 
  The client will be allowed to enter various commands such as: 
  PUT, CREATE, LIST, SHOW, DELETE, SEARCH, WORDCOUNT and EXIT
  
  Each member contributed equally as this assignment was completed via Discord. 
'''

from socket import *
import os
from os import listdir
from os.path import isfile,join
from os.path import exists as file_exists

serverName = "Localhost"

#random port number 
serverPort = 12009

# create TCP socket on client to use for connecting to remote
# server.  Indicate the server's remote listening port
# Error in textbook?   socket(socket.AF_INET, socket.SOCK_STREAM)  Amer 4-2013 
clientSocket = socket(AF_INET, SOCK_STREAM)

# open the TCP connection
clientSocket.connect((serverName,serverPort))

print("Connected to Server...")

exitCommand=False;

while(exitCommand==False):
    
    #prompting the user for the command
    readData = input("\nEnter your command: ")
    #command input can be 1 or 2 words, the command itself and the file
    
    numWords= readData.split()   
    size= len(numWords) 

    #if the command is 1 just carry on 
    #if its 2 words, split the string into command and data(location)

    if size == 1:
        command = readData
    else:
        (command,data)=readData.split(maxsplit=1)  

    #sending the command to the server
    
    
    clientSocket.send(bytes(command, "utf-8"))


    if(command=="SEARCH"):
        
        #sending the data to the server
        clientSocket.send(bytes(data, "utf-8"))
        
        #code to receive whether file exists in server folder and converts it to string
        existing= clientSocket.recv(1024)
        existing= existing.decode("utf-8")
        existing= str(existing)
        
        #if the file does exist
        if(existing == "yes"):
            
            #promt for the key to search for and send to server socket
            response = input("Enter your word to search: ")
            clientSocket.send(bytes(response, "utf-8"))
            
            #receive if the key is found or not
            verdict= clientSocket.recv(1024)
            verdict = str(verdict, 'UTF-8')
            
            print(response, verdict)
            
        else:
            print("The file:", data, "not found")
    
    elif(command == "WORDCOUNT"):
        
        #sending the data to the server
        clientSocket.send(bytes(data, "utf-8"))
        
        #code to receive whether file exists in server folder and converts it to string
        existing= clientSocket.recv(1024)
        existing= existing.decode("utf-8")
        existing= str(existing)
        
        #if the file does exist
        if(existing == "yes"):
            
            #receive the amount of words as interger
            answer= clientSocket.recv(1024)
            answer= answer.decode("utf-8")
            answer= int(answer)
            print("Number of words in", data, ":", answer)
            
        else:
            print("The file:", data, "not found")
            
        
    elif(command == "DELETE"):
        
        #sending the data to the server 
        clientSocket.send(bytes(data, "utf-8"))
        
        #receive whether the file was removed or not found
        verdict= clientSocket.recv(1024)
        verdict = str(verdict, 'UTF-8')
        print(data, verdict)
        
    
    elif(command == "SHOW"):
        
        #sending the data to the server
        clientSocket.send(bytes(data, "utf-8"))
        print("Command Sent to Server...")
        
        #code to receive whether file exists in server folder and converts it to string
        existing= clientSocket.recv(1024)
        existing= existing.decode("utf-8")
        existing= str(existing)
        
        if(existing == "yes"):
            
            #receives the contents and converts to string
            contents= clientSocket.recv(1024)
            contents = str(contents, 'UTF-8')
            print("Contents of",data,":", contents)
        else:
            print("The file:", data, "not found")
        
        
    elif(command == "LIST"):
        
        #receiving the files in the folder the server socket is running from 
        files= clientSocket.recv(1024)
        files= files.decode("utf-8")
        files= str(files)
        print("List of files in folder:", files)
        
    elif(command== "CREATE"):
        filename= data
        clientSocket.send(bytes(filename, "utf-8"))
        fileContext= input("Enter your line of text: ")
        clientSocket.send(bytes(fileContext, "utf-8"))
        
        
        #this was from the top of the while loop with the split data
        #f = open (data, "w+") #could data could be switched with filename ? 
        #this calls the file and opens it of that name if the file does not exist, the "w+" writes the file and creates it.
        #print ("Enter your line of Text ")
        #filedata = input (": ")
        #f.write(filedata)
        
    
    elif (command == "PUT"):
        
        #sending the data to the server
        clientSocket.send(bytes(data, "utf-8"))
        
        if(os.path.exists(data)):
                
            #if file exists, open it.
            existing=("yes")
            clientSocket.send(bytes(existing, 'UTF-8'))
           
            f=open(data,"rb")
            file=f.read(1024)
            
            clientSocket.send(file) 
            print("File sent!")
            
        else:
            existing=("no")
            print("File not found")
            clientSocket.send(bytes(existing, 'UTF-8'))
    
    elif (command == "EXIT"):
        
        #sending the command to the server
        clientSocket.send(bytes(command, "utf-8"))
        exitCommand = True
        
    else: 
        print("Invalid Command")
    

#User selected exit//close sockets
print("User selected EXIT...program terminated")
clientSocket.close()
