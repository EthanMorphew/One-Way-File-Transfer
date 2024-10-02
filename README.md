This Repo was created to contain code for an assignment for a networked applications class.
It functions as an extremely simple one way file transfer protocol with a client-server architecture.

Running the myfileserver.py binds the server to port 50555 by default but you can easily modify it within the code.

Once the server is running you can make requests for files in the following format:

    fileClient.py <ip address> <port> <filename>

The protocol.txt was a requirement of the project and goes into further detail about the actual message exchange between the server and client during file transfer

under the ./Server directory you can find some example files I used for testing. 
