# NET 4005 Assignment 1 
# By: Ethan Morphew
# ID: 101182095
# 2024-09-20
# File Client

import socket
import sys

try:
    serverIP = sys.argv[1]
    serverPort = int(sys.argv[2])
    requestedFile = sys.argv[3]
except:
    print("Not enough arguments (fileClient.py <ip address> <port> <filename>)")
    exit()

#Connect to server
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serverSocket.connect((serverIP,serverPort))
except:
    print("Failed to connect to server.")
    exit()

#Send the requested file Name
serverSocket.send(requestedFile.encode('utf-8'))

info = serverSocket.recv(1024).decode('utf-8')
info = info.split(",")
fileSize = int(info[0])
requestNumber = info[1]
successfulRequests = info[2]

if fileSize > 0:
    print()
    print("File " + requestedFile + " found at server")
    print("Server handled " + str(requestNumber) + " requests, " + str(successfulRequests) + " were successful")
    print("Downloading file " + requestedFile)
    #Open the file to write to and send ready signal to server
    writeFile = open(requestedFile, 'wb')
    writeFile.write(serverSocket.recv(fileSize))
    #Close the file and confirm success with server
    writeFile.close() 
    print("Download complete")  
#Sever sends an ERROR control message if file does not exist 
else:
    print("File not found at server")
    print("Server handled " + str(requestNumber) + " requests, " + str(successfulRequests) + " were successful")
serverSocket.shutdown(2)
serverSocket.close()
