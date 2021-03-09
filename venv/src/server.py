import threading
import socket
import sys
import random
import time
import argparse

cmdParser = argparse.ArgumentParser(description="This script takes in one argument,"
                                                " namely the port that will be used to define the"
                                                " server socket")

cmdParser.add_argument("-port", help="The provided port number is used to define the socket "
                                     "to be binded to.")

arguments = cmdParser.parse_args();
port = int(arguments.port);

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('0.0.0.0', port))

serverSocket.listen()

connectionList = []; # The list of all connected clients.

def end():
    serverSocket.close()

  # This class is used to let the server socket communicate with clients separately. Since each
  # thread is separate. Each TCP connection is isolated from eachother.
class connection(threading.Thread):

    def __init__(self, threadNumber, clientSocket, clientAddress):
        self.thread = threading.Thread.__init__(self)
        self.threadNumber = threadNumber
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.stillConnected = True; # used to track whether client is still connected

    def run(self):
        print(f"\nConnection {self.threadNumber}: Successful connection with {self.clientAddress} established.")

        while (self.stillConnected):
            message = "";
            try:
              message = self.clientSocket.recv(1024).decode() # .recv() is also used to track whether
                                                              # the client is still connected.
            except:
              print(f"Client at connection {self.threadNumber} is no longer connected."
                    f" Removing client connection from list.")
              self.stillConnected = False;
              self.removeSelf()

            if (message != ""):
                print(message)
                relay(self, message)
            else:
                self.stillConnected = False;

    def newSuggestion(self, text):

        if (self.stillConnected):   #does not send unless client is still connected.
           self.clientSocket.send(text.encode())
        else:   # Removes self from connectionList if server no longer connected to client.
            print(f"Client at connection {self.threadNumber} is no longer connected."
                  f" Removing client connection from list.")
            self.removeSelf()

    def removeSelf(self):
        removeFromList(self)

def relay(conn, msg):
    for c in connectionList:
        if (c != conn):
           c.clientSocket.send(msg.encode());

  # This class manages connections. It allows a client to connect to the server socket regardless
  # of what the server socket is doing with other clients.
class connector(threading.Thread):
    def __init__(self, connectionList):
        self.thread = threading.Thread.__init__(self)
        self.connectionList = connectionList

    def run(self):

        while True:

            clientSocket, address = serverSocket.accept()

            newConnection = connection(len(connectionList), clientSocket, address)

            connectionList.append(newConnection)
            connectionList[len(connectionList) - 1].start()

    def discard(self, disconnectedC):
        self.connectionList.remove(disconnectedC)
        print(f"Connection {disconnectedC.threadNumber} was successfully removed from connectionList.")

connector = connector(connectionList)
connector.daemon = True;
connector.start()

def removeFromList(disconnectedClient):
    connector.discard(disconnectedClient)

 # Server updates suggestion at even intervals.
verb = "";
for counter in range(10):
    time.sleep(12)
    verb = random.choice(["cook", "eat", "sleep", "study", "read", "cry", "think", "meet", "overthrow", "play", "work"])
    suggestion = "\nHost: How about {}?".format(verb + "ing")
    print(suggestion)
    for conn in connectionList:
        conn.newSuggestion(suggestion)



 # Communication ends on server timout.
print("Closing session.")
sys.exit()