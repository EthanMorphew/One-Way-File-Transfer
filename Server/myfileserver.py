# NET 4005 Assignment 1 
# By: Ethan Morphew
# ID: 101182095
# 2024-09-20
# File Server

import socket
import concurrent.futures
import os
import threading

port = 50555
threadPool = concurrent.futures.ThreadPoolExecutor(max_workers = 10)
varLock = threading.Lock()
printLock = threading.Lock()

requestNumber = 0
successfulRequests = 0

#Function called by Thread Pool used to handle incoming requests
def requestHandler(clientSocket, clientAddress, requestNumber):
    global successfulRequests
    try:
        #Receive File Name
        fileName = clientSocket.recv(1024).decode('utf-8')

        printLock.acquire()
        print("REQ " + str(requestNumber) + ": " "File " + fileName + " Requested from " + str(clientAddress[0]))
        printLock.release()

        #Check if file exists, send control message
        if os.path.isfile(fileName):

            varLock.acquire()
            successfulRequests += 1
            clientSocket.send((str(os.path.getsize(fileName) + 1) + "," + str(requestNumber) + "," + str(successfulRequests)).encode('utf-8'))#ensures empty files have size of at least 1 bytes
            varLock.release()

            #Wait until client confirms its ready to receive the file with CONTROL Message
            clientFile = open('./' + fileName, 'rb')

            printLock.acquire()
            print("REQ " + str(requestNumber) + ": " + "Successful")
            printLock.release()

            #Send file 1024 bytes at a time until whole file is sent, then send CONTROL Message
            fileData = clientFile.read()
            clientSocket.sendall(fileData)

            printLock.acquire()
            varLock.acquire()
            print("REQ " + str(requestNumber) + ": " + "Total successful requests so far = " + str(successfulRequests))
            varLock.release()
            print("REQ " + str(requestNumber) + ": " + "File Transfer Complete")
            printLock.release()
        else:
            clientSocket.send(('0' + "," + str(requestNumber) + "," + str(successfulRequests)).encode('utf-8'))#Send size 0 only if file does not exist
            printLock.acquire()
            varLock.acquire()
            print("REQ " + str(requestNumber) + ": " + "Total successful requests so far = " + str(successfulRequests))
            varLock.release()
            print("REQ " + str(requestNumber) + ": " + "Not Successful")
            printLock.release()

        clientSocket.shutdown(2)
        clientSocket.close()
    except socket.error:
        printLock.acquire()
        print("REQ " + str(requestNumber) + ": " "An error occured with client at " + str(clientAddress[0]))
        printLock.release()
        clientSocket.close()
    return

#Server Startup
try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('',port))
    print("Server is bound to port", port)
    serverSocket.listen()
    print("Server is listening")
except socket.error as error:
    print("An Error occured during startup!")
    exit()
#Server main loop, incoming connections are passed to the ThreadpoolExecutor which handles threading and queuing
while True:
    clientSocket, clientAddress = serverSocket.accept()
    requestNumber += 1
    threadPool.submit(requestHandler(clientSocket, clientAddress, requestNumber))