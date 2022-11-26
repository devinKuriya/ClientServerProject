#Devin Kuriya 40111954
#Server Code
#I certify that this is my own submission and meets Gina Cody School's expectation of Originality

from http import client
from multiprocessing.connection import wait
import os
import base64
import time
from socket import *

def fileexists_check(path):
        #print("In function")
        if os.path.isfile(path)!=True:
            return False
        else:
            return True

def checkdebug(input):#Used to check if messages should be printed
    if(input==str(0)):
        return False#In standard mode 
    else:
        return True#Debug Mode

def getopcode(message):
    opcode=message[0:3]
    return opcode

def getfilelength(message):
    length=message[3:8]
    return length

def getfilename(message):
    limit=getfilelength(message)
    #print("Limit:"+str(int(limit,2)))
    filename=message[8:8+int(limit,2)]
    return filename

def getnewname_change(message,oldlength):
    shift=int(oldname_length,2)+8
    #print(message)
    new_length=message[shift:shift+5]
    filename=message[5+shift:5+shift+int(new_length,2)]
    #print("Change:"+filename)
    return filename

#Response Messages
pc_resposne_message=0b000#Response message for good Put and Change messages

serverPort=12000
serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
space=" "
print('Server ready to receive on port:'+str(serverPort))
debug_standard_input=input('Debug Mode(1) or Standard Mode(0): \n')
while True:
    message,clientAddress=serverSocket.recvfrom(2048)
    mM=message.decode()
    
    #HELP
    if getopcode(mM)==str(format(0b11,"03b")):
        print("Help")
        responsemessage=f"{str(0b110)}{space}{'Commands are: bye change get help put'}"
        if(checkdebug(debug_standard_input)):
            print(responsemessage)
        serverSocket.sendto(responsemessage.encode(),clientAddress)
    
    #PUT
    
    elif getopcode(mM)==str(format(0b0,"03b")):
       
        print("Put")
        #Code to store file
        filename=getfilename(mM)
        with open("ServerFiles/"+filename, 'w') as f:
            data = serverSocket.recv(4096)
            print(filename)
            f.write(data.decode())
            print(f.name+" has been downloaded successfully.")
        if(checkdebug(debug_standard_input)):
            print(str(format(0b000,"08b")))
        serverSocket.sendto(str(0b000).encode(),clientAddress)
        
    #GET
    elif getopcode(mM)==str(format(0b001,"03b")):
        print("get") 
        #Code to send file
        filename=getfilename(mM)
        result=fileexists_check("ServerFiles/"+filename)
        if(result==True):
            f= open("ServerFiles/"+filename,'rb')
            l = f.read(1024)
            
            opcode=format(0b1,"03b")
            filename_length=format(len(filename),"05b")
            file_size=format(os.path.getsize("ServerFiles/"+filename),"04b")
            responsemessage=f"{str(opcode)}{str(filename_length)}{str(filename)}{str(file_size)}"
            if(checkdebug(debug_standard_input)):
                print(responsemessage)
            serverSocket.sendto(responsemessage.encode(),clientAddress)
           
            while (l):
                serverSocket.sendto(l,clientAddress)
                print('Sending...')
                l = f.read(1024)
            f.close()
           
            print('Done sending')
        else:
            if(checkdebug(debug_standard_input)):
                print(str(format(0b010,"03b")+"00000"))
            serverSocket.sendto(str(0b010).encode(),clientAddress)
    
    
    #CHANGE
    elif getopcode(mM)==str(format(0b10,"03b")):
        print("Change") 
        #Code to change file name
        oldname=getfilename(mM)
        oldname_length=getfilelength(mM)
        newname=getnewname_change(mM,oldname_length)

        if(fileexists_check("ServerFiles/"+oldname)!=True):
            if(checkdebug(debug_standard_input)):
                print(str(format(0b010,"03b")+"00000"))
            serverSocket.sendto(str(0b010).encode(),clientAddress)
        else:
            os.rename("ServerFiles/"+oldname,"ServerFiles/"+newname)
            #Check if rename happened properly
            if(fileexists_check("ServerFiles/"+newname!=True)):
                if(checkdebug(debug_standard_input)):
                    print(str(format(0b101,"03b")+"00000"))
                serverSocket.sendto(str(0b101).encode(),clientAddress)
            else:
                if(checkdebug(debug_standard_input)):
                    print(str(format(pc_resposne_message,"03b")+"00000"))
                    #print(str(pc_resposne_message))
                serverSocket.sendto(str(pc_resposne_message).encode(),clientAddress)

    #Not a valid command
    else:
        print("Not a valid command")
        if(checkdebug(debug_standard_input)):
            print(str(format(0b011,"03b")+"00000"))
        serverSocket.sendto(str(0b011).encode(),clientAddress)
    
    
           
        
   
    
    
    

