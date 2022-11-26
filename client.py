#Devin Kuriya 40111954
#Client Code
#I certify that this is my own submission and meets Gina Cody School's expectation of Originality

import abc
from http import client
from pydoc import cli
from socket import *
import os
import time
#OpCodes
put_op=0b000
get_op=0b001
change_op=0b010
help_op=0b011

def fileexists_check(path):
        #print("In function")
        if os.path.isfile(path)!=True:
            return False
        else:
            return True

def resonsemessage_check(data_from_server):
    opcode=data_from_server.split()[0]
    if(str(opcode)==str(0b010)):
        print("Error:File not found on server")
    elif(str(opcode)==str(0b011)):
        print("Error:Unknown Request")
        print("Not a command, consider using the command: help")
    elif(str(opcode)==str(0b101)):
        print("Error:Response for change unsuccessful")
    elif(str(opcode)==str(0b001)):
        return True
    elif(str(opcode)==str(0b110)):
        return True
    elif(str(opcode)==str(0b000)):
        return True
   
def resonsemessage_check_get(opcode):
    if(str(opcode)==str(0b010)):
        print("Error:File not found on server")
    elif(str(opcode)==str(0b011)):
        print("Error:Unknown Request")
        print("Not a command, consider using the command: help")
    elif(str(opcode)==str(0b101)):
        print("Error:Response for change unsuccessful")
    elif(str(opcode)==format(0b1,"03b")):
        return True
    elif(str(opcode)==str(0b000)):
        return True  

def checkdebug(input):#Used to check if messages should be printed
    if(debug_standard_input==str(1)):
        return True
    else:
        return False
   
        


userInput_ServerName=input('Please input an ip address(localhost): \n')
userInput_PortNumber=input('Please input a port number(12000): \n')


serverName=userInput_ServerName
serverPort=int(userInput_PortNumber)
clientSocket=socket(AF_INET,SOCK_DGRAM)
space=" "
debug_standard_input=input('Debug Mode(1) or Standard Mode(0): \n')
#User inputs commands forever until bye command is used to break connection
while True:
    message=input('Please input a command: \n')

    #Help command
    if message.split()[0]=="help":
        debug=checkdebug(debug_standard_input)
        requestmessage=str(format(help_op,"03b"))
        if(debug==True):
            print(requestmessage)
        clientSocket.sendto(requestmessage.encode(),(serverName,serverPort))
        dataFromServer = clientSocket.recv(2048)
        result=resonsemessage_check(dataFromServer.decode())
        if result==True:
            print(dataFromServer.decode()[2:])
    
    #Get command
    elif message.split()[0]=="get":

        filename=message.split()[1]
        opcode=format(get_op,"03b")
        filename_length=format(len(filename),"05b")
        requestmessage=f"{str(opcode)}{str(filename_length)}{str(filename)}"
        if(checkdebug(debug_standard_input)):
            print(requestmessage)
        clientSocket.sendto(requestmessage.encode(),(serverName,serverPort))
        #Code for getting file from server
        responsemessage=clientSocket.recv(1024)
        opcode=responsemessage.decode()[0:3]
        result=resonsemessage_check_get(opcode)
    
        if(result==True):
            with open("ClientFiles/"+message.split()[1], 'wb') as f:
                data = clientSocket.recv(1024)
                f.write(data)
                print(filename+" has been downloaded successfully.")
        
    #Put command
    elif message.split()[0]=="put":
        #Code for putting files into server
        filename=message.split()[1]

        if(fileexists_check("ClientFiles/"+filename)):
            filename_length=format(len(filename),"05b")
            file_size=format(os.path.getsize("ClientFiles/"+filename),"04b")
            opcode=format(put_op,"03b")
            requestmessage=f"{str(opcode)}{str(filename_length)}{str(filename)}{str(file_size)}"
            if(checkdebug(debug_standard_input)):
                print(requestmessage)
            clientSocket.sendto(requestmessage.encode(),(serverName,serverPort))
            #time.sleep(1)
            f = open("ClientFiles/"+filename,'rb')
            l = f.read(1024)
            while (l):
                clientSocket.sendto(l,(serverName,serverPort))
                #print('Sent')
                l = f.read(1024)
            f.close()
            print('Done sending')
            opcode=clientSocket.recv(2048)
            result=resonsemessage_check(opcode.decode())
            if(result==True):
                print("File successfully moved to server")
        else:
            print("File does not exist")
    
    #Change command
    elif message.split()[0]=="change":
        #Code for changing file name 
        
        oldname=message.split()[1]#OldFileName
        newname=message.split()[2]#NewFileName
        
        filename_length_oldname=format(len(oldname),"05b")
        opcode=format(change_op,"03b")
        filename_length_newname=format(len(newname),"05b")

        requestmessage=f"{str(opcode)}{filename_length_oldname}{oldname}{filename_length_newname}{newname}"
        if(checkdebug(debug_standard_input)):
            print(requestmessage)
        clientSocket.sendto(requestmessage.encode(),(serverName,serverPort))
        
        
        responsemessage=clientSocket.recv(2048).decode()
        
    
        result=resonsemessage_check(responsemessage)
        if(result==True):
            print(oldname+" has been changed into "+newname)
        
    #Bye command   
    elif message.split()[0]=="bye":
        print('Session is terminated')
        break
    
    
    else:
        requestmessage=f""
        clientSocket.sendto(requestmessage.encode(),(serverName,serverPort)) 
        responsemessage=clientSocket.recv(2048).decode()
        resonsemessage_check(responsemessage)



clientSocket.close()
   

    